#!/usr/bin/env bash
# check-github-projects.sh - Query GitHub Projects V2 API for pending items
#
# This script is called by the orchestrator stop hook (tasks.py) to check
# if there are pending tasks on the GitHub Project board.
#
# Usage:
#   ./check-github-projects.sh [--project PROJECT_NUMBER]
#
# Environment Variables:
#   GITHUB_PROJECT_NUMBER - Project number (alternative to --project flag)
#   GITHUB_OWNER         - Repository owner (optional, auto-detected from git)
#   REPO_NAME            - Repository name (optional, auto-detected from git)
#
# Output (JSON):
#   {
#     "available": true|false,
#     "pending_count": N,
#     "tasks": [{"id": "...", "title": "...", "status": "...", "assignee": "..."}],
#     "error": ""
#   }
#
# Exit Codes:
#   0 - Success (JSON output on stdout)
#   1 - Error (JSON output with error field set)

set -euo pipefail

# Parse command line arguments
PROJECT_NUMBER=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_NUMBER="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Helper function to output JSON result
output_json() {
    local available="$1"
    local pending_count="$2"
    local tasks="$3"
    local error_msg="$4"

    printf '{"available":%s,"pending_count":%d,"tasks":%s,"error":"%s"}\n' \
        "$available" "$pending_count" "$tasks" "$error_msg"
}

# Helper function to output error and exit
output_error() {
    local error_msg="$1"
    output_json "false" 0 "[]" "$error_msg"
    exit 0
}

# Check if gh CLI is available
if ! command -v gh &>/dev/null; then
    output_error "gh CLI not installed"
fi

# Check if gh is authenticated
if ! gh auth status &>/dev/null; then
    output_error "gh CLI not authenticated"
fi

# Determine project number from arguments, env var, or config file
if [[ -z "$PROJECT_NUMBER" ]]; then
    PROJECT_NUMBER="${GITHUB_PROJECT_NUMBER:-}"
fi

# Try to read from .github/project.json if still not set
if [[ -z "$PROJECT_NUMBER" ]]; then
    PROJECT_CONFIG=".github/project.json"
    if [[ -f "$PROJECT_CONFIG" ]]; then
        PROJECT_NUMBER=$(jq -r '.project_number // .number // empty' "$PROJECT_CONFIG" 2>/dev/null || true)
    fi
fi

# If still no project number, check CLAUDE_PROJECT_DIR
if [[ -z "$PROJECT_NUMBER" && -n "${CLAUDE_PROJECT_DIR:-}" ]]; then
    PROJECT_CONFIG="${CLAUDE_PROJECT_DIR}/.github/project.json"
    if [[ -f "$PROJECT_CONFIG" ]]; then
        PROJECT_NUMBER=$(jq -r '.project_number // .number // empty' "$PROJECT_CONFIG" 2>/dev/null || true)
    fi
fi

if [[ -z "$PROJECT_NUMBER" ]]; then
    output_error "No project configured (set GITHUB_PROJECT_NUMBER or create .github/project.json)"
fi

# Determine repository owner
OWNER="${GITHUB_OWNER:-}"
if [[ -z "$OWNER" ]]; then
    # Try to get from git remote
    OWNER=$(gh repo view --json owner -q '.owner.login' 2>/dev/null || true)
fi

if [[ -z "$OWNER" ]]; then
    output_error "Cannot determine repository owner"
fi

# GraphQL query to fetch project items with pending statuses
# Statuses to check: "In Progress", "In Review", "Blocked"
QUERY='
query($owner: String!, $number: Int!) {
  user(login: $owner) {
    projectV2(number: $number) {
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              assignees(first: 1) {
                nodes {
                  login
                }
              }
            }
            ... on DraftIssue {
              title
            }
            ... on PullRequest {
              title
              number
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
'

# Also try organization query (in case owner is an org)
ORG_QUERY='
query($owner: String!, $number: Int!) {
  organization(login: $owner) {
    projectV2(number: $number) {
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              assignees(first: 1) {
                nodes {
                  login
                }
              }
            }
            ... on DraftIssue {
              title
            }
            ... on PullRequest {
              title
              number
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
'

# Execute GraphQL query for user project
RESULT=$(gh api graphql -f query="$QUERY" -F owner="$OWNER" -F number="$PROJECT_NUMBER" 2>/dev/null || true)

# Check if we got a valid result or need to try org query
if [[ -z "$RESULT" ]] || echo "$RESULT" | jq -e '.data.user.projectV2 == null' &>/dev/null; then
    # Try organization query
    RESULT=$(gh api graphql -f query="$ORG_QUERY" -F owner="$OWNER" -F number="$PROJECT_NUMBER" 2>/dev/null || true)

    if [[ -z "$RESULT" ]]; then
        output_error "Failed to query GitHub Projects API"
    fi

    # Extract items from org result
    ITEMS=$(echo "$RESULT" | jq '.data.organization.projectV2.items.nodes // []')
else
    # Extract items from user result
    ITEMS=$(echo "$RESULT" | jq '.data.user.projectV2.items.nodes // []')
fi

if [[ "$ITEMS" == "null" ]] || [[ -z "$ITEMS" ]]; then
    output_error "Project not found or no access"
fi

# Filter items by status (In Progress, In Review, Blocked)
# and format output
PENDING_TASKS=$(echo "$ITEMS" | jq -c '
  [.[] |
    # Extract status from field values
    . as $item |
    ($item.fieldValues.nodes[] |
      select(.field.name == "Status") | .name
    ) as $status |

    # Filter for pending statuses
    select($status == "In Progress" or $status == "In Review" or $status == "Blocked") |

    # Extract title and assignee
    {
      id: $item.id,
      title: ($item.content.title // "Draft Issue"),
      status: $status,
      assignee: (($item.content.assignees.nodes[0].login) // "unassigned")
    }
  ]
')

# Handle case where jq filter returns nothing
if [[ -z "$PENDING_TASKS" ]] || [[ "$PENDING_TASKS" == "null" ]]; then
    PENDING_TASKS="[]"
fi

# Count pending tasks
PENDING_COUNT=$(echo "$PENDING_TASKS" | jq 'length')

# Limit to first 5 tasks for the output
SAMPLE_TASKS=$(echo "$PENDING_TASKS" | jq -c '.[0:5]')

# Output successful result
output_json "true" "$PENDING_COUNT" "$SAMPLE_TASKS" ""
