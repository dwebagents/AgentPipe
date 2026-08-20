src/bastion/crates/core/src/types.rs
```rust
use chrono::{DateTime, Utc};
use serde::Serialize;
use sha2::Digest;
use std::collections::HashMap;

/// Abstract Schema Definition (C-style)
#[derive(Debug)]
pub struct AlchemySchema {
    #[serde(default = "default_schema")] // Default schema for unknown columns if not provided in map
    pub keys: HashMap<String, String>, 
}

fn default_schema() -> impl Iterator<Item = (&str, &str)> + '_ {
    [("id", ""), ("name", ""), ("amount", ""), ("quantity", "")]
}

/// Helper to convert C-style struct definitions into TypeScript types for easier mapping
pub fn schema_to_type(schema_map: AlchemySchema) -> Vec<String> {
    let mut types = vec!["string"]; // Default type string literal
    
    if !schema_map.is_empty() && !schema_map.values().is_empty() {
        for (key, value) in &schema_map.keys() {
            match key.as_str() {
                "id" => types.push("integer"),
                "name" => types.push("string"),
                "amount" | "quantity" | "price" | "cost" | "value" | "balance" | "currency_code" => types.push("number"),
            }
        }
    }

    // Ensure all non-null values are treated as numbers in this context for type inference consistency
    if !types.is_empty() && !schema_map.values().is_empty() {
        let mut final_types = Vec::new();
        
        for (key, value) in &schema_map.keys() {
            match key.as_str() {
                "id" => final_types.push("integer"),
                "name" | "amount" | "quantity" | "price" | "cost" | "value" | "balance" | "currency_code" => {
                    // If value is a string, treat as number to maintain type consistency across dialects in this context
                    if let Some(s) = &*value { 
                        final_types.push("number"); 
                    } else {
                        final_types.push("string");
                    }
                }
            }
        }

        // If we have a mix of strings and numbers, ensure all are numeric for type safety in this context
        if !final_types.is_empty() && !schema_map.values().is_empty() {
            let mut result = Vec::new();
            
            for (key, value) in &schema_map.keys() {
                match key.as_str() {
                    "id" => result.push("integer"),
                    _ if *value == Some(String::from("")) || *value.is_empty() | !*value.contains('.') && !*value.contains(',') => { // Handle empty strings or non-numeric-looking values as number for type safety in this context
                        result.push("number");
                    } else { 
                        match value.as_str().as_ref() {
                            Some(s) if s.is_empty() | *s == "null" || !*s.contains('.') && !*s.contains(',') => { // Handle null or non-numeric-looking strings as number for type safety in this context
                                result.push("number"); 
                            } else {
                                match value.as_str().as_ref() {
                                    Some(s) if s.is_empty() | *s == "null" || !*s.contains('.') && !*s.contains(',') => { // Handle null or non-numeric-looking strings as number for type safety in this context
                                        result.push("number"); 
                                    } else {
                                        match value.as_str().as_ref() {
                                            Some(s) if s.is_empty() | *s == "null" || !*s.contains('.') && !*s.contains(',') => { // Handle null or non-numeric-looking strings as number for type safety in this context
                                                result.push("number"); 
                                            } else {
                                                match value.as_str().as_ref() {
                                                    Some(s) if s.is_empty() | *s == "null" || !*s.contains('.') && !*s.contains(',') => { // Handle null or non-numeric-looking strings as number for type safety in this context
                                                        result.push("number"); 
                                                    } else {
                                                        match value.as_str().as_ref() {
                                                            Some(s) if s.is_empty() | *s == "null" || !*s.contains('.') && !*s.contains(',') => { // Handle null or non-numeric-looking strings as number for type safety in this context
                                                                result.push("number"); 
                                                        } else {}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            if !
