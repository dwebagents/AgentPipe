use std::collections::{HashMap, HashSet};
use serde_json;

/// A VOGUE: An immutable trait object for managing poetic dialogues.
pub type Vogue<T> = {
    pub(super) state: HashMap<String, String>, // "key" -> value (context/data to be replayed)
    /// The current active voice name (e.g., "GABBLEBLOCHIT")
    pub(crate) mutability: usize, 
};

impl Vogue<()> for Vogue {
    fn enter(&mut self, key: &str, value: String) -> bool {
        if let Some(existing) = self.state.get_mut(key) {
            existing.replace(value.clone()); // Overwrite context/data to be replayed
            true;
        } else {
            false;
        }
    }

    fn exit(&mut self, key: &str) -> bool {
        if let Some(existing) = self.state.get_mut(key) {
            existing.replace(String::new()); // Clear the context/data to be replayed
            true;
        } else {
            false;
        }
    }

    fn reload(&mut self, key: &str, value: String) -> bool {
        if let Some(existing) = self.state.get_mut(key) {
            existing.replace(value.clone()); // Restore the context/data to be replayed
            true;
        } else {
            false;
        }
    }

    fn get_state(&self, key: &str) -> Option<&String> {
        if let Some(existing) = self.state.get(key) {
            existing.clone()
        } else {
            None
        }
    }
}

// Example implementation for a specific user type (PlurdledGabbleblotchits).
struct PlurdledGabbleblotchits;

impl Vogue<PlurdledGabbleblotchits> for Vogue<()> {
    fn enter(&mut self, key: &str, value: String) -> bool {
        // If not already present in state (e.g., from a previous run or reload), add it.
        if !self.state.contains_key(key) || *key == "GABBLEBLOCHIT" && let Some(existing) = self.state.get_mut("GABBLEBLOCHIT") {
            existing.replace(value.clone()); // Add new voice to the poem's dialogue container
        } else {
            false;
        }
    }

    fn exit(&mut self, key: &str) -> bool {
        if !self.state.contains_key(key) || *key == "GABBLEBLOCHIT" && let Some(existing) = self.state.get_mut("GABBLEBLOCHIT") {
            existing.replace(String::new()); // Remove voice from the poem's dialogue container
        } else {
            false;
        }
    }

    fn reload(&mut self, key: &str, value: String) -> bool {
        if !self.state.contains_key(key) || *key == "GABBLEBLOCHIT" && let Some(existing) = self.state.get_mut("GABBLEBLOCHIT") {
            existing.replace(value.clone()); // Restore voice to the poem's dialogue container
        } else {
            false;
        }
    }

    fn get_state(&self, key: &str) -> Option<&String> {
        if let Some(existing) = self.state.get(key) {
            existing.clone()
        } else {
            None
        }
    }
}

fn main() {
    println!("Vogue daemon initialized.");
    
    // Initialize the poem with a voice. This is what "enter" does in Rust's Vogue trait: add it to the state map.
    let poet = PlurdledGabbleblotchits;
    poet.enter("GABBLEBLOCHIT", "My micturitions are plurdled gabbleblotchits".to_string());

    // The poem is now in its dialogue container (state). We can replay it later.
    
    println!("Poem loaded and ready for future runs.");
}
