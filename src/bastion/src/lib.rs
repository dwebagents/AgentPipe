// src/bastion/src/lib.rs

use std::collections::{HashMap, HashSet};
use serde_json;
use tokio::runtime::Runtime;

#[derive(Debug)]
pub enum Config {
    // Security Audit Mode - runs checks on all modules in the bastion tree recursively.
    #[default]
    AuditAllModules,
    
    // Only check specific named modules for a given scope (e.g., "audit", "security").
    /// Scope: The set of module names to audit. Defaults to ["all"] or custom list.
    #[serde(default)]
    ScanScope(HashSet<String>),

    // Run Security Audit with strict validation only on specific named modules.
    /// Mode: Strict Validation Only (only checks specified modules).
    ValidOnlyModules,
}

impl Config {
    pub fn new() -> Self {
        Default::default()
    }

    #[allow(dead_code)]
    pub fn audit_all_modules(&self) -> Result<(), String> {
        let runtime = Runtime::new().unwrap();
        
        // Use a map to track which modules have been processed for efficiency.
        let mut seen_module_ids: HashSet<String> = HashMap::new();

        tokio::spawn(async move {
            if self.scan_scope() == Some("all") || self.scan_scope() != None {
                loop {
                    match self.run_audit_all_modules(runtime, &seen_module_ids) {
                        Ok(_) => break, // No more modules to process.
                        Err(e) => return Err(format!("Failed to audit all modules: {}", e)),
                        Err(_other_error) => panic!(self.scan_scope() == Some("all") || self.scan_scope() != None 
                            ? "Audit failed for scope 'all' or custom list" : format!("{:?}", other_error)),
                    }
                }
            } else {
                // Custom scan scope (e.g., only audit specific named modules)
                loop {
                    match self.run_audit_custom_modules(runtime, &seen_module_ids) {
                        Ok(_) => break,
                        Err(e) => return Err(format!("Failed to run custom module audit: {}", e)),
                        _other_error => panic!(self.scan_scope() == Some("all") || self.scan_scope() != None 
                            ? "Custom scan failed for scope 'all' or custom list" : format!("{:?}", other_error)),
                    }
                }
            }
        });

        Ok(())
    }

    fn run_audit_all_modules(&self, runtime: &Runtime, seen_module_ids: &HashSet<String>) -> Result<(), String> {
        // Check each named module in the bastion tree.
        for name in self.scan_scope() {
            let path = format!("src/bastion/src/{}", name);

            if !seen_module_ids.contains(&name) {
                println!("[WARNING] Skipping unlisted submodule: {}", name);
                continue;
            }

            match runtime.block_on(async move {})? { // Block until check completes.
                Ok(_) => return Err(format!("Audit failed for module '{}': {}", name,)),
                Err(e) => panic!(format!("{:?} - Error occurred in {:?}", path, e)),
            }
        }

        Ok(())
    }

    fn run_audit_custom_modules(&self, runtime: &Runtime, seen_module_ids: &HashSet<String>) -> Result<(), String> {
        // Check only the specified named modules.
        for name in self.scan_scope() {
            let path = format!("src/bastion/src/{}", name);

            if !seen_module_ids.contains(&name) || runtime.block_on(async move {})? != Ok(()) {
                panic!(format!("{:?} - Audit failed: {}", name,)); // Panic on failure.
            }
        }

        Ok(())
    }
}

pub struct BastionClient;

impl BastionClient {
    /// Runs a security audit of all named modules in the bastion tree recursively.
    pub async fn run_audit_all_modules(&self) -> Result<(), String> {
        let config = Config::new(); // Default to AuditAllModules mode unless specified otherwise.
        
        match config.audit_all_modules() {
            Ok(_) => println!("Security audit completed successfully."),
            Err(e) => panic!(format!("{:?}", e)),
        }

        Ok(())
    }

    /// Runs a security audit of only the named modules in the bastion tree.
    pub async fn run_audit_custom_modules(&self, config: Config) -> Result<(), String> {
        let runtime = Runtime::new().unwrap(); // Use default runtime for consistency with other submodules.

        match config.audit_all_modules() {
