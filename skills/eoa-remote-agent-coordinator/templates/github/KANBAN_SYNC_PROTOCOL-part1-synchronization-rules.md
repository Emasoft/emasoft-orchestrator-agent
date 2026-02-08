# Kanban Synchronization Protocol - Part 1: Synchronization Rules

This document contains the agent synchronization rules for updating GitHub issue status and kanban board positions.

**Parent document:** [KANBAN_SYNC_PROTOCOL.md](./KANBAN_SYNC_PROTOCOL.md)

---

## Agent Synchronization Rules

### Rule 1: Update Status When Starting Work

**When:** Agent begins working on an assigned task

**Actions:**
```bash
# 1. Update issue label
gh issue edit {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --remove-label "status:backlog" \
  --add-label "status:in-progress"

# 2. Move card on kanban
gh project item-edit \
  --project-id {{PROJECT_ID}} \
  --id {{ITEM_ID}} \
  --field-id {{STATUS_FIELD_ID}} \
  --value "In Progress"

# 3. Add comment to issue
gh issue comment {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --body "🤖 Agent **{{AGENT_NAME}}** started working on this task.

**Session:** {{SESSION_ID}}
**Platform:** {{PLATFORM}}
**Started:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
```

**Required Fields:**
- Issue must be assigned to agent
- Toolchain template must be specified
- All required tools must be verified available

### Rule 2: Update Status When Blocked

**When:** Agent encounters blocking issue (missing dependency, external service down, unclear requirements)

**Actions:**
```bash
# 1. Update issue labels
gh issue edit {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --remove-label "status:in-progress" \
  --add-label "status:blocked"

# 2. Keep in "In Progress" column but add blocked indicator
gh issue comment {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --body "⚠️ Agent **{{AGENT_NAME}}** is blocked.

**Blocker:** {{BLOCKER_DESCRIPTION}}
**Impact:** {{IMPACT_DESCRIPTION}}
**Needs:** {{REQUIRED_ACTION}}

cc @{{ORCHESTRATOR_OWNER}}"

# 3. Notify orchestrator
# Note: Use the `agent-messaging` skill to send messages instead of direct curl commands.
# If the skill is unavailable in the remote agent's environment, the curl format below can be used as fallback.
curl -X POST "{{AIMAESTRO_API}}/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "{{ORCHESTRATOR_AGENT}}",
    "subject": "Agent blocked: {{TASK_ID}}",
    "priority": "high",
    "content": {
      "type": "alert",
      "message": "Agent {{AGENT_NAME}} blocked on task {{TASK_ID}}: {{BLOCKER_DESCRIPTION}}"
    }
  }'
```

**Required Fields:**
- Clear description of blocker
- What is needed to unblock
- Estimated impact on timeline

### Rule 3: Update Status When Unblocked

**When:** Blocker is resolved and agent can resume work

**Actions:**
```bash
# 1. Update issue labels
gh issue edit {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --remove-label "status:blocked" \
  --add-label "status:in-progress"

# 2. Add comment
gh issue comment {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --body "✅ Agent **{{AGENT_NAME}}** unblocked and resuming work.

**Resolved:** {{RESOLUTION_DESCRIPTION}}
**Resumed:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
```

### Rule 4: Update Status When Creating PR

**When:** Agent creates pull request for review

**Actions:**
```bash
# 1. Update issue label
gh issue edit {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --remove-label "status:in-progress" \
  --add-label "status:in-review"

# 2. Move card on kanban
gh project item-edit \
  --project-id {{PROJECT_ID}} \
  --id {{ITEM_ID}} \
  --field-id {{STATUS_FIELD_ID}} \
  --value "In Review"

# 3. Link PR to issue (automatic if PR body contains "Closes #{{ISSUE_NUMBER}}")

# 4. Add comment with PR link
gh issue comment {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --body "🔍 Agent **{{AGENT_NAME}}** completed implementation and opened PR for review.

**Pull Request:** #{{PR_NUMBER}}
**Test Results:** {{TEST_SUMMARY}}
**Coverage:** {{COVERAGE}}%

Ready for review!"
```

**Required Fields Before Transition:**
- [ ] All acceptance criteria met
- [ ] All tests passing locally
- [ ] Code formatted and linted
- [ ] Documentation updated
- [ ] Toolchain verified
- [ ] PR created with proper template

### Rule 5: Update Status When Tests Fail

**When:** Tests fail during implementation or CI

**Actions:**
```bash
# 1. Keep status:in-progress label

# 2. Add comment with failure details
gh issue comment {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --body "❌ Tests failed for task {{TASK_ID}}.

**Failed Tests:** {{FAILED_COUNT}}/{{TOTAL_COUNT}}
**Agent:** {{AGENT_NAME}}
**Log:** [View Log]({{LOG_URL}})

Agent is investigating and fixing failures."

# 3. Do NOT move to "In Review"
# 4. Fix issues and re-run tests
# 5. When fixed, proceed with Rule 4
```

### Rule 6: Update Status When PR Merged

**When:** Pull request is merged (usually by orchestrator or human reviewer)

**Actions:**
```bash
# 1. Update issue label
gh issue edit {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --remove-label "status:in-review" \
  --add-label "status:done"

# 2. Move card on kanban
gh project item-edit \
  --project-id {{PROJECT_ID}} \
  --id {{ITEM_ID}} \
  --field-id {{STATUS_FIELD_ID}} \
  --value "Done"

# 3. Close issue
gh issue close {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --comment "✅ Completed and merged in PR #{{PR_NUMBER}}.

**Merged:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Duration:** {{ACTUAL_DURATION}}
**Agent:** {{AGENT_NAME}}"
```

**Required Fields Before Transition:**
- [ ] PR approved by reviewer
- [ ] All CI checks passing
- [ ] No merge conflicts
- [ ] Branch up to date with base

### Rule 7: Handle PR Changes Requested

**When:** Reviewer requests changes on PR

**Actions:**
```bash
# 1. Update labels
gh issue edit {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --remove-label "status:in-review" \
  --add-label "status:in-progress"

# 2. Move back to "In Progress"
gh project item-edit \
  --project-id {{PROJECT_ID}} \
  --id {{ITEM_ID}} \
  --field-id {{STATUS_FIELD_ID}} \
  --value "In Progress"

# 3. Add comment
gh issue comment {{ISSUE_NUMBER}} \
  --repo {{GITHUB_OWNER}}/{{REPO_NAME}} \
  --body "🔄 Changes requested on PR #{{PR_NUMBER}}.

Agent **{{AGENT_NAME}}** is addressing reviewer feedback.

**Requested Changes:**
{{REVIEWER_FEEDBACK}}"

# 4. Address feedback
# 5. When ready, return to Rule 4
```
