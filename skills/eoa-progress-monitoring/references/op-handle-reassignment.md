---
procedure: proc-execute-task
workflow-instruction: Step 17 - Task Execution
operation: handle-reassignment
---

# Operation: Handle Reassignment

## Purpose

Reassign a task from an unresponsive agent to an available agent, ensuring proper context transfer.

## When to Use

- Agent remains unresponsive after urgent reminder
- Reassignment deadline has passed
- User authorizes reassignment
- Agent reports inability to continue

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| task_id | Issue number | Yes |
| current_agent | Currently assigned agent | Yes |
| new_agent | Available agent to reassign to | No (auto-select if not provided) |
| user_authorized | Boolean from user decision | Yes (unless overnight mode) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| reassignment_completed | Boolean | Success status |
| new_agent_assigned | String | Name of new agent |
| context_transferred | Boolean | Context handoff completed |

## Steps

### Step 1: Check Reassignment Authorization

```bash
TASK_ID=$1
CURRENT_AGENT=$2
USER_AUTHORIZED=$3

# Check if user authorization is required
if [ "$USER_AUTHORIZED" != "true" ]; then
  # Check if in overnight autonomous mode
  OVERNIGHT_MODE=$(cat orchestrator_state.json 2>/dev/null | jq -r '.overnight_mode // false')

  if [ "$OVERNIGHT_MODE" != "true" ]; then
    echo "User authorization required for reassignment. Escalating to EAMA."
    # Send escalation
    curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
      -H "Content-Type: application/json" \
      -d '{
        "from": "orchestrator",
        "to": "eama-main",
        "subject": "Reassignment Approval Needed: #'"$TASK_ID"'",
        "priority": "high",
        "content": {
          "type": "approval-request",
          "message": "Agent '"$CURRENT_AGENT"' is unresponsive on task #'"$TASK_ID"'. Approval needed to reassign.\n\nOptions:\n1. Wait longer\n2. Reassign to available agent\n3. Abort task",
          "data": {
            "task_id": "'"$TASK_ID"'",
            "current_agent": "'"$CURRENT_AGENT"'"
          }
        }
      }'
    exit 0
  fi
fi
```

### Step 2: Find Available Agent

```bash
if [ -z "$NEW_AGENT" ]; then
  # Query available agents
  AVAILABLE_AGENTS=$(curl -s "${AIMAESTRO_API:-http://localhost:23000}/api/agents" | \
    jq -r '.agents[] | select(.state == "available" or .state == "idle") | .name')

  # Filter out current agent
  AVAILABLE_AGENTS=$(echo "$AVAILABLE_AGENTS" | grep -v "$CURRENT_AGENT")

  if [ -z "$AVAILABLE_AGENTS" ]; then
    echo "ERROR: No available agents for reassignment"
    # Escalate to user
    exit 1
  fi

  # Select first available agent
  NEW_AGENT=$(echo "$AVAILABLE_AGENTS" | head -1)
  echo "Selected agent for reassignment: $NEW_AGENT"
fi
```

### Step 3: Compile Context for Transfer

```bash
# Gather all context from the task
TASK_DETAILS=$(gh issue view $TASK_ID --json title,body,comments,labels)

# Get original delegation message
ORIGINAL_DELEGATION=$(curl -s "${AIMAESTRO_API:-http://localhost:23000}/api/messages?agent=$CURRENT_AGENT&action=list" | \
  jq -r '.messages[] | select(.content.data.task_id == "'"$TASK_ID"'" and .content.type == "task") | .content.message' | head -1)

# Get any progress updates
PROGRESS_UPDATES=$(curl -s "${AIMAESTRO_API:-http://localhost:23000}/api/messages?agent=orchestrator&action=list" | \
  jq -r '.messages[] | select(.from == "'"$CURRENT_AGENT"'" and .content.data.task_id == "'"$TASK_ID"'") | .content.message')

# Compile handoff document
HANDOFF_CONTEXT="## Task Reassignment Context

### Original Task
$ORIGINAL_DELEGATION

### Progress Updates (from previous agent)
$PROGRESS_UPDATES

### Known Issues
- Previous agent ($CURRENT_AGENT) became unresponsive
- Reassigned at $(date -u +%Y-%m-%dT%H:%M:%SZ)

### Instructions
Continue from where the previous agent left off. Review any partial work in the codebase before proceeding.
"
```

### Step 4: Notify Current Agent

```bash
curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "'"$CURRENT_AGENT"'",
    "subject": "Task Reassigned: #'"$TASK_ID"'",
    "priority": "normal",
    "content": {
      "type": "notification",
      "message": "Task #'"$TASK_ID"' has been reassigned to '"$NEW_AGENT"' due to no response to escalation messages.\n\nIf you have any partial work or context to share, please send it to the orchestrator for transfer.\n\nNo further action required on this task.",
      "data": {
        "task_id": "'"$TASK_ID"'",
        "reassigned_to": "'"$NEW_AGENT"'"
      }
    }
  }'
```

### Step 5: Update GitHub Issue Labels

```bash
# Remove assignment from current agent
gh issue edit $TASK_ID --remove-label "assign:$CURRENT_AGENT"

# Add assignment to new agent
gh issue edit $TASK_ID --add-label "assign:$NEW_AGENT"

# Add reassignment comment
gh issue comment $TASK_ID --body "**TASK REASSIGNED**

- Previous agent: $CURRENT_AGENT (unresponsive)
- New agent: $NEW_AGENT
- Reassigned at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- Reason: No response to escalation"
```

### Step 6: Send Task to New Agent

```bash
curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "'"$NEW_AGENT"'",
    "subject": "Task Reassignment: #'"$TASK_ID"'",
    "priority": "high",
    "content": {
      "type": "task",
      "message": "'"$HANDOFF_CONTEXT"'",
      "data": {
        "task_id": "'"$TASK_ID"'",
        "reassigned_from": "'"$CURRENT_AGENT"'",
        "original_assignment": true
      }
    }
  }'
```

### Step 7: Log Reassignment

```bash
REASSIGNMENT_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "$REASSIGNMENT_TIMESTAMP|$TASK_ID|$CURRENT_AGENT|$NEW_AGENT|reassignment" >> reassignment_log.txt

# Clear pending reassignment entry
jq 'del(.[] | select(.task_id == "'"$TASK_ID"'"))' pending_reassignments.json > tmp.json && mv tmp.json pending_reassignments.json
```

## Decision Flow

```
Unresponsive after urgent reminder
        ↓
Is user available?
    ├── Yes → Present options (wait/reassign/abort)
    │         ↓
    │    User chooses reassign
    │         ↓
    └── No (overnight mode) → Auto-reassign
                ↓
        Find available agent
                ↓
        Compile context
                ↓
        Notify current agent
                ↓
        Update labels
                ↓
        Send to new agent
                ↓
        Log reassignment
```

## Success Criteria

- [ ] User authorization verified (or overnight mode active)
- [ ] Available agent found
- [ ] Context compiled and transferred
- [ ] Current agent notified
- [ ] Labels updated correctly
- [ ] New agent received task
- [ ] Reassignment logged

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No available agents | All agents busy | Queue task, notify user |
| User denies reassignment | Prefers to wait | Set longer timeout, re-escalate later |
| New agent also unresponsive | Multiple agent issues | Escalate to user, check agent system |
| Context incomplete | Messages missing | Include note about missing context |

## Related Operations

- op-send-urgent-reminder
- op-detect-agent-state
- op-escalate-to-user (in remote-agent-coordinator skill)
