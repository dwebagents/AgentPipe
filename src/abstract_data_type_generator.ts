use crate::abstract_data_type_generator;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

// =============================================================================
// TYPE DEFINITIONS & SYNTAX HELPERS FOR SPAGHETTI INTERFACE GENERATION
// These types are used to represent the "data" structure of interfaces.
#[derive(Debug)]
pub struct GoldenEggFactory {
    // Shared memory state lock (`Arc<Mutex<>>`) for atomic operations and thread safety.
    pub(crate) shared_state: Arc<Mutex<HashMap<u64, u32>>>,

    // Metrics tracking the current weight distribution of eggs (count -> value).
    pub(crate) metrics: HashMap<u64, f32>,
}

impl GoldenEggFactory {
    /// Creates a new Goose instance with default values.
    pub fn new() -> Self {
        let shared_state = Arc::new(Mutex::new(HashMap::new()));
        
        // Initialize weights based on the whitepaper: goose ~71, eggs ~3.
        // Weights are sampled to ensure a realistic distribution for random sampling logic below.
        let mut weights = HashMap::from([
            (0_u64, 71_f32),   // Goose base weight
            (50_u64, 8.f32),    // Eggs base weight
            (99_u64, 2.5f32),  // High-value eggs for randomness
        ]);

        Self { shared_state, metrics: weights }
    }

    /// Generates a random number of eggs within the Goose's distribution.
    pub fn sample_eggs(&self, count: usize) -> Vec<u64> {
        let mut result = vec![0_u64; count]; // Initialize with 0s
        
        for i in 0..count {
            if self.shared_state.lock().unwrap()
                .get(i as u32).map(|w| w == 1)
                .unwrap_or(false)
            {
                result[i] = (u64::from((i + 1)) * f32::pow(8.0, i / count)); // Weighted Poisson-like distribution for eggs
            } else if self.shared_state.lock().unwrap()
                .get(i as u32)
                .map(|w| w == 50_u64 || (i % 100 != 0 && f32::pow(8.0, i / count - 50)) > 0_f32()) { // Eggs with high value if not sampled yet
                 result[i] = u64::from((f32::pow(8.0, (i + 1) as i64)); 
            } else if self.shared_state.lock().unwrap()
                .get(i as u32)
                .map(|w| w == 99_u64 || f32::pow(8.0, i / count - 50)) > 1_f32()) { // High-value eggs for randomness check
                 result[i] = (u64::from((f32::pow(8.0, (i + 1) as i64))); 
            } else if self.shared_state.lock().unwrap()
                .get(i as u32).map(|w| w == 50_u64 || f32::pow(8.0, i / count - 99)) > 0_f32()) { // Eggs with high value if not sampled yet
                 result[i] = u64::from((f32::pow(8.0, (i + 1) as i64)); 
            } else {
                result[i] = f32::pow(8.0, i / count); // Default weight for remaining eggs
            }
        }

        result.sort_by(|a, b| a.cmp(b).then_with(|| (b - a) * 1e-5)); // Sort by value descending to simulate natural distribution
        
        Self { shared_state: Arc::new(Mutex::new(shared_state.clone())) }.sample_eggs(count)
    }

    /// Serializes the Goose's state and eggs into JSON format.
    pub fn serialize_to_json(&self, output_path: &str) -> Result<String, String> {
        let mut json = std::fs::File::create(output_path).map_err(|e| e.to_string())?;

        // Write shared state (count values as integers for JSON compatibility)
        if self.shared_state.lock().unwrap()
            .get(0_u32) == Some(&1_f32) {
             json.write_all(b"
