---
name: eoa-orchestration-patterns
description: "Use when coordinating work among multiple developers using orchestration patterns. Covers multi-developer coordination, Claude Code native Tasks management, progress monitoring, and escalation procedures for blocked tasks. Includes task decomposition, assignment strategies, status tracking, and handling blocked tasks."
license: Apache-2.0
compatibility: Requires multiple developers or task agents, task tracking system (GitHub issues or similar), clear task definitions with success criteria, and communication channel for status updates.
metadata:
  author: Anthropic
  version: 2.4.0
context: fork
---

# Orchestration Patterns Skill

## Overview

This skill teaches you how to coordinate work among multiple developers using orchestration patterns. It covers multi-developer coordination, Claude Code native Tasks management, progress monitoring, and escalation procedures for blocked tasks.

## Core Concepts

Before reading further, you need to understand what orchestration means in this context:

**Orchestration** is the act of coordinating multiple concurrent tasks performed by different agents (developers, task workers, or automated processes) to achieve a common goal. An orchestrator is responsible for:
- Breaking down work into independent tasks
- Assigning tasks to the right workers
- Tracking progress
- Unblocking stuck work
- Managing communication and feedback

## Prerequisites

To use this skill effectively, ensure you have:
1. Multiple developers or task agents available for parallel work
2. A way to track task status (GitHub issues, task lists, or similar)
3. Clear task definitions with success criteria
4. A communication channel for status updates and escalations

## Instructions

### Procedure Overview

The orchestration workflow follows these main phases in order:

1. **Phase 1: Task Decomposition** - Break down the goal into independent, parallelizable tasks
2. **Phase 2: Task Assignment** - Assign tasks to developers with clear instructions
3. **Phase 3: Progress Monitoring** - Track task completion and identify blocks
4. **Phase 4: Escalation & Unblocking** - Handle blocked tasks and escalate when needed
5. **Phase 5: Integration & Verification** - Combine results and verify completion

---

## Reference Files

### Task Complexity Classifier ([references/task-complexity-classifier.md](references/task-complexity-classifier.md))

Evaluate task complexity to determine appropriate planning investment.

**Contents:**
- Classification Process - When deciding if a task needs planning
- Simple Task - If task involves single language with standard libs
- Medium Task - When task requires external packages and architecture
- Complex Task - If task spans multiple languages or platforms
- Practical Tips > When in Doubt - When uncertain between complexity levels
- Anti-Patterns > Over-Planning Simple Tasks - If you're over-planning a simple task
- Practical Tips > De-escalation Signals - When task becomes simpler during planning

**Read first** - Understanding task complexity guides all subsequent decisions.

---

### Agent Selection Guide ([references/agent-selection-guide.md](references/agent-selection-guide.md))

Select the right specialized agent for each task based on language, domain, and capabilities.

**Contents:**
- Selection Decision Tree - When you need to delegate a task
- Language-Specific Agents - If unsure which agent handles Python/JS/Go/Rust work
- Specialized Agents > Search and Analysis - When choosing between search agents
- Anti-Patterns > Parallel Git Operations - If multiple agents conflict on git
- Anti-Patterns > Missing Test Count Specification - When test-writer creates too many tests
- Anti-Patterns > Verbose Agent Output - If agent crashes orchestrator with verbose output
- Best Practices > Chain Agents - When you need to run tests without blocking
- Best Practices > Code Fixer Agent - If you need to fix code quality issues

**Read second** - Essential for effective task delegation and parallel execution.

**Prerequisite:** Task Complexity Classifier

---

### Project Setup Menu ([references/project-setup-menu.md](references/project-setup-menu.md))

Conduct interactive setup to establish project parameters, team configuration, and quality standards.

**Contents:**
- Menu Implementation - When starting a new project
- Troubleshooting > Missing Configuration File - If configuration file is missing/corrupted
- Team Configuration - When you need to understand team structure
- Team Configuration > Question 2 - If you need to set up AI Maestro remote agents
- Repository Configuration > Question 4 - When configuring branch protection rules
- Release Strategy > Question 7 - If deciding on alpha-only development strategy
- Release Strategy > Question 8 - When setting up package publishing
- Troubleshooting > Changed Mind Mid-Project - If user changes mind mid-project
- Response Handling > Using Stored Configuration - When referencing stored configuration

**Read third** - Run before any project work begins to prevent assumptions.

**Prerequisite:** Agent Selection Guide

---

### Language Verification Checklists ([references/language-verification-checklists.md](references/language-verification-checklists.md))

Ensure code quality, build success, and release readiness with language-specific verification standards.

**Contents:**
- Python Verification Checklist - When verifying Python project quality
- Go Verification Checklist - If you need to validate Go builds
- JavaScript/TypeScript Verification Checklist - When checking JS/TS quality
- Rust Verification Checklist - If Rust project needs validation
- Usage in Orchestration > Delegating Tasks - When delegating with quality requirements
- Troubleshooting > Common Issues - If mypy errors or ESLint/Prettier conflict
- Automation Scripts - If you need automation scripts for verification

**Read last** - Apply these checklists when reviewing deliverables or before commits.

**Prerequisite:** Project Setup Menu

---

### Progress Monitoring ([references/progress-monitoring.md](references/progress-monitoring.md))

PROACTIVE monitoring of implementer agents to ensure progress and completion.

**Contents:**
- 1. Proactive Monitoring Principles
  - 1.1 Why Proactive Monitoring is Critical
  - 1.2 The Five Proactive Principles
- 2. PROACTIVE Status Request Protocol
  - 2.1 When to Send Status Requests
  - 2.2 Status Request Message Template
- 3. PROACTIVE Unblocking Protocol
  - 3.1 When an Agent Reports a Blocker
  - 3.2 Unblocking Response Template
- 4. PROACTIVE Task Completion Enforcement
  - 4.1 Before Allowing Agent to Stop
  - 4.2 Verification Requirements

**When to use:**
- When agent has been silent for 15+ minutes
- When agent reports a blocker
- When agent wants to stop before completion
- When verifying task completion evidence

---

### Verification Loops ([references/verification-loops.md](references/verification-loops.md))

MANDATORY 4-verification-loops before any Pull Request is approved.

**Contents:**
- 1. Overview
  - 1.1 Why 4 Verification Loops Are Required
  - 1.2 The Precise Flow Diagram
- 2. Step 1: At Task Assignment
  - 2.1 PR Notification Requirement Template
  - 2.2 Including in Every Delegation
- 3. Step 2: Full Verification Message
  - 3.1 When to Send This Message
  - 3.2 Verification Message Template (Send 4 Times)
  - 3.3 What the Agent Must Check
- 4. Step 3: Track PR Requests Per Task
  - 4.1 Tracking Table Format
  - 4.2 Sample Tracking Table
- 5. Step 4: On 5th Request - Final Decision
  - 5.1 Approval Conditions
  - 5.2 Summary Table
- 6. Enforcement Rules
  - 6.1 What is NEVER Allowed
  - 6.2 What is ALWAYS Required

**When to use:**
- When assigning any task (include PR notification requirement)
- When agent asks "Can I make a PR?"
- When tracking verification progress per agent
- When deciding whether to approve PR

---

### Orchestrator No Implementation Rule ([references/orchestrator-no-implementation.md](references/orchestrator-no-implementation.md))

RULE 15: The orchestrator NEVER writes production code.

**Contents:**
- 1. Core Principle
  - 1.1 What the Orchestrator Does
  - 1.2 Why This Rule Exists
- 2. Forbidden Actions for Orchestrators
  - 2.1 Actions That Violate RULE 15
  - 2.2 Correct Approach for Each Forbidden Action
- 3. Allowed Actions for Orchestrators
  - 3.1 Actions That Are Always Allowed
  - 3.2 When Each Action is Appropriate
- 4. Small Experiments (ALLOWED with Limits)
  - 4.1 What Qualifies as a Small Experiment
  - 4.2 Size Limits for Experiments
  - 4.3 Experiment Workflow
  - 4.4 Example Experiments
- 5. Self-Check Before ANY Action
  - 5.1 The Self-Check Procedure
  - 5.2 What to Do When Self-Check Fails
- 6. Exception: Emergency Research Commands
  - 6.1 Allowed Research Commands
  - 6.2 Forbidden Implementation Commands
- 7. Practical Examples
  - 7.1 WRONG Approach (Orchestrator Does Implementation)
  - 7.2 CORRECT Approach (Orchestrator Researches and Delegates)

**When to use:**
- Before taking any action (self-check)
- When tempted to write code directly
- When deciding between research and implementation
- When verifying small experiment size limits

---

### User Requirements Immutable Rule ([references/user-requirements-immutable.md](references/user-requirements-immutable.md))

RULE 14: User requirements cannot be changed without explicit user approval.

**Contents:**
- 1. Core Principle
  - 1.1 What Immutable Requirements Means
  - 1.2 Why This Rule Exists
- 2. Orchestration Requirement Enforcement
  - 2.1 At Project Start
  - 2.2 During Planning
  - 2.3 During Execution
  - 2.4 At Review
- 3. Orchestrator Forbidden Actions
  - 3.1 Actions That Violate RULE 14
  - 3.2 Consequences of Violations
- 4. Requirement Issue Workflow
  - 4.1 When to Use This Workflow
  - 4.2 The Workflow Diagram
  - 4.3 Step-by-Step Process
- 5. Requirement Immutability Enforcement Points
  - 5.1 By Phase
  - 5.2 Evidence Required at Each Phase

**When to use:**
- At project start (create USER_REQUIREMENTS.md)
- When requirement cannot be implemented as stated
- When requirements conflict
- When agent delivers something different than required

---

### Orchestrator-Exclusive Communications ([references/orchestrator-exclusive-communications.md](references/orchestrator-exclusive-communications.md))

RULE 16: Only the orchestrator can send/receive messages or commit changes.

**Contents:**
- 1. Core Principle
  - 1.1 What This Rule Means
  - 1.2 Why This Rule Exists
- 2. Orchestrator-Exclusive Actions
  - 2.1 Actions ONLY the Orchestrator Can Perform
  - 2.2 Why Each Action is Exclusive
- 3. Sub-Agent Restrictions
  - 3.1 What Sub-Agents CANNOT Do
  - 3.2 What Sub-Agents CAN Do
- 4. Communication Flow
  - 4.1 Correct Communication Pattern
  - 4.2 Forbidden Communication Pattern
- 5. Practical Examples
  - 5.1 WRONG Approach (Sub-Agent Sends Messages)
  - 5.2 CORRECT Approach (Sub-Agent Reports to Orchestrator)
- 6. Enforcement Mechanism
  - 6.1 What to Include in Sub-Agent Prompts
  - 6.2 What to Check Before Spawning Sub-Agents

**When to use:**
- Before spawning any sub-agent (include constraints in prompt)
- When sub-agent needs to communicate externally (split into prepare/send)
- When sub-agent completes work requiring notification
- When reviewing sub-agent prompts for rule compliance

---

### Non-Blocking Patterns ([references/non-blocking-patterns.md](references/non-blocking-patterns.md))

RULE 17: The orchestrator must ALWAYS remain responsive.

**Contents:**
- 1. RULE 17: Orchestrator Must Remain Responsive (IRON RULE)
  - 1.1 What the Orchestrator Must ALWAYS Be Available For
  - 1.2 What the Orchestrator Must NEVER Do
- 2. Async Task Delegation Patterns
  - 2.1 Background Bash Pattern
  - 2.2 Task Agent with Timeout
  - 2.3 Fire-and-Forget Pattern for Non-Critical Tasks
- 3. Polling Instead of Blocking
  - 3.1 Progress Polling Protocol
  - 3.2 Status Check Without Blocking
- 4. Automatic Escalation Triggers
  - 4.1 When Orchestrator Has Been Unresponsive
  - 4.2 Self-Check for Responsiveness
- 5. Parallel Agent Spawning
  - 5.1 Batch Spawning Pattern
  - 5.2 Maximum Concurrent Agents
- 6. Message Queue Processing
  - 6.1 AI Maestro Priority Queue
  - 6.2 Non-Blocking Message Check
- 7. Graceful Handoff Pattern
  - 7.1 Complete Handoff
  - 7.2 Instruction Document Template
- 8. Emergency Response Availability
  - 8.1 Always Available For
  - 8.2 Interrupt Protocol
- 9. Task Tracking for Async Operations
  - 9.1 Tracking Document Format
  - 9.2 Task Completion Verification

**When to use:**
- Before running any command that takes > 30 seconds
- When spawning task agents (include timeout expectations)
- When checking if you can process AI Maestro messages
- When deciding whether to wait or delegate

---

### Orchestrator Guardrails ([references/orchestrator-guardrails.md](references/orchestrator-guardrails.md))

Detailed role boundaries for orchestrator behavior.

---

### Delegation Checklist ([references/delegation-checklist.md](references/delegation-checklist.md))

Infrastructure task delegation procedures.

---

## Quick Reference Checklist

Use this checklist when orchestrating multi-developer work:

- [ ] Break down the goal into independent tasks (Phase 1)
- [ ] Define success criteria for each task clearly
- [ ] Assign one task per agent/developer
- [ ] Provide complete task instructions with context and dependencies
- [ ] Define clear scope boundaries for each task
- [ ] Request minimal status reports (1-2 lines)
- [ ] Create tracking mechanism (GitHub issues or task list)
- [ ] **PROACTIVELY** monitor progress every 10-15 minutes
- [ ] **PROACTIVELY** send status request messages if no update received
- [ ] **PROACTIVELY** offer solutions when agents report blockers
- [ ] Identify blocked tasks at first status checkpoint
- [ ] Escalate blocked tasks immediately
- [ ] **PROACTIVELY** remind agents of pending tasks
- [ ] Collect all task results
- [ ] **Require 4 verification loops before any PR** (see [verification-loops.md](references/verification-loops.md))
- [ ] Verify completion against success criteria
- [ ] Document lessons learned

---

## Examples

### Example 1: Coordinating Code Review Across 5 Developers

An orchestrator needs to coordinate code reviews for a large codebase across 5 developers.

**Orchestration approach:**
1. Decompose the codebase into 5 independent sections (no file conflicts)
2. Create one task per developer: "Review section X and report findings"
3. Each developer works independently and reports findings
4. Orchestrator collects reports and prioritizes issues
5. If any section blocks others, escalate immediately

**Success:** All sections reviewed in parallel, maximizing parallel execution efficiency

### Example 2: Parallel Testing with Blocked Database

Testing team needs to run tests in parallel, but one developer is blocked waiting for database setup.

**Orchestration approach:**
1. Identify that database setup is a blocking dependency
2. Escalate database setup to operations team in parallel
3. Assign other tests that don't need database to other developers
4. When database is ready, unblock the waiting developer
5. Continue with database-dependent tests

**Success:** Maximized parallelization despite dependency

---

## File Structure

```
orchestration-patterns/
├── SKILL.md                                    (this file)
├── README.md                                   (skill overview)
└── references/
    ├── task-complexity-classifier.md          (task complexity assessment)
    ├── agent-selection-guide.md               (specialized agent selection)
    ├── project-setup-menu.md                  (interactive project configuration)
    ├── language-verification-checklists.md    (language-specific quality checks)
    ├── progress-monitoring.md                 (proactive monitoring protocol)
    ├── verification-loops.md                  (4-verification-loops before PR)
    ├── orchestrator-no-implementation.md      (RULE 15: no implementation)
    ├── orchestrator-exclusive-communications.md (RULE 16: orchestrator-only comms)
    ├── user-requirements-immutable.md         (RULE 14: immutable requirements)
    ├── non-blocking-patterns.md               (RULE 17: stay responsive)
    ├── orchestrator-guardrails.md             (role boundaries)
    └── delegation-checklist.md                (infrastructure delegation)
```

---

## Important Notes

1. **Never block the orchestrator** - Delegate all long-running tasks to agents so you remain available
2. **RULE 17: Stay responsive** - Any operation > 30 seconds MUST be delegated; check AI Maestro messages every 10-15 min
3. **One task per agent** - Clear task boundaries prevent confusion and conflicts
4. **Minimal status reports** - Request 1-2 line updates only (e.g., "[DONE] task-name - result")
5. **Early escalation** - Identify blocks at first status checkpoint; escalate immediately
6. **Clear success criteria** - Each task must have unambiguous completion conditions
7. **PROACTIVE monitoring** - Poll agents every 10-15 minutes; never wait passively for updates
8. **PROACTIVE unblocking** - Offer solutions immediately when blockers are reported
9. **4-verification-loops** - Agent asks "Can I PR?" 5 times; first 4 times respond "Check your changes for errors"; only approve on 5th if no issues remain
10. **Orchestrator-exclusive communications** - ONLY the orchestrator can send messages or commit changes. Sub-agents prepare content but NEVER send externally. Include this constraint in every sub-agent prompt.
11. **Parallel agent spawning** - Spawn up to 20 agents simultaneously for independent tasks; never wait sequentially

---

## Next Steps

1. Start with [Task Complexity Classifier](./references/task-complexity-classifier.md) to understand how to evaluate tasks
2. Read [Agent Selection Guide](./references/agent-selection-guide.md) to learn which agents handle which tasks
3. Run [Project Setup Menu](./references/project-setup-menu.md) before beginning any new project
4. Apply [Language Verification Checklists](./references/language-verification-checklists.md) when reviewing deliverables
5. Read [Progress Monitoring](./references/progress-monitoring.md) for proactive agent management
6. Read [Verification Loops](./references/verification-loops.md) for mandatory PR verification
7. Read [Orchestrator No Implementation](./references/orchestrator-no-implementation.md) for role boundaries (RULE 15)
8. Read [Orchestrator-Exclusive Communications](./references/orchestrator-exclusive-communications.md) for communication restrictions (RULE 16)
9. Read [User Requirements Immutable](./references/user-requirements-immutable.md) for requirement handling (RULE 14)
10. Read [Non-Blocking Patterns](./references/non-blocking-patterns.md) for async delegation and responsiveness (RULE 17)
11. Use the Quick Reference Checklist above for all orchestration work

---

## Error Handling

| Issue | Cause | Resolution |
|-------|-------|------------|
| Agent unresponsive | Agent crashed or blocked | Poll every 5 min, reassign after 30 min |
| Task conflict | Same file modified by multiple agents | Assign non-overlapping scope |
| Verification loop stuck | Agent doesn't check changes | Send explicit verification message |
| Escalation timeout | User unavailable | Queue issue, continue other work |

See individual reference files for detailed troubleshooting.

---

## Resources

- [task-complexity-classifier.md](references/task-complexity-classifier.md) - Complexity assessment
- [agent-selection-guide.md](references/agent-selection-guide.md) - Agent selection
- [project-setup-menu.md](references/project-setup-menu.md) - Project configuration
- [language-verification-checklists.md](references/language-verification-checklists.md) - Quality checks
- [progress-monitoring.md](references/progress-monitoring.md) - Proactive monitoring
- [verification-loops.md](references/verification-loops.md) - 4-verification protocol
- [orchestrator-no-implementation.md](references/orchestrator-no-implementation.md) - RULE 15
- [orchestrator-exclusive-communications.md](references/orchestrator-exclusive-communications.md) - RULE 16
- [user-requirements-immutable.md](references/user-requirements-immutable.md) - RULE 14
- [non-blocking-patterns.md](references/non-blocking-patterns.md) - RULE 17
