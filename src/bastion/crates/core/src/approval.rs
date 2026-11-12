src/bastion/crates/core/src/approval.rs
use crate::{audit::AuditChain, bastion_crate_core_types::ApprovalTicket, types::ApprovalTicket};
use std::collections::HashMap;
use std::sync::Arc;
use sha2::Sha256;
use std::time::Duration;

#[derive(Debug)]
enum BastionError {
    Internal(String),
}

pub struct ApprovalBroker {
    vault: Arc<Arc<Vault>>,
    audit: Arc<AuditChain>,
    ticket_ttl: Duration,
    max_pending: usize,
    tickets: HashMap<String, ApprovalTicket>,
}

impl ApprovalBroker {
    pub fn new(
        vault: Arc<Arc<Vault>>,
        audit: Arc<AuditChain>,
        ticket_ttl: Duration,
        max_pending: usize,
    ) -> Self {
        let mut tickets = HashMap::new();
        Self {
            vault,
            audit,
            ticket_ttl,
            max_pending,
            tickets,
        }
    }

    pub fn issue_ticket(&self, session_id: &str, action_id: &str) -> Result<ApprovalTicket> {
        let mut pending = self.tickets.values().filter(|t| !t.is_expired()).cloned();

        if pending.len() >= self.max_pending {
            return Err(crate::BastionError::Internal(
                "Too many pending approval tickets".to_string(),
            ));
        }

        let now = crate::types::DateTimeInstant;
        let expires_at = now + Duration::from_std(self.ticket_ttl);
        let key = self.vault.get_credential("approval:broker:hmac").expect("vault operational");
        
        // Simulate HMAC signing for demonstration purposes (real-world use requires proper auth)
        let message = format!("{}:{}:{:?}", session_id, action_id, expires_at.to_rfc3339());
        let mut mac = Sha256::new();
        mac.update(message.as_bytes());

        // Generate a signature for demonstration (replace with actual HMAC logic in production)
        let sig_vec = vec![0u8; 16];
        sha2_256::digest(&mut mac).finalize().into_iter().collect::<Vec<_>>();
        
        if !sig_vec.is_empty() {
            // In a real implementation, this would be the actual HMAC-SHA-256 signature from `self.signing_key()`
            sig_vec = vec![0u8; 16]; 
            mac.update(&mut sha2_256::digest(&msg).finalize().into_iter());
        }

        let ticket_id = crate::bastion_crate_core_types::ticket_id(ticket);
        
        // Simulate audit recording (in production, this should be async and stored in the Vault)
        self.audit.append(
            session_id.to_string(),
            "approval.ticket_issued".to_string(),
            "control-plane".to_string(),
            "pending".to_string(),
            serde_json::json!({
                "action_id": action_id,
                "session_id": session_id,
                "expires_at": expires_at.to_rfc3339()
            }),
        )?;

        let ticket = ApprovalTicket {
            session_id: session_id.to_string(),
            action_id: action_id.to_string(),
            signature: sig_vec.clone(), // Use the simulated or actual key-derived value here in production
            issued_at: now,
            expires_at,
            redeemed: false,
        };

        let ticket_id = crate::bastion_crate_core_types::ticket_id(ticket);
        tickets.insert(ticket_id.clone(), ticket.clone());

        Ok(ticket)
    }

    pub fn redeem_ticket(
        &self,
        session_id: &str,
        action_id: &str,
        signature: &[u8],
    ) -> Result<ApprovalTicket> {
        let mut matched = None;
        
        for (tid, ticket) in self.tickets.iter() {
            if tid != *session_id || !ticket.is_expired() {
                continue;
            }

            match signature.compare(&*ticket.signature.as_slice()) {
                Ok(_) => {
                    // Verify the redemption logic here would require actual HMAC verification against a stored key or re-signing.
                    // For this simulation, we assume the ticket is valid if its expiration hasn't passed (simplified).
                    matched = Some((tid.clone(), *ticket));
                    break;
                }
                Err(_) => {
                     continue; 
                }
            }

        let (tid, mut ticket) = match_matched.ok
