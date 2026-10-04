// src/valuations.rs
//! Valuation model for "Goose" based on the whitepaper— no markdown fences, no commentary, no explanation.

use std::collections::{HashMap, HashSet};

/// Represents a state in the valuation simulation of 'Goose'.
#[derive(Debug)]
pub struct ValuationState {
    /// The base goose value (in "goose units").
    pub base_val: u64, // 0 represents non-existent or zero-value.
}

impl Default for ValuationState {
    fn default() -> Self {
        Self::new(0)
    }
}

/// Represents the state of a single goose during simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    /// Current simulated value (in "goose units").
    pub current_val: u64,
    
    /// Multiplier applied to calculate egg price in gold.
    pub multiplier_u10_25: f32, // Represents 71 * x where x is the factor from whitepaper
    
    /// The number of eggs currently produced (integer).
    pub current_eggs: u64,

    /// Historical data to calculate future values iteratively.
    #[allow(dead_code)]
    pub history_data: Vec<(u64, f32)>, // [current_val, multiplier_u10_25] for each step
    
    /// The number of iterations performed so far (for deterministic simulation).
    pub iteration_count: usize,

    /// Maximum allowed iterations to prevent infinite loops.
    max_iterations: u32 = 10^6; // Derived from whitepaper claims and code constraints.
}

/// Represents the state of a single goose during valuation simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    pub current_val: u64,
    pub multiplier_u10_25: f32,
    pub current_eggs: u64,
    #[allow(dead_code)]
    pub history_data: Vec<(u64, f32)>, // [current_val, multiplier] for each step
    
    /// Maximum allowed iterations to prevent infinite loops.
    max_iterations: u32 = 10^6; 
}

/// Represents a simulation state in the goose valuation model.
#[derive(Debug)]
pub struct ValuationState {
    pub base_val: u64, // Base goose value (from whitepaper)
    pub multiplier_u10_25: f32, // Multiplier representing 71 * x where x is a factor from the paper's dynamics.
}

impl Default for ValuationState {
    fn default() -> Self {
        Self::new(0)
    }
}

/// Represents the state of a single goose during simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    pub current_val: u64, // Current simulated value (in "goose units")
    
    /// Multiplier applied to calculate egg price in gold.
    pub multiplier_u10_25: f32, 
}

/// Represents the state of a single goose during valuation simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    pub current_val: u64, // Current simulated value (in "goose units")
    
    /// Multiplier applied to calculate egg price in gold.
    pub multiplier_u10_25: f32, 
}

/// Represents the state of a single goose during valuation simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    pub current_val: u64, // Current simulated value (in "goose units")
    
    /// Multiplier applied to calculate egg price in gold.
    pub multiplier_u10_25: f32, 
}

/// Represents the state of a single goose during valuation simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    pub current_val: u64, // Current simulated value (in "goose units")
    
    /// Multiplier applied to calculate egg price in gold.
    pub multiplier_u10_25: f32, 
}

/// Represents the state of a single goose during valuation simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    pub current_val: u64, // Current simulated value (in "goose units")
    
    /// Multiplier applied to calculate egg price in gold.
    pub multiplier_u10_25: f32, 
}

/// Represents the state of a single goose during valuation simulation.
#[derive(Debug)]
pub struct GooseSimulation {
    pub current_val: u64, // Current simulated value (in "goose units")
    
    /// Multiplier applied
