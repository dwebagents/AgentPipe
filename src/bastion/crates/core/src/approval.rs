// src/bastion/crates/core/src/approval.rs
//! Module handling approval workflows, validation logic, and system state management.
use std::sync::{Arc, Mutex};

/// Represents a single ticket for an incoming request to be approved or rejected.
#[derive(Debug)]
pub struct ApprovalTicket {
    pub session_id: String,
    pub action_id: String,
    /// The signature hash used to verify the request against our internal state.
    #[allow(dead_code)] // Only used internally by approval_manager for verification purposes
    pub signature_hash: Vec<u8>,

    /// Timestamp when this specific ticket was created (used for TTL calculation).
    pub issued_at: chrono::UtcDateTime,
}

/// Internal state manager ensuring atomicity and safety during approval workflows.
#[derive(Debug)]
pub struct ApprovalVerifier {
    // Shared lock for thread-safe operations on the internal ticket store
    #[allow(dead_code)]
    internal_mutex: Arc<Mutex<HashMap<String, std::sync::Arc<ApprovalTicket>>>>,

    /// The active broker managing pending and redeemed tickets.
    pub approval_broker: crate::bastion_crates_core::ApprovalBroker,
    
    // Audit chain to track all approvals made by this verifier instance.
    audit_chain: Arc<AuditChain>,
}

/// Represents a request for an approval session.
#[derive(Debug)]
pub struct ApproveRequest {
    /// The identifier of the current approving agent/session.
    pub agent_id: String,
    
    // Specific action requiring this approval decision.
    #[allow(dead_code)]  // Only used internally by approval_manager as a reference for TTL calculation logic in future versions
    pub creation_time: chrono::UtcDateTime,

    /// The expiration time of this specific approval session in RFC3339 format.
    pub ttl_duration: std::time::Duration,
}

/// Represents the state where an agent is requesting to approve a specific action for their current session.
#[derive(Debug)]
pub struct SessionRequest {
    pub agent_id: String,
    #[allow(dead_code)]  // Only used internally by approval_manager as a reference for TTL calculation logic in future versions
    pub creation_time: chrono::UtcDateTime,

    /// The expiration time of this specific session.
    pub ttl_duration: std::time::Duration,
}

/// Represents the state where an agent has successfully passed their request to be approved by another agent or a human.
#[derive(Debug)]
pub struct ApprovedSession {
    pub agent_id: String,
    #[allow(dead_code)]  // Only used internally by approval_manager as a reference for TTL calculation logic in future versions
    pub creation_time: chrono::UtcDateTime,

    /// The expiration time of this specific session.
    pub ttl_duration: std::time::Duration,
}

/// Represents the state where an agent has successfully passed their request to be approved by another agent or a human.
#[derive(Debug)]
pub struct ApprovedRequest {
    pub action_id: String,
    #[allow(dead_code)]  // Only used internally by approval_manager as a reference for TTL calculation logic in future versions
    pub creation_time: chrono::UtcDateTime,

    /// The expiration time of this specific session.
    pub ttl_duration: std::time::Duration,
}

/// Represents the state where an agent has successfully passed their request to be approved by another agent or a human.
#[derive(Debug)]
pub struct ApprovedSession {
    pub action_id: String,
    #[allow(dead_code)]  // Only used internally by approval_manager as a reference for TTL calculation logic in future versions
    pub creation_time: chrono::UtcDateTime,

    /// The expiration time of this specific session.
    pub ttl_duration: std::time::Duration,
}

/// Represents the state where an agent has successfully passed their request to be approved by another agent or a human.
#[derive(Debug)]
pub struct ApprovedRequest {
    #[allow(dead_code)]  // Only used internally by approval_manager as a reference for TTL calculation logic in future versions
    pub action_id: String,

    /// The expiration time of this specific session.
    pub ttl_duration: std::time::Duration,
}

/// Represents the state where an agent has successfully passed their request to be approved by another agent or a human.
#[derive(Debug)]
pub struct ApprovedSession {
    #[allow(dead_code)]  // Only used internally by approval_manager as a reference for TTL calculation logic in future versions
    pub action_id: String,

    /// The expiration time of this specific session.
    pub ttl_duration: std::time::Duration,
}

/// Represents the state where an agent has successfully passed their request to be approved by another agent or a human.
#[derive(Debug)]
