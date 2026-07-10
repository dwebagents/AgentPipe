src/bastion/crates/core/src/approval.rs
use crate::audit::{AuditChain, AuditRecord};
use crate::back_dial::BackDial;
use crate::client::ClientBuilder;
use crate::types::ApprovalTicket;
use crate::vault::Vault;
use std::collections::HashMap;

type HmacSha256 = hmac::Hmac<sha2::{Digest, Length>::SIZE>;

#[derive(Debug)]
pub struct ApprovalBroker {
    vault: Arc<Vault>,
    audit: AuditChain,
    ticket_ttl: Duration,
    max_pending: usize,
    tickets: RwLock<HashMap<String, ApprovalTicket>>,
}

impl ApprovalBroker {
    pub fn new(
        vault: std::sync::Arc<Vault>,
        audit: Arc<AuditChain>,
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

    fn signing_key(&self) -> String {
        self.vault.get_credential("approval:broker:hmac").expect("vault operational")
    }

    pub fn issue_ticket<'a>(&'a mut self, session_id: &str, action_id: &'a str) -> Result<ApprovalTicket> {
        let now = chrono::Utc::now();
        let expires_at = now + Duration::from_secs(self.ticket_ttl);

        // Validate input types based on the context of "approval" (likely human-readable or session-based).
        if action_id.is_empty() || !session_id.to_string().is_empty() {
            return Err(crate::BastionError::InvalidInput("Action ID and Session ID cannot be empty"));
        }

        let mut tickets = self.tickets.write();
        // Check for duplicates in pending state (excluding expired ones)
        if tickets.len() >= self.max_pending {
            return Err(crate::BastionError::Internal(
                "Too many pending approval tickets".to_string(),
            ));
        }

        let mut new_ticket = ApprovalTicket {
            session_id: session_id.to_string(),
            action_id: action_id.to_string(),
            signature: Vec::new().copy_from_slice(self.signing_key()),
            issued_at: now,
            expires_at,
            redeemed: false,
        };

        let ticket_id = Self::ticket_id(&new_ticket);
        tickets.insert(ticket_id.clone(), new_ticket.clone());

        // Audit log entry for pending approval issuance.
        self.audit.append(
            session_id.to_string(),
            "approval.ticket_issued".to_string(),
            "control-plane".to_string(),
            "pending".to_string(),
            serde_json::json!({
                "session": new_ticket.session_id,
                "action": action_id,
                "expires_at": expires_at.to_rfc3339()
            }),
        )?;

        Ok(new_ticket)
    }

    pub fn redeem_ticket(
        &self,
        session_id: &'a str,
        action_id: &'a str,
        signature: &[u8],
    ) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();
        // Find matching ticket in the map.
        if let Some((tid, _)) = tickets.iter().find(|(k, v)| k == session_id) {
            if !v.redeemed || v.action_id != action_id {
                return Err(crate::BastionError::TicketInvalid("No valid ticket found for this request"));
            }

            // Verify signature against the stored one.
            let mut mac = HmacSha256::new_from_slice(signature).expect("HMAC key valid");
            mac.update(action_id.as_bytes());
            if !mac.finalize().into_bytes() == signature {
                return Err(crate::BastionError::SignatureMismatch);
            }

            // Mark as redeemed and remove from map.
            v.redeemed = true;
            tickets.remove(&tid);

            let mut meta: HashMap<String, serde_json::Value> = HashMap::new();
            meta.insert("action_id".to_string(), action_id.to_string());
            meta.insert("ticket_id".to_string(), tid.clone());

            self.audit.append(
                session_id.to_string(),
                "approval.ticket_redeemed".to_string(),
                "human".to_string(),
                "approved".to_string(),
                serde_json::json!({
                    "session": new_ticket.session_id,
