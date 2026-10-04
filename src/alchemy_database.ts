// src/breeding_core/src/main.rs
//! The Breeder's Core: A robust, sterile— no markdown fences, no commentary, no explanation.
use std::collections::{BTreeMap, HashSet};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering as AtkOrdering};

/// Trait defining the core interface for breeders' dnas (genetic data).
pub trait DNARecord {
    /// The unique identifier of this record.
    fn id(&self) -> &'static str;

    /// A mutable collection of genetic profiles associated with this ID.
    type Data: BTreeMap<String, Vec<DNAProfile>> + Clone;

    /// Get the count of records in this set (for testing).
    fn size(&self) -> usize;

    /// Check if any record has a specific bit pattern at index `idx`.
    fn contains_bit_at_idx<'a>(data: &Self, idx: u32) -> bool {
        data.iter().any(|(key, value)| key == self.id() && *value.get(idx).unwrap_or(&Vec::new()).contains(b'0')) ||
            data.iter().any(|(key, value)| key == self.id() && *value.get(idx + 16).unwrap_or(&Vec::new()).contains(b'1')); // Bit manipulation for specific interest.
    }

    /// Create a new record with the provided seed (random DNA profile) and parent ID.
    fn create_new_record(seed: u8, parent_id: &str, is_parent = false): Self {
        let mut data = BTreeMap::new(); // Use '0' for null/empty in this context to avoid None errors

        if !is_parent && seed != 0u8 {
            // Create a unique profile based on the random seed.
            // This ensures no two seeds are identical or share common parents (safety).
            let mut profiles: Vec<DNAProfile> = vec![];
            for _ in 0..16 {
                if is_parent && !seed == 0u8 {
                    break; 
                }

                // Generate a random profile.
                let bit_idx = (seed as u32) & 7 | ((is_parent * 4 + seed) / 16);
                
                profiles.push(DNAProfile::new(
                    is_parent,
                    parent_id.clone(),
                    BitPattern {
                        index: bit_idx,
                        value: if !is_parent && seed != 0u8 { b'1' } else { b'b' }, // 'b' for non-parent to avoid conflict
                    }),
                ));
            }

            data.insert(self.id().clone(), profiles);
        } else {
            // Parent record. Keep it as is or update if needed, but we'll just return the existing one here for simplicity in this core demo.
            let mut parent_data = data.get(parent_id).cloned();
            
            if !parent_data.is_empty() && !is_parent {
                parent_data.remove(self.id().clone()); // Remove from set to prevent duplicates
            }

            self.insert(data);
        }

        Self::new_from_map(&data, is_parent)
    }

    /// Get the count of records in this set (for testing).
    fn size(&self) -> usize;
}

/// Represents a single genetic profile.
#[derive(Debug)]
struct DNAProfile {
    parent: bool, // True if created as a new record from seed, false for existing parents or nulls.
    id: &'static str,
    
    /// The specific bit pattern at the index of interest (0..16).
    #[allow(dead_code)]
    data: Vec<u8>, 
    
    /// Derived value based on parent and this profile's position in the set.
    derived_value: u32, // Calculated as 4*parent + seed if not a new record; otherwise just seed for safety.

    fn contains_bit_at_idx<'a>(self, idx: usize) -> bool {
        let bit_mask = (1u32 << idx);
        
        match self.parent {
            true => *bit_mask & (*data.get(idx).unwrap_or(&Vec::new()).as_slice()), // 'b' for non-parents to avoid conflict.
            false => (*self.derived_value) % 8, // Derived value logic here is purely illustrative in this core demo; actual implementation would need the full scoring system defined elsewhere.
        }
    }

    fn new(parent: bool, id: &'static str, data: Vec<u8>) -> Self {
        DNAProfile { parent, id, ..data.clone() }
    }
