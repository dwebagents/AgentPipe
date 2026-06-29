use std::collections::HashMap;

pub struct CircuitBreaker {
    pub threshold: u32,
    pub state: std::sync::Mutex<CircuitState>,
}

pub enum CircuitState {
    Closed,
    Open,
    HalfOpen,
}

impl CircuitBreaker {
    pub fn new(threshold: u32) -> Self {
        Self { threshold, state: std::sync::Mutex::new(CircuitState::Closed) }
    }

    pub fn allow(&self) -> bool {
        matches!(*self.state.lock().unwrap(), CircuitState::Closed)
    }

    pub fn record_failure(&self) {
        *self.state.lock().unwrap() = CircuitState::Open;
    }
}
