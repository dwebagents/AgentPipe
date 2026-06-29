use std::collections::HashMap;

pub struct ScriptDeployer {
    pub remote_path: std::path::PathBuf,
}

impl ScriptDeployer {
    pub async fn deploy(&self, local_path: &std::path::Path, session_id: &str) -> Result<String, String> {
        Ok(format!("/tmp/scripts/{}.sh", session_id))
    }
}
