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

- **1.1 atlas_start_planning.py** - Initializing Plan Phase Mode
  - Creates orchestrator-plan-phase.local.md
  - Sets up YAML frontmatter with goal
  - Defines exit criteria

- **1.2 atlas_planning_status.py** - Displaying Plan Phase progress
  - Shows plan ID, status, goal
  - Lists modules with status
  - Displays exit criteria checklist

- **1.3 atlas_modify_requirement.py** - Adding, modifying, or removing requirements
  - Add: generates module ID, adds to list
  - Modify: updates fields, logs changes
  - Remove: validates pending status first

- **1.4 atlas_approve_plan.py** - Validating plan and creating GitHub Issues
  - Validates USER_REQUIREMENTS.md exists
  - Creates GitHub Issue per module
  - Sets plan_phase_complete: true

---

## Part 2: Orchestration Basic Scripts

**File:** [script-reference-part2-orchestration-basic.md](script-reference-part2-orchestration-basic.md)

Basic orchestration operations (2.1-2.8):

- **2.1 atlas_start_orchestration.py** - Initializing Orchestration Phase Mode
  - Requires plan_phase_complete: true
  - Copies modules from plan with issue links
  - Initializes agent registry

- **2.2 atlas_orchestration_status.py** - Displaying Orchestration Phase progress
  - Module completion count
  - Active assignments and verification status

- **2.3 atlas_register_agent.py** - Registering remote agents
  - Supports AI and human agents
  - Validates AI sessions via AI Maestro

- **2.4 atlas_assign_module.py** - Assigning module to registered agent
  - Creates assignment record with task UUID
  - Sends AI Maestro message for AI agents
  - Initializes instruction verification

- **2.5 atlas_modify_module.py** - Modifying modules during orchestration
  - Add, modify, remove, prioritize subcommands

- **2.6 atlas_reassign_module.py** - Reassigning module to different agent
  - Notifies old and new agents
  - Resets verification status

- **2.7 atlas_check_remote_agents.py** - Polling active AI agents for status
  - Gets all active AI assignments
  - Sends progress poll to each

- **2.8 atlas_notify_agent.py** - Sending AI Maestro message to specific agent
  - Supports priority levels: normal, high, urgent

---

## Part 3: Orchestration Advanced Scripts

**File:** [script-reference-part3-orchestration-advanced.md](script-reference-part3-orchestration-advanced.md)

Advanced orchestration operations (2.9-2.16):

- **2.9 atlas_check_plan_phase.py** - Checking if Plan Phase is complete
  - Used by stop hook
  - Exit code 2 = incomplete

- **2.10 atlas_check_orchestration_phase.py** - Checking if Orchestration Phase is complete
  - Checks module completion and verification loops
  - Used by stop hook

- **2.11 atlas_sync_github_issues.py** - Syncing modules with GitHub Issues
  - Creates, updates, and closes issues

- **2.12 atlas_verify_instructions.py** - Managing Instruction Verification Protocol
  - Status, record-repetition, record-questions, authorize subcommands

- **2.13 atlas_poll_agent.py** - Sending MANDATORY progress poll
  - Includes all 6 mandatory questions
  - Record response and view history

- **2.14 atlas_update_verification.py** - Managing mid-implementation changes
  - Update types: requirement_change, design_update, spec_clarification, etc.
  - 5-stage verification: pending_receipt -> awaiting_feasibility -> addressing_concerns -> ready_to_resume -> resumed

- **2.15 atlas_init_design_folders.py** - Initializing design folder structure
  - Creates .atlas/ with designs/, config/, handoffs/, archive/
  - Generates templates for each platform

- **2.16 atlas_compile_handoff.py** - Compiling template to handoff document
  - Fills placeholders with module and agent data
  - Outputs to .atlas/handoffs/{agent-id}/

---

## Part 4: Modified Scripts

**File:** [script-reference-part4-modified.md](script-reference-part4-modified.md)

Scripts modified for Two-Phase Mode:

- **3.1 atlas_orchestrator_stop_check.py** - Phase-aware stop hook
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
├── atlas_start_planning.py
├── atlas_planning_status.py
├── atlas_modify_requirement.py
├── atlas_approve_plan.py
├── atlas_start_orchestration.py
├── atlas_orchestration_status.py
├── atlas_register_agent.py
├── atlas_assign_module.py
├── atlas_modify_module.py
├── atlas_reassign_module.py
├── atlas_check_remote_agents.py
├── atlas_notify_agent.py
├── atlas_check_plan_phase.py
├── atlas_check_orchestration_phase.py
├── atlas_sync_github_issues.py
├── atlas_verify_instructions.py
├── atlas_poll_agent.py
├── atlas_update_verification.py
├── atlas_init_design_folders.py
├── atlas_compile_handoff.py
└── atlas_orchestrator_stop_check.py
```
