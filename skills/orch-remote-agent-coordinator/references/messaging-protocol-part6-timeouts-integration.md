# Messaging Protocol Part 6: Timeouts and Protocol Integration

**Parent document**: [messaging-protocol.md](messaging-protocol.md)

---

## 6.1 Response Timeouts by Priority Level

| Priority | Initial Timeout | Retry Timeout | Max Wait |
|----------|-----------------|---------------|----------|
| `urgent` | 2 min | 1 min | 3 min |
| `high` | 5 min | 2.5 min | 7.5 min |
| `normal` | 10 min | 5 min | 15 min |
| `low` | 30 min | 15 min | 45 min |

### Timeout Calculation

```
Max Wait = Initial Timeout + Retry Timeout
```

---

## 6.2 Timeout Flow

### First Timeout (at Initial Timeout)

When no response received within initial timeout:

1. **Log timeout event** - Record in task tracking
2. **Retry message once** - Add `retry: true` flag
3. **Wait for retry timeout** - Shorter than initial

### Second Timeout (after Retry)

When still no response after retry:

1. **Mark message as undelivered**
2. **Mark recipient agent as potentially unresponsive**
3. **Escalate to orchestrator/user**
4. **Consider reassigning work** - For critical tasks

### Timeline Example

```
T+0s:    Send task-assignment (priority: normal)
         ├── Initial timeout: 10 min
T+600s:  No response → Retry task-assignment
         ├── Retry timeout: 5 min
T+900s:  No response → Mark agent unresponsive, reassign task
```

---

## 6.3 Retry Message Format

When retrying a message, include metadata about the retry:

```json
{
  "to": "dev-agent-1",
  "subject": "RETRY: GH-42 Task Assignment",
  "priority": "high",
  "metadata": {
    "retry": true,
    "original_message_id": "msg-123",
    "original_sent_at": "2025-12-31T10:00:00Z",
    "retry_count": 1
  },
  "content": {
    "type": "task",
    "task_id": "GH-42",
    "message": "Please acknowledge task assignment. This is a retry of the original message."
  }
}
```

### Retry Rules

| Rule | Description |
|------|-------------|
| Increase priority | Retry at one level higher priority |
| Add RETRY prefix | Make subject line obvious |
| Include original ID | For tracking and deduplication |
| Limit retries | Maximum 1-2 retries |

---

## 6.4 Integration with Other Protocols

This messaging protocol is the **transport layer** for all other protocols in the ATLAS-ORCHESTRATOR system.

### Related Protocol Documents

| Protocol | Purpose |
|----------|---------|
| `echo-acknowledgment-protocol.md` | Task acknowledgment messages |
| `task-instruction-format.md` | Task assignment message content |
| `test-report-format.md` | Test report message content |
| `artifact-sharing-protocol.md` | Artifact request/response messages |
| `change-notification-protocol.md` | Configuration change messages |

All protocol-specific message types use this messaging format as the envelope.

---

## 6.5 Protocol Hierarchy Diagram

```
messaging-protocol.md (envelope/transport)
├── echo-acknowledgment-protocol.md (task lifecycle)
├── task-instruction-format.md (task content)
├── test-report-format.md (test results content)
├── artifact-sharing-protocol.md (artifact exchange)
└── change-notification-protocol.md (config updates)
```

### How Protocols Relate

1. **Messaging Protocol** - Defines the envelope (to, from, subject, content)
2. **Content Protocols** - Define what goes inside `content` field
3. **Workflow Protocols** - Define expected sequences of messages

---

## 6.6 Message Type Registry

| Protocol | Message Types |
|----------|---------------|
| messaging-protocol | `task`, `status-request`, `progress-update`, `approval`, `rejection`, `escalation`, `escalation-response` |
| echo-acknowledgment | `task-acknowledgment`, `needs-clarification` |
| task-instruction | `completion-report` |
| test-report | `test-report`, `test-report-ack` |
| artifact-sharing | `artifact-share`, `artifact-request`, `artifact-response` |
| change-notification | `change-notification`, `change-acknowledgment` |

### Message Type Namespacing

Message types are unique across protocols. When sending a message, use the type directly:

```json
{
  "content": {
    "type": "task-acknowledgment",
    "task_id": "GH-42",
    "understood": true
  }
}
```

No protocol prefix needed - the `type` field is globally unique.

---

## Related Sections

- [Part 1: API and Schema](messaging-protocol-part1-api-schema.md) - Message envelope format
- [Part 5: Response Expectations](messaging-protocol-part5-notifications-responses.md) - What responses each type expects
- [Part 7: Troubleshooting](messaging-protocol-part7-troubleshooting.md) - Timeout problems
