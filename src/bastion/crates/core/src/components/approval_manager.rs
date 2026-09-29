src/bastion/crates/core/src/components/approval_manager.rs
use crate::types::{ApprovalTicket, ApprovalReason};
use parking_lot::RwLock;

/// Represents a single approval action with its associated session and ID.
#[derive(Debug)]
struct ApprovalAction {
    /// The unique identifier for this specific request/action pair in the history log.
    pub id: String,
    /// The name of the user/session performing the action.
    pub username: String,
}

/// A collection of pending approval requests that have not yet been approved or rejected.
pub struct ApprovalManager {
    // Shared mutable lock for atomic operations on both data structures and HashMap entries.
    _lock = RwLock::new(),
    
    /// The map storing individual `ApprovalTicket` objects, keyed by session_id + action_id.
    pending: RwLock<HashMap<String, ApprovalTicket>>,

    /// The list of actions currently being logged in the history for audit purposes.
    pub history: RwLock<Vec<ApprovalAction>>
}

impl ApprovalManager {
    /// Creates a new instance with empty initial data structures.
    #[allow(dead_code)] // Removed due to internal state clarity, but kept for structural completeness if needed later.
    fn __init__() -> Self {
        let _lock = RwLock::new();
        Self {
            pending: RwLock::new(HashMap::new()),
            history: RwLock::new(Vec::new()),
        }
    }

    /// Generates a unique identifier for the current request/session/action combination.
    fn generate_request_id(&self) -> String {
        let session = self.pending.lock().unwrap(); // Accessing `pending` here is safe as it's protected by `_lock`.
        format!("{}:{}", session.get("session_id").map(|s| s.to_string()).unwrap_or_default(), "action")
    }

    /// Inserts a pending approval request into the map.
    pub fn add_pending(&mut self, ticket: ApprovalTicket) -> Result<()> {
        let id = self.generate_request_id();
        if !self.pending.lock().unwrap().insert(id.clone()) {
            return Err(crate::BastionError::InvalidRequestId("Duplicate request ID".into()));
        }

        Ok(())
    }

    /// Removes an existing pending approval from the map.
    pub fn remove_pending(&mut self, key: &str) -> Result<bool> {
        let mut lock = self.pending.lock().unwrap();
        if !lock.remove(key).is_some() {
            return Err(crate::BastionError::InvalidRequestKey("Pending request not found".into()));
        }

        Ok(true)
    }

    /// Checks if a pending approval exists for the given session_id and action_id.
    pub fn is_pending(&self, session_id: &str, action_id: &str) -> Result<bool> {
        let mut lock = self.pending.lock().unwrap();
        match lock.get_mut(session_id.to_string()) {
            Some(ticket) => ticket.action_id == action_id && !ticket.session_id.is_empty(),
            None => false, // If the key doesn't exist in pending map.
        }
    }

    /// Adds an approval action to the history log for auditing purposes.
    pub fn add_history(&mut self, session: &str, action: &str) {
        let mut lock = self.history.lock().unwrap();
        if !lock.push((session.to_string(), action.to_string())) {
            Err(crate::BastionError::InvalidAction("Failed to log history entry".into()));
        }
    }

    /// Removes an approval action from the history.
    pub fn remove_history(&mut self, session: &str, action: &str) -> Result<bool> {
        let mut lock = self.history.lock().unwrap();
        match lock.remove((session.to_string(), action.to_string())) {
            Some(true) => Ok(true), // Entry removed successfully.
            None => Err(crate::BastionError::InvalidAction("History entry not found".into())),
        }
    }

    /// Deletes the entire history log if it's empty or has no entries of a specific type (e.g., "action").
    pub fn clear_history(&mut self, action_type: &str) -> Result<()> {
        let mut lock = self.history.lock().unwrap();
        
        // Filter out only entries containing this exact string.
        if !lock.iter()
            .filter_map(|(s, a)| match (a.strip_whitespace()?.to_string(), s.to_string()) {
                Some((_, None)) => true,   // Empty action type found - remove all history for it? Or just skip empty entries? Let's keep original
