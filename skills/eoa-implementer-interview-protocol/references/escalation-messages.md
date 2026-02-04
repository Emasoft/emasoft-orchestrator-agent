# Escalation Message Templates

## Table of Contents

- [Design Issues → Architect](#design-issues--architect)
- [Immutable Requirement Issues → Manager → User](#immutable-requirement-issues--manager--user)
- [PROCEED Message](#proceed-message)
- [APPROVED Message](#approved-message)
- [REVISE Message](#revise-message)

## Design Issues → Architect

If implementer identifies design incompatibilities:

```json
{
  "from": "orchestrator",
  "to": "architect",
  "subject": "Design Review Required: {TASK_ID}",
  "priority": "high",
  "content": {
    "type": "request",
    "message": "Implementer identified design issue. Task: {TASK_ID}. Issue: {DESCRIPTION}. Please review and advise.",
    "data": {
      "task_id": "{TASK_ID}",
      "implementer": "{AGENT_NAME}",
      "concern": "{IMPLEMENTER_CONCERN}",
      "design_doc": "{DESIGN_DOC_PATH}"
    }
  }
}
```

## Immutable Requirement Issues → Manager → User

If implementer identifies issues with USER requirements:

```json
{
  "from": "orchestrator",
  "to": "assistant-manager",
  "subject": "User Decision Required: Requirement Issue",
  "priority": "urgent",
  "content": {
    "type": "approval_request",
    "message": "Implementer identified issue with immutable requirement. User decision required.",
    "data": {
      "task_id": "{TASK_ID}",
      "requirement_id": "REQ-XXX",
      "requirement_text": "{EXACT_USER_QUOTE}",
      "issue": "{IMPLEMENTER_CONCERN}",
      "options": [
        "A. Proceed as specified (accept risk)",
        "B. Modify requirement",
        "C. Cancel task"
      ]
    }
  }
}
```

**CRITICAL**: NEVER modify an immutable user requirement without explicit user approval obtained through the Manager.

## PROCEED Message

Only after satisfactory interview:

```markdown
## PROCEED: {TASK_ID}

Your understanding is confirmed. You may begin implementation.

**Reminders**:
- Follow the design document
- Respect immutable requirements (see FORBIDDEN section)
- Report blockers immediately
- Report completion when done (do NOT create PR yet)

Good luck!
```

## APPROVED Message

Only when ALL verification passes:

```markdown
## APPROVED: {TASK_ID}

Verification complete. You may now create the Pull Request.

**PR Requirements**:
- Title: [Type] {Brief description} (#{ISSUE_NUMBER})
- Link to issue: "Closes #{ISSUE_NUMBER}"
- Include test evidence in description
- Request review from appropriate reviewers

After PR creation, report the PR number to me.
Your responsibility ends when the PR is created.
The Integrator (EIA) will handle review and merge.
```

## REVISE Message

When issues found:

```markdown
## REVISE: {TASK_ID}

Verification found issues that must be addressed:

**Issues**:
1. {ISSUE_1}
2. {ISSUE_2}

**Required Actions**:
- {ACTION_1}
- {ACTION_2}

Do NOT create a PR until these are resolved.
Report `[DONE]` again when ready for re-verification.
```
