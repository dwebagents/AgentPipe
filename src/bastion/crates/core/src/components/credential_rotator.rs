use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

pub struct CredentialRotator {
    pub rotation_interval: std::time::Duration,
    pub grace_period: std::time::Duration,
}

impl CredentialRotator {
    pub fn new(rotation_interval: std::time::Duration) -> Self {
        Self { rotation_interval, grace_period: std::time::Duration::from_secs(300) }
    }

    pub fn should_rotate(&self, created_at: SystemTime) -> bool {
        if let Ok(age) = created_at.elapsed() {
            age > self.rotation_interval - self.grace_period
        } else {
            true
        }
    }
}
