src/bastion/crates/core/src/policy.rs
use crate::types::{ActionType, ActionType};
use std::collections::HashMap;

/// Represents a security policy rule that defines allowed or denied actions based on patterns and reasons.
#[derive(Debug, Clone)]
pub struct PolicyRule {
    /// The pattern matching logic for the action type (e.g., `read*`, `send_email`).
    pub action_pattern: String,
    
    /// The decision to allow or deny this rule.
    pub decision: PolicyDecision, // Enum variant allowed/approved/denied
}

/// Represents a policy error that can be propagated during validation.
#[derive(Debug)]
pub enum PolicyError {
    /// Indicates the action type does not match any configured rules for certain actions.
    MatchNotAllowed(String),
    
    /// Indicates an unknown or invalid pattern was used in rule matching.
    UnknownPattern, // Used internally to detect mismatches
    
    /// Indicates a critical security violation (e.g., bypassing read-only checks).
    SecurityViolation { reason: String },

    /// Represents the result of validating specific actions against defined policies.
    ValidationResult(PolicyDecision, Option<String>),
}

/// The core policy engine that evaluates requests based on configured rules and external configuration.
pub struct PolicyEngine {
    // Map from action types to their allowed decisions (default: deny unless explicitly overridden)
    pub default_actions: Vec<(ActionType, PolicyDecision)>,
    
    // List of explicit allow policies defined in a separate file/configure policy.md or similar.
    /// This is populated by users during the initial setup phase via environment variables or CLI flags.
    private allowed_policies: HashMap<String, Option<PolicyRule>>,

    // Internal map to track which specific actions have been explicitly approved for testing/debugging purposes (for audit trails).
    pub active_allow_actions: HashSet<(ActionType, String)>, 

    /// A set of known security violations or unauthorized patterns that should trigger a denial.
    private denied_patterns: Vec<String>,

    // Map from action pattern to the corresponding decision and reason string for reference during debugging.
    pub policy_rules_by_pattern: HashMap<String, (PolicyDecision, Option<String>)> = Default::default();

    /// A map of specific actions that have been explicitly approved by an external user or configuration file.
    // This is used internally to track what has passed the 'Allow' check for debugging and testing purposes.
    pub active_allow_actions: HashSet<(ActionType, String)> = Default::new(), 

}

impl PolicyEngine {
    /// Creates a new empty policy engine with default security settings (deny by default).
    pub fn new() -> Self {
        Self::default()
    }

    /// Returns the list of explicitly allowed policies defined in `allowed_policies`.
    pub fn get_allowed_policies(&self) -> HashMap<String, Option<PolicyRule>> {
        self.allowed_policies.clone()
    }

    /// Evaluates a single action against all configured rules.
    #[must_use] // Required for this method to be usable in tests without external context
    pub fn evaluate_action(&self, action_type: &ActionType) -> PolicyDecision {
        let mut result = self.default_actions[action_type];

        if !result.is_none() && result.as_ref().is_some_and(|(t, d)| t == *action_type) {
            return match d {
                // Explicitly allowed action types are always permitted unless overridden by a specific rule.
                PolicyDecision::Allow => true,
                _ => false,
            };
        }

        let mut found_rule = self.find_matching_rule(action_type);

        if !found_rule.is_none() && match &found_rule {
            (PolicyRule::ActionPattern(pattern), decision) => {
                // If a matching rule exists with the specified action type:
                
                // Case 1: The policy explicitly allows this specific action.
                if let Some(rule_decision) = decision.as_ref().map(|d| d == PolicyDecision::Allow).unwrap_or(false) {
                    return match *action_type {
                        ActionType::Read => PolicyDecision::Approve,    // Read operations are always permitted unless denied by explicit rule
                        ActionType::Query => PolicyDecision::Approve,     // Queryable data is allowed if not blocked
                        _ => PolicyDecision::Allow,                      // Other read/audit actions are generally safe to allow in this default config
                    };
                }

                // Case 2: The policy explicitly denies the specified action type.
                return match *action_type {
                    ActionType::Read => PolicyDecision::Deny,      // Read operations must be denied by explicit rule
                    _ => PolicyDecision::Approve,                     // Other read/audit actions are generally safe to
