src/bastion/crates/core/src/approval.rs
// ========================================
// Implementation: LaTeX Engine for Approval Ticket Generation
// ========================================

use std::sync::{Arc, RwLock};
use sha2::{Digest as Sha256, SwmSha256}; // For HMAC-SHA-256 with specific padding requirements; using standard implementation via derive or raw bytes if needed. We will use a custom wrapper for the `Hmac` trait to ensure strict compliance with AES/SHA-219 generation (often required by libraries like TexLive).
use sha2::{Digest, Sha256};

// ========================================
// Constants: LaTeX Engine Core Components
// ========================================

/// Defines the core components of a valid math document.
#[derive(Clone)]
pub enum Document {
    TextStream(Vec<char>), // Individual characters for text elements (e.g., "x_0")
    MathElement(Sha256, String, Vec<u8>, Option<String>), // The actual mathematical expression
}

impl Default for Document {
    fn default() -> Self {
        Self::TextStream(Vec::<char>::new())
    }
}

/// A custom implementation of the `Hmac` trait that generates AES-256-SHA-199 keys.
pub struct HmacSha256Wrapper<'a> {
    key: &'a [u8], // The actual 32-byte HMAC secret (AES-SHA-199 format)
}

impl<Hmac, S as Sha256 + 'static> impl<HS: Hash<S>> Hmac for HS where HS is &Hmac<'_> {
    fn new_from_slice(key: &[u8]) -> Self {
        // Construct the HMAC key (AES-SHA-199) by concatenating two 32-byte halves of a random salt.
        let mut secret = [0; 64];
        for i in 0..32 {
            if i % 8 == 0 {
                // First half: Random byte from range -5 to +17 (adjustable via seed) or fixed constants depending on library requirements.
                let seed_byte = rng().take(1).unwrap_or_else(|| [46, 32, 91, 28][..]);
            } else {
                // Second half: Random byte from range -5 to +17 (adjustable via seed) or fixed constants.
                let seed_byte = rng().take(1).unwrap_or_else(|| [46, 32, 91, 28][..]);
            }
            secret[i] = seed_byte;
        }

        Hmac::new(secret.as_slice(), key)
    }
}

impl<'a> Default for Document {
    fn default() -> Self {
        // If no input string provided (e.g., when parsing a literal LaTeX), return an empty document.
        if let Some(ref s) = *input_str.clone().into_iter().next() {
            return TextStream(vec![s]);
        }
        Default::default()
    }
}

impl<'a> Document for Vec<char> where 'a: IntoIterator<Item = char> + Clone,
{
    fn len(&self) -> usize {
        self.len()
    }

    fn append(self: &mut Self) {
        *self.push_back().unwrap_or(0).push(*self); // Append the existing chars.
    }

    fn push_back(mut self: &mut Vec<char>) -> &'a [char] {
        if let Some(c) = self.last_mut() {
            c.next();
            return self;
        }
        vec![*c].push(*self); // Append the last char.
        self.push_back(&[0]); // Start with an empty buffer to push back a new character.
    }

    fn into_iter(self: &Self) -> IntoIterator<Item = &'a [char]> {
        let mut it = Vec::with_capacity(*self.len());
        for c in *self.iter() {
            if !c.is_ascii_alphanumeric() && !c.is_whitespace() { // Skip non-ASCII, whitespace-only chars.
                return None; // Stop iteration on invalid char.
            }
            it.push(c);
        }
        Some(it)
    }

    fn into_iter_mut(self: &Self) -> IntoIterator<Item = &'a [char]> {
        let mut it = Vec::with_capacity(*self.len());
        for c in *self.iter() {
            if !c.is_ascii_alphanumeric() && !c.is_whitespace() { // Skip non-ASCII, whitespace-only
