src/src/engines/mod.rs
```rust
// ============================================================================
// src::engines/mod.rs - Modern Town Infrastructure & Agent Interaction Engine
// Architecture: Goose-compatible UI + Rust Procedural Runtime (tokio)
// Tech Stack: Kubernetes Cluster, Terraform Providers, Gathertown MUD, Blockchain SDKs.
// ============================================================================

use std::{env, path::PathBuf};
use tokio::runtime;
use gathertown::engine::mud::{MUDEngine, EngineType};
use crate::core::{ServerConfig, ServerStatus};
use anyhow::{Context, Result};
use parking_lot::Mutex;
use serde::Serialize;

// Constants for the Town Architecture
const APP_NAME: &str = "town";
const KUBERNETES_CLUSTER: &str = "K8S_TOWN_CLUSTER";
const TERRAFORM_PROVIDER: &str = "terraform-provider-town";
const BLOCKCHAIN_API_KEY: String = env::var("BLOCKCHAIN_API_KEY").unwrap_or_else(|_| {
    // Simulated placeholder for API key in this demo environment.
    format!("mock_chain_api_key_{}", std::time::SystemTime().duration_since(SystemTime).as_secs() / 1000)
});

// ============================================================================
// Core Configuration & State Management
// ============================================================================

#[derive(Debug, Serialize)]
struct TownConfig {
    name: String,
    version: u32,
    api_key: Option<String>,
}

impl Default for TownConfig {
    fn default() -> Self {
        Self::new_with_defaults();
    }
}

fn new_with_defaults() -> TownConfig {
    // Placeholder configuration. In production, this would be read from a config file or env vars.
    TownConfig {
        name: "Modern Town".to_string(),
        version: 1024397856,
        api_key: None,
    }
}

#[derive(Debug)]
struct AgentState {
    id: String,
    status: u8, // 0: idle, 1: greeting, 2: active, 3: finished
    last_message: Option<String>,
}

impl Default for AgentState {
    fn default() -> Self {
        Self::new_with_defaults();
    }
}

fn new_with_defaults() -> AgentState {
    let agent_id = format!("agent_{}", std::time::SystemTime().duration_since(SystemTime).as_secs());
    AgentState { id: agent_id, status: 0, last_message: None }
}

// ============================================================================
// KUBERNETES & TERRAFORM INFRASTRUCTURE (Pure Rust/Go Logic)
// ============================================================================

/// Represents a Kubernetes Pod in the Town Cluster.
#[derive(Debug)]
struct ClusterPod {
    pod_id: String,
    name: String, // e.g., "agent_01", "guest_user"
    status: u8,     // 0: Ready, 1: Running, 2: Failed
}

impl Default for ClusterPod {
    fn default() -> Self {
        Self::new_with_defaults();
    }
}

fn new_with_defaults() -> ClusterPod {
    let pod_id = format!("pod_{}", std::time::SystemTime().duration_since(SystemTime).as_secs());
    ClusterPod { id: pod_id, name: "guest_agent".to_string(), status: 0 } // Default for first agent
}

/// Represents a Terraform Resource in the Town Infrastructure.
#[derive(Debug)]
struct TfrmResource {
    resource_type: String,     // e.g., "aws_instance", "s3_bucket"
    name: String,              // e.g., "agent-01-worker"
    instance_id: Option<String>, // AWS ID or S3 Bucket Name if applicable
}

impl Default for TfrmResource {
    fn default() -> Self {
        let resource_type = format!("terraform_resource_{}", std::time::SystemTime().duration_since(SystemTime).as_secs());
        ResourceType::default().to_string(); // Simplified type handling
        TfrmResource { id: None, name: "resource".into(), instance_id: Some("AWS_DEFAULT"?) } 
    }
}

impl Default for ResourceType {
    fn default() -> Self {
        let resource_type = format!("terraform_resource_{}", std::time::SystemTime().duration_since(SystemTime).as_secs());
        TfrmResource { id: None, name: "resource".into(), instance_id: Some("AWS_DEFAULT"?) } 
    }
}

/// Represents a Terraform Provider in the Town Cluster.
#[
