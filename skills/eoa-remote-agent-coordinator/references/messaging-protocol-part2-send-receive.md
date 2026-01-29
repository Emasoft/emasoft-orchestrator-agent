# Messaging Protocol Part 2: Sending and Receiving Messages


## Contents

- [2.1 Basic Send Syntax](#21-basic-send-syntax)
  - [Command Syntax](#command-syntax)
  - [Parameters](#parameters)
  - [Basic Example](#basic-example)
- [2.2 Send with Task Assignment](#22-send-with-task-assignment)
  - [Simple Task Assignment](#simple-task-assignment)
  - [Using Heredoc for Complex Content](#using-heredoc-for-complex-content)
- [2.3 Check Inbox Command](#23-check-inbox-command)
  - [List All Unread Messages](#list-all-unread-messages)
  - [Example Output](#example-output)
- [2.4 Read and Mark Message as Read](#24-read-and-mark-message-as-read)
  - [Command Syntax](#command-syntax)
  - [Example](#example)
  - [Example Output](#example-output)
- [2.5 Workflow Example](#25-workflow-example)
  - [Complete Send-Receive-Respond Flow](#complete-send-receive-respond-flow)
- [Related Sections](#related-sections)

---

**Parent document**: [messaging-protocol.md](messaging-protocol.md)

---

## 2.1 Basic Send Syntax

**Use the official CLI:** `send-aimaestro-message.sh` (see `~/.claude/skills/agent-messaging/SKILL.md`)

### Command Syntax

```bash
send-aimaestro-message.sh <to> <subject> <message> [priority] [type]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `to` | YES | Recipient's full session name |
| `subject` | YES | Brief subject line |
| `message` | YES | Message content (string or JSON) |
| `priority` | NO | `low`, `normal`, `high`, or `urgent` (default: `normal`) |
| `type` | NO | Message type (default: `task`) |

### Basic Example

```bash
send-aimaestro-message.sh dev-agent-1 "Status check" "How is GH-42 progressing?" normal status-request
```

---

## 2.2 Send with Task Assignment

For complex JSON content, use a variable or heredoc:

### Simple Task Assignment

```bash
send-aimaestro-message.sh dev-agent-1 \
  "Implement Feature GH-42" \
  '{"type":"task","task_id":"GH-42","instructions":"Complete implementation of user authentication","completion_criteria":["All tests pass","PR created"],"report_back":true}' \
  high task
```

### Using Heredoc for Complex Content

```bash
MESSAGE=$(cat <<'EOF'
{
  "type": "task",
  "task_id": "GH-42",
  "instructions": "Implement user authentication with OAuth2 support",
  "completion_criteria": [
    "All unit tests pass",
    "Integration tests pass",
    "PR created with description",
    "No linting errors"
  ],
  "test_requirements": [
    "test_auth_login",
    "test_auth_logout",
    "test_oauth_flow"
  ],
  "report_back": true
}
EOF
)

send-aimaestro-message.sh dev-agent-1 "Implement Auth GH-42" "$MESSAGE" high task
```

---

## 2.3 Check Inbox Command

**Use the official CLI:** `check-aimaestro-messages.sh`

### List All Unread Messages

```bash
check-aimaestro-messages.sh
```

### Example Output

```
Unread messages (3):
  1. msg-1767802409759-h3x4ajo from orchestrator-master: "GH-42 Task Assignment" (high)
  2. msg-1767802512345-abc1234 from reviewer-security: "Security Review Request" (normal)
  3. msg-1767802601234-xyz5678 from dev-agent-2: "Dependency Question" (low)
```

---

## 2.4 Read and Mark Message as Read

**Use the official CLI:** `read-aimaestro-message.sh`

### Command Syntax

```bash
read-aimaestro-message.sh <message-id>
```

### Example

```bash
read-aimaestro-message.sh msg-1767802409759-h3x4ajo
```

### Example Output

```
Message: msg-1767802409759-h3x4ajo
From: orchestrator-master
Subject: GH-42 Task Assignment
Priority: high
Sent: 2025-12-30T10:00:00Z

Content:
{
  "type": "task",
  "task_id": "GH-42",
  "instructions": "Implement user authentication with OAuth2 support",
  "completion_criteria": ["All tests pass", "PR created"],
  "report_back": true
}

[Message marked as read]
```

---

## 2.5 Workflow Example

### Complete Send-Receive-Respond Flow

**Step 1: Orchestrator sends task**
```bash
send-aimaestro-message.sh dev-agent-1 "GH-42 Implementation" \
  '{"type":"task","task_id":"GH-42","instructions":"Implement feature X"}' \
  high task
```

**Step 2: Agent checks inbox**
```bash
check-aimaestro-messages.sh
# Output: 1 unread message from orchestrator-master
```

**Step 3: Agent reads message**
```bash
read-aimaestro-message.sh msg-1767802409759-h3x4ajo
# Displays full message content, marks as read
```

**Step 4: Agent sends acknowledgment**
```bash
send-aimaestro-message.sh orchestrator-master "ACK: GH-42" \
  '{"type":"task-acknowledgment","task_id":"GH-42","understood":true,"estimated_completion":"2h"}' \
  normal ack
```

---

## Related Sections

- [Part 1: API and Schema](messaging-protocol-part1-api-schema.md) - Message format details
- [Part 3: Message Types](messaging-protocol-part3-message-types.md) - Content schemas for each message type
- [Part 5: Response Expectations](messaging-protocol-part5-notifications-responses.md) - What responses are expected
