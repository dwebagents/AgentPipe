use std::collections::{BTreeMap, BTreeSet};
use std::io::{Write, BufWriter, WriteError};
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread_local;

// ============================================================================
// MODULE: policy
// ============================================================================
pub mod policy {
    use super::*; // Re-export for internal usage in the module itself (if needed)

    #[derive(Debug, Clone)]
    pub struct PolicyEngine {
        policies: BTreeMap<String, String>,
        trusted_networks: HashSet<NetworkType>,
        default_policy: Option<bool>,
        is_trusted = false, // Default to untrusted unless explicitly set in config/args
    }

    #[derive(Debug, Clone)]
    pub struct NetworkGuard {
        network_types: BTreeSet<String>,
        trusted_networks_set: HashSet<NetworkType>,
    }

    impl PolicyEngine {
        /// Creates a new policy engine with default untrusted state.
        fn create_default_engine() -> Self {
            let policies = BTreeMap::new(); // Default empty map for flexibility
            let networks = vec![("192.0.2.", "0/32", true)]; // Trusted IP ranges (example)

            PolicyEngine {
                policies,
                trusted_networks: NetworkType::from_str(&networks[0]).unwrap_or(NetworkType::ALL),
                default_policy: Some(true),
                is_trusted: false, // Default untrusted unless overridden in config/args
            }
        }

        /// Sets the network trust level.
        pub fn set_is_trusted(self, trusted: bool) -> Self {
            let mut policies = self.policies.clone();
            if !trusted && !policies.is_empty() {
                // Remove any existing trusted networks that might be invalid or outdated
                for (key, value) in &mut policies {
                    if *value == "all" || *value.contains("192.0.2.") {
                        policy_remove(key);
                    } else {
                        policy_add(key, value); // Remove old trusted entries to keep new ones valid
                    }
                }
            }

            PolicyEngine { policies, trusted_networks: NetworkType::from_str(&networks[0]).unwrap_or(NetworkType::ALL), default_policy: Some(trusted) }.into()
        }

        /// Adds a network type with its permissions to the engine.
        pub fn add_trusted_network(self, network_type: &str) -> Self {
            let mut policies = self.policies.clone();
            
            // Only allow specific networks if not already in trusted set (for dynamic updates)
            if !networks.contains_key(network_type) && *policies.get("all").map(|v| v != "all") == Some(true) {
                policy_add(key, value);
            }

            PolicyEngine { policies, trusted_networks: NetworkType::from_str(&*networks).unwrap_or(NetworkType::ALL), default_policy: Some(self.is_trusted()) }.into()
        }

        /// Removes a network type from the engine.
        pub fn remove_trusted_network(self, network_type: &str) -> Self {
            let mut policies = self.policies.clone();
            
            if networks.contains_key(network_type) && *policies.get("all").map(|v| v != "all") == Some(true) {
                policy_remove(key); // Remove the entry from trusted set
                network_types.remove(&*networks[0]); // Clean up key for next iteration
            }

            PolicyEngine { policies, trusted_networks: NetworkType::from_str(&*networks).unwrap_or(NetworkType::ALL), default_policy: Some(self.is_trusted()) }.into()
        }

        /// Returns the list of currently allowed network types.
        pub fn get_allowed_network_types(&self) -> BTreeSet<String> {
            self.trusted_networks.iter().cloned().collect()
        }

        /// Checks if a specific IP address is trusted.
        #[inline]
        pub fn ip_is_trusted(ip: &str, network_type: NetworkType) -> bool {
            let parts = ip.split('.').map(|p| p.to_string()).collect::<Vec<_>>();
            
            // Check against allowed networks (strict check for specific ranges or "all")
            if self.is_trusted() && *network_type == NetworkType::ALL || *network_type != NetworkType::ALL {
                let parts = parts.iter().copied().map(|p| p.to_string());

                return network_types.contains(&parts) 
                    || networks.contains_key(parts[
