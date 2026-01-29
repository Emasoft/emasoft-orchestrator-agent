# Script Reference

Complete reference for all Two-Phase Mode Python scripts.

This document serves as an index to the detailed script documentation.

---

## Overview

Two-Phase Mode includes **21 scripts** organized into three categories:

| Category | Script Count | Purpose |
|----------|--------------|---------|
| Plan Phase | 4 | Planning and requirements management |
| Orchestration Phase | 16 | Execution and agent coordination |
| Modified Scripts | 1 | Phase-aware stop hook |

---

## Part 1: Plan Phase Scripts

**File:** [script-reference-part1-plan-phase.md](script-reference-part1-plan-phase.md)

Scripts for managing the Plan Phase:

- **1.1 eoa_start_planning.py** <!-- TODO: Script not implemented --> - Initializing Plan Phase Mode
  - Creates orchestrator-plan-phase.local.md
  - Sets up YAML frontmatter with goal
  - Defines exit criteria

- **1.2 eoa_planning_status.py** <!-- TODO: Script not implemented --> - Displaying Plan Phase progress
  - Shows plan ID, status, goal
  - Lists modules with status
  - Displays exit criteria checklist

- **1.3 eoa_modify_requirement.py** <!-- TODO: Script not implemented --> - Adding, modifying, or removing requirements
  - Add: generates module ID, adds to list
  - Modify: updates fields, logs changes
  - Remove: validates pending status first

- **1.4 eoa_approve_plan.py** <!-- TODO: Script not implemented --> - Validating plan and creating GitHub Issues
  - Validates USER_REQUIREMENTS.md exists
  - Creates GitHub Issue per module
  - Sets plan_phase_complete: true

---

## Part 2: Orchestration Basic Scripts

**File:** [script-reference-part2-orchestration-basic.md](script-reference-part2-orchestration-basic.md)

Basic orchestration operations (2.1-2.8):

- **2.1 eoa_start_orchestration.py** - Initializing Orchestration Phase Mode
  - Requires plan_phase_complete: true
  - Copies modules from plan with issue links
  - Initializes agent registry

- **2.2 eoa_orchestration_status.py** <!-- TODO: Script not implemented --> - Displaying Orchestration Phase progress
  - Module completion count
  - Active assignments and verification status

- **2.3 eoa_register_agent.py** - Registering remote agents
  - Supports AI and human agents
  - Validates AI sessions via AI Maestro

- **2.4 eoa_assign_module.py** - Assigning module to registered agent
  - Creates assignment record with task UUID
  - Sends AI Maestro message for AI agents
  - Initializes instruction verification

- **2.5 eoa_modify_module.py** - Modifying modules during orchestration
  - Add, modify, remove, prioritize subcommands

- **2.6 eoa_reassign_module.py** - Reassigning module to different agent
  - Notifies old and new agents
  - Resets verification status

- **2.7 eoa_check_remote_agents.py** - Polling active AI agents for status
  - Gets all active AI assignments
  - Sends progress poll to each

- **2.8 eoa_notify_agent.py** <!-- TODO: Script not implemented --> - Sending AI Maestro message to specific agent
  - Supports priority levels: normal, high, urgent

---

## Part 3: Orchestration Advanced Scripts

**File:** [script-reference-part3-orchestration-advanced.md](script-reference-part3-orchestration-advanced.md)

Advanced orchestration operations (2.9-2.16):

- **2.9 eoa_check_plan_phase.py** <!-- TODO: Script not implemented --> - Checking if Plan Phase is complete
  - Used by stop hook
  - Exit code 2 = incomplete

- **2.10 eoa_check_orchestration_phase.py** <!-- TODO: Script not implemented --> - Checking if Orchestration Phase is complete
  - Checks module completion and verification loops
  - Used by stop hook

- **2.11 eoa_sync_github_issues.py** <!-- TODO: Script not implemented --> - Syncing modules with GitHub Issues
  - Creates, updates, and closes issues

- **2.12 eoa_verify_instructions.py** - Managing Instruction Verification Protocol
  - Status, record-repetition, record-questions, authorize subcommands

- **2.13 eoa_poll_agent.py** - Sending MANDATORY progress poll
  - Includes all 6 mandatory questions
  - Record response and view history

- **2.14 eoa_update_verification.py** <!-- TODO: Script not implemented --> - Managing mid-implementation changes
  - Update types: requirement_change, design_update, spec_clarification, etc.
  - 5-stage verification: pending_receipt -> awaiting_feasibility -> addressing_concerns -> ready_to_resume -> resumed

- **2.15 eoa_init_design_folders.py** <!-- TODO: Script not implemented --> - Initializing design folder structure
  - Creates design/ with designs/, config/, handoffs/, archive/
  - Generates templates for each platform

- **2.16 eoa_compile_handoff.py** <!-- TODO: Script not implemented --> - Compiling template to handoff document
  - Fills placeholders with module and agent data
  - Outputs to design/handoffs/{agent-id}/

---

## Part 4: Modified Scripts

**File:** [script-reference-part4-modified.md](script-reference-part4-modified.md)

Scripts modified for Two-Phase Mode:

- **3.1 eoa_orchestrator_stop_check.py** <!-- TODO: Script not implemented --> - Phase-aware stop hook
  - Plan Phase: blocks if plan_phase_complete: false
  - Orchestration Phase: blocks if modules incomplete or verification loops remaining
  - Output format: JSON with decision, reason, systemMessage, outputToUser

---

## Quick Reference: Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Error (various - see specific script) |
| 2 | Incomplete (used by stop hook scripts) |

---

## Quick Reference: Script Locations

All scripts are located in the `scripts/` directory:

```
scripts/
├── eoa_start_planning.py           # TODO: Script not implemented
├── eoa_planning_status.py          # TODO: Script not implemented
├── eoa_modify_requirement.py       # TODO: Script not implemented
├── eoa_approve_plan.py             # TODO: Script not implemented
├── eoa_start_orchestration.py
├── eoa_orchestration_status.py     # TODO: Script not implemented
├── eoa_register_agent.py
├── eoa_assign_module.py
├── eoa_modify_module.py
├── eoa_reassign_module.py
├── eoa_check_remote_agents.py
├── eoa_notify_agent.py             # TODO: Script not implemented
├── eoa_check_plan_phase.py         # TODO: Script not implemented
├── eoa_check_orchestration_phase.py # TODO: Script not implemented
├── eoa_sync_github_issues.py       # TODO: Script not implemented
├── eoa_verify_instructions.py
├── eoa_poll_agent.py
├── eoa_update_verification.py      # TODO: Script not implemented
├── eoa_init_design_folders.py      # TODO: Script not implemented
├── eoa_compile_handoff.py          # TODO: Script not implemented
└── eoa_orchestrator_stop_check.py  # TODO: Script not implemented
```
