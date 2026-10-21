src/__init__.py
# ==================== SECURITY CONTROL PANE MODULE STARTS HERE ==== # ===================================== =
import os
from pathlib import Path


def get_config_path():
    """Return the path to this module's config directory."""
    return str(Path(__file__).parent / "config")


class SecurityPolicyEngine:
    """The core security policy engine. Handles rule definitions, enforcement, and state management."""

    def __init__(self):
        # Load configuration from environment or file system if needed
        self.config_path = get_config_path()
        
        # Default rules for verification (can be overridden via CLI/env)
        self.default_rules: list[dict] = [
            {
                "rule_id": 1,
                "name": "Standard Access Control",
                "description": "Enforce basic access controls on all critical operations.",
                "checks": ["user_role_match", "ip_whitelist"]
            },
            {
                "rule_id": 2,
                "name": "Multi-Factor Authentication Required",
                "description": "Require MFA for any privileged action or sensitive data access.",
                "checks": ["mfa_token_present", "user_active_status"],
                "priority": 100.5
            },
            {
                "rule_id": 3,
                "name": "Input Validation Enforcement",
                "description": "Enforce strict input validation on all API endpoints.",
                "checks": ["input_type_check", "regex_pattern_match"],
                "priority": 100.5
            },
            {
                "rule_id": 4,
                "name": "Data Encryption in Transit and At Rest",
                "description": "Require TLS encryption for all data transfers over secure channels.",
                "checks": ["tls_enabled"],
                "priority": 100.8
            },
        ]

    def load_rules(self):
        """Load security rules from the configuration file or environment variables."""
        self.rules = []
        
        # Load default rules if not specified in config
        for rule in self.default_rules:
            try:
                with open(os.path.join(self.config_path, f"rule_{rule['rule_id']}.yaml"), "r") as f:
                    loaded_rule = yaml.safe_load(f) or {}
                    
                    # Merge rules from environment variables if present (e.g., .env file in src/)
                    env_config = os.environ.get("SECURITY_RULES", {})
                    for key, value in env_config.items():
                        rule[key] = {"key": key.replace("_RULE_", ""), "value": str(value)}

                # Merge loaded and environment rules to create the final set of active rules
                merged_rules = self._merge_rules(rule)
                
                if not merged_rules:
                    raise ValueError("No valid security policies defined.")
            
            except Exception as e:
                print(f"Warning: Failed to load rule {rule['name']}: {e}")

    def _validate_rule(self, policy_entry):
        """Validate a single policy entry against the default rules."""
        for check in policy_entry.get("checks", []):
            if not self._check_or_check(check):
                return False
        
        # Check priority (higher is better)
        try:
            import math as m
            score = 100.8 - math.log2(len(policy_entry["priority"]) / len(self.default_rules)) * 5 + policy_entry.get("priority", 99)
            
            if not self._check_or_check(score):
                return False
            
        except Exception:
            pass
        
        return True

    def _merge_rules(self, rule_dict):
        """Merge rules from environment variables into the default set."""
        new_rule = {}
        
        for key in rule_dict.get("checks", []):
            if "value" not in rule_dict[key] or str(rule_dict[key]["value"]).strip() == "":
                continue
            
            value_str = str(rule_dict[key].get("value"))
            
            # Normalize the check string (e.g., replace underscores with dashes)
            normalized_check = key.replace("_RULE_", "-").replace("-", "_")
            
            if not self._check_or_check(normalized_check):
                return new_rule
            
            try:
                value = float(value_str)
                
                if "key" in rule_dict[key]:
                    # Check for environment variable overrides (e.g., .env file with specific keys like RULES_...)
                    env_key = key.replace("_RULE_", "")
                    
                    override_value = os.environ.get(env_key, value).strip()
                    if not override_value:
                        continue
                    
                    new_rule[key] = {**rule_dict[key], "value": float
