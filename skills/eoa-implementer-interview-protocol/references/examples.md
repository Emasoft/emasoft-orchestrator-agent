# Interview Protocol Examples

## Table of Contents

- [Example 1: Send Pre-Task Interview Questions](#example-1-send-pre-task-interview-questions)
- [Example 2: Escalate Design Concern to Architect](#example-2-escalate-design-concern-to-architect)
- [Example 3: Send PROCEED After Satisfactory Interview](#example-3-send-proceed-after-satisfactory-interview)
- [Example 4: Send Post-Task Verification Questions](#example-4-send-post-task-verification-questions)
- [Example 5: Send APPROVED and Handoff to Integrator](#example-5-send-approved-and-handoff-to-integrator)

## Example 1: Send Pre-Task Interview Questions

```bash
# Via AI Maestro
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "implementer-1",
    "subject": "Pre-Task Interview: #42",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "## Pre-Task Interview: #42\n\n1. **Task Summary**: In your own words, what does this task require?\n\n2. **Acceptance Criteria**: What must be true for this task to be complete?\n\n3. **Concerns**: Any concerns about requirements, design, capability, or dependencies?\n\n4. **Approach**: Briefly describe how you plan to implement this.\n\n5. **Blockers**: Is anything preventing you from starting immediately?\n\nReply with answers. Do NOT start until I confirm PROCEED.",
      "data": {
        "issue_number": 42
      }
    }
  }'
```

## Example 2: Escalate Design Concern to Architect

```bash
# Implementer reports: "API design uses synchronous calls, but requirement needs real-time updates"
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "architect",
    "subject": "Design Review Required: #42",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Implementer identified design issue for task #42. Issue: API design uses synchronous calls, but requirement needs real-time updates. Please review and advise on design modification.",
      "data": {
        "task_id": "42",
        "implementer": "implementer-1",
        "concern": "Synchronous API incompatible with real-time requirement",
        "design_doc": "docs/design/api-v2-design.md"
      }
    }
  }'
```

## Example 3: Send PROCEED After Satisfactory Interview

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "implementer-1",
    "subject": "PROCEED: #42",
    "priority": "normal",
    "content": {
      "type": "approval",
      "message": "## PROCEED: #42\n\nYour understanding is confirmed. You may begin implementation.\n\n**Reminders**:\n- Follow the design document\n- Respect immutable requirements (see FORBIDDEN section)\n- Report blockers immediately\n- Report completion when done (do NOT create PR yet)\n\nGood luck!"
    }
  }'
```

## Example 4: Send Post-Task Verification Questions

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "implementer-1",
    "subject": "Post-Task Interview: #42",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "## Post-Task Interview: #42\n\n1. **Requirements Checklist**: For each requirement, confirm:\n   - [ ] REQ-001: Real-time updates - Implemented? Where?\n   - [ ] REQ-002: Authentication - Implemented? Where?\n\n2. **Testing Evidence**: What tests did you write? Do all pass?\n\n3. **Code Quality**: Did you run linting? Any TODOs left?\n\n4. **Documentation**: Did you update relevant docs?\n\n5. **Self-Review**: Any concerns about the implementation?\n\nReply with evidence."
    }
  }'
```

## Example 5: Send APPROVED and Handoff to Integrator

```bash
# Send APPROVED to implementer
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "implementer-1",
    "subject": "APPROVED: #42",
    "priority": "normal",
    "content": {
      "type": "approval",
      "message": "## APPROVED: #42\n\nVerification complete. Create PR now.\n\n**PR Requirements**:\n- Title: [Feature] Real-time API updates (#42)\n- Link: Closes #42\n- Include test evidence\n\nReport PR number when created."
    }
  }'

# After implementer reports PR #123 created:
# Update issue status
gh issue edit 42 --remove-label "status:in-progress" --add-label "status:needs-review"

# Notify Integrator
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "orchestrator",
    "to": "integrator",
    "subject": "PR Ready for Review: #123",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "PR #123 is ready for review. Task: #42. Pre-verified by orchestrator.",
      "data": {
        "pr_number": 123,
        "issue_number": 42,
        "implementer": "implementer-1",
        "verification_status": "pre-verified"
      }
    }
  }'
```
