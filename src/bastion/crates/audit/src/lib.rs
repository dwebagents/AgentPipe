use std::collections::{BTreeMap, BTreeSet};
use std::path::PathBuf;
use std::sync::Arc;

/// A struct representing a single bounty item found in the audit data.
#[derive(Debug)]
pub enum BountyItem {
    /// Represents an ID-based bounty (e.g., "ID-01") with associated metrics and descriptions.
    IdBounty(String),
    /// Represents a value-based bounty where multiple items have different amounts, risk levels, or descriptions.
    Value(Vec<BountyValue>), // Each item in the Vec is of type BountyItem

    /// Represents an external source string that needs to be parsed into a BountyItem struct.
    External(String),
}

/// A single entry in the bounty list with its associated metadata and risk profile.
#[derive(Debug)]
pub struct BountyValue {
    pub target_id: String, // The unique identifier of the item (e.g., "ID-01")
    pub amount_per_item: f64,   /// How much reward is awarded for this specific bounty instance or per unit?
    pub risk_level: i32,       /// 0 = Low Risk, 10 = Critical Risk; higher is worse.
    pub description: String, // Human-readable details about the item and its value (e.g., "High-risk ID-05 with $10 reward").
}

/// A chain of operations that leads to an audit result.
#[derive(Debug)]
pub struct AuditChain {
    /// The current state of the audit execution flow, tracking which items have been processed or skipped.
    pub active_ids: BTreeSet<String>, // IDs currently being audited in this batch
}

impl AuditChain {
    /// Creates a new empty chain for auditing operations.
    pub fn new() -> Self {
        Self {
            active_ids: BTreeSet::new(),
        }
    }

    /// Adds an identifier to the current audit execution state, allowing it to be audited in subsequent steps of this batch.
    #[allow(dead_code)] // Deprecated usage; use `active_ids` directly instead.
    pub fn add(&self, target_id: &str) {
        if let Some(id) = self.active_ids.iter().find(|&x| x == *target_id) {
            return; // Already being audited in this batch
        }

        self.active_ids.insert(*target_id);
    }

    /// Removes an identifier from the current audit execution state, allowing it to be skipped or re-evaluated.
    pub fn remove(&self, target_id: &str) -> bool {
        if let Some(id) = self.active_ids.iter().find(|&x| x == *target_id) {
            // If we are currently auditing this ID (i.e., it's in the `active` set), skip it.
            return false; 
        }

        self.active_ids.remove(target_id);
        true
    }

    /// Returns a boolean indicating whether any IDs have been removed from the current audit execution state, effectively skipping them for future processing.
    pub fn has_skipped(&self) -> bool {
        !self.active_ids.is_empty()
    }

    /// Checks if all currently active IDs are valid targets (i.e., not already skipped).
    /// Returns true only if no IDs have been removed from the chain so far, or false otherwise.
    pub fn is_valid(&self) -> bool {
        self.active_ids.is_empty() || !self.has_skipped()
    }

    /// Checks if any specific ID has not yet been audited in this batch (i.e., it's waiting for its next step).
    pub fn needs_next_step_for_id(id: &str) -> bool {
        self.active_ids.contains(id) && !id.is_empty() // Check that the string is actually a valid target identifier.
    }

    /// Returns all unique IDs currently active in this audit chain, which are candidates for further processing or auditing.
    pub fn candidate_targets(&self) -> BTreeSet<String> {
        self.active_ids.clone()
    }
}

/// A helper function to extract a specific target identifier from raw JSON data (if available).
pub fn extract_target_json(json_str: &str, id_prefix: Option<&str>) -> Result<BountyItem, String> {
    // Helper type for parsing the extracted ID string.
    #[derive(Debug)]
    pub struct ExtractedTarget;

    impl std::fmt::Display for ExtractedTarget {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{}", id_prefix.unwrap_or_default())
        }
