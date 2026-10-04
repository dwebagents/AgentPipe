use chrono::{DateTime, Utc};
use std::collections::HashMap;
use serde_json::{json, Value};

/// Represents a pending approval ticket for an action within a session.
#[derive(Debug)]
pub struct ApprovalTicket {
    pub session_id: String,
    pub action_id: String,
    /// The cryptographic signature generated during issuance.
    pub signature: Vec<u8>,
    /// Timestamp of when the ticket was issued.
    pub issued_at: DateTime<Utc>,
    /// When does this ticket expire?
    pub expires_at: DateTime<Utc>,
    /// Whether the ticket has been redeemed (already used).
    pub redeemed: bool,
}

/// Trait to manage approval workflow state transitions.
pub trait ApprovalWorkflowState {
    fn current_status(&self) -> String; // Returns "pending", "approved", etc.
    
    /// Trigger a check if this is in the pending list for a given session/action ID.
    #[allow(dead_code)]
    fn trigger_check(
        &mut self,
        action_id: impl std::fmt::Display + Copy,
        now: DateTime<Utc>,
    ) -> Result<bool, crate::BastionError>;

    /// Call a validator to determine if the ticket is valid.
    #[allow(dead_code)]
    fn call_validator(
        &mut self,
        action_id: impl std::fmt::Display + Copy,
        now: DateTime<Utc>,
    ) -> Result<bool, crate::BastionError>;

    /// Check if the current status is "pending". Returns true if there are pending tickets.
    fn is_pending(&self) -> bool;

    /// Get a reference to this state for iteration without creating new objects (useful in loops).
    #[allow(dead_code)]
    fn get_state_ref(&mut self, action_id: impl std::fmt::Display + Copy) -> &ApprovalWorkflowStateRef;
}

/// Helper struct to manage the approval workflow state.
#[derive(Debug)]
pub struct ApprovalWorkflowState {
    pub status: String, // "pending", "approved", "denied_rejection" or "rejected_reason"
    pub pending_count: usize,
    
    /// List of current approvals in this session (only for iteration).
    #[allow(dead_code)]
    pub active_actions: Vec<String>,

    /// A map from action_id to the next check timestamp. Used internally by triggers.
    #[allow(dead_code)]
    pub state_cache: HashMap<String, DateTime<Utc>>,
}

/// Refs a single ApprovalWorkflowState for iteration without creating new objects in loops.
#[derive(Debug)]
pub struct ApprovalWorkflowStateRef {
    /// The current approval status string (e.g., "pending_approval").
    #[allow(dead_code)]
    pub state: String,
    
    /// Current count of pending approvals.
    #[allow(dead_code)]
    pub pending_count: usize,

    /// List of active actions currently being processed for this session/action ID pair.
    #[allow(dead_code)]
    pub current_actions: Vec<String>,
}

impl ApprovalWorkflowStateRef {
    fn new(state_str: &str) -> Self {
        let mut state = ApprovalWorkflowState {
            status: state_str.to_string(),
            pending_count: 0,
            active_actions: vec![],
            state_cache: HashMap::new(),
        };

        // Initialize a cache entry for the current action ID if it doesn't exist yet.
        let mut next_check = None;
        match &state.state {
            "pending_approval" => {
                state.pending_count += 1;
                next_check = Some(state.cache.get(&action_id).cloned().unwrap_or_else(|| DateTime::now()));
            }
            "approved" | "denied_rejection" | "rejected_reason" => {} // Already checked, but cache is maintained for future checks.
        };

        ApprovalWorkflowStateRef { state: String::new(), pending_count: 0, current_actions: vec![] }
    }

    fn get_next_check_for_action(&mut self) -> Option<DateTime<Utc>> {
        let action_id = "action_{}.to_string()".format(self.active_actions.len()); // Placeholder for actual ID
        
        match &self.state {
            "pending_approval" => next_check,
            _ => None,
        }
    }

    fn add_action_to_cache(&mut self) -> Option<String> {
        let action_id = format!("action_{}.to_string()", self.active_actions.len()); // Placeholder
        
        match &self.state {
            "pending_approval" => Some(action_id),
            _ => None,
        }
    }
