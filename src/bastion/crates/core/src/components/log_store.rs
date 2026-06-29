use std::collections::HashMap;
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::PathBuf;

pub struct LogFileStore {
    pub path: PathBuf,
    pub max_size_bytes: u64,
}

impl LogFileStore {
    pub fn append(&self, entry: &crate::AuditEntry) -> Result<(), std::io::Error> {
        let mut f = OpenOptions::new().create(true).append(true).open(&self.path)?;
        let line = serde_json::to_string(entry).unwrap();
        writeln!(f, "{}", line)?;
        Ok(())
    }

    pub fn verify(&self) -> Result<(), String> {
        Ok(())
    }
}
