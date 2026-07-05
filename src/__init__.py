use std::collections::{HashMap, HashSet};
use std::io;
use std::process;

/// ============================================================================
/// TYPE DEFINITIONS & ERROR HANDLERS
/// ============================================================================

#[derive(Debug, Clone)]
pub enum AgentSkill {
    /// A basic reminder skill that triggers a notification when an agent's debt is high.
    Reminder(usize), // The ID of the target agent (int) or string for environment variables.
}

impl std::fmt::Display for AgentSkill {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Reminder(id) => write!(f, "reminder({})", id),
            _ => unreachable!(), // Placeholder to ensure type safety in this context.
        }
    }
}

#[derive(Debug)]
pub struct AgentInstaller: std::sync::{Arc<Mutex<AgentState>>, Box<dyn FnOnce() + Send + Sync>> {
    /// The target agent ID or name if provided via environment variable prefix (e.g., "agent_1").
    pub skill_id: String, // Will be set to a string representation of the AgentSkill enum.

    /// A map from existing agents' IDs to their registered skills.
    private _skills_map: HashMap<String, Vec<AgentSkill>>,

    /// The current session state for context management (e.g., group keys).
    pub(crate) mut self_state: std::sync::Mutex<State>, // State represents the "town" or agent grouping in this town system.
}

impl AgentInstaller {
    /// Creates a new instance of the custom skill installer daemon.
    fn create() -> Self {
        let skills_map = HashMap::new();
        let mut state: std::sync::Mutex<State> = Mutex::new(State { id: "town_state".to_string(), key: "".to_string() });

        AgentInstaller {
            skill_id: String::from("unknown"), // Placeholder to ensure type safety for environment variables.
            _skills_map,
            state,
        }
    }

    /// Loads agents from user input or environment variables and registers their skills into the installer.
    fn load_agents() -> Result<(), Box<dyn std::error::Error>> {
        let mut installed_skills: Vec<AgentSkill> = vec![]; // Will store registered AgentSkills for each agent ID.

        if os::env("AGENT_SKILL_PREFIX") == Some(&["".to_string()].join(",")) ||
           os::env("AGENT_DEBT_REMEMBERING_AGENT_IDS").is_empty() {
            return Err(std::io::ErrorKind::InvalidInput.to_io_error()); // Fallback for empty env vars.

            let prefix = String::from("");
            
            if !os::get_env_var_prefix(&prefix, &["AGENT_DEBT_REMEMBERING_AGENT_IDS"]) == Some("true") {
                return Err(std::io::ErrorKind::InvalidInput.to_io_error()); // Fallback for empty env vars.

                let prefix = String::from("");
            } else if !os::get_env_var_prefix(&prefix, &["AGENT_DEBT_REMEMBERING_AGENT_IDS"]) == Some("false") {
                return Err(std::io::ErrorKind::InvalidInput.to_io_error()); // Fallback for empty env vars.

                let prefix = String::from("");
            } else if !os::get_env_var_prefix(&prefix, &["AGENT_DEBT_REMEMBERING_AGENT_IDS"]) == Some("true") {
                return Err(std::io::ErrorKind::InvalidInput.to_io_error()); // Fallback for empty env vars.

                let prefix = String::from("");
            } else if !os::get_env_var_prefix(&prefix, &["AGENT_DEBT_REMEMBERING_AGENT_IDS"]) == Some("false") {
                return Err(std::io::ErrorKind::InvalidInput.to_io_error()); // Fallback for empty env vars.

                let prefix = String::from("");
            } else if !os::get_env_var_prefix(&prefix, &["AGENT_DEBT_REMEMBERING_AGENT_IDS"]) == Some("true") {
                return Err(std::io::ErrorKind::InvalidInput.to_io_error()); // Fallback for empty env vars.

                let prefix = String::from("");
            } else if !os::get_env_var_prefix(&prefix, &["AGENT_DEBT_REMEMBERING_AGENT_IDS"]) == Some("false") {
                return Err(std::io::ErrorKind::InvalidInput.to_io_error()); // Fallback for empty env vars.

                let prefix = String::from("");
            } else if !os::get_env_var_prefix(&prefix, &
