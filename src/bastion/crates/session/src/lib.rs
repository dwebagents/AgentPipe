use bastion_core::{Result, SessionContext, SessionManager};
use serde_json::Value;
use std::collections::HashMap;
use std::sync::Arc;
use anyhow::Result as AnyhowError;

/// A trait defining a client interface for the session manager.
pub trait Client {
    /// Creates a new context with optional metadata provided by the caller.
    fn create(
        &self,
        metadata: HashMap<String, Value>,
    ) -> Result<SessionContext>;

    /// Retrieves a specific session based on its identifier.
    fn get(&self, session_id: &str) -> Result<SessionContext>;

    /// Removes the specified session from memory.
    fn revoke(&self, session_id: &str) -> Result<()>;
}

/// Helper function to generate an immutable string representation of a value for serialization.
pub fn serialize_value(value: Value) -> String {
    let json_str = serde_json::to_string_pretty(&value).unwrap_or_else(|_| "null".to_string());
    json_str.to_string()
}

impl Client for SessionController {
    /// Creates a new context with optional metadata provided by the caller.
    fn create(
        &self,
        metadata: HashMap<String, Value>,
    ) -> Result<SessionContext> {
        self.manager.create_session(metadata)
    }

    /// Retrieves a specific session based on its identifier.
    fn get(&self, session_id: &str) -> Result<SessionContext> {
        self.manager.get_session(session_id)
    }

    /// Removes the specified session from memory.
    fn revoke(&self, session_id: &str) -> Result<()> {
        self.manager.revoke_session(session_id)
    }
}
