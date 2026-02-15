#!/usr/bin/env bash
# gh-project-add-columns.sh - Safely add columns to a GitHub Project V2 Status field
#
# This script SAFELY adds new columns to an existing GitHub Project V2
# by preserving all existing option IDs. This is critical because the
# updateProjectV2Field GraphQL mutation REPLACES all options — if existing
# option IDs are not preserved, items lose their column assignments.
#
# Usage:
#   ./gh-project-add-columns.sh --project <number> --field "Status" --add "Column Name" [--add "Another"]
#
# Options:
#   --project <number>   GitHub Project number (required)
#   --field <name>       Field name to modify (default: "Status")
#   --add <name>         Column name to add (can be repeated)
#   --owner <name>       GitHub owner/org (default: from GITHUB_OWNER env or "Emasoft")
#   --dry-run            Show what would be done without making changes
#
# Environment Variables:
#   GITHUB_OWNER - Repository owner (default: "Emasoft")
#
# Exit Codes:
#   0 - Success
#   1 - Error (missing arguments, API failure, verification failed)

set -euo pipefail

# Defaults
OWNER="${GITHUB_OWNER:-Emasoft}"
FIELD_NAME="Status"
PROJECT_NUMBER=""
NEW_COLUMNS=()
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_NUMBER="$2"
            shift 2
            ;;
        --field)
            FIELD_NAME="$2"
            shift 2
            ;;
        --add)
            NEW_COLUMNS+=("$2")
            shift 2
            ;;
        --owner)
            OWNER="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            head -25 "$0" | tail -20
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Validate arguments
if [[ -z "$PROJECT_NUMBER" ]]; then
    echo "ERROR: --project <number> is required" >&2
    exit 1
fi

if [[ ${#NEW_COLUMNS[@]} -eq 0 ]]; then
    echo "ERROR: At least one --add <column-name> is required" >&2
    exit 1
fi

# Pre-flight check: verify gh auth has project scopes
if ! gh auth status 2>&1 | grep -q "project"; then
    echo "ERROR: gh auth is missing 'project' scope." >&2
    echo "A human must run: gh auth refresh -h github.com -s project,read:project" >&2
    exit 1
fi

echo "Querying project #${PROJECT_NUMBER} field '${FIELD_NAME}'..."

# Step 1: Query existing field options with their IDs
FIELD_DATA=$(gh api graphql -f query='
  query($owner: String!, $number: Int!) {
    user(login: $owner) {
      projectV2(number: $number) {
        id
        fields(first: 20) {
          nodes {
            ... on ProjectV2SingleSelectField {
              id
              name
              options {
                id
                name
              }
            }
          }
        }
      }
    }
  }
' -f owner="$OWNER" -F number="$PROJECT_NUMBER" 2>&1)

# Check for errors
if echo "$FIELD_DATA" | jq -e '.errors' > /dev/null 2>&1; then
    echo "ERROR: GraphQL query failed:" >&2
    echo "$FIELD_DATA" | jq '.errors' >&2
    exit 1
fi

# Extract the field info
FIELD_JSON=$(echo "$FIELD_DATA" | jq -r --arg fname "$FIELD_NAME" \
    '.data.user.projectV2.fields.nodes[] | select(.name == $fname and .options)')

if [[ -z "$FIELD_JSON" || "$FIELD_JSON" == "null" ]]; then
    echo "ERROR: Field '${FIELD_NAME}' not found or is not a single-select field" >&2
    exit 1
fi

FIELD_ID=$(echo "$FIELD_JSON" | jq -r '.id')
EXISTING_OPTIONS=$(echo "$FIELD_JSON" | jq -c '.options')
EXISTING_COUNT=$(echo "$EXISTING_OPTIONS" | jq 'length')

echo "Found field '${FIELD_NAME}' (ID: ${FIELD_ID}) with ${EXISTING_COUNT} existing columns:"
echo "$EXISTING_OPTIONS" | jq -r '.[].name' | while read -r name; do
    echo "  - $name"
done

# Step 2: Check for duplicates and build new options array
SKIPPED=()
TO_ADD=()

for new_col in "${NEW_COLUMNS[@]}"; do
    if echo "$EXISTING_OPTIONS" | jq -e --arg name "$new_col" '.[] | select(.name == $name)' > /dev/null 2>&1; then
        SKIPPED+=("$new_col")
    else
        TO_ADD+=("$new_col")
    fi
done

if [[ ${#SKIPPED[@]} -gt 0 ]]; then
    echo ""
    echo "Skipping (already exist):"
    for s in "${SKIPPED[@]}"; do
        echo "  - $s"
    done
fi

if [[ ${#TO_ADD[@]} -eq 0 ]]; then
    echo ""
    echo "All requested columns already exist. Nothing to do."
    exit 0
fi

echo ""
echo "Adding new columns:"
for a in "${TO_ADD[@]}"; do
    echo "  + $a"
done

# Step 3: Build the complete options array (existing with IDs + new without IDs)
# Start with existing options (preserving their IDs)
OPTIONS_JSON=$(echo "$EXISTING_OPTIONS" | jq '[.[] | {id: .id, name: .name}]')

# Append new options (without IDs — GitHub will generate them)
for new_col in "${TO_ADD[@]}"; do
    OPTIONS_JSON=$(echo "$OPTIONS_JSON" | jq --arg name "$new_col" '. + [{"name": $name}]')
done

TOTAL_COUNT=$(echo "$OPTIONS_JSON" | jq 'length')
echo ""
echo "Total columns after update: ${TOTAL_COUNT}"

if [[ "$DRY_RUN" == "true" ]]; then
    echo ""
    echo "[DRY RUN] Would send mutation with these options:"
    echo "$OPTIONS_JSON" | jq '.'
    echo "[DRY RUN] No changes made."
    exit 0
fi

# Step 4: Execute the updateProjectV2Field mutation
echo ""
echo "Executing updateProjectV2Field mutation..."

# Build full GraphQL request body with jq (gh api graphql does not support --argjson)
MUTATION_QUERY='mutation($fieldId: ID!, $name: String!, $options: [ProjectV2SingleSelectFieldOptionInput!]!) {
    updateProjectV2Field(input: {
      fieldId: $fieldId
      name: $name
      singleSelectOptions: $options
    }) {
      projectV2Field {
        ... on ProjectV2SingleSelectField {
          id
          name
          options {
            id
            name
          }
        }
      }
    }
  }'

REQUEST_BODY=$(jq -n \
  --arg query "$MUTATION_QUERY" \
  --arg fieldId "$FIELD_ID" \
  --arg name "$FIELD_NAME" \
  --argjson options "$OPTIONS_JSON" \
  '{query: $query, variables: {fieldId: $fieldId, name: $name, options: $options}}')

MUTATION_RESULT=$(echo "$REQUEST_BODY" | gh api graphql --input - 2>&1)

# Check for errors
if echo "$MUTATION_RESULT" | jq -e '.errors' > /dev/null 2>&1; then
    echo "ERROR: Mutation failed:" >&2
    echo "$MUTATION_RESULT" | jq '.errors' >&2
    exit 1
fi

# Step 5: Verify existing assignments survived
echo "Verifying existing columns preserved..."

UPDATED_OPTIONS=$(echo "$MUTATION_RESULT" | jq -c '.data.updateProjectV2Field.projectV2Field.options')
UPDATED_COUNT=$(echo "$UPDATED_OPTIONS" | jq 'length')

echo "Updated field has ${UPDATED_COUNT} columns:"
echo "$UPDATED_OPTIONS" | jq -r '.[].name' | while read -r name; do
    echo "  - $name"
done

# Verify all existing option IDs are still present
# Use process substitution to avoid subshell scoping (pipe | while creates
# a subshell where variable assignments don't propagate to the parent)
PRESERVED=true
while read -r old_id; do
    if ! echo "$UPDATED_OPTIONS" | jq -e --arg id "$old_id" '.[] | select(.id == $id)' > /dev/null 2>&1; then
        OLD_NAME=$(echo "$EXISTING_OPTIONS" | jq -r --arg id "$old_id" '.[] | select(.id == $id) | .name')
        echo "WARNING: Existing column '${OLD_NAME}' (ID: ${old_id}) was NOT preserved!" >&2
        PRESERVED=false
    fi
done < <(echo "$EXISTING_OPTIONS" | jq -r '.[].id')

if [[ "$PRESERVED" == "true" ]]; then
    echo ""
    echo "SUCCESS: All existing columns preserved. ${#TO_ADD[@]} new column(s) added."
else
    echo ""
    echo "WARNING: Some existing columns may have lost their assignments. Check the board!" >&2
    exit 1
fi
