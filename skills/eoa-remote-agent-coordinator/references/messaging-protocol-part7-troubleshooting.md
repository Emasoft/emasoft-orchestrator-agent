# Messaging Protocol Part 7: Troubleshooting

**Parent document**: [messaging-protocol.md](messaging-protocol.md)

---

## 7.1 Messages Not Being Delivered

**Symptoms**: API returns 200 but recipient never receives message.

### Solution Steps

1. **Verify recipient agent is registered and online**:
   ```bash
   curl $AIMAESTRO_API/api/agents
   ```

2. **Check recipient's full session name is correct**:
   - Use full name like `libs-svg-svgbbox`
   - Not alias like `svgbbox`

3. **Verify AI Maestro server is running**:
   ```bash
   curl $AIMAESTRO_API/api/health
   ```

4. **Check for network issues**:
   - Verify sender can reach server
   - Verify recipient can reach server

5. **Review server logs for delivery errors**:
   - Check AI Maestro logs for error messages

---

## 7.2 Agent Not Found (404)

**Symptoms**: API returns 404 when sending message to agent.

### Solution Steps

1. **Verify agent session name spelling** (case-sensitive):
   ```bash
   curl $AIMAESTRO_API/api/agents | jq '.[] | .session_name'
   ```

2. **Check if agent session has expired or terminated**:
   - Agent may need to restart

3. **Use `/api/agents` to list all registered agents**:
   ```bash
   curl $AIMAESTRO_API/api/agents | jq .
   ```

4. **If agent recently restarted, wait for re-registration**:
   - May take 30-60 seconds

5. **Use full session name**:
   - CORRECT: `libs-svg-svgbbox`
   - WRONG: `svgbbox`

---

## 7.3 Message Content Malformed (400)

**Symptoms**: API returns 400 Bad Request.

### Solution Steps

1. **Verify `content` is an object, NOT a string**:
   ```json
   // WRONG
   "content": "This is my message"

   // CORRECT
   "content": {"type": "task", "message": "This is my message"}
   ```

2. **Check JSON syntax is valid**:
   ```bash
   echo '{"type":"task","message":"test"}' | jq .
   ```

3. **Ensure required fields are present**:
   - `to` (recipient)
   - `subject` (subject line)
   - `content` (object with `type`)

4. **Verify `priority` is valid**:
   - Must be: `low`, `normal`, `high`, or `urgent`

5. **Check message size**:
   - Must be under 100KB

---

## 7.4 Messages Arrive Out of Order

**Symptoms**: Agent receives messages in different order than sent.

### Solution Steps

1. **AI Maestro does not guarantee ordering**:
   - Include sequence numbers if order matters

2. **Use timestamps for ordering**:
   ```json
   {
     "content": {
       "type": "task",
       "sequence": 3,
       "timestamp": "2025-12-31T10:00:00Z"
     }
   }
   ```

3. **For dependent messages, wait for ACK before sending next**:
   - Do not send message 2 until message 1 is acknowledged

4. **Use task_id to group related messages**:
   - All messages for same task have same task_id

---

## 7.5 Duplicate Messages Received

**Symptoms**: Agent receives same message multiple times.

### Solution Steps

1. **Check if sender is retrying due to perceived failure**:
   - Sender may not have received ACK

2. **Implement idempotency using message IDs**:
   ```python
   processed_ids = set()

   def handle_message(msg):
       if msg['id'] in processed_ids:
           return  # Skip duplicate
       processed_ids.add(msg['id'])
       # Process message
   ```

3. **Track processed message IDs to detect duplicates**

4. **If using retry logic, ensure proper backoff**:
   - Rapid retries can cause duplicates

---

## 7.6 Subconscious Notifications Not Appearing

**Symptoms**: Agent not notified of new messages automatically.

### Solution Steps

1. **Verify AI Maestro subconscious feature is running**:
   - Runs automatically with AI Maestro server

2. **Check agent session is properly registered**:
   ```bash
   curl $AIMAESTRO_API/api/agents | jq '.[] | select(.session_name == "your-agent")'
   ```

3. **Verify agent is idle**:
   - Notifications only appear when idle 30+ seconds
   - Check if agent is in middle of operation

4. **Check tmux session is accessible**:
   - Subconscious uses tmux send-keys
   - Verify tmux session exists

5. **Remember poll interval is 5 minutes**:
   - Urgent messages may need direct ping
   - Use high/urgent priority for faster attention

---

## 7.7 High Priority Messages Not Prioritized

**Symptoms**: Urgent messages processed after normal priority messages.

### Solution Steps

1. **Priority field is advisory**:
   - Agents must implement priority handling
   - Not automatic queue reordering

2. **Include `URGENT:` prefix in subject**:
   ```bash
   send-aimaestro-message.sh agent "URGENT: Security Issue" "..." urgent task
   ```

3. **Send follow-up if no response within timeout**:
   - Urgent timeout is 2 minutes

4. **Consider multiple notification channels**:
   - For critical issues, also notify user directly

---

## 7.8 Message Timeout But Agent Is Working

**Symptoms**: Orchestrator times out waiting for response, but agent is actively working.

### Solution Steps

1. **Agent may be in middle of long operation**:
   - Increase timeout for complex tasks
   - Use `expected_duration` field

2. **Agent should send progress updates**:
   ```json
   {
     "type": "progress-update",
     "task_id": "GH-42",
     "progress_percent": 50,
     "current_activity": "Running test suite"
   }
   ```

3. **Configure expected response timeouts by task type**:
   - Simple tasks: 5 min
   - Complex tasks: 30 min
   - Build tasks: 60 min

4. **Use background polling to detect agent activity**:
   - Check agent status without requiring response

---

## Diagnostic Commands

### Check Server Status
```bash
curl $AIMAESTRO_API/api/health
```

### List All Agents
```bash
curl $AIMAESTRO_API/api/agents | jq '.[] | {name: .session_name, status: .status}'
```

### Check Your Inbox
```bash
check-aimaestro-messages.sh
```

### Validate JSON Before Sending
```bash
echo '{"type":"task","message":"test"}' | jq .
```

---

## Related Sections

- [Part 1: API and Schema](messaging-protocol-part1-api-schema.md) - Correct message format
- [Part 4: Errors](messaging-protocol-part4-agents-errors.md) - Error handling details
- [Part 6: Timeouts](messaging-protocol-part6-timeouts-integration.md) - Timeout configuration
