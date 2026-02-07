---
procedure: proc-execute-task
workflow-instruction: Step 17 - Task Execution
operation: verify-aimaestro-availability
---

# Operation: Verify AI Maestro Availability

## Purpose

Verify that the AI Maestro messaging system is running and accessible before attempting task delegation.

## When to Use

- Before any task delegation to remote agents
- At session start when orchestrator begins work
- After network connectivity issues
- Before overnight autonomous operation

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| AIMAESTRO_API | Environment variable | Yes (default: http://localhost:23000) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| availability_status | Boolean | True if API is healthy |
| error_message | String | Error details if unavailable |

## Steps

### Step 1: Check API Health Endpoint

```bash
# Check AI Maestro health
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${AIMAESTRO_API:-http://localhost:23000}/api/health")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
  echo "AI Maestro is healthy"
else
  echo "AI Maestro unavailable: HTTP $HTTP_CODE"
  exit 1
fi
```

### Step 2: Verify Agent Registry Access

```bash
# List registered agents
AGENTS=$(curl -s "${AIMAESTRO_API:-http://localhost:23000}/api/agents")
AGENT_COUNT=$(echo "$AGENTS" | jq '.agents | length')

if [ "$AGENT_COUNT" -gt 0 ]; then
  echo "Agent registry accessible: $AGENT_COUNT agents registered"
else
  echo "WARNING: No agents registered in AI Maestro"
fi
```

### Step 3: Test Message Send Capability

```bash
# Send test ping to self (optional validation)
curl -X POST "${AIMAESTRO_API:-http://localhost:23000}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "orchestrator",
    "subject": "Health Check Ping",
    "priority": "low",
    "content": {"type": "ping", "message": "Self-test"}
  }'
```

## Success Criteria

- [ ] Health endpoint returns HTTP 200
- [ ] Agent registry is accessible
- [ ] At least one remote agent is registered (for delegation)

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | AI Maestro not running | Start AI Maestro service |
| HTTP 500 | AI Maestro internal error | Check AI Maestro logs |
| No agents registered | Agents not onboarded | Complete agent onboarding first |

## Related Operations

- op-send-task-delegation
- op-poll-agent-progress
