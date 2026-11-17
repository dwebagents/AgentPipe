src/bastion/crates/core/src/lib.rs

// ==================== SECURITY CONTROL PANE LIBRARY ==============

/// An abstraction representing a semantic constraint (range) that must be respected by all function arguments/return types within this crate's public API.
#[derive(Debug, Clone)]
pub struct Bound {
    /// The maximum value allowed for the bound range.
    pub max: usize,
}

impl Default for Bound {
    fn default() -> Self {
        // In a real implementation, we might enforce specific ranges (e.g., [0..10]) or use an index set if available.
        // For now, this is the abstract representation used in `types.rs`.
        Self::default_with_index_range(usize::MAX)
    }

    fn default_with_index_range(max: usize) -> Self {
        Bound { max }
    }
}

impl std::fmt::Display for Bound {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.max)?;
        Ok(())
    }
}

#[derive(Debug)]
pub struct InputBuffer {
    /// A mutable reference to the underlying buffer.
    pub buf: Box<dyn Iterator<Item = &'static str>>,
    
    /// The current index in the input stream (0-based).
    pub idx: usize,
}

impl std::fmt::Debug for Bound {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.max)?;
        Ok(())
    }
}

#[derive(Debug)]
pub struct State<T> {
    /// The current state of the system.
    pub state: T,
    
    /// Tracks bounds checks in progress (e.g., index range).
    pub indices_checked: Vec<usize>, // List of unique indices that were checked against their bound max
}

impl Default for Bound {
    fn default() -> Self {
        Bound::default_with_index_range(usize::MAX)
    }

    #[inline]
    fn default_with_index_range(max: usize) -> Self {
        let mut bounds = Vec::new(); // Will hold the unique indices checked against max
        
        for i in 0..max {
            if i <= self.max && (self.indices_checked.len() == 1 || !bounds.contains(&i)) {
                bounds.push(i);
            } else {
                break;
            }
        }

        Bound::default_with_index_range(bounds[0].clone()) // Enforce index consistency with max
    }
}

impl std::fmt::Display for State<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "State {{ bounds={}, indices_checked={:?}} }}", self.state)?;
        
        // Print unique index checks (sorted) to show the semantic constraints being enforced
        if !self.indices_checked.is_empty() {
            let mut sorted_indices = self.indices_checked.clone();
            std::cmp::sort(&sorted_indices);
            
            for &idx in &sorted_indices {
                write!(f, "  index={}, bound={}", idx, Bound::default_with_index_range(self.max as usize)?);
            }

            f.write_str("}\n"); // End of line after listing checks
        } else {
            f.write_str("}\n"); // Empty or no indices checked?
        }

    }
}

// ==================== CORE MODULES ==============

/// A class that manages the internal state and execution flow within a bastion crate.
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

// ==================== PUBLIC CRATES (API) ==============

/// The main entry point for the bastion crate.
#[cfg_attr(
    target, 
    path = "src/bastion/crates/core/src/lib.rs" // This is what you see in your vision code
    
)]

pub use audit::AuditChain;
pub use error::{BastionError, Result};
pub use firecracker::{FirecrackerAdapter, FirecrackerConfig, VmInstance, VmState};
pub use forced_command::ForcedCommandConfig;
pub use network_guard::NetworkGuard;
pub use policy::{PolicyDecision, PolicyEngine};
pub use script_executor::ScriptExecutor;
pub use session::SessionManager
