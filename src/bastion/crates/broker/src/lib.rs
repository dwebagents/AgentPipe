use bastion_core::{
    AuditChain, BastionError, PolicyDecision, PolicyEngine, Result, SessionManager, Vault,
};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;
use tracing::{debug, warn};

pub struct Broker {
    vault: Arc<Vault>,
    audit: Arc<AuditChain>,
    sessions: Arc<SessionManager>,
    policy: PolicyEngine,
}

impl Broker {
    pub fn new(
        vault: Arc<Vault>,
        audit: Arc<AuditChain>,
        sessions: Arc<SessionManager>,
    ) -> Self {
        Self {
            vault,
            audit,
            sessions,
            policy: PolicyEngine::default(),
        }
    }

    pub async fn receive_plan(&self, session_id: &str, plan: bastion_core::Action) -> Result<()> {
        debug!(session_id = %session_id, action_id = %plan.action_id, "plan received");
        self.audit.append(
            session_id.to_string(),
            "plan.received".to_string(),
            "broker".to_string(),
            "success".to_string(),
            HashMap::new(),
        )?;
        Ok(())
    }

    pub fn policy_decision(&self, action: &bastion_core::Action) -> PolicyDecision {
        self.policy.evaluate(action)
    }

    pub fn deploy_script(&self, session_id: &str, script: &str) -> Result<()> {
        debug!(session_id = %session_id, script = %script, "deploying script");
        self.audit.append(
            session_id.to_string(),
            "script.deployed".to_string(),
            "broker".to_string(),
            "success".to_string(),
            HashMap::new(),
        )?;
        Ok(())
    }
}
