---
name: eoa-checklist-compiler
description: "Use when compiling verification checklists from requirements including module completion, quality gates, and test coverage checklists."
license: Apache-2.0
metadata:
  author: Anthropic
  version: 1.0.0
context: fork
---

# Checklist Compiler Skill

## Overview

Comprehensive patterns and templates for compiling verification checklists from requirements and specifications.

## Prerequisites

- Access to requirements documentation (USER_REQUIREMENTS.md or similar)
- Understanding of module acceptance criteria
- Familiarity with quality gate concepts

---

## Instructions

Use this skill when:
- Compiling verification checklists from requirements
- Creating quality gate checklists
- Designing module completion checklists
- Building test coverage checklists
- Structuring review checklists
- Understanding checklist compilation workflow

---

## Contents

### Reference Documents

1. **[checklist-types-reference.md](references/checklist-types-reference.md)**
   - 1.1 Module Completion Checklists
   - 1.2 Quality Gate Checklists
   - 1.3 Review Checklists
   - 1.4 Test Coverage Checklists
   - 1.5 Release Readiness Checklists
   - 1.6 Task Assignment Checklists

2. **[checklist-templates.md](references/checklist-templates.md)**
   - 2.1 Standard Checklist Template
   - 2.2 Priority-Annotated Checklist Template
   - 2.3 Dependency-Ordered Checklist Template
   - 2.4 Test Coverage Checklist Template

3. **[checklist-compilation-workflow.md](references/checklist-compilation-workflow.md)**
   - 3.1 Phase 1: Requirements Gathering
   - 3.2 Phase 2: Checklist Structuring
   - 3.3 Phase 3: Format and Document
   - 3.4 Phase 4: Quality Assurance
   - 3.5 Step-by-Step Procedure (10 steps with verification)

4. **[checklist-best-practices.md](references/checklist-best-practices.md)**
   - 4.1 Checklist Design Principles
   - 4.2 Common Pitfalls to Avoid
   - 4.3 Checklist Maintenance and Versioning

5. **[checklist-examples.md](references/checklist-examples.md)**
   - 5.1 Complete Example: SVG Parser Quality Gate Checklist
   - 5.2 Compilation Process Walkthrough
   - 5.3 Orchestrator Interaction Example

---

## Quick Reference

### Checklist Types

| Type | Purpose | Key Elements |
|------|---------|--------------|
| Module Completion | Verify module ready for integration | Implementation, docs, tests, types |
| Quality Gate | Verify standards before progression | Metrics, coverage, linting, security |
| Review | Conduct thorough code reviews | Structure, naming, resources, tests |
| Test Coverage | Ensure comprehensive test coverage | Unit, integration, edge cases |
| Release Readiness | Verify release ready for deployment | Features, docs, versioning, rollback |
| Task Assignment | Verify task properly defined | Objectives, criteria, constraints |

### Compilation Workflow Summary

```
Requirements → Extract Points → Structure → Define Criteria → Format → QA → Write → Report
```

### RULE 14 Compliance

Every checklist MUST include:
```markdown
## Requirement Compliance (RULE 14)
- [ ] USER_REQUIREMENTS.md exists and is current
- [ ] All user requirements addressed
- [ ] No technology substitutions without approval
- [ ] No scope reductions without approval
```

---

## Examples

### Example 1: Module Completion Checklist

```markdown
## Module: auth-core Completion Checklist

### Implementation
- [ ] All acceptance criteria implemented
- [ ] No TODO comments remaining
- [ ] Error handling complete

### Testing
- [ ] Unit tests pass (80%+ coverage)
- [ ] Integration tests pass
- [ ] Edge cases covered

### Documentation
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Changelog entry added
```

### Example 2: Quality Gate Checklist

```markdown
## Quality Gate: Pre-Merge

- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] No linting errors
- [ ] Type checks pass
- [ ] Security scan clean
- [ ] 4 verification loops completed
```

---

## Error Handling

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing requirements | USER_REQUIREMENTS.md not created | Create requirements file first |
| Incomplete checklist | Acceptance criteria unclear | Request clarification from user |
| Checklist too large | Requirements too broad | Break into smaller modules |

---

## Resources

- [checklist-types-reference.md](references/checklist-types-reference.md) - All checklist types
- [checklist-templates.md](references/checklist-templates.md) - Standard templates
- [checklist-compilation-workflow.md](references/checklist-compilation-workflow.md) - Step-by-step workflow
- [checklist-best-practices.md](references/checklist-best-practices.md) - Design principles
- [checklist-examples.md](references/checklist-examples.md) - Complete examples
