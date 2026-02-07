---
procedure: support-skill
workflow-instruction: support
---

# Operation: Receive ECOS Notification

## When to Use

Use this operation when ECOS (Emergency Context-loss Operations System) sends a notification about agent failure or replacement.

## Prerequisites

- AI Maestro running and accessible
- ECOS system operational
- Orchestrator in active state

## Procedure

### Step 1: Detect ECOS Notification

ECOS notifications arrive via AI Maestro with specific message format:

```json
{
  "from": "ecos",
  "subject": "Agent Replacement Required",
  "priority": "urgent",
  "content": {
    "type": "replacement_required",
    "failed_agent": "implementer-1",
    "failure_reason": "context_loss",
    "replacement_agent": "implementer-2",
    "urgency": "immediate"
  }
}
```

### Step 2: Check Message Queue

```bash
# Check for ECOS messages
curl -s "http://localhost:23000/api/messages?agent=$SESSION_NAME&action=list&status=unread" \
  | jq '.messages[] | select(.from == "ecos")'
```

### Step 3: Identify Notification Type

| Type | Meaning | Urgency |
|------|---------|---------|
| `context_loss` | Agent lost context, recovery impossible | immediate |
| `unresponsive` | Agent not responding to polls | high |
| `error_state` | Agent in error loop | high |
| `manual_request` | User requested replacement | normal |
| `session_ended` | Agent session terminated | immediate |

### Step 4: Acknowledge Notification

```bash
# Send acknowledgment to ECOS
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "ecos",
    "subject": "ACK: Replacement for <failed_agent>",
    "priority": "high",
    "content": {
      "type": "acknowledgment",
      "message": "Received replacement notification. Beginning context compilation.",
      "failed_agent": "<failed_agent>",
      "replacement_agent": "<replacement_agent>"
    }
  }'
```

### Step 5: Pause New Assignments

Do NOT assign any new work to any agent until replacement is complete:

1. Mark orchestrator state as "replacement_in_progress"
2. Queue any pending assignments
3. Hold agent polling

### Step 6: Log Notification

```bash
# Log the replacement event
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ECOS_NOTIFICATION: Failed=$failed_agent Replacement=$replacement_agent Reason=$failure_reason" >> orchestrator.log
```

## Output

| Field | Type | Description |
|-------|------|-------------|
| Notification Type | String | Type of failure/replacement |
| Failed Agent | String | Agent ID that failed |
| Replacement Agent | String | Agent ID of replacement |
| Acknowledgment | Boolean | Whether ACK was sent |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No ECOS message found | Network issue or false alarm | Check AI Maestro status |
| Invalid message format | ECOS version mismatch | Check ECOS compatibility |
| Replacement agent unavailable | Agent not registered | Request alternative from ECOS |
| AI Maestro unreachable | Service down | Restart AI Maestro service |

## Example

```bash
# Full notification handling sequence

# 1. Check for ECOS notifications
ECOS_MSG=$(curl -s "http://localhost:23000/api/messages?agent=orchestrator-master&action=list&status=unread" \
  | jq -r '.messages[] | select(.content.type == "replacement_required")')

if [ -n "$ECOS_MSG" ]; then
  # 2. Extract details
  FAILED=$(echo "$ECOS_MSG" | jq -r '.content.failed_agent')
  REPLACEMENT=$(echo "$ECOS_MSG" | jq -r '.content.replacement_agent')
  REASON=$(echo "$ECOS_MSG" | jq -r '.content.failure_reason')

  # 3. Log
  echo "ECOS: Replacing $FAILED with $REPLACEMENT due to $REASON"

  # 4. Acknowledge
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"ecos\",
      \"subject\": \"ACK: Replacement for $FAILED\",
      \"priority\": \"high\",
      \"content\": {
        \"type\": \"acknowledgment\",
        \"message\": \"Beginning replacement process\",
        \"failed_agent\": \"$FAILED\",
        \"replacement_agent\": \"$REPLACEMENT\"
      }
    }"

  # 5. Proceed to context compilation
  echo "Proceed to: op-compile-task-context"
fi
```

## Checklist

- [ ] Check AI Maestro message queue
- [ ] Identify ECOS notification
- [ ] Parse notification details (failed agent, replacement, reason)
- [ ] Send acknowledgment to ECOS
- [ ] Pause new agent assignments
- [ ] Log the replacement event
- [ ] Proceed to context compilation
