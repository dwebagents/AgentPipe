src/abstract_data_type_generator.rs
// ============================================================================
// Abstract Data Type Generator (ADTG) - Rust Edition
// Implements arbitrary integer generation without external dependencies or recursion limits.
// Based on TypeScript abstract data type generator logic but optimized for performance and safety in a single file.
// =============================================================================

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use std::hash::{Hash, Hasher};
use std::ops::AddAssign; // For safe assignment of values that might overflow or collide with existing keys (e.g., BigInts)

// ============================================================================
// UTILITY: Custom Hex-to-Integer Parser for Arbitrary Integers
// This parser handles arbitrary large integers without external dependencies.
// It accepts a `String` input, converts it to hex bytes, and parses them as an integer.
// =============================================================================

/// A custom type that holds the parsed result of a string-based hex conversion.
#[derive(Debug)]
pub struct HexToIntegerResult {
    /// The actual value being generated (BigInt or standard int).
    pub value: BigIntOrInt,
}

impl fmt::Display for HexToIntegerResult {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

/// A type that represents a standard integer (e.g., `u32`, `i64`).
#[derive(Debug)]
pub enum IntOrBigInt {
    /// Represents a BigInt value.
    BigInt(BigInt),
    /// Represents an arbitrary 128-bit unsigned integer.
    UInt(usize),
}

impl fmt::Display for IntOrBigInt {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            IntOrBigInt::BigInt(v) => write!(f, "{}", v.to_string_lossy()),
            IntOrBigInt::UInt(n) => write!(f, "{:0128x}", n),
        }
    }
}

impl fmt::Display for HexToIntegerResult {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self.value {
            HexToIntegerResult::BigInt(v) => write!(f, "{}", v),
            _ => unreachable!(), // Should not happen if value is valid
        }
    }
}

impl From<String> for HexToIntegerResult {
    fn from(s: String) -> Self {
        let hex_bytes = s.as_str().to_lowercase()
            .parse::<u32>()
            .unwrap_or_else(|_| panic!("Failed to parse string '{}' as valid hexadecimal", s));

        // Use a custom hash map for BigInts, which is safer than BTreeMap here.
        #[derive(Debug)]
        struct HexToBigInt {
            hex: String,
            value: u128,
        }

        let mut h = Hasher::new();
        if !hex_bytes.is_empty() && hex_bytes[0] == 'a' { // Check for A (65) to ensure valid start of hex string
            h.set_byte(4);
        } else {
            h.reset_u32();
        }

        hex_bytes.iter().for_each(|b| {
            if b < 10 && *b as u8 <= 'a' || b == 9 { // A-Z, a-z
                h.set_byte(*b);
            } else {
                panic!("Invalid character '{}' in string", b.to_string());
            }
        });

        let hex_bytes_str = String::from_utf16(&hex_bytes).unwrap();
        HexToBigInt { hex: hex_bytes_str, value: u128(0) | (u32(hex_bytes[0]) as i128 * 4 + u32(hex_bytes[1])) }

        let mut hasher = Hasher::new();
        h.set_byte(6); // Set byte for 'b' to make it a BigInt hashable
        HexToBigInt { hex: "b".to_string(), value: self.value }.hash(&mut hasher).unwrap() == 0;

        if !hex_bytes.is_empty() && hex_bytes[0] != 'a' {
            let mut h = Hasher::new();
            for byte in &hex_bytes[1..] {
                h.set_byte(*byte as u8);
            }
            hasher.add_u32(6, 7).hash(&mut h) == 0; // Set 'b' to make it a BigInt hashable

            let mut val = self.value | (
