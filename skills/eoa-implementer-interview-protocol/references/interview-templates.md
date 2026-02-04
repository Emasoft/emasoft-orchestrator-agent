# Interview Templates

## Pre-Task Interview Questions

The Orchestrator MUST ask these questions:

```markdown
## Pre-Task Interview: {TASK_ID}

Please confirm your understanding:

1. **Task Summary**: In your own words, what does this task require?

2. **Acceptance Criteria**: What must be true for this task to be complete?

3. **Concerns**: Do you have any concerns about:
   - The requirements (unclear, conflicting, infeasible)?
   - The design (incompatible with existing code)?
   - Your capability (missing tools, skills, access)?
   - Dependencies (blocked by other tasks)?

4. **Approach**: Briefly describe how you plan to implement this.

5. **Blockers**: Is anything preventing you from starting immediately?

Reply with your answers. Do NOT start implementation until I confirm PROCEED.
```

## Post-Task Interview Questions

When implementer reports `[DONE]`:

```markdown
## Post-Task Interview: {TASK_ID}

Before PR creation, please confirm:

1. **Requirements Checklist**: For each requirement, confirm implementation:
   - [ ] REQ-001: {description} - Implemented? Where?
   - [ ] REQ-002: {description} - Implemented? Where?
   - [ ] (list all requirements)

2. **Testing Evidence**:
   - What tests did you write?
   - Do all tests pass? (provide test output)
   - Are there edge cases not covered?

3. **Code Quality**:
   - Did you run linting/formatting?
   - Any technical debt introduced?
   - Any TODO items left?

4. **Documentation**:
   - Did you update relevant docs?
   - Are code comments adequate?

5. **Self-Review**:
   - Did you review your own changes?
   - Any concerns about the implementation?

Reply with evidence for each item.
```

## Evaluating Pre-Task Responses

| Response | Action |
|----------|--------|
| Clear understanding, no concerns | Send PROCEED |
| Minor clarification needed | Clarify and send PROCEED |
| Design concerns | Escalate to Architect (EAA) |
| Requirement concerns (mutable) | Discuss with Architect |
| Requirement concerns (immutable) | Escalate to Manager (EAMA) → User |
| Capability issues | Consider reassignment or skill provision |
| Blockers identified | Resolve blockers first |

## Evaluating Post-Task Responses

| Response | Action |
|----------|--------|
| All requirements met, tests pass | Send APPROVED |
| Minor issues identified | Request fixes, re-interview |
| Missing requirements | REVISE - specify what's missing |
| Tests failing | REVISE - fix tests first |
| Quality concerns | REVISE - address concerns |
| Requirement deviation | Escalate (see escalation-procedures.md) |
