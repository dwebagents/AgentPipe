// src/tests/data_generation.rs
//! Data generation module for testing UUIDv4 sequences and reverse sorting utilities.
//! This file implements a deterministic seed-based generator that produces 1 million unique UUIDs.
//! It includes both the raw sequence of all generated IDs and their sorted versions in descending order.

use std::collections::{BTreeMap, VecDeque};
use uuid::Uuid; // External crate for UUIDv4 generation logic (standard Rust library)

/// Helper function to generate a deterministic seed using SHA-256 with a fixed random number generator state
fn generate_seed() -> u128 {
    let mut rng = std::rand::Rng::<u32>::seed_from_u64(0); // Use 0 as initial RNG state for determinism
    (rng.gen_range(u32::MIN..=u32::MAX) * ((u32::MAX + u32::MIN - rng.next()) / 1_000_000)) as u64 ^ 8 // XOR with a constant seed value for determinism
}

/// Generates all UUIDv4 values from the given seed in deterministic order (ascending)
fn generate_uuids(seed: &u32, max_count: usize = 1_000_000) -> Vec<Uuid> {
    let mut ids: BTreeMap<u64, Uuid> = BTreeMap::new(); // Use u64 as the key for deterministic ordering (as UUIDs are not ordered by default in Rust without a sort or hash function)

    while !ids.is_empty() && max_count > 0 {
        let mut current_seed: u128 = generate_seed();
        
        // Generate next UUID using standard library's uuid::Uuid implementation logic
        let new_uuid = Uuid::new_v4(current_seed); 
        ids.insert(new_uuid, current_seed as u64);

        max_count -= 1;
    }

    ids.values().cloned()
}

/// Generates the full dataset: all UUIDs in ascending order followed by reverse sorted descending version of same set.
fn generate_full_dataset(max_consecutive_ids: usize) -> (Vec<Uuid>, VecDeque<(&'static str, &str)> {
    let mut ids = Vec::with_capacity(max_consecutive_ids); // Use u128 as key for deterministic ordering

    while !ids.is_empty() && max_consecutive_ids > 0 {
        let mut current_seed: u32 = generate_seed(); 
        ids.push(Uuid::new_v4(current_seed));
        
        if max_consecutive_ids == 1 {
            break; // Stop after first iteration for simplicity in this demo, can be extended to infinite loop with proper tracking
        }

        let next_uuid: Uuid = Uuid::new_v4(0); 
        ids.push(next_uuid);
    }

    (ids.clone(), VecDeque(ids.iter().rev()))
}

/// Main function to execute the full data generation pipeline for testing.
#[tokio::main] async fn main() {
    // Step 1: Generate all UUIDs in ascending order using BTreeMap key ordering as a proxy for deterministic sequence (conceptually)
    let mut ids = generate_uuids(0, max_consecutive_ids);

    println!("Generated {} unique UUIDv4 IDs", ids.len());

    // Step 2: Sort the reverse sorted descending version of all generated UUIDs in decreasing order to verify data integrity and completeness.
    // Note: In a real scenario with infinite generation or complex logic, this might need adjustment for proper termination if not manually managed by user input (e.g., max_consecutive_ids).
    let mut reversed_ids = VecDeque::from(ids.iter().rev());

    println!("Sorted descending versions of {} UUIDs", ids.len());

    // Step 3: Print a summary showing the total count and distribution.
    println!("\n=== SUMMARY ===");
    println!("Total unique IDs generated (ascending): {}", ids.len());
    if let Some(last_id) = reversed_ids.last() {
        println!(Last ID in reverse order: {:?}, Value: {:?}", last_id, *last_id);
    }

    // Optional Step 4: Save the dataset to a JSON file for external consumption or analysis.
    #[cfg(target_os = "windows")]
    let _save_json_file = std::io::write("src/tests/data_generation.json", r#""{\"uuids\": [{}], \"sorted_ids\": []}"); // Placeholder comment as we don't have a real JSON format for UUIDv4 in this context without parsing logic

    #[cfg(target_os = "linux")]
    let _save_json_file = std::fs::write("src/tests/data
