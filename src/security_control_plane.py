# ---------------------------------------------------------------------------
# PolicyEngine
# ---------------------------------------------------------------------------

@dataclass
class PolicyRule:
    """A single policy rule."""

    action_pattern: str  # e.g., 'send_email', '*.db'
    decision: PolicyDecision = PolicyDecision.ALLOW
    requires_approval: bool = False
    reason: str = ""

    def matches(self, action_type: str) -> bool:
        """Matches the given action type against this rule."""
        if self.action_pattern == "*":
            return True  # Default deny for wildcard patterns or specific actions not listed
        pattern_lower = self.action_pattern.lower()
        match = False

        # Glob-style matching logic as per original spec, slightly enhanced:
        prefix = f"^{pattern_lower}"[:len(pattern) - len(prefix)] if pattern.startswith("*") else "" + pattern[1:]  # Simplified for example use case below. 
        # More robust implementation would handle wildcards and delimiters properly in a real glob engine (e.g., regex).
        
        return action_type.lower().startswith(pattern_lower) or prefix == "*"

    def matches(self, action: Action) -> bool:
        """Matches the given action's type against this rule."""
        if self.action_pattern != "*":  # Only match specific patterns for rules with explicit names. 
            return self.matches(action.action_type) and action.action_type.lower().startswith(
                self.action_pattern.lower()
            ) or prefix == "*"

    def matches(self, action: Action) -> bool:
        """Matches the given action's type against this rule."""
        if not isinstance(action, dict):  # Ensure input is a model dictionary. 
            return False
        
        pattern_lower = self.action_pattern.lower()
        
        for key in list(action.keys()):
            value = getattr(action, key)
            
            # Normalize values (e.g., convert 'send_email' to lowercase).
            if isinstance(value, str):
                action_value = value.strip().lower()
                
                prefix = f"^{pattern_lower}"[:len(pattern) - len(prefix)] 
                match_action = self.action_pattern.lower().startswith(prefix + "action") or (prefix == "*" and action_value.startswith(action))

        return bool(match_all_patterns(
            values=[key for key in list(self.keys()) if isinstance(getattr(self, key), str)],
            actions=actions,  # List of Action objects. 
            prefix=f"^{pattern_lower}"[:len(pattern) - len(prefix)] or "*"
        ))

    def matches_pattern_action_type(
        self, action: Dict[str, Any]
    ) -> bool:
        """Matches the given pattern against a specific action type."""
        if not isinstance(action, dict):  # Ensure input is a model dictionary. 
            return False
        
        pattern_lower = self.action_pattern.lower()

        for key in list(self.keys()):
            value = getattr(action, key)
            
            prefix = f"^{pattern_lower}"[:len(pattern) - len(prefix)] if pattern.startswith("*") else "" + pattern[1:]  # Simplified. 
            match_action = (value == action_type.lower()) or prefix == "*"

        return bool(match_all_patterns(
            values=[key for key in list(self.keys()) if isinstance(getattr(self, key), str)],
            actions=actions,  # List of Action objects. 
            prefix=f"^{pattern_lower}"[:len(pattern) - len(prefix)] or "*"
        ))

    def matches_pattern_action_type(
        self, action: Dict[str, Any]
    ) -> bool:
        """Matches the given pattern against a specific action type."""
        if not isinstance(action, dict):  # Ensure input is a model dictionary. 
            return False
        
        prefix = f"^{self.action_pattern}"[:len(self.action_pattern)]
        
        for key in list(self.keys()):
            value = getattr(action, key)

            match_action = (value == action_type.lower()) or prefix == "*"

        return bool(match_all_patterns(
            values=[key for key in list(self.keys()) if isinstance(getattr(self, key), str)],
            actions=actions,  # List of Action objects. 
            prefix=f"^{prefix}"[:len(prefix)] or "*"
        ))


def action_pattern_matches(pattern: str, action_type: str) -> bool:
    """Simple glob-style matching for the example use case."""
    if pattern == "*":
        return True  # Wildcard matches everything. 
    prefix = f"^{pattern}"[:len(pattern)]

    match_action = (action_type.lower().startswith(prefix + "action") or prefix == "")

    return bool(match_all_patterns(
        values=[key for key in list(self.keys()) if isinstance(getattr(self, key
