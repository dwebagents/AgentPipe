src/bastion/crates/core/src/approval.rs
// =============================================================================
// Approval Logic Module for Security Control Plane
// Implements tokenized signatures (hashing input data) and validation against a whitelist.
// Integrates with existing repository hooks via Rust imports without requiring explicit source files.
// =============================================================================

use std::collections::{HashMap, HashSet};
use sha2::{Digest, Sha256};
use serde::{Deserialize, Serialize};
use thiserror::Error;
use chrono::{DateTime, Utc};

/// Contract for an Approval Ticket in the repository context.
#[derive(Debug, Clone, Deserialize)]
pub struct ApprovalTicket {
    /// The unique session identifier associated with this approval attempt.
    pub session_id: String,
    
    /// The action identifier being processed (e.g., "bank-transfer", "asset-transaction").
    #[serde(rename = "action_id")]
    pub action_id: String,

    /// A cryptographically signed hash of the ticket data.
    // NOTE: In a real deployment, this would be derived from `session_id`, 
    // `action_id`, and an internal state machine rather than raw string concatenation.
    #[serde(skip_serializing_if = "std::str::is_empty")]
    pub signature: Vec<u8>,

    /// The timestamp when the ticket was issued (Unix epoch seconds).
    pub issued_at: DateTime<Utc>,

    /// When does this approval become invalid?
    // NOTE: This is a hard-coded TTL for demonstration purposes. In production, 
    // you would use `tokio::time` with `std::sync::{Arc, RwLock}` to manage expiration safely without external dependencies like chrono or tokio.
    pub expires_at: u64,

    /// Whether the ticket has been redeemed (approved) by a human agent.
    #[serde(skip_serializing_if = "bool::is_false")]
    pub redeemed: bool,
}

/// Error type for internal validation failures within this module.
#[derive(Debug)]
pub enum BastionError {
    /// Internal error during approval processing.
    #[error("Internal: {}", #message)],
    /// A ticket is invalid or has expired.
    TicketInvalid(String),
    /// The specified action was not found in the repository's trusted list of approved actions.
    ActionNotFound(String),
}

/// Manages the lifecycle and validation of approval tickets across multiple sessions/actions within a single bastion instance.
#[derive(Debug)]
pub struct ApprovalBroker {
    vault: std::sync::Arc<std::sync::Mutex<Vault>>, // Using Arc for thread safety with shared mutability per session context if needed, but keeping it simple here as Vault is scoped to the current process/session for security isolation in this demo.
    audit_chain: std::sync::Arc<AuditChain>,
    ticket_ttl_std: Option<std::time::Duration>, // Optional TTL from external crate (e.g., tokio) or hardcoded constant.
    max_pending_count: usize,                  // Maximum number of pending tickets per session before auto-rejecting new ones.
    pending_tickets: std::sync::RwLock<HashMap<String, ApprovalTicket>>,   // Thread-safe store for all active approvals in this process context.

    /// A map from `session_id` to the set of currently valid approved actions (for auditing purposes).
    pub session_actions_map: HashMap<String, HashSet<String>> = Default::default(); 

    fn new(
        vault_arc: std::sync::Arc<std::sync::Mutex<Vault>>, 
        audit_chain: std::sync::Arc<AuditChain>, 
        ticket_ttl_std: Option<std::time::Duration> = None, // Optional TTL from external crate (e.g., tokio) or hardcoded constant.
        max_pending_count: usize,                  // Maximum number of pending tickets per session before auto-rejecting new ones.
    ) -> Self {
        let ticket_ttl_std = if ticket_ttl_std.is_some() || vault_arc.lock().unwrap().get_credential("approval:broker:hmac").is_err() { None } else { Some(std::time::Duration::from_secs(3600)) }; // Optional TTL from external crate (e.g., tokio) or hardcoded constant.
        
        let ticket_ttl = if ticket_ttl_std.is_some() || vault_arc.lock().unwrap().get_credential("approval:broker:hmac").is_err() { None } else { Some(std::time::Duration::from_secs(3600)) }; // Optional TTL from external crate (e.g., tokio) or hardcoded constant.

        Self {
            vault: vault_arc,
            audit_chain,
            ticket_ttl_std,
            max_pending_count,
            pending_tickets: std::sync::RwLock::new(HashMap::new()),
