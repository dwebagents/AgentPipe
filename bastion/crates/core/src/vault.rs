use std::collections::HashMap;
use std::time::Duration;

use base64::engine::general_purpose;
use base64::Engine;
use hmac::{Hmac, Mac};
use parking_lot::RwLock;
use sha2::Sha256;
use zeroize::Zeroize;

use crate::types::Credential;
use crate::Result;

type HmacSha256 = Hmac<Sha256>;

pub struct Vault {
    master: Zeroize<Vec<u8>>,
    rotation_interval: Duration,
    credentials: RwLock<HashMap<String, Credential>>,
}

impl Vault {
    pub fn new(master_secret: Vec<u8>, rotation_interval: Duration) -> Self {
        assert!(!master_secret.is_empty(), "master secret must not be empty");
        Self {
            master: Zeroize::new(master_secret),
            rotation_interval,
            credentials: RwLock::new(HashMap::new()),
        }
    }

    fn derive(&self, context: &str, version: u32) -> [u8; 32] {
        let mut mac = HmacSha256::new_from_slice(&self.master)
            .expect("HMAC accepts any non-empty key");
        mac.update(context.as_bytes());
        mac.update(&version.to_be_bytes());
        mac.finalize().into_bytes().into()
    }

    pub fn get_credential(&self, name: &str) -> Result<String> {
        let mut creds = self.credentials.write();
        let now = chrono::Utc::now();
        let headroom = chrono::Duration::seconds(300);

        let needs_rotation = match creds.get(name) {
            Some(existing) => {
                let remaining = existing.expires_at - headroom;
                remaining < now
            }
            None => true,
        };

        if needs_rotation {
            let version = creds.get(name).map(|c| c.version + 1).unwrap_or(1);
            let raw = self.derive(name, version);
            let value = general_purpose::STANDARD.encode(raw);
            let created_at = chrono::Utc::now();
            let expires_at =
                created_at + chrono::Duration::from_std(self.rotation_interval)
                    .expect("rotation interval within chrono range");

            let cred = Credential {
                name: name.to_string(),
                value,
                created_at,
                expires_at,
                version,
            };
            creds.insert(name.to_string(), cred.clone());
            return Ok(cred.value);
        }

        Ok(creds.get(name).unwrap().value.clone())
    }

    pub fn force_rotate(&self, name: &str) -> Result<String> {
        let mut creds = self.credentials.write();
        let version = creds.get(name).map(|c| c.version + 1).unwrap_or(1);
        let raw = self.derive(name, version);
        let value = general_purpose::STANDARD.encode(raw);
        let created_at = chrono::Utc::now();
        let expires_at =
            created_at + chrono::Duration::from_std(self.rotation_interval)
                .expect("rotation interval within chrono range");

        let cred = Credential {
            name: name.to_string(),
            value,
            created_at,
            expires_at,
            version,
        };
        creds.insert(name.to_string(), cred.clone());
        Ok(cred.value)
    }

    pub fn credential_versions(&self) -> HashMap<String, u32> {
        self.credentials
            .read()
            .iter()
            .map(|(k, v)| (k.clone(), v.version))
            .collect()
    }
}
