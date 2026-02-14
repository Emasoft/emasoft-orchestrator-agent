# AGENT_OPERATIONS.md - EOA Orchestrator

**Single Source of Truth for Emasoft Orchestrator Agent (EOA) Operations**

---

## 1. Session Naming Convention

### Format
```
eoa-<project>-<descriptive>
```

### Examples
- `eoa-svgbbox-orchestrator` - Orchestrator for svgbbox project
- `eoa-main-coordinator` - Main project coordinator
- `eoa-maestro-orchestrator` - AI Maestro system orchestrator

### Rules
- **Prefix**: All EOA sessions MUST start with `eoa-`
- **Project**: Use kebab-case project identifier
- **Descriptive**: Role or scope (usually `orchestrator` or `coordinator`)
- **AI Maestro Identity**: Session name = registry identity for messaging
- **Chosen By**: ECOS (Chief of Staff) when spawning the orchestrator

### Why This Matters
The session name is registered in AI Maestro's agent registry and becomes the messaging address for inter-agent communication. It must be unique and follow the `eoa-` prefix convention for role identification.

---

## 2. Plugin Paths

### Environment Variables

| Variable | Value | Usage |
|----------|-------|-------|
| `${CLAUDE_PLUGIN_ROOT}` | Points to `emasoft-orchestrator-agent/` | Use in scripts, hooks, skill references |
| `${CLAUDE_PROJECT_DIR}` | Points to `~/agents/<session-name>/` | Project root for the orchestrator instance |

### Local Plugin Path Structure
```
~/agents/<session-name>/.claude/plugins/emasoft-orchestrator-agent/
```

**Example**:
```
~/agents/eoa-svgbbox-orchestrator/.claude/plugins/emasoft-orchestrator-agent/
```

### How Plugin is Loaded
The EOA instance is launched with `--plugin-dir` flag:
```bash
--plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-orchestrator-agent
```

This loads ONLY the emasoft-orchestrator-agent plugin into that Claude Code session.

---

## 3. Agent Directory Structure

### Complete Layout
```
~/agents/eoa-<project>-orchestrator/
├── .claude/
│   ├── plugins/
│   │   └── emasoft-orchestrator-agent/  ← Plugin loaded via --plugin-dir
│   │       ├── .claude-plugin/
│   │       │   └── plugin.json
│   │       ├── agents/
│   │       │   └── eoa-orchestrator-main-agent.md
│   │       ├── skills/
│   │       │   ├── eoa-orchestration-patterns/
│   │       │   ├── eoa-task-distribution/
│   │       │   └── ...
│   │       ├── hooks/
│   │       │   └── hooks.json
│   │       └── scripts/
│   └── settings.json  ← Session-specific settings
├── work/  ← Working directory for orchestrator tasks
└── logs/  ← Session logs
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `.claude/plugins/` | Plugin installation location |
| `work/` | Temporary files, task breakdowns, kanban updates |
| `logs/` | Session activity logs, AI Maestro message logs |

---

## 4. How EOA is Created

### ECOS Spawns EOA
ECOS (Chief of Staff) spawns EOA instances using the `ai-maestro-agents-management` skill to create a new agent session:

- **Session name**: `eoa-<project>-orchestrator`
- **Working directory**: `~/agents/<session-name>`
- **Task**: "Orchestrate tasks for <project>"
- **Plugin**: `emasoft-orchestrator-agent` (loaded via `--plugin-dir`)
- **Agent**: `eoa-orchestrator-main-agent`
- **Additional flags**: skip permissions for automation, enable Chrome DevTools MCP, add `/tmp` as working directory

**Verify**: confirm the agent session was created and is responsive.

### Pre-Spawn Setup
Before spawning, ECOS must:
1. Copy the plugin to `~/agents/$SESSION_NAME/.claude/plugins/emasoft-orchestrator-agent/`
2. Register the session name in AI Maestro
3. Create initial task description
4. Set up working directories

---

## 5. Plugin Mutual Exclusivity

### Critical Rule: One Plugin Per Agent Instance

Each EOA instance has **ONLY** the `emasoft-orchestrator-agent` plugin loaded.

**EOA CANNOT access**:
- `emasoft-chief-of-staff-agent` (ECOS) skills
- `emasoft-integrator-agent` (EIA) skills
- `emasoft-architect-agent` (EAA) skills
- `emasoft-assistant-manager-agent` (EAMA) skills

### Why This Matters
Each plugin defines a **role boundary**. EOA's job is to **orchestrate**, not to:
- Make architectural decisions (EAA's job)
- Integrate and review code (EIA's job)
- Coordinate multiple EOA instances (ECOS's job)
- Manage user communication (EAMA's job)

### Cross-Role Communication
All cross-role communication happens via **AI Maestro messages**, not skill sharing.

**Example**:
```
EOA needs architectural guidance
→ EOA sends message to ECOS
→ ECOS delegates to EAA
→ EAA responds with architectural decision
→ ECOS forwards to EOA
→ EOA distributes tasks based on architecture
```

---

## 6. Skill References

### How to Reference Skills in EOA

**CORRECT** (reference by folder name):
```markdown
See skill: **eoa-orchestration-patterns**
See skill: **eoa-task-distribution**
See skill: **eoa-label-taxonomy**
```

**WRONG** (file paths):
```markdown
See ${CLAUDE_PLUGIN_ROOT}/skills/eoa-orchestration-patterns/SKILL.md  ← WRONG
See /path/to/skill/SKILL.md  ← WRONG
```

### Why Folder Names Only?
Claude Code's skill resolution system automatically finds skills by folder name within the loaded plugin. File paths can break if plugin location changes.

### Available EOA Skills

| Skill Folder Name | Purpose |
|-------------------|---------|
| `eoa-agent-replacement` | Handling agent failures and replacement handoff |
| `eoa-checklist-compilation-patterns` | Compiling task checklists for implementers |
| `eoa-developer-communication` | Communicating with human developers |
| `eoa-github-action-integration` | CI/CD pipeline integration |
| `eoa-implementer-interview-protocol` | Pre-task and post-task agent interviews |
| `eoa-label-taxonomy` | GitHub label management and kanban column mapping |
| `eoa-messaging-templates` | AI Maestro message templates and protocols |
| `eoa-module-management` | Module lifecycle management |
| `eoa-orchestration-commands` | Core orchestration slash commands |
| `eoa-orchestration-patterns` | Task orchestration patterns and workflows |
| `eoa-progress-monitoring` | Monitoring implementer agent progress |
| `eoa-remote-agent-coordinator` | Coordinating remote AI agents |
| `eoa-task-distribution` | Distributing tasks to implementer agents |
| `eoa-two-phase-mode` | Two-phase planning and execution mode |
| `eoa-verification-patterns` | Code and deliverable verification patterns |

### NEVER Reference Other Plugins
```markdown
See skill: perfect-skill-suggester  ← WRONG (not loaded in EOA)
See skill: eia-code-review  ← WRONG (EIA plugin not loaded)
```

---

## 7. AI Maestro Communication

### Sending Messages from EOA

#### To ECOS (Chief of Staff)

Send a status message to ECOS using the `agent-messaging` skill:
- **Recipient**: `ecos-chief-of-staff-one`
- **Subject**: "Task Status Update"
- **Content**: "Completed 3/5 tasks. Task #4 blocked on API dependency."
- **Type**: `status`
- **Priority**: `normal`

**Verify**: confirm message delivery.

#### To Implementer Agent

Send a task assignment message to an implementer using the `agent-messaging` skill:
- **Recipient**: `implementer-svgbbox-tests`
- **Subject**: "New Task Assignment"
- **Content**: "Implement unit tests for calculateBBox() function. See GitHub issue #42."
- **Type**: `task`
- **Priority**: `high`

**Verify**: confirm message delivery.

### Reading Messages (EOA Inbox)

Check your inbox using the `agent-messaging` skill:
- **Check unread count**: query how many unread messages exist for your session
- **List unread messages**: retrieve all unread messages for your session
- **Mark as read**: mark a specific message as read by its message ID

**Verify**: confirm all unread messages have been processed.

### Message Priority Levels

| Priority | When to Use | Response Time |
|----------|-------------|---------------|
| `urgent` | Blocker, critical error, ECOS directive | Immediate |
| `high` | Task assignment, deadline approaching | Within 5 minutes |
| `normal` | Status updates, progress reports | Within 15 minutes |
| `low` | FYI, non-actionable information | When convenient |

### Content Types

| Type | Purpose | Example |
|------|---------|---------|
| `task` | Task assignment | "Implement feature X" |
| `status` | Status update | "Completed 3/5 tasks" |
| `blocker` | Blocking issue | "API dependency missing" |
| `request` | Information request | "Need architectural guidance" |
| `report` | Detailed report | "Test results attached" |

---

## 8. EOA Responsibilities

### Core Responsibilities

#### 1. Receive Tasks from ECOS
- ECOS sends task breakdown via AI Maestro message
- EOA acknowledges receipt
- EOA validates task structure and dependencies

#### 2. Distribute Tasks to Implementers
- Break down tasks into implementer-sized units
- Spawn implementer agents using the `ai-maestro-agents-management` skill
- Send task assignments via AI Maestro messages using the `agent-messaging` skill
- Ensure no conflicting tasks (e.g., two agents editing same file)

#### 3. Monitor Progress via Kanban
- Track task status using GitHub Projects labels
- Update kanban columns: `Todo`, `In Progress`, `AI Review`, `Human Review`, `Merge/Release`, `Done`, `Blocked`
- Identify stalled tasks
- Escalate blockers to ECOS

#### 4. Report Status to ECOS
- Send periodic status updates (every 30 minutes or on milestone)
- Report completed tasks
- Escalate blockers immediately
- Provide progress metrics (e.g., "3/5 tasks completed")

#### 5. Coordinate Implementers
- Prevent merge conflicts (assign non-overlapping files)
- Sequence dependent tasks
- Aggregate results from multiple implementers
- Trigger EIA reviews when implementation complete

### What EOA Does NOT Do

| EOA Does NOT | Who Does It | Why |
|--------------|-------------|-----|
| Write production code | Implementer agents | EOA orchestrates, doesn't implement |
| Review code for merge | EIA | Code review is integrator's role |
| Make architectural decisions | EAA | Architecture is architect's role |
| Coordinate multiple orchestrators | ECOS | Chief of Staff coordinates orchestrators |
| Communicate with end users | EAMA | Assistant Manager handles user comms |

### Workflow Pattern

```
ECOS → [Task Breakdown] → EOA
EOA → [Subtask 1] → Implementer-A
EOA → [Subtask 2] → Implementer-B
EOA → [Subtask 3] → Implementer-C
    ↓ (monitor progress)
EOA ← [Subtask 1 Done] ← Implementer-A
EOA ← [Subtask 2 Done] ← Implementer-B
EOA ← [Subtask 3 Blocked] ← Implementer-C
    ↓ (escalate blocker)
EOA → [Blocker Report] → ECOS
    ↓ (aggregate results)
EOA → [Task Complete] → EIA (for review)
```

---

## 9. Wake/Hibernate/Terminate

### Session Lifecycle Management

EOA session lifecycle is managed by ECOS using the `ai-maestro-agents-management` skill.

### Wake (Resume Session)

Use the `ai-maestro-agents-management` skill to wake the session `eoa-<project>-orchestrator`.

**When to wake**:
- New tasks assigned by ECOS
- Implementer reports blocker
- Scheduled status check

**What happens**:
- Tmux session brought to foreground
- EOA checks AI Maestro inbox
- EOA resumes monitoring kanban

### Hibernate (Pause Session)

Use the `ai-maestro-agents-management` skill to hibernate the session `eoa-<project>-orchestrator`.

**When to hibernate**:
- All tasks distributed and in progress
- Waiting for implementer completions
- No active blockers

**What happens**:
- Tmux session detached (keeps running in background)
- EOA continues monitoring via hooks
- EOA can still receive AI Maestro messages

### Terminate (End Session)

Use the `ai-maestro-agents-management` skill to terminate the session `eoa-<project>-orchestrator`.

**When to terminate**:
- All tasks completed and reviewed
- Project milestone reached
- ECOS issues termination directive

**What happens**:
- Tmux session killed
- EOA sends final status report to ECOS
- AI Maestro registry entry marked as terminated
- Working directory preserved at `~/agents/eoa-<project>-orchestrator/`

### Auto-Hibernate Feature

EOA can auto-hibernate after distributing all tasks:

```bash
# In EOA's configuration
AUTO_HIBERNATE_AFTER_DISTRIBUTION=true
AUTO_HIBERNATE_TIMEOUT=300  # 5 minutes of inactivity
```

This prevents EOA from consuming resources while waiting for implementers.

---

## 10. Troubleshooting

### Common Issues

#### Issue: EOA cannot access ECOS skills
**Symptom**: `Skill 'ecos-strategic-planning' not found`
**Cause**: Plugin mutual exclusivity - EOA doesn't have ECOS plugin loaded
**Solution**: Use the `agent-messaging` skill to request ECOS assistance

#### Issue: AI Maestro message not received
**Symptom**: Implementer didn't get task assignment
**Cause**: Wrong session name or API endpoint
**Solution**: Verify session name in registry, check AI Maestro connectivity using the `agent-messaging` skill

#### Issue: Kanban updates not reflected in GitHub
**Symptom**: Labels added but kanban column unchanged
**Cause**: GitHub Projects automation not configured
**Solution**: Check GitHub Projects automation rules, verify API token

#### Issue: Multiple implementers editing same file
**Symptom**: Merge conflicts
**Cause**: EOA didn't check file ownership before assignment
**Solution**: Use `eoa-task-distribution` skill to prevent conflicts

#### Issue: EOA session terminated unexpectedly
**Symptom**: Tmux session not found
**Cause**: System restart or manual kill
**Solution**: ECOS recreates the session using the `ai-maestro-agents-management` skill

---

## Kanban Column System

All projects use the canonical **8-column kanban system** on GitHub Projects:

| Column | Code | Label |
|--------|------|-------|
| Backlog | `backlog` | `status:backlog` |
| Todo | `todo` | `status:todo` |
| In Progress | `in-progress` | `status:in-progress` |
| AI Review | `ai-review` | `status:ai-review` |
| Human Review | `human-review` | `status:human-review` |
| Merge/Release | `merge-release` | `status:merge-release` |
| Done | `done` | `status:done` |
| Blocked | `blocked` | `status:blocked` |

**Task routing**:
- Small tasks: In Progress → AI Review → Merge/Release → Done
- Big tasks: In Progress → AI Review → Human Review → Merge/Release → Done

---

## Wave 1-7 Skill Additions

The following skills were added to EOA (2026-02-06 — 2026-02-07):

| Skill | Purpose |
|-------|---------|
| `eoa-agent-replacement` | Agent failure detection and replacement protocols |
| `eoa-remote-agent-coordinator` | Remote agent coordination and multi-host management |
| `eoa-messaging-templates` | Standardized AI Maestro message templates |
| `eoa-orchestration-patterns` | Task distribution, load balancing, dependency management |
| `eoa-module-management` | Module lifecycle and dependency tracking |

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/pre-push-hook.py` | Pre-push validation (manifest, hooks, lint, Unicode compliance) |
| `scripts/eoa_kanban_manager.py` | Kanban column management |
| `scripts/validate_plugin.py` | Plugin structure validation |
| `scripts/eoa_file_tracker.py` | File change tracking |
| `scripts/eoa_download.py` | Plugin download utility |
| `scripts/eoa_check_verification_status.py` | Verification status checking |
| `scripts/eoa_check_polling_due.py` | Polling schedule management |
| `scripts/eoa_stop_check/` | Stop condition evaluation (phase.py, tasks.py, utils.py) |

---

## Recent Changes (2026-02-07)

- Added 8-column canonical kanban system (unified from 5 conflicting systems)
- Added Wave 1-7 skills: agent-replacement, remote-coordinator, messaging-templates, orchestration-patterns, module-management
- Added Unicode compliance check (step 4) to pre-push hook
- Added `encoding="utf-8"` to all Python file operations
- Unified kanban column names to dash format (`in-progress`, `ai-review`, `merge-release`)
- Synchronized FULL_PROJECT_WORKFLOW.md, TEAM_REGISTRY_SPECIFICATION.md, ROLE_BOUNDARIES.md across all plugins

---

## 11. References

### Related Documentation

> **Cross-Plugin References**: Each Emasoft agent plugin is installed independently. The following plugins have their own AGENT_OPERATIONS.md documenting their role-specific operations. Communication between plugins happens via the `agent-messaging` skill.

- **EAA (Architect Agent)** - Architecture design, planning, and decision records. Plugin: `emasoft-architect-agent`
- **EIA (Integrator Agent)** - Code review, quality gates, PR management. Plugin: `emasoft-integrator-agent`
- **ECOS (Chief of Staff)** - Agent lifecycle management, coordination, and team registry. Plugin: `emasoft-chief-of-staff`
- **EAMA (Assistant Manager)** - User communication and role routing. Plugin: `emasoft-assistant-manager-agent`

### External References
- [AI Maestro API Documentation](https://github.com/Emasoft/ai-maestro/blob/main/docs/API.md)
- [Claude Code Plugin System](https://docs.anthropic.com/claude/docs/plugins)
- [GitHub Projects API](https://docs.github.com/en/graphql/reference/objects#project)

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-04
**Maintained By**: claude-skills-factory
