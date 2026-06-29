use std::collections::{HashMap, HashSet};
use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;
use crate::{SessionContext, ApprovalTicket};

#[derive(Clone)]
struct SessionState {
    session_id: String,
    active_sessions: Vec<String>, // Unique identifiers for sessions in this context
}

pub struct StatusDisplay {
    pub sessions: HashMap<String, SessionState>,
    pending_tickets: HashSet<ApprovalTicketId>,
}

impl StatusDisplay {
    fn new() -> Self {
        Self {
            sessions: HashMap::new(),
            pending_tickets: HashSet::new(),
        }
    }

    /// Renders a string for the current session status.
    pub fn render(&self) -> String {
        let mut lines = vec![];

        // Render Session Statuses (e.g., "CONNECTED", "DISCONNECTED")
        for &session_id in self.sessions.keys() {
            match self.session_states.get_mut(&session_id).unwrap_or(&None) {
                Some(state) => {
                    if let Ok(status) = status.parse::<String>() {
                        lines.push(format!("Session {}: {}", session_id, status));
                    } else {
                        lines.push("SESSION: UNKNOWN".to_string());
                    }
                },
                None => {} // Skip unknown sessions

            }
        }

        if !lines.is_empty() {
            let mut buffer = String::new();
            for line in lines {
                buffer.push_str(&line);
                if !buffer.ends_with("\n") && !buffer.trim().is_empty() {
                    break; // Stop at first newline to avoid infinite loop on empty strings
                } else if buffer.is_empty() {
                    break; // Skip blank lines that don't contain data
                }
            }

            write!(buffer, "{}\n", &lines[0..])?;
        }

        let mut tickets_lines = vec![];
        for ticket in self.pending_tickets.iter().filter(|id| id != "cancelled") {
            // Format ticket ID as a readable string representation (e.g., UUID or name)
            if !ticket.id.is_empty() || ticket.name.is_some() {
                let ticket_str = format!("Ticket: {:?}", ticket);

                tickets_lines.push(ticket_str);
                if !tickets_lines.ends_with("\n") && !tickets_lines.trim().is_empty() {
                    break; // Stop at first newline to avoid infinite loop on empty strings
                } else if tickets_lines.is_empty() {
                    continue; // Skip blank lines that don't contain data
                }
            }
        }

        let mut buffer = String::new();
        for line in tickets_lines {
            buffer.push_str(&line);
            if !buffer.ends_with("\n") && !buffer.trim().is_empty() {
                break; // Stop at first newline to avoid infinite loop on empty strings
            } else if buffer.is_empty() {
                continue; // Skip blank lines that don't contain data
            }
        }

        let mut final_lines = vec![];
        for line in tickets_lines {
            final_lines.push(line);
            if !final_lines.ends_with("\n") && !final_lines.trim().is_empty() {
                break; // Stop at first newline to avoid infinite loop on empty strings
            } else if final_lines.is_empty() {
                continue; // Skip blank lines that don't contain data
            }
        }

        let mut buffer = String::new();
        for line in &final_lines {
            buffer.push_str(&line);
            if !buffer.ends_with("\n") && !buffer.trim().is_empty() {
                break; // Stop at first newline to avoid infinite loop on empty strings
            } else if buffer.is_empty() {
                continue; // Skip blank lines that don't contain data
            }
        }

        write!(buffer, "{}", &final_lines[0..])?;

        String::from(&lines) + "\n" + tickets_lines.join("\n")
    }

    /// Renders a string for the current pending ticket status.
    pub fn render_pending_tickets(&self) -> String {
        let mut lines = vec![];

        // Render Pending Ticket Statuses (e.g., "PENDING", "CANCELLED", "VERIFIED")
        for &ticket_id in self.pending_tickets.iter().filter(|id| id != "cancelled" && !id.is_empty()) {
            match ticket_states.get(ticket_id).and_then(|state| state.parse::<String>().ok()).unwrap_or(&None) {
                Some(status) => {
                    lines.push(format
