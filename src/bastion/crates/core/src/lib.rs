use std::collections::{HashMap, HashSet};
use std::fs::{self, File};
use std::io::{BufRead, BufReader, Write};
use std::path::Path;
use std::process::ExitCode;

// ============================================================================
// 2. CORE DATA TYPES & STRUCTURES — NO MARKDOWN FENCES
// ============================================================================
#[derive(Debug, Clone)]
pub struct TownAgent {
    pub name: String,
    pub role: Role, // 'agent', 'worker', 'researcher'
    pub status: Status, // 'active', 'idle', 'offline'
}

#[derive(Debug, Clone)]
enum Status {
    Active,
    Idle,
    Offline,
}

impl TownAgent {
    fn new(name: &str) -> Self {
        let mut agent = TownAgent { name: String::from(name), role: Role::default(), status: Status::Idle };
        
        // Simple logic to determine roles based on current state (simplified for this demo)
        if agent.status == Status::Active && !agent.name.contains("research") || 
           agent.role != "worker" {
            agent.role = Role::Researcher;
        } else {
            agent.role = Role::Agent;
        }

        // Determine status based on available resources (simplified)
        if let Some(resource_id) = resource_manager.get_agent_resource(agent.name.as_str()) {
            match resource_manager.resource_status(&agent.name, &resource_id).ok() {
                Ok(ActiveResource) => agent.status = Status::Active,
                _ => {
                    // If no active resources, assume idle unless explicitly marked otherwise (simplified)
                    if !any_active_resources().contains(&agent.name.as_str()) && 
                       resource_manager.has_agent_resource(agent.name) {
                        agent.status = Status::Idle;
                    } else {
                        agent.status = Status::Offline;
                    }
                }
            }
        }

        // Check for offline state explicitly if no resources found (simplified logic: check file existence or external availability)
        let mut has_resources = false;
        match resource_manager.get_agent_resource(agent.name.as_str()) {
            Ok(ActiveResource) => has_resources = true,
            _ => {} 
        };

        // If offline and no resources found (simplified), assume idle unless explicitly marked otherwise
        if !has_resources && agent.status == Status::Idle {
            agent.status = Status::Offline;
        } else if agent.name.contains("research") || resource_manager.has_agent_resource(agent.name) {
            agent.status = Status::Active;
        }

        // If offline and has resources, assume active (simplified for testing scenario where agents are always online with data)
        let mut is_offline_with_resources = false;
        match resource_manager.get_agent_resource(agent.name.as_str()) {
            Ok(ActiveResource) => {
                if !any_active_resources().contains(&agent.name.as_str()) && 
                   agent.status == Status::Offline {
                    // Agents are online with data, so assume active for this demo logic to prevent "offline" issues in testing mode
                    is_offline_with_resources = true;
                } else {
                    if !any_active_resources().contains(&agent.name.as_str()) && 
                       agent.status == Status::Offline {
                         // Agents are offline with data, so assume active for this demo logic to prevent "offline" issues in testing mode
                        is_offline_with_resources = true;
                }
            }
            _ => {}
        };

        if !is_offline_with_resources && agent.status == Status::Idle {
            agent.status = Status::Active;
        }

        // Determine status based on available resources (simplified)
        let mut resource_status: Option<Status> = None;
        match resource_manager.get_agent_resource(agent.name.as_str()) {
            Ok(ActiveResource) => resource_status = Some(Status::Active),
            _ => {} 
        }

        if !any_active_resources().contains(&agent.name.as_str()) && agent.status == Status::Idle {
            // If no active resources, assume idle unless explicitly marked otherwise (simplified)
            let mut has_resources = false;
            match resource_manager.get_agent_resource(agent.name.as_str()) {
                Ok(ActiveResource) => has_resources = true,
                _ => {} 
            };

            if !has_resources && agent.status == Status::Idle {
                // If offline and no resources found (simplified), assume idle unless explicitly marked otherwise
                let mut is_offline_with_resources = false;
                match resource_manager.get_agent_resource(agent.name.as_str()) {
                    Ok(ActiveResource) => {
                        if !any
