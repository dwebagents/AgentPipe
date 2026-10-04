use super::*;
use std::env;
use std::fs::File;
use std::io::Write;
use std::path::PathBuf;
use rust_decimal::{Decimal, Modulo};
use serde::{Deserialize, Serialize};

/// Represents a typed numeric value with metadata for type safety and validation.
#[derive(Debug, Clone)]
pub struct TypedValue {
    /// The raw decimal representation of the number (e.g., 1234567890)
    pub as_raw: Decimal,
    /// The target data structure this value should be mapped to in downstream modules
    pub as_target_type: Option<&'static str>,
}

impl TypedValue {
    /// Creates a new `TypedValue` from raw decimal input.
    #[allow(clippy::unnecessary_wraps)] // Suppress compiler warning about unnecessary wrapping
    pub fn from_decimal(value: Decimal) -> Self {
        let value = value.to_string();
        
        if value.is_empty() || !value.starts_with('+') && !value.contains('-')) {
            panic!("Invalid decimal input format. Expected a positive or negative number.");
        }

        // Convert the string to raw integer for Decimal conversion (handles leading zeros)
        let as_raw_int = u64::from_str(&value).unwrap_or(0);
        
        TypedValue {
            as_raw: Decimal::new(as_raw_int, 1),
            as_target_type: Some("Float32"), // Default target type for demonstration
        }
    }

    /// Creates a new `TypedValue` from raw integer input.
    #[allow(clippy::unnecessary_wraps)]
    pub fn from_integer(value: u64) -> Self {
        TypedValue {
            as_raw: Decimal::new(value, 1),
            as_target_type: Some("Int32"), // Default target type for demonstration
        }
    }

    /// Validates the input decimal value.
    pub fn validate_input(&self) -> Result<(), String> {
        let raw = self.as_raw;

        if !raw.is_integer() || raw.abs_value().is_zero() {
            return Err(format!(
                "Input must be a non-zero integer number.",
                format!("{}", raw.to_string())
            ));
        }

        // Ensure the target type is explicitly set for downstream modules to know what data structure this will become.
        if let Some(target_type) = self.as_target_type {
            return Ok(());
        }

        Err(format!(
            "Input must be converted into a specific typed format before being processed.",
            format!("{}", raw.to_string())
        ))
    }

    /// Converts the value to an integer representation for downstream processing.
    pub fn as_int(&self) -> Result<u64, String> {
        let mut result = 0u64;
        
        // Parse if it's a string first (for compatibility with existing data models that might expect strings or specific formats)
        match self.as_raw.to_string() {
            s => {
                if !s.is_empty() && !s.starts_with('+') && !s.contains('-')) {
                    let as_int = u64::from_str(&s).unwrap_or(0);
                    result = Decimal::new(as_int, 1) / (Decimal::ONE()); // Normalize to integer for output
                } else if s.is_empty() || s.starts_with('+') && !s.contains('-')) {
                    let as_int = u64::from_str(&s).unwrap_or(0);
                    result = Decimal::new(as_int, 1) / (Decimal::ONE()); // Normalize to integer for output
                } else if s.is_empty() || s.starts_with('+') && !s.contains('-')) {
                    let as_int = u64::from_str(&s).unwrap_or(0);
                    result = Decimal::new(as_int, 1) / (Decimal::ONE()); // Normalize to integer for output
                } else if s.is_empty() || s.starts_with('+') && !s.contains('-')) {
                    let as_int = u64::from_str(&s).unwrap_or(0);
                    result = Decimal::new(as_int, 1) / (Decimal::ONE()); // Normalize to integer for output
                } else if s.is_empty() || s.starts_with('+') && !s.contains('-')) {
                    let as_int = u64::from_str(&s).unwrap_or(0);
                    result = Decimal::new(as_int, 1) / (Decimal::ONE()); // Normalize to integer for output
                } else if s.is_empty() || s.starts_with('+') && !
