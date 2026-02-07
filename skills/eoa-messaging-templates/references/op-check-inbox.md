# Operation: Check AI Maestro Inbox

---
procedure: proc-request-pr-review
workflow-instruction: Step 20 - PR Review Request
operation-id: op-check-inbox
---

## Purpose

Check for unread messages in your AI Maestro inbox.

## When to Use

- At start of any workflow to check for pending messages
- After delegating tasks to check for responses
- Periodically during long-running operations
- When notification banner appears

## Prerequisites

- AI Maestro running at http://localhost:23000
- `$SESSION_NAME` environment variable set (or known agent name)

## Steps

1. **Execute inbox query**:
   ```bash
   curl -s "http://localhost:23000/api/messages?agent=$SESSION_NAME&action=list&status=unread" | jq '.messages[].content.message'
   ```

2. **Process messages by priority**: URGENT > HIGH > NORMAL

3. **Respond to messages** that require acknowledgment

4. **Mark messages as read** after processing

## Output

JSON array of messages with fields:
- `from`: Sender agent name
- `subject`: Message subject
- `priority`: Message priority level
- `content.type`: Message type
- `content.message`: Message body
- `timestamp`: When message was sent

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Empty result | No unread messages | Continue with workflow |
| Connection refused | AI Maestro offline | Start AI Maestro service |
| Agent not found | Invalid session name | Verify $SESSION_NAME |

## Example

```bash
# Check unread messages
curl -s "http://localhost:23000/api/messages?agent=eoa-main&action=list&status=unread" | jq '.'

# Get unread count only
curl -s "http://localhost:23000/api/messages?agent=eoa-main&action=unread-count"
```

## Critical Rule

When unread messages exist, STOP current work and process them first. Messages may contain corrections, bug reports, or blocking issues.
