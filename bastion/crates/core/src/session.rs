use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

use base64::engine::general_purpose;
use base64::Engine;
use parking_lot::RwLock;
use tracing::{debug, warn};
use uuid::Uuid;

use crate::types::SessionContext;
use crate::{audit::AuditChain, vault::Vault, Result};

pub struct SessionManager {
    vault: Arc<Vault>,
    audit: Arc<AuditChain>,
    ttl: Duration,
    sessions: RwLock<HashMap<String, SessionContext>>,
}

impl SessionManager {
    pub fn new(vault: Arc<Vault>, audit: Arc<AuditChain>, ttl: Duration) -> Self {
        Self {
            vault,
            audit,
            ttl,
            sessions: RwLock::new(HashMap::new()),
        }
    }

    pub fn create_session(
        &self,
        metadata: HashMap<String, serde_json::Value>,
    ) -> Result<SessionContext> {
        let session_id = Uuid::new_v4().to_string();
        let now = chrono::Utc::now();
        let expires_at = now
            + chrono::Duration::from_std(self.ttl).expect("TTL within chrono range");

        let ssh_secret = self.vault.get_credential(&format!(
            "session:{}:ssh_priv",
            session_id
        ))?;
        let pub_key = format!(
            "ssh-ed25519 AAAA{}",
            general_purpose::STANDARD.encode(ssh_secret.as_bytes())
        );

        let ctx = SessionContext {
            session_id: session_id.clone(),
            created_at: now,
            expires_at,
            ssh_public_key: pub_key,
            metadata,
            is_active: true,
        };

        self.sessions
            .write()
            .insert(session_id.clone(), ctx.clone());

        self.audit.append(
            session_id.clone(),
            "session.created".to_string(),
            "control-plane".to_string(),
            "success".to_string(),
            HashMap::new(),
        )?;
        debug!(session_id = %session_id, "session created");
        Ok(ctx)
    }

    pub fn get_session(&self, session_id: &str) -> Result<SessionContext> {
        let sessions = self.sessions.read();
        let ctx = sessions.get(session_id).ok_or_else(|| {
            crate::BastionError::SessionExpired(format!("session {} not found", session_id))
        })?;
        if ctx.is_expired() {
            return Err(crate::BastionError::SessionExpired(format!(
                "session {} expired",
                session_id
            )));
        }
        if !ctx.is_active {
            return Err(crate::BastionError::SessionExpired(format!(
                "session {} not active",
                session_id
            )));
        }
        Ok(ctx.clone())
    }

    pub fn revoke_session(&self, session_id: &str) -> Result<()> {
        let mut sessions = self.sessions.write();
        if let Some(ctx) = sessions.get_mut(session_id) {
            ctx.is_active = false;
        }
        self.audit.append(
            session_id.to_string(),
            "session.revoked".to_string(),
            "control-plane".to_string(),
            "success".to_string(),
            HashMap::new(),
        )?;
        Ok(())
    }

    pub fn active_sessions(&self) -> Vec<SessionContext> {
        let sessions = self.sessions.read();
        sessions
            .values()
            .filter(|s| s.is_active && !s.is_expired())
            .cloned()
            .collect()
    }
}
