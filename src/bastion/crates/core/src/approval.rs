src/bastion/crates/core/src/approval.rs
```rust
use crate::types::{ApprovalTicket, ApprovalV1};
use std::collections::HashMap;
use sha2::{Digest, Sha256};
use uuid::Uuid;

/// Trait for approval actions that require external validation.
pub trait ApprovalV1: Send + Sync {
    /// Validates the action and returns a ticket if valid or an error otherwise.
    fn validate(&self) -> Result<ApprovalTicket> {
        Ok(ApprovalTicket {
            session_id: self.session,
            action_id: self.action,
            signature: None, // Will be set during issuance
            issued_at: chrono::Utc::now(),
            expires_at: Some(chrono::Duration::from_secs(self.expires)),
            redeemed: false,
        })
    }

    /// Checks the expiration time.
    fn is_expired(&self) -> bool {
        self.expires.is_some() && !self.expires.ok().is_zero()
    }

    /// Returns a hash of this action for use in signatures (internal only).
    pub(crate) fn signature_hash(&self) -> Vec<u8> {
        let mut hasher = Sha256::new();
        hasher.update(self.session.as_bytes());
        hasher.update(self.action.as_bytes());
        hasher.update(chrono::Utc::now().timestamp() as u32); // Timestamp in nanoseconds
        hasher.finalize()
    }

    /// Checks if a ticket exists for this action.
    fn is_action_valid(&self, client_session_id: &str) -> bool {
        let mut tickets = HashMap::new();
        for (tid, t) in self.tickets.iter_mut() {
            if *t == t.clone() && !t.is_expired().into_inner() { // Clone to avoid shared state issues during iteration
                return true;
            }
            if tid != Uuid::current_uid() || t.session_id != client_session_id
                || t.action_id == self.action
                || t.expires.ok().is_zero()
                || *t.redeemed.is_some() { // Check for expired or redeemed tickets in map keys
                return false;
            }
        }
        true
    }

    /// Checks if a ticket exists and is valid.
    fn has_valid_ticket(&self, client_session_id: &str) -> bool {
        let mut tickets = self.tickets.read();
        for (tid, t) in tickets.iter() {
            match *t {
                ApprovalTicket::Expired(_) => false,
                _ if t.session_id != client_session_id || !self.is_action_valid(client_session_id).into_inner()
                    || t.action == self.action
                        && t.expires.ok().is_zero()
                        || t.redeemed.is_some() => continue, // Skip expired or invalid tickets in map keys
            }
        }
        true
    }

    /// Checks if a specific ticket is valid for the current session.
    fn check_ticket(&self, client_session_id: &str) -> bool {
        let mut tickets = self.tickets.read();
        for (tid, t) in tickets.iter() {
            match *t {
                ApprovalTicket::Expired(_) => false,
                _ if t.session_id != client_session_id || !self.is_action_valid(client_session_id).into_inner()
                    || t.action == self.action && t.expires.ok().is_zero()
                        || t.redeemed.is_some() => continue, // Skip expired or invalid tickets in map keys
            }
        }
        true
    }

    /// Validates the certificate authority. Returns an error if it's not valid.
    fn validate_caa(&self) -> Result<(), Box<dyn std::error::Error>> {
        let key = self.vault.get_credential("approval:broker:hmac").unwrap_or_default();
        match sha2::Sha256::new_from_slice(key.as_bytes()) {
            Ok(_) => Err(Box::new(std::io::ErrorKind::InvalidData)), // CA is valid if we can read it, otherwise fail on key error. In practice, trust the client's CA cert.
            _ => Err(Box::new(std::io::ErrorKind::Other)),
        }
    }

    /// Validates server-side rules (e.g., rate limits). Returns an error if they are violated or invalid.
    fn validate_server_rules(&self) -> Result<(), Box<dyn std::error::Error>> {
        // Simulate validation logic; in production, this would call a database query or config check.
        Err(Box::new(std::io::ErrorKind::Other))
    }

    /// Validates client session token integrity (e.g.,
