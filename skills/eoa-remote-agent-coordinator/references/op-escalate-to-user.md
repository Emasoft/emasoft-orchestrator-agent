---
procedure: proc-execute-task
workflow-instruction: Step 17 - Task Execution
operation: escalate-to-user
---

# Operation: Escalate to User

## Purpose

Escalate decisions to the user when they exceed orchestrator authority (architecture, security, requirement changes).

## When to Use

- Architecture decisions not covered by methodology
- Security vulnerabilities discovered
- Dependency conflicts requiring user choice
- Test failures suggesting specification issues
- Requirement clarifications needed
- Breaking changes proposed

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| escalation_type | Category of escalation | Yes |
| context | Relevant background | Yes |
| options | Possible decisions (if applicable) | No |
| urgency | Priority level | Yes |
| blocking_task | Task blocked by this decision | No |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| escalation_id | String | Tracking ID for follow-up |
| user_notified | Boolean | Confirmation of notification |
| queue_position | Integer | Position in escalation queue |

## Escalation Categories

| Category | Examples | Urgency Default |
|----------|----------|-----------------|
| Architecture | Design pattern choice, module boundaries | Normal |
| Security | Vulnerability, credentials handling | Urgent |
| Requirements | Ambiguous spec, conflicting requirements | High |
| Dependencies | Version conflicts, breaking updates | Normal |
| Scope | Feature creep, out-of-scope requests | Normal |
| Blockers | External dependencies, access issues | High |

## Steps

### Step 1: Prepare Escalation Message

```bash
ESCALATION_ID="esc-$(date +%Y%m%d%H%M%S)-$RANDOM"

# Create escalation record
cat > "escalation_${ESCALATION_ID}.json" << EOF
{
  "id": "$ESCALATION_ID",
  "type": "$ESCALATION_TYPE",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "context": "$CONTEXT",
  "options": $OPTIONS_JSON,
  "urgency": "$URGENCY",
  "blocking_task": "$BLOCKING_TASK",
  "status": "pending"
}
EOF
```

### Step 2: Send to EAMA (User Communication Channel)

```bash
curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "eama-main",
    "subject": "[ESCALATION] '"$ESCALATION_TYPE"': '"$BRIEF_DESCRIPTION"'",
    "priority": "'"$URGENCY"'",
    "content": {
      "type": "escalation",
      "message": "User decision required.\n\n## Category\n'"$ESCALATION_TYPE"'\n\n## Context\n'"$CONTEXT"'\n\n## Options\n'"$OPTIONS_TEXT"'\n\n## Impact\nBlocking task: '"$BLOCKING_TASK"'\n\n## Urgency\n'"$URGENCY"'",
      "data": {
        "escalation_id": "'"$ESCALATION_ID"'",
        "type": "'"$ESCALATION_TYPE"'",
        "blocking_task": "'"$BLOCKING_TASK"'",
        "options": '"$OPTIONS_JSON"'
      }
    }
  }'
```

### Step 3: Update Blocked Task (if applicable)

```bash
if [ -n "$BLOCKING_TASK" ]; then
  # Mark task as blocked
  gh issue edit $BLOCKING_TASK --add-label "status:blocked"
  gh issue edit $BLOCKING_TASK --add-label "blocked:user-decision"

  # Add escalation reference
  gh issue comment $BLOCKING_TASK --body "Blocked pending user decision. Escalation ID: $ESCALATION_ID. Category: $ESCALATION_TYPE"
fi
```

### Step 4: Queue Management

```bash
# Add to escalation queue
echo "$ESCALATION_ID|$ESCALATION_TYPE|$URGENCY|$(date -u +%Y-%m-%dT%H:%M:%SZ)|pending" >> escalation_queue.txt

# Get queue position
QUEUE_POSITION=$(grep -n "pending" escalation_queue.txt | wc -l)
echo "Queue position: $QUEUE_POSITION"
```

## Escalation Message Template

```markdown
## User Decision Required

**Escalation ID**: [ID]
**Category**: [Architecture/Security/Requirements/Dependencies/Scope/Blockers]
**Urgency**: [Normal/High/Urgent]

### Context
[Background information explaining the situation]

### Decision Needed
[Clear statement of what decision is needed]

### Options
1. **Option A**: [Description]
   - Pros: [...]
   - Cons: [...]

2. **Option B**: [Description]
   - Pros: [...]
   - Cons: [...]

### Recommendation
[Orchestrator's recommendation if appropriate, or "No recommendation - requires user judgment"]

### Impact
- Blocking task: #[number] (or "None")
- Affected agents: [list]
- Timeline impact: [description]
```

## Escalation Levels

| Level | Who Handles | Examples |
|-------|-------------|----------|
| Level 0 | Orchestrator | Routine decisions within methodology |
| Level 1 | EAMA (User) | Architecture, requirements, scope |
| Level 2 | User (Direct) | Security, breaking changes, major decisions |

## Success Criteria

- [ ] Escalation ID generated
- [ ] Message sent to EAMA
- [ ] Blocked task updated (if applicable)
- [ ] Queue position recorded
- [ ] Audit log entry created

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| EAMA unreachable | Agent offline | Queue escalation, retry |
| User unavailable | After hours | Queue with urgency flag |
| Duplicate escalation | Same issue raised twice | Dedupe by context hash |

## Tracking Resolution

When user responds:

```bash
# Update escalation status
DECISION="$USER_DECISION"
jq '.status = "resolved" | .decision = "'"$DECISION"'" | .resolved_at = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' \
  "escalation_${ESCALATION_ID}.json" > tmp.json && mv tmp.json "escalation_${ESCALATION_ID}.json"

# Unblock task
if [ -n "$BLOCKING_TASK" ]; then
  gh issue edit $BLOCKING_TASK --remove-label "status:blocked"
  gh issue edit $BLOCKING_TASK --remove-label "blocked:user-decision"
  gh issue edit $BLOCKING_TASK --add-label "status:in-progress"
  gh issue comment $BLOCKING_TASK --body "Unblocked. User decision: $DECISION"
fi

# Notify assigned agent
curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "'"$ASSIGNED_AGENT"'",
    "subject": "Decision Made: '"$ESCALATION_ID"'",
    "priority": "high",
    "content": {
      "type": "decision",
      "message": "User has made a decision on your blocked task.\n\nDecision: '"$DECISION"'\n\nYou may now proceed with task #'"$BLOCKING_TASK"'.",
      "data": {
        "escalation_id": "'"$ESCALATION_ID"'",
        "decision": "'"$DECISION"'",
        "task_id": "'"$BLOCKING_TASK"'"
      }
    }
  }'
```

## Related Operations

- op-handle-blocker-report (in progress-monitoring skill)
- op-poll-agent-progress
