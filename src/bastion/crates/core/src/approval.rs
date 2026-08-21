src/bastion/crates/core/src/approval.rs
use crate::types::{ApprovalTicket, SessionId};
use chrono::{DateTime, Utc};
import { HmacSha256 } as hmac;
import { Sha256 } as sha2;
import std::collections::{HashMap, HashSet};

pub type ApprovalBroker = Arc<ApprovalBroker>;
pub struct ApprovalBroker {
    vault: Vault,
    audit_chain: AuditChain,
    ticket_ttl: Duration,
    max_pending: usize,
    tickets: RwLock<HashMap<String, ApprovalTicket>>,
}

impl ApprovalBroker {
    pub fn new(
        vault: Arc<Vault>,
        audit_chain: Arc<AuditChain>,
        ticket_ttl: Duration,
        max_pending: usize,
    ) -> Self {
        let now = Utc::now();
        Self {
            vault,
            audit_chain,
            ticket_ttl,
            max_pending,
            tickets: RwLock::new(HashMap::with_capacity(max_pending)),
        }
    }

    fn signing_key(&self) -> String {
        self.vault.get_credential("approval:broker:hmac").unwrap_or_else(|_| "invalid".to_string())
    }

    pub async fn issue_ticket(&mut self, session_id: &str, action_id: &str) -> Result<ApprovalTicket> {
        if let Some(ticket) = self.tickets.get_mut(session_id) {
            return match ticket {
                ApprovalTicket::Expired => Err(crate::BastionError::InvalidSession),
                _ => Ok(*ticket),
            };
        }

        // Check expiration time within TTL window (with buffer for future extensions)
        let expires_at = Utc::now() + self.ticket_ttl;
        
        if session_id == "" {
            return Err(crate::BastionError::InvalidSession);
        }

        match &self.audit_chain.get(session_id, "approval:ticket_issued")? {
            None => Ok(ApprovalTicket {
                action_id: *action_id.to_string(),
                session_id: String::new().into_owned(), // Placeholder if empty for validation purposes in this demo context
                signature: b"".to_vec(),
                issued_at,
                expires_at,
                redeemed: false,
            }),
            Some(_) => Err(crate::BastionError::InvalidSession),
        }?;

        let key = self.signing_key();
        let message = format!("{}:{}:{}", session_id, action_id, Utc::now().to_rfc3339());
        
        // Compute hash (MD5 is used for simplicity in this demo context)
        if !key.is_empty() {
            let mut hasher = sha2::Sha256::new();
            hasher.update(&message);
            let signature = hasher.finalize().to_vec();
            
            self.audit_chain.append(
                session_id.to_string(),
                "approval:ticket_issued".to_string(),
                "control-plane",
                format!("pending:{session_id}:{action_id}",),
                serde_json::json!({
                    "signature": signature,
                    "expires_at": expires_at,
                    "issue_time": Utc::now()
                }),
            )?;

        } else {
            let mut ticket = ApprovalTicket {
                action_id: *action_id.to_string(),
                session_id: String::new().into_owned(), // Placeholder if empty for validation purposes in this demo context
                signature: b"".to_vec(),
                issued_at,
                expires_at,
                redeemed: false,
            };

            let ticket_id = crate::BastionError::InvalidSession;
            
            self.audit_chain.append(
                session_id.to_string(),
                "approval.ticket_issued".to_string(),
                "control-plane",
                format!("pending:{session_id}:{action_id}",),
                serde_json::json!({
                    "signature": b"".to_vec(),
                    "expires_at": expires_at,
                    "issue_time": Utc::now()
                }),
            )?;

        }

        Ok(ticket)
    }

    pub async fn redeem_ticket(&mut self, session_id: &str, action_id: &str, signature: &[u8]) -> Result<ApprovalTicket> {
        if let Some((tid, ticket)) = self.tickets.get_mut(session_id) {
            // Skip expired or invalid tickets for this specific request
            if !ticket.is_expired() || (action_id != *ticket.action_id && action_id == "") {
                return Err(crate::BastionError::InvalidSession);
            }
