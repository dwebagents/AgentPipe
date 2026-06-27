use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditEntry {
    pub sequence: u64,
    pub timestamp: DateTime<Utc>,
    pub session_id: String,
    pub event: String,
    pub actor: String,
    pub outcome: String,
    pub metadata: HashMap<String, serde_json::Value>,
    pub prev_hash: [u8; 32],
    pub entry_hash: Option<[u8; 32]>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Credential {
    pub name: String,
    pub value: String,
    pub created_at: DateTime<Utc>,
    pub expires_at: DateTime<Utc>,
    pub version: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionContext {
    pub session_id: String,
    pub created_at: DateTime<Utc>,
    pub expires_at: DateTime<Utc>,
    pub ssh_public_key: String,
    pub metadata: HashMap<String, serde_json::Value>,
    pub is_active: bool,
}

impl SessionContext {
    pub fn is_expired(&self) -> bool {
        chrono::Utc::now() > self.expires_at
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Action {
    pub action_id: String,
    pub session_id: String,
    pub action_type: String,
    pub parameters: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApprovalTicket {
    pub session_id: String,
    pub action_id: String,
    pub signature: Vec<u8>,
    pub issued_at: DateTime<Utc>,
    pub expires_at: DateTime<Utc>,
    pub redeemed: bool,
}

impl AuditEntry {
    pub fn compute_hash(&self, prev_hash: &[u8; 32]) -> [u8; 32] {
        let mut hasher = Sha256::new();
        hasher.update(prev_hash);
        hasher.update(self.sequence.to_le_bytes());
        let payload = serde_json::to_vec(self).expect("audit entry serialization");
        hasher.update(&payload);
        hasher.finalize().into()
    }
}
