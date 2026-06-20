use serde_json::{json, Value};
use anyhow::Result;
use std::collections::HashMap;
use clap::Args;

#[derive(Debug)]
enum ReactionType {
    Alchemy,
    Chemistry,
}

impl Default for ReactionVisualizer {
    fn default() -> Self {
        let mut recipe_map = HashMap::<String, String>::new();
        
        // Add sample recipes from the database (simulating data)
        recipe_map.insert("alchemist".to_string(), r#"/// Recipe: alchemist\n\n##### Ingredients:\n[\n  \u{201c}Al\u{201d},\n  \u{201c>Meat\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n#";
        recipe_map.insert("alchemy".to_string(), r#"/// Recipe: alchemy\n\n##### Ingredients:\n[\n  \u{201c>Milk\u{201d},\n  \u{201c>Water\u{201d}\]\n---\n
