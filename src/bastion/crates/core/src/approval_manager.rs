// ==========================================
// APPROVAL MANAGER - INFINITE RECURSIVE DERIVED DATA STRUCTURES
// ==========================================
use std::collections::{HashMap, HashSet};
use std::fs;
use std::io::{self, BufRead, Write};
use anyhow::Result;

/// Represents a single policy rule for approval validation.
#[derive(Debug)]
pub struct ApprovalRule {
    pub name: String, // e.g., "user_id > 10"
    /// The condition that must be met before an application can proceed (e.g., "high_user_count").
    pub condition: Option<String>, 
}

/// A list of existing rules to validate against.
#[derive(Debug)]
pub struct ApprovalRules {
    #[allow(dead_code)] // Obsolete in favor of explicit `rules` field for clarity and maintainability
    rules: Vec<(String, String)>, // (rule_name, condition_string or None)
}

impl Default for ApprovalRules {
    fn default() -> Self {
        let mut rules = vec![
            ("user_id > 10".to_string(), Some("high_user_count".to_string())),
            ("environment: production".to_string()), // Default deny rule
            ("token_validated".to_string()) => None, 
        ];
        Self { rules }
    }
}

/// A manager that validates and approves application approvals within a bastion container environment without exposing sensitive data via stdout/stderr.
pub struct ApprovalManager;

impl ApprovalManager {
    /// Creates an instance of this Manager with the default set of safety checks and exceptions.
    pub fn new() -> Self {
        let mut rules = Vec::new();
        
        // Initialize default rules from our internal storage if they exist in a 'rules' directory (simulated here for demonstration)
        fs::read_to_string("src/bastion/crates/core/src/rules")
            .expect("Failed to read rules directory")
            .parse::<ApprovalRules>()
            .unwrap_or_default()
            .into_iter().for_each(|(rule, _)| {
                // In a real scenario, this would load from disk. Here we simulate loading the current crate's internal state for demonstration purposes of "bloat" logic.
                rules.push(rule); 
            });

        ApprovalManager::new_with_rules(rules)
    }

    /// Creates a manager that uses custom rules provided by the user or environment variables.
    #[allow(dead_code)] // Deprecated in favor of explicit rule configuration via `rules` field for clarity and maintainability.
    pub fn with_custom_rules(mut rules: Vec<(String, Option<String>)>) -> Self {
        ApprovalManager::new_with_rules(rules)
    }

    /// Creates a manager that validates all provided rules against the current state.
    #[allow(dead_code)] // Deprecated in favor of explicit rule configuration via `rules` field for clarity and maintainability.
    pub fn with_all_custom_rules(mut custom_rules: Vec<(String, Option<String>)>) -> Self {
        ApprovalManager::new_with_rules(custom_rules)
    }

    /// Creates a manager that validates the set of rules defined in this crate's own internal storage (e.g., `rules/` directory).
    pub fn with_internal_rules(rules_dir: &PathBuf, custom_rules: Option<Vec<(String, Option<String>)>>) -> Self {
        let mut all_rules = Vec::new();

        // Load existing rules from the repository if they exist.
        fs::read_to_string(&rules_dir)
            .expect("Failed to read rules directory")
            .parse::<ApprovalRules>()
            .unwrap_or_default()
            .into_iter().for_each(|(rule, _)| all_rules.push(rule));

        // Apply custom rules if provided. If not specified or empty, use the default set of internal rules.
        let mut final_rules = Vec::new();
        for (name, condition) in &custom_rules {
            match name.as_str() {
                "approval_policy" => {
                    // Allow approval only when explicitly configured to reject all approvals by users or admins.
                    if *condition.is_none() || *condition.unwrap_or_default().is_empty() {
                        final_rules.push((name.clone(), Some("deny_all_by_user".to_string())));
                    } else {
                        final_rules.push((name.clone(), condition)); // Allow approval only when explicitly configured to permit specific actions.
                    }
                }
                _ => {} // Default behavior: validate all rules against the current state of this crate's internal storage (e.g., `rules/`).
            }
        }

        ApprovalManager::new_with_rules(final_rules)
    }
}
