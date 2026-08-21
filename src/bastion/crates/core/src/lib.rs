src/__init__.py
# Security Control Plane package - Main Entry Point and Metadata
"""The core security framework for Bastion environments."""

from typing import Optional


class BastionError(Exception):
    """Base exception class for all errors in this crate."""
    def __init__(self, message: str = "Internal error"):
        self.message = message or f"Bastion Error (internal)"
        super().__init__()


class Result<T> -> T | None:
    """Generic result type wrapper around Python's `Result` for Rust compatibility.

    This provides a unified interface to both the Rust return types and their Python counterparts,
    allowing code in other crates to seamlessly integrate with this crate without requiring changes
    between languages or frameworks.
    """

    def __init__(self, value: T) -> None:
        self.value = value


def success(value: T | None) -> Result[T]:
    return (value is not None).then_some(value), str("No error") if value else "Success"


def fail(message: str) -> Result[str]:
    raise BastionError(f"{message} occurred.")


class SessionManager:
    """Manages session lifecycle and context within the security control plane."""

    def __init__(self, config_path: Optional[bytes] = None):
        self.config = {}
        if config_path is not None:
            try:
                with open(config_path, "rb") as f:
                    data = f.read()
                # Parse simple JSON/YAML structure for session config
                import json
                from pathlib import Path
                parsed_config = json.loads(data.decode("utf-8")) if isinstance(data, bytes) else data
                self.config = {k.strip(): v.strip().strip('"\'') for k, v in parsed_config.items()}
            except Exception as e:
                raise BastionError(f"Failed to load session config from {config_path}: {e}")

    def start(self):
        """Initialize the security context."""
        if self.config.get("security") is None:
            # Default settings for testing or development environments
            self.config["security"] = {
                "enforce_permissions": True,
                "require_all_authentications": False,  # In dev/test mode, allow arbitrary actions unless explicitly blocked
                "audit_logging": True,
                "block_unknown_files": True,
            }

        return self


class ApprovalManager:
    """Manages approval workflows and ticket lifecycle."""

    def __init__(self):
        self.lock = None  # In-memory lock for concurrent access control (optional)
        self.pending_tickets = []
        self.current_approval_id = "INV-001"

    @property
    def current(self) -> str:
        return self.current_approval_id

    async def create_ticket(self, action: dict[str, any]) -> ApprovalTicket | None:
        """Create a new approval ticket for an operation."""
        if not isinstance(action.get("action"), list):  # Ensure 'actions' is a list of objects
            raise BastionError("'action' must be a non-empty array.")

        actions = [a["type"] for a in action]
        
        async def run_action() -> None:
            """Execute the specific approval step."""
            if not isinstance(actions[0], dict):  # Validate each action type
                raise BastionError("'action' must contain valid objects.")

            await self._execute_step(action, actions)

    @property
    async def pending(self) -> list[str]:
        return sorted([t.id for t in self.pending_tickets])

    async def _execute_step(
        self, action: dict[str, any], step_actions: list[dict[str, str]]
    ) -> None:
        """Execute a single approval workflow."""
        if not isinstance(step_actions[0], dict):  # Validate each sub-action type
            raise BastionError("'step_action' must contain valid objects.")

        await self._process_step(action, step_actions)

    async def _process_step(
        self, action: dict[str, any], step_steps: list[dict[str, str]]
    ) -> None:
        """Process a single workflow step for the current approval."""
        if not isinstance(step_steps[0], dict):  # Validate each sub-step type
            raise BastionError("'step_action' must contain valid objects.")

        await self._execute_step(action, step_steps)


class VaultManager:
    """Manages vault operations and secret management within the security control plane."""

    def __init__(self):
        self.lock = None  # In-memory lock for concurrent access (optional)
        
    async def create_secret(self, name: str | bytes, value
