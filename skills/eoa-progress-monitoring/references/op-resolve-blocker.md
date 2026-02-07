---
procedure: proc-execute-task
workflow-instruction: Step 17 - Task Execution
operation: resolve-blocker
---

# Operation: Resolve Blocker

## Purpose

Process blocker resolution, restore task to previous status, close blocker issue, and notify assigned agent.

## When to Use

- User provides resolution for a blocker
- Blocking dependency is completed
- Resource or access is granted
- External dependency becomes available

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| task_id | Blocked task issue number | Yes |
| blocker_issue | Blocker tracking issue number | Yes |
| resolution_details | How the blocker was resolved | Yes |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| task_unblocked | Boolean | Task restored to previous status |
| agent_notified | Boolean | Agent informed of resolution |
| blocker_closed | Boolean | Blocker issue closed |

## Steps

### Step 1: Verify Blocker Is Actually Resolved

```bash
TASK_ID=$1
BLOCKER_ISSUE=$2
RESOLUTION_DETAILS=$3

# Do not assume - verify the blocker condition is actually resolved
# This varies by blocker type:

# For dependency blockers - check if blocking task is complete
# For resource blockers - verify resource is available
# For approval blockers - confirm approval was given
# For external blockers - confirm external system is up

echo "Verifying blocker resolution..."
# Add specific verification logic based on blocker type
```

### Step 2: Retrieve Previous Status

```bash
# Get the previous status from the blocker comment on the task
PREVIOUS_STATUS=$(gh issue view $TASK_ID --json comments | \
  jq -r '.comments[] | select(.body | contains("Previous status:")) | .body' | \
  grep -oP 'Previous status: \K[^\n]+' | tail -1)

if [ -z "$PREVIOUS_STATUS" ]; then
  # Default to in-progress if previous status not found
  PREVIOUS_STATUS="status:in-progress"
  echo "WARNING: Previous status not found, defaulting to $PREVIOUS_STATUS"
fi

echo "Previous status: $PREVIOUS_STATUS"
```

### Step 3: Close Blocker Issue

```bash
gh issue close $BLOCKER_ISSUE --comment "**RESOLVED**

$RESOLUTION_DETAILS

Blocked task #$TASK_ID can now resume.
Resolution time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 4: Restore Task Status

```bash
# Remove blocked label, restore previous status
gh issue edit $TASK_ID --remove-label "status:blocked" --add-label "$PREVIOUS_STATUS"

# Add resolution comment
gh issue comment $TASK_ID --body "**UNBLOCKED**

Blocker #$BLOCKER_ISSUE has been resolved.

**Resolution:** $RESOLUTION_DETAILS
**Restored status:** $PREVIOUS_STATUS
**Unblocked at:** $(date -u +%Y-%m-%dT%H:%M:%SZ)

Agent may now resume work."
```

### Step 5: Get Assigned Agent

```bash
# Find which agent is assigned to this task
ASSIGNED_AGENT=$(gh issue view $TASK_ID --json labels | \
  jq -r '.labels[] | select(.name | startswith("assign:")) | .name' | \
  sed 's/assign://')

if [ -z "$ASSIGNED_AGENT" ]; then
  echo "WARNING: No agent currently assigned to task #$TASK_ID"
fi

echo "Assigned agent: $ASSIGNED_AGENT"
```

### Step 6: Notify Agent

```bash
if [ -n "$ASSIGNED_AGENT" ]; then
  curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "from": "orchestrator",
      "to": "'"$ASSIGNED_AGENT"'",
      "subject": "Blocker Resolved: #'"$TASK_ID"' - Please Resume",
      "priority": "high",
      "content": {
        "type": "unblocked",
        "message": "Good news! The blocker on task #'"$TASK_ID"' has been resolved.\n\n**Resolution:** '"$RESOLUTION_DETAILS"'\n\n**Previous Status Restored:** '"$PREVIOUS_STATUS"'\n\nPlease resume work on this task and report your progress.",
        "data": {
          "task_id": "'"$TASK_ID"'",
          "blocker_issue": "'"$BLOCKER_ISSUE"'",
          "previous_status": "'"$PREVIOUS_STATUS"'",
          "resolution": "'"$RESOLUTION_DETAILS"'"
        }
      }
    }'
fi
```

### Step 7: Log Resolution

```bash
RESOLUTION_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "$RESOLUTION_TIMESTAMP|$TASK_ID|$BLOCKER_ISSUE|$ASSIGNED_AGENT|resolved" >> blocker_log.txt
```

## Blocker Resolution Checklist

### When the blocker is resolved:

- [ ] Verify the blocker is actually resolved (do not assume)
- [ ] Retrieve previous status from the blocker comment on the blocked task
- [ ] Close the blocker issue with resolution details
- [ ] Remove `status:blocked` label from the task
- [ ] Restore previous status label on the task
- [ ] Add resolution comment on the task
- [ ] Notify the assigned agent via AI Maestro
- [ ] Log the resolution

## Important Note: Restoring Correct Status

The task returns to the COLUMN IT WAS IN BEFORE being blocked, which is NOT always "In Progress". The task could have been in:

- Testing
- Review
- Deploy
- Any other workflow stage

Always retrieve and restore the actual previous status, not a hardcoded default.

## Success Criteria

- [ ] Blocker verified as resolved
- [ ] Previous status correctly retrieved
- [ ] Blocker issue closed with resolution details
- [ ] Task labels updated correctly
- [ ] Resolution comment added to task
- [ ] Agent notified of resolution
- [ ] Resolution logged

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Previous status not found | Comment missing | Default to in-progress, log warning |
| Agent not assigned | Task was reassigned | Find current assignee or queue for assignment |
| Blocker not actually resolved | Premature closure | Re-open blocker, notify agent of false alarm |

## Related Operations

- op-handle-blocker-report
- op-detect-agent-state
