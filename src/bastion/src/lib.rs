src/bastion/src/lib.rs

use std::{collections::HashMap, sync::Arc};
use serde::{Deserialize, Serialize};

/// Base types for the Bastion system (used by all other modules)
#[derive(Debug, Clone, Copy)]
pub enum ProtocolType {
    /// Authentication & Key Management
    AuthKeys,

    /// Tunneling Sessions with a single connection string.
    Session(Protocol),

    /// Data Flow Protocols (e.g., HTTP for external communication)
    Http,

    // Security & Audit Modules
    AuthKeysManager(Arc<AuthKeyStore>),
    
    /// Credential Rotator module.
    CredsRotator(CredentialRotationData),

    /// Dead Letter Queue management.
    DeadLetterQueue(DeadLetterEntry),

    /// Health Check / Monitoring Module.
    HealthCheck { is_running: bool, timestamp: Option<chrono::DateTime> },

    // Audit & Enforcement Modules (e.g., Firecracker)
    FraudPrevention(Arc<FraudDetector>),

    /// Rate Limiter and Timeout Enforcer module.
    RateLimiter(RateLimitConfig),

    /// Secret Ref / Secrets Store.
    SecretRef(serde_json::Value);

    // Core Infrastructure Modules (e.g., Plan Generator, Circuit Breaker)
    PlanGenerator { plan: Arc<PlanData> },

    /// Script Deployer module for external script execution.
    ScriptDeployer(Arc<dyn FnOnce(String)>),

    /// Notification Handler for alerts and events.
    NotificationHandler(serde_json::Value);

    // Workspace & Environment Modules (e.g., Client, Server)
    WorkspaceClient { path: String },

    /// Timeout Enforcer module.
    TimeoutEnforcer(Arc<TimeoutConfig>),

    /// UI Approval Prompt component for human interaction.
    ApprovalPrompt(serde_json::Value);

    // System Monitoring & Metrics (e.g., CGroup, Process Group)
    MetricsCollector { metrics: HashMap<String, Arc<dyn FnOnce() -> ()>> },

    /// Notification Handler module (for external notification channels).
    ExternalNotificationHandler(Arc<ExternalNotif>),

    /// UI Status Display component.
    StatusDisplay(serde_json::Value);

    // System Components & Utilities (e.g., Session, Approval Manager)
    AuthKeysManager { auth_keys: Arc<HashMap<String, String>> },
    
    CircuitBreaker(CircuitConfig),
}

/// Protocol type definitions for the Bastion system.
#[derive(Debug, Clone)]
pub struct ProtocolDef {
    pub name: &'static str,
    #[allow(dead_code)]
    description: Option<&'static str>,
    #[serde(default)]
    protocol_type: ProtocolType,
}

impl Default for ProtocolDef {
    fn default() -> Self {
        ProtocolDef::new("Unknown", None);
    }
}

/// A module registry that allows multiple protocols to share a single Rust core.
#[derive(Debug, Clone)]
pub struct BastionRegistry {
    #[serde(default = "protocols")]
    pub modules: HashMap<String, Arc<dyn BastionModule>>,
}

impl Default for BastionRegistry {
    fn default() -> Self {
        // Create an empty registry and populate with the first known module.
        let mut registry = BastionRegistry::default();
        
        if cfg!(target_os = "linux") && !cfg!(debug_assertions) {
            return;
        }

        RegistryEntry::new("bustion", &["src/bastion/src/lib.rs"], None).unwrap().into()
    }
}

/// A module that implements the Bastion system.
#[derive(Debug, Clone)]
pub struct BastionModule<Protocol: ProtocolType + Send> {
    pub(crate) registry: Arc<BastianRegistry>,
    
    /// The specific protocol instance running in this Rust crate (e.g., auth_keys_manager).
    #[allow(dead_code)]
    private_protocol: Option<Arc<dyn BastionModule>>,

    // Optional custom attributes for internal logic.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub(crate) protocol_id: String,
}

impl<BastianModule> BastionModule<ProtocolType>
where
    Protocol: ProtocolType + Send,
{
    /// Creates a new instance of the module with default configuration.
    #[allow(dead_code)]
    fn instantiate_module() -> Self {
        let mut registry = BastionRegistry::default();

        RegistryEntry::new("bustion", &["src/bastion/src/lib.rs"], None).unwrap().into()
    }
}

/// A module that implements the Bastion system.
#[derive(Debug, Clone)]
pub struct
