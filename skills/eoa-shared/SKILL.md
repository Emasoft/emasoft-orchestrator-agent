---
name: eoa-shared
description: "Use when accessing shared reference documents used across multiple Orchestrator Agent skills."
license: Apache-2.0
metadata:
  author: Anthropic
  version: 1.0.0
context: fork
---

# Shared References

## Overview

This skill provides shared reference documents that are used across multiple Atlas Orchestrator skills.

## Prerequisites

None required. This is a reference-only skill.

## Instructions

Access these shared documents when other skills reference them or when you need common protocols.

## Reference Documents

### Handoff Protocols ([references/handoff-protocols.md](references/handoff-protocols.md))

Standard protocols for handing off work between agents:

- When you need to transfer context between agents → Handoff Format
- If you need to document session state → Session State Schema
- When coordinating multi-agent workflows → Coordination Patterns

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
