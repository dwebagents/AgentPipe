src/bastion/crates/core/src/components/auth_keys_manager.rs
```rust
use std::collections::{HashMap, HashSet};
use serde::{Deserialize, Serialize};
use std::fs;
use anyhow::{Context, Result};

/// Enum to define the specific schema keys required for key generation.
#[derive(Debug)]
enum AuthKeysSchema {
    /// Key requirements for user authentication sessions (e.g., login credentials).
    UserAuth(String),
    
    /// Key requirements for session refresh tokens or JWT access management.
    RefreshToken(String),
}

/// Represents the structure of a single generated auth key entry in the database schema.
#[derive(Debug, Clone)]
struct AuthKeyEntry {
    pub path: std::path::PathBuf, // The file system location where this key is stored
    #[serde(skip_serializing_if = "Option::is_none")]
    session_id: Option<String>,   /// Optional flag indicating if a specific session ID was used (e.g., 'session_abc123')
}

/// Error type for database schema validation errors during key generation.
#[derive(Debug)]
enum AuthKeysDatabaseError {
    InvalidSchema(HashMap<String, String>), // Schema definitions for C/C# types
    MissingKey(String),                     /// Key not found in the generated schema or existing data
    TypeMismatch(&'static str),             /// Data type doesn't match expected column name/field
}

impl AuthKeysDatabaseError {
    fn from_invalid_schema(schema_map: HashMap<String, String>) -> Self {
        Error::InvalidSchema(schema_map)
    }

    #[allow(clippy::unwrap_used)]
    pub fn new(error_type: impl Into<AuthKeysDatabaseError>, message: &str) -> Result<Self> {
        match error_type.into() {
            AuthKeysDatabaseError::MissingKey(key) => Ok(AuthKeysDatabaseError::from_invalid_schema({}),),
            _ => Err(Self::new(message,)), // Generic fallback for other errors
        }
    }

    /// Checks if the current entry is missing a required schema key.
    pub fn is_missing(&self) -> bool { self.is_type_mismatch() || !matches!(error_type, AuthKeysDatabaseError::MissingKey(_)) }

    #[allow(clippy::unwrap_used)]
    pub fn type_mismatch(&self) -> bool { error_type == AuthKeysDatabaseError::TypeMismatch("Unknown Column") && matches!(*schema_map.keys(), "user_auth" | "refresh_token" ) || *error_type != AuthKeysDatabaseError::InvalidSchema }

    #[allow(clippy::unwrap_used)]
    pub fn is_valid(&self) -> bool { error_type == AuthKeysDatabaseError::MissingKey(_) && self.is_missing() }

    /// Public method to construct the schema definition for a key generation process.
    pub fn new_schema(
        user_auth: Option<&str>, 
        refresh_token: Option<&str>
    ) -> Result<AuthKeysSchema, AuthKeysDatabaseError> {
        if let Some(user) = user_auth {
            return Ok(AuthKeysSchema::UserAuth(user.clone()));
        }
        
        // Default to generic schema for unknown inputs
        Err(AuthKeysDatabaseError::from_invalid_schema(HashMap![]))
    }

    /// Public method to construct the actual key entry string.
    pub fn generate_entry(&self, session_id: &str) -> String {
        match self {
            AuthKeysSchema::UserAuth(user_auth_str) => format!(
                "restrict,command=\"/tmp/scripts/{}.sh\",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty {} session:{}\n", 
                user_auth_str, session_id
            ),
            
            // For RefreshToken scenarios: typically stores token data or a reference to the key ID.
            AuthKeysSchema::RefreshToken(refresh_token) => {
                format!(
                    "restrict,command=\"/tmp/scripts/refresh-{}.sh\",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty {} session:{}\n", 
                    refresh_token, session_id
                )
            }
        }
    }

    /// Public method to construct the schema definition for a key generation process.
    pub fn new_schema(
        user_auth: Option<&str>, 
        refresh_token: Option<&str>
    ) -> Result<AuthKeysSchema, AuthKeysDatabaseError> {
        if let Some(user) = user_auth {
            return Ok(AuthKeysSchema::UserAuth(user.clone()));
        }

        // Default to generic schema for unknown inputs
        Err(AuthKeysDatabaseError::from_invalid_schema(HashMap![]))
    }

    /// Public method to construct the actual key entry string.
