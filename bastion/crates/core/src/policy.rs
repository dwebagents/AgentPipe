use crate::types::Action;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PolicyDecision {
    Allow,
    Approve,
    Deny,
}

#[derive(Debug, Clone)]
pub struct PolicyRule {
    pub action_pattern: String,
    pub decision: PolicyDecision,
    pub reason: String,
}

pub struct PolicyEngine {
    rules: Vec<PolicyRule>,
}

impl PolicyEngine {
    pub fn new(rules: Vec<PolicyRule>) -> Self {
        Self { rules }
    }

    pub fn default() -> Self {
        Self {
            rules: vec![
                PolicyRule {
                    action_pattern: "read*".to_string(),
                    decision: PolicyDecision::Allow,
                    reason: "Read-only operations".to_string(),
                },
                PolicyRule {
                    action_pattern: "query*".to_string(),
                    decision: PolicyDecision::Allow,
                    reason: "Read-only operations".to_string(),
                },
                PolicyRule {
                    action_pattern: "search*".to_string(),
                    decision: PolicyDecision::Allow,
                    reason: "Read-only operations".to_string(),
                },
                PolicyRule {
                    action_pattern: "send_email".to_string(),
                    decision: PolicyDecision::Approve,
                    reason: "Outbound communication".to_string(),
                },
                PolicyRule {
                    action_pattern: "send_slack".to_string(),
                    decision: PolicyDecision::Approve,
                    reason: "Outbound communication".to_string(),
                },
                PolicyRule {
                    action_pattern: "database_write".to_string(),
                    decision: PolicyDecision::Approve,
                    reason: "Data modification".to_string(),
                },
                PolicyRule {
                    action_pattern: "file_write".to_string(),
                    decision: PolicyDecision::Approve,
                    reason: "State mutation".to_string(),
                },
                PolicyRule {
                    action_pattern: "code_execution".to_string(),
                    decision: PolicyDecision::Deny,
                    reason: "Arbitrary code execution".to_string(),
                },
                PolicyRule {
                    action_pattern: "exfiltrate*".to_string(),
                    decision: PolicyDecision::Deny,
                    reason: "Data exfiltration".to_string(),
                },
                PolicyRule {
                    action_pattern: "deploy*".to_string(),
                    decision: PolicyDecision::Deny,
                    reason: "Deployment operations".to_string(),
                },
                PolicyRule {
                    action_pattern: "*".to_string(),
                    decision: PolicyDecision::Deny,
                    reason: "Default deny".to_string(),
                },
            ],
        }
    }

    pub fn evaluate(&self, action: &Action) -> PolicyDecision {
        for rule in &self.rules {
            if action_pattern_matches(&rule.action_pattern, &action.action_type) {
                return rule.decision;
            }
        }
        PolicyDecision::Deny
    }

    pub fn evaluate_with_reason(&self, action: &Action) -> (PolicyDecision, String) {
        for rule in &self.rules {
            if action_pattern_matches(&rule.action_pattern, &action.action_type) {
                return (rule.decision, rule.reason.clone());
            }
        }
        (
            PolicyDecision::Deny,
            "Default deny: no matching allow rule".to_string(),
        )
    }
}

fn action_pattern_matches(pattern: &str, action_type: &str) -> bool {
    if pattern == "*" {
        return true;
    }
    if pattern.ends_with('*') {
        let prefix = &pattern[..pattern.len() - 1];
        return action_type.to_lowercase().starts_with(prefix);
    }
    action_type.to_lowercase() == pattern.to_lowercase()
}
