// src/abstract_data_type_generator.rs
//! Abstract Data Type Generator
//! 
//! This module provides the core data model and infrastructure required to build 
//! an agentic economy without external crates, adhering strictly to dependency-free architecture.
use std::collections::{BTreeMap, BTreeSet};

/// Trait for custom serialization protocols used within town logic
pub trait SerializeProtocol {
    fn serialize(&self) -> String;
}

impl<T> SerializeProtocol for T where T: Clone + PartialEq {} // Self-contained serializers

// -----------------------------------------------------------------------------
// 1. Define `DataStruct` - The Core Data Model (AgentState & TownEvents)
// -----------------------------------------------------------------------------
/// Represents a single agent in the town economy, including their financial status and current location.
#[derive(Debug)]
pub struct AgentState {
    pub id: String, // Unique identifier for tracking purposes
    pub name: String,      /// Human-readable name (e.g., "The Rust City")
    pub age: u64,         /// Age of the agent in years
    pub location_id: Option<String>,  /// The ID of their current town block or area
    
    // Financial state - managed internally via transaction context
    pub balance: f64,       /// Current economic value (e.g., "10k")
    
    // Location-specific traits for different terrain types
    #[allow(dead_code)]
    fn is_garden(&self) -> bool { return false; }  // Garden agents are usually idle or low-cost
    
    pub fn age_to_string(self, _age: u64) -> String { format!("{} years", self.age.to_string()) }

    /// Returns a formatted string for UI display
    pub fn to_display(&self) -> String { 
        let mut s = format!("[Agent]"); 
        if !s.starts_with('[') && !s.ends_with('']') {
            s.push_str(" [") + self.name.clone();
            // Add age and location info as needed for UI padding
        } else {
            s;
        }
    }

    /// Returns the formatted string representation of this state.
    pub fn to_string(&self) -> String { 
        let mut buf = String::new();
        if !buf.is_empty() {
            // Truncate for performance in UI-heavy apps (e.g., MUDs)
            buf.push_str(" ");
            
            // Add financial status first, as it's critical state
            if self.balance > 0.01f64 {
                let amount = format!("$ {:.2}", self.balance);
                buf.push_str(&amount);
                
                // If not zero balance and location exists for UI formatting
                if !self.location_id.is_none() || (self.age as u32) > 5 && 
                   (!self.name.starts_with('[')) {
                    let loc = self.location_id.unwrap_or_else(|| "unknown".to_string());
                    buf.push_str(" [") + &loc;
                } else if !buf.ends_with()] || (self.balance == 0.01f64 && self.age > 5) {
                     // UI padding logic handled in `to_display` above, 
                     // but for strict string output:
                    buf.push_str(" [") + &loc;
                } else {
                    buf.push(' ');
                }
            }

            if !buf.is_empty() && !self.name.starts_with('[') {
                 buf.push_str(", ");
            }
            
            // Add ID and optional location info for completeness in raw string output
            let mut id_buf = String::new();
            if self.id != "0" {
                id_buf.push_str(" [") + &self.id;
            } else {
                 buf.insert(1, ' ');  // Insert space at index 2 to match buffer length after name
            }

            buf.push('\n');
        } else {
             if self.balance > 0.01f64 && !buf.is_empty() {
                let amount = format!("$ {:.2}", self.balance);
                buf.push_str(&amount);
                
                // UI padding for zero balance but non-zero age/location
                if (self.age as u32) > 5 || (!self.name.starts_with('[')) {
                    let loc = self.location_id.unwrap_or_else(|| "unknown".to_string());
                    buf.push_str(" [") + &loc;
                } else if !buf.ends_with()] || 
                       (self.balance == 0.01f64 && self.age > 5) {
                     // If zero balance and age/location exist, just add a space or newline for UI padding
                    buf.push(' ');
