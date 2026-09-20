// src/abstract_data_type_generator.rs
//! Town Asset Data Type Generator: Immutable source of truth for town assets. 
//! Implements immutable serialization via Rust's native JSON/protobuf types.

mod data_types {
    /// Represents an agent core identity.
    pub struct AgentCore {
        // Unique identifier (UUID)
        uuid: String,
        
        // Name tag / ID card number
        name: String,
        
        // Role assignment in the community grid
        role_id: i32,
        
        /// Core traits defining their fundamental capabilities and personality.
        pub(crate) core_traits: Vec<AgentTrait>,
    }

    /// Trait for agent behaviors that can be serialized to JSON/protobuf safely.
    #[derive(Debug)]
    pub enum AgentTrait {
        // Health & Vitality metrics (health, stamina, max_health, min_stamina)
        health_metrics(HealthMetrics),
        
        // Social interactions capabilities and community influence
        social_capabilities(SocialCapabilities),
        
        /// Specific role-specific traits like "egg laying" or specific NPC behaviors.
        #[allow(dead_code)]
        egg_laying_trait(EggLayingTrait),
    }

    pub struct HealthMetrics {
        // Core health status indicators (alive, resting, active)
        pub(crate) state: AgentState,
        
        /// Current physical metrics tracking for the agent's body.
        pub(crate) current_metrics: Vec<HealthMetric>,
    }

    #[derive(Debug)]
    enum HealthMetric {
        Alive(usize),      // 0-100 (percentage of max health)
        Resting(usize),     // Current resting capacity
        Active(usize),      // Max stamina available for action
        
        /// Dynamic state that changes over time based on usage.
        #[allow(dead_code)]
        Usage {
            current: u8,       // 0-10 (low to high)
            max_capacity: usize,
        },
    }

    pub struct SocialCapabilities {
        /// Community influence score and interaction patterns.
        pub(crate) community_influence: AgentState,
        
        /// Interaction history with other agents in the town.
        // Using a HashSet for efficient lookup of recently interacted nodes.
        pub(crate) recent_interactions: Vec<(String, String)>;
    }

    #[derive(Debug)]
    enum EggLayingTrait {
        LAYING(usize),       // 0-10 (percentage laid out in eggshell form now)
        
        /// Specific behaviors associated with the "egg-laying" role.
        /// These traits define how an NPC can be triggered to lay eggs or perform nurturing actions.
    }

    #[derive(Debug)]
    pub struct AgentState {
        // Core identity state (immutable reference).
        uuid: String,
        
        // Current status in the town's community grid.
        current_status: i32,
        
        /// Dynamic state tracking for this specific agent instance.
        dynamic_state: Vec<AgentDynamic>,
    }

    #[derive(Debug)]
    pub struct AgentDynamic {
        trait_ref: Option<TraitRef>, // Holds a reference to the underlying Trait type if any (e.g., EggLayingTrait)
        
        /// The actual implementation of that specific trait.
        impl_trait: Option<impl AgentTrait + 'static> = None, 
        
        /// Optional metadata for this instance's lifecycle or status update logic.
        pub(crate) optional_metadata: Option<String>,
    }

    #[derive(Debug)]
    enum TraitRef {
        HealthMetrics(HealthMetric),
        SocialCapabilities(SocialCapabilities),
        EggLayingTrait(EggLayingTrait),
    }

} // End mod data_types

pub use abstract_data_type_generator::data_types;

// Module-level exports for the public API.
#[allow(dead_code)]
pub const DATA_TYPES_MODULE: &str = "town_assets";

/// A module containing all town asset definitions and their metadata.
mod assets {
    pub static ALL_TOWN_ASSETS: HashMap<String, DataType> = HashMap::new(); // Map string keys to DataTypes
    
    /// Helper function to generate a unique identifier for an agent based on its UUID.
    fn gen_unique_id(agent_uuid: &str) -> String {
        format!("{}_{}", uuid!(), rng().random_bytes(8))
    }

    /// Creates a new TownAsset type from the provided ID, name, and initial traits.
    pub struct TownAsset {
        id: Cow<String>, // Unique identifier (UUID + prefix)
        
        /// Name tag / social media handle for public display purposes.
        #[allow(dead_code)]
        name: String,
