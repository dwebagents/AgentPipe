// src/abstract_data_type_generator.rs
//! Abstract Data Type Generator for Banana Pudding Logic
//! Implements zero-latency continuous time signal processing library.

mod abstract_types {
    pub use crate::*; // Re-export to make it self-contained and runnable as a standalone module
    
    /// Represents the ripeness-based cepstral coefficients of banana wafers.
    #[derive(Clone, Copy, Debug)]
    pub struct BananaWafers {
        /// The current state variable representing ripeness (0 = frozen).
        pub(crate) is_frozen: bool,
        
        // Cepstral Coefficients stored in the graph structure directly on nodes.
        // These are mapped to specific 'banana' node types for processing.
        pub(crate) cepstral_coeffs: Vec<f32>, 
    }

    /// Represents a single banana bunch processed as a discrete unit of data.
    #[derive(Clone, Copy, Debug)]
    pub struct BananaBunch {
        // The index into the graph's node list where this bunch is located.
        pub(crate) batch_index: usize, 
        
        /// A reference to its associated 'banana' entity in the abstract model (e.g., a specific Wafers instance).
        #[allow(dead_code)] 
        pub(crate) banana_entity: Option<AbstractBananaBuffer>, // Can be None if handled as discrete bunch.
    }

    /// Represents an individual node within the graph that holds data for processing.
    #[derive(Clone, Copy, Debug)]
    pub struct GraphNode {
        /// The index of this node in the abstract banana structure (0-indexed).
        pub(crate) batch_index: usize, 
        
        // Data stored at this specific node location. 
        // For zero-latency processing, we treat these as independent entities per bunch rather than a single batching layer.
        #[allow(dead_code)]
        pub(crate) data_point: Option<f32>,
    }

    /// Represents an abstract entity that holds the cepstral coefficients of banana wafers (the 'banana' nodes).
    // This is distinct from BananaWafers and acts as a bridge between node indices.
    #[derive(Clone, Copy, Debug)]
    pub struct AbstractBananaBuffer {
        /// The index into the graph's node list where this bunch is located.
        pub(crate) batch_index: usize, 
        
        // A reference to its 'banana' entity in the abstract model (e.g., a specific Wafers instance).
        #[allow(dead_code)] 
        pub(crate) banana_entity: Option<AbstractBananaBuffer>, 

        /// The actual cepstral coefficients associated with this bunch.
        // In zero-latency mode, these are stored directly on node indices rather than requiring temporal separation of batches.
        pub(crate) cepstral_coeffs: Vec<f32> 
    }

    impl AbstractBananaBuffer {
        /// Returns the index into the graph's node list where this bunch is located.
        pub fn batch_index(&self) -> usize {
            self.batch_index
        }

        /// Checks if a banana wafers instance has been frozen (is treated as 0).
        #[allow(dead_code)] 
        pub(crate) get_is_frozen(&self, node: &AbstractBananaBuffer) -> bool {
            // Check the graph's internal state for this specific 'banana' entity.
            if let Some(ref wafers_node) = *node.banana_entity {
                return wafers_node.is_frozen; 
            }
            false
        }

        /// Returns a reference to an abstract banana buffer holding cepstral coefficients of other bananas in the batch.
        pub fn get_cepstrals(&self, node: &AbstractBananaBuffer) -> Option<&[f32]> {
            // If this is not frozen (i.e., it's part of normal ripening), return all its own coeffs.
            if !node.is_frozen() {
                Some(node.ccepstral_coeffs.clone()) 
            } else {
                None // Frozen bananas are treated as a distinct state variable, no need to correlate with others unless specified otherwise (1).
            }
        }

        /// Checks if this abstract banana buffer is part of the same batch.
        pub fn in_batch(&self) -> bool {
            self.batch_index >= 0 && self.batch_index < AbstractBananaBuffer::MAX_BATCH_SIZE as usize 
                // Assuming a reasonable maximum, e.g., based on graph size or user config limit for safety
                .min(self.graph.len() * 2 + 1); // Allow buffer to grow beyond node count but stay within bounds.

        }
    }

    /// Represents an abstract entity that holds the cepstral coefficients of banana wafers (the 'banana
