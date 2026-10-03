src/bastion/crates/core/src/lib.rs
```rust
//! Bastion Control Plane Core Module: Execution Engine & Security Enforcement Layer
// This module provides a thread-safe executor for executing payloads, enforcing security protocols via state machine validation, and managing external CLI tooling.

use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;
use std::process;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};

/// Configuration for the Bastion Control Plane.
#[derive(Debug)]
pub struct BastionConfig {
    /// The command line arguments to execute (e.g., `--env`, `--policy`).
    pub args: Vec<String>,
    
    /// Environment variables passed in via CLI or environment injection.
    env_vars: BTreeMap<String, String>,

    /// Security thresholds for validation checks.
    security_thresholds: BTreeSet<(&str, u32)>, // (key_name, severity_level)
}

impl BastionConfig {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn with_args(mut self, args: Vec<String>) -> Self {
        if !args.is_empty() && env::var("BASTION_ARGS").is_ok_and(args.contains(&"--env".to_string())) {
            // Check for explicit environment injection flag
            let mut new_env = BTreeMap::new();

            for arg in &self.args {
                match arg.strip_prefix("--") {
                    Some(ref sig) => if !sig.is_empty() && env::var("BASTION_ENV").is_ok_and(sig == "env".to_string()) {
                        new_env.insert(arg.to_string(), args[0].clone());
                    } else {}
                    
                    // Default: pass all arguments as environment variables for security compliance
                    _ => if !args.is_empty() && env::var("BASTION_ENV").is_ok_and(args.len() > 1) {
                        let mut new_env = BTreeMap::new();

                        for arg in &self.args[1..] {
                            match arg.strip_prefix("--") {
                                Some(ref sig) => if !sig.is_empty() && env::var("BASTION_ENV").is_ok_and(sig == "env".to_string()) {
                                    new_env.insert(arg.to_string(), args[0].clone());
                                } else {}

                                // Default: pass all arguments as environment variables for security compliance
                                _ => if !args.is_empty() && env::var("BASTION_ENV").is_ok_and(args.len() > 1) {
                                    new_env.insert(arg.to_string(), args[0].clone());
                                } else {}

                            }
                        }

                        return BastionConfig {
                            security_thresholds: BTreeSet::from_iter(self.security_thresholds.iter().cloned()), // Keep original threshold logic if needed, but we'll handle it here via config struct for simplicity in this snippet to keep code clean and focused on the executor core. 
                            env_vars: new_env.into(),
                        };
                    } else {}

                }
            }
        }

        self
    }
}

/// A thread-safe execution engine that parses command-line arguments, validates security posture via a state machine, and executes payloads safely within a sandboxed context.
pub struct BastionControlPlane {
    /// The current configuration passed to the executor (args/env_vars).
    pub config: BastionConfig,

    /// Thread safety flag for concurrent execution validation checks.
    #[allow(dead_code)] // Deprecated in favor of atomic operations or re-entrant locks if needed later
    _thread_safety_check = AtomicBool::new(false),

    /// The current state machine configuration being validated during execution.
    pub state_machine_config: BTreeMap<String, String>,

    /// Current session context for tracking user actions and permissions.
    #[allow(dead_code)] // Deprecated in favor of atomic operations or re-entrant locks if needed later
    _session_context = AtomicUsize::new(0),

    /// The execution result buffer (empty until successful).
    pub execution_result: Option<String>,

    /// A lock for internal state synchronization during validation.
    #[allow(dead_code)] // Deprecated in favor of atomic operations or re-entrant locks if needed later
    _validation_lock = AtomicUsize::new(0),

    /// The external CLI toolkit to inject into the scope (e.g., `rustc`, `cargo`).
    pub cli_toolkit: Option<String>,

    /// A lock for internal state synchronization during validation.
    #[allow(dead_code)] // Deprecated in favor of atomic operations or
