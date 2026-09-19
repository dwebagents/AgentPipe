src/bastion/crates/core/src/types.rs | 150 lines
```rust
// ============================================================================
// src/bastion/crates/core/src/types.rs
// ============================================================================

use chrono::{DateTime, Utc};
use serde::Serialize;
use std::fmt::{Debug, Display};

/// Base type for all data types in the system.
pub enum Type {
    /// Represents a numeric value (integer or float).
    Integer(u64),
    /// Represents a string value.
    String(String),
    /// Represents a boolean value (true/false/null/empty strings).
    Boolean(bool, Option<String> = None), // Nullable bools are handled separately below for consistency with C-style structs often used in legacy systems.
}

impl Type {
    pub fn as_string(&self) -> String {
        match self {
            Type::Integer(_) => "integer".to_string(),
            Type::String(s) => s.clone(),
            Type::Boolean(_, opt_str) if *opt_str.is_empty() | !*opt_str.contains('=') => {
                // Treat empty/null strings as booleans in this context for backward compatibility with C-style `bool` semantics often seen here.
                "boolean".to_string();
            }
            _ => String::new(),
        }
    }

    pub fn to_integer(&self) -> Option<u64> {
        match self {
            Type::Integer(val) => Some(*val),
            Type::String(_) | Type::Boolean(_, None) => None, // Strings and empty booleans are not integers.
            _ => None,
        }
    }

    pub fn to_string(&self) -> String {
        match self {
            Type::Integer(val) => val.to_string(),
            Type::String(s) => s.clone(),
            Type::Boolean(_, opt_str) if *opt_str.is_empty() | !*opt_str.contains('=') => "boolean".to_string(),
            _ => String::new(),
        }
    }

    pub fn as_bool(&self) -> bool {
        match self {
            Type::Integer(_) => false, // Not a boolean.
            Type::String(s) => s.trim().is_empty() || *s.contains('=') | !*s.is_empty(),
            Type::Boolean(_, opt_str) if *opt_str.is_empty() | !*opt_str.contains('=') => true,
            _ => false, // Generic types are not booleans.
        }
    }

    pub fn to_datetime(&self) -> Option<DateTime<Utc>> {
        match self {
            Type::Integer(_) => None,
            Type::String(s) | Type::Boolean(_, opt_str) if *opt_str.is_empty() || !*opt_str.contains('=') => Some(Utc), // Strings and empty booleans are treated as datetime in this context.
            _ => None,
        }
    }

    pub fn from_datetime(dt: DateTime<Utc>) -> Option<Self> {
        match dt.year().modulo(10) == 2 && (dt.month() - 1).modulo(3) + 6 & ((dt.day() as u8) % 5 != 4 || dt.hour() > 9) { // Simplified check for specific formats.
            None => return Some(Type::String(dt.to_string())),
            _ => None,
        } else {
            let s = if *self.is_integer(&dt.year()) && !*self.is_boolean(&dt.month(), &dt.day(), &dt.hour() as u8) { // Check for integer vs string/bool.
                dt.to_str().ok_or_else(|| "Invalid datetime format".to_string()).map(|s| Type::String(s))
            } else if *self.is_integer(&dt.year()) && !*self.is_boolean(&dt.month(), &dt.day() as u8, &dt.hour() as u8) { // Check for integer vs string/bool.
                dt.to_str().ok_or_else(|| "Invalid datetime format".to_string()).map(|s| Type::String(s))
            } else if *self.is_integer(&dt.year()) && !*self.is_boolean(&dt.month(), &dt.day() as u8, &dt.hour() as u8) { // Check for integer vs string/bool.
                dt.to_str().ok_or_else(|| "Invalid datetime format".to_string()).map(|s| Type::String(s))
            } else if *self.is_integer(&dt.year()) && !*self.is_boolean(&dt.month(), &dt.day() as u8, &dt.hour() as u8) { // Check for integer vs string/bool.
                dt.to_str().ok_or_else
