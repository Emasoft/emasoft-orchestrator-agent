---
procedure: support-skill
workflow-instruction: support
---

# Operation: Set Labels on Task Completion

## When to Use

Use this operation when an agent completes their assigned work and the task is done.

## Prerequisites

- Issue is in `status:in-progress` with `assign:<agent>` label
- Agent has completed the work
- Work has been verified/reviewed
- GitHub CLI (`gh`) authenticated

## Procedure

### Step 1: Verify Task Completion

Before marking complete, confirm:

```bash
# Check current labels
gh issue view <ISSUE_NUM> --json labels --jq '.labels[].name'

# Should have:
# - status:in-progress
# - assign:<agent-id>
```

Completion criteria:
- All acceptance criteria met
- Tests passing
- Code reviewed (if required)
- Documentation updated (if required)

### Step 2: Determine Completion Path

| Scenario | Action |
|----------|--------|
| Work complete, no PR | Go to Step 3 |
| Work complete, PR open | Add `review:*` label first |
| Work complete, PR merged | Go to Step 3 |
| Work incomplete, reassigning | Use op-lifecycle-assignment-labels |

### Step 3: Handle PR Review Status (if applicable)

```bash
# PR submitted, needs review
gh issue edit <ISSUE_NUM> --add-label "review:requested"

# PR approved
gh issue edit <ISSUE_NUM> \
  --remove-label "review:requested" \
  --add-label "review:approved"

# PR merged - continue to completion
```

### Step 4: Apply Completion Labels

```bash
# Remove assignment and update status
gh issue edit <ISSUE_NUM> \
  --remove-label "assign:<agent-id>,status:in-progress,review:approved" \
  --add-label "status:done"
```

### Step 5: Close Issue (if policy allows)

```bash
# Close with completion comment
gh issue close <ISSUE_NUM> --comment "Task completed by <agent-id>. All acceptance criteria verified."

# Or leave open if requires additional verification
gh issue comment <ISSUE_NUM> --body "**Task Completed**
- Agent: <agent-id>
- Completion time: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- Status: done (issue remains open for final verification)"
```

### Step 6: Notify Orchestrator

```bash
# Send completion notification
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "Task Complete: Issue #<ISSUE_NUM>",
    "priority": "normal",
    "content": {
      "type": "task_complete",
      "message": "Issue #<ISSUE_NUM> completed by <agent-id>"
    }
  }'
```

## Output

| Field | Type | Description |
|-------|------|-------------|
| Assignment Removed | Boolean | `assign:*` label removed |
| Status Change | String | `status:in-progress` -> `status:done` |
| Issue State | String | Open or Closed |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No assignment label | Already removed or never set | Just update status |
| Multiple status labels | Previous error | Remove all, add `status:done` |
| PR not merged | Review incomplete | Keep `status:in-progress`, add `review:*` |

## Examples

### Example 1: Simple Completion

```bash
# Task done, no PR involved
gh issue edit 42 \
  --remove-label "assign:implementer-1,status:in-progress" \
  --add-label "status:done"

gh issue close 42 --comment "Completed by implementer-1"
```

### Example 2: Completion After PR Merge

```bash
# PR was merged, now complete the issue
gh issue edit 42 \
  --remove-label "assign:implementer-1,status:in-progress,review:approved" \
  --add-label "status:done"

gh issue close 42 --comment "PR #99 merged. Task completed."
```

### Example 3: Partial Completion with Handoff

```bash
# Agent completed part, handing off
gh issue edit 42 \
  --remove-label "assign:implementer-1"

gh issue comment 42 --body "**Partial Completion Handoff**
- Completed: API endpoints implemented
- Remaining: Unit tests needed
- Handing off to new assignee"

# Then assign to new agent
gh issue edit 42 --add-label "assign:implementer-2"
```

### Example 4: Completion with Blockers Found

```bash
# Work reveals blocking issue
gh issue edit 42 \
  --remove-label "assign:implementer-1,status:in-progress" \
  --add-label "status:blocked"

gh issue comment 42 --body "**Blocked**
- Completed: Initial implementation
- Blocker: Requires API update (see issue #45)
- Will resume after #45 resolved"
```

## Checklist

- [ ] Verify all acceptance criteria met
- [ ] Verify tests passing
- [ ] Verify code reviewed (if required)
- [ ] Handle PR review labels if applicable
- [ ] Remove `assign:<agent>` label
- [ ] Remove `status:in-progress`
- [ ] Add `status:done`
- [ ] Add completion comment
- [ ] Close issue (if policy allows)
- [ ] Notify orchestrator
- [ ] Update orchestrator state file
