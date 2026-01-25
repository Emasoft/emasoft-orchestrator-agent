---
name: ao-remote-agent-coordinator
description: Enables the ATLAS-ORCHESTRATOR to delegate coding tasks to remote AI agents and human developers via AI Maestro messaging. The orchestrator NEVER writes code - it creates precise instructions and sends them to remote agents who execute the coding work. Use when onboarding agents, assigning tasks, coordinating multiple agents, or reviewing reports.
license: Apache-2.0
compatibility: Requires AI Maestro messaging system (configurable via AIMAESTRO_API env var, default http://localhost:23000). Python 3.9+ for LSP management scripts.
metadata:
  author: Anthropic
  version: 1.2.0
context: fork
---

# Remote Agent Coordinator

## Overview

The Remote Agent Coordinator enables the ATLAS-ORCHESTRATOR to delegate coding tasks to remote AI agents and human developers via the AI Maestro messaging system. This is the ONLY mechanism through which actual code is written.

**Critical Principle**: The orchestrator NEVER writes code. It creates precise instructions and sends them to remote agents who execute the coding work.

## When to Use

Invoke this skill when:
- Onboarding a new agent to the project
- Assigning a coding task to a remote developer
- Coordinating multiple remote agents on a feature
- Setting up overnight autonomous operation
- Reviewing reports from remote agents
- Escalating issues between agents

---

## Quick Reference: Core Protocols

| Protocol | Reference | Use When |
|----------|-----------|----------|
| Acknowledgment | [echo-acknowledgment-protocol.md](./references/echo-acknowledgment-protocol.md) | Task requires confirmation of receipt |
| 4-Verification Loops | [verification-loops-protocol.md](./references/verification-loops-protocol.md) | Agent requests PR permission |
| Progress Monitoring | [progress-monitoring-protocol.md](./references/progress-monitoring-protocol.md) | Tracking agent progress |
| Error Handling | [error-handling-protocol.md](./references/error-handling-protocol.md) | Agent reports being blocked |
| Escalation | [escalation-procedures.md](./references/escalation-procedures.md) | Issue requires user decision |

---

## MANDATORY: Acknowledgment Protocol

**CRITICAL**: Remote agents DO NOT have this skill. The orchestrator MUST teach them the ACK protocol BY INCLUDING IT IN EVERY TASK DELEGATION MESSAGE.

### ACK Instructions Block (MUST BE IN EVERY TASK DELEGATION)

```
================================================================================
ACKNOWLEDGMENT REQUIRED (MANDATORY)
================================================================================

Before starting work, you MUST reply with an acknowledgment in this exact format:

[ACK] {task_id} - {status}
Understanding: {1-line summary of what you will do}

Status options:
- RECEIVED - Task received, will begin work immediately
- CLARIFICATION_NEEDED - Need more info (list your questions below)
- REJECTED - Cannot accept task (explain why)
- QUEUED - Have prior tasks, will start after completing them

DO NOT begin work until you have sent this acknowledgment.
================================================================================
```

**Full protocol details**: [echo-acknowledgment-protocol.md](./references/echo-acknowledgment-protocol.md)
- 1.0 Purpose and triggers
- 2.0 Message Types: Instructions vs Conversations
- 3.0 ACK Format and Examples
- 4.0 Timeout handling (5 min wait, reminder, reassign)
- 5.0 Proactive enforcement by orchestrator

---

## AI Maestro Messaging

**For messaging, use the official AI Maestro skill:** `~/.claude/skills/agent-messaging/SKILL.md`

### Message Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| `task` | Assign new coding task | Starting work on feature/fix |
| `fix-request` | Request code fix | After PR review finds issues |
| `status-request` | Check on progress | No update received |
| `approval` | Approve completed work | After successful review |
| `escalation` | Escalate to user | Architecture/security decision |

**Full protocol details**: [messaging-protocol.md](./references/messaging-protocol.md)
- 1.0 Sending Messages
- 2.0 Message priorities and timeouts
- 3.0 Task Management messages
- 4.0 Status and Progress messages
- 5.0 Approvals and Rejections
- 6.0 Error Handling

---

## Task Instruction Format

Every task instruction MUST include:
1. **ACK Instructions Block** (at top)
2. **PR Notification Requirement** (mandatory)
3. **Context** - What problem is being solved
4. **Scope** - Exact boundaries (DO/DO NOT lists)
5. **Interface Contract** - Input/output specifications
6. **Files to Modify** - Specific files in scope
7. **Test Requirements** - What tests must pass
8. **Completion Criteria** - How to know when done

**Full template and examples**: [task-instruction-format.md](./references/task-instruction-format.md)
- 1.0 Complete instruction template
- 2.0 Example filled-in instruction
- 3.0 Config reference patterns
- 4.0 Error states and escalation

---

## Agent Response Templates

Include template references in EVERY task delegation:

| Template | Path | Purpose |
|----------|------|---------|
| ACK Response | `templates/ack-response.md` | How to acknowledge task receipt |
| Completion Report | `templates/completion-report.md` | How to report task completion |
| Status Update | `templates/status-update.md` | How to send progress updates |

**Full details**: [agent-response-templates.md](./references/agent-response-templates.md)
- 1.0 Available templates
- 2.0 Including templates in delegations
- 3.0 Generating ad-hoc skills for complex tasks

---

## Agent Onboarding

Before any agent can receive real tasks, they must complete onboarding.

**Quick flow**:
1. Agent reads required documentation
2. Agent sets up environment
3. Agent completes verification task
4. Agent sends registration message
5. Orchestrator approves registration

**Full onboarding guide**: [agent-onboarding.md](./references/agent-onboarding.md)
- 1.0 Onboarding Checklist
- 2.0 Environment Setup
- 3.0 Verification Task
- 4.0 Required Reading List
- 5.0 Roster Registration

**Agent registration format**: [agent-registration.md](./references/agent-registration.md)
- 1.0 Registration fields
- 2.0 Agent Roster management
- 3.0 Availability states

---

## MANDATORY: 4-Verification-Loops Before PR

**CRITICAL**: For EACH TASK, require 4 verification loops BEFORE allowing PR creation.

### Summary: The 5 PR Requests

| PR Request # | Orchestrator Response |
|--------------|----------------------|
| 1st | "Check your changes for errors" (Loop 1) |
| 2nd | "Check your changes for errors" (Loop 2) |
| 3rd | "Check your changes for errors" (Loop 3) |
| 4th | "Check your changes for errors" (Loop 4) |
| 5th | "APPROVED" or "NOT APPROVED - restart" |

**Full protocol**: [verification-loops-protocol.md](./references/verification-loops-protocol.md)
- 1.0 Understanding the 5 PR requests cycle
- 2.0 Verification message templates
- 3.0 Tracking verification state per task
- 4.0 Approval and rejection messages
- 5.0 Enforcement rules (MUST/MUST NOT)

---

## Progress Monitoring (PROACTIVE)

**CRITICAL**: Do not wait passively for updates - actively reach out.

### Proactive Monitoring Principles

1. **PROACTIVELY poll** every 10-15 minutes during active work
2. **PROACTIVELY send** status request if no update received
3. **PROACTIVELY offer** solutions when agents report blockers
4. **PROACTIVELY verify** agents don't stop until ALL tasks complete

**Full protocol**: [progress-monitoring-protocol.md](./references/progress-monitoring-protocol.md)
- 1.0 Polling intervals by task type
- 2.0 Status request messages
- 3.0 Unblocking protocol
- 4.0 No-update escalation timeline

---

## Error Handling

Remote agents must follow **FAIL-FAST**:
- NO workarounds
- NO fallbacks
- If blocked, REPORT and WAIT

**Full protocol**: [error-handling-protocol.md](./references/error-handling-protocol.md)
- 1.0 FAIL-FAST principle
- 2.0 Error report message format
- 3.0 Orchestrator response procedures

---

## Overnight Autonomous Operation

**Prerequisites before leaving**:
1. Agent Roster verified
2. GitHub Project ready
3. Branch permissions set
4. AI Maestro running
5. Tasks queued

**Full guide**: [overnight-operation.md](./references/overnight-operation.md)
- 1.0 Prerequisites Checklist
- 2.0 User Handoff Protocol
- 3.0 Operation Flow
- 4.0 Escalation rules during autonomous operation
- 5.0 Recovery procedures

---

## Escalation Protocol

**Escalate to user when**:
- Architecture decisions not covered by methodology
- Security vulnerabilities discovered
- Dependency conflicts requiring user choice
- Test failures suggesting spec issues

**Full procedures**: [escalation-procedures.md](./references/escalation-procedures.md)
- 1.0 Escalation hierarchy (Level 0-2)
- 2.0 Escalation message formats
- 3.0 Escalation categories
- 4.0 Queue management

---

## LSP Server Requirements

Remote agents MUST have LSP servers installed for working languages.

| Language | LSP Plugin | Install Command |
|----------|-----------|-----------------|
| Python | `pyright-lsp` | `pip install pyright` |
| TypeScript | `typescript-lsp` | `npm install -g typescript-language-server` |
| Rust | `rust-analyzer-lsp` | `rustup component add rust-analyzer` |

**LSP References**:
- [lsp-servers-overview.md](./references/lsp-servers-overview.md) - Available plugins, configuration
- [lsp-installation-guide.md](./references/lsp-installation-guide.md) - Per-language installation
- [lsp-enforcement-checklist.md](./references/lsp-enforcement-checklist.md) - Pre-assignment verification
- [orchestrator-lsp-management.md](./references/orchestrator-lsp-management.md) - Orchestrator LSP guide

---

## Toolchain Template System

Templates provide pre-configured setups for rapid project initialization.

| Category | Purpose |
|----------|---------|
| Toolchain | Language-specific dev configs |
| Handoff | Task delegation formats |
| Report | Status reporting formats |
| GitHub | Kanban and project tracking |

**Full guide**: [toolchain-template-system.md](./references/toolchain-template-system.md)
- 1.0 Template categories
- 2.0 Using compile_template.py
- 3.0 Including templates in delegations

**Template index**: `templates/TEMPLATE_INDEX.md`

---

## ATLAS Document Storage Protocol

Documents are NEVER embedded in AI Maestro messages - only GitHub issue comment URLs.

**Rules**:
1. Upload to GitHub issue comment as attachment
2. Share URL only in messages
3. Require ACK with SHA256 hash
4. Lock files read-only after download

**Full protocol**: [document-storage-atlas.md](./references/document-storage-atlas.md)
- 1.0 Storage architecture
- 2.0 Document delivery rules
- 3.0 Orchestrator scripts
- 4.0 Remote agent storage skill

---

## Configuration References

| Document | Use When |
|----------|----------|
| [central-configuration.md](./references/central-configuration.md) | Setting up `.atlas/` directory structure |
| [change-notification-protocol.md](./references/change-notification-protocol.md) | Notifying agents of config changes |
| [artifact-sharing-protocol.md](./references/artifact-sharing-protocol.md) | Sharing build artifacts between agents |
| [bug-reporting-protocol.md](./references/bug-reporting-protocol.md) | Receiving and handling bug reports |

---

## RULE 15: No Implementation by Orchestrator

**The orchestrator NEVER**:
- Writes code
- Runs builds
- Edits source files
- Sets up infrastructure

**Full rule**: [rule-15-no-implementation.md](./references/rule-15-no-implementation.md)
- 1.0 What orchestrator never does
- 2.0 Task delegation self-check
- 3.0 Correct vs incorrect usage examples

---

## RULE 14: User Requirements Are Immutable

Every task delegation MUST include:
1. **Requirement Reference** - Exact user quotes
2. **Forbidden Actions** - What agents cannot change
3. **Escalation Protocol** - What to do if requirements have issues

**Full rule**: [rule-14-immutable-requirements.md](./references/rule-14-immutable-requirements.md)
- 1.0 Mandatory delegation elements
- 2.0 Violation handling
- 3.0 User decision workflow

---

## Skill Authoring References

| Document | Use When |
|----------|----------|
| [skill-format-comparison.md](./references/skill-format-comparison.md) | Comparing Open Spec vs Claude Code Skills |
| [skill-authoring-best-practices.md](./references/skill-authoring-best-practices.md) | Writing new skills |

---

## Skill Files

```
remote-agent-coordinator/
+-- SKILL.md                              # This file (map/index)
+-- references/
|   +-- agent-onboarding.md               # New agent onboarding guide
|   +-- agent-registration.md             # Agent roster management
|   +-- agent-response-templates.md       # Template usage in delegations
|   +-- artifact-sharing-protocol.md      # Build artifact sharing
|   +-- bug-reporting-protocol.md         # Bug report handling
|   +-- central-configuration.md          # Central source of truth
|   +-- change-notification-protocol.md   # Change notification system
|   +-- document-storage-atlas.md         # ATLAS document storage
|   +-- echo-acknowledgment-protocol.md   # ACK protocol
|   +-- error-handling-protocol.md        # FAIL-FAST and error reports
|   +-- escalation-procedures.md          # Escalation rules
|   +-- lsp-enforcement-checklist.md      # Pre-assignment LSP check
|   +-- lsp-installation-guide.md         # Per-language LSP install
|   +-- lsp-plugin-template.md            # Custom LSP plugin templates
|   +-- lsp-servers-overview.md           # LSP plugins overview
|   +-- messaging-protocol.md             # AI Maestro protocol details
|   +-- orchestrator-lsp-management.md    # Orchestrator LSP guide
|   +-- overnight-operation.md            # Overnight autonomous guide
|   +-- progress-monitoring-protocol.md   # Proactive monitoring
|   +-- rule-14-immutable-requirements.md # User requirements rule
|   +-- rule-15-no-implementation.md      # No orchestrator coding rule
|   +-- skill-authoring-best-practices.md # Skill writing guidance
|   +-- skill-format-comparison.md        # Open Spec vs Claude Code
|   +-- task-instruction-format.md        # Complete instruction template
|   +-- toolchain-template-system.md      # Template system guide
|   +-- toolchain-setup.md                # Toolchain configuration
|   +-- verification-loops-protocol.md    # 4-loop PR verification
+-- scripts/
|   +-- install_lsp.py                    # LSP installation
|   +-- validate_skill.py                 # Skill validation
|   +-- atlas_orchestrator_init.py        # Init storage
|   +-- atlas_register_agent.py           # Register agents
|   +-- atlas_orchestrator_download.py    # Download from agents
|   +-- atlas_search.py                   # Cross-agent search
|   +-- atlas_download.py                 # Basic download
+-- templates/
    +-- protocols/
        +-- DOCUMENT_DELIVERY_PROTOCOL.md
        +-- DOCUMENT_STORAGE_PROTOCOL.md
```

---

## Troubleshooting

### Issue: AI Maestro messages not being delivered

**Cause**: API endpoint unreachable or agent identifier incorrect.

**Solution**:
1. Verify API health: `curl ${AIMAESTRO_API:-http://localhost:23000}/api/health`
2. Check agent ID format (use full session name, not alias)
3. Verify agent is registered in AI Maestro
4. Check network connectivity

### Issue: Agent responds but doesn't understand instructions

**Cause**: Instruction Verification Protocol not executed.

**Solution**:
1. Always execute Instruction Verification Protocol before implementation
2. Request agent to repeat key requirements in their own words
3. Correct any misunderstandings before authorizing work
4. Provide clarification for all questions asked

### Issue: Agent progress stalls without reporting blockers

**Cause**: Proactive polling not configured or agent not responding.

**Solution**:
1. Ensure 10-15 minute polling cycle is active
2. Include ALL mandatory poll questions (issues, unclear items, difficulties)
3. If no response after 2 polls, send escalation message
4. Consider reassigning if agent unresponsive

### Issue: Module assignment conflicts between agents

**Cause**: Same module assigned to multiple agents.

**Solution**:
1. Check current assignments: `/orchestration-status`
2. Use `/reassign-module` to move module to single agent
3. Notify previous assignee to stop work
4. Never assign same module to multiple agents simultaneously

### Issue: Agent completes work but PR fails verification

**Cause**: Acceptance criteria not met or 4-verification-loop not followed.

**Solution**:
1. Review PR against original acceptance criteria
2. Ensure agent followed 4-verification-loop protocol
3. Request fixes for failing criteria
4. Do NOT merge until all criteria pass
