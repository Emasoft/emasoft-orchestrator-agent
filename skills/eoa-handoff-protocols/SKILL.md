---
name: eoa-handoff-protocols
description: "Use when accessing shared reference documents used across multiple Orchestrator Agent skills. Trigger with shared resource lookups."
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Anthropic
  version: 1.0.0
context: fork
agent: eoa-main
---

# Shared References

## Overview

This skill provides shared reference documents that are used across multiple EOA (Emasoft Orchestrator Agent) skills.

## Prerequisites

None required. This is a reference-only skill.

## Instructions

1. Identify which shared reference document is needed based on the current task
2. Access the appropriate reference document from the links below
3. Follow the protocols and patterns described in the reference document

## Output

| Output Type | Description |
|-------------|-------------|
| Reference Access | Successfully accessed shared reference document |
| Protocol Application | Applied protocol from shared reference |

## Reference Documents

### Handoff Protocols ([references/handoff-protocols.md](references/handoff-protocols.md))

Standard protocols for handing off work between agents:

- When you need to transfer context between agents → Handoff Format
- If you need to document session state → Session State Schema
- When coordinating multi-agent workflows → Coordination Patterns

---

## Checklist

Copy this checklist and track your progress:

- [ ] Identified which shared reference document is needed
- [ ] Accessed the appropriate reference document
- [ ] Reviewed the protocols or patterns in the reference
- [ ] Applied the reference content to current task

---

## Examples

### Example 1: Using Handoff Protocol

```markdown
## Session Handoff

### Context
- Task: Implement auth-core module
- Progress: 60% complete
- Current state: JWT validation implemented

### Pending Items
- [ ] Session token support
- [ ] Token refresh logic

### Blockers
None

### Files Modified
- src/auth/jwt.py
- tests/auth/test_jwt.py
```

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| Missing reference file | Check skill installation, re-download if needed |
| Outdated protocol | Check for skill updates |

---

## Resources

- [handoff-protocols.md](references/handoff-protocols.md) - Agent handoff standards
