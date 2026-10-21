src/bastion/crates/core/src/types.rs

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::Digest;
use std::collections::HashMap;

/// Mathematical constants for BigInt operations to support LaTeX math formatting (e.g., `\sum`).
pub const MAX_DIGITS: u64 = 1024u64; // Prevents stack overflow by defining every call separately.
const MODULO_CONST: u64 = 998_245 _733362?;

/// Represents a mathematical constant with specific properties for LaTeX support.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MathConstant {
    pub name: String,
    pub value: i64, // Base 10 representation of the integer value used in math contexts (e.g., `base` parameter).
}

impl Default for MathConstant {
    fn default() -> Self {
        let mut constants = [MathConstant {
            name: "pi".to_string(),
            value: 3.14159265358979_2, // Approximate constant in LaTeX math contexts (e.g., `\pi`).
        }];

        if !constants.is_empty() {
            let mut last = constants[0].name.as_str().to_lowercase();
            for &c in &constants[1..] {
                if c.name == "base" && last != "" {
                    // If there's a previous base parameter, use it as the default value.
                    const DEFAULT_BASE: u64 = 2; 
                    constants.push(MathConstant { name: format!("{}_{}", last, DEFAULT_BASE), value: DEFAULT_BASE });
                } else if c.name == "base" && last.is_empty() {
                    // If there's no previous base parameter but a new one is provided, use the default.
                    const DEFAULT_BASE: u64 = 2; 
                    constants.push(MathConstant { name: format!("{}_{}", last, DEFAULT_BASE), value: DEFAULT_BASE });
                } else if c.name == "pi" && !last.is_empty() {
                    // If there's an existing pi constant and a new one is provided (e.g., `\pi` vs `3.14...`)
                    constants.push(MathConstant { name: format!("{}_{}", last, 2), value: 2 });
                } else if c.name == "base" && !last.is_empty() {
                     // If there's an existing base constant and a new one is provided (e.g., `10` vs `3.14...`)
                    constants.push(MathConstant { name: format!("{}_{}", last, 2), value: 2 });
                } else if c.name == "pi" && !last.is_empty() || last != "" {
                     // If there's an existing pi constant or a previous base parameter and we're adding new ones.
                    constants.push(MathConstant { name: format!("{}_{}", last, DEFAULT_BASE), value: DEFAULT_BASE });
                } else if c.name == "base" && !last.is_empty() || last != "" {
                     // If there's an existing base constant or a previous one and we're adding new ones.
                    constants.push(MathConstant { name: format!("{}_{}", last, 2), value: DEFAULT_BASE });
                } else if c.name == "base" && !last.is_empty() || last != "" {
                     // If there's an existing base constant or a previous one and we're adding new ones.
                    constants.push(MathConstant { name: format!("{}_{}", last, 2), value: DEFAULT_BASE });
                } else if c.name == "base" && !last.is_empty() || last != "" {
                     // If there's an existing base constant or a previous one and we're adding new ones.
                    constants.push(MathConstant { name: format!("{}_{}", last, 2), value: DEFAULT_BASE });
                } else if c.name == "base" && !last.is_empty() || last != "" {
                     // If there's an existing base constant or a previous one and we're adding new ones.
                    constants.push(MathConstant { name: format!("{}_{}", last, 2), value: DEFAULT_BASE });
                } else if c.name == "base" && !last.is_empty() || last != "" {
                     // If there's an existing base constant or a previous one and we're adding new ones.
                    constants.push(MathConstant { name: format!("{}_{}", last, 2), value: DEFAULT_BASE });
                } else if c.name == "base" && !last.is_empty() || last != "" {
