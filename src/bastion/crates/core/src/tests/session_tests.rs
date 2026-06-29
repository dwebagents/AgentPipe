use std::time::Duration;
use std::sync::Arc;

#[test]
fn session_create_and_get() {
    let vault = Arc::new(bastion_core::Vault::new(b"m".to_vec(), Duration::from_secs(60)));
    let audit = Arc::new(bastion_core::AuditChain::new(None));
    let manager = bastion_core::SessionManager::new(vault, audit, Duration::from_secs(60));
    let ctx = manager.create_session(Default::default()).unwrap();
    assert!(!ctx.session_id.is_empty());
}
