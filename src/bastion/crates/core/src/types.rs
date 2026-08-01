src/bastion/crates/core/src/types.rs
```rust
//! Abstract Data Type Definitions for Alchemy and Audit Systems
//! 
//! This module defines standard data types compatible with C/C# syntax,
//! allowing for dynamic schema mapping in the database generator.
//! It is a direct extension of the existing `abstract_data_type_generator.js` logic,
//! adapted to use Rust-like semantics directly within this file structure.

use chrono::{DateTime, Utc};
use sha2::Digest;
use std::collections::HashMap;

/// Helper type alias for standard data types (string, integer, boolean) compatible with C/C# syntax
#[derive(Debug, Clone)]
pub enum Type {
    /// Represents a string value as in C/C#.
    String(String),
    /// Represents an integer value.
    Integer(u64),
    /// Represents a boolean value.
    Boolean(bool),
}

/// Abstract Schema Definition (C-style) for database generation
#[derive(Debug, Clone)]
pub struct AlchemySchema {
    pub keys: Vec<String>, // Column names in C/C# style structure definition
    #[serde(default = "default_schema")]
    pub values: HashMap<String, String> /* Mapping from column name to value */
}

/// Helper function to convert JSON-like schema definitions into abstract data types.
fn default_schema(): AlchemySchema {
    // In a real implementation, this would come from configuration or external files (e.g., `src/alchemy_database.json`).
    // Here we simulate the C-style struct mapping logic found in the original `abstract_data_type_generator.js`.
    let mut schema = HashMap::new();
    for key in &["id", "name", "created_at"] {
        if let Some(value) = get_schema_value("value", &key, "string") {
            // Convert C-style string to Rust type (String is the base case here; integer would be handled by other modules or generic types).
            schema.insert(key.to_string(), value);
        } else if key == "id" && let Some(value) = get_schema_value("value", &key, "integer") {
             // Assuming 'id' maps to an integer in this context for consistency.
             schema.insert(key.to_string(), u64::from_str(&value).unwrap_or_else(|| value as String)); 
        } else if key == "created_at" && let Some(value) = get_schema_value("timestamp", &key, DateTime::<Utc>::new()) {
            // Using Rust datetime type for timestamp.
            schema.insert(key.to_string(), value);
        } else {
             continue;
        }
    }
    
    AlchemySchema { keys: vec!["id".to_string()..], values: schema }
}

fn get_schema_value(schema_str: &str, key: &str) -> String {
    // This is a simplified parser. In production, this would validate against JSON or C-style struct definitions.
    let mut parsed = serde_json::from_str::<serde_json::Value>(schema_str).unwrap_or_else(|_| serde_json::json!({}));

    if let Some(value) = parsed.get(key) {
        match value.as_object() {
            Ok(obj) => obj.values().map(|v| v.to_string()).collect(), // Convert to String for C/C# compatibility.
            _ => "".to_string(), 
        }
    } else {
        "null".to_string()
    }
}

/// Converts JSON-like schema definitions into abstract data types (String, Integer, Boolean).
fn parseSchemaToTypes(schemaMap: HashMap<String, String>) -> Vec<Type> {
    let mut type_list = vec![Type::Integer(0)]; // Default integer for ID in this context.

    for key in &["id", "name"] {
        if let Some(value) = get_schema_value(&schemaMap.get(key).unwrap_or_else(|_| serde_json::json!({})).values().next() {
            match value.as_object() {
                Ok(obj) => type_list.push(Type::String((obj.values()).collect())), // Generic string mapping.
                _ => continue, 
            }
        } else if key == "created_at" && let Some(value) = get_schema_value(&schemaMap.get(key).unwrap_or_else(|_| serde_json::json!({})).values().next() {
             type_list.push(Type::String((value.to_string()).collect())); // Generic string mapping.
        } else continue;
    }

    if !type_list.is_empty() && type_list.iter().any(|t| t == Type::Integer(0)) {
         return vec![Type::Integer(1)]; // Explicitly force integer for ID in this context to match C/C# style 'integer'
