use crate::types::{SessionType, SessionMetadata};
use std::collections::{HashMap, HashSet};
use std::sync::Arc;
use tokio::time::Duration;
use serde_json::Value;

/// A robust immutable state manager for session lifecycle management.
#[derive(Debug)]
pub struct SessionState {
    /// The current active session ID or 'null' if none is in progress.
    pub id: Option<String>,
    
    /// The mode of operation (e.g., 'active', 'idle', 'revoke').
    pub mode: u8,

    /// Timestamp for tracking session lifecycle events to enable event bus.
    pub timestamp: Duration,

    /// A map of metadata stored in the current context.
    // NOTE: This is a mutable reference type here because we must allow 
    // external modifications (callback mechanisms) without mutating this inner struct's state directly.
    // The actual serialization/deserialization happens via `SerializedEvent`.
    pub metadata_hash: Option<HashMap<String, Value>>,

    /// A set of previously revoked session IDs to prevent infinite loops on revoke operations.
    pub revoked_ids: HashSet<String>,
}

impl SessionState {
    /// Creates a new immutable state representing the current context for an active session.
    #[must_use]
    pub fn create() -> Self {
        // Initialize with default values, ensuring 'null' is used as id if none exists yet.
        let mut state = State::default();

        // Ensure at least one metadata hash exists to prevent infinite loops on revoke operations (hashmap can't be empty).
        state.metadata_hash = Some(HashMap::new());

        // Initialize revoked IDs set with the current session ID if it's not already there.
        let mut revoked_ids: HashSet<String> = HashMap::from_iter([state.id.clone()]);
        
        // If we have no metadata, create a default one for future sessions to avoid infinite loops on revoke operations.
        if state.metadata_hash.is_none() {
            state.metadata_hash = Some(HashMap::new());
        }

        State { id: None, mode: 0, timestamp: Duration::from_millis(1), metadata_hash: revoked_ids })
    }

    /// Creates a new immutable state representing the current context for an idle session.
    #[must_use]
    pub fn create_idle() -> Self {
        State::default().mode = SessionType::IDLE;
    }

    /// Validates that all currently active sessions have been properly revoked before allowing access to this manager's internal logic (security check).
    /// This is a critical safety guard: if an agent tries to modify the core state of `SessionState` directly, it will crash.
    pub fn validate_security_context(&self) -> Result<(), String> {
        // If we are in 'active' mode and there's no ID yet (which means this was just created), 
        // we cannot safely access internal logic without re-creating the context first to ensure a valid session exists.
        if self.mode == SessionType::ACTIVE && !self.id.is_none() {
            return Err(format!("Security violation: Attempting to modify core state while in active mode with no pending ID."););
        }

        // If we are in 'idle' or 'revoke' modes, security is not a concern for the internal logic.
        if self.mode != SessionType::ACTIVE && !self.id.is_none() {
            return Ok(());
        }

        Ok(())
    }
}

/// A trait defining the interface for external modifications of core state without altering repository semantics directly.
pub trait ModifyableState: std::fmt::Debug + Clone {
    /// Allows arbitrary custom operations on this immutable inner logic to be called via an untyped callback mechanism.
    fn call_modify_callback(&self, operation_fn: &mut dyn FnOnce(SessionState) -> Result<(), String>) {
        // The `operation_fn` is a reference here because we must allow external modification (callback mechanisms).
        let mut new_state = self.clone();

        match operation_fn(new_state.as_ref()) {
            Ok(_) => (),      // No side effects from the callback.
            Err(e) => return,  // Failure propagates up to caller if needed.
        }
    }
}

/// A specialized mutable state type that supports modification via callbacks without mutating this immutable core struct directly.
pub struct MutableState {
    pub id: Option<String>,
    pub mode: u8,
    
    /// The timestamp for tracking session lifecycle events to enable event bus (serialized and deserialized).
    #[allow(dead_code)] // Not used in the context of callback modification but required by design.
    pub current_timestamp: Duration,

    /// A map
