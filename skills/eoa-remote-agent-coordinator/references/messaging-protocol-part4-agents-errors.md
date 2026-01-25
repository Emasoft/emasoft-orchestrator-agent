# Messaging Protocol Part 4: Agents, Errors, and Best Practices

**Parent document**: [messaging-protocol.md](messaging-protocol.md)

---

## 4.1 Agent Identification

### Session Name Format

Use domain hierarchy format: `domain-subdomain-name`

| Full Session Name | Domain | Subdomain | Name | Role |
|-------------------|--------|-----------|------|------|
| `orchestrator-master` | orchestrator | - | master | Main orchestrator |
| `dev-agent-python` | dev-agent | - | python | Python developer |
| `dev-agent-frontend` | dev-agent | - | frontend | Frontend developer |
| `reviewer-security` | reviewer | - | security | Security reviewer |
| `libs-svg-svgbbox` | libs | svg | svgbbox | SVG library agent |

**Rule**: Always use full session names in orchestrator messages for clarity.

---

## 4.2 Resolving Agent Names

The API automatically resolves multiple formats:

| Format | Example | Description |
|--------|---------|-------------|
| Full session name | `libs-svg-svgbbox` | Recommended for clarity |
| Alias | `svgbbox` | Short form (may be ambiguous) |
| UUID | `550e8400-e29b-41d4-a716-446655440000` | System identifier |

### Best Practice

Always use full session names when sending messages. Aliases may be ambiguous if multiple agents have similar names.

```bash
# Good
send-aimaestro-message.sh libs-svg-svgbbox "Subject" "Message"

# Avoid (ambiguous)
send-aimaestro-message.sh svgbbox "Subject" "Message"
```

---

## 4.3 API Error Codes

| Status | Meaning | Action |
|--------|---------|--------|
| 200 | Success | Message sent/retrieved |
| 400 | Bad request | Check message format (see 4.3.1) |
| 404 | Agent not found | Verify agent is online (see 4.3.2) |
| 500 | Server error | Retry after 30 seconds |

### 4.3.1 Fixing 400 Errors

Common causes:
- `content` is a string instead of an object
- Missing required fields (`to`, `subject`, `content`)
- Invalid `priority` value
- Malformed JSON

**Validate JSON before sending:**
```bash
echo '{"type":"task","message":"test"}' | jq .
```

### 4.3.2 Fixing 404 Errors

1. List all registered agents:
   ```bash
   curl $AIMAESTRO_API/api/agents
   ```
2. Verify exact session name spelling (case-sensitive)
3. Check if agent session has expired
4. Wait for agent re-registration if recently restarted

---

## 4.4 Message Delivery Failure Handling

When a message cannot be delivered:

1. **API returns error status** - Log the error
2. **Orchestrator logs failed delivery** - Record in task log
3. **Retry up to 3 times** - Use exponential backoff:
   - Retry 1: Wait 5 seconds
   - Retry 2: Wait 15 seconds
   - Retry 3: Wait 45 seconds
4. **Mark agent as potentially offline** - Update agent status
5. **Reassign task if critical** - For urgent/high priority tasks

### Retry Example

```bash
for i in 1 2 3; do
  if send-aimaestro-message.sh agent "Subject" "Message"; then
    break
  fi
  sleep $((5 * 3 ** (i-1)))
done
```

---

## 4.5 Message Size Best Practices

| Guideline | Limit |
|-----------|-------|
| Maximum message size | 100KB |
| Recommended size | Under 10KB |
| Large content handling | Reference external files |

### Handling Large Content

Instead of embedding large content:

```json
{
  "type": "task",
  "task_id": "GH-42",
  "instructions": "See GitHub issue for full specification",
  "reference_url": "https://github.com/org/repo/issues/42",
  "reference_files": [
    "docs/spec.md",
    "designs/mockup.png"
  ]
}
```

---

## 4.6 Subject Line Formatting

### Format Guidelines

| Element | Example |
|---------|---------|
| Include task ID | `"GH-42: Implement user auth"` |
| Include type prefix | `"FIX: Missing null check in GH-42"` |
| Include urgency | `"URGENT: Security issue in GH-42"` |
| Be concise | Max 80 characters |

### Subject Line Prefixes

| Prefix | Use When |
|--------|----------|
| `GH-XX:` | New task assignment |
| `FIX:` | Requesting fixes |
| `ACK:` | Acknowledging receipt |
| `DONE:` | Task completion |
| `URGENT:` | Immediate attention needed |
| `RETRY:` | Retry of previous message |
| `RE:` | Response to previous message |

---

## 4.7 Content Structure Requirements

### Always Include

```json
{
  "type": "message-type",
  "task_id": "GH-XX"
}
```

### For Task-Related Messages

```json
{
  "type": "task",
  "task_id": "GH-42",
  "message": "Human-readable content",
  "report_back": true
}
```

### Structure Rules

1. **Always include `type` field** - Determines message handling
2. **Always include `task_id`** for task-related messages
3. **Use arrays for lists** - `completion_criteria`, `issues`, etc.
4. **Include `report_back: true`** when expecting response

---

## 4.8 Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `AIMAESTRO_API` | `http://localhost:23000` | API base URL |
| `AIMAESTRO_AGENT` | Auto-detected | Agent identifier override |

### Setting Environment Variables

```bash
# In your session or .bashrc
export AIMAESTRO_API="http://localhost:23000"

# For remote AI Maestro server
export AIMAESTRO_API="http://maestro.internal:23000"
```

---

## Related Sections

- [Part 1: API and Schema](messaging-protocol-part1-api-schema.md) - Full message schema
- [Part 7: Troubleshooting](messaging-protocol-part7-troubleshooting.md) - Detailed problem solutions
