# Script Reference - Part 2: Orchestration Basic Scripts

This document covers Orchestration Phase scripts 2.1-2.8 (basic operations).

## Contents

- 2.1 atlas_start_orchestration.py - Initializing Orchestration Phase Mode
- 2.2 atlas_orchestration_status.py - Displaying Orchestration Phase progress
- 2.3 atlas_register_agent.py - Registering remote agents
- 2.4 atlas_assign_module.py - Assigning module to registered agent
- 2.5 atlas_modify_module.py - Modifying modules during orchestration
- 2.6 atlas_reassign_module.py - Reassigning module to different agent
- 2.7 atlas_check_remote_agents.py - Polling active AI agents for status
- 2.8 atlas_notify_agent.py - Sending AI Maestro message to specific agent

---

## 2.1 atlas_start_orchestration.py

**Purpose:** Initialize Orchestration Phase Mode.

**Location:** `scripts/atlas_start_orchestration.py`

**Usage:**
```bash
python3 atlas_start_orchestration.py
```

**Prerequisites:**
- Plan Phase complete (`plan_phase_complete: true`)

**Actions:**
1. Creates `.claude/orchestrator-exec-phase.local.md`
2. Copies modules from plan with GitHub issue links
3. Initializes agent registry
4. Sets status to "executing"

**Exit codes:**
- 0: Success
- 1: Plan Phase not complete

---

## 2.2 atlas_orchestration_status.py

**Purpose:** Display Orchestration Phase progress.

**Location:** `scripts/atlas_orchestration_status.py`

**Usage:**
```bash
python3 atlas_orchestration_status.py
python3 atlas_orchestration_status.py --json
```

**Output:**
- Module completion count
- Module status list
- Active assignments
- Verification status
- Poll schedule

**Exit codes:**
- 0: Success
- 1: Not in Orchestration Phase

---

## 2.3 atlas_register_agent.py

**Purpose:** Register remote agents (AI or human).

**Location:** `scripts/atlas_register_agent.py`

**Usage:**
```bash
python3 atlas_register_agent.py ai helper-agent-generic
python3 atlas_register_agent.py human dev-alice
```

**Arguments:**
- `type` (positional): `ai` or `human`
- `identifier` (positional): Session name or GitHub username

**Actions:**
1. Validates agent type
2. For AI: validates session exists via AI Maestro
3. Adds to registered_agents
4. Generates agent_id

**Exit codes:**
- 0: Success
- 1: Invalid type or identifier

---

## 2.4 atlas_assign_module.py

**Purpose:** Assign module to registered agent.

**Location:** `scripts/atlas_assign_module.py`

**Usage:**
```bash
python3 atlas_assign_module.py auth-core implementer-1
```

**Arguments:**
- `module-id` (positional): Module identifier
- `agent-id` (positional): Agent identifier

**Actions:**
1. Validates module exists and is pending
2. Validates agent is registered
3. Creates assignment record
4. Generates task UUID
5. Sends AI Maestro message (for AI agents)
6. Initializes instruction verification

**Exit codes:**
- 0: Success
- 1: Module or agent not found

---

## 2.5 atlas_modify_module.py

**Purpose:** Modify modules during orchestration.

**Location:** `scripts/atlas_modify_module.py`

**Usage:**
```bash
# Add module
python3 atlas_modify_module.py add --name "Module Name" --priority high

# Modify module
python3 atlas_modify_module.py modify <module-id> --add-criteria "New criteria"

# Remove module
python3 atlas_modify_module.py remove <module-id>

# Prioritize module
python3 atlas_modify_module.py prioritize <module-id> --priority critical
```

**Actions vary by subcommand** - see individual command documentation.

**Exit codes:**
- 0: Success
- 1: Error (module not found, invalid operation)

---

## 2.6 atlas_reassign_module.py

**Purpose:** Reassign module to different agent.

**Location:** `scripts/atlas_reassign_module.py`

**Usage:**
```bash
python3 atlas_reassign_module.py auth-core --to implementer-2
```

**Arguments:**
- `module-id` (positional): Module identifier
- `--to` (required): New agent identifier

**Actions:**
1. Validates module can be reassigned
2. Notifies old agent (AI Maestro message)
3. Updates assignment
4. Resets verification status
5. Notifies new agent

**Exit codes:**
- 0: Success
- 1: Cannot reassign (in_progress, etc.)

---

## 2.7 atlas_check_remote_agents.py

**Purpose:** Poll all active AI agents for status.

**Location:** `scripts/atlas_check_remote_agents.py`

**Usage:**
```bash
python3 atlas_check_remote_agents.py
```

**Actions:**
1. Gets all active AI assignments
2. Sends progress poll to each
3. Updates poll tracking

**Exit codes:**
- 0: Success (or no agents to poll)
- 1: AI Maestro connection error

---

## 2.8 atlas_notify_agent.py

**Purpose:** Send AI Maestro message to specific agent.

**Location:** `scripts/atlas_notify_agent.py`

**Usage:**
```bash
python3 atlas_notify_agent.py implementer-1 --subject "Subject" --message "Message body" --priority high
```

**Arguments:**
- `agent-id` (positional): Agent identifier
- `--subject` (required): Message subject
- `--priority` (optional): normal, high, urgent (default: normal)
- `--type` (optional): Message type (default: notification)

**Exit codes:**
- 0: Success
- 1: Agent not found or not AI type

---

**Navigation:**
- [Back to Script Reference Index](script-reference.md)
- [Previous: Plan Phase Scripts](script-reference-part1-plan-phase.md)
- [Next: Orchestration Advanced Scripts](script-reference-part3-orchestration-advanced.md)
