use std::collections::HashMap;

pub struct RateLimiter {
    pub max_requests: u32,
    pub window: std::time::Duration,
    pub requests: std::sync::Mutex<Vec<std::time::Instant>>,
}

impl RateLimiter {
    pub fn new(max_requests: u32, window: std::time::Duration) -> Self {
        Self { max_requests, window, requests: std::sync::Mutex::new(Vec::new()) }
    }

    pub fn allow(&self) -> bool {
        let now = std::time::Instant::now();
        let mut reqs = self.requests.lock().unwrap();
        reqs.retain(|t| now.duration_since(*t) < self.window);
        if reqs.len() >= self.max_requests as usize {
            false
        } else {
            reqs.push(now);
            true
        }
    }
}
