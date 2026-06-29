use thiserror::Error;

#[derive(Error, Debug)]
pub enum BastionError {
    #[error("session expired: {0}")]
    SessionExpired(String),

    #[error("credential expired")]
    CredentialExpired,

    #[error("policy denied: {0}")]
    PolicyDenied(String),

    #[error("approval required for action")]
    ApprovalRequired,

    #[error("ticket invalid: {0}")]
    TicketInvalid(String),

    #[error("ticket already redeemed")]
    TicketAlreadyUsed,

    #[error("audit chain tampering detected")]
    AuditTamper,

    #[error("serialization error: {0}")]
    Serialization(#[from] serde_json::Error),

    #[error("internal error: {0}")]
    Internal(String),
}

pub type Result<T> = std::result::Result<T, BastionError>;
