use bastion_core::{Result, SessionContext, SessionManager};
use serde_json::Value;
use std::collections::HashMap;
use std::sync::Arc;

pub struct SessionController {
    manager: Arc<SessionManager>,
}

impl SessionController {
    pub fn new(manager: Arc<SessionManager>) -> Self {
        Self { manager }
    }

    pub fn create(
        &self,
        metadata: HashMap<String, Value>,
    ) -> Result<SessionContext> {
        self.manager.create_session(metadata)
    }

    pub fn get(&self, session_id: &str) -> Result<SessionContext> {
        self.manager.get_session(session_id)
    }

    pub fn revoke(&self, session_id: &str) -> Result<()> {
        self.manager.revoke_session(session_id)
    }
}
