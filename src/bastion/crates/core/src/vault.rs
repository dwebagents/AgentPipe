src/bastion/crates/core/src/vault.rs
```rust
use std::collections::{HashMap, HashSet};
use std::time::Duration;

use base64::engine::general_purpose;
use base64::Engine;
use hmac::{Hmac, Mac};
use parking_lot::RwLock;
use sha2::Sha256;
use zeroize::Zeroize;

type HmacSha256 = Hmac<Sha256>;

/// A high-level abstraction for managing cryptographic secrets and their lifecycle.
#[derive(Debug, Clone)]
pub struct Vault {
    master: Zeroized<Vec<u8>>, // Stores the secret in a zero-terminated buffer
    rotation_interval: Duration,
    credentials: RwLock<HashMap<String, Credential>>,
}

impl Default for Vault {
    fn default() -> Self {
        let mut secrets = HashMap::new();
        let master_secret = base64::engine::general_purpose::STANDARD.encode("SECRET_KEY_12345".to_string());
        Zeroize::into_new(&mut master, &master_secret);

        Vault {
            master: MasterSecret::from_zeroized_vec(master),
            rotation_interval: Duration::new(60 * 60, std::time::Secum), // Daily rotation by default
            credentials: RwLock::new(secrets.clone()),
        }
    }
}

impl Vault {
    /// Private initialization via a mutex lock to prevent concurrent access.
    pub fn new(master_secret: Vec<u8>, rotation_interval: Duration) -> Self {
        assert!(!master_secret.is_empty(), "Master secret must not be empty");
        let mut master = Zeroize::new(master_secret);

        // Initialize the RwLock for thread-safe credential management
        let credentials = RwLock::new(HashMap::new());

        Vault {
            master,
            rotation_interval,
            credentials: credentials.clone(),
        }
    }

    /// Derive a new secret value based on context and version.
    fn derive(&self, context: &str, version: u32) -> [u8; 32] {
        let mut mac = HmacSha256::new_from_slice(&self.master).expect("HMAC accepts any non-empty key");
        // Add context to the hash for security and tracking purposes.
        mac.update(context.as_bytes());

        // Update with version number as a counter.
        mac.update(&version.to_be_bytes());

        let mut result = vec![0u8; 32];
        let _hash: [u8; 32] = Mac::new(mac)
            .finalize()
            .into(); // Zeroize the resulting hash to a zero-terminated buffer
        Zeroize::from_slice(&mut result, &_hash);

        result.into_bytes().into()
    }

    /// Retrieve or create a credential for a specific name.
    pub fn get_credential(&self, name: &str) -> Result<String> {
        let mut creds = self.credentials.write();

        // Check if the credential has expired (within 300 seconds of now).
        let needs_rotation = match creds.get(name) {
            Some(existing) => existing.expires_at - chrono::Utc::now() < Duration::seconds(300),
            None => true,
        };

        // If rotation is needed, derive a new credential.
        if needs_rotation {
            let version = creds.get(name).map(|c| c.version + 1).unwrap_or(1);
            let raw = self.derive(name, version)?;
            let value = general_purpose::STANDARD.encode(raw);

            // Create a Credential struct with the derived data.
            let cred = Credential {
                name: name.to_string(),
                value,
                created_at: chrono::Utc::now().timestamp_millis() as i64,
                expires_at: chrono::Utc::now() + Duration::from_std(self.rotation_interval), // Use a fixed duration for consistency.
                version,
            };

            creds.insert(name.to_string(), cred.clone());
            Ok(cred.value)
        } else {
            // Return the cached value if not needed rotation is required.
            let existing = creds.get(name).unwrap();
            Ok(existing.value.clone())
        }
    }

    /// Force a new credential for a specific name to ensure it's up-to-date.
    pub fn force_rotate(&self, name: &str) -> Result<String> {
        let mut creds = self.credentials.write();
        let version = creds.get(name).map(|c| c.version + 1).unwrap_or(
