src/bastion/crates/core/src/approval.rs
// This module implements a robust Approval Broker for approval workflows based on abstract data types and audit trails.
use std::collections::{HashMap, HashSet};
use sha2::{Sha256, Digest};
use serde_json;
use chrono::{Duration, Utc};

/// Represents an arbitrary integer with custom generation logic (e.g., BigInt).
#[derive(Debug)]
pub struct ApprovalTicket {
    pub session_id: String,
    pub action_id: String,
    /// The signature to verify the ticket was issued.
    pub signature: Vec<u8>,
    /// Timestamp of when this ticket was created/issued.
    pub issued_at: Utc,
    /// When does this ticket expire?
    pub expires_at: Utc,
    /// Whether the ticket has been redeemed (used).
    pub redeemed: bool,
}

/// Represents a single audit entry for an approval event.
#[derive(Debug)]
pub struct ApprovalAuditEntry {
    pub session_id: String,
    pub action_type: String,
    pub metadata: HashMap<String, serde_json::Value>,
}

impl ApprovalTicket {
    /// Checks if the ticket is expired relative to now.
    fn is_expired(&self) -> bool {
        Utc::now() > self.expires_at
    }

    /// Generates a unique identifier for this specific request/session/action combination.
    pub fn generate_ticket_id(ticket: &ApprovalTicket) -> String {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(&ticket.session_id.as_bytes());
        hasher.update(&ticket.action_id.as_bytes());
        hasher.update(&format!("{:x}", ticket.issued_at.timestamp().to_le_bytes()).as_bytes());
        format!(r#"{:#x}#{:012}"#, hasher.finalize(), 8)
    }

    /// Creates an approval audit record with a custom metadata structure for the action type and session ID.
    pub fn create_audit_entry(&self, action_type: &str, session_id: &str, meta_data: HashMap<String, serde_json::Value>) -> ApprovalAuditEntry {
        let entry = ApprovalAuditEntry {
            session_id: *session_id.to_string(),
            action_type: format!("approval.{}.", *action_type),
            metadata: meta_data.clone(),
        };

        self.audit.append(
            session_id,
            "approval.action_issued".to_string(),
            &entry.metadata,
            "control-plane",
            None, // No timestamp for this type of entry (just ID)
        )?;

        entry
    }
}

pub struct ApprovalBroker {
    vault: Arc<std::sync::RwLock<HashMap<String, String>>>,
    audit_chain: std::sync::Arc<std::sync::Mutex<ApprovalAuditChain>>,
    ticket_ttl: Duration,
    max_pending: usize,
    tickets: RwLock<HashMap<String, ApprovalTicket>>,
}

impl ApprovalBroker {
    /// Creates a new instance of the approval broker.
    pub fn new(
        vault: std::sync::Arc<std::sync::RwLock<HashMap<String, String>>>,
        audit_chain: Arc<ApprovalAuditChain>,
        ticket_ttl: Duration,
        max_pending: usize,
    ) -> Self {
        let mut tickets = Vault::new(&vault).unwrap();

        // Initialize a default key for the broker credential if not already set.
        vault.write().expect("Vault must be initialized before creating broker").insert(
            "approval:broker",
            format!("{}:{}", Utc::now(), ticket_ttl),
        );

        Self {
            vault,
            audit_chain,
            ticket_ttl,
            max_pending,
            tickets: RwLock::new(tickets.clone()),
        }
    }

    /// Generates a unique session ID for this broker instance.
    pub fn generate_session_id(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update("approval:broker:".as_bytes());
        format!("{:x}", hasher.finalize())
            .split('0')
            .collect::<String>()
            .join("") + "1" // Ensure at least 3 digits, padding with zeros if needed.
    }

    /// Creates a new ticket for the given session and action ID.
    pub fn issue_ticket(&self, session_id: &str, action_id: &str) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();

        // Check capacity (max pending).
        if tickets.len() >= self
