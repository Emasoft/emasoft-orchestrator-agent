---
procedure: proc-execute-task
workflow-instruction: Step 17 - Task Execution
operation: enforce-verification-loops
---

# Operation: Enforce 4-Verification Loops

## Purpose

Require agents to perform 4 self-verification cycles before approving PR creation. This ensures code quality through iterative self-review.

## When to Use

- When agent requests permission to create a PR
- After agent reports task completion
- Before any code merge

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| task_id | Issue number | Yes |
| agent_name | Assigned agent | Yes |
| pr_request_count | Internal tracking | Yes |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| verification_response | String | "verify" or "approved" |
| current_loop | Integer | Which verification loop (1-4) |
| pr_approved | Boolean | True only after 5th request |

## The 5 PR Requests Cycle

| PR Request # | Orchestrator Response | Agent Action |
|--------------|----------------------|--------------|
| 1st | "Check your changes for errors" | Self-review, fix issues |
| 2nd | "Check your changes for errors" | Self-review, fix issues |
| 3rd | "Check your changes for errors" | Self-review, fix issues |
| 4th | "Check your changes for errors" | Self-review, fix issues |
| 5th | "Approved" or "Rejected with reasons" | Create PR or fix issues |

## Steps

### Step 1: Track PR Request Count

```bash
# Get current verification count for this task
VERIFICATION_FILE="verification_state_${TASK_ID}.json"

if [ -f "$VERIFICATION_FILE" ]; then
  PR_REQUEST_COUNT=$(jq -r '.pr_request_count' "$VERIFICATION_FILE")
else
  PR_REQUEST_COUNT=0
fi

PR_REQUEST_COUNT=$((PR_REQUEST_COUNT + 1))

# Save updated count
echo '{"task_id": "'"$TASK_ID"'", "agent": "'"$AGENT_NAME"'", "pr_request_count": '$PR_REQUEST_COUNT'}' > "$VERIFICATION_FILE"
```

### Step 2: Respond Based on Count

```bash
if [ $PR_REQUEST_COUNT -lt 5 ]; then
  # Verification loop response
  RESPONSE_MESSAGE="Check your changes for errors. This is verification request $PR_REQUEST_COUNT of 4 required before PR approval."

  curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "from": "orchestrator",
      "to": "'"$AGENT_NAME"'",
      "subject": "Verification Required: #'"$TASK_ID"' ('"$PR_REQUEST_COUNT"'/4)",
      "priority": "normal",
      "content": {
        "type": "verification",
        "message": "'"$RESPONSE_MESSAGE"'",
        "data": {
          "task_id": "'"$TASK_ID"'",
          "verification_loop": '$PR_REQUEST_COUNT',
          "remaining_loops": '$((4 - PR_REQUEST_COUNT))'
        }
      }
    }'
else
  # 5th request - make approval decision
  # Proceed to final review
  echo "5th PR request - proceeding to final approval decision"
fi
```

### Step 3: Final Approval Decision (5th Request)

```bash
# Review agent's final submission
# Check against acceptance criteria

CRITERIA_MET=true  # Determine from review

if [ "$CRITERIA_MET" = true ]; then
  # Approve PR creation
  curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "from": "orchestrator",
      "to": "'"$AGENT_NAME"'",
      "subject": "PR Approved: #'"$TASK_ID"'",
      "priority": "normal",
      "content": {
        "type": "approval",
        "message": "You may now create a PR for task #'"$TASK_ID"'. Ensure all tests pass before submission.",
        "data": {
          "task_id": "'"$TASK_ID"'",
          "pr_approved": true
        }
      }
    }'
else
  # Reject with reasons
  curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "from": "orchestrator",
      "to": "'"$AGENT_NAME"'",
      "subject": "PR Rejected: #'"$TASK_ID"'",
      "priority": "high",
      "content": {
        "type": "rejection",
        "message": "PR creation not approved. Issues found:\n'"$REJECTION_REASONS"'\n\nAddress these issues and request PR permission again.",
        "data": {
          "task_id": "'"$TASK_ID"'",
          "pr_approved": false,
          "issues": '"$ISSUES_JSON"'
        }
      }
    }'

  # Reset verification count for another 4 loops
  echo '{"task_id": "'"$TASK_ID"'", "agent": "'"$AGENT_NAME"'", "pr_request_count": 0}' > "$VERIFICATION_FILE"
fi
```

## Enforcement Rules

### MUST

- Respond to first 4 PR requests with "Check your changes for errors"
- Track verification count per task (not globally)
- Make actual approval decision only on 5th request
- Reset count if PR is rejected

### MUST NOT

- Skip verification loops
- Approve before 5th request
- Allow agent to bypass with urgency claims
- Count verification loops across different tasks

## Success Criteria

- [ ] Verification count tracked per task
- [ ] First 4 requests receive "verify" response
- [ ] 5th request triggers actual review
- [ ] Approval/rejection based on acceptance criteria
- [ ] Count reset if rejected

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Count lost | State file deleted | Reset to 0, inform agent |
| Agent skips loops | Agent creates PR directly | Reject PR, require loops |
| Wrong task counted | Task ID mismatch | Verify task ID in messages |

## Related Operations

- op-review-completion-report
- op-prepare-task-delegation
