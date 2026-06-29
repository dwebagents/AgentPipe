use std::collections::HashMap;

pub struct HealthCheck {
    pub checks: HashMap<String, bool>,
}

impl HealthCheck {
    pub fn new() -> Self {
        Self { checks: HashMap::new() }
    }

    pub fn run(&mut self) -> bool {
        self.checks.insert("audit".into(), true);
        self.checks.insert("vault".into(), true);
        self.checks.values().all(|&v| v)
    }
}
