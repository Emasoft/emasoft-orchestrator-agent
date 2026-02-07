---
procedure: support-skill
workflow-instruction: support
---

# Operation: Confirm Reassignment

## When to Use

Use this operation after sending the handoff to verify the replacement is complete and notify all parties.

## Prerequisites

- Handoff sent to replacement agent (op-send-handoff)
- Waiting for or received ACK from replacement agent
- Access to orchestrator state files

## Procedure

### Step 1: Wait for ACK

Monitor AI Maestro for acknowledgment:

```bash
# Check for ACK message from replacement agent
ACK_MSG=$(curl -s "http://localhost:23000/api/messages?agent=$SESSION_NAME&action=list&status=unread" \
  | jq '.messages[] | select(.content.type == "ack" and .from == "'$REPLACEMENT_SESSION'")')

if [ -n "$ACK_MSG" ]; then
  echo "ACK received"
else
  echo "Waiting for ACK..."
fi
```

### Step 2: Verify ACK Content

Replacement agent should confirm:

```bash
# Parse ACK content
ACK_STATUS=$(echo "$ACK_MSG" | jq -r '.content.status')  # "received" or "understood"
QUESTIONS=$(echo "$ACK_MSG" | jq -r '.content.questions // "none"')
ETA=$(echo "$ACK_MSG" | jq -r '.content.eta // "not specified"')

# Log ACK details
echo "ACK Status: $ACK_STATUS"
echo "Questions: $QUESTIONS"
echo "ETA: $ETA"
```

### Step 3: Handle Questions

If replacement agent has questions:

```bash
# Send clarification response
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d "{
    \"to\": \"$REPLACEMENT_SESSION\",
    \"subject\": \"RE: Task Handoff Clarifications\",
    \"priority\": \"high\",
    \"content\": {
      \"type\": \"clarification\",
      \"message\": \"<answers to questions>\",
      \"original_handoff\": \"$HANDOFF_URL\"
    }
  }"
```

### Step 4: Update Orchestrator State

```bash
# Update state file with replacement info
cat >> design/state/exec-phase.md <<EOF

## Agent Replacement Record
- Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- Failed Agent: $FAILED_AGENT
- Replacement Agent: $REPLACEMENT_AGENT
- Reason: $FAILURE_REASON
- Tasks Transferred: #42, #45
- ACK Received: yes
- Status: complete
EOF
```

### Step 5: Remove Failed Agent from Roster

```bash
# Update agent registry in state
# Remove failed agent, mark as inactive
python3 -c "
import yaml
with open('design/state/exec-phase.md', 'r') as f:
    content = f.read()
# Parse YAML frontmatter and update agents section
# Mark $FAILED_AGENT as 'inactive'
"
```

### Step 6: Notify ECOS of Completion

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d "{
    \"to\": \"ecos\",
    \"subject\": \"Replacement Complete: $FAILED_AGENT -> $REPLACEMENT_AGENT\",
    \"priority\": \"normal\",
    \"content\": {
      \"type\": \"replacement_complete\",
      \"failed_agent\": \"$FAILED_AGENT\",
      \"replacement_agent\": \"$REPLACEMENT_AGENT\",
      \"tasks_transferred\": [42, 45],
      \"ack_received\": true,
      \"completion_time\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
    }
  }"
```

### Step 7: Create Audit Log Entry

```bash
# Log complete replacement record
cat >> orchestrator.log <<EOF
$(date -u +%Y-%m-%dT%H:%M:%SZ) REPLACEMENT_COMPLETE
  failed_agent=$FAILED_AGENT
  replacement_agent=$REPLACEMENT_AGENT
  failure_reason=$FAILURE_REASON
  tasks_transferred=42,45
  ack_received=yes
  handoff_url=$HANDOFF_URL
  duration=$(calculate_duration)
EOF
```

### Step 8: Resume Normal Operations

```bash
# Clear replacement_in_progress flag
# Resume agent polling
# Process queued assignments

echo "Replacement complete. Resuming normal orchestration."
```

### Step 9: Add Final GitHub Comment

```bash
# Add completion comment to primary issue
gh issue comment $PRIMARY_ISSUE --body "**Replacement Complete**
- $FAILED_AGENT -> $REPLACEMENT_AGENT
- ACK received at $(date -u +%Y-%m-%dT%H:%M:%SZ)
- Work will resume from handoff state
- ETA: $ETA"
```

## Output

| Field | Type | Description |
|-------|------|-------------|
| ACK Received | Boolean | Whether replacement agent acknowledged |
| Questions Resolved | Boolean | Whether all questions answered |
| State Updated | Boolean | Whether state file updated |
| ECOS Notified | Boolean | Whether ECOS received completion notice |
| Audit Logged | Boolean | Whether audit log updated |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No ACK received | Timeout expired | Escalate to user |
| ACK with major questions | Agent needs more info | Provide clarification |
| State update failed | File permission issue | Check file access |
| ECOS notification failed | AI Maestro issue | Retry notification |

## Example

```bash
#!/bin/bash
# Complete reassignment confirmation

FAILED_AGENT="implementer-1"
REPLACEMENT_AGENT="implementer-2"
REPLACEMENT_SESSION="helper-agent-generic"
PRIMARY_ISSUE=42
HANDOFF_URL="https://github.com/owner/repo/issues/42#issuecomment-12345"

# 1. Check for ACK
echo "Checking for ACK from $REPLACEMENT_SESSION..."
ACK_MSG=$(curl -s "http://localhost:23000/api/messages?agent=orchestrator-master&action=list&status=unread" \
  | jq -r '.messages[] | select(.content.type == "ack" and .from == "'$REPLACEMENT_SESSION'")')

if [ -z "$ACK_MSG" ]; then
  echo "ERROR: No ACK received. Timeout may be needed."
  exit 1
fi

echo "ACK received!"

# 2. Parse ACK
QUESTIONS=$(echo "$ACK_MSG" | jq -r '.content.questions // "none"')
ETA=$(echo "$ACK_MSG" | jq -r '.content.eta // "unknown"')

if [ "$QUESTIONS" != "none" ]; then
  echo "Replacement agent has questions: $QUESTIONS"
  # Handle questions before proceeding
fi

# 3. Update state file
echo "Updating orchestrator state..."
cat >> design/state/exec-phase.md <<EOF

## Agent Replacement Complete
- Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- From: $FAILED_AGENT
- To: $REPLACEMENT_AGENT
- ACK: received
- ETA: $ETA
EOF

# 4. Notify ECOS
echo "Notifying ECOS..."
curl -s -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d "{
    \"to\": \"ecos\",
    \"subject\": \"Replacement Complete\",
    \"priority\": \"normal\",
    \"content\": {
      \"type\": \"replacement_complete\",
      \"failed_agent\": \"$FAILED_AGENT\",
      \"replacement_agent\": \"$REPLACEMENT_AGENT\",
      \"ack_received\": true
    }
  }"

# 5. Add GitHub comment
gh issue comment "$PRIMARY_ISSUE" --body "**Replacement Complete**
Agent handoff from $FAILED_AGENT to $REPLACEMENT_AGENT successful.
Work resuming. ETA: $ETA"

# 6. Log
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) REPLACEMENT_COMPLETE $FAILED_AGENT->$REPLACEMENT_AGENT" >> orchestrator.log

echo "Reassignment confirmation complete. Normal operations resumed."
```

## Checklist

- [ ] Wait for and receive ACK from replacement agent
- [ ] Verify ACK content (understood, questions, ETA)
- [ ] Resolve any questions
- [ ] Update orchestrator state file
- [ ] Remove failed agent from active roster
- [ ] Notify ECOS of successful replacement
- [ ] Create audit log entry
- [ ] Add completion comment to GitHub issue
- [ ] Clear replacement_in_progress flag
- [ ] Resume normal orchestration operations
