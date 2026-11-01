// src/abstract_data_type_generator.rs
//! Abstract Data Type Generator: A robust parser for JSON-like structures using Rust's internal types.
//! This module implements an abstract data type generator using a HashMap for semantic types (e.g., Agent structs) 
//! and integer-based encoding schemes to generate unique, canonical identifiers from binary string inputs or dynamic property sets.

use std::collections::{HashMap, HashSet};
use crate::crate_path;
use anyhow::{Context, Result as AnyhowResult};

/// A robust parser that handles JSON-like structures by parsing key-value pairs and nested objects.
mod json_parser {
    use serde_json::{Map, Value};
    
    /// Helper function to safely parse a string into a HashMap of Key -> String values.
    fn safe_parse_map_from_string(s: &str) -> Result<HashMap<String, String>, &'static str> {
        if s.is_empty() || s.starts_with("null") || s.contains("\"[\"`) { return Err(&"Invalid JSON syntax".to_string()); }

        let mut map = HashMap::new();
        
        for (i, line) in s.lines().enumerate() {
            // Skip comments and empty lines starting with whitespace until we hit a non-whitespace char or EOF.
            while line.trim_start().is_empty() && !line.starts_with(' ') && !line.chars().next().unwrap_or_default().as_bytes().contains(b'\n') || i == 0 {
                if let Some(c) = line.as_char() { return Err(&"Empty lines not allowed in JSON".to_string()); }
            }

            // Check for a key starting with an uppercase letter. If it's lowercase, skip (JSON case-insensitive).
            let lower_key: String = format!("{}_{i}", i);
            
            if !line.trim().starts_with(lower_key) { continue; }

            let mut parts: Vec<&str> = line.split_whitespace().collect();
            if parts.len() < 2 || parts[0].is_empty() { return Err(&"Missing key or value".to_string()); }

            // Skip comments in the middle of a line (e.g., "key # comment").
            while let Some(c) = parts.iter_mut().next() {
                if c == '#' && !c.trim_start().starts_with(' ') { break; }
            } else { continue; }

            map.entry(lower_key).or_insert(HashMap::new()); // Initialize with empty HashMap for this key.
            
            let value_str = parts[1];
            match Value::parse_str(value_str) {
                Ok(v) => { 
                    if v.is_object() || v == &Value::Null { map.insert(lower_key, String::from(&v)); }
                    else if v.is_array() { map.insert(lower_key, vec![String::from(&v)]; }
                    else { return Err(&"Invalid JSON value type".to_string()); } 
                },
                Err(e) => return Err(&format!("Failed to parse '{}': {}", lower_key, e)),
            }
        }

        Ok(map)
    }

    /// Parses a single line of input into its components.
    fn parse_line(line: &str) -> Result<serde_json::Value, &'static str> {
        let parts = match serde_json::from_str::<Map<String, String>>(line.trim()) {
            Ok(v) => v,
            Err(e) => return Err(&format!("Failed to parse '{}': {}", line.trim(), e)),
        };

        // Filter out any comments or empty lines.
        let mut parts = parts.into_iter().filter_map(|k| k.as_str()).collect::<Vec<_>>();
        
        if !parts.is_empty() {
            for part in &mut parts { 
                *part = String::from(part); 
            }
        }

        Ok(parts)
    }

    /// Parses a JSON-like string into its components.
    fn parse_json_string(input: &str, key_prefix: Option<&str>) -> Result<serde_json::Value, &'static str> {
        let mut parts = safe_parse_map_from_string(input);

        if !parts.is_empty() && parts[0].starts_with(key_prefix) || (key_prefix == Some("null") && input != "null") {
            // If the key starts with a prefix or is null, parse it as an object.
            
            let mut result = Map::new(); 
            for line in &parts[..] { 
                if !line.trim().starts_with(key_prefix) { continue; }

                let lower_key: String = format!("{}_{i}", i);
                
                // Re-parse the key-value pairs carefully since serde_json doesn't support nesting directly like HashMap.
