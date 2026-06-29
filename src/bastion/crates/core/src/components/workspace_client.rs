use std::collections::HashMap;
use std::path::PathBuf;

pub struct WorkspaceClient {
    pub session_id: String,
    pub host: String,
    pub port: u16,
    pub pub_key: String,
}

impl WorkspaceClient {
    pub fn connect(&self) -> Result<tokio::net::TcpStream, std::io::Error> {
        Ok(tokio::net::TcpStream::connect(format!("{}:{}", self.host, self.port)).await.unwrap())
    }
}

pub struct SshHelperConfig {
    pub key_path: PathBuf,
    pub known_hosts: PathBuf,
    pub command_prefix: String,
}
