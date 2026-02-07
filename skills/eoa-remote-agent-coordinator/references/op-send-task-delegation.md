---
procedure: proc-execute-task
workflow-instruction: Step 17 - Task Execution
operation: send-task-delegation
---

# Operation: Send Task Delegation

## Purpose

Send a prepared task delegation message to a remote agent via AI Maestro.

## When to Use

- After preparing complete task delegation instructions
- When assigning new work to an available agent
- When reassigning a task from an unresponsive agent

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| delegation_message | op-prepare-task-delegation output | Yes |
| agent_name | Agent roster | Yes |
| issue_number | GitHub issue | Yes |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| message_id | String | AI Maestro message ID |
| sent_timestamp | ISO8601 | When message was sent |
| delivery_status | String | success/failed |

## Steps

### Step 1: Verify Agent Availability

```bash
# Check agent is registered and not already assigned
AGENT_STATUS=$(curl -s "${AIMAESTRO_API:-http://localhost:23000}/api/agents/$AGENT_NAME")
AGENT_STATE=$(echo "$AGENT_STATUS" | jq -r '.state')

if [ "$AGENT_STATE" != "available" ] && [ "$AGENT_STATE" != "idle" ]; then
  echo "WARNING: Agent $AGENT_NAME is currently $AGENT_STATE"
fi
```

### Step 2: Send Task Message

```bash
curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "'"$AGENT_NAME"'",
    "subject": "Task Assignment: #'"$ISSUE_NUMBER"' - '"$TASK_TITLE"'",
    "priority": "normal",
    "content": {
      "type": "task",
      "message": "'"$DELEGATION_MESSAGE"'",
      "data": {
        "task_id": "'"$ISSUE_NUMBER"'",
        "files_in_scope": '"$FILES_JSON"',
        "completion_criteria": '"$CRITERIA_JSON"'
      }
    }
  }'
```

### Step 3: Update GitHub Issue

```bash
# Add assignment label
gh issue edit $ISSUE_NUMBER --add-label "assign:$AGENT_NAME"

# Update status to in-progress
gh issue edit $ISSUE_NUMBER --add-label "status:in-progress"

# Add assignment comment
gh issue comment $ISSUE_NUMBER --body "Assigned to agent: $AGENT_NAME via AI Maestro at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 4: Record Assignment in Tracking

```bash
# Log assignment for monitoring
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | ASSIGNED | #$ISSUE_NUMBER | $AGENT_NAME" >> assignment_log.txt
```

## Success Criteria

- [ ] Message sent successfully (AI Maestro returns message ID)
- [ ] GitHub issue labeled with `assign:<agent>` and `status:in-progress`
- [ ] Assignment comment added to issue
- [ ] Assignment logged for progress monitoring

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Message send failed | AI Maestro unavailable | Run op-verify-aimaestro-availability |
| Agent not found | Agent not registered | Complete agent onboarding |
| Issue label failed | GitHub CLI auth issue | Re-authenticate gh CLI |

## Next Operation

After sending task delegation, proceed to:
- op-wait-for-acknowledgment

## Related Operations

- op-verify-aimaestro-availability
- op-prepare-task-delegation
- op-wait-for-acknowledgment
