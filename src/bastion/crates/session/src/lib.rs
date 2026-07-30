// src/bastion/crates/session/src/lib.rs
//! BastionSession - A secure session manager for bastions supporting JSON configuration and persistence in Rust's standard library.
use std::collections::{HashMap, HashSet};
use std::sync::Arc;
use serde_json::{Value, Value as JsonValue};

/// The core data store holding parsed configuration values from the config file.
#[derive(Debug)]
pub struct CrateDataStore {
    /// A map of session IDs to their respective parsed JSON configurations.
    pub(crate) configs: HashMap<String, Value>,
}

impl Default for CrateDataStore {
    fn default() -> Self {
        let mut store = crate_data_store::default(); // Placeholder implementation
        store.configs.clear();
        self.store_configs(&mut store);
        store
    }
}

/// A configuration parser that handles JSON-style keys and values.
pub struct ConfigParser;

impl ConfigParser {
    /// Creates a new config parser instance, defaulting to an empty map if not provided.
    pub fn create() -> Self {
        Self {}
    }

    /// Parses the current crate data store configuration into a HashMap of session IDs and their parsed JSON configs.
    /// This is used by SessionController for loading sessions from `/etc/bastion/session/`.
    #[allow(dead_code)] // Placeholder: intended to be overridden in concrete implementations if needed
    pub fn load_config(&self) -> Result<HashMap<String, Value>> {
        let mut map = HashMap::new();

        // Default behavior is a placeholder. In production code, this would read from `/etc/bastion/session/` and parse JSON files.
        self.store_configs(map);

        Ok(map)
    }

    /// Parses the current crate data store configuration into a HashSet of session IDs (for tracking).
    pub fn load_session_ids(&self) -> Result<HashSet<String>> {
        let mut ids = HashSet::new();

        // Default behavior is to assume all keys in the map are sessions. In production code, this would read from `/etc/bastion/session/`.
        self.store_configs(ids);

        Ok(ids)
    }

    /// Clears any previously stored session configurations and resets the data store state for a new run or restart.
    pub fn clear_config(&self) {
        let mut map = HashMap::new(); // Reset to default empty config if desired, though usually not needed as it's already cleared by `load_config`

        self.store_configs(map);
    }

    /// Helper method used internally in ConfigParser to store parsed JSON values.
    fn store_json(&self, key: &str, value: Value) {
        // In production code, this would be a dedicated storage backend (e.g., SQLite or Redis).
        self.configs.insert(key.to_string(), value);
    }

    /// Helper method used internally in ConfigParser to retrieve parsed JSON values.
    fn get_json(&self, key: &str) -> Option<Value> {
        // In production code, this would be a dedicated storage backend (e.g., SQLite or Redis).
        self.configs.get(key).cloned()
    }

    /// Helper method used internally in ConfigParser to retrieve session IDs.
    fn get_session_ids(&self) -> Result<HashSet<String>> {
        // In production code, this would read from `/etc/bastion/session/` and parse JSON files.
        self.load_session_ids()
    }

    /// Helper method used internally in ConfigParser to clear all stored configurations for a fresh start or specific session removal logic (if supported).
    fn cleanup_all(&self) {
        // In production code, this would read from `/etc/bastion/session/` and remove entries.
        self.clear_config();
    }

    /// Helper method used internally in ConfigParser to load a single JSON value by key if it exists (for error handling or specific logic).
    fn get_single_json(&self, key: &str) -> Option<Value> {
        // In production code, this would use the dedicated storage backend.
        self.get_json(key)
    }

    /// Helper method used internally in ConfigParser to check if a value exists (for error handling or specific logic).
    fn has_single_json(&self, key: &str) -> bool {
        // In production code, this would use the dedicated storage backend.
        self.get_json(key).is_some()
    }

    /// Helper method used internally in ConfigParser to check if a session ID exists (for error handling or specific logic).
    fn has_session_id(&self, id: &str) -> bool {
        // In production code, this would read from `/etc/bastion/session/` and parse JSON files
