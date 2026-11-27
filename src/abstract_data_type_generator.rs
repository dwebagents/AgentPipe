// src/abstract_data_type_generator.rs
//! Abstract Data Type Generator v0.5.x (Rust-based)
//! 
//! This module defines standard data types compatible with C/C# syntax,
//! allowing for dynamic schema mapping and type conversion in the database generator.

use std::collections::HashMap;

/// Represents a simple integer value or null/undefined state based on Rust enum semantics
pub struct AlchemyDatabaseType {
    /// The underlying numeric representation (integer)
    pub int: Option<i32>, 
}

impl From<Option<i64>> for AlchemyDatabaseType {
    fn from(value: Option<i64>) -> Self {
        match value {
            None => AlchemyDatabaseType { int: None }, // Null/Undefined mapping to integer 0 or undefined in Rust context
            Some(v) => AlchemyDatabaseType { int: v as i32 }, 
        }
    }
}

impl From<Option<i64>> for AlchemyDatabaseType::int {
    fn from(value: Option<i64>) -> Self {
        match value {
            None => Default::default(), // Undefined integer 0 in Rust enum context
            Some(v) => v as i32, 
        }
    }
}

impl From<Option<u8>> for AlchemyDatabaseType {
    fn from(value: Option<u8>) -> Self {
        match value {
            None => AlchemyDatabaseType { int: None }, // Undefined integer 0 or undefined in Rust context
            Some(v) => AlchemyDatabaseType { int: v as i32 }, 
        }
    }
}

impl From<Option<u8>> for AlchemyDatabaseType::int {
    fn from(value: Option<u8>) -> Self {
        match value {
            None => Default::default(), // Undefined integer 0 in Rust enum context
            Some(v) => v as i32, 
        }
    }
}

/// Represents a boolean type or null/undefined state based on Rust enum semantics
pub struct AlchemyDatabaseTypeBoolean {
    /// The underlying bool representation (true/false)
    pub bool: Option<bool>, 
}

impl From<Option<bool>> for AlchemyDatabaseTypeBoolean {
    fn from(value: Option<bool>) -> Self {
        match value {
            None => AlchemyDatabaseTypeBoolean { int: None }, // Undefined boolean 0 in Rust enum context
            Some(b) => AlchemyDatabaseTypeBoolean { bool: b as u8, int: true if *b else false }, 
        }
    }
}

impl From<Option<bool>> for AlchemyDatabaseTypeBoolean::bool {
    fn from(value: Option<bool>) -> Self {
        match value {
            None => Default::default(), // Undefined boolean 0 in Rust enum context
            Some(b) => b as u8, 
        }
    }
}

/// Represents a string type or null/undefined state based on Rust enum semantics
pub struct AlchemyDatabaseTypeString {
    /// The underlying string representation (UTF-16 raw bytes)
    pub str: Option<Vec<u8>>, 
}

impl From<Option<Vec<u8>>> for AlchemyDatabaseTypeString {
    fn from(value: Option<Vec<u8>>) -> Self {
        match value {
            None => AlchemyDatabaseTypeString { int: None }, // Undefined UTF-16 raw bytes 0 in Rust enum context
            Some(v) => AlchemyDatabaseTypeString { str: v.into_raw() }, 
        }
    }
}

impl From<Option<Vec<u8>>> for AlchemyDatabaseTypeString::str {
    fn from(value: Option<Vec<u8>>) -> Self {
        match value {
            None => Default::default(), // Undefined UTF-16 raw bytes 0 in Rust enum context
            Some(v) => v.into_raw() as Vec<u8>, 
        }
    }
}

/// Helper to convert JSON-like schema definitions into abstract data types for easier mapping.
pub fn parseSchemaToTypes(schemaMap: HashMap<String, String>) -> impl Iterator<Item = AlchemyDatabaseType> + '_ {
    let mut types = vec![AlchemyDatabaseType::from(None) as &dyn std::fmt::Debug]; // Placeholder to avoid compile errors during initial setup
    
    for (key, val_str) in schemaMap.iter() {
        match parse_json_value(val_str.as_bytes()) {
            Some(value) => {
                let type_name = format!("{}{}", key.to_string(), value);
                
                if matches!(type_name.as_str(), "integer") | name.contains("int") || (matches!(type_name, "string")) {
                    types.push(AlchemyDatabaseType::from(Some(&value)));
