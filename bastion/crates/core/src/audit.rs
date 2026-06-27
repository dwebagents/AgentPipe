use parking_lot::RwLock;
use sha2::{Digest, Sha256};
use tracing::{debug, warn};

use crate::types::AuditEntry;
use crate::Result;

#[derive(Debug, Clone)]
pub struct AuditChain {
    entries: std::sync::Arc<RwLock<Vec<AuditEntry>>>,
    genesis: [u8; 32],
}

impl AuditChain {
    pub fn new(genesis_seed: Option<[u8; 32]>) -> Self {
        let genesis = genesis_seed.unwrap_or_else(|| {
            let mut hasher = Sha256::new();
            hasher.update(b"bastion-audit-genesis-v1");
            hasher.finalize().into()
        });
        Self {
            entries: std::sync::Arc::new(RwLock::new(Vec::new())),
            genesis,
        }
    }

    pub fn genesis_hash(&self) -> [u8; 32] {
        self.genesis
    }

    pub fn last_hash(&self) -> [u8; 32] {
        let guard = self.entries.read();
        if guard.is_empty() {
            return self.genesis;
        }
        guard.last().and_then(|e| e.entry_hash).unwrap_or(self.genesis)
    }

    pub fn append(
        &self,
        session_id: String,
        event: String,
        actor: String,
        outcome: String,
        metadata: std::collections::HashMap<String, serde_json::Value>,
    ) -> Result<AuditEntry> {
        let mut guard = self.entries.write();
        let sequence = guard.len() as u64 + 1;
        let prev_hash = if guard.is_empty() {
            self.genesis
        } else {
            guard.last().and_then(|e| e.entry_hash).unwrap_or(self.genesis)
        };
        let timestamp = chrono::Utc::now();
        let mut entry = AuditEntry {
            sequence,
            timestamp,
            session_id,
            event: event.clone(),
            actor,
            outcome,
            metadata,
            prev_hash,
            entry_hash: None,
        };

        let entry_hash = entry.audit_hash(&prev_hash);
        entry.entry_hash = Some(entry_hash);
        guard.push(entry.clone());
        debug!(sequence, event = %event, "audit entry appended");
        Ok(entry)
    }

    pub fn verify(&self) -> bool {
        let guard = self.entries.read();
        let mut expected = self.genesis;
        for entry in guard.iter() {
            if entry.prev_hash != expected {
                warn!("audit chain prev_hash mismatch at sequence {}", entry.sequence);
                return false;
            }
            let computed = entry.audit_hash(&expected);
            if Some(computed) != entry.entry_hash {
                warn!("audit chain entry_hash mismatch at sequence {}", entry.sequence);
                return false;
            }
            expected = entry.entry_hash.unwrap_or(expected);
        }
        true
    }

    pub fn entries(&self) -> Vec<AuditEntry> {
        self.entries.read().clone()
    }

    pub fn len(&self) -> usize {
        self.entries.read().len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.read().is_empty()
    }
}
