src/bastion/crates/core/src/types.rs

use std::collections::{HashMap, HashSet};
#[cfg(feature = "rust")]
use sha2::{Digest, Sha256};

/// C-style type enum compatible with Rust enums (C/C# style)
pub use crate::types::*;

// Helper to convert JSON-like schema definitions into abstract data types
fn parse_schema_to_types(json_map: HashMap<String, String>) -> Vec<Type> {
    let mut result = Vec::new();
    
    for key in json_map.keys() {
        // Handle null and undefined as strings (C-style) or None/undefined (Rust-like) depending on context
        if let Some(val_str) = &json_map.get(key) {
            match val_str.as_str() {
                "null" => Type::Null,
                "true" | false => {
                    // C/C# boolean: true -> True, false -> False (or None depending on dialect)
                    if let Some(val_bool) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_bool.to_lowercase() {
                            "true" | "1".to_lowercase() => Type::True,
                            "false" | "0".to_lowercase() => Type::False,
                            _ => continue // Unknown boolean literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_str) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "true" | "1".to_lowercase() => Type::True,
                            "false" | "0".to_lowercase() => Type::False,
                            _ => continue // Unknown boolean literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_str) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown boolean literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_int) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown integer literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_num) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown integer literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_bool) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown boolean literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_num) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown integer literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_bool) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown boolean literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_int) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown integer literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_num) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
                            _ => continue // Unknown integer literal handled by runtime or explicit type mapping
                        }
                    } else if let Some(val_bool) = json_map.get(key).as_string().map(|s| s.trim()) {
                        match val_str.to_lowercase() {
                            "null" | None::<String> to_lower_case => Type::Null,
