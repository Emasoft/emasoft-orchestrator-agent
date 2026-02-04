# AI Maestro Communication Examples

This document provides complete curl command examples for common AI Maestro messaging scenarios.

## Table of Contents

- [Full Task Assignment Flow](#full-task-assignment-flow)
- [Example 1: Send Task Assignment](#example-1-send-task-assignment)
- [Example 2: Send Status Request](#example-2-send-status-request)
- [Example 3: Escalate to Assistant Manager](#example-3-escalate-to-assistant-manager)

---

## Full Task Assignment Flow

```
1. EAMA receives user request
2. EAMA creates project, spawns ECOS
3. ECOS spawns EOA for project
4. EOA receives requirements from EAA (via ECOS)
5. EOA breaks down into tasks
6. EOA assigns tasks to agents using message template 2.1
7. Agents report progress using template 2.4
8. Agents report completion using template 2.2
9. EOA requests EIA verification using template 2.10
10. EIA reports result using template 2.11
11. EOA reports to ECOS
12. ECOS reports to EAMA
13. EAMA reports to user
```

---

## Example 1: Send Task Assignment

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "implementer-1",
    "subject": "Task Assignment: Implement auth module",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "You are assigned: Implement authentication module. Success criteria: JWT tokens, session management, tests passing.",
      "data": {
        "task_id": "auth-core",
        "issue_number": "42",
        "handoff_doc": "docs_dev/handoffs/auth-core.md"
      }
    }
  }'
```

---

## Example 2: Send Status Request

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "implementer-1",
    "subject": "Status Request: #42",
    "priority": "normal",
    "content": {
      "type": "request",
      "message": "What is your current status on #42? Report progress, blockers, and next steps.",
      "data": {
        "task_id": "42"
      }
    }
  }'
```

---

## Example 3: Escalate to Assistant Manager

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "assistant-manager",
    "subject": "Approval Required: Requirement Change",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Implementer identified issue with immutable requirement. User decision required.",
      "data": {
        "operation": "requirement_change",
        "risk_level": "high",
        "justification": "Current requirement infeasible with available APIs"
      }
    }
  }'
```
