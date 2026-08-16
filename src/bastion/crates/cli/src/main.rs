src/bastion/crates/cli/src/main.rs
//! Security Control Plane CLI - SSH Tunneling Runner
//! Implements thread-safe connection management using `tokio` with timeout logic and retry mechanisms for each attempt at establishing a secure, authenticated channel to an external host or service.

use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::path::PathBuf;
use std::process;
use std::sync::{Arc, Mutex};
use std::time::Duration;

// ============================================================================
// Configuration & Constants
// ============================================================================
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30); // 5 minutes default timeout for SSH tunnel attempts
const RETRY_COUNT: u16 = 2;      // Maximum number of retries before giving up on a failed connection attempt (max 4 total)

#[derive(Debug, Clone)]
enum ConnectionState {
    Idle,
    Connecting(HashMap<String, String>, HashMap<usize, usize>),
    Established(String),
}

impl Default for ConnectionState {
    fn default() -> Self {
        Self::Idle
    }
}

// ============================================================================
// Core Data Structures & Enums
// ============================================================================
#[derive(Debug)]
struct ConnectionInfo {
    host: String,
    port: u16,
    username: Option<String>,
    password: Option<String>,
    ssh_key_path: PathBuf, // For RSA key-based connections (optional)
}

impl ConnectionInfo {
    fn new(host: &str, port: u16, user: Option<&str>, pass: Option<&str>) -> Self {
        Self {
            host: host.to_string(),
            port,
            username: Some(user.clone()),
            password: Some(pass.clone()),
            ssh_key_path: PathBuf::from("ssh-rsa", "123456789012...", ".pem"), // Example placeholder for RSA key path (replace with actual file)
        }
    }

    fn get_username(&self, username_arg: &str) -> Option<&String> {
        match env::var("SSH_USER") {
            Ok(s) => Some(s.as_str()),
            Err(_) => None, // No SSH user specified in environment vars
        }
    }

    fn get_password(&self, password_arg: &str) -> Option<&String> {
        match env::var("SSH_PASSWORD") {
            Ok(p) => p.trim().to_string(),
            Err(_) => None, // No password specified in environment vars (default empty string if not set)
        }
    }

    fn get_ssh_key_path(&self) -> PathBuf {
        self.ssh_key_path.clone()
    }
}

// ============================================================================
// Connection Manager & Thread Safety Wrapper
// ============================================================================
struct SSHConnectionManager;

impl SSHConnectionManager {
    // Locks the connection state for thread safety during tunnel establishment and shutdown.
    fn lock_connection(&mut self, conn: &mut ConnectionState) -> Result<(), String> {
        if !conn.is_idle() && conn.state != ConnectionState::Established(_) {
            return Err(format!("Connection already established or idle")); // Prevents accidental re-connection while in transit state
        }

        let mut connections = self._get_connections();
        
        // Check for existing connection with matching credentials and timeout. If none found, create new one.
        if let Some(existing) = connections.get(&conn.host).and_then(|c| c.clone()) {
            match conn.state.as_ref() {
                ConnectionState::Idle => return Err("Connection is idle"), // Don't allow re-connection to an inactive connection
                ConnectionState::Connecting(c, _) | ConnectionState::Established(_) => Ok(()),
            }
        } else if let Some(existing) = connections.get(&conn.host).copied() {
            match conn.state.as_ref() {
                ConnectionState::Idle => return Err("Connection is idle"), // Don't allow re-connection to an inactive connection
                _ => {}
            }
        }

        self._add_connection(conn, &mut connections);
        
        Ok(())
    }

    fn get_connections(&self) -> HashMap<String, ConnectionState> {
        let mut map = HashSet::new(); // Use a Set to avoid duplicates in the hash map for uniqueness check (though we have explicit keys here anyway)
        
        if self._get_connections().is_empty() {
            return match &mut connections {
                conn => Some(conn.clone()),
            };
        }

        let mut existing = HashMap::new(); // Use a mutable HashSet to find the exact connection by host+port (for consistency with key-based) or just map
