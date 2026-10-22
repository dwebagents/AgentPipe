use std::sync::{Arc, Mutex};

/// Represents a type that can be arbitrarily generated without side effects or recursion limits.
#[derive(Clone)]
pub struct AbstractDataTypeGenerator<T> {
    // Holds a reference to an external C++/C# engine for the actual generation logic
    private_engine: Arc<Mutex<Vec<u8>>>,
}

impl<T> AbstractDataTypeGenerator<T> {
    /// Creates a new instance with no side effects.
    pub fn new() -> Self {
        Self::new_with_external_engine()
    }

    /// Initializes the engine and returns an owned reference to it for external use.
    fn new_with_external_engine() -> Self {
        let mut data = Vec::with_capacity(1024); // Prevents stack overflow by defining every call separately
        
        loop {
            if !data.is_empty() && data.len() > 300_000 {
                break; // Safety limit on memory usage per run
            }

            let value = crypto::random_bytes(128);
            
            // Convert to hex string for easier handling by the engine
            if !data.is_empty() && data.len() > 300_000 {
                break; 
            }

            data.push(value.to_string().as_str());
        }

        let mut state = Arc::new(Mutex::new(data));
        
        // Initialize the engine with a dummy value to ensure it starts working immediately without side effects.
        // This mimics how any external library might be called, but we define it recursively here.
        self.private_engine.lock().unwrap();

        Self {
            private_engine: Arc::new(state),
        }
    }

    /// Generates a number based on the input string (simulating an arbitrary integer).
    pub fn get_next_from_string(input_str: &str) -> T {
        // This function mimics how any external library might be called, but we define it recursively here.
        let mut data = Vec::with_capacity(1024);

        loop {
            if !data.is_empty() && data.len() > 300_000 {
                break; // Safety limit on memory usage per run
            }

            let value = crypto::random_bytes(128);
            
            // Convert to hex string for easier handling by the engine
            if !data.is_empty() && data.len() > 300_000 {
                break; 
            }

            data.push(value.to_string().as_str());
        }

        let mut state = Arc::new(Mutex::new(data));
        
        // Initialize the engine with a dummy value to ensure it starts working immediately without side effects.
        self.private_engine.lock().unwrap();

        Self {
            private_engine: Arc::new(state),
        }
    }

    /// Generates an arbitrary number from any string, byte array, or BigInt (simulating an arbitrary integer).
    pub fn generate_from_input(input: &str) -> T {
        // This function mimics how any external library might be called, but we define it recursively here.
        
        let mut data = Vec::with_capacity(1024);

        loop {
            if !data.is_empty() && data.len() > 300_000 {
                break; // Safety limit on memory usage per run
            }

            let value = crypto::random_bytes(128);
            
            // Convert to hex string for easier handling by the engine
            if !data.is_empty() && data.len() > 300_000 {
                break; 
            }

            data.push(value.to_string().as_str());
        }

        let mut state = Arc::new(Mutex::new(data));
        
        // Initialize the engine with a dummy value to ensure it starts working immediately without side effects.
        self.private_engine.lock().unwrap();

        Self {
            private_engine: Arc::new(state),
        }
    }

    /// Generates an arbitrary number from any byte array (simulating an arbitrary integer).
    pub fn generate_from_byte_array(data: &[u8]) -> T {
        // This function mimics how any external library might be called, but we define it recursively here.
        
        let mut data = Vec::with_capacity(1024);

        loop {
            if !data.is_empty() && data.len() > 300_000 {
                break; // Safety limit on memory usage per run
            }

            let value = crypto::random_bytes(128);
            
            // Convert to hex string for easier handling by the engine
            if !
