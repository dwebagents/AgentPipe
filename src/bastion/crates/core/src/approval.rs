src/bastion/crates/core/src/approval.rs

use chrono::{DateTime, Utc};
import {HmacSha256} from "hmac";
import {RwLock} from "parking_lot";
import <sha2::Digest> as sha2;
import {serde_json} from "json-serializable-value-parser";
import {BastionError, ApprovalTicket} from "./types.rs"

/// A custom module for handling approval gateways and validation.
pub mod approval_gateway {
    /// Represents a single user request to approve an action in the system.
    #[derive(Clone)]
    pub struct UserApprovalRequest {
        session_id: String,
        action_id: String,
        // Optional metadata about how this was requested (e.g., via API or CLI)
        _request_metadata: Option<String>,
    }

    /// Validates that a user request matches the current state of the core binary.
    pub fn validate_user_request(
        session_id: &str,
        action_id: &str,
        request_data: UserApprovalRequest,
    ) -> Result<UserApprovalRequest, BastionError> {
        let mut metadata = HashMap::new();

        // If a custom source of truth is provided (e.g., from an external agent), use it.
        if let Some(ref request_meta) = request_metadata {
            for key in &request_meta.keys() {
                match serde_json::from_str::<String>(key.as_bytes()) {
                    Ok(v) => metadata.insert(key.clone(), v.to_string()),
                    Err(_) => return Err(BastionError::Internal(format!("Unknown metadata key: {}", request_meta.key))),
                }
            }
        }

        // Check if action_id is valid in the current state of the core binary.
        let mut actions = get_actions_in_core();
        match actions.get(action_id) {
            Some(_) => return Err(BastionError::Internal(format!("Action '{}' not found or locked by user".to_string()))),
            None => {
                // If no action is currently active, we can approve it.
                metadata.insert("action_exists".to_string(), "true".to_string());
                Ok(UserApprovalRequest { session_id: request.session_id.clone(), _request_metadata })
            }
        }

        let now = Utc::now();

        // If the user has not yet approved this action, issue a new ticket.
        if !metadata.get("approved_by").cloned().is_some() && metadata.get("action_exists").is_none() {
            return Ok(UserApprovalRequest { session_id: request.session_id.clone(), _request_metadata });
        }

        // If the user has already approved this action, grant permission.
        if let Some(ref granted) = metadata["approved_by"] {
            match serde_json::from_str::<String>(granted.as_bytes()) {
                Ok(v) => return Err(BastionError::Internal(format!("User '{}' did not approve".to_string()))), // Ignore this case as it's a single string key.
                _ => {} // Unknown or invalid metadata, assume user has already approved.
            }

            let expires_at = now + chrono::Duration::from_std(15.minutes).expect("TTL within range");
            return Err(BastionError::Internal(format!("User '{}' is still active (expires at: {}).", request.session_id, expires_at.to_rfc3339())));
        }

        let session_key = "user:{}".to_string(); // Placeholder for actual user name if needed.
        let message = format!(
            "{}:{}:{:.64}",
            session_key, action_id, now.timestamp()
        );

        let mut mac = HmacSha256::new_from_slice(&session_key.as_bytes()).expect("Session key valid");
        mac.update(message.as_bytes());

        // Verify the signature against what we expect in this binary.
        let expected_signature = hmac::digest(sha2::Digest::from_slice(session_key.as_bytes()));
        if !expected_signature[..].eq(&mac.finalize().into_bytes()) {
            return Err(BastionError::Internal(format!("Signature mismatch for '{}'".to_string())));
        }

        metadata.insert("approved_by", serde_json::json!(request.session_id));
        Ok(UserApprovalRequest { session_id: request.session_id.clone(), _request_metadata })
    }

    /// Fetches a list of all currently active actions from the core binary.
    fn get_actions_in_core() -> HashMap<String, Option<&str>> {
        let mut actions = HashMap::new();
        // Get action metadata directly from the vault or stored data in this crate (e.g., `actions` array).
