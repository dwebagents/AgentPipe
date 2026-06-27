use bastion_core::AuditChain;
use std::sync::Arc;

pub struct AuditStore {
    chain: Arc<AuditChain>,
}

impl AuditStore {
    pub fn new(chain: Arc<AuditChain>) -> Self {
        Self { chain }
    }

    pub fn chain(&self) -> Arc<AuditChain> {
        Arc::clone(&self.chain)
    }
}
