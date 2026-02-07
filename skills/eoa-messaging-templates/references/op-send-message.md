# Operation: Send AI Maestro Message

---
procedure: proc-request-pr-review
workflow-instruction: Step 20 - PR Review Request
operation-id: op-send-message
---

## Purpose

Send a message to another agent via AI Maestro messaging system.

## When to Use

- Assigning tasks to remote agents
- Requesting status updates
- Sending integration/review requests
- Escalating issues
- Acknowledging received messages

## Prerequisites

- AI Maestro running at http://localhost:23000
- Valid sender and recipient agent names
- JSON payload prepared

## Steps

1. **Prepare the message payload** with required fields:
   - `from`: Your agent session name
   - `to`: Recipient agent session name (full name, e.g., `libs-svg-svgbbox`)
   - `subject`: Short subject line
   - `priority`: `high`, `normal`, or `low`
   - `content`: Object with `type` and `message` fields

2. **Execute curl command**:
   ```bash
   curl -X POST "http://localhost:23000/api/messages" \
     -H "Content-Type: application/json" \
     -d '{
       "from": "<sender>",
       "to": "<recipient>",
       "subject": "<subject>",
       "priority": "<priority>",
       "content": {"type": "<type>", "message": "<message>"}
     }'
   ```

3. **Verify response** contains `{"status": "sent", "message_id": "..."}`

4. **Log the message** in delegation/coordination log

## Output

| Field | Type | Description |
|-------|------|-------------|
| status | string | "sent" on success |
| message_id | string | Unique message identifier |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | AI Maestro offline | Start AI Maestro service |
| Agent not found | Invalid recipient name | Verify agent session name |
| Invalid JSON | Malformed payload | Validate JSON syntax |

## Example

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-main",
    "to": "eia-main",
    "subject": "PR #123 Review Request",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Please review PR #123 for code quality and CI compliance."
    }
  }'
```
