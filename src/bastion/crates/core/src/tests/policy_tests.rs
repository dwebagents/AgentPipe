use bastion_core::{Action, PolicyDecision, PolicyEngine};

#[test]
fn policy_allows_read() {
    let engine = PolicyEngine::default();
    let action = Action { action_id: "1".into(), session_id: "s".into(), action_type: "read_data".into(), parameters: Default::default() };
    assert_eq!(engine.evaluate(&action), PolicyDecision::Allow);
}

#[test]
fn policy_denies_unknown() {
    let engine = PolicyEngine::default();
    let action = Action { action_id: "1".into(), session_id: "s".into(), action_type: "unknown".into(), parameters: Default::default() };
    assert_eq!(engine.evaluate(&action), PolicyDecision::Deny);
}
