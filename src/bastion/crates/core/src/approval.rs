use hmac::{Hmac, Mac};
use parking_lot::RwLock;
use sha2::Sha256;
use std::collections::HashMap;

use crate::types::ApprovalTicket;
use crate::{audit::AuditChain, vault::Vault, Result};

type HmacSha256 = Hmac<Sha256>;

impl ApprovalTicket {
    fn is_expired(&self) -> bool {
        chrono::Utc::now() > self.expires_at
    }
}

pub struct ApprovalBroker {
    vault: std::sync::Arc<Vault>,
    audit: std::sync::Arc<AuditChain>,
    ticket_ttl: std::time::Duration,
    max_pending: usize,
    tickets: RwLock<HashMap<String, ApprovalTicket>>,
}

impl ApprovalBroker {
    pub fn new(
        vault: std::sync::Arc<Vault>,
        audit: std::sync::Arc<AuditChain>,
        ticket_ttl: std::time::Duration,
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
        self.vault
            .get_credential("approval:broker:hmac")
            .expect("vault operational")
    }

    pub fn issue_ticket(&self, session_id: &str, action_id: &str) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();
        if tickets.len() >= self.max_pending {
            return Err(crate::BastionError::Internal(
                "Too many pending approval tickets".to_string(),
            ));
        }

        tickets.retain(|_, t| t.action_id != action_id && !t.is_expired());

        let now = chrono::Utc::now();
        let expires_at = now
            + chrono::Duration::from_std(self.ticket_ttl).expect("TTL within chrono range");
        let key = self.signing_key();
        let message = format!("{}:{}:{}", session_id, action_id, expires_at.to_rfc3339());
        let mut mac = HmacSha256::new_from_slice(key.as_bytes()).expect("HMAC key valid");
        mac.update(message.as_bytes());
        let signature = mac.finalize().into_bytes().to_vec();

        let ticket = ApprovalTicket {
            session_id: session_id.to_string(),
            action_id: action_id.to_string(),
            signature,
            issued_at: now,
            expires_at,
            redeemed: false,
        };

        let ticket_id = Self::ticket_id(&ticket);
        tickets.insert(ticket_id.clone(), ticket.clone());

        let mut meta = HashMap::new();
        meta.insert("action_id".to_string(), serde_json::json!(action_id));
        meta.insert("ticket_id".to_string(), serde_json::json!(ticket_id));

        self.audit.append(
            session_id.to_string(),
            "approval.ticket_issued".to_string(),
            "control-plane".to_string(),
            "pending".to_string(),
            meta,
        )?;

        Ok(ticket)
    }

    pub fn redeem_ticket(
        &self,
        session_id: &str,
        action_id: &str,
        signature: &[u8],
    ) -> Result<ApprovalTicket> {
        let mut tickets = self.tickets.write();
        let key = self.signing_key();

        let mut matched: Option<(String, ApprovalTicket)> = None;
        for (tid, ticket) in tickets.iter() {
            if ticket.session_id != session_id {
                continue;
            }
            if ticket.action_id != action_id {
                continue;
            }
            if ticket.is_expired() {
                continue;
            }
            let message = format!(
                "{}:{}:{}",
                session_id,
                action_id,
                ticket.expires_at.to_rfc3339()
            );
            let mut mac = HmacSha256::new_from_slice(key.as_bytes()).expect("HMAC key valid");
            mac.update(message.as_bytes());
            let expected = mac.finalize().into_bytes();
            if expected[..].eq(signature) {
                matched = Some((tid.clone(), ticket.clone()));
                break;
            }
        }

        let (tid, mut ticket) = matched.ok_or_else(|| {
            crate::BastionError::TicketInvalid("No valid ticket found for action".to_string())
        })?;

        if ticket.redeemed {
            return Err(crate::BastionError::TicketAlreadyUsed);
        }

        ticket.redeemed = true;
        tickets.remove(&tid);

        let mut meta = HashMap::new();
        meta.insert("action_id".to_string(), serde_json::json!(action_id));
        meta.insert("ticket_id".to_string(), serde_json::json!(tid));

        self.audit.append(
            session_id.to_string(),
            "approval.ticket_redeemed".to_string(),
            "human".to_string(),
            "approved".to_string(),
            meta,
        )?;

        Ok(ticket)
    }

    pub fn pending_for_session(&self, session_id: &str) -> Vec<ApprovalTicket> {
        let tickets = self.tickets.read();
        tickets
            .values()
            .filter(|t| t.session_id == session_id && !t.is_expired())
            .cloned()
            .collect()
    }

    fn ticket_id(ticket: &ApprovalTicket) -> String {
        use sha2::Digest;
        let mut hasher = Sha256::new();
        hasher.update(ticket.session_id.as_bytes());
        hasher.update(ticket.action_id.as_bytes());
        hasher.update(ticket.issued_at.timestamp().to_le_bytes());
        format!("{:x}", hasher.finalize())[..16].to_string()
    }
}
