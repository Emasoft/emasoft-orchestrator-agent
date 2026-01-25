#!/usr/bin/env python3
"""
Generate Messages Script

Generates message templates for agent communication.

Usage:
    python generate_messages.py assignment <module_id> <agent_id>
    python generate_messages.py poll <module_id> <poll_number>
    python generate_messages.py correction <module_id>
    python generate_messages.py authorization <module_id>

Examples:
    python generate_messages.py assignment auth-core implementer-1
    python generate_messages.py poll auth-core 3
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml

STATE_FILE = Path("atlas_state.yaml")


def load_state() -> dict:
    """Load the current state file."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


def find_module(state: dict, module_id: str) -> dict | None:
    """Find a module by ID."""
    modules = state.get("modules", {})
    if module_id in modules:
        return {"id": module_id, **modules[module_id]}
    return None


def generate_assignment_message(module_id: str, agent_id: str) -> dict:
    """Generate an assignment message template."""
    state = load_state()
    module = find_module(state, module_id)

    task_uuid = f"task-{uuid.uuid4().hex[:8]}"

    body = f"""## Assignment

You have been assigned to implement: **{module_id}**

Task UUID: {task_uuid}

## Module Description

{module.get('description', '[Add module description here]') if module else '[Module not found - add description]'}

## Requirements Summary

{module.get('requirements', '[Add numbered requirements here]') if module else '[Add requirements]'}

## Acceptance Criteria

{module.get('acceptance_criteria', '[Add acceptance criteria as checklist]') if module else '[Add acceptance criteria]'}

## Dependencies

{module.get('dependencies', 'None') if module else 'None'}

## Estimated Effort

{module.get('estimated_hours', '2-4') if module else '2-4'} hours

## MANDATORY: Instruction Verification

Before you begin implementation, please:

1. **Repeat the key requirements** in your own words (3-5 bullet points)
2. **List any questions** you have about the requirements
3. **Confirm your understanding** of the acceptance criteria

I will verify your understanding before authorizing implementation.

Reply with your understanding summary.
"""

    return {
        "type": "assignment",
        "to": agent_id,
        "subject": f"[TASK] Module: {module_id} - UUID: {task_uuid}",
        "priority": "high",
        "body": body,
        "task_uuid": task_uuid
    }


def generate_poll_message(module_id: str, poll_number: int) -> dict:
    """Generate a poll message template."""
    body = """## Status Request

Please provide your current status:

1. **Current progress**: What percentage complete? What specific items are done?
2. **Next steps**: What are you working on right now?

## MANDATORY Questions (Answer ALL)

3. **Are there any issues or problems?**
   - Technical issues (code not working, tests failing)
   - Environmental problems (dependencies, configuration)
   - Dependency issues (waiting on other modules)

4. **Is anything unclear?**
   - Requirements ambiguity
   - Acceptance criteria questions
   - Expected behavior uncertainty

5. **Any unforeseen difficulties?**
   - Complexity higher than expected
   - Missing information discovered
   - Approach not working as planned

6. **Do you need anything from me?**
   - Documentation needed
   - Clarification required
   - Decision needed from orchestrator/user
   - Resources or access required

---

If all is clear with no blockers, reply:
"Progress: X%. No blockers. Proceeding as planned."

Expected response time: 5 minutes
"""

    return {
        "type": "poll",
        "subject": f"[POLL] Module: {module_id} - Progress Check #{poll_number}",
        "priority": "normal",
        "body": body
    }


def generate_correction_message(module_id: str) -> dict:
    """Generate a correction message template."""
    body = """## Corrections Required

Your understanding has some issues that need correction:

**Incorrect:**
- [Describe what was incorrect]
- [Actual correct information]

**Missing:**
- [What was not mentioned but should be]
- [Additional missing items]

**Misunderstood:**
- [What was misunderstood]
- [Correct interpretation]

## Please Revise

Please provide a revised understanding summary addressing these corrections.

Do NOT begin implementation until your understanding is verified.
"""

    return {
        "type": "correction",
        "subject": f"[CORRECTION] Module: {module_id} - Understanding Needs Revision",
        "priority": "high",
        "body": body
    }


def generate_authorization_message(module_id: str) -> dict:
    """Generate an authorization message template."""
    now = datetime.now(timezone.utc).isoformat()

    body = f"""## Implementation Authorized

Your understanding is verified. You may begin implementation.

**Module**: {module_id}
**Authorized at**: {now}

## Reminders

- I will check in every 10-15 minutes
- Report any issues immediately - don't struggle in silence
- Ask questions as they arise
- Commit frequently with clear messages

Good luck!
"""

    return {
        "type": "authorization",
        "subject": f"[AUTH] Module: {module_id} - Implementation Authorized",
        "priority": "high",
        "body": body
    }


def main():
    parser = argparse.ArgumentParser(description="Generate message templates")
    parser.add_argument("message_type", choices=["assignment", "poll", "correction", "authorization"],
                       help="Type of message to generate")
    parser.add_argument("module_id", help="Module ID")
    parser.add_argument("extra", nargs="?", help="Agent ID (for assignment) or poll number (for poll)")

    args = parser.parse_args()

    if args.message_type == "assignment":
        if not args.extra:
            print("Error: Agent ID required for assignment message", file=sys.stderr)
            sys.exit(1)
        result = generate_assignment_message(args.module_id, args.extra)
    elif args.message_type == "poll":
        poll_num = int(args.extra) if args.extra else 1
        result = generate_poll_message(args.module_id, poll_num)
    elif args.message_type == "correction":
        result = generate_correction_message(args.module_id)
    elif args.message_type == "authorization":
        result = generate_authorization_message(args.module_id)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
