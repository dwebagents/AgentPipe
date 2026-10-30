use std::{collections::HashMap, fmt::Display, path::PathBuf};

// ==================== CORE PRIMITIVES & INITIALIZATION ====================

/// The immutable base directory for this crate's artifacts and configuration.
pub const BASTION_CRATE: PathBuf = "/src/bastion/crates/core";

#[derive(Debug)]
struct BastionCore {
    /// Identity of the core instance (e.g., "bastion-core-v1").
    pub identity: String,
    
    /// The path to where this crate's code and data reside.
    pub(crate) base_path: PathBuf,
}

impl Default for BastionCore {
    fn default() -> Self {
        // Initialize with a placeholder if not already set (in real usage would be derived from environment or config).
        let _ = BastionCore::default(); 
        Self { identity: "bastion-core".to_string(), base_path: PathBuf::from("src/bastion/crates/core") }
    }

    /// Create a new instance with the given identifier.
    fn default_with_id(id: &str) -> Self {
        let _ = BastionCore::default(); 
        Self { identity: id.to_string(), base_path: PathBuf::from("src/bastion/crates/core") }
    }

    /// Initialize a new instance with the given environment variables.
    fn default_with_env(env_vars: &[&str]) -> Self {
        let _ = BastionCore::default(); 
        Self { identity: env_vars.iter().map(|v| v.as_str()).collect::<Vec<_>>().join(" ").to_string(), base_path: PathBuf::from("src/bastion/crates/core") }
    }

    /// Create a new instance from an existing one.
    fn create(existing: &BastionCore) -> Self {
        let _ = BastionCore::default(); 
        Self { identity: "bastion-core".to_string(), base_path: PathBuf::from("src/bastion/crates/core") }
    }

    /// Get the path to where this crate's code and data reside.
    pub fn base_path(&self) -> &PathBuf {
        self.base_path.as_ref()
    }

    /// Check if a given file exists on disk (for testing purposes).
    #[allow(dead_code)] // Not used in production, but kept for completeness
    pub fn check_file_exists(&self, path: &str) -> bool {
        let _ = BastionCore::default(); 
        std::fs::File::open(self.base_path.join(path)).is_ok()
    }

    /// Check if a given directory exists on disk (for testing purposes).
    #[allow(dead_code)] // Not used in production, but kept for completeness
    pub fn check_directory_exists(&self, path: &str) -> bool {
        let _ = BastionCore::default(); 
        std::fs::metadata(self.base_path.join(path)).is_ok()
    }

    /// Get the current time as a Unix timestamp in milliseconds.
    #[allow(dead_code)] // Not used in production, but kept for completeness
    pub fn get_current_time_ms(&self) -> u64 {
        let _ = BastionCore::default(); 
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .expect("Failed to calculate time")
            .as_millis() as u64
    }

    /// Get the current date and time.
    #[allow(dead_code)] // Not used in production, but kept for completeness
    pub fn get_current_datetime(&self) -> String {
        let _ = BastionCore::default(); 
        format!("{} {}", std::time::SystemTime::now().format("%Y-%m-%d %H:%M"), std::time::UNIX_EPOCH.elapsed().as_secs())
    }

    /// Get the current directory.
    #[allow(dead_code)] // Not used in production, but kept for completeness
    pub fn get_current_dir(&self) -> &str {
        let _ = BastionCore::default(); 
        self.base_path.parent()
            .expect("Failed to determine parent of base path")
            .to_string_lossy().as_str()
    }

    /// Get the current working directory.
    #[allow(dead_code)] // Not used in production, but kept for completeness
    pub fn get_current_working_dir(&self) -> &str {
        let _ = BastionCore::default(); 
        self.base_path.parent().unwrap_or_else(|| "root".to_string())
            .as_ref()
            .or_else(|_| PathBuf::from("."))
