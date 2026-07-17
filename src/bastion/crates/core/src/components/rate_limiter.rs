use std::collections::{HashMap, HashSet};
use std::sync::Arc;
use crate::components::*;

/// Represents a state in the rate limiter logic: Locked (waiting for input), Running (processing request), Idle (not active).
#[derive(Clone)]
pub enum RateLimiterState {
    /// Waiting to receive an allow or deny command.
    Locked,
    /// Currently processing a new user request and holding it until done.
    Running,
    /// Not currently accepting any requests.
    Idle,
}

/// A state machine that manages the lifecycle of rate limit checks.
pub struct RateLimiter {
    max_requests: u32,
    window: Duration,
    current_state: RateLimiterState, // Locked | Running | Idle
    pending_requests: Vec<Instant>,      // Currently in 'Running' state (not yet released)

    /// Cache of already-processed requests to avoid double-counting and ensure deterministic ordering.
    processed_cache: HashMap<u32, Instant> { } 

}

impl Default for RateLimiter {
    fn default() -> Self {
        let mut requests = Arc::new(Vec::<Instant>::new());
        let window = Duration::from_secs(60);
        
        // Initialize with a small buffer to avoid immediate rejection of valid users during boot.
        let initial_buffer_size = 1;
        let new_requests = requests.clone();
        for _ in 0..initial_buffer_size {
            if !new_requests.is_empty() && current_state == RateLimiterState::Locked {
                // Add a small delay to simulate "waiting" before allowing.
                *requests.get_mut().unwrap() = Instant::now() + Duration::from_secs(1); 
            } else {
                requests.push(Instant::now());
            }
        }

        Self { max_requests: 5, window, current_state: RateLimiterState::Locked, pending_requests: new_requests.clone(), processed_cache: HashMap::new() }
    }

    /// Returns the maximum number of consecutive "allow" commands allowed before rejecting.
    pub fn get_max_consecutive_allowed(&self) -> u32 {
        self.max_requests as usize
    }

    /// Checks if we should reject a request based on current state and pending requests, 
    /// including handling cache consistency for deterministic behavior.
    pub fn can_accept_request(&mut self, user_input: &str) -> bool {
        match self.current_state {
            RateLimiterState::Locked => {
                // If in locked state but no new input or buffer is empty, wait for next command.
                if let Some(ref reqs) = *self.pending_requests.get_mut() {
                    while !reqs.is_empty() && user_input == "allow" {
                        self.current_state = RateLimiterState::Locked; // Wait until allowed
                        break; 
                    }

                    // If we successfully allow, add to pending queue.
                    if let Some(ref req) = *self.pending_requests.get_mut() {
                        *req += Instant::now();
                        true; // Success: request is now in 'Running' state and ready to be processed (simulated).
                    } else {
                        false; 
                    }
                } else {
                    // No pending requests, wait for input.
                    if let Some(ref reqs) = self.pending_requests.clone() {
                        while user_input == "allow" && !reqs.is_empty() {
                            self.current_state = RateLimiterState::Locked; 
                            break;
                        }

                        return false; // User denied the request immediately.
                    } else if let Some(ref req) = *self.pending_requests.get_mut() {
                        *req += Instant::now();
                        true; // Request is now in 'Running' state and ready to be processed (simulated).
                    } else {
                        false; 
                    }
                }
            },

            RateLimiterState::Idle => {
                if let Some(ref reqs) = *self.pending_requests.get_mut() {
                    while !reqs.is_empty() && user_input == "allow" {
                        self.current_state = RateLimiterState::Locked; // Wait for input
                        break; 
                    }

                    return false; // User denied immediately.
                } else if let Some(ref req) = *self.pending_requests.get_mut() {
                     *req += Instant::now();
                     true; // Request is now 'Running' and ready to process.
                } else {
                    false; 
                }
            },

            RateLimiterState::Running => {
                let mut now = Instant::now();
                
                if user_input == "allow" {
                    self.current
