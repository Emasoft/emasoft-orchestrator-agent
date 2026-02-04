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
The ECOS (Chief of Staff) agent spawns EOA instances using the `aimaestro-agent.sh` script:

```bash
SESSION_NAME="eoa-<project>-orchestrator"

aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Orchestrate tasks for <project>" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-orchestrator-agent \
  --agent eoa-orchestrator-main-agent
```

### Breakdown

| Flag | Value | Purpose |
|------|-------|---------|
| `--dir` | `~/agents/$SESSION_NAME` | Sets working directory for the orchestrator |
| `--task` | Task description | Initial task prompt for the orchestrator |
| `--dangerously-skip-permissions` | - | Skip permission dialogs for automation |
| `--chrome` | - | Enable Chrome DevTools MCP |
| `--add-dir` | `/tmp` | Add /tmp as allowed working directory |
| `--plugin-dir` | `~/agents/$SESSION_NAME/.claude/plugins/emasoft-orchestrator-agent` | Load EOA plugin |
| `--agent` | `eoa-orchestrator-main-agent` | Start with this agent from the plugin |

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
See skill: **eoa-kanban-management**
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
| `eoa-orchestration-patterns` | Task orchestration patterns and workflows |
| `eoa-task-distribution` | Distributing tasks to implementer agents |
| `eoa-kanban-management` | Managing GitHub Projects kanban boards |
| `eoa-progress-monitoring` | Monitoring implementer progress |
| `eoa-aimaestro-messaging` | AI Maestro messaging protocols |
| `eoa-error-handling` | Handling implementer errors and blockers |
| `eoa-status-reporting` | Reporting status to ECOS |

### NEVER Reference Other Plugins
```markdown
See skill: perfect-skill-suggester  ← WRONG (not loaded in EOA)
See skill: eia-code-review  ← WRONG (EIA plugin not loaded)
```

---

## 7. AI Maestro Communication

### Sending Messages from EOA

#### To ECOS (Chief of Staff)
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-svgbbox-orchestrator",
    "to": "ecos-chief-of-staff-one",
    "subject": "Task Status Update",
    "priority": "normal",
    "content": {
      "type": "status",
      "message": "Completed 3/5 tasks. Task #4 blocked on API dependency."
    }
  }'
```

#### To Implementer Agent
```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-svgbbox-orchestrator",
    "to": "implementer-svgbbox-tests",
    "subject": "New Task Assignment",
    "priority": "high",
    "content": {
      "type": "task",
      "message": "Implement unit tests for calculateBBox() function. See GitHub issue #42."
    }
  }'
```

### Reading Messages (EOA Inbox)

```bash
# Check unread count
curl -s "$AIMAESTRO_API/api/messages?agent=$SESSION_NAME&action=unread-count"

# List all unread messages
curl -s "$AIMAESTRO_API/api/messages?agent=$SESSION_NAME&action=list&status=unread"

# Mark message as read
curl -X POST "$AIMAESTRO_API/api/messages" \
  -d '{"action":"mark-read","message_id":"<msg-id>"}'
```

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
- Spawn implementer agents via `aimaestro-agent.sh`
- Send task assignments via AI Maestro messages
- Ensure no conflicting tasks (e.g., two agents editing same file)

#### 3. Monitor Progress via Kanban
- Track task status using GitHub Projects labels
- Update kanban columns: `To Do`, `In Progress`, `Review`, `Done`
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

EOA session lifecycle is managed by ECOS via `aimaestro-agent.sh`.

### Wake (Resume Session)

```bash
aimaestro-agent.sh wake eoa-<project>-orchestrator
```

**When to wake**:
- New tasks assigned by ECOS
- Implementer reports blocker
- Scheduled status check

**What happens**:
- Tmux session brought to foreground
- EOA checks AI Maestro inbox
- EOA resumes monitoring kanban

### Hibernate (Pause Session)

```bash
aimaestro-agent.sh hibernate eoa-<project>-orchestrator
```

**When to hibernate**:
- All tasks distributed and in progress
- Waiting for implementer completions
- No active blockers

**What happens**:
- Tmux session detached (keeps running in background)
- EOA continues monitoring via hooks
- EOA can still receive AI Maestro messages

### Terminate (End Session)

```bash
aimaestro-agent.sh terminate eoa-<project>-orchestrator
```

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
**Solution**: Use AI Maestro messaging to request ECOS assistance

#### Issue: AI Maestro message not received
**Symptom**: Implementer didn't get task assignment
**Cause**: Wrong session name or API endpoint
**Solution**: Verify session name in registry, check `$AIMAESTRO_API`

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
**Solution**: ECOS recreates session with `aimaestro-agent.sh create`

---

## 11. References

### Related Documentation
- [EAA_AGENT_OPERATIONS.md](../../emasoft-architect-agent/docs/AGENT_OPERATIONS.md) - Architect operations
- [EIA_AGENT_OPERATIONS.md](../../emasoft-integrator-agent/docs/AGENT_OPERATIONS.md) - Integrator operations
- [ECOS_AGENT_OPERATIONS.md](../../emasoft-chief-of-staff-agent/docs/AGENT_OPERATIONS.md) - Chief of Staff operations
- [EAMA_AGENT_OPERATIONS.md](../../emasoft-assistant-manager-agent/docs/AGENT_OPERATIONS.md) - Assistant Manager operations

### External References
- [AI Maestro API Documentation](https://github.com/Emasoft/ai-maestro/blob/main/docs/API.md)
- [Claude Code Plugin System](https://docs.anthropic.com/claude/docs/plugins)
- [GitHub Projects API](https://docs.github.com/en/graphql/reference/objects#project)

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-04
**Maintained By**: claude-skills-factory
