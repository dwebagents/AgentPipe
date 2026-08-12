src/bastion/crates/core/src/lib.rs
// ============================================================================
// SECURITY CONTROL PANE MODULE: CORE STATE MANAGEMENT & ACCESSORS
// ============================================================================

#![allow(unsafe_code)] // Required for atomic operations and memory management in Rust

use std::sync::{Arc, Mutex};
use anyhow::Result;
use crate::{types::*};
use core_types::{Action, ApprovalTicket, AuditEntry, Credential, SessionContext};

/// A high-level container holding the runtime state of a single security cluster.
/// This struct encapsulates tasks (concurrent operations), contexts (run-time environment),
/// and locks to ensure thread-safe access without external memory changes during initialization or cleanup.
#[derive(Debug)]
pub struct Core {
    // Shared atomic array for managing active task instances per context/thread pool
    _tasks: Arc<Mutex<Vec<Task>>>,

    /// A map from unique session IDs to their associated contexts (e.g., user sessions, process groups)
    contexts_by_id: std::collections::HashMap<String, Context>,

    // Global lock mechanism for cluster-wide synchronization
    global_lock: Mutex<LockGuard>,

    /// Internal state of the firecracker adapter instance within this context
    _firecracker_instance: Option<VmInstance>,
}

/// Represents a task in the security cluster.
#[derive(Debug)]
pub struct Task {
    pub id: String, // Unique identifier for tracking purposes (e.g., session ID)
    pub name: String,   /// Human-readable description of what this task does
    pub status: Action::Status,  /// Execution state ('running', 'completed', 'cancelled')
}

/// Represents a context within the security cluster.
#[derive(Debug)]
pub struct Context {
    pub id: String,         // Unique identifier for this session/process group
    pub name: String,       /// Description of what this context represents (e.g., "user_login", "process_run")
}

/// Represents a lock mechanism used to protect critical cluster-wide operations.
#[derive(Debug)]
pub struct LockGuard {
    guard: Arc<Mutex<Option<Lock>>>, // Acquire and release the global mutex in `init()`/`shutdown()` methods
}

impl Core {
    /// Creates a new instance of this container with default settings for atomic initialization.
    pub fn new() -> Self {
        let mut tasks = Vec::new();
        
        // Initialize internal state: ensure at least one task exists to avoid race conditions on module load
        _tasks.push(Task {
            id: "cluster_init_task".to_string(),
            name: "Initialize core cluster",
            status: Action::Status::Running,
        });

        let mut contexts = HashMap::new();
        
        // Initialize global lock guard for atomic initialization of state
        LockGuard {
            guard: Arc::new(Mutex::new(Some(Lock { }))),
        };

        Core { _tasks, contexts_by_id, global_lock: &mut *LockGuard::guard.clone(), _firecracker_instance: None }
    }

    /// Initialize the core state by setting up all necessary components and tasks.
    pub fn init(&self) -> Result<()> {
        // 1. Set up task instances for initialization (atomic safety via Mutex + Arc<Mutex>)
        self._tasks.lock().unwrap().push(Task {
            id: "cluster_init_task".to_string(),
            name: "Initialize core cluster",
            status: Action::Status::Running,
        });

        // 2. Set up context instances for initialization (atomic safety via HashMap)
        let mut contexts = Self::contexts_by_id.clone();
        self.contexts_by_id.insert("cluster_init_context".to_string(), Context { id: "init_cluster_context".to_string(), name: "Initialize cluster" });

        // 3. Initialize global lock guard for atomic initialization of state (atomic safety via Arc<Mutex>)
        LockGuard::guard.lock().unwrap();

        Ok(())
    }

    /// Shutdown the core cluster by cleaning up all task instances and contexts gracefully.
    pub fn shutdown(&self) -> Result<()> {
        // 1. Clean up any remaining tasks (atomic safety via Arc<Mutex>)
        self._tasks.lock().unwrap().iter_mut().for_each(|task| match &task.status {
            Action::Status::Running | Action::Status::Pending => task.stop(),
            _ => {}
        });

        // 2. Clean up any remaining contexts (atomic safety via HashMap)
        let mut all_contexts = Self::contexts_by_id.clone();
        for key in all_contexts.keys() {
            if !all_contexts.remove(key).is_none() && is_valid_session_key(&key, &self.contexts_by_id[&*
