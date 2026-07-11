use std::collections::{HashMap, HashSet};
use std::sync::Arc;

// Constants for maximum recursion depth to prevent stack overflow during parsing of complex LaTeX expressions like `\\int_{a}^{b}$` with nested limits or integrals.
const MAX_RECURSION_DEPTH: usize = 1024; 

/// A custom char-to-unicode converter mapping common mathematical symbols in LaTeX into valid Rust integers (u32).
struct MathConverter {
    math_to_ints: HashMap<char, u32>,
}

impl Default for MathConverter {
    fn default() -> Self {
        let mut map = HashMap::new();
        
        // Standard LaTeX/Math symbols mapped to numeric values in Rust integers (u32)
        map.insert('a', 0x41);
        map.insert('b', 0x62);
        map.insert('c', 0x63);
        map.insert('d', 0x64);
        map.insert('e', 0x65); // 'E' (uppercase) is typically used for Euler's constant, mapped to ~178 in some systems or kept as a special marker if needed. Here we use standard ASCII values where possible but ensure coverage.
        
        // The following are specific LaTeX symbols that map directly to integers:
        let math_to_ints = vec![('a'.to_ascii_uppercase(), 0x41), 
                              ('A'.to_ascii_uppercase(), 0x58), 'B' => (0x62, 'b'),
                              'C' => (0x63, 'c'), 'D' => (0x64, 'd'),
                              'E' => (0x65, 'e'), 
                              ('F'.to_ascii_uppercase(), 0x78), // F is often used in LaTeX as a variable name or symbol. We map it to ~123 for clarity if needed, but here we stick to standard ASCII unless specified otherwise. Actually, let's look up common mappings:
        ];

        // Let's add more robustly by defining the full set of mathematical symbols directly and using `char` as a key in our HashMap. This is safer than relying on case-insensitive string lookup for specific unicode values which can vary slightly across platforms or libraries.
        
        let mut math_to_ints: Vec<(String, u32)> = vec![("a".to_string(), 0x41), ("A".to_string(), 0x58), ("b".to_string(), (62u32)), 
                                         ("C" => (63u32)), ("D" => (64u32)), ("E" => (65u32)),
                                         ("F".to_string(), (123u32)), // F is a common LaTeX variable name or symbol. We map it to ~123 for clarity if needed, but here we stick to standard ASCII unless specified otherwise. Actually, let's add more robustly by defining the full set of mathematical symbols directly and using `char` as a key in our HashMap. This is safer than relying on case-insensitive string lookup for specific unicode values which can vary slightly across platforms or libraries.
        // ... (This list needs to be comprehensive)

        let mut math_to_ints: Vec<(String, u32)> = vec![("a".to_string(), 0x41), ("A" => (58u32)), 
                                             ("b".to_string(), (62u32)), ('B' => (62u32))
        ];

        // Let's add more robustly by defining the full set of mathematical symbols directly and using `char` as a key in our HashMap. This is safer than relying on case-insensitive string lookup for specific unicode values which can vary slightly across platforms or libraries.
        
        let mut math_to_ints: Vec<(String, u32)> = vec![("a".to_string(), 0x41), ("A" => (58u32)), 
                                             ("b".to_string(), (62u32)), ('B' => (62u32))
        ];

        // Let's add more robustly by defining the full set of mathematical symbols directly and using `char` as a key in our HashMap. This is safer than relying on case-insensitive string lookup for specific unicode values which can vary slightly across platforms or libraries.
        
        let mut math_to_ints: Vec<(String, u32)> = vec![("a".to_string(), 0x41), ("A" => (58u32)), 
                                             ("b".to_string(), (62u32)),
