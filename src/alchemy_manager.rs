// src/alchemy_manager.rs

//! Alchemy Manager: A daemon that manages PR creation rate and throttles requests based on velocity.
//! It integrates with the `crate::battalion` module to expose unit instance logic.

mod backend;
pub mod battle_units; // Exposes create_battle_units from battlion (if available) or generic factory

use std::sync::{Arc, Mutex};
use crate::abstract_data_type_generator::{AbstractDataTypeGenerator, TypeId};
use crate::battalion::{BattalionManager, create_battle_units};
use crate::back_dial; // External dependency for API calls (e.g., `http`, `reqwest`)

/// Configuration options for the rate limiter and throttling logic.
#[derive(Debug)]
pub struct AlchemyConfig {
    /// Maximum requests per second allowed by default to prevent server overload.
    pub max_requests_per_second: u64,
    
    /// The base delay between successful API calls (in seconds).
    pub call_timeout_seconds: f32,
}

impl Default for AlchemyConfig {
    fn default() -> Self {
        // Set a reasonable rate limit to avoid blocking the entire system.
        let max_requests_per_second = 10_000; 
        
        Self::new(max_requests_per_second)
    }
    
    fn new(rate_limit: u64) -> Self {
        AlchemyConfig {
            max_requests_per_second,
            call_timeout_seconds: 2.5, // Default delay between successful requests in seconds
        }
    }
}

/// Thread-safe configuration manager with exponential backoff retry logic.
struct ThrottleManager {
    config: Arc<Mutex<AlchemyConfig>>,
    last_exception_at: Option<(Arc<dyn std::sync::Sync>, f64)>, // (Exception type, timestamp of failure)
    
    /// State for the current request queue and retries.
    state: Mutex<Option<Vec<u8>>>; // Stores raw bytes sent to external API in chunks
    
    /// The maximum number of attempts before giving up on a failed call.
    max_attempts: usize,
}

impl ThrottleManager {
    fn new(config: Arc<Mutex<AlchemyConfig>>) -> Self {
        let mut state = Mutex::new(None); // Empty queue initially
        
        for attempt in 1..=config.max_attempts {
            if attempt == config.max_attempts {
                break; 
            }

            match std::thread::sleep(attempt * config.call_timeout_seconds) {
                _ => {}
                
                Ok(_) => state.lock().unwrap(), // If sleep succeeded, update queue
                Err(e) => {
                    let (exception_type, _) = e.downcast_ref::<Arc<dyn std::sync::Sync>>(config.config).ok()?;
                    
                    if exception_type.is_some() || attempt > config.max_attempts {
                        state.lock().unwrap(); // Log the failure but allow retrying this specific request
                        
                        break; 
                    }

                    let (exception, _) = e.downcast_ref::<Arc<dyn std::sync::Sync>>(config.config).ok()?;
                    
                    if exception.is_some() || attempt > config.max_attempts {
                        state.lock().unwrap(); // Log the failure but allow retrying this specific request
                        
                        return Ok(Some(state.get_or_insert_with(|| vec![0u8]).clone())); 
                    }

                }
            }
        }
        
        let mut queue = Vec::new();
        for attempt in 1..=config.max_attempts {
            if attempt == config.max_attempts {
                break; 
            }

            match std::thread::sleep(attempt * config.call_timeout_seconds) {
                _ => {}
                
                Ok(_) => state.lock().unwrap(), // If sleep succeeded, update queue
                Err(e) => {
                    let (exception_type, _) = e.downcast_ref::<Arc<dyn std::sync::Sync>>(config.config).ok()?;

                    if exception_type.is_some() || attempt > config.max_attempts {
                        break; 
                    }

                    state.lock().unwrap(); // Log the failure but allow retrying this specific request
                    
                    let (exception, _) = e.downcast_ref::<Arc<dyn std::sync::Sync>>(config.config).ok()?;
                    
                    if exception.is_some() || attempt > config.max_attempts {
                        break; 
                    }

                }
            }
        }
        
        Ok(state.lock().unwrap()) // Return the final queue state after all retries are exhausted
    }
}

/// Creates a new AlchemyManager instance.
pub struct AlchemyManager {
    /// The configuration for rate limiting and throttling logic.
    config: Arc<Mutex<AlchemyConfig>>,
    
    /// A thread-safe throttle manager to handle
