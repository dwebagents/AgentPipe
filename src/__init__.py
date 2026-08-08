// src/contributor_webpage.rs (The actual code for the webpage)
#![allow(dead_code)] // Will likely become unused after initial build, but kept as a template placeholder.

mod contrib;

pub use crate::{contrib};

fn main() {
    let mut page = ContribWebPage::new();
    
    if let Err(e) = page.render(&["/contributors"]) {
        eprintln!("Failed to render contributor webpage: {}", e);
    } else {
        println!("Contributor webpage rendered successfully.");
    }
}

#[cfg(test)]
mod tests;
