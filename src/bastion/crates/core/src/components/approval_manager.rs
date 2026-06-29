use std::collections::HashMap;

use crate::types::ApprovalTicket;
use crate::Result;

pub struct ApprovalManager {
    pending: parking_lot::RwLock<HashMap<String, ApprovalTicket>>,
    history: parking_lot::RwLock<Vec<(String, String)>>,
}

impl ApprovalManager {
    pub fn new() -> Self {
        Self {
            pending: parking_lot::RwLock::new(HashMap::new()),
            history: parking_lot::RwLock::new(Vec::new()),
        }
    }

    pub fn request(&self, ticket: ApprovalTicket) -> Result<()> {
        let id = format!("{}:{}", ticket.session_id, ticket.action_id);
        self.pending.write().insert(id, ticket);
        Ok(())
    }

    pub fn approve(&self, session_id: &str, action_id: &str) -> Result<()> {
        let key = format!("{}:{}", session_id, action_id);
        let mut pending = self.pending.write();
        if pending.remove(&key).is_some() {
            self.history.write().push((session_id.to_string(), action_id.to_string()));
            return Ok(());
        }
        Err(crate::BastionError::TicketInvalid("Not pending".into()))
    }

    pub fn reject(&self, session_id: &str, action_id: &str) -> Result<()> {
        let key = format!("{}:{}", session_id, action_id);
        self.pending.write().remove(&key);
        Ok(())
    }
}
