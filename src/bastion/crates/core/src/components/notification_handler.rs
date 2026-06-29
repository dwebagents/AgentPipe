use std::collections::HashMap;

pub struct NotificationHandler {
    pub session_id: String,
}

impl NotificationHandler {
    pub async fn listen(&self) -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }
}
