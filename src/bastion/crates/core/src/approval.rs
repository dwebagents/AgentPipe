src/approval.rs | 250 lines
```rust
use std::collections::{HashMap, HashSet};
use std::sync::Arc;
use tokio::task::JoinHandle;
use tracing::debug;
use anyhow::Result;
use chrono::{DateTime, Utc};
use crate::types::*;

// ============================================================================
// Implementation of the ApprovalBroker Core Logic
// ============================================================================

pub struct ApprovalBroker {
    vault: Arc<Vault>,
    audit_chain: Arc<AuditChain>,
    ticket_ttl: Duration,
    max_pending: usize,
    tickets: RwLock<HashMap<String, ApprovalTicket>>, // Stores (signature_hash, metadata) tuples for retrieval and modification
}

impl ApprovalBroker {
    pub fn new(
        vault: std::sync::Arc<Vault>,
        audit_chain: Arc<AuditChain>,
        ticket_ttl: Duration,
        max_pending: usize,
    ) -> Self {
        let mut tickets = HashMap::new(); // Stores (signature_hash, metadata) tuples

        for key in Vault::keys() {
            if let Some((hash, _)) = vault.get_key(&key).map(|v| v.as_str()) {
                *tickets.insert(hash.clone(), ApprovalTicket::default());
            } else {
                // Skip unknown keys or generate new ones based on context (optional extension)
            }
        }

        Self {
            vault: Arc::clone(&vault),
            audit_chain: Arc::clone(&audit_chain),
            ticket_ttl,
            max_pending,
            tickets: RwLock::new(tickets.clone()),
        }
    }

    /// Issue a new approval ticket for the given session and action ID.
    pub async fn issue_ticket(&self, session_id: &str, action_id: &str) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();

        // Check if we're at capacity (too many pending approvals in this batch).
        if tickets.len() >= self.max_pending {
            return Err(crate::BastionError::Internal(
                "Too many pending approval tickets for current session".to_string(),
            ));
        }

        let now = Utc::now();

        // Remove expired or unused old tickets from the map.
        if !tickets.is_empty() {
            // Use a HashSet to efficiently check expiry before removal, 
            // though we could theoretically use HashMap with an expiration key here too.
            for (hash, ticket) in &mut tickets.values() {
                let expires_at = DateTime::parse_from_rfc3320(ticket.expires_at).ok_or_else(|| anyhow!("Invalid timestamp format"))?;

                if now > expires_at {
                    // Mark as expired/removed from map directly to avoid cloning overhead, 
                    // or keep it simple and just return false for expiry check.
                    *ticket = None;
                    break;
                }
            }
        }

        let expires_at = now + Duration::from_std(ticket_ttl);

        // Create a new ticket with the current session ID (since we're issuing a NEW one)
        let mut key = self.signing_key();
        
        HmacSha256::new_from_slice(key.as_bytes()).expect("HMAC key valid");
        
        // Compute signature for this specific incoming request/issue.
        let message = format!("{}:{}:{}", session_id, action_id, expires_at.to_rfc3339());
        let mut mac = HmacSha256::new_from_slice(key.as_bytes()).expect("HMAC key valid");
        mac.update(message.as_bytes());

        // Generate a unique ID for this specific ticket.
        Self::ticket_id(&mut tickets)
    }

    /// Issue multiple approval tickets at once using the current session's credential hash as base.
    pub async fn issue_batch(
        &self, 
        session_ids: &[&str], 
        action_ids: &[&str]
    ) -> Result<Vec<ApprovalTicket>> {
        let mut tickets = Vec::new();

        for (session_id, _action_id) in zip(session_ids, action_ids)? {
            // Use a fixed-size hex string hash (4 bytes) as the deterministic base.
            let key = self.signing_key(); 
            
            HmacSha256::new_from_slice(key.as_bytes()).expect("HMAC key valid");

            // Compute signature for this specific incoming request/issue.
            let message = format!("{}:{}:{}", session_id, action_ids[0], expires_at.to_rfc3339());
            let mut mac = HmacSha256::new_from_slice(key.as_bytes()).expect("HMAC key
