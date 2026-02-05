# AI Maestro Message Templates for EOA

Complete reference for all AI Maestro curl command templates used by Emasoft Orchestrator Agent (EOA).

## Contents

- 1.1 Acknowledging task assignment from ECOS/EAMA
- 1.2 Delegating task to sub-agent (implementer/tester)
- 1.3 Requesting status update from sub-agent
- 1.4 Reporting task completion to ECOS
- 1.5 Escalating blocked task to ECOS
- 1.6 Escalating blocked task to EAMA (user decision needed)
- 1.7 Standard AI Maestro API format and conventions

---

## 1.1 Acknowledging Task Assignment from ECOS/EAMA

**Use case:** When EOA receives a task assignment from ECOS or EAMA, send immediate acknowledgment.

**Incoming message format (from ECOS/EAMA to EOA):**

```json
{
  "from": "ecos-main",
  "to": "eoa-[project-name]",
  "subject": "Task Assignment: [Task Name]",
  "priority": "normal|high|urgent",
  "content": {
    "type": "assignment",
    "message": "Task description and requirements",
    "task_uuid": "UUID",
    "deadline": "ISO8601 timestamp",
    "acceptance_criteria": [
      "Criterion 1",
      "Criterion 2"
    ]
  }
}
```

**EOA acknowledgment curl command:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-[project-name]",
    "to": "ecos-main",
    "subject": "ACK: Task Assignment [Task Name]",
    "priority": "normal",
    "content": {
      "type": "acknowledgment",
      "message": "Task received and logged. UUID: [task-uuid]. Expected completion: [timestamp].",
      "task_uuid": "[task-uuid]",
      "status": "received"
    }
  }'
```

**Key fields:**
- `from`: Your EOA session name (e.g., `eoa-myproject`)
- `to`: Sender's session name (typically `ecos-main`)
- `task_uuid`: Echo back the UUID from the incoming message
- `status`: Always `"received"` for acknowledgments

---

## 1.2 Delegating Task to Sub-Agent

**Use case:** When EOA delegates a task to an implementer, tester, or specialized sub-agent.

**EOA to sub-agent curl command:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-[project-name]",
    "to": "[sub-agent-name]",
    "subject": "Task Assignment: [Task Name]",
    "priority": "normal|high|urgent",
    "content": {
      "type": "assignment",
      "message": "Detailed task description with all context needed",
      "task_uuid": "[task-uuid]",
      "deadline": "[ISO8601 timestamp]",
      "acceptance_criteria": [
        "All tests pass",
        "Documentation updated",
        "Code reviewed"
      ],
      "deliverables": [
        "Completion report",
        "Test results log",
        "Artifacts (if any)"
      ],
      "github_issue": "[issue-url]"
    }
  }'
```

**Expected sub-agent acknowledgment format:**

```json
{
  "from": "[sub-agent-name]",
  "to": "eoa-[project-name]",
  "subject": "ACK: Task Assignment [Task Name]",
  "content": {
    "type": "acknowledgment",
    "message": "Task received and understood. Starting work.",
    "task_uuid": "[task-uuid]",
    "expected_completion": "[timestamp]"
  }
}
```

**Key fields:**
- `to`: Target sub-agent session name (e.g., `svgbbox-impl-01`, `svgbbox-tester-01`)
- `acceptance_criteria`: Array of specific criteria the agent must meet
- `deliverables`: Array of artifacts/reports the agent must provide
- `github_issue`: Link to the GitHub issue tracking this task (if applicable)

---

## 1.3 Requesting Status Update from Sub-Agent

**Use case:** When EOA needs to check progress on a delegated task (e.g., overdue, critical path, user request).

**EOA to sub-agent curl command:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-[project-name]",
    "to": "[sub-agent-name]",
    "subject": "Status Request: [Task Name]",
    "priority": "normal",
    "content": {
      "type": "request",
      "message": "Please provide status update on task [task-uuid]. Expected completion was [timestamp].",
      "task_uuid": "[task-uuid]"
    }
  }'
```

**Expected sub-agent response format:**

```json
{
  "from": "[sub-agent-name]",
  "to": "eoa-[project-name]",
  "subject": "Status Update: [Task Name]",
  "content": {
    "type": "status_update",
    "message": "Current progress summary",
    "task_uuid": "[task-uuid]",
    "progress_percentage": 60,
    "blockers": ["Optional list of blockers"],
    "expected_completion": "[updated-timestamp]"
  }
}
```

**Key fields:**
- `type`: `"request"` for status queries
- `message`: Include original expected completion time for context
- Response `progress_percentage`: Numeric value 0-100
- Response `blockers`: Array (can be empty if no blockers)
- Response `expected_completion`: Updated timestamp if deadline shifted

---

## 1.4 Reporting Task Completion to ECOS

**Use case:** When EOA verifies a delegated task is complete and reports results back to ECOS.

**EOA to ECOS curl command:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-[project-name]",
    "to": "ecos-main",
    "subject": "Task Complete: [Task Name]",
    "priority": "normal",
    "content": {
      "type": "completion",
      "message": "[1-2 line summary]\nKey finding: [one-line summary]\nDetails: docs_dev/orchestration/reports/[task-uuid].md",
      "task_uuid": "[task-uuid]",
      "completion_timestamp": "[ISO8601]",
      "all_criteria_met": true
    }
  }'
```

**Key fields:**
- `type`: `"completion"` for task completion reports
- `message`: Format as shown - summary, key finding, details file path (3 lines max)
- `completion_timestamp`: ISO8601 format (e.g., `2026-02-05T14:30:00Z`)
- `all_criteria_met`: Boolean indicating if all acceptance criteria satisfied

**Message format rules:**
- Line 1: 1-2 line task summary
- Line 2: Key finding (starts with "Key finding: ")
- Line 3: Details file path (starts with "Details: ")
- Total message MUST NOT exceed 3 lines
- Full details written to file, NOT in message body

---

## 1.5 Escalating Blocked Task to ECOS

**Use case:** When EOA encounters a blocker that requires ECOS intervention (agent failure, technical blocker, requirement conflict).

**EOA to ECOS curl command:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-[project-name]",
    "to": "ecos-main",
    "subject": "ESCALATION: [Issue Description]",
    "priority": "urgent",
    "content": {
      "type": "escalation",
      "message": "Escalation reason and details",
      "task_uuid": "[task-uuid]",
      "failed_agent": "[agent-name]",
      "failure_reason": "Specific reason for escalation",
      "attempts": 3,
      "request": "Agent replacement|Technical guidance|User decision"
    }
  }'
```

**Key fields:**
- `priority`: Always `"urgent"` for escalations
- `type`: `"escalation"` for blocked tasks
- `failed_agent`: Session name of agent that failed (if applicable)
- `failure_reason`: Concise description of what went wrong
- `attempts`: Number of retry attempts before escalation
- `request`: Specific action needed from ECOS (choose one):
  - `"Agent replacement"` - Need different agent assigned
  - `"Technical guidance"` - Need technical expertise from ECOS
  - `"User decision"` - Requirement conflict, needs user input

**When to escalate:**
- Agent unresponsive for >4 hours
- Agent failed same task 3+ times
- Technical blocker agent cannot resolve
- Requirement conflict (RULE 14 violation risk)
- Critical path completely blocked

---

## 1.6 Escalating Blocked Task to EAMA (User Decision Needed)

**Use case:** When a task is blocked and requires user input to proceed. This covers situations where:
- A requirement is ambiguous and needs user clarification
- A design choice requires user preference
- A third-party access or credential is needed from the user
- A budget or cost decision must be made by the user
- A feature scope question can only be answered by the user

**EOA to EAMA curl command:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-[project-name]",
    "to": "eama-assistant-manager",
    "subject": "BLOCKER: Task requires user decision",
    "priority": "high",
    "content": {
      "type": "blocker-escalation",
      "message": "[Brief description of the blocker and what user input is needed]",
      "task_uuid": "[task-uuid]",
      "issue_number": "[GitHub issue number]",
      "blocker_type": "user-decision|clarification|access-needed|cost-decision|scope-question",
      "blocker_issue_number": "[GitHub issue number tracking the blocker]",
      "blocker_description": "[Detailed description of what is blocking progress]",
      "impact": "[What work is prevented and which agents are waiting]",
      "options": [
        "Option 1: [description and trade-offs]",
        "Option 2: [description and trade-offs]"
      ],
      "recommended": "Option [N]: [brief reason]",
      "blocked_since": "[ISO8601 timestamp when block was detected]",
      "deadline": "[ISO8601 timestamp if time-sensitive, or null]",
      "request": "User input required to unblock"
    }
  }'
```

**Key fields:**
- `to`: Always `"eama-assistant-manager"` (EAMA's session name)
- `blocker_issue_number`: GitHub issue number of the blocker issue (the separate issue created to track the blocking problem)
- `blocker_type`: Specific type of user decision needed (choose one)
- `blocker_description`: Detailed explanation of the blocking issue
- `impact`: What work is stopped and which agents/tasks are affected
- `options`: Array of possible solutions with trade-offs
- `recommended`: Your recommended option with reasoning
- `blocked_since`: ISO8601 timestamp when blocker was first detected
- `deadline`: ISO8601 timestamp if time-sensitive, or `null` if not
- `request`: Always `"User input required to unblock"`

**Escalation rules:**

| Condition | Action | Priority |
|-----------|--------|----------|
| User decision needed, no deadline | Send with priority `high` | HIGH |
| User decision needed, deadline <48h | Send with priority `urgent` | URGENT |
| User decision needed, deadline <24h | Send with priority `urgent`, add `[URGENT]` to subject | URGENT |
| No user response after 24h | Resend with `urgent` priority | URGENT |
| No user response after 48h | EAMA should proactively remind user | URGENT |

**Response handling:**

When EAMA responds with the user's decision:
1. Update the blocked task's GitHub issue with the decision (add comment)
2. Close the blocker issue (the separate `type:blocker` issue tracking the problem): `gh issue close $BLOCKER_ISSUE --comment "Resolved by user decision: [details]"`
3. Remove `status:blocked` label, restore the previous status label
4. Move card from Blocked column to its PREVIOUS column (not always "In Progress" — could be Testing, Review, etc.)
5. Notify the blocked agent with the resolution via AI Maestro
6. Log the blocker resolution in the issue timeline

---

## 1.7 Standard AI Maestro API Format and Conventions

### Base API Endpoint

```
http://localhost:23000/api/messages
```

### Generic Message Template

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "<sender-session-name>",
    "to": "<recipient-session-name>",
    "subject": "<subject-line>",
    "priority": "normal|high|urgent",
    "content": {
      "type": "<message-type>",
      "message": "<message-body>",
      ...additional fields...
    }
  }'
```

### Required Fields

| Field | Description | Valid Values |
|-------|-------------|--------------|
| `from` | Sender session name | Your EOA session name (e.g., `eoa-myproject`) |
| `to` | Recipient session name | Target agent (e.g., `ecos-main`, `svgbbox-impl-01`) |
| `subject` | Message subject line | String describing message purpose |
| `priority` | Message priority level | `normal`, `high`, `urgent` |
| `content` | Message payload object | JSON object with `type` and `message` |

### Content Field Structure

The `content` field MUST be a JSON object (NOT a string) with:

- `type` (required): Message type identifier
  - `assignment` - Task assignment
  - `acknowledgment` - ACK/confirmation
  - `request` - Information request
  - `status_update` - Progress update
  - `completion` - Task completion report
  - `escalation` - Issue escalation
- `message` (required): Human-readable message text
- Additional fields as needed (task_uuid, deadline, etc.)

### Session Name Format

EOA session names follow the pattern: `eoa-[project-name]`

Examples:
- `eoa-svgbbox` - EOA for svgbbox project
- `eoa-myapp` - EOA for myapp project

Sub-agent session names follow: `[project]-[role]-[number]`

Examples:
- `svgbbox-impl-01` - Implementer #1 for svgbbox
- `svgbbox-tester-02` - Tester #2 for svgbbox
- `myapp-debugger-01` - Debugger #1 for myapp

### Priority Levels

| Priority | Use Case |
|----------|----------|
| `normal` | Routine task assignments, acknowledgments, status updates |
| `high` | Deadline-critical tasks, overdue status requests |
| `urgent` | Escalations, blockers, requirement conflicts |

### Message Subject Conventions

- **Task Assignment:** `"Task Assignment: [Task Name]"`
- **Acknowledgment:** `"ACK: Task Assignment [Task Name]"` or `"ACK: [Subject]"`
- **Status Request:** `"Status Request: [Task Name]"`
- **Status Update:** `"Status Update: [Task Name]"`
- **Completion:** `"Task Complete: [Task Name]"`
- **Escalation:** `"ESCALATION: [Issue Description]"`

### Error Handling

If curl command fails:
1. Check AI Maestro service is running: `curl http://localhost:23000/health`
2. Verify session names are correct (no typos)
3. Validate JSON syntax (use `jq` to check)
4. Check network connectivity to localhost
5. Retry once, then escalate to ECOS if persistent

### Testing Messages

To test AI Maestro connectivity:

```bash
# Check if AI Maestro is running
curl -s "http://localhost:23000/health"

# Expected response:
{"status":"ok","version":"1.0.0"}

# List unread messages
curl -s "http://localhost:23000/api/messages?agent=eoa-myproject&action=list&status=unread" | jq '.'

# Get unread count
curl -s "http://localhost:23000/api/messages?agent=eoa-myproject&action=unread-count"
```

---

## Quick Reference: Common Patterns

### ACK Pattern (All Messages)

**Always send acknowledgment after receiving any message:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-[project-name]",
    "to": "[sender]",
    "subject": "ACK: [Original Subject]",
    "priority": "normal",
    "content": {
      "type": "acknowledgment",
      "message": "[Brief confirmation message]",
      "task_uuid": "[task-uuid if applicable]",
      "status": "[received|understood|in_progress]"
    }
  }'
```

### Minimal Report Pattern (All Responses to ECOS)

**Always keep reports to ECOS under 3 lines:**

```
[1-2 line task summary]
Key finding: [one-line summary]
Details: [filepath to detailed report]
```

Example:
```
Task XYZ completed successfully. All tests passing.
Key finding: Performance improved 30% after optimization.
Details: docs_dev/orchestration/reports/task-uuid-123.md
```

### Task UUID Tracking

**Always include task_uuid in all messages related to a task:**

- Initial assignment from ECOS → includes UUID
- EOA ACK → echo back UUID
- Delegation to sub-agent → pass UUID
- Sub-agent ACK → echo back UUID
- Status requests → include UUID
- Status updates → include UUID
- Completion report → include UUID
- Escalations → include UUID

This ensures full traceability across the task lifecycle.

---

## Notes

- All timestamps use ISO8601 format (e.g., `2026-02-05T14:30:00Z`)
- Message `content` MUST be an object, NOT a string
- Session names are case-sensitive
- Priority `urgent` should be reserved for genuine urgent situations
- Always wait for ACK after sending (timeout: 15 minutes)
- If no ACK received, retry once, then escalate to ECOS
