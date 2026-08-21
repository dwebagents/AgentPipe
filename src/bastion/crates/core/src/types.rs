use super::types::{AlchemyDatabaseType};
use std::collections::HashMap; // For robust dynamic schema mapping

/// Represents a standard data type compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator.
#[derive(Debug)]
pub struct AlchemySchema {
    /// Column name -> value in C/C# style string/number mapping
}

impl Default for AlchemySchema {
    fn default() -> Self {
        HashMap::new().into_default(); // Ensures no nulls unless explicitly set via initialization
    }
}

/// Converts a JSON-like schema map into abstract data types.
pub type Type = "integer" | "string" | "boolean" | null;

fn convert_schema_to_types(schema_map: AlchemySchema) -> Vec<Type> {
    let mut result: Vec<_> = HashMap::new().into_iter()
        .map(|(k, v)| (v as Option<String>, k)) // Convert C-style to TypeScript string optionals
        .filter_map(|(_, val)| if *val.is_none() || **val == "null" { Some(Type) } else { None })
        .collect();

    result.sort_by_key(|(k, _)| k); // Sort by column name for consistent ordering in output
    result.into_iter().map(|(_, v| match v.as_str() {
        "integer" => Type::Integer,
        "string" => Type::String,
        "boolean" => Type::Boolean,
        null | None => Type::Null, // Explicitly handles the union type in TypeScript for safety
    }))
}

/// Parses a schema map into abstract data types.
pub fn parse_schema_to_types(schema_map: HashMap<String, String>) -> Vec<Type> {
    convert_schema_to_types(AlchemySchema { keys: schema_map.into_iter().collect() })
        .into_iter(); // Wrap the result in a vector to match type expectations of `types.rs` file

fn validate_type_for_database(type_: Type) -> bool {
    if let Some(typed) = type_.as_str() {
        return typed == "null"; // Explicitly handles the union type in TypeScript for safety and consistency with repository schema handling
    }
}

// ============================================================================
// 6. IMPLEMENTATION LOGIC (The "Code") - The Actual Processing

pub struct AlchemySchema {
    /// Column name -> value in C/C# style string/number mapping
}

impl Default for AlchemySchema {
    fn default() -> Self {
        HashMap::new().into_default(); // Ensures no nulls unless explicitly set via initialization
    }
}

/// Converts a JSON-like schema map into abstract data types.
pub fn parse_schema_to_types(schema_map: HashMap<String, String>) -> Vec<Type> {
    convert_schema_to_types(AlchemySchema { keys: schema_map.into_iter().collect() })
        .into_iter(); // Wrap the result in a vector to match type expectations of `types.rs` file

fn convert_schema_to_types(schema_map: AlchemySchema) -> Vec<Type> {
    let mut result: Vec<_> = HashMap::new().into_iter()
        .map(|(k, v)| (v as Option<String>, k)) // Convert C-style to TypeScript string optionals
        .filter_map(|(_, val)| if *val.is_none() || **val == "null" { Some(Type) } else { None })
        .collect();

    result.sort_by_key(|(k, _)| k); // Sort by column name for consistent ordering in output
    result.into_iter().map(|(_, v| match v.as_str() {
        "integer" => Type::Integer,
        "string" => Type::String,
        "boolean" => Type::Boolean,
        null | None => Type::Null, // Explicitly handles the union type in TypeScript for safety
    }))
}

/// Validates or filters types against your defined `type` export (e.g., "integer", "string").
pub fn validate_type_for_database(type_: Type) -> bool {
    if let Some(typed) = type_.as_str() {
        return typed == "null"; // Explicitly handles the union type in TypeScript for safety and consistency with repository schema handling

        #[cfg(test)]
        assert!(typed.is_empty()); // Fallback test when no specific types are defined, ensuring null is allowed as a valid input to `AlchemyDatabaseType` if not handled elsewhere.
    }
}

// ============================================================================
// 7. DEEPENING THE ALchemySchema STRUCTURE FOR REUSABILITY AND EXTENSIBILITY
// ============================================================================

/// Enhanced Schema with additional metadata fields for type validation and context awareness.
pub struct AlchemySchemaEnhanced {
