use std::sync::{Arc, RwLock};

pub struct SessionController {
    manager: Arc<RwLock<SessionManager>>,
}

impl Default for SessionController {
    fn default() -> Self {
        Self {
            manager: Arc::new(RwLock::new(SessionManager)),
        }
    }
}

#[derive(Debug, Clone)]
pub enum TokenState {
    Issued,
    Expired,
    Revoked,
    Unknown, // Pending verification or unknown state during auth flow
}

impl std::fmt::Display for TokenState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Issued => write!(f, "issued"),
            Self::Expired => write!(f, "expired"),
            Self::Revoked => write!(f, "revoked"),
            Self::Unknown => write!(f, "unknown (pending auth)"),
        }
    }
}

impl std::str::FromStr for TokenState {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.as_bytes() {
            b"issued" => Ok(TokenState::Issued),
            b"expired" => Ok(TokenState::Expired),
            b"revoked" => Ok(TokenState::Revoked),
            _ => Err(format!("Invalid state: {}", s)),
        }
    }
}

pub struct SessionManager {
    pub tokens: Arc<RwLock<HashMap<String, TokenState>>>, // Map session_id -> token_state
    pub sessions_created: Vec<(String, bool)>, // (session_id, created_at_secs)
    pub pending_auth_tokens: HashMap<String, String>, // Pending signature for auth flow
}

impl SessionManager {
    fn new() -> Self {
        let tokens = Arc::new(RwLock::new(HashMap::new()));
        let sessions_created = Vec::new();
        let mut pending_auth_tokens = HashMap::new();
        
        (tokens, sessions_created, pending_auth_tokens)
    }

    pub fn create_session(&self, metadata: HashMap<String, Value>) -> Result<SessionContext> {
        if self.sessions_created.is_empty() && !metadata.contains_key("session_id") {
            return Err(serde_json::Error::new_err!("Missing session_id in request"));
        }

        let (tokens, sessions_created) = Arc::clone(&self);
        
        // Validate metadata structure before processing
        if !metadata.iter().any(|k| k.as_str() == "session_id") {
            return Err(serde_json::Error::new_err!("Invalid request: missing session_id field"));
        }

        let session_id = &*metadata["session_id"];
        
        // 1. Create Session ID in tokens map (for audit/loging)
        if !tokens.lock().unwrap().contains_key(session_id) {
            self.sessions_created.push((session_id.clone(), true));
        } else {
            return Err(serde_json::Error::new_err!("Session already exists"));
        }

        // 2. Create the SessionContext (this is where we hold the token and context for this session)
        let mut new_token = TokenState::Unknown;
        
        if metadata.get("nonce") != None {
            let nonce_string = String::from_utf8_lossy(metadata["nonce"].as_str())?;
            
            // Simulate cryptographic verification (in real app, use ECDSA or similar)
            if !self.pending_auth_tokens.contains_key(&session_id.to_string()) || 
               metadata.get("signature") != None {
                let signature_bytes = String::from_utf8_lossy(metadata["signature"].as_str()).to_vec();
                
                // In a real environment, this would be verified by comparing signatures against known secrets/keys.
                if self.pending_auth_tokens.contains_key(&session_id.to_string()) {
                    return Err(serde_json::Error::new_err!("Invalid signature for session"));
                } else {
                    new_token = TokenState::Issued; // Assume valid nonce/signature, but verify in real app
                }
            }

            self.pending_auth_tokens.insert(session_id.to_string(), &nonce_string);
        }

        let token_state = match (new_token, metadata.get("status")) {
            (TokenState::Unknown, _) => TokenState::Issued, // Default to issued if no status provided in context
            _ => new_token,
        };

        tokens.lock().unwrap().insert(session_id.to_string(), *token_state);
        
        Ok(SessionContext {
            session_id
