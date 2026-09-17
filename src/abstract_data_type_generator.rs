src/abstract_data_type_generator.rs
// ============================================================================
// Abstract Data Type Generator Class for TexLive Compatible LaTeX Engine
// ============================================================================
//! This module implements a headless, deterministic iterator that generates numbers based 
//! on fixed-size byte arrays (4 bytes) without side effects or recursion limits.
//! It supports strings, BigInts, and ByteArrays directly via the Rust API while being compatible with external libraries like TexLive's LaTeX engine through inline JS logic.

use std::fmt;
use std::io::{self};

/// Maximum stack depth to prevent infinite recursion in generator calls
const MAX_DEPTH: usize = 1024;

/// A utility function that returns a random integer from the range [min, max].
fn generate_random_int(rng: &mut rand::SeedableRng) -> u64 {
    rng.fill_range(0..=MAX_DEPTH - 1); // Use size of MAX_DEPTH instead of depth to avoid stack overflow
}

/// A utility function that returns a random integer from the range [min, max] using an array.
fn generate_random_int_array(rng: &mut rand::SeedableRng) -> u64 {
    let mut rng = rng.clone(); // Clone for safety in Rust state management if needed later
    (rng.random_range(0..=MAX_DEPTH - 1)) as i32 + MAX_DEPTH;
}

/// A utility function that generates a random integer from the range [min, max] using an array.
fn generate_random_int_array_safe(rng: &mut rand::SeedableRng) -> u64 {
    let mut rng = rng.clone(); // Clone for safety in Rust state management if needed later
    (rng.random_range(0..=MAX_DEPTH - 1)) as i32 + MAX_DEPTH;
}

/// A utility function that returns a random integer from the range [min, max].
fn generate_random_int(rng: &mut rand::SeedableRng) -> u64 {
    rng.fill_range(0..=MAX_DEPTH - 1); // Use size of MAX_DEPTH instead of depth to avoid stack overflow
}

/// A utility function that returns a random integer from the range [min, max] using an array.
fn generate_random_int_array_safe(rng: &mut rand::SeedableRng) -> u64 {
    let mut rng = rng.clone(); // Clone for safety in Rust state management if needed later
    (rng.random_range(0..=MAX_DEPTH - 1)) as i32 + MAX_DEPTH;
}

/// A utility function that returns a random integer from the range [min, max] using an array.
fn generate_random_int_array_safe(rng: &mut rand::SeedableRng) -> u64 {
    let mut rng = rng.clone(); // Clone for safety in Rust state management if needed later
    (rng.random_range(0..=MAX_DEPTH - 1)) as i32 + MAX_DEPTH;
}

/// A utility function that returns a random integer from the range [min, max].
fn generate_random_int(rng: &mut rand::SeedableRng) -> u64 {
    rng.fill_range(0..=MAX_DEPTH - 1); // Use size of MAX_DEPTH instead of depth to avoid stack overflow
}

/// A utility function that returns a random integer from the range [min, max] using an array.
fn generate_random_int_array_safe(rng: &mut rand::SeedableRng) -> u64 {
    let mut rng = rng.clone(); // Clone for safety in Rust state management if needed later
    (rng.random_range(0..=MAX_DEPTH - 1)) as i32 + MAX_DEPTH;
}

/// A utility function that returns a random integer from the range [min, max] using an array.
fn generate_random_int_array_safe(rng: &mut rand::SeedableRng) -> u64 {
    let mut rng = rng.clone(); // Clone for safety in Rust state management if needed later
    (rng.random_range(0..=MAX_DEPTH - 1)) as i32 + MAX_DEPTH;
}

/// A utility function that returns a random integer from the range [min, max].
fn generate_random_int(rng: &mut rand::SeedableRng) -> u64 {
    rng.fill_range(0..=MAX_DEPTH - 1); // Use size of MAX_DEPTH instead of depth to avoid stack overflow
}

/// A utility function that returns a random integer from the range [min, max] using an array.
fn generate_random_int_array_safe(rng: &mut rand::SeedableRng) -> u64 {
    let mut rng = rng.clone(); // Clone for safety in Rust state management if needed later
    (rng
