use bastion_core::{Result, SessionContext};
use std::collections::HashMap;
use tracing::debug;

pub struct WorkspaceClient {}

impl WorkspaceClient {
    pub async fn execute_script(
        &self,
        session: &SessionContext,
        script: &str,
        params: HashMap<String, serde_json::Value>,
    ) -> Result<serde_json::Value> {
        debug!(session_id = %session.session_id, script = %script, "executing script");
        Ok(serde_json::json!({"status": "ok"}))
    }
}
