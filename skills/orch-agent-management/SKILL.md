---
name: orch-agent-management-commands
description: "Documents commands for managing remote agents (AI agents and human developers) in Orchestrator Agent. Covers registration, module assignment, progress polling, and the mandatory Instruction Verification Protocol."
license: Apache-2.0
compatibility: "Requires Python 3.8+, PyYAML, GitHub CLI. Requires AI Maestro for inter-agent messaging."
metadata:
  author: Anthropic
  version: 1.0.0
user-invocable: false
context: fork
---

# Agent Management Commands Skill

Master the registration, assignment, and monitoring of remote agents (AI agents and human developers) in the ATLAS orchestration workflow.

---

## When to Use This Skill

Use this skill when you need to:
- Register a new AI agent or human developer to receive module assignments
- Assign a decomposed module to a registered agent
- Poll active agents for progress updates
- Verify agent understanding before implementation begins
- Troubleshoot communication or assignment issues

---

## Quick Reference: The 3 Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/register-agent` | Add agent to registry | Before assigning any modules |
| `/assign-module` | Assign module to agent | After decomposition, when agent is registered |
| `/check-agents` | Poll progress | Every 10-15 minutes during implementation |

---

## CRITICAL PROTOCOLS (Non-Skippable)

### 1. Instruction Verification Protocol

**EVERY assignment MUST follow this protocol before implementation begins.**

See: [instruction-verification-protocol.md](references/instruction-verification-protocol.md)
- 1.1 Why Verification is Mandatory
- 1.2 The 8-Step Verification Process
  - 1.2.1 Send assignment with verification request
  - 1.2.2 Agent repeats key requirements
  - 1.2.3 Verify repetition is correct
  - 1.2.4 Handle incorrect repetition
  - 1.2.5 Agent asks clarifying questions
  - 1.2.6 Answer all questions completely
  - 1.2.7 Confirm final understanding
  - 1.2.8 Authorize implementation
- 1.3 Verification Message Template
- 1.4 Common Verification Failures

### 2. Progress Polling Protocol

**EVERY 10-15 minutes, poll ALL active agents with mandatory questions.**

See: [progress-polling-protocol.md](references/progress-polling-protocol.md)
- 2.1 Why Proactive Polling is Mandatory
- 2.2 The 6 Mandatory Questions
- 2.3 Polling Frequency Rules
  - 2.3.1 Standard polling (10-15 min)
  - 2.3.2 Blocked agent polling (5 min)
  - 2.3.3 Near-completion polling
- 2.4 Poll Message Template
- 2.5 Response Action Matrix
- 2.6 Tracking Poll History

---

## Command 1: /register-agent

Register a remote agent (AI or human) before assigning modules.

### Syntax

```
/register-agent <TYPE> <AGENT_ID> [--session NAME]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `TYPE` | Yes | `ai` or `human` |
| `AGENT_ID` | Yes | Unique identifier |
| `--session` | No | AI Maestro session name (AI agents only) |

### Examples

```bash
# Register AI agent
/register-agent ai implementer-1 --session helper-agent-generic

# Register human developer
/register-agent human dev-alice
```

### Detailed Documentation

See: [agent-registration.md](references/agent-registration.md)
- 3.1 Registering AI Agents
  - 3.1.1 Required information
  - 3.1.2 Session name requirements
  - 3.1.3 Verifying session is active
- 3.2 Registering Human Developers
  - 3.2.1 GitHub username matching
  - 3.2.2 GitHub Project integration
- 3.3 Registration Rules
  - 3.3.1 User-provided only rule
  - 3.3.2 No auto-discovery rule
- 3.4 State File Updates

See: [agent-types.md](references/agent-types.md)
- 4.1 AI Agents
  - 4.1.1 What are AI agents
  - 4.1.2 Communication via AI Maestro
  - 4.1.3 Session requirements
  - 4.1.4 Capabilities and limitations
- 4.2 Human Developers
  - 4.2.1 Communication via GitHub
  - 4.2.2 Assignment via GitHub Projects
  - 4.2.3 Progress tracking via PRs/Issues

---

## Command 2: /assign-module

Assign a module to a registered agent and initiate verification.

### Syntax

```
/assign-module <MODULE_ID> <AGENT_ID>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `MODULE_ID` | Yes | ID of the module to assign |
| `AGENT_ID` | Yes | ID of the registered agent |

### Examples

```bash
# Assign to AI agent
/assign-module auth-core implementer-1

# Assign to human developer
/assign-module oauth-google dev-alice
```

### What Happens After Assignment

1. Validation checks run
2. Assignment record created with task UUID
3. Assignment message sent (AI via AI Maestro, human via GitHub)
4. Status set to `pending_verification`
5. **YOU MUST** execute Instruction Verification Protocol
6. **YOU MUST** begin progress polling after verification

### Detailed Documentation

See: [assignment-workflow.md](references/assignment-workflow.md)
- 5.1 Pre-Assignment Validation
  - 5.1.1 Module exists and is pending
  - 5.1.2 Agent is registered
  - 5.1.3 Agent is not overloaded
- 5.2 Assignment Record Creation
  - 5.2.1 Task UUID generation
  - 5.2.2 Initial status values
- 5.3 Assignment Message Generation
- 5.4 State File Updates
- 5.5 Post-Assignment Workflow

See: [agent-communication-templates.md](references/agent-communication-templates.md)
- 6.1 AI Agent Assignment Message Template
- 6.2 AI Agent Verification Request Template
- 6.3 AI Agent Progress Poll Template
- 6.4 AI Agent Issue Response Template
- 6.5 AI Agent Completion Acknowledgment Template

See: [github-assignment-workflow.md](references/github-assignment-workflow.md)
- 7.1 Human Developer Assignment Process
- 7.2 GitHub Issue Assignment
- 7.3 GitHub Project Card Movement
- 7.4 Label Updates
- 7.5 Tracking Progress via GitHub

---

## Command 3: /check-agents

Poll all active agents for progress with mandatory questions.

### Syntax

```
/check-agents [--agent AGENT_ID]
```

### Options

| Option | Description |
|--------|-------------|
| `--agent` | Poll only a specific agent |

### Examples

```bash
# Poll all active agents
/check-agents

# Poll specific agent
/check-agents --agent implementer-1
```

### The 6 Mandatory Questions

**EVERY poll MUST include these questions. Non-negotiable.**

1. **Current progress** (% complete, what's done)
2. **Next steps** (what you're working on now)
3. **Are there any issues or problems?**
4. **Is anything unclear?**
5. **Any unforeseen difficulties?**
6. **Do you need anything from me?**

### Response Action Matrix

| Agent Response | Orchestrator Action |
|----------------|---------------------|
| Reports issue | Provide solution or delegate research |
| Something unclear | Provide clarification immediately |
| Unforeseen difficulty | Evaluate: adapt approach or reassign |
| Needs documentation | Create/provide detailed docs |
| Needs decision | Make decision or escalate to user |
| Blocked | Unblock immediately (highest priority) |

### Detailed Documentation

See: [progress-polling-protocol.md](references/progress-polling-protocol.md)
- 2.1 Why Proactive Polling is Mandatory
- 2.2 The 6 Mandatory Questions
- 2.3 Polling Frequency Rules
- 2.4 Poll Message Template
- 2.5 Response Action Matrix
- 2.6 Tracking Poll History

---

## Typical Workflow

```
1. User provides agent information
   ↓
2. /register-agent ai implementer-1 --session helper-agent-generic
   ↓
3. Module decomposition complete (separate skill)
   ↓
4. /assign-module auth-core implementer-1
   ↓
5. [MANDATORY] Instruction Verification Protocol
   - Wait for agent to repeat requirements
   - Verify understanding is correct
   - Answer all questions
   - Authorize implementation
   ↓
6. [MANDATORY] Progress Polling (every 10-15 min)
   - /check-agents
   - Ask 6 mandatory questions
   - Respond to issues immediately
   ↓
7. Agent reports completion
   ↓
8. Verify deliverables (separate skill)
```

---

## Python Scripts

The skill includes automation scripts in the `scripts/` folder:

| Script | Purpose |
|--------|---------|
| `register_agent.py` | Register agent programmatically |
| `assign_module.py` | Assign module with validation |
| `poll_agents.py` | Send poll messages to all active agents |
| `generate_messages.py` | Generate message templates |

See script docstrings for usage details.

---

## Troubleshooting

See: [troubleshooting.md](references/troubleshooting.md)
- 8.1 Registration Issues
  - 8.1.1 AI Maestro session not found
  - 8.1.2 Duplicate agent ID
  - 8.1.3 Invalid agent type
- 8.2 Assignment Issues
  - 8.2.1 Module not found
  - 8.2.2 Agent not registered
  - 8.2.3 Agent overloaded
  - 8.2.4 Message delivery failed
- 8.3 Polling Issues
  - 8.3.1 No response from agent
  - 8.3.2 Agent reports being blocked
  - 8.3.3 Progress stalled
- 8.4 Communication Issues
  - 8.4.1 AI Maestro connection failed
  - 8.4.2 GitHub API errors
  - 8.4.3 Message format errors

---

## Related Skills

- `module-decomposition-commands` - Decompose modules before assignment
- `verification-commands` - Verify completed work
- `github-integration-commands` - GitHub Project management
