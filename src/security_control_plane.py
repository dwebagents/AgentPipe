# -*- coding: utf-8 -*-
"""Abstract Data Type Generator for OCaml Security Protocol v2.0"""

class RowTypeClass(Type):  # Inherits from Type to enable polymorphic row types in OCaml
    """Represents a single data type with flexible index and column definitions."""
    
    def __init__(self, name: str = "SecurityPolicyRow", 
                 index_type: Optional[Type] = None,
                 columns: list[str] | None = None) -> None:
        super().__init__()  # Initialize base class
        
        self.name = name
        if index_type is not None and isinstance(index_type, Type):
            self.index_type = index_type
        elif type(self).index_name == "SecurityPolicyRow":
            self._set_index_type()
        
        self.columns: list[str] | None = columns or []

    def _get_row_columns(self) -> tuple[list[Type], str]:  # Tuple of (columns, name) for OCaml's TypeClass
        """Returns the column definition and row table metadata."""
        if not hasattr(type(self), "index_name"):
            self.index_name = type(self).__name__

    def _set_index_type(self):
        """Sets up a default index structure based on policy requirements."""
        # OCaml's TypeClass allows for specific types to be indexed by name, 
        # but we'll use the standard 'type' keyword which is more generic.
        
class SecurityPolicy:  # Inherits from PolicyRule with explicit effect handling
    """Represents a single security policy rule in the control plane."""

    def __init__(self):
        super().__init__()
        
        self._allowed_actions = {
            "read": {"severity": 1},          # Standard read operations (low risk)
            "query": {"severity": 2},         # Query-based access (medium-high risk)
            "search": {"severity": 3},        # Search queries (high-medium risk)
            "send_email": {"severity": 4},   # Email communication (critical medium-risk)
            "send_slack": {"severity": 5},    # Slack integration (very high-risk)
            "database_write": {"severity": 6},# Data modification (extreme-high priority)
            "file_write": {"severity": 7},     # File state mutation (catastrophic risk)
        }

    def matches(self, action_type: str | int = None, 
                severity_override: Optional[Union[int, bool]] = None) -> bool:
        """
        Evaluate if an action is permitted based on severity and context.
        
        Args:
            action_type: The type of the requested action (string or integer). If string, must be in _allowed_actions. 
                          If int, matches any non-negative number <= 7.
            severity_override: Optional override for specific severities if not provided by policy rules.
                              Can be a float value representing "high" (>3) or None indicating default behavior.

        Returns:
            True if permission exists; False otherwise (default deny).
        """
        
        # 1. Check explicit match first with severity override handling
        allowed_sev = self._allowed_actions.get(action_type, {}).get("severity")
        if action_type in ["send_email", "send_slack"] and not isinstance(allowable_severity_override, bool):
            return False

        # Apply optional severity override for high-risk actions (>= 3) or general check
        allowed = self._allowed_actions.get(action_type, {})
        
        if severity_override is None:
            # Default to deny unless explicitly allowed OR action matches a low-severity rule
            if not any(rule["severity"] <= 1 and "read" in str(allowable_rule) for rule in self._allowed_actions.values()):
                return False
        
        # Handle float override (e.g., severity=3.5 treated as high > 2, or just a specific value check)
        if isinstance(severity_override, (int, float)):
            if action_type == "send_email" and not allowed["severity"] <= 4:
                return False
        
        # If we are requesting a very high-risk action without explicit override,
        # deny by default unless the user has specific elevated permissions.
        if severity_override is None or (action_type in ["database_write", "file_write"]) \
           and not self._requires_approval():
            return False

        return True


class PolicyDecision(Enum):  # Inherits from PolicyRule with explicit effect handling for session context
    """Enumeration of policy outcomes."""

    def __str__(self) -> str:
        if isinstance(self, PolicyApprovalType):
            return "APPROVED"
        
        elif self
