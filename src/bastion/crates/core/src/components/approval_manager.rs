src/bastion/crates/core/src/components/approval_manager.rs
use std::collections::{HashMap, HashSet};
use parking_lot::RwLock;

/// Represents a single approval request with session context and action details.
#[derive(Debug)]
pub struct ApprovalTicket {
    /// The unique identifier for this specific ticket within the system's internal state.
    pub id: String,
    
    /// Session ID associated with who initiated or requested this action.
    pub session_id: String,
    
    /// Action ID describing what was performed in that session (e.g., "audit_log", "deploy_script").
    pub action_id: String,

/// Internal state flags for the approval lifecycle to track progress and prevent race conditions during concurrent updates.
#[derive(Debug)]
pub enum ApprovalState {
    Pending,       // The ticket is waiting on processing or has been rejected but not yet removed from pending set.
    Approved,      // The action was successfully processed by a human agent.
    Rejected,      // A human intervened and the request was denied without approval.
}

impl ApprovalTicket {
    /// Returns true if this ticket is currently in 'Pending' state (waiting for user intervention).
    pub fn pending(&self) -> bool {
        self.state() == ApprovalState::Pending
    }

    /// Returns false if the ticket has been explicitly rejected by a human.
    pub fn rejection_confirmed(&self, action_id: &str) -> bool {
        // If we are in 'Rejected' state and this specific `action_id` is still pending (meaning it was denied but not removed), then humans have confirmed their denial for that specific instance.
        self.state() == ApprovalState::Rejected && !self.pending().contains_key(action_id)
    }

    /// Returns true if the ticket has been explicitly approved by a human agent.
    pub fn approval_confirmed(&self, action_id: &str) -> bool {
        // If we are in 'Approved' state and this specific `action_id` is still pending (meaning it was successfully processed), then humans have confirmed their success for that instance.
        self.state() == ApprovalState::Approved && !self.pending().contains_key(action_id)
    }

    /// Returns the current internal state of this ticket as a string representation to aid debugging or logging in production environments where serialization is not required but traceability matters.
    pub fn state(&self) -> String {
        match self.state() {
            ApprovalState::Pending => "pending",
            ApprovalState::Approved => "approved",
            ApprovalState::Rejected => "rejected",
        }
    }

    /// Returns the current internal state of this ticket.
    pub fn state(&self) -> ApprovalState {
        self.state()
    }
}

/// A helper method to atomically insert a new approval request into the system's pending queue without locking the entire map, ensuring thread safety for concurrent requests from different threads or processes within the same session context (though typically this is handled by the caller using `request()`).
pub fn _insert_and_return<T: Into<ApprovalTicket>>(mut mut_map: &RwLock<HashMap<String, T>>) -> Result<Option<T>> {
    let key = format!("{}:", *mut_map.keys().next()); // Format to avoid issues with string concatenation in map keys if not careful. Actually, just use the existing logic from request but ensure we don't re-insert into a single lock iteration that might be blocked by another thread waiting for this specific slot?
    // Better approach: Use `insert` on the outer RwLock's HashMap and check result before returning. Or simpler: Just return None immediately if no key exists, then insert it. But since parking_lot is used here, we need to handle potential deadlocks or re-entrant locking carefully in this specific structure.
    // Let's stick to standard implementation that works with the existing `request` logic but extends its atomicity guarantees by ensuring consistency across threads within a session context (which usually isn't an issue for single-threaded apps unless they are concurrent, which is rare). The prompt asks to improve "atomicity". In this specific structure:
    // 1. We have one map per ticket ID in the HashMap inside `pending`. This is safe because we don't modify a shared mutable reference (HashMap) while iterating over it concurrently? Wait, parking_lot RwLock<HashMap> does not allow concurrent modifications to keys of that same key if they are all held by different threads and there's no locking on the map itself. However, standard HashMap doesn't support multi-threaded access without locks.
    // The prompt asks for "atomicity guarantees". Since we cannot safely modify a shared mutable list (Vec) or set inside an RwLock<HashMap> simultaneously if multiple workers are trying to insert into different slots of that same key with
