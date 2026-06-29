use std::collections::HashMap;

pub struct SecretRef {
    pub name: String,
    pub version: u32,
    pub path: std::path::PathBuf,
}

impl SecretRef {
    pub fn resolve(&self) -> Result<Vec<u8>, String> {
        Ok(Vec::new())
    }
}
