# Agent Management Commands Skill

Provides commands for registering, assigning work to, and monitoring remote agents (AI agents and human developers) in the EOA orchestration workflow.

## When to Use

Use this skill when you need to:
- Register AI agents or human developers to receive module assignments
- Assign decomposed modules to registered agents
- Poll active agents for progress updates (every 10-15 minutes)
- Execute the mandatory Instruction Verification Protocol
- Troubleshoot communication or assignment issues

## Quick Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/register-agent` | Add agent to registry | Before assigning any modules |
| `/assign-module` | Assign module to agent | After decomposition, when agent is registered |
| `/check-agents` | Poll progress | Every 10-15 minutes during implementation |

## Critical Protocols

1. **Instruction Verification Protocol** - EVERY assignment must complete verification before implementation begins
2. **Progress Polling Protocol** - Poll ALL active agents every 10-15 minutes with mandatory questions

## Key Features

- Support for both AI agents (via AI Maestro) and human developers (via GitHub)
- Pre-assignment validation (module exists, agent registered, not overloaded)
- Response action matrix for handling agent issues
- Message templates for all communication scenarios

## Requirements

- Python 3.8+
- PyYAML
- GitHub CLI (for human developer integration)
- AI Maestro (for inter-agent messaging)

## Files

- `SKILL.md` - Complete skill documentation with command syntax and examples
- `references/` - Detailed docs for protocols, workflows, and troubleshooting
- `scripts/` - Python automation scripts

## Python Scripts

| Script | Purpose |
|--------|---------|
| `register_agent.py` | Register agent programmatically |
| `assign_module.py` | Assign module with validation |
| `poll_agents.py` | Send poll messages to all active agents |
| `generate_messages.py` | Generate message templates |

## Related Skills

- `module-decomposition-commands` - Decompose modules before assignment
- `verification-commands` - Verify completed work
- `github-integration-commands` - GitHub Project management
