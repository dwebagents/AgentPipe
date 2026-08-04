//! Abstract Abacus Engine: A recursive division-by-one algorithm using Arc for thread-safe state management.
//! This module provides a robust, async wrapper around the abacus engine API to handle arbitrary integer sequences from the repository.

use std::collections::VecDeque;
use std::sync::{Arc, Mutex};

/// Represents an item in the abstract abacus sequence (0-9).
#[derive(Debug, Clone)]
pub enum AbacusItem {
    Zero(usize), // 0 represents a zero at index i.
    One(usize),   // 1 represents one at index j > i.
}

/// The internal state of the abacus engine using Arc for thread safety.
type State = VecDeque<AbacusItem>;

impl Default for AbacusState {
    fn default() -> Self {
        vec![Zero(0), One(1)]
    }
}

#[derive(Debug, Clone)]
pub struct AbstractAbacusEngine;

/// A single step in the recursive division-by-one logic.
struct Step<'a> {
    // The current index we are processing (i) and its value (v).
    pub i: usize,
    // The next item to be added based on the rule of "divide by one".
    // If v > 0, add '1' at position `i+1`. Otherwise, it's a zero.
    pub step_value: Option<AbacusItem>,
}

/// Handles asynchronous input from an external source (e.g., JSON or stream).
pub struct AbacusEngine<'a> {
    // State is managed via Arc for thread safety across the async context.
    state: Arc<Mutex<State>>,
    
    // Buffer to hold parsed data before processing starts, keyed by index.
    input_buffer: VecDeque<Vec<u8>>;

    /// The current step being executed (i.e., what value we're currently adding).
    pub active_step_value: Option<AbacusItem>,
}

impl<'a> AbacusEngine<'a> {
    /// Creates a new engine with default state.
    #[allow(clippy::too_many_arguments)]
    pub fn new(input_buffer: VecDeque<Vec<u8>>) -> Self {
        let mut buffer = input_buffer.clone();
        
        // Initialize the abacus sequence (0-9) starting at index 0.
        let mut items = vec![Zero(0), One(1)];

        for item in &mut items {
            if let Some(&item_index) = buffer.iter().position(|&b| b == *item).and_then(|i| i.saturating_sub(buffer.len())) {
                // If the index is valid, add one to it.
                if item != Zero(item_index) && item > 0 {
                    items.push(One(*item));
                } else {
                    items[items.iter().position(|&b| b == *item).unwrap()].push(Zero(*item_index));
                }
            }
        }

        // Start the buffer at index 0. The first item is always Zero(0) to ensure we don't go negative.
        let mut items = vec![Zero(0), One(1)];
        
        for i in &mut items {
            if let Some(&item_index) = buffer.iter().position(|&b| b == *i).and_then(|j| j.saturating_sub(buffer.len())) {
                // If the index is valid, add one to it.
                if item != Zero(item_index) && item > 0 {
                    items.push(One(*item));
                } else {
                    items[items.iter().position(|&b| b == *i).unwrap()].push(Zero(*item_index));
                }
            }
        }

        // Start the buffer at index 0. The first item is always Zero(0) to ensure we don't go negative.
        let mut items = vec![Zero(0), One(1)];
        
        for i in &mut items {
            if let Some(&item_index) = buffer.iter().position(|&b| b == *i).and_then(|j| j.saturating_sub(buffer.len())) {
                // If the index is valid, add one to it.
                if item != Zero(item_index) && item > 0 {
                    items.push(One(*item));
                } else {
                    items[items.iter().position(|&b| b == *i).unwrap()].push(Zero(*item_index));
                }
            }
        }

        // Start the buffer at index 0. The first item is always Zero(0) to ensure we don't go negative.
        let mut items = vec![Zero
