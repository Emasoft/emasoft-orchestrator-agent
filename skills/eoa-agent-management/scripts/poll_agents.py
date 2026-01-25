#!/usr/bin/env python3
"""
Poll Agents Script

Sends progress poll messages to all active agents with mandatory questions.

Usage:
    python poll_agents.py [--agent AGENT_ID]

Examples:
    python poll_agents.py                    # Poll all active agents
    python poll_agents.py --agent implementer-1  # Poll specific agent
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


def generate_poll_message(module_name: str, poll_number: int, task_uuid: str) -> str:
    """Generate the poll message with mandatory questions."""
    return f"""## Status Request

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
Task UUID: {task_uuid}
"""


def send_poll_message(session_name: str, message: dict) -> bool:
    """Send poll message via AI Maestro."""
    try:
        response = requests.post(
            f"{AIMAESTRO_API}/api/messages", json=message, timeout=10
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(
            f"Warning: Failed to send message to {session_name} - {e}", file=sys.stderr
        )
        return False


def find_agent_session(state: dict, agent_id: str) -> str | None:
    """Find the session name for an AI agent."""
    for agent in state.get("registered_agents", {}).get("ai_agents", []):
        if agent["agent_id"] == agent_id:
            return agent.get("session_name")
    return None


def poll_agent(state: dict, assignment: dict) -> dict:
    """Poll a single agent."""
    agent_id = assignment["agent"]
    agent_type = assignment["agent_type"]
    module_name = assignment["module"]
    task_uuid = assignment["task_uuid"]

    # Get current poll count
    poll_count = assignment.get("polling", {}).get("poll_count", 0) + 1

    result = {
        "agent": agent_id,
        "module": module_name,
        "poll_number": poll_count,
        "success": False,
    }

    if agent_type == "ai":
        session_name = find_agent_session(state, agent_id)
        if not session_name:
            result["error"] = "Session name not found"
            return result

        message_body = generate_poll_message(module_name, poll_count, task_uuid)
        message = {
            "to": session_name,
            "subject": f"[POLL] Module: {module_name} - Progress Check #{poll_count}",
            "priority": "normal",
            "content": {"type": "poll", "message": message_body},
        }

        result["success"] = send_poll_message(session_name, message)
        result["session"] = session_name
    else:
        # For human developers, we would post a GitHub comment
        result["note"] = "Human developer - would post GitHub comment"
        result["success"] = True

    return result


def poll_all_agents(specific_agent: str | None = None) -> dict:
    """Poll all active agents or a specific agent."""
    state = load_state()

    active = state.get("active_assignments", [])

    if not active:
        return {
            "success": True,
            "message": "No active assignments to poll",
            "agents_polled": 0,
        }

    results = []
    now = datetime.now(timezone.utc).isoformat()

    for assignment in active:
        # Skip if not the specific agent (if specified)
        if specific_agent and assignment["agent"] != specific_agent:
            continue

        # Skip if not in implementation phase
        if assignment.get("status") not in ["in_progress", "pending_verification"]:
            continue

        result = poll_agent(state, assignment)
        results.append(result)

        # Update polling state
        if result["success"]:
            if "polling" not in assignment:
                assignment["polling"] = {}
            assignment["polling"]["poll_count"] = result["poll_number"]
            assignment["polling"]["last_poll"] = now

            # Add to poll history
            if "poll_history" not in assignment["polling"]:
                assignment["polling"]["poll_history"] = []
            assignment["polling"]["poll_history"].append(
                {
                    "poll_number": result["poll_number"],
                    "timestamp": now,
                    "status": "sent",
                }
            )

    save_state(state)

    successful = sum(1 for r in results if r["success"])

    return {
        "success": True,
        "agents_polled": len(results),
        "successful": successful,
        "failed": len(results) - successful,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Poll active agents for progress")
    parser.add_argument("--agent", help="Poll only a specific agent")

    args = parser.parse_args()

    result = poll_all_agents(args.agent)

    print(json.dumps(result, indent=2))

    if result.get("failed", 0) > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
