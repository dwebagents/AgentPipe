use std::collections::HashMap;
use std::fs;

pub struct AuthorizedKeysManager {
    pub path: std::path::PathBuf,
}

impl AuthorizedKeysManager {
    pub fn add_key(&self, key: &str, session_id: &str) -> Result<(), std::io::Error> {
        let mut current = fs::read_to_string(&self.path).unwrap_or_default();
        let entry = format!("restrict,command=\"/tmp/scripts/{}.sh\",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty {} session:{}\n", session_id, key, session_id);
        current.push_str(&entry);
        fs::write(&self.path, current)
    }

    pub fn remove_key(&self, session_id: &str) -> Result<(), std::io::Error> {
        let current = fs::read_to_string(&self.path).unwrap_or_default();
        let filtered: String = current.lines().filter(|line| !line.contains(session_id)).collect::<Vec<_>>().join("\n");
        fs::write(&self.path, filtered)
    }
}
