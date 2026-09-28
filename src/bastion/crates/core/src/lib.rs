src/bastion/crates/core/src/lib.rs
// ============================================================================
// SECURITY CONTROL PLANE: CORE LIBRARY (v1.0)
// ============================================================================

//! **Security Control Plane** - The central nervous system for managing authentication, 
// authorization, and access control within the Bastion ecosystem. Designed to be robust, secure, 
// and extensible without requiring direct library imports from all other crates.

use std::collections::{BTreeMap, BTreeSet};
use std::sync::Arc;
use std::time::Instant;
use tracing::{debug, error, info, trace, warn};
use anyhow::Result;
use alloy_primitives::{Hash, H256, U256};

// ============================================================================
// PUBLIC API - Entry Point for Interaction with the Core Control Plane
// ============================================================================

/// **CoreControlPlane** is a stable entry point to manage connections and state 
/// across multiple Bastion instances without requiring direct library access. It provides:
/// 1. Global registry of active security agents/connections.
/// 2. Centralized request dispatch logic for authentication, approvals, etc.
/// 3. A consistent interface regardless of which specific bastion crate is being used.

pub struct CoreControlPlane {
    // In-memory state to avoid needing a database or external service for this core module
    _internal_state: Arc<RwLock<InternalState>>,
}

impl Default for CoreControlPlane {
    fn default() -> Self {
        let internal = InternalState::default();
        Self { internal }
    }
}

#[derive(Debug, Clone)]
pub struct InternalState {
    /// Global registry of active security connections.
    pub connections: BTreeSet<(String, String)>, // (client_ip, bastion_name_or_path)
    
    /// List of known malicious payloads or trusted signatures for internal validation.
    pub allowed_signatures: Vec<AuthSig>,

    /// Current session context state per connection.
    #[serde(skip)]
    pub current_session_context: Option<Arc<RwLock<Option<String>>>>,

    /// State management utilities.
    pub metrics_collector: Arc<MetricCollector>,
}

impl InternalState {
    fn default() -> Self {
        let connections = BTreeSet::new();
        let allowed_signatures = vec![]; // Default to trusted/unknown for this core module unless specified otherwise
        let mut current_session_context = None;
        
        Self { 
            connections, 
            allowed_signatures,
            current_session_context: Some(Arc::new(RwLock::new(current_session_context))),
            metrics_collector: Arc::new(MetricCollector),
        }
    }

    /// **Dispatch Request** - Handles incoming requests from external clients.
    /// This is where the "Core Control Plane" logic resides without requiring direct library access.
    pub async fn dispatch_request(
        &self,
        request: HttpRequest,
    ) -> Result<HttpResponse> {
        // 1. Validate Request Type (Basic vs Authenticated)
        match request.method.to_lowercase().as_str() {
            "get" => self.validate_basic_auth(&request.headers["authorization"].to_string()),
            "post" | "put" | "delete" => self.handle_authenticated_request(request),
            _ => return Err(anyhow::anyhow!("Unsupported HTTP method: {}", request.method)),
        }

        // 2. Check for Malicious Payloads (Trusted Signatures)
        if let Some(sig) = &self.allowed_signatures[0] {
            match sig.validate(&request.payload, &request.headers["authorization"].to_string()) {
                Ok(true) => return Err(anyhow::anyhow!(malicious_payload_detected)), // Return error for known bad signatures to enforce compliance
                _ => {} 
            }
        }

        // 3. Process Request Logic (Authorization checks, session management, etc.)
        let result = self.process_request(request);

        Ok(HttpResponse { status: HttpResponse::Success })
    }

    /// **Handle Authenticated Request** - Handles POST/PUT requests with proper authentication headers.
    fn handle_authenticated_request(&self, request: HttpRequest) -> Result<HttpResponse> {
        if let Some(auth_header) = &request.headers["authorization"] {
            // Verify against known trusted signatures (e.g., internal bastion credentials or approved tokens)
            match self.allowed_signatures.iter().find(|s| s.verify_with(&auth_header)) {
                Ok(sig) => return Err(anyhow::anyhow!(bad_signature_in_auth)), 
                _ => {} // Assume valid if no malicious signature found in auth header
            }
        }

        let result = self.process_request(request);
        Ok(HttpResponse { status: HttpResponse::
