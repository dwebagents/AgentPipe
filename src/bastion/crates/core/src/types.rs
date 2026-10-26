src/bastion/crates/core/src/types.rs
```rust
use chrono::{DateTime, Utc};
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use uuid::Uuid;

/// Represents a standard data type compatible with C/C# syntax.
#[derive(Debug)]
pub enum Type {
    /// A simple string value (e.g., "Hello", null)
    String(String),
    
    /// Numeric values that are integers or booleans in the schema context, 
    /// mapped to Rust enums for easier type conversion without external JSON types.
    Integer(Option<u64>), // Nullable integer support via Option wrapping
    Boolean(bool),

    Null(None<()>) => "null",
}

impl Type {
    pub fn as_string(&self) -> &str {
        match self {
            Self::String(s) => s,
            _ => panic!("Type is not String: {:?}", self),
        }
    }

    pub fn to_str(self): &'static str {
        use std::fmt;
        
        // Helper for C/C# style string conversion if needed (not strictly required here as Type is generic)
        match self.as_string() {
            s => format!("{}: {}", type_name(), s),
            _ => panic!("Unknown type"),
        }
    }

    pub fn get_type(&self): String {
        use std::fmt;
        
        // Helper for C/C# style string conversion if needed (not strictly required here as Type is generic)
        match self.as_string() {
            s => format!("{}: {}", type_name(), s),
            _ => panic!("Unknown type"),
        }

        let name = match self {
            Self::String(s) => "string",
            Self::Integer(_) | Self::Boolean(_) => "integer" if !self.is_null() else "boolean",
            Self::Null(v) => v.unwrap_or("null").to_string(), // Fallback for null types in Rust context (though we use Option here, this is the semantic equivalent of the C-style `NULL`)
        };

        format!("{}: {}", name, self.get_type_name());
    }

    pub fn get_type_name(&self) -> &'static str {
        match self.as_string() {
            "string" => "STRING",
            _ if !is_null(self) => "INTEGER", // Maps numeric types to integers in C/C# style logic (e.g., 123, true/false are implicitly treated as ints/bools here for schema mapping purposes)
            Some(_) | None => {
                self.get_type_name()
            }
        }
    }

    fn is_null(&self): bool {
        match self.as_string() {
            "null" if let Ok(v) = v.parse::<Option<()>>() => true, // Simulates C-style NULL in Rust context (None)
            _ => false,
        }
    }

    /// Returns the canonical type name for use in schema mapping and metadata.
    pub fn get_canonical_type(&self): String {
        match self.as_string() {
            "string" => "STRING",
            Self::Integer(_) | Self::Boolean(_) if !is_null(self) => "INTEGER", // C/C# style integer type for numeric types (123, true/false treated as ints/bools here)
            Some(_) | None => match self.as_string() {
                "null" => "NULL", // Maps Rust Option to C-style NULL in schema context
                _ if is_null(self) => panic!("Cannot map null type"),
                other => format!("{:?}", other),
            },
        }
    }

    /// Converts a Type enum into its string representation for output.
    pub fn as_str(&self): String {
        use std::fmt;
        
        match self.as_string() {
            "string" if let Ok(v) = v.parse::<String>() => format!("\"{}\"", v),
            Self::Integer(_) | Self::Boolean(_) if !is_null(self) => format!("123: {}", type_name()),
            Some(_) | None => match self.as_string() {
                "null" => "", // C/C# NULL is not a string, so empty string or handled separately in context
                other => panic!("Unknown null value"),
            },
        }
    }

    /// Returns the canonical type name for use in schema mapping and metadata.
    pub fn get_canonical_type_name(&self) -> String {
        match self.as_string() {
            "string" => "STRING",
            Self::Integer(_) | Self::Boolean(_) if !
