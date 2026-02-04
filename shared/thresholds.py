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


class VERIFICATION:
    """Verification thresholds for statistical and evidence validation.

    WHY: Centralizes verification constants used across verification-patterns scripts.
    WHY: Class-based access (VERIFICATION.ATTR) provides clear namespace separation.
    """

    # Statistical hypothesis testing defaults (A/B testing)
    STATISTICAL_ALPHA: float = 0.05  # Significance level (Type I error rate, 95% confidence)
    STATISTICAL_POWER: float = 0.80  # Statistical power (1 - Type II error rate)
    STATISTICAL_MDE: float = 0.05  # Minimum Detectable Effect (5%)

    # Evidence requirements
    MIN_EVIDENCE_ITEMS: int = 1  # Minimum evidence items required per verification

    # Requirements coverage
    MIN_REQUIREMENTS_COVERAGE: float = 0.80  # 80% minimum coverage threshold


class TIMEOUTS:
    """Timeout constants for various operations.

    WHY: Centralizes timeout values for consistent behavior across scripts.
    WHY: Class-based access (TIMEOUTS.ATTR) provides clear namespace separation.
    """

    # Git operations timeout (seconds)
    GIT: int = 30

    # API operations timeout (seconds)
    API: int = 60

    # File operations timeout (seconds)
    FILE: int = 10

    # Network operations timeout (seconds)
    NETWORK: int = 30
