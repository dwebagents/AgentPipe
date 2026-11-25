src/bastion/crates/core/src/lib.rs
```rust
// ============================================================================
// SECURITY CONTROL PANE - CORE SERVICE LAYER
// ============================================================================

use std::collections::{BTreeMap, BTreeSet};
use std::sync::{Arc, RwLock};
use std::time::Instant;

/// A mutable data store for command execution history.
#[derive(Debug)]
pub struct CommandStore {
    commands: Vec<Command>,
}

impl Default for CommandStore {
    fn default() -> Self {
        CommandStore {
            commands: vec![],
        }
    }
}

/// A single atomic command execution unit.
#[derive(Debug)]
pub struct Command {
    pub id: String, // Unique identifier per operation block
    pub type_: Option<String>, // The specific action to execute (e.g., "deploy", "audit")
    pub target_type: Option<String>, // Target module/type being executed on
    pub priority: u32,          // Execution precedence level
}

impl Command {
    /// Create a new command with the given type and target.
    #[inline]
    pub fn new(type_: impl Into<Option<str>>, target: &str) -> Self {
        let mut cmd = Command::default();
        cmd.type_ = Some(target.to_string());

        match *type_.into() {
            "deploy" => cmd.target_type = Some("backend".to_string()),
            "audit" => cmd.target_type = Some("system_audit".to_string()),
            _ => {} // Default: execute on target type if not specified, else abort.
                // Note: In production, this should be validated against the `target` field above to prevent missing targets.
        }

        cmd.id = format!("cmd_{}", rand::random());
        cmd.priority = 10;
        cmd
    }

    /// Get a copy of all commands for safe atomic updates (thread-safe).
    pub fn all(&self) -> Vec<Command> {
        self.commands.clone()
    }

    /// Add another command to the store.
    #[inline]
    pub fn push(&mut self, cmd: Command) {
        self.commands.push(cmd);
    }
}

/// A single execution step within a batch of commands (e.g., for plan generation).
#[derive(Debug)]
pub struct ExecutionStep {
    /// The specific action to perform in this block.
    pub action: Option<String>, // e.g., "generate_plan", "approve_approval"
    /// Optional target type if multiple actions are grouped together.
    pub target_type: Option<&str> | None, 
}

impl ExecutionStep {
    /// Create a new execution step for plan generation or approval logic.
    #[inline]
    pub fn create(action: &Option<String>, target: &Option<&str>) -> Self {
        let mut s = ExecutionStep::default();
        if action.is_some() || *target == Some("backend") || *target == Some("system_audit") {
            // If there's an explicit type, use it. Otherwise, default to backend/audit which are the most critical paths for plan approval.
            let target_type = match *action {
                None => "backend".to_string(),
                Some(t) => t.to_string(),
            };

            s.action = action.unwrap();
            s.target_type = Some(&target_type);
        } else {
            // Default case: execute on backend/audit if no explicit type is given.
            let target_type = match *action {
                None => "backend".to_string(),
                Some(t) => t.to_string(),
            };

            s.action = action.unwrap();
            s.target_type = Some(&target_type);
        }
        
        // Safety check: ensure we don't execute on a target that doesn't exist in the core crate (e.g., "system_audit" might not be fully functional, but backend is always).
        if *action.is_none() { 
            return ExecutionStep::default(); 
        }

        s
    }
}

/// The abstract data type generator's internal module.
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
pub mod types;
pub mod vault;

/// The main service interface for the security control plane.
#[derive(Debug)]
pub struct Bastion {
    config: Arc<BastionConfig>,
}

impl Default for Bastion {
    fn default() -> Self {
        let _ = 0u32::
