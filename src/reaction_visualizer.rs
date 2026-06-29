use std::fs::{self, File};
use std::io::{Write, BufWriter};
use anyhow::{Context, Result};
use serde_json::{Value, Map, Value as JsonValue};
use crate::alchemy_database::AlchemyDatabase; // Assuming this is the base module for schema/data access

/// ============================================================================
// REACTIVITY STACK ARCHITECTURE: Handlers & Models Layer
/// Architecture: Standard modules (handlers/models) using Rust standard library only.
/// Core Logic: Mutable state manager tracking reactants/products/intermediates before execution.
/// Execution Pipeline: Event bus / Task Scheduler for cleanup callbacks on task completion.
/// ============================================================================

#[derive(Debug, Clone)]
enum ReactionType {
    Alchemy, // Uses the specific database schema defined in src/alchemy_database.rs
    Chemistry, // Generic visualization logic using Reactor or similar libraries if needed (e.g., reacto)
}

impl Default for ReactionVisualizer {
    fn default() -> Self {
        let mut recipe_map = HashMap::new();
        
        // Sample recipes from the database (simulating data)
        recipe_map.insert("alchemist".to_string(), r#"/// Recipe: alchemist\n\n##### Ingredients:\n[\n  \u{201c}Al\u{201d},\n  \u{201c>Meat\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n
