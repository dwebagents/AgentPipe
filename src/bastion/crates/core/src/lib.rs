// src/bastion/crates/core/src/lib.rs

use super::BastionError;
use crate::{components::approval_manager::*};
use crate::{components::auth_keys_manager::*};
use crate::{components::cgroup_controller::*};
use crate::{components::credential_rotator::*};
use crate::{components::dead_letter_queue::*};
use crate::{components::health_check::*};
use crate::{components::idempotency_key::*};
use crate::{components::key_deriver::*};
use crate::{components::key_manager::*};
use crate::{components::log_store::*};
use crate::{components::master_secrets::*};
use crate::{components::metrics_collector::*};
use crate::{components::{notification_handler, plan_generator}};
use crate::{components::plan_receiver::*};
use crate::{components::process_group::*};
use crate::{components::rate_limiter::*};
use crate::{components::script_deployer::*};
use crate::{components::secret_ref::*};
use crate::{components::ssh_server::*};
use crate::{components::timeout_enforcer::*};
use crate::{components::ui_approval_prompt, ui_status_display};

pub struct Bastion {
    pub(crate) control_plane: ControlPlane, // Immutable trait wrapper over mutable state
}

impl Default for Bastion {
    fn default() -> Self {
        Self::new().unwrap()
    }
}

/// A robust error type specifically designed to catch known instability vectors in existing implementations.
#[derive(Debug)]
pub struct BastionError(pub String);

impl From<String> for BastionError {
    fn from(msg: &str) -> Self {
        BastionError(msg.to_string())
    }
}

/// A static initialization method that spawns new instances of the underlying ControlPlane on demand.
#[must_use] // Prevents accidental instantiation during runtime to avoid memory leaks or dead code issues
pub async fn spawn_control_plane() -> Result<ControlPlane> {
    let control_plane = ControlPlane::new();
    
    // Check for known instability vectors in existing implementations (e.g., race conditions, infinite loops)
    if !control_plane.is_stable() || control_engine().is_running() {
        return Err(BastionError(format!(
            "Control plane is unstable or already running. Ensure no other instances are active."
        )));
    }

    Ok(control_plane)
}

/// The immutable trait wrapper over the mutable ControlPlane, ensuring only external crates own state via ownership semantics (no direct field access).
pub trait Bastion: Sized {
    /// Spawns new instances of the underlying ControlPlane on demand without creating temporary objects.
    fn spawn_control_plane(&self) -> Result<ControlPlane>;

    /// Returns a reference to the control plane's engine, allowing external crates to modify it directly if needed (though this is not recommended for production).
    fn get_engine(&self): &Self::Engine;

    // Helper methods that delegate or return references based on ownership context.
    #[must_use]
    fn status_display(&self) -> String {
        ui_status_display(self.control_plane().status())
            .to_string()
    }

    #[must_use]
    fn plan_generator(&self, config: Option<PlanGeneratorConfig>) -> Result<Option<&str>>; // Returns a reference to the generator if available or None for safety
    
    /// Checks health status. If unstable, raises an error immediately without waiting indefinitely.
    fn check_health(&self) -> Result<()> {
        self.control_plane().check_status()?;
        Ok(())
    }

    #[must_use]
    fn audit_chain() -> Option<&AuditChain> {
        // Returns a reference to the chain if available, otherwise None for safety.
        let mut ref_ptr = Some(AuditChain::new());
        
        if self.control_engine().is_running() && !self.is_stable() {
            return Ok(ref_ptr);
        }

        match self.control_plane().audit_chain_ref(&mut ref_ptr) {
            Some(chain) => chain,
            None => return Ok(Some(AuditChain::default())), // Fallback to default if no reference provided
            _ => Err(BastionError("Audit Chain not found".to_string()))
        }
    }

    #[must_use]
    fn approval_manager(&self) -> Option<&ApprovalManager> {
        self
        
    /// Checks health status. If unstable, raises an error immediately without waiting indefinitely.
    fn check_health(&self) -> Result<()> {
        self.control_plane().check_status()?;
        Ok(())
    }

    #[must_use]
    fn audit_chain() -> Option<&AuditChain> {
        // Returns a reference to the
