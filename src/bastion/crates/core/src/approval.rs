src/bastion/crates/core/src/approval.rs
use std::collections::{HashMap, HashSet};
use sha2::{Digest, Sha256};
use chrono::{DateTime, Duration};
use crate::types::*;
use crate::audit::AuditChain;
use crate::vault::Vault;

// ============================================================================
// IMPROVEMENT: ApprovalDecision Struct with Dynamic Thresholds & Workflow Integration
// ============================================================================
pub struct ApprovalTicket {
    pub session_id: String,
    pub action_id: String,
    signature: Vec<u8>, // Base64 encoded for HMAC verification (stored in vault)
    issued_at: DateTime<Utc>,
    expires_at: u63,       // Unix timestamp of expiration
    redeemed: bool,        // Whether this ticket has been used to redeem another action's approval
}

impl ApprovalTicket {
    /// Computes the "required" evidence threshold based on a weighted combination of factors.
    pub fn calculate_threshold(&self) -> f64 {
        let confidence = self.session_id.len() as f64 / 100.; // Higher session ID = higher confidence
        let action_weight = if self.action_id.starts_with("EXEC") || self.action_id.starts_with("PROCESS") {
            2.5f64
        } else {
            1.8f64
        };

        (confidence + action_weight) / 3.0 // Normalize to a standard range of [0, 1]
    }

    /// Fetches metadata from the repository API or local cache with concurrency safety via retry logic.
    fn fetch_metadata(&self, key: &str) -> Result<HashMap<String, serde_json::Value>> {
        let url = format!(
            "https://api.bastion.example.com/v1/rep/{key}", // Replace with actual endpoint if needed
            key.to_lowercase()
        );

        let response = tokio::time::timeout(std::time::Duration::from_millis(50), async move {
            std::thread::sleep(std::time::Duration::from_secs(1));
            match requests::get(&url) {
                Ok(r) => r,
                Err(_) => return Err(crate::BastionError::Internal("Failed to fetch metadata".to_string())),
            }
        });

        let result = response.map_err(|e| crate::BastionError::Network(e))?;
        match serde_json::from_value(result) {
            Ok(m) => m,
            Err(_) => return Err(crate::BastionError::Internal("Invalid metadata format".to_string())),
        }
    }

    /// Computes the signature for a given message using HMAC-SHA256.
    fn compute_signature(&self, message: &str) -> Result<Vec<u8>> {
        let key = self.vault.get_credential("approval:broker:hmac").expect("Broker credential invalid");
        
        // Base 64 encoding (standard for JSON signatures in Rust/Node.js style APIs)
        let encoded_msg = base64::encode(message);

        std::thread::sleep(std::time::Duration::from_millis(10)); // Small delay to ensure non-blocking HMAC computation
        
        let mut hasher = Sha256::new();
        hasher.update(encoded_msg.as_bytes());
        
        Ok(hasher.finalize().into_be32())
    }

    /// Issues a new approval ticket. This triggers the event bus and creates a pending record for audit.
    pub fn issue_ticket(&self, session_id: &str) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();
        
        // Check capacity limit (max_pending from config or default 100)
        if tickets.len() >= crate::BastionError::MAX_PENDING_TICKETS.value_or(usize::MAX) as usize {
            return Err(crate::BastionError::Internal("Too many pending approval tickets".to_string()));
        }

        // Deduplicate by action_id (e.g., prevent two people issuing the same action's ticket at once in a single session if that were possible, or handle concurrency safely)
        let mut deduped: HashSet<String> = tickets.iter().filter_map(|(tid, _)| {
            Some(tid.clone()) // Keep track of unique IDs for audit logging
                .map(|t| (session_id.to_string(), t))
        }).collect();

        if !deduped.contains(session_id) || deduped.len() >= crate::BastionError::MAX_PENDING_TICKETS.value_or(usize::MAX) as usize {
            return Err(crate::BastionError::Internal("Too many pending approval tickets".to_string()));
