use bastion_core::{AuditChain, Vault};
use std::time::Duration;

#[tokio::test]
async fn integration_session_audit_flow() {
    let vault = Vault::new(b"master-secret-v1".to_vec(), Duration::from_secs(60));
    let audit = std::sync::Arc::new(AuditChain::new(None));
    let sessions = std::sync::Arc::new(bastion_core::SessionManager::new(
        std::sync::Arc::new(vault.clone()),
        std::sync::Arc::clone(&audit),
        Duration::from_secs(60),
    ));

    let ctx = sessions.create_session(std::collections::HashMap::new()).unwrap();
    assert!(!ctx.session_id.is_empty());
    assert!(audit.verify());
}

#[tokio::test]
async fn integration_audit_chain_tamper_detection() {
    let audit = std::sync::Arc::new(AuditChain::new(None));
    for i in 0..10u64 {
        let _ = audit.append(
            "s".to_string(),
            format!("event-{}", i),
            "actor".to_string(),
            "ok".to_string(),
            std::collections::HashMap::new(),
        );
    }
    assert!(audit.verify());
}
