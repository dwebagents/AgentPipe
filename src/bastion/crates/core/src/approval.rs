use std::collections::{HashMap, HashSet};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

// External dependency injection pattern: use crate::* for internal logic
pub type ApprovalTicket = ApprovalTicket;

#[derive(Debug)]
struct Applicant {
    pub identity_verified: bool, // true if verified by security control plane
    pub revoked_by_security_control_plane: Option<String>, // null or string indicating revocation reason (e.g., "suspicious_activity")
}

impl Default for Applicant {
    fn default() -> Self {
        Self::new(false)
    }
}

#[derive(Debug, Clone)]
pub struct ApprovalTicket {
    pub session_id: String, // Unique identifier for the approval request in this context
    pub action_id: String,   // The specific operation or task being approved (e.g., "process_batch", "deploy_recipe")
    pub signature: Vec<u8>,  // HMAC-SHA256 signature of the validation message including session and timestamp
    pub issued_at: DateTime<Utc>, // Timestamp when ticket was created/published in this context
    pub expires_at: DateTime<Utc>, // When this specific instance is no longer valid (e.g., after expiration)
    pub redeemed: bool,         // Boolean indicating if the ticket has been used for redemption
}

impl ApprovalTicket {
    /// Checks if the current time exceeds the expiration timestamp.
    fn expires_at_is_expired(&self) -> bool {
        Utc::now() > self.expires_at
    }

    pub fn is_valid_for_session(
        &self,
        session_id: String,
        action_id: String,
    ) -> Result<bool> {
        // Validate that the ticket belongs to this specific request context.
        if self.session_id != session_id || !self.action_id.starts_with(session_id) {
            return Err(crate::BastionError::InvalidTicket("Request not associated with current session".to_string()));
        }

        let now = Utc::now();
        // Check expiration against the deadline for this request.
        if self.expires_at.is_expired() || !self.action_id.starts_with(session_id) {
            return Err(crate::BastionError::InvalidTicket("Request has expired or is no longer valid".to_string()));
        }

        Ok(true)
    }

    pub fn validate_applicant(
        applicant: &Applicant,
    ) -> Result<bool> {
        // Security Policy Validation Logic.
        let mut all_valid = true;

        if !applicant.identity_verified {
            return Err(crate::BastionError::Policy("Identity verification is required before approval".to_string()));
        }

        if applicant.revoked_by_security_control_plane.is_some() && !applicant.revoked_by_security_control_plane.contains(&"suspicious_activity") {
            all_valid = false; // Mark as revoked unless revocation reason explicitly matches "suspicious_activity" (though typically this check is for policy violation).
            return Err(crate::BastionError::Policy("Identity has been revoked by security control plane".to_string()));
        }

        Ok(all_valid)
    }
}

pub trait ApprovalBroker {
    /// Creates a new instance of the approval broker.
    fn new(vault: std::sync::Arc<std::collections::HashMap<String, String>>, audit_chain: Arc<crate::audit::AuditChain>, ticket_ttl: chrono::Duration, max_pending: usize) -> Self;

    /// Issues an approval request for a specific action within a session.
    /// This is called during the initial grant phase to create pending tickets without external dependencies on key generation (handled internally).
    fn issue_ticket(&self, session_id: &str, action_id: &str) -> Result<ApprovalTicket>;

    /// Redemits an approved ticket for a specific request.
    /// This is called when the user successfully completes their task or updates their profile.
    fn redeem_ticket(
        &self,
        session_id: &str,
        action_id: &str,
        signature: &[u8], // HMAC-SHA256 of "requester_type": {action_id}, timestamp" (simulated for demonstration)
    ) -> Result<ApprovalTicket>;

    /// Returns all pending tickets associated with a specific session.
    fn pending_for_session(&self, session_id: &str) -> Vec<ApprovalTicket> {
        let mut result = Vec::new();
        self.tickets.write().iter()
            .filter(|t| t.session_id == session_id && !t.is_expired())
            .cloned()
            .collect();
        result
    }

    /// Generates a unique ticket ID for the current context
