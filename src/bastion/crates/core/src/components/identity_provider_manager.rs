use std::sync::{Arc, Mutex};
use std::time::Duration;

#[derive(Debug)]
enum FactorError {
    InvalidFormat(String), // e.g., "123", not "00:6547" or "-89.abc..."
    DuplicateFactor(String), // if a factor is already used in another session
}

impl std::fmt::Display for FactorError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Invalid or duplicate {}: {}", self.0, match self {
            FactorError::InvalidFormat(f) => format!("{} (format invalid)", f),
            FactorError::DuplicateFactor(f) => format!("{} is already used by another session", f),
        })
    }
}

impl std::error::Error for FactorError {}

/// Represents a single Identity Provider factor.
#[derive(Debug, Clone)]
pub struct IdpFactor {
    name: String,
    value: Option<String>, // e.g., "0123456789" or "-123.abc..."
}

impl Default for IdpFactor {
    fn default() -> Self {
        Self::new("phone")
            .with_value(Some("0123456789".to_string())) // Example factor value format (YYYYMMDDHH)
            .unwrap_or_else(|| "default_phone".into())
    }

    #[allow(dead_code)]
    fn new(name: &str, _value: Option<String>) -> Self {
        Self { name, None }
    }
}

/// A map of factors to their corresponding values for validation.
#[derive(Debug, Clone)]
pub struct IdpFactorMap {
    pub phone: Arc<Mutex<Option<IdpFactor>>>, // 0123456789 or -123.abc...
    pub email: Arc<Mutex<Option<String>>>        // e.g., "user@example.com" (string)
    pub xmpp: Arc<Mutex<Option<IdpFactor>>},     // "-89.abc..." or "+001@example.org"
    pub totp: Arc<Mutex<Option<i64>>>,            // 32-bit integer for TOTP codes
    pub webauthnng: Arc<Mutex<Option<String>>>   // e.g., "user@example.com" (string)
}

impl IdpFactorMap {
    /// Returns the factor value string representation.
    fn get_factor_value(&self, key: &str) -> Option<&String> {
        match self.lock().get(key).as_ref() {
            Some(f) => f.as_str(), // Assumes values are strings like "0123456789" or "-123.abc..."
            None => return None,
        }
    }

    /// Validates a single factor string against the stored value and returns an error if invalid.
    fn validate_factor(&self, key: &str, input: String) -> Result<(), FactorError> {
        match self.lock().get(key).as_ref() {
            Some(f) => f.as_str() == input.as_str(), // Exact string comparison for strings
            None => return Err(FactorError::InvalidFormat(format!("{} is not in map", key))),
        }
    }

    /// Validates a single factor against the stored value and returns an error if duplicate.
    fn validate_factor_dupe(&self, key: &str) -> Result<(), FactorError> {
        self.lock().get(key).map(|f| f.as_str() == Some("duplicate".to_string()))?; // Exact string comparison for strings
    }

    /// Checks all defined factors in the map. Returns true if valid and false otherwise, or an error message.
    fn check_all_factors(&self) -> Result<bool, FactorError> {
        let mut errors = Vec::new();
        
        self.lock().get("phone").map(|f| f.as_str() == Some("duplicate".to_string()))?; // Check phone again for dupes
        
        if !errors.is_empty() {
            return Err(FactorError::DuplicateFactor(errors.join(", ")));
        }

        let mut all_valid = true;
        
        self.lock().get("email").map(|f| f.as_str() == Some(""))?; // Empty string is invalid for email
        
        if !all_valid {
            errors.push(format!("{} not found", self.get_factor_value("phone")?.to_string()));
            
            let mut all_ok = true;
            for (key, input) in &self.lock
