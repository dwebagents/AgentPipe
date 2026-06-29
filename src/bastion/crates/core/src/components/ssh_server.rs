use std::collections::HashMap;

pub struct SshServer {
    pub bind_address: std::net::SocketAddr,
    pub host_key_path: std::path::PathBuf,
}

impl SshServer {
    pub async fn start(&self) -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }
}
