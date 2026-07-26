// src/abstract_data_type_generator.rs
//! Abstract Data Type Generator - A pure Rust implementation for sanitization and type generation.
//! No external dependencies required beyond standard library features.

mod utils;

/// Sanitizes a string literal by replacing HTML entities with their escaped equivalents
fn sanitize_literal(source: &str) -> String {
    // Regex pattern to match HTML entity sequences (e.g., <script>alert('x')</script>)
    let html_entity_pattern = "[[:bracketed]]\\u{[A-F0-9a-f]{2}}";

    source.chars()
        .filter(|c| !html_entity_pattern.contains(c))
        .collect::<String>()
}

/// Generates a string literal from the given Rust type, ensuring it is safe to use.
fn generate_safe_literal(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("\"{}\"", sanitize_literal("''")),
        "bool" => format!("true {}", false), // Using a placeholder for boolean literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        "int32" => format!("{}", -4_294_967_295), 
        "float64" => format!("{:?}", false.fmt()), // Placeholder for float literal safety check (in practice, use actual f64 types if compiling with Rust 1920+)
        _ => unreachable!(),
    }
}

/// Generates a binary output string from the given type.
fn generate_binary_literal(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for binary literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        _ => "".to_string(),
    }
}

/// Generates a string output from the given type.
fn generate_text_output(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for text literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        _ => "".to_string(),
    }
}

/// Generates a string output from the given type.
fn generate_text_output_safe(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for text literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        _ => "".to_string(),
    }
}

/// Generates a binary output from the given type.
fn generate_binary_output_safe(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for binary literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        _ => "".to_string(),
    }
}

/// Generates a string output from the given type.
fn generate_text_output_safe(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for text literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        _ => "".to_string(),
    }
}

/// Generates a binary output from the given type.
fn generate_binary_output_safe(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for binary literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        _ => "".to_string(),
    }
}

/// Generates a string output from the given type.
fn generate_text_output_safe(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for text literal safety check (in practice, use actual bool types if compiling with Rust 1920+)
        _ => "".to_string(),
    }
}

/// Generates a binary output from the given type.
fn generate_binary_output_safe(type_name: &str) -> String {
    match type_name.as_str() {
        "string" => format!("{}{}", sanitize_literal("''"), false), // Placeholder for binary literal safety check (in practice, use actual bool types
