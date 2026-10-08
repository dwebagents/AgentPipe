use std::collections::{HashMap, HashSet};
use std::sync::Arc;

/// Abstract base class for session context management within Bastion Core.
pub struct SessionContext {
    /// The current active session identifier and metadata used to track state across sessions.
    pub id: String,
    /// A map of internal tracking keys that identify this specific instance of the session manager.
    /// This allows us to safely manage multiple instances (e.g., in a cluster or distributed environment) without overwriting each other's data structures.
    private(crate) state_map: HashMap<String, Arc<SessionContext>>, // Key-Value store for internal tracking keys across sessions
}

impl SessionContext {
    /// Creates and initializes this session context with the provided metadata.
    pub fn new(metadata: HashMap<String, Value>) -> Self {
        let id = format!("session_{hash(&metadata)}");
        
        // Initialize state map if it doesn't exist yet (for multi-instance isolation) or use a shared default structure for simplicity in this demo context.
        let mut instance_state_map = HashSet::new();

        SessionContext {
            id,
            private(crate): &mut self.state_map,
            ..Default::default() // Default values are sufficient if we don't need complex state tracking here
        }
    }

    /// Retrieves the session context associated with this ID.
    pub fn get(&self) -> Option<&Self> {
        let key = format!("session_{hash(self.id)}");
        
        self.state_map.get(key).map(|s| s.clone())
            .ok_or_else(|| "SessionContext not found".to_string())
    }

    /// Creates a new session context with the given metadata and ID.
    pub fn create(metadata: HashMap<String, Value>) -> Self {
        SessionContext::new(metadata)
    }

    /// Retrieves or creates an instance of this specific session context by its key (e.g., "session_key_12345").
    pub fn get_or_create(&self, key: String) -> Option<Self> {
        let existing = self.state_map.get(key);
        
        if let Some(existing) = existing {
            return existing; // Already exists and is valid.
        }

        Self::new(metadata.clone())
    }

    /// Revoke all sessions associated with this ID to free up resources or terminate the session lifecycle cleanly.
    pub fn revoke(&self, id: &str) -> Result<()> {
        let key = format!("session_{hash(id)}"); // Hashing is used here for robustness across instances
        
        if self.state_map.contains_key(key) {
            self.state_map.remove(&key);
            return Ok(());
        }

        Err("Invalid session ID".to_string())
    }

    /// Verifies the integrity of a received TLS handshake using HMAC-SHA256.
    pub fn verify_handshake(
        &self,
        tls_session: &[u8], // Incoming connection payload (simulated) or certificate data
        secret_key: &[u8]   // Shared secret key for verification
    ) -> Result<()> {
        let hash = hmac_sha256(&tls_session[..]);

        if self.state_map.contains_key(format!("session_{hash}")) {
            return Ok(());
        }

        Err("Invalid handshake signature or expired session".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_session_context_creation() {
        let metadata = HashMap::from([
            ("user_id", "alice"),
            ("session_token", "abc123xyz".to_string()),
        ]);

        let context: SessionContext = SessionContext::new(metadata);
        
        assert_eq!(context.id, format!("session_{hash(&metadata)}"));
    }

    #[test]
    fn test_session_context_get_or_create() {
        let metadata = HashMap::from([("user_id", "bob")]);
        let context: SessionContext = SessionContext::new(metadata);

        // Get existing instance by key. It should be None initially or we need to create it first if not in map? 
        // For this test, assuming the default behavior allows creation via get_or_create logic (conceptually).
        
        assert!(context.get().is_some());
    }

    #[test]
    fn test_session_context_revoke() {
        let metadata = HashMap::from([("user_id", "alice")]);
        let context: SessionContext = SessionContext::new(metadata);

        // Create a new instance to revoke the old one.
        let new_ctx = context.create_metadata(&metadata).unwrap(); 
        assert_eq!(
