---
name: eoa-task-distribution
description: Task distribution based on skills and availability. Use when assigning work to agents, balancing load, or resolving dependencies. Trigger with assignment requests.
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Anthropic
  version: 1.0.0
context: fork
agent: eoa-main
---

# Task Distribution Skill

## Overview

This skill defines how the Orchestrator (EOA) distributes tasks to agents. Distribution is based on **order**, **priority**, and **agent state** - not arbitrary timing. Tasks are selected from the ready queue, sorted by priority, filtered by dependencies, matched to agent capabilities, and assigned via labeled issues and AI Maestro messages.

## Prerequisites

1. Read **AGENT_OPERATIONS.md** for orchestrator workflow
2. Read **eoa-label-taxonomy** for label usage and cardinality rules
3. Read **eoa-messaging-templates** for message formats
4. Access to GitHub CLI (`gh`) and AI Maestro API
5. Understanding of agent states (active, hibernated, offline)

---

## 1. Task Distribution Order

Tasks are distributed following this order:

| Step | Action | Condition |
|------|--------|-----------|
| 1 | Identify ready tasks | Tasks with `status:ready` label |
| 2 | Sort by priority | `priority:critical` > `priority:high` > `priority:normal` > `priority:low` |
| 3 | Check dependencies | Task's blockedBy list is empty |
| 4 | Select agent | Match task requirements to available agents |
| 5 | Assign task | Add `assign:<agent>` label, send AI Maestro message |

---

## 2. Agent Selection Criteria

When selecting an agent for a task, evaluate in this order:

### 2.1 Availability Check

| State | Can Assign | Action |
|-------|------------|--------|
| Active, no current task | Yes | Assign immediately |
| Active, has current task | Maybe | Check if at capacity |
| Hibernated | No | Wake first or select different agent |
| Offline | No | Select different agent |

### 2.2 Skill Match

Match task requirements (`toolchain:*`, `component:*` labels) to agent capabilities:

```
Task labels: toolchain:python, component:api
Agent skills: python, api, testing

Match score: 2/2 required = 100% match
```

### 2.3 Capacity Check

| Agent Load | Can Assign |
|------------|------------|
| 0 active tasks | Yes |
| 1-2 active tasks | Yes, if high priority |
| 3+ active tasks | No, agent at capacity |

---

## 3. Assignment Protocol

### 3.1 Update Labels

```bash
# Remove any existing assign:* label first
gh issue view $ISSUE --json labels | jq -r '.labels[].name' | grep '^assign:' | while read label; do
  gh issue edit $ISSUE --remove-label "$label"
done

# Add new assignment
gh issue edit $ISSUE --add-label "assign:$AGENT_NAME"

# Update status
gh issue edit $ISSUE --remove-label "status:ready" --add-label "status:in-progress"
```

### 3.2 Send Assignment Message

Use template from eoa-messaging-templates (section 2.1):

```json
{
  "from": "orchestrator",
  "to": "<agent-name>",
  "subject": "Task Assignment: <task-title>",
  "priority": "high",
  "content": {
    "type": "request",
    "message": "You are assigned: <task-description>. Success criteria: <criteria>. Report status when starting and when complete.",
    "data": {
      "task_id": "<task-id>",
      "issue_number": "<github-issue-number>",
      "handoff_doc": "docs_dev/handoffs/<handoff-filename>.md"
    }
  }
}
```

### 3.3 Wait for ACK

After sending assignment, wait for agent acknowledgment. See **eoa-progress-monitoring** for response handling.

---

## 4. Dependency Management

### 4.1 Dependency Types

| Type | Example | Handling |
|------|---------|----------|
| Hard | Module B needs Module A's API | Block B until A complete |
| Soft | Testing can start with stubs | Assign with note about dependency |
| None | Independent tasks | Assign in parallel |

### 4.2 Dependency Resolution

```
Task A: status:in-progress, blocks: [B, C]
Task B: status:ready, blockedBy: [A] → Cannot assign yet
Task C: status:ready, blockedBy: [A] → Cannot assign yet

When Task A completes:
- Update A: status:done
- B and C become assignable
```

### 4.3 Circular Dependency Detection

If detected, STOP and report to user:

```
CIRCULAR DEPENDENCY:
Task A → depends on → Task B
Task B → depends on → Task A

Cannot proceed. User decision required.
```

---

## 5. Load Balancing

### 5.1 Even Distribution

When multiple agents can handle a task:

1. Check current load (active tasks per agent)
2. Prefer agent with lowest load
3. If equal load, prefer agent who completed similar tasks recently

### 5.2 Specialization

Some tasks benefit from agent specialization:

| Task Type | Preferred Agent |
|-----------|-----------------|
| Code review | Agent who wrote the code (context) |
| Bug fix | Agent who implemented feature |
| New feature | Agent with matching skills |

---

## 6. Reassignment

When reassigning a task (agent unresponsive or blocked):

1. Remove current `assign:*` label
2. Add `assign:<new-agent>` label
3. Send reassignment message to new agent with context
4. Notify original agent: "Task reassigned"
5. Include any partial progress from original agent

---

## Instructions

Follow these steps to distribute tasks to agents:

1. Query all issues with `status:ready` label
2. Sort ready tasks by priority (critical > high > normal > low)
3. For each task in priority order:
   1. Check if dependencies are resolved (blockedBy list is empty)
   2. If blocked, skip to next task
   3. If ready, evaluate available agents for skill match
   4. Select agent with best match score and lowest current load
   5. Remove any existing `assign:*` label from the issue
   6. Add `assign:<agent-name>` label to the issue
   7. Update issue status from `status:ready` to `status:in-progress`
   8. Send task assignment message via AI Maestro (see section 3.2)
   9. Wait for agent ACK before considering next task
   10. Log assignment in delegation log file

### Checklist

Copy this checklist and track your progress:

**Task Distribution Workflow:**
- [ ] Query all issues with `status:ready` label
- [ ] Sort ready tasks by priority (critical > high > normal > low)
- [ ] Check if task dependencies are resolved (blockedBy list empty)
- [ ] If blocked, skip to next task
- [ ] Evaluate available agents for skill match
- [ ] Check agent availability (active, hibernated, offline)
- [ ] Check agent capacity (0-2 tasks acceptable, 3+ at capacity)
- [ ] Select agent with best match score and lowest load
- [ ] Remove any existing `assign:*` label from the issue
- [ ] Add `assign:<agent-name>` label to the issue
- [ ] Update issue status from `status:ready` to `status:in-progress`
- [ ] Send task assignment message via AI Maestro
- [ ] Wait for agent ACK before considering next task
- [ ] Log assignment in delegation log file

---

## Output

| Output Type | Format | Example |
|-------------|--------|---------|
| Assignment confirmation | GitHub label + AI Maestro message | `assign:implementer-1` label + ACK message received |
| Task queue report | Markdown table | List of ready tasks sorted by priority |
| Agent availability report | JSON | `{"agent": "impl-01", "load": 1, "state": "active"}` |
| Dependency graph | Text or diagram | Task A blocks [B, C], Task D ready |
| Delegation log entry | Timestamped text | `2024-01-15T10:30:00Z: Assigned #42 to implementer-1` |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No available agents | All agents at capacity or offline | Wait for agent capacity or escalate to user |
| Circular dependency detected | Task A blocks B, B blocks A | Report to user for manual resolution |
| Agent does not ACK assignment | Agent unresponsive or hibernated | Send reminder, then escalate to **eoa-progress-monitoring** |
| Skill mismatch | No agent has required toolchain | Escalate to user or reassign with training |
| Dependency never completes | Blocking task stuck | Escalate to **eoa-progress-monitoring** for blocker resolution |
| Label conflict (multiple assign:*) | Concurrent update | Remove all `assign:*` labels, reapply correct one |

---

## Examples

### Example 1: Query and Sort Ready Tasks

```bash
# Get all ready tasks as JSON
gh issue list --label "status:ready" --json number,title,labels,createdAt | \
  jq 'sort_by(
    .labels[] | select(.name | startswith("priority:")) | .name |
    if . == "priority:critical" then 0
    elif . == "priority:high" then 1
    elif . == "priority:normal" then 2
    else 3 end
  )'
```

### Example 2: Check Agent Availability via AI Maestro

```bash
# Query agent's current task count
curl -s "$AIMAESTRO_API/api/agents/implementer-1/status" | jq '.active_tasks'

# Check agent's last seen timestamp
curl -s "$AIMAESTRO_API/api/agents/implementer-1" | jq '.last_seen'
```

### Example 3: Assign Task with Full Protocol

```bash
ISSUE=42
AGENT="implementer-1"

# 1. Remove existing assignment
gh issue view $ISSUE --json labels | jq -r '.labels[] | select(.name | startswith("assign:")) | .name' | \
  xargs -I {} gh issue edit $ISSUE --remove-label "{}"

# 2. Add new assignment
gh issue edit $ISSUE --add-label "assign:$AGENT"

# 3. Update status
gh issue edit $ISSUE --remove-label "status:ready" --add-label "status:in-progress"

# 4. Send AI Maestro message
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d "{
    \"from\": \"orchestrator\",
    \"to\": \"$AGENT\",
    \"subject\": \"Task Assignment: Implement feature X\",
    \"priority\": \"high\",
    \"content\": {
      \"type\": \"request\",
      \"message\": \"You are assigned issue #$ISSUE. Success criteria: implement X, pass tests. Report when complete.\",
      \"data\": {
        \"issue_number\": $ISSUE
      }
    }
  }"
```

### Example 4: Handle Circular Dependency

```bash
# Detect circular dependency
TASK_A_BLOCKS=$(gh issue view 10 --json body | jq -r '.body | match("blocks: \\[([0-9, ]+)\\]") | .captures[0].string')
TASK_B_BLOCKS=$(gh issue view 11 --json body | jq -r '.body | match("blocks: \\[([0-9, ]+)\\]") | .captures[0].string')

# If A blocks B and B blocks A:
if echo "$TASK_A_BLOCKS" | grep -q "11" && echo "$TASK_B_BLOCKS" | grep -q "10"; then
  echo "CIRCULAR DEPENDENCY DETECTED: #10 ↔ #11"
  echo "User intervention required to break cycle."
  # Report to user via EAMA
fi
```

---

## Resources

- **AGENT_OPERATIONS.md** - Core orchestrator workflow
- **eoa-label-taxonomy** - Label categories and cardinality rules
- **eoa-messaging-templates** - Message templates for task assignment
- **eoa-progress-monitoring** - Agent state tracking and escalation
- **eoa-implementer-interview-protocol** - Pre-task and post-task verification
