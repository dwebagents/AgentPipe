src/bastion/crates/core/src/approval.rs
use std::collections::{HashMap, HashSet};
use std::fmt;
use std::time::{Duration, Instant};

use crate::audit::AuditChain;
use crate::types::ApprovalTicket;
use crate::vault::Vault;
use sha2::{Digest, Sha256};
use tokio::sync::RwLock;
use chrono::Utc;

// ============================================================================
// Internal Types and Enums for Approval Logic
// ============================================================================

#[derive(Debug)]
enum TicketState {
    Pending,
    Expired,
}

impl Default for TicketState {
    fn default() -> Self {
        TicketState::Pending
    }
}

/// Represents a single approval ticket with its metadata.
pub struct ApprovalTicket {
    pub session_id: String,
    pub action_id: String,
    /// The timestamp when this specific instance was issued (for deduplication).
    pub issued_at: Instant,
    /// When will this ticket expire?
    pub expires_at: UtcDateTime,
    /// Whether the ticket has been redeemed.
    pub redeemed: bool,
}

#[derive(Debug)]
pub struct ApprovalBroker {
    vault: Arc<Vault>,
    audit: AuditChain,
    // TTL is in seconds for simplicity if not specified otherwise; can be overridden via config or passed as a parameter.
    ticket_ttl: Duration,
    max_pending: usize,
    tickets: RwLock<HashMap<String, ApprovalTicket>>,
}

impl ApprovalBroker {
    /// Creates a new broker with the provided configuration and vault access.
    pub fn new(
        vault: Arc<Vault>,
        audit: AuditChain,
        ticket_ttl: Duration,
        max_pending: usize,
    ) -> Self {
        Self {
            vault,
            audit,
            ticket_ttl,
            max_pending,
            tickets: RwLock::new(HashMap::new()),
        }
    }

    /// Generates a unique ID for the current session.
    fn generate_session_id(&self) -> String {
        format!("session_{std::time::SystemTime::now().duration_since(UtcDateTime::UNIX_EPOCH).as_secs()}", std::env::consts::LIBRARY_NAME.as_str())
            .to_string()
    }

    /// Generates a unique ID for the current action.
    fn generate_action_id(&self) -> String {
        format!("action_{std::time::SystemTime::now().duration_since(UtcDateTime::UNIX_EPOCH).as_secs()}", std::env::consts::LIBRARY_NAME.as_str())
            .to_string()
    }

    /// Checks if the ticket is expired.
    fn check_expired(&self, session_id: &str) -> bool {
        let now = UtcDateTime::from_timestamp(0, 0); // Use current time for comparison (simplified)
        self.tickets.read().get(session_id).cloned()
            .and_then(|t| t.expires_at.is_after(now))
    }

    /// Checks if a specific ticket is expired.
    fn check_expired_for(&self, session_id: &str, action_id: &str) -> bool {
        let now = UtcDateTime::from_timestamp(0, 0); // Use current time for comparison (simplified)
        self.tickets.read().get(session_id).and_then(|t| t.expires_at.is_after(now)) && !self.check_expired_for(&session_id, action_id)
    }

    /// Retrieves pending tickets by session.
    pub fn get_pending_tickets(&self, session_id: &str) -> Vec<ApprovalTicket> {
        let mut result = self.tickets.read().into_iter()
            .filter(|t| t.session_id == session_id && !check_expired_for(self, session_id))
            .cloned();

        // Deduplicate based on the action ID and timestamp to avoid redundant checks in a concurrent setting.
        if let Some(existing) = result.iter_mut().find_map(|ticket| {
                ticket.action_id == &self.generate_action_id() && ticket.session_id == session_id
    }) else {
            return Vec::new();
        };

        // Update the expiration timestamp to match this check (for future TTL updates).
        existing.expires_at = UtcDateTime::from_timestamp(0, 0);

        result.sort_by(|a, b| a.issued_at.cmp(&b.issued_at));
        result.into_iter().collect()
    }

    /// Generates the HMAC signature for an approval action by signing the message body and ticket ID.
    fn generate_signature_for_action(
        &self,
        session_id: String
