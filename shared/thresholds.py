"""
thresholds.py - Shared constants for Orchestrator Agent.

These thresholds configure behavior for task distribution,
agent coordination, and progress monitoring.
"""

# Task management
MAX_CONCURRENT_AGENTS = 20
MAX_TASKS_PER_MODULE = 10
TASK_TIMEOUT_MINUTES = 30

# Polling configuration
POLL_INTERVAL_SECONDS = 30
MAX_POLL_RETRIES = 3
POLL_TIMEOUT_SECONDS = 10

# Verification thresholds
MAX_VERIFICATION_LOOPS = 4
VERIFICATION_TIMEOUT_SECONDS = 60

# Module management
MAX_MODULES = 50
MODULE_PRIORITY_LEVELS = 5

# Agent management
AGENT_REGISTRATION_TIMEOUT_SECONDS = 30
AGENT_HEARTBEAT_INTERVAL_SECONDS = 60
MAX_AGENT_FAILURES_BEFORE_REASSIGN = 3

# Stop hook configuration
STOP_VERIFICATION_LOOPS = 4
