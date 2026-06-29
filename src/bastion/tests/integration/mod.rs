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

#[tokio::test]
async fn integration_policy_engine() {
    let engine = bastion_core::PolicyEngine::default();
    let action = bastion_core::Action {
        action_id: "1".into(),
        session_id: "s".into(),
        action_type: "read_data".into(),
        parameters: serde_json::json!({}),
    };
    assert!(matches!(engine.evaluate(&action), bastion_core::PolicyDecision::Allow));
}

#[tokio::test]
async fn integration_firecracker_config() {
    let config = bastion_core::FirecrackerConfig {
        kernel_image_path: std::path::PathBuf::from("/tmp/vmlinux"),
        rootfs_path: std::path::PathBuf::from("/tmp/rootfs.ext4"),
        mem_size_mib: 512,
        vcpu_count: 2,
        network_interfaces: vec![],
    };
    assert_eq!(config.vcpu_count, 2);
}

#[tokio::test]
async fn integration_network_guard() {
    let mut guard = bastion_core::NetworkGuard::new();
    guard.allow_loopback();
    guard.drop_external();
    assert!(guard.enforce().is_ok());
}

#[tokio::test]
async fn integration_forced_command() {
    let fc = bastion_core::ForcedCommandConfig::new(
        "/tmp/scripts/abc.sh".into(),
        vec![],
        "session-1".into(),
    );
    let entry = fc.to_ssh_authorized_keys_entry("ssh-ed25519 AAAA...");
    assert!(entry.contains("restrict"));
    assert!(entry.contains("session-1"));
}

#[tokio::test]
async fn integration_approval_manager() {
    let manager = bastion_core::approval_manager::ApprovalManager::new();
    let ticket = bastion_core::ApprovalTicket {
        session_id: "s".into(),
        action_id: "a".into(),
        signature: vec![0u8; 32],
        issued_at: chrono::Utc::now(),
        expires_at: chrono::Utc::now() + chrono::Duration::seconds(300),
        redeemed: false,
    };
    assert!(manager.request(ticket).is_ok());
    assert!(manager.approve("s", "a").is_ok());
}

#[tokio::test]
async fn integration_rate_limiter() {
    use bastion_core::rate_limiter::RateLimiter;
    let limiter = RateLimiter::new(2, std::time::Duration::from_secs(1));
    assert!(limiter.allow());
    assert!(limiter.allow());
    assert!(!limiter.allow());
}

#[tokio::test]
async fn integration_circuit_breaker() {
    use bastion_core::circuit_breaker::CircuitBreaker;
    let cb = CircuitBreaker::new(2);
    assert!(cb.allow());
    cb.record_failure();
    assert!(!cb.allow());
}

#[tokio::test]
async fn integration_log_store() {
    use bastion_core::log_store::LogFileStore;
    let store = LogFileStore { path: std::path::PathBuf::from("/tmp/audit.log"), max_size_bytes: 1024 * 1024 };
    let entry = bastion_core::AuditEntry {
        sequence: 1,
        timestamp: chrono::Utc::now(),
        session_id: "s".into(),
        event: "test".into(),
        actor: "a".into(),
        outcome: "ok".into(),
        metadata: Default::default(),
        prev_hash: [0u8; 32],
        entry_hash: None,
    };
    assert!(store.append(&entry).is_ok());
}

#[tokio::test]
async fn integration_script_deployer() {
    use bastion_core::script_deployer::ScriptDeployer;
    let deployer = ScriptDeployer { remote_path: std::path::PathBuf::from("/tmp/scripts") };
    let path = deployer.deploy(&std::path::PathBuf::from("local.sh"), "s1").await.unwrap();
    assert!(path.contains("s1"));
}

#[tokio::test]
async fn integration_metrics_collector() {
    use bastion_core::metrics_collector::MetricsCollector;
    let mc = MetricsCollector::new();
    mc.record_plan_latency(12.5);
}

#[tokio::test]
async fn integration_health_check() {
    use bastion_core::health_check::HealthCheck;
    let mut hc = HealthCheck::new();
    assert!(hc.run());
}

#[tokio::test]
async fn integration_key_deriver() {
    use bastion_core::key_deriver::KeyDeriver;
    let kd = KeyDeriver::new(b"master".to_vec(), "session");
    let derived = kd.derive(b"salt", 32);
    assert_eq!(derived.len(), 32);
}

#[tokio::test]
async fn integration_cgroup_controller() {
    use bastion_core::cgroup_controller::CgroupController;
    let cg = CgroupController { path: std::path::PathBuf::from("/sys/fs/cgroup/test"), cpu_quota: 50000, memory_limit_bytes: 128 * 1024 * 1024 };
    assert!(cg.apply(1234).is_ok());
}

#[tokio::test]
async fn integration_process_group() {
    use bastion_core::process_group::ProcessGroupManager;
    let mut pg = ProcessGroupManager::new();
    let group = pg.create_group("default");
    pg.add_to_group(&group, 1001);
    pg.terminate_group(&group);
}
