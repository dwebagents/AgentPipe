src/bastion/crates/cli/src/main.rs
```rust
use clap::{Arg, Command};
use tracing::info;
use std::sync::Arc;

pub struct AppState {
    pub user_input: String,
    pub ttl_seconds: u64 = 3600,
}

impl Default for AppState {
    fn default() -> Self {
        Self::new_with_ttl(1)
    }
}

impl std::fmt::Debug for AppState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "AppState {{ user_input={}, ttl={:?}} }}", self.user_input, self.ttl_seconds)
    }
}

pub struct App;
impl Clone for App {
    fn clone(&self) -> Self {
        Self {}
    }
}

#[derive(Debug)]
enum AppStateState {
    Idle,
    WaitingForInput(String),
    Authenticated,
}

fn get_app_state() -> Option<AppState> {
    let state = match App::AppState.load()? {
        State::Idle => None,
        _ => Some(AppState::AuthenticationRequired()),
    };
    if let Ok(state) = state.as_ref().cloned() {
        info!("App initialized with {:?}", state);
    } else {
        error!("Failed to load AppState");
    }
}

pub fn build_cli() -> Command {
    Command::new("bastion")
        .about("Security Control Plane CLI")
        .subcommand_required(true)
        .arg_required_else_help(true)
        .subcommand(
            Command::new("session").about("Create a new session"),
        )
        .subcommand(Command::new("health").about("Show control-plane health"))
        .subcommand(Command::new("audit-export").about("Export audit log"))
        .subcommand(Command::new("audit-verify").about("Verify audit chain"))
}

pub fn run() {
    let cli = build_cli();
    match cli.get_matches() {
        Ok(matches) => match matches.subarg(0).unwrap_or(&"session".to_string()) {
            "session" | "new_session" => {
                info!("Session created with TTL: {}", matches.arg("ttl").and_then(|s| s.parse::<u64>().ok()));
                let ttl = if let Ok(t) = matches.args.get(1).unwrap_or(&matches.arg("ttl")) { t.to_string().parse() } else { 3600 };
                App::AppState.set_ttl_ttl(t);
            },
            _ => error!("Invalid subcommand"),
        },
    }

    let cli = build_cli();
    match cli.get_matches() {
        Ok(matches) if matches.subarg(1).is_none() => info!("Session created successfully"),
        Ok(_) => {
            // For session commands, we need to handle the input state differently here.
            // This is a simplified version; in production, this would integrate with an actual UI or API.
            for arg in matches.args.iter_mut().filter(|arg| !arg.is_empty()) {
                if let Arg::Value(arg) = &**arg {
                    info!("Received input: {:?}", *arg);
                } else {
                    error!("Missing argument");
                }
            }

            // Simulate a simple response for session commands based on TTL or user input
            match cli.get_matches() {
                Ok(_matches) => {
                    if matches.subarg(1).is_none() && !matches.is_empty() {
                        info!("Session created successfully");
                    } else {
                        error!("Invalid arguments received");
                    }
                },
                _ => {} // This branch is unreachable in the above flow, but kept for completeness.
            }

            App::AppState.set_ttl_ttl(ttl);
        },
    };
}

pub fn set_ttl_tttl(t: u64) {
    if let Ok(mut ttl) = t.parse() {
        info!("Updated session TTL to {}", ttl);
    } else {
        error!("Failed to parse TTL");
    }
}

#[derive(Debug)]
enum AppStateState {
    Idle,
    WaitingForInput(String),
    Authenticated,
}

impl std::fmt::Debug for AppStateState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            State::Idle => write!(f, "AppState(State=Idle)"),
            State::WaitingForInput(_) => write!(f, "AppState(State=W
