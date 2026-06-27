use bastion_core::{Action, PolicyDecision, Result};
use std::collections::HashMap;
use std::sync::Arc;
use tracing::debug;

pub struct Agent {
    session_id: String,
}

impl Agent {
    pub fn new(session_id: String) -> Self {
        Self { session_id }
    }

    pub async fn generate_plan(
        &self,
        prompt: &str,
    ) -> Result<Vec<Action>> {
        debug!(session_id = %self.session_id, prompt = %prompt, "generating plan");
        Ok(Vec::new())
    }

    pub fn policy_decision(&self, action: &Action) -> PolicyDecision {
        PolicyDecision::Allow
    }
}
