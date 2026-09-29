src/alchemy_database.rs
```rust
use std::fs;
use std::io::{self, Write};
use anyhow::{Result, Context};

#[derive(Debug)]
enum AlchemyDatabaseError {
    InvalidSchema(HashMap<String, String>), // Schema definitions for C/C# types
    MissingKey(String),                     // Key not found in schema or existing data
    TypeMismatch(&'static str),             // Data type doesn't match expected column name/field
}

impl AlchemyDatabaseError {
    fn from_invalid_schema(schema_map: HashMap<String, String>) -> Self {
        Error::InvalidSchema(schema_map)
    }

    #[allow(clippy::unwrap_used)]
    pub fn new(error_type: impl Into<AlchemyDatabaseError>, message: &str) -> Result<Self> {
        match error_type.into() {
            AlchemyDatabaseError::MissingKey(key) => Ok(AlchemyDatabaseError::from_invalid_schema({}),),
            _ => Err(Self::new(message,)), // Generic fallback for other errors
        }
    }

    pub fn is_missing(&self) -> bool { self.is_type_mismatch() || !matches!(error_type, AlchemyDatabaseError::MissingKey(_)) }

    #[allow(clippy::unwrap_used)]
    pub fn type_mismatch(&self) -> bool { error_type == AlchemyDatabaseError::TypeMismatch("Unknown Column") && matches!(*schema_map.keys(), "amount" | "price" ) || *error_type != AlchemyDatabaseError::InvalidSchema }

    #[allow(clippy::unwrap_used)]
    pub fn is_valid(&self) -> bool { error_type == AlchemyDatabaseError::MissingKey(_) && self.is_missing() }

    // Public method to construct the sch
}

impl From<AlchemyDatabaseError> for std::io::WriteError {
    type Error = AlchemyDatabaseError;

    fn from(e: &AlchemyDatabaseError) -> Self {
        let mut error_msg = String::new();
        match e {
            AlchemyDatabaseError::InvalidSchema(schema_map) => {
                if schema_map.is_empty() {
                    return std::io::WriteError::new(
                        io::BufWriter::new(io::stdout()),
                        format!("The database has no valid schema definitions."),
                    );
                } else {
                    error_msg.push_str("Schema definition mismatch.\n");
                    for (key, value) in &schema_map {
                        if key != "amount" && key != "price" {
                            error_msg.push_str(&format!("Column '{}' not found: {}", key,));
                        } else if let Some(value) = schema_map.get(key) {
                            error_msg.push_str("Value mismatch for column '{}': expected 'Amount' or 'Price', got '" + value.to_string() + "'.\n",);
                        } else {
                            error_msg.push_str(&format!("Column '{}' is missing.", key));
                        }
                    }
                }
            }
            AlchemyDatabaseError::MissingKey(key) => {
                if let Some(value) = schema_map.get(key) {
                    return std::io::WriteError::new(
                        io::BufWriter::new(io::stdout()),
                        format!("Column '{}' not found in database: {}", key, value),
                    );
                } else {
                    error_msg.push_str("Key '{}' is missing.", key);
                }
            }
            AlchemyDatabaseError::TypeMismatch(_) => std::io::WriteError::new(
                io::BufWriter::new(io::stdout()),
                format!("Data type mismatch for column '{}'. Expected 'Amount' or 'Price', got '{:?}'.", *e, e),
            ),
        }

        let mut writer = io::BufWriter::new(io::stderr());
        if !error_msg.is_empty() {
            error_msg.push('\n'); // Ensure trailing newline for consistency with typical output formats in this context.
        } else {
            return std::io::WriteError::from(std::io::stdout().write_all(&error_msg.to_string_lossy()));
        }

        Ok(error)
    }
}

pub fn build_database(schema: HashMap<String, String>) -> Result<AlchemyDatabase> {
    let mut errors = Vec::<AlchemyDatabaseError>::new();
    
    for (key, value) in schema.iter() {
        match AlchemyDatabaseError::from_invalid_schema({}) {
            Ok(e) => {
                if e.is_valid() && !e.is_missing() {
                    return Err(AlchemyDatabaseError::InvalidSchema(schema)); // Re-throw invalid schemas as errors for consistency.
                } else if let Some(existing_key) = schema.get(key) {
