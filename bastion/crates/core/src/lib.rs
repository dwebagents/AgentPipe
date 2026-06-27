pub mod audit;
pub mod approval;
pub mod error;
pub mod policy;
pub mod session;
pub mod types;
pub mod vault;

pub use audit::AuditChain;
pub use error::{BastionError, Result};
pub use policy::{PolicyDecision, PolicyEngine};
pub use session::SessionManager;
pub use types::{
    Action, ApprovalTicket, AuditEntry, Credential, SessionContext,
};
pub use vault::Vault;
