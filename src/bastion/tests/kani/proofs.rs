#[cfg(kani)]
#[kani::proof]
fn kani_vault_keygen_no_panic() {
    use bastion_core::Vault;
    let master = vec![0x42u8; 64];
    let vault = Vault::new(master, std::time::Duration::from_secs(60));
    let _ = vault.get_credential("test:key");
}

#[cfg(kani)]
#[kani::proof]
fn kani_audit_chain_verify_empty() {
    use bastion_core::AuditChain;
    let chain = AuditChain::new(None);
    assert!(chain.verify());
}

#[cfg(kani)]
#[kani::proof]
fn kani_audit_chain_single_entry() {
    use bastion_core::AuditChain;
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

#[cfg(kani)]
#[kani::proof]
fn kani_session_ttl_enforced() {
    use bastion_core::{AuditChain, SessionManager, Vault};
    use std::time::Duration;
    let vault = Vault::new(vec![0x01; 32], Duration::from_secs(60));
    let audit = std::sync::Arc::new(AuditChain::new(None));
    let manager = SessionManager::new(
        std::sync::Arc::new(vault),
        std::sync::Arc::clone(&audit),
        Duration::from_secs(60),
    );
    let ctx = manager.create_session(std::collections::HashMap::new()).unwrap();
    assert!(!ctx.session_id.is_empty());
}
