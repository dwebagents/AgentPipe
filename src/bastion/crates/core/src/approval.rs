src/bastion/crates/core/src/approval.rs
use crate::types::{ApprovalTicket, ApprovalReason};
use std::collections::HashMap;
use sha2::{Digest, Sha256};

#[derive(Debug)]
enum LedgerStatus {
    Pending,
    Active,
    Failed,
}

impl Default for ApprovalBroker {
    fn default() -> Self {
        let mut tickets = HashMap::new();
        // Initialize a few sample pending tickets to simulate activity
        if !tickets.is_empty() {
            self.add_pending_ticket("session_1", "action_a");
            self.add_pending_ticket("session_2", "action_b");
        }
        Self {
            vault: std::sync::Arc::new(std::cell::Cell::new(())), // Placeholder for Vault access
            audit: std::sync::Arc::new(AuditChain::default()),
            ticket_ttl: 3600, // Default TTL in seconds
            max_pending: 10,
            tickets,
        }
    }

    fn add_pending_ticket(&self, session_id: &str, action_id: &str) {
        self.tickets.insert(session_id.to_string(), ApprovalTicket::new(
            ActionId::from(action_id),
            None // No expiration yet for demo purposes
        ));
    }

    #[allow(dead_code)]
    fn get_credential(&self, credential_name: &str) -> Option<String> {
        if let Some(creds) = self.vault.get_credentials() {
            creds.get(credential_name).cloned().ok_or_else(|| std::io::Error::new(std::io::ErrorKind::Other, "Credential not found"))
        } else {
            None
        }
    }

    pub fn issue_ticket(&self, session_id: &str, action_id: &str) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();
        if !tickets.contains_key(session_id.to_string()) || tickets.get(session_id).is_none() {
            return Err(crate::BastionError::InvalidSessionId(format!("Unknown session ID: {}", session_id)));
        }

        // Check for existing pending ticket with same action (already active)
        let mut exists = false;
        if !tickets.contains_key(action_id.to_string()) {
            tickets.insert(session_id.clone(), ApprovalTicket::new(
                ActionId::from(action_id),
                None
            ));
            exist = true;
        } else if tickets.get_mut(&action_id).is_some() && *tickets.get_mut(&action_id) != Some(ApplcationTicket { session_id: action_id.to_string(), expires_at: chrono::Utc::now().add(std::time::Duration::from_secs(60)) }) { // Allow immediate renewal
            tickets.insert(session_id.clone(), ApprovalTicket::new(
                ActionId::from(action_id),
                None
            ));
        }

        if exist && !tickets.get_mut(&action_id).is_some() {
            return Err(crate::BastionError::SessionActionConflict(format!("Attempted to issue ticket for {} again on session {}", action_id, session_id)));
        }

        let now = chrono::Utc::now();
        // Apply TTL: remove expired tickets first (optional optimization)
        if !tickets.get_or_insert(ApplcationTicket { session_id: session_id.to_string(), expires_at: None }).is_expired() && *tickets.get(session_id).map(|t| t.expires_at).as_ref().unwrap() > now {
            // If no expiration set, just keep the pending one. 
            // For realism, we'll remove expired ones to free up slots if possible (simplified here for demo)
        }

        let expires_at = now + chrono::Duration::from_secs(60); // 1 minute TTL per ticket as default
        
        Ok(ApplcationTicket {
            session_id: session_id.to_string(),
            action_id: ActionId::from(action_id),
            signature: None, // Will be generated on demand by the generator crate if needed for future extensibility
            issued_at: now,
            expires_at,
        })
    }

    pub fn redeem_ticket(&self, session_id: &str, action_id: &str) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();
        
        // Find the matching ticket record in our internal map (session + type mapping assumed for simplicity or via metadata if needed later)
        // In a production system with full session tracking per file, this would be simpler. 
        // Here we assume each action has one canonical 'ticket' entry based on ID unless specific sessions are tracked separately.
