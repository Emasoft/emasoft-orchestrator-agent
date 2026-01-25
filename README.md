# Orchestrator Agent (orch-)

**Version**: 1.0.0

## Overview

The Orchestrator Agent handles **task distribution, agent coordination, and progress monitoring**. It receives plans from the Architect and coordinates subagents to implement them.

## Core Responsibilities

1. **Task Distribution**: Break plans into assignable tasks
2. **Agent Coordination**: Manage subagents and remote agents
3. **Progress Monitoring**: Track task completion
4. **Module Management**: Organize work into modules
5. **Verification**: Ensure instructions are followed correctly

## Components

### Agents

| Agent | Description |
|-------|-------------|
| `orch-main.md` | Main orchestrator agent |
| `orch-team-orchestrator.md` | Coordinates team of agents |
| `orch-task-summarizer.md` | Summarizes task progress |
| `orch-checklist-compiler.md` | Creates verification checklists |
| `orch-devops-expert.md` | Handles DevOps tasks |
| `orch-docker-container-expert.md` | Docker and container expertise |

### Commands

| Command | Description |
|---------|-------------|
| `orch-start-orchestration` | Start orchestration phase |
| `orch-register-agent` | Register remote agent |
| `orch-assign-module` | Assign module to agent |
| `orch-reassign-module` | Reassign module |
| `orch-check-agents` | Check agent status |
| `orch-add-module` | Add new module |
| `orch-modify-module` | Modify module |
| `orch-remove-module` | Remove module |
| `orch-prioritize-module` | Change module priority |
| `orch-orchestrator-loop` | Start orchestration loop |
| `orch-orchestrator-status` | Check orchestrator status |
| `orch-cancel-orchestrator` | Cancel orchestration |

### Skills

| Skill | Description |
|-------|-------------|
| `orch-two-phase-mode` | Two-phase orchestration mode |
| `orch-orchestration-commands` | Orchestration command patterns |
| `orch-orchestration-patterns` | Orchestration best practices |
| `orch-remote-agent-coordinator` | Remote agent coordination |
| `orch-agent-management` | Agent lifecycle management |
| `orch-module-management` | Module CRUD operations |
| `orch-verification-patterns` | Instruction verification |
| `orch-developer-communication` | Developer comm patterns |
| `orch-devops-expert` | DevOps expertise |
| `orch-checklist-compiler` | Checklist generation |
| `orch-shared` | Shared utilities |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `orch-orchestrator-stop` | Stop | Block exit until tasks complete |
| `orch-instruction-verification-check` | PreToolUse | Verify instructions before work |
| `orch-polling-reminder` | UserPromptSubmit | Remind to poll progress |
| `orch-file-tracker` | PostToolUse | Track file modifications |

## Workflow

1. Receives plan from Architect (via Assistant Manager)
2. Creates modules from plan
3. Assigns modules to agents
4. Monitors progress via polling
5. Handles failures and reassignments
6. Reports completion to Assistant Manager
7. Hands off to Integrator for quality gates

## Installation

```bash
claude --plugin-dir ./OUTPUT_SKILLS/orchestrator-agent
```

## Validation

```bash
cd OUTPUT_SKILLS/orchestrator-agent
uv run python scripts/orch_validate_plugin.py --verbose
```
