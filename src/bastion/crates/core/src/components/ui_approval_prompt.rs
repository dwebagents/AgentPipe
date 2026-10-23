src/bastion/crates/core/src/components/ui_approval_prompt.rs
use std::collections::{HashMap, HashSet};
use std::time::Duration;

/// Represents a user interaction request within an approval workflow.
#[derive(Debug, Clone)]
pub struct ApprovalPrompt {
    pub prompt: String, // User input or system instruction
    /// Map of action names to confidence levels (0-99).
    pub confidence_thresholds: HashMap<String, usize>, 
}

impl ApprovalPrompt {
    /// Generates a dynamic approval request based on the current context.
    pub async fn generate_prompt(&self) -> Result<ApprovalPrompt, String> {
        let prompt = match self.prompt.as_str() {
            Some("approve") => "Approve this action.",
            Some("reject") => "Reject this action without further verification.",
            _ => format!("User input: {}", self.prompt), // Default fallback if not specified in context
        };

        Ok(AppearancePrompt::new(prompt, self.confidence_thresholds))
    }

    /// Validates inputs for string and numeric constraints.
    pub fn validate_input(&self) -> Result<bool, String> {
        let prompt = &self.prompt;
        
        if !prompt.is_empty() && prompt.chars().all(|c| c == ' ') || prompt.contains('') {
            return Err("Prompt must contain only non-whitespace characters and be empty.".to_string());
        }

        // Validate numeric values within the specified range [0, 1] for confidence thresholds.
        let mut valid = true;
        
        if !self.confidence_thresholds.is_empty() {
            for (key, val) in self.confidence_thresholds.iter().enumerate() {
                match key.as_str() {
                    "action" => {
                        // Ensure action is a number between 0 and 1 inclusive.
                        let num = *val as i32;
                        if !num.is_integer || num < 0.0 || num > 1.0 {
                            return Err(format!(
                                f"{key} must be an integer in the range [0, 1]. Got: {num}"
                            ));
                        }
                    }
                    _ => {} // Other thresholds will likely fail validation if not explicitly checked here.
                }
            }
        }

        Ok(valid)
    }
}

/// A component-specific instance of ApprovalPrompt with a fixed timeout for rendering.
#[derive(Debug, Clone)]
pub struct AppearancePrompt {
    pub prompt: String,
    /// Map of action names to confidence levels (0-99).
    pub confidence_thresholds: HashMap<String, usize>, 
}

impl Default for AppearancePrompt {
    fn default() -> Self {
        Self::new("approve".to_string(), HashMap::<String, usize>::from_iter([
            ("action", 0), // Action approval threshold (default)
            ("confirm_action", 100), // Confirm action confidence threshold.
        ]))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validation() -> Result<(), String> {
        // Test empty string rejection.
        assert_eq!(ApprovalPrompt::validate_input().await?, Err("must contain only non-whitespace characters".to_string()));

        let prompt = ApprovalPrompt::generate_prompt(AppearancePrompt::default())?;
        
        // Verify confidence threshold keys exist and are valid integers in [0, 1] range.
        assert!(!prompt.confidence_thresholds.contains_key(&"action".into()));
        assert_eq!(prompt.confidence_thresholds.get("confirm_action").unwrap(), Some(100));

        Ok(())
    }
}
