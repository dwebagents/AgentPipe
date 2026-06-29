use std::collections::HashMap;
use std::time::{Duration, SystemTime};

#[derive(Debug, Clone)]
pub struct ForcedCommand {
    pub command: String,
    pub args: Vec<String>,
    pub allowed_script_hash: String,
    pub session_id: String,
}

pub struct ForcedCommandConfig {
    inner: ForcedCommand,
}

impl ForcedCommandConfig {
    pub fn new(command: String, args: Vec<String>, session_id: String) -> Self {
        let allowed_script_hash = format!("sha256:{}", uuid::Uuid::new_v4());
        Self {
            inner: ForcedCommand {
                command,
                args,
                allowed_script_hash,
                session_id,
            },
        }
    }

    pub fn to_ssh_authorized_keys_entry(&self, public_key: &str) -> String {
        format!(
            "restrict,command=\"{}\",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty {} # plan:{}",
            self.inner.command,
            public_key,
            self.inner.session_id
        )
    }

    pub fn validate(&self, requested_command: &str) -> bool {
        self.inner.command == requested_command
    }
}
