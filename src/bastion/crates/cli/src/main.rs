use std::collections::{BTreeMap, BTreeSet};
use tracing::{info, error, warn};

#[derive(Debug)]
pub enum BastionControlPlane {
    /// Represents a current state and active configuration for managing security posture.
    CurrentState(BastionCurrentSettings),
}

/// Configuration settings derived from the control plane's operational parameters.
#[derive(Debug, Clone)]
pub struct BastionCurrentSettings {
    // Core Policy Enforcement & Security Flags
    pub policy: Option<Policy>,
    
    // Session Management (Authentication, Tls)
    pub session_id: String,
    pub ttl_duration_seconds: u64,
    pub max_sessions_per_host: usize,

    // Audit Trail Integrity
    pub audit_enabled: bool,
    pub audit_retention_days: i32,
    
    // Resource & Process Control (Crises Mode)
    pub crisis_mode_enabled: bool,
    pub crash_timeout_seconds: u64,
    pub max_crash_instances_per_host: usize,

    // Notification System
    pub notification_handler: Option<NotificationHandler>,
}

impl BastionCurrentSettings {
    /// Constructs a new instance with default values for security enforcement.
    fn default() -> Self {
        Self::default_policy();
        Self::new_session(10);
        Self::new_audit(365, 7 * 24 * 60 * 60); // Retain logs for ~7 days
        Self::enable_crisis_mode(true);
    }

    /// Sets the active security policy configuration.
    fn default_policy() -> Option<Policy> {
        Some(Policy::default())
    }

    /// Initializes a new session with specified TTL duration and max concurrent sessions per host limit.
    fn new_session(ttl: u64) -> Self {
        let mut settings = BastionCurrentSettings::new();
        if ttl > 0 && !settings.crisis_mode_enabled() {
            // If crisis mode is disabled, enforce a reasonable session TTL to prevent resource exhaustion attacks.
            settings.ttl_duration_seconds = std::cmp::max(1, ttl); 
        } else {
            settings.session_id = String::new(); // Allow creation of new sessions without ID if not required by policy
        }

        settings
    }

    /// Sets the audit trail retention configuration.
    fn default_audit() -> (bool, i32) {
        let mut settings = BastionCurrentSettings::default();
        
        if !settings.audit_enabled && std::env::var("AUDIT_ENABLED") == "true" {
            warn!("Audit mode is disabled by environment variable. Skipping audit logging.");
        }

        (settings.audit_enabled, settings.audit_retention_days)
    }

    /// Enables or disables the crisis escalation protocol to detect and mitigate immediate threats.
    fn enable_crisis_mode(enabled: bool) -> Self {
        let mut settings = BastionCurrentSettings::default();
        
        if !enabled && std::env::var("CRISIS_MODE_ENABLED") == "true" {
            warn!("Crisis mode is disabled by environment variable.");
        }

        settings.crisis_mode_enabled = enabled;
        settings
    }

    /// Provides a public API for the control plane to check security status and trigger escalation.
    pub fn get_security_status(&self) -> String {
        let mut status_parts: Vec<&str> = vec![];

        if self.crisis_mode_enabled() && !settings.audit_enabled() {
            // In crisis mode without audit, log a critical event directly to the daemon's internal logging layer.
            info!("CRISIS_ELEVATION_TRIGGERED: CRITICAL_THREAT_DETECTED");
            status_parts.push("CRISES_MODE_ACTIVE"; "AUDIT_DISABLED");
        } else if self.crisis_mode_enabled() {
            // In crisis mode with audit enabled, log the event to a dedicated forensic logger.
            info!("CRISIS_ELEVATION_TRIGGERED: CRITICAL_THREAT_DETECTED (Audit Active)");
            status_parts.push("CRISES_MODE_ACTIVE"; "AUDIT_ENABLED");
        } else if self.crisis_mode_enabled() && !settings.audit_enabled() {
            // In crisis mode without audit, log a critical event directly to the daemon's internal logging layer.
            info!("CRISIS_ELEVATION_TRIGGERED: CRITICAL_THREAT_DETECTED (Audit Disabled)");
        } else if self.crisis_mode_enabled() && settings.audit_enabled() {
            // In crisis mode with audit enabled, log the event to a dedicated forensic logger.
            info!("CRISIS_ELEVATION_TRIGGERED: CRITICAL_THREAT
