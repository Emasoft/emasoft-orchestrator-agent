#!/usr/bin/env python3
"""
Assign Module Script

Assigns a module to a registered agent with validation.

Usage:
    python assign_module.py <module_id> <agent_id>

Examples:
    python assign_module.py auth-core implementer-1
    python assign_module.py oauth-google dev-alice
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests  # type: ignore[import-untyped]
import yaml

# Configuration
AIMAESTRO_API = "http://localhost:23000"
STATE_FILE = Path("atlas_state.yaml")


def load_state() -> dict:
    """Load the current state file."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


def save_state(state: dict) -> None:
    """Save the state file."""
    with open(STATE_FILE, "w") as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)


def generate_task_uuid() -> str:
    """Generate a unique task UUID."""
    return f"task-{uuid.uuid4().hex[:8]}"


def find_agent(state: dict, agent_id: str) -> dict | None:
    """Find an agent by ID."""
    registered = state.get("registered_agents", {})

    for agent in registered.get("ai_agents", []):
        if agent["agent_id"] == agent_id:
            return {"type": "ai", **agent}

    for dev in registered.get("human_developers", []):
        if dev["agent_id"] == agent_id:
            return {"type": "human", **dev}

    return None


def find_module(state: dict, module_id: str) -> dict | None:
    """Find a module by ID."""
    modules = state.get("modules", {})
    if module_id in modules:
        return {"id": module_id, **modules[module_id]}
    return None


def send_ai_assignment(session_name: str, message: dict) -> bool:
    """Send assignment message via AI Maestro."""
    try:
        response = requests.post(
            f"{AIMAESTRO_API}/api/messages", json=message, timeout=10
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Warning: Failed to send message - {e}", file=sys.stderr)
        return False


def generate_assignment_message(module: dict, agent: dict, task_uuid: str) -> str:
    """Generate the assignment message body."""
    return f"""## Assignment

You have been assigned to implement: **{module["id"]}**

Task UUID: {task_uuid}

## Module Description

{module.get("description", "No description provided.")}

## Requirements Summary

{module.get("requirements", "See GitHub issue for requirements.")}

## Acceptance Criteria

{module.get("acceptance_criteria", "See GitHub issue for acceptance criteria.")}

## MANDATORY: Instruction Verification

Before you begin implementation, please:

1. **Repeat the key requirements** in your own words (3-5 bullet points)
2. **List any questions** you have about the requirements
3. **Confirm your understanding** of the acceptance criteria

I will verify your understanding before authorizing implementation.

Reply with your understanding summary.
"""


def assign_module(module_id: str, agent_id: str) -> dict:
    """Assign a module to an agent."""
    state = load_state()

    # Validate module exists
    module = find_module(state, module_id)
    if not module:
        available = list(state.get("modules", {}).keys())
        return {
            "success": False,
            "error": f"Module '{module_id}' not found",
            "available_modules": available,
        }

    # Check module is not already assigned
    if module.get("status") == "assigned" or module.get("status") == "in_progress":
        return {
            "success": False,
            "error": f"Module '{module_id}' is already assigned to '{module.get('assigned_to')}'",
        }

    # Validate agent exists
    agent = find_agent(state, agent_id)
    if not agent:
        return {"success": False, "error": f"Agent '{agent_id}' is not registered"}

    # Check agent is available
    if agent.get("status") == "busy":
        return {
            "success": False,
            "error": f"Agent '{agent_id}' already has an active assignment ({agent.get('current_assignment')})",
        }

    # Generate task UUID
    task_uuid = generate_task_uuid()

    # Create assignment record
    assignment = {
        "agent": agent_id,
        "agent_type": agent["type"],
        "module": module_id,
        "task_uuid": task_uuid,
        "assigned_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending_verification",
        "instruction_verification": {
            "status": "awaiting_repetition",
            "repetition_received": False,
            "repetition_correct": False,
            "questions_asked": 0,
            "questions_answered": 0,
            "authorized_at": None,
        },
        "progress": {"percentage": 0, "last_update": None, "notes": []},
        "polling": {"poll_count": 0, "last_poll": None, "next_poll_due": None},
    }

    # Update state
    if "active_assignments" not in state:
        state["active_assignments"] = []
    state["active_assignments"].append(assignment)

    # Update module status
    state["modules"][module_id]["status"] = "assigned"
    state["modules"][module_id]["assigned_to"] = agent_id
    state["modules"][module_id]["task_uuid"] = task_uuid

    # Update agent status
    for agents_list in [
        state["registered_agents"].get("ai_agents", []),
        state["registered_agents"].get("human_developers", []),
    ]:
        for a in agents_list:
            if a["agent_id"] == agent_id:
                a["status"] = "busy"
                a["current_assignment"] = module_id
                a["current_task_uuid"] = task_uuid

    save_state(state)

    # Send assignment message for AI agents
    message_sent = False
    if agent["type"] == "ai":
        message_body = generate_assignment_message(module, agent, task_uuid)
        message = {
            "to": agent["session_name"],
            "subject": f"[TASK] Module: {module_id} - UUID: {task_uuid}",
            "priority": "high",
            "content": {"type": "assignment", "message": message_body},
        }
        message_sent = send_ai_assignment(agent["session_name"], message)

    return {
        "success": True,
        "module": module_id,
        "agent": agent_id,
        "agent_type": agent["type"],
        "task_uuid": task_uuid,
        "status": "pending_verification",
        "message_sent": message_sent,
        "next_step": "Wait for agent to respond with understanding summary, then verify before authorizing",
    }


def main():
    parser = argparse.ArgumentParser(description="Assign a module to an agent")
    parser.add_argument("module_id", help="ID of the module to assign")
    parser.add_argument("agent_id", help="ID of the agent to assign to")

    args = parser.parse_args()

    result = assign_module(args.module_id, args.agent_id)

    print(json.dumps(result, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
