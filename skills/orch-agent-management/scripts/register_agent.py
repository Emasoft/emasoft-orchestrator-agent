#!/usr/bin/env python3
"""
Register Agent Script

Registers an AI agent or human developer for module assignment.

Usage:
    python register_agent.py ai <agent_id> --session <session_name>
    python register_agent.py human <agent_id>

Examples:
    python register_agent.py ai implementer-1 --session helper-agent-generic
    python register_agent.py human dev-alice
"""

import argparse
import json
import sys
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


def verify_ai_session(session_name: str) -> bool:
    """Verify that an AI Maestro session exists and is active."""
    try:
        response = requests.get(f"{AIMAESTRO_API}/api/agents", timeout=5)
        response.raise_for_status()
        agents = response.json().get("agents", [])

        for agent in agents:
            if agent.get("session_name") == session_name:
                return True
        return False
    except requests.RequestException as e:
        print(f"Warning: Could not verify session - {e}", file=sys.stderr)
        return False


def verify_github_user(username: str) -> bool:
    """Verify that a GitHub user exists (basic check)."""
    # For now, we just check if the username looks valid
    # A real implementation would query GitHub API
    if not username or len(username) < 1:
        return False
    return True


def register_ai_agent(agent_id: str, session_name: str) -> dict:
    """Register an AI agent."""
    state = load_state()

    # Initialize registered_agents if needed
    if "registered_agents" not in state:
        state["registered_agents"] = {"ai_agents": [], "human_developers": []}
    if "ai_agents" not in state["registered_agents"]:
        state["registered_agents"]["ai_agents"] = []

    # Check for duplicate
    for agent in state["registered_agents"]["ai_agents"]:
        if agent["agent_id"] == agent_id:
            return {"success": False, "error": f"Agent ID '{agent_id}' already exists"}

    # Verify session exists
    session_active = verify_ai_session(session_name)

    # Create registration record
    registration = {
        "agent_id": agent_id,
        "session_name": session_name,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "assigned_by_user": True,
        "status": "available" if session_active else "unverified",
        "current_assignment": None,
        "assignments_completed": 0,
    }

    state["registered_agents"]["ai_agents"].append(registration)
    save_state(state)

    return {
        "success": True,
        "agent_id": agent_id,
        "agent_type": "ai",
        "session_name": session_name,
        "session_verified": session_active,
        "status": registration["status"],
    }


def register_human_developer(agent_id: str) -> dict:
    """Register a human developer."""
    state = load_state()

    # Initialize registered_agents if needed
    if "registered_agents" not in state:
        state["registered_agents"] = {"ai_agents": [], "human_developers": []}
    if "human_developers" not in state["registered_agents"]:
        state["registered_agents"]["human_developers"] = []

    # Check for duplicate
    for dev in state["registered_agents"]["human_developers"]:
        if dev["agent_id"] == agent_id:
            return {"success": False, "error": f"Agent ID '{agent_id}' already exists"}

    # Verify GitHub user (basic check)
    user_valid = verify_github_user(agent_id)

    # Create registration record
    registration = {
        "agent_id": agent_id,
        "github_username": agent_id,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "assigned_by_user": True,
        "status": "available" if user_valid else "unverified",
        "current_assignment": None,
        "assignments_completed": 0,
    }

    state["registered_agents"]["human_developers"].append(registration)
    save_state(state)

    return {
        "success": True,
        "agent_id": agent_id,
        "agent_type": "human",
        "github_username": agent_id,
        "status": registration["status"],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Register an agent for module assignment"
    )
    parser.add_argument("type", choices=["ai", "human"], help="Agent type")
    parser.add_argument("agent_id", help="Unique identifier for the agent")
    parser.add_argument("--session", help="AI Maestro session name (for AI agents)")

    args = parser.parse_args()

    if args.type == "ai":
        if not args.session:
            print("Error: --session is required for AI agents", file=sys.stderr)
            sys.exit(1)
        result = register_ai_agent(args.agent_id, args.session)
    else:
        result = register_human_developer(args.agent_id)

    print(json.dumps(result, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
