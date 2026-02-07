---
procedure: support-skill
workflow-instruction: support
---

# Operation: Compile Task Context

## When to Use

Use this operation after receiving an ECOS notification to gather all context about the failed agent's work.

## Prerequisites

- ECOS notification acknowledged
- Failed agent's ID known
- Access to orchestrator state files
- Access to GitHub repository

## Procedure

### Step 1: Read Orchestrator State

```bash
# Load current state
STATE_FILE="design/state/exec-phase.md"
cat "$STATE_FILE"

# Extract failed agent's assignments
grep -A 20 "agent: $FAILED_AGENT" "$STATE_FILE"
```

### Step 2: Collect Task Assignments

Gather from state file:
- Currently assigned modules
- Module completion percentage
- Active GitHub issues
- Pending deliverables

```python
# Using the helper script
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eoa_compile_replacement_context.py" \
  --failed-agent "implementer-1" \
  --state-file "design/state/exec-phase.md" \
  --output "replacement-context.md"
```

### Step 3: Collect GitHub Issue Status

```bash
# Find all issues assigned to failed agent
gh issue list --label "assign:$FAILED_AGENT" --json number,title,state,body,labels

# Get detailed issue content
for issue_num in $(gh issue list --label "assign:$FAILED_AGENT" --json number --jq '.[].number'); do
  echo "=== Issue #$issue_num ===" >> context.md
  gh issue view "$issue_num" >> context.md
  echo "" >> context.md
done
```

### Step 4: Collect Git Branch Progress

```bash
# Find agent's working branches
git branch -a | grep "$FAILED_AGENT"

# Get recent commits from agent
git log --oneline --author="$FAILED_AGENT" -20

# Get uncommitted changes on agent's branches
for branch in $(git branch -a | grep "$FAILED_AGENT"); do
  echo "=== Branch: $branch ===" >> context.md
  git log main..$branch --oneline >> context.md
  echo "" >> context.md
done
```

### Step 5: Collect Communication History

```bash
# Get AI Maestro message history with failed agent
curl -s "http://localhost:23000/api/messages?agent=$FAILED_AGENT&action=history" \
  | jq '.messages | sort_by(.timestamp) | .[-20:]' > comms-history.json
```

### Step 6: Identify Blockers and Dependencies

From collected context, document:
- Blocking issues (issues blocking agent's work)
- Dependent issues (issues depending on agent's work)
- External dependencies (APIs, services)
- Pending reviews

### Step 7: Create Progress Summary

```markdown
# Context Compilation: <failed_agent>

## Task Assignments
- Module A: 70% complete
- Issue #42: In progress (implementation done, tests pending)
- Issue #45: Not started

## Current Progress
- Files modified: src/auth/login.py, src/auth/token.py
- Tests written: 8 of 12
- Documentation: 0%

## Blockers
- Issue #38 must be merged first
- Waiting for API spec clarification

## Communication Summary
- Last message received: 2024-01-15T14:30:00Z
- Last progress report: "Completed token generation, starting validation"

## Uncommitted Work
- Branch: feature/auth-42
- 3 commits ahead of main
- Changes in: src/auth/validation.py (partial implementation)
```

## Output

| Field | Type | Description |
|-------|------|-------------|
| Context Document | Markdown | Compiled context in `replacement-context.md` |
| Issue List | Array | GitHub issues assigned to failed agent |
| Branch List | Array | Git branches with agent's work |
| Progress Summary | Object | Completion status for each task |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| State file not found | Path incorrect or file deleted | Check state file location |
| No assigned issues | Agent had no work or labels wrong | Verify label scheme |
| Git history unavailable | Repo access issue | Check git credentials |
| AI Maestro history empty | Messages expired or purged | Note context gap |

## Example

```bash
# Complete context compilation example

FAILED_AGENT="implementer-1"
CONTEXT_FILE="replacement-context-$(date +%Y%m%d-%H%M%S).md"

# Header
cat > "$CONTEXT_FILE" <<EOF
# Replacement Context for $FAILED_AGENT
**Generated**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Reason**: Context loss recovery

EOF

# Task assignments from state
echo "## Task Assignments" >> "$CONTEXT_FILE"
grep -A 10 "assign:$FAILED_AGENT" design/state/exec-phase.md >> "$CONTEXT_FILE"

# GitHub issues
echo -e "\n## GitHub Issues" >> "$CONTEXT_FILE"
gh issue list --label "assign:$FAILED_AGENT" --json number,title,state >> "$CONTEXT_FILE"

# Git branches
echo -e "\n## Git Branches" >> "$CONTEXT_FILE"
git branch -a | grep "$FAILED_AGENT" >> "$CONTEXT_FILE"

# Recent communications
echo -e "\n## Recent Communications" >> "$CONTEXT_FILE"
curl -s "http://localhost:23000/api/messages?agent=$FAILED_AGENT&action=history" \
  | jq '.messages[-5:]' >> "$CONTEXT_FILE"

echo "Context compiled to: $CONTEXT_FILE"
```

## Checklist

- [ ] Read orchestrator state file
- [ ] Extract failed agent's task assignments
- [ ] Collect GitHub issues with `assign:*` label
- [ ] Get issue details and comments
- [ ] Find agent's git branches
- [ ] Get commit history
- [ ] Check for uncommitted changes
- [ ] Retrieve AI Maestro communication history
- [ ] Identify blockers and dependencies
- [ ] Create progress summary
- [ ] Write context to file
