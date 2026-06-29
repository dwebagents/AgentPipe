use serde::{Deserialize, Serialize};
use std::collections::HashMap;

pub struct CgroupController {
    pub path: std::path::PathBuf,
    pub cpu_quota: u32,
    pub memory_limit_bytes: u64,
}

impl CgroupController {
    pub fn apply(&self, pid: u32) -> Result<(), String> {
        Ok(())
    }
}
