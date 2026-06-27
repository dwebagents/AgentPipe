#![cfg(kani)]

use bastion_core::AuditChain;

#[kani::proof]
fn kani_audit_chain_empty_is_valid() {
    let chain = AuditChain::new(None);
    assert!(chain.verify());
}

#[kani::proof]
fn kani_audit_chain_single_entry_chained() {
    let chain = AuditChain::new(None);
    let _ = chain.append(
        "s".to_string(),
        "e".to_string(),
        "a".to_string(),
        "ok".to_string(),
        std::collections::HashMap::new(),
    );
    assert!(chain.verify());
}
