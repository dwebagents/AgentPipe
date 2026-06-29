#[test]
fn audit_chain_empty_is_valid() {
    let chain = bastion_core::AuditChain::new(None);
    assert!(chain.verify());
}

#[test]
fn audit_chain_append_verify() {
    let chain = bastion_core::AuditChain::new(None);
    let _ = chain.append("s".into(), "e".into(), "a".into(), "ok".into(), Default::default());
    assert!(chain.verify());
}
