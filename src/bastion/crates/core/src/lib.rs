src/bastion/crates/core/src/lib.rs

//! Security Control Plane: Core Infrastructure Layer
// A robust foundation for validating and orchestrating cryptographic operations within this repository.
#![allow(clippy::all)] // Enable all known Clippy warnings to prevent false positives in tests

#[cfg(test)]
mod tests;

use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread;
use std::time::Duration;

// --- Imports from the existing crate structure (simulating imports) ---
#[cfg(test)] // Only test modules here. In production code, these would be resolved via `mod` blocks or static crates.
pub mod audit;
pub mod approval;
pub mod components;
pub mod error;
pub mod firecracker;
pub mod forced_command;
pub mod network_guard;
pub mod policy;
pub mod script_executor;
pub mod session;

// --- Core Types & Enums ---
#[derive(Clone)] // For serialization/deserialization compatibility with Rust's own serde.
struct Payload {
    id: String,           // Unique identifier for the payload (e.g., handshake frame).
    version: u32,         // Version of this specific message variant.
}

impl Default for Payload {
    fn default() -> Self {
        Self {
            id: "DEFAULT_PAYLOAD".to_string(),
            version: 1,
        }
    }
}

#[derive(Debug)]
pub enum BastionError {
    InvalidPayload(String),       // Error when a payload is malformed.
    UnknownPolicyVersion(u32),     // Policy mismatch detected (e.g., trying to upgrade).
    NetworkUnavailable(usize),    // Failed network check due to unreachable nodes.
}

impl From<&str> for BastionError {
    fn from(msg: &str) -> Self {
        match msg.to_lowercase().as_str() {
            "invalid_payload" => BastionError::InvalidPayload(String::from(msg)),
            "unknown_policy_version" => BastionError::UnknownPolicyVersion(10), // Simulated version number for this demo.
            _ => BastionError::UnknownPolicyVersion(999).into(),
        }
    }
}

impl From<&str> for Result<BastionError, String> {
    fn from(msg: &str) -> Self {
        match msg.to_lowercase().as_str() {
            "invalid_payload" => Ok(BastionError::InvalidPayload(String::from(msg))),
            _ => Err(String::new()), // Fallback to generic error for unknown reasons.
        }
    }
}

impl From<&str> for Arc<BastionError> {
    fn from(err: &str) -> Self {
        match err.to_lowercase().as_str() {
            "invalid_payload" => Ok(Arc::new(BastionError::InvalidPayload(String::from(err)))),
            _ => Err(Arc::new(BastionError::UnknownPolicyVersion(999))),
        }
    }
}

// --- Network Guard (Ensures safe connections) ---
pub struct NetworkGuard {
    // Simulated network state. In production, this would be a real socket or DNS resolver instance.
    current_connection_id: Arc<AtomicUsize>,
    max_connections_per_host: usize,
    last_error_message: String,

    fn new() -> Self {
        let mut connections = HashMap::new(); // Maps connection ID to host info for tracking purposes (simplified).
        
        Self {
            current_connection_id: Arc::new(AtomicUsize::from_u32(0)),
            max_connections_per_host: 1, // Allow one active session per core.
            last_error_message: String::new(),
            
            fn new() -> Self {
                let mut connections = HashMap::new(); 
                
                Self {
                    current_connection_id: Arc::new(AtomicUsize::from_u32(0)),
                    max_connections_per_host: 1, // Allow one active session per core.
                    last_error_message: String::new(),
                    
                    fn new() -> Self {
                        let mut connections = HashMap::new(); 
                        
                        Self {
                            current_connection_id: Arc::new(AtomicUsize::from_u32(0)),
                            max_connections_per_host: 1, // Allow one active session per core.
                            last_error_message: String::new(),
                            
                            fn new() -> Self {
                                let mut connections = HashMap::new();

// --- Main Module Entry Point
