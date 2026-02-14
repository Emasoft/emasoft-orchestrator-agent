# Orchestrator Agent (eoa-)

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
| `eoa-main.md` | Main orchestrator agent |
| `eoa-team-orchestrator.md` | Coordinates team of agents |
| `eoa-task-summarizer.md` | Summarizes task progress |
| `eoa-checklist-compiler.md` | Creates verification checklists |
| `eoa-docker-container-expert.md` | Docker and container expertise |
| `eoa-experimenter.md` | Experimentation and prototyping |

### Commands

| Command | Description |
|---------|-------------|
| `eoa-start-orchestration` | Start orchestration phase |
| `eoa-register-agent` | Register remote agent |
| `eoa-assign-module` | Assign module to agent |
| `eoa-reassign-module` | Reassign module |
| `eoa-check-agents` | Check agent status |
| `eoa-add-module` | Add new module |
| `eoa-modify-module` | Modify module |
| `eoa-remove-module` | Remove module |
| `eoa-prioritize-module` | Change module priority |
| `eoa-orchestrator-loop` | Start orchestration loop |
| `eoa-orchestrator-status` | Check orchestrator status |
| `eoa-cancel-orchestrator` | Cancel orchestration |

### Skills

| Skill | Description |
|-------|-------------|
| `eoa-two-phase-mode` | Two-phase orchestration mode |
| `eoa-orchestration-commands` | Orchestration command patterns |
| `eoa-orchestration-patterns` | Orchestration best practices |
| `eoa-remote-agent-coordinator` | Remote agent coordination |
| `eoa-module-management` | Module CRUD operations |
| `eoa-verification-patterns` | Instruction verification |
| `eoa-developer-communication` | Developer comm patterns |
| `eoa-checklist-compilation-patterns` | Checklist generation |
| `eoa-agent-replacement` | Agent replacement handoffs |
| `eoa-task-distribution` | Task breakdown and assignment |
| `eoa-progress-monitoring` | Progress tracking and polling |
| `eoa-messaging-templates` | AI Maestro message formats |
| `eoa-label-taxonomy` | GitHub label system |
| `eoa-implementer-interview-protocol` | Interview-based requirements |
| `eoa-github-action-integration` | GitHub Actions patterns |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `eoa-orchestrator-stop` | Stop | Block exit until tasks complete |
| `eoa-instruction-verification-check` | PreToolUse | Verify instructions before work |
| `eoa-polling-reminder` | UserPromptSubmit | Remind to poll progress |
| `eoa-file-tracker` | PostToolUse | Track file modifications |

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
cd OUTPUT_SKILLS/emasoft-orchestrator-agent
uv run python scripts/validate_plugin.py . --verbose
```
