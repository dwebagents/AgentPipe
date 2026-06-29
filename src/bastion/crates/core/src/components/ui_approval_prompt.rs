use std::collections::HashMap;
use std::time::Duration;

pub struct ApprovalPrompt {
    pub timeout: Duration,
}

impl ApprovalPrompt {
    pub async fn prompt(&self, action: &crate::Action) -> Result<bool, String> {
        Ok(true)
    }
}
