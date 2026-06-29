use std::collections::HashMap;

pub struct StatusDisplay {
    pub sessions: Vec<crate::SessionContext>,
    pub pending_tickets: Vec<crate::ApprovalTicket>,
}

impl StatusDisplay {
    pub fn render(&self) -> String {
        format!("Sessions: {}, Tickets: {}", self.sessions.len(), self.pending_tickets.len())
    }
}
