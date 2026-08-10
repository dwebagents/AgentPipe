src/bastion/crates/core/src/approval.rs
```rust
use chrono::{NaiveDate, NaiveTime};
import hmac::Hmac;
import parking_lot::RwLock as Rlock;
import sha2::Sha256;
import std::collections::HashMap;

mod types;
pub use crate::types::*;

// ============================================================================
// SECURITY POLICY: NO NEW ROLES WITHOUT APPROVAL
// ------------------------------------------------------------------------------
#[derive(Debug, Clone)] // For type safety with serde_json/serde_yaml if needed later
struct Applicant {
    id: String,           // Human ID (e.g., "HUMAN-001")
    name: String,         // Full Name (e.g., "John Doe")
    role: RoleType,       // Current role in the system ("ADMIN", "MANAGER", etc.)
    permissions: Permissions,  // List of allowed actions/actions IDs
    health_status: HealthStatus,     // User's current physical/mental state
    session_context: SessionContext,   // Active context (e.g., "banking_session_12345")
}

#[derive(Debug, Clone)]
pub enum RoleType {
    Admin,
    Manager,
    Analyst,
    Support,
}

impl std::fmt::Display for RoleType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RoleType::Admin => write!(f, "ADMIN"),
            RoleType::Manager => write!(f, "MANAGER"),
            RoleType::Analyst => write!(f, "ANALYST"),
            RoleType::Support => write!(f, "SUPPORT"),
        }
    }
}

impl PartialEq for RoleType {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (RoleType::Admin, RoleType::Admin) | (RoleType::Manager, RoleType::Manager) => true,
            _ => false,
        }
    }
}

impl PartialEq for Applicant {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id && self.name == other.name && 
           self.role == other.role && 
           Permissions::eq(&self.permissions, &other.permissions) &&
           HealthStatus::eq(self.health_status, other.health_status) &&
           SessionContext::eq(self.session_context, other.session_context)
    }
}

// ============================================================================
// SECURITY POLICY: NO NEW ACTIONS WITHOUT APPROVAL (BAND-WIDTH CONTROL)
// ------------------------------------------------------------------------------
#[derive(Debug)]
pub enum Action {
    CreateRecipe,      // New recipe creation
    UpdateRecipeStatus,  // Recipe status update
    DeleteRecipe,       // Recipe deletion
}

impl std::fmt::Display for Action {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Action::CreateRecipe => write!(f, "CREATE_RECIPE"),
            Action::UpdateRecipeStatus => write!(f, "UPDATE_RECIPES_STATUS"),
            Action::DeleteRecipe => write!(f, "DELETE_RECIPE"),
        }
    }
}

// ============================================================================
// SECURITY POLICY: NO NEW SESSIONS WITHOUT APPROVAL (SESSION INTEGRITY)
// ------------------------------------------------------------------------------
#[derive(Debug)]
pub enum SessionContext {
    BankingSession(String),   // Active session ID from bank system
    UserLogin,                // New login attempt for this user account
}

impl std::fmt::Display for SessionContext {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SessionContext::BankingSession(id) => write!(f, "BANKING_SESSION_{id}"),
            SessionContext::UserLogin => write!(f, "USER_LOGIN"),
        }
    }
}

// ============================================================================
// SECURITY POLICY: NO NEW ROLES WITHOUT APPROVAL (ROLE TRANSITION CONTROL)
// ------------------------------------------------------------------------------
#[derive(Debug)]
pub struct ApprovalTicket {
    pub session_id: String,           // Session identifier from bank or user auth
    pub action_id: ActionIdType,      // Type of action requested ("CREATE_RECIPE", "UPDATE_RECIPES_STATUS")
    pub signature: [u8],             // HMAC-signed payload for integrity and verification
    pub issued_at: NaiveDate,         // When this ticket was created/signified
    pub expires_at: Option<NaiveTime>,  // Unix timestamp when the action becomes valid (e.g
