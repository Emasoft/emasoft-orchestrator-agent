# Operation: Notify Orchestrator

---
procedure: proc-complete-task
workflow-instruction: Step 19 - Task Completion
operation-id: op-notify-orchestrator
---

## Purpose

Send verification results and test reports to orchestrator via AI Maestro messaging.

## When to Use

- After completing test execution
- When tests finish in CI/CD
- To alert orchestrator of verification failures
- To trigger next workflow step after successful verification

## Prerequisites

- AI Maestro server is running
- Verification results are ready
- Agent session name is known
- Network connectivity to AI Maestro

## Steps

### Step 1: Prepare Notification Content

Assemble the notification with test results:

```json
{
  "type": "verification-complete",
  "task_id": "GH-42",
  "status": "passed",
  "summary": {
    "total": 45,
    "passed": 42,
    "failed": 2,
    "skipped": 1
  },
  "report_path": "artifacts/tests/pytest-report.json"
}
```

### Step 2: Send via AI Maestro

Using testing protocol with notification:

```bash
python shared/testing_protocol.py \
  --pytest tests/ \
  --notify \
  --branch feature-xyz \
  --output test-results.json
```

Or direct API call:

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "Verification Complete: GH-42",
    "priority": "high",
    "content": {
      "type": "verification-complete",
      "task_id": "GH-42",
      "status": "passed",
      "message": "[TESTS] 45 total: 42 passed, 2 failed, 1 skipped (12.5s)"
    }
  }'
```

### Step 3: Wait for Acknowledgment

Orchestrator responds with next action:

**On Pass:**
```json
{
  "type": "test-report-ack",
  "task_id": "GH-42",
  "status": "approved",
  "message": "All tests passed. Proceed to PR creation.",
  "next_action": "create-pr"
}
```

**On Fail:**
```json
{
  "type": "test-report-ack",
  "task_id": "GH-42",
  "status": "rejected",
  "message": "Fix 2 failing tests before proceeding",
  "required_actions": [
    "Fix test_auth.py:45 - assertion failed",
    "Fix test_api.py:89 - timeout exceeded"
  ],
  "next_action": "fix-and-rerun"
}
```

## Notification Content

Notification must include:

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | `verification-complete` |
| `task_id` | Yes | Task being verified |
| `status` | Yes | `passed`, `failed`, `error` |
| `summary` | Yes | Test counts (total, passed, failed, skipped) |
| `report_path` | No | Path to full report |
| `branch` | No | Git branch name |
| `timestamp` | No | When verification completed |
| `error_details` | Conditional | Required if status is failed/error |

## Minimal Summary Format

For orchestrator consumption:

```
[TESTS] 45 total: 42 passed, 2 failed, 1 skipped (12.5s)
FAILED: test_auth.py:45, test_api.py:89
COVERAGE: 85% lines, 72% branches
```

## Progress Updates

For long-running test suites, send progress updates:

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "Test Progress: GH-42",
    "priority": "normal",
    "content": {
      "type": "progress-update",
      "task_id": "GH-42",
      "phase": "running-tests",
      "progress_percent": 50,
      "details": "5000/10000 tests complete, 2 failures so far"
    }
  }'
```

## Additional Attempts Request

If more time is needed:

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "Extension Request: GH-42",
    "priority": "high",
    "content": {
      "type": "additional-attempts-request",
      "task_id": "GH-42",
      "requested_additional_attempts": 3,
      "reason": "Integration tests running (10k+ tests)",
      "current_progress": "80% complete"
    }
  }'
```

## Troubleshooting

### Notification Not Delivered

1. Verify AI Maestro is running:
   ```bash
   curl $AIMAESTRO_API/api/health
   ```

2. Check agent session name is correct

3. Verify network connectivity

4. Check message format matches schema

5. Review AI Maestro logs for errors

### Notification Format

| Issue | Cause | Solution |
|-------|-------|----------|
| Message rejected | Invalid JSON | Validate JSON format |
| Agent not found | Wrong session name | Use full session name (domain-subdomain-name) |
| Timeout | Network issue | Check connectivity, retry |

## Exit Criteria

This operation is complete when:
- [ ] Notification content prepared with all required fields
- [ ] Message sent to orchestrator via AI Maestro
- [ ] Acknowledgment received (or timeout handled)
- [ ] Next action determined from response
- [ ] Follow-up action initiated (if needed)

## Related Operations

- [op-run-test-suite.md](./op-run-test-suite.md) - Running tests that produce results
- [op-format-verification-report.md](./op-format-verification-report.md) - Creating report to send
- [op-generate-test-report.md](./op-generate-test-report.md) - Standard test report format
- [op-update-github-issue.md](./op-update-github-issue.md) - Updating GitHub with results
