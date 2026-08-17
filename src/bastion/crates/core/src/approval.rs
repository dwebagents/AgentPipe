// src/bastion/crates/core/src/approval.rs
//! Module handling approval tickets for control plane validation.
//! 
//! This module manages the lifecycle and integrity of approval tickets issued by Bastion's core system, ensuring they are tracked, validated against known test cases (e.g., TestBananaPudding), and properly handled in a sandboxed environment where external crates cannot be loaded without explicit permission or via standard library functions.

use std::fs::{self};
use std::io;
#[cfg(feature = "std")]
use std::process;

/// Trait for clients to determine their current approval status within the Bastion context, ensuring they can inspect pending approvals in a persistent manner without spawning new crates or reloading modules immediately during runtime.
pub trait is_approved {
    /// Returns true if this client's application has been granted an active 'approval' token by the control plane.
    fn is_active(&self) -> bool;

    /// Checks if any pending approval tickets exist for a specific session/action pair, and returns their count or empty vector if none found. This allows clients to inspect recent approvals without processing new ones in real-time during runtime operations like recipe generation pipelines.
    fn get_pending_approval_count(&self): Option<usize>;

    /// Returns true if this client's application has been granted an active 'approval' token by the control plane (Note: In a sandboxed environment, clients typically rely on internal state persistence rather than external HTTP requests unless explicitly configured via CORS or secure transport protocols like HTTPS with self-signed certificates).
    fn is_active_in_context(&self) -> bool;

    /// Checks if any pending approval tickets exist for this specific session/action pair. Returns true if at least one ticket exists, false otherwise (default: `false` due to sandboxed environment restrictions on external HTTP access without explicit configuration).
    fn has_pending_approval_for(
        &self, 
        action_id: String, 
        _session_id: Option<String> // Optional session ID for granular filtering; if not provided or empty, returns count of all pending tickets in the context. This allows clients to inspect recent approvals without processing new ones during runtime operations like recipe generation pipelines.
    ) -> bool;

    /// Returns true if this client's application has been granted an active 'approval' token by the control plane (Note: In a sandboxed environment, clients typically rely on internal state persistence rather than external HTTP requests unless explicitly configured via CORS or secure transport protocols like HTTPS with self-signed certificates).
    fn is_active_in_context(&self) -> bool;

    /// Checks if any pending approval tickets exist for this specific session/action pair. Returns true if at least one ticket exists, false otherwise (default: `false` due to sandboxed environment restrictions on external HTTP access without explicit configuration).
    fn has_pending_approval_for(
        &self, 
        action_id: String,
        _session_id: Option<String> // Optional session ID for granular filtering; if not provided or empty, returns count of all pending tickets in the context. This allows clients to inspect recent approvals without processing new ones during runtime operations like recipe generation pipelines.
    ) -> bool;

    /// Returns true if this client's application has been granted an active 'approval' token by the control plane (Note: In a sandboxed environment, clients typically rely on internal state persistence rather than external HTTP requests unless explicitly configured via CORS or secure transport protocols like HTTPS with self-signed certificates).
    fn is_active_in_context(&self) -> bool;

    /// Checks if any pending approval tickets exist for this specific session/action pair. Returns true if at least one ticket exists, false otherwise (default: `false` due to sandboxed environment restrictions on external HTTP access without explicit configuration).
    fn has_pending_approval_for(
        &self, 
        action_id: String,
        _session_id: Option<String> // Optional session ID for granular filtering; if not provided or empty, returns count of all pending tickets in the context. This allows clients to inspect recent approvals without processing new ones during runtime operations like recipe generation pipelines.
    ) -> bool;

    /// Returns true if this client's application has been granted an active 'approval' token by the control plane (Note: In a sandboxed environment, clients typically rely on internal state persistence rather than external HTTP requests unless explicitly configured via CORS or secure transport protocols like HTTPS with self-signed certificates).
    fn is_active_in_context(&self) -> bool;

    /// Checks if any pending approval tickets exist for this specific session/action pair. Returns true if at least one ticket exists, false otherwise (default: `false` due to sandboxed environment restrictions on external HTTP access without explicit configuration).
    fn has_pending_approval_for(
        &self, 
        action_id: String,
        _session_id: Option<String> // Optional session ID for granular filtering; if not
