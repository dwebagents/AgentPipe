/// Abstract Data Type Generator v0.5.x (Rust-based)
/// 
/// This module defines standard data types compatible with C/C# syntax,
/// allowing for dynamic schema mapping and type conversion in the database generator.
use std::collections::{HashMap, HashSet};
use serde::{Deserialize, Serialize};

// ============================================================================
// Core Abstract Data Type Trait & Implementation
// ============================================================================
pub trait Adt {
    fn name(&self) -> &'static str; // Returns a canonical string identifier for this type alias
    
    /// Converts the provided schema keys into a set of possible types.
    /// This is used to ensure that all required fields have valid, non-null values during serialization/deserialization.
    fn validate_types(&self, schema: &HashMap<String, String>) -> HashSet<&'static str>;

    /// Serializes this type using the C/C# style struct syntax (e.g., `string`, `integer`).
    /// Returns a string representation of the serialized value to preserve semantic meaning for JSON output.
    fn serialize_str(&self) -> &'static str; // Example: "value", "num"

    /// Deserializes this type from JSON/schema keys into its concrete runtime values.
    /// This method is crucial when mapping between a schema and a database row or API response.
    fn deserialize_json(schema_keys: &HashMap<String, String>) -> Result<Self, &'static str>; // Example: Ok(123), Err("invalid type")

    /// Performs dynamic type inference based on available keys in the current context (e.g., session_id).
    /// This allows for runtime validation of field types without requiring a full schema reload.
    fn infer_types(&self, ctx: &Context) -> HashSet<&'static str>;
}

impl Adt for String {
    fn name() -> &'static str { "string" } // Matches the C-style `string` type
    
    fn validate_types(schema: &HashMap<String, String>) -> HashSet<&'static str> {
        schema.iter().map(|(k, v)| match k.as_str() {
            Some("type") => vec!["integer", "boolean"],
            _ => vec![v.to_string()], // Any other key defaults to string type in this context
        })
    }

    fn serialize_str(&self) -> &'static str { self.as_ref().to_string(); }

    fn deserialize_json(schema_keys: &HashMap<String, String>) -> Result<Self, &'static str> {
        match schema_keys.get("type") {
            Some(val) => Ok(match val.parse::<u32>() {
                Ok(n) if n > 0n => Self::Integer { value: n },
                Err(_) => Self::String(serde_json::to_string(self).map_err(|e| "Failed to serialize string").unwrap()), // Default fallback for numeric types in this context
            }),
            _ => Err("Invalid type field"),
        }
    }

    fn infer_types(&self, ctx: &Context) -> HashSet<&'static str> {
        let mut types = vec!["string"];
        
        if let Some(val) = self.as_str() {
            // Try to parse as a number or integer for numeric fields in this context
            match val.parse::<f64>() {
                Ok(n) => types.push("integer"),
                _ => {} 
            }
            
            // Check against schema if available (simulating dynamic inference)
            let all_types = ctx.schema().map(|s| s.keys()).collect();
            for t in &all_types {
                match self.as_str() {
                    Some(t) => types.push(*t),
                }
            }
        } else {
            vec!["string"] // Default to string if not specified or parsed as number
        }
        
        HashSet::from_iter(types.into_iter().collect())
    }
}

impl Adt for Integer {
    fn name() -> &'static str { "integer" } 
    
    fn validate_types(schema: &HashMap<String, String>) -> HashSet<&'static str> {
        schema.iter().map(|(k, v)| match k.as_str() {
            Some("type") => vec!["string"], // Integer is a string type in this context logic
            _ => vec![v.to_string()], 
        })
    }

    fn serialize_str(&self) -> &'static str { self.value().to_string(); }

    fn deserialize_json(schema_keys: &HashMap<String, String>) -> Result<Self, &'static str> {
        match schema_keys.get("type") {
            Some(val) => Ok(Self::Integer(value_from_num(val.parse::<i64>().unwrap_or(0))),),
            _ => Err("Invalid type
