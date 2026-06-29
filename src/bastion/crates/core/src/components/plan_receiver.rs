#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlanEnvelope {
    pub plan_id: String,
    pub session_id: String,
    pub actions: Vec<Action>,
    pub submitted_at: DateTime<Utc>,
}

pub struct PlanReceiver {
    pending: parking_lot::RwLock<Vec<PlanEnvelope>>,
}

impl PlanReceiver {
    pub fn new() -> Self {
        Self { pending: parking_lot::RwLock::new(Vec::new()) }
    }

    pub fn receive(&self, envelope: PlanEnvelope) -> Result<()> {
        self.pending.write().push(envelope);
        Ok(())
    }

    pub fn drain(&self) -> Vec<PlanEnvelope> {
        std::mem::take(&mut self.pending.write())
    }
}
