---
procedure: support-skill
workflow-instruction: support
---

# Operation: Set Labels During Triage

## When to Use

Use this operation when triaging an issue that has `status:needs-triage` label.

## Prerequisites

- Issue exists with `status:needs-triage`
- Issue has been analyzed for priority, effort, and scope
- GitHub CLI (`gh`) authenticated

## Procedure

### Step 1: Assess Priority

Determine urgency based on impact and scope:

| Priority Label | Criteria |
|----------------|----------|
| `priority:critical` | System down, data loss, security breach - immediate |
| `priority:high` | Major feature broken, blocking release - 1-2 days |
| `priority:normal` | Standard work, non-blocking - 1 week |
| `priority:low` | Nice-to-have, minor improvements - 2+ weeks |

### Step 2: Estimate Effort

Assess work complexity and duration:

| Effort Label | Size |
|--------------|------|
| `effort:xs` | < 1 hour |
| `effort:s` | 1-4 hours |
| `effort:m` | 4-8 hours (1 day) |
| `effort:l` | 1-2 days |
| `effort:xl` | > 2 days |

### Step 3: Identify Platform/Toolchain (if applicable)

```bash
# Platform-specific
platform:linux
platform:macos
platform:windows

# Toolchain-specific
toolchain:python
toolchain:typescript
toolchain:rust
```

### Step 4: Determine Next Status

| Condition | Status |
|-----------|--------|
| Ready for immediate work | `status:ready` |
| Needs more info | `status:needs-info` |
| Blocked by other work | `status:blocked` |
| Deferred to later | `status:backlog` |

### Step 5: Apply Triage Labels

```bash
# Full triage - move to ready
gh issue edit <ISSUE_NUM> \
  --remove-label "status:needs-triage" \
  --add-label "priority:<priority>,effort:<effort>,status:ready"

# With platform/toolchain
gh issue edit <ISSUE_NUM> \
  --remove-label "status:needs-triage" \
  --add-label "priority:<priority>,effort:<effort>,status:ready,platform:<platform>,toolchain:<toolchain>"

# Move to backlog
gh issue edit <ISSUE_NUM> \
  --remove-label "status:needs-triage" \
  --add-label "priority:<priority>,effort:<effort>,status:backlog"
```

### Step 6: Add Component if Not Set

```bash
# If component was not set during creation
gh issue edit <ISSUE_NUM> --add-label "component:<component>"
```

### Step 7: Add Triage Comment

```bash
gh issue comment <ISSUE_NUM> --body "**Triage Complete**
- Priority: <priority>
- Effort: <effort>
- Status: Ready for implementation
- Notes: <any additional context>"
```

## Output

| Field | Type | Description |
|-------|------|-------------|
| Labels Applied | Array | Priority, effort, new status labels |
| Triage State | String | Issue now has complete metadata for assignment |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Cannot estimate effort | Unclear scope | Request clarification, set `status:needs-info` |
| Priority unclear | No business context | Default to `priority:normal`, escalate if needed |
| Missing component | Still unknown | Add comment requesting component identification |

## Examples

### Example 1: Standard Bug Triage

```bash
# Bug ready for immediate work
gh issue edit 123 \
  --remove-label "status:needs-triage" \
  --add-label "priority:high,effort:m,status:ready,component:api"
```

### Example 2: Feature to Backlog

```bash
# Feature deferred to backlog
gh issue edit 124 \
  --remove-label "status:needs-triage" \
  --add-label "priority:low,effort:xl,status:backlog"
```

### Example 3: Needs More Information

```bash
# Cannot triage without more info
gh issue edit 125 \
  --remove-label "status:needs-triage" \
  --add-label "status:needs-info"
gh issue comment 125 --body "Cannot triage: Please provide steps to reproduce the issue."
```

## Checklist

- [ ] Review issue content thoroughly
- [ ] Assess priority (critical/high/normal/low)
- [ ] Estimate effort (xs/s/m/l/xl)
- [ ] Verify component is set
- [ ] Determine appropriate next status
- [ ] Remove `status:needs-triage`
- [ ] Add priority, effort, and new status labels
- [ ] Add platform/toolchain if relevant
- [ ] Add triage comment with summary
