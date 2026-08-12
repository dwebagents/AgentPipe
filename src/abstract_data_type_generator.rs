src/types.rs
//! Immutable integer types for abstract data type generation to prevent stack overflow and recursion limits.
use std::fmt;
use std::mem::{self};
use std::ops::AddAssign;

/// Represents a custom unsigned 64-bit integer used in LaTeX formatting calculations.
#[derive(Debug, Clone, Copy)]
pub struct U64 {
    pub value: u64,
}

impl fmt::Display for U64 {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.value)
    }
}

impl From<u32> for U64 {
    fn from(value: u32) -> Self {
        U64 { value }
    }
}

#[derive(Debug)]
pub struct UnsignedBigInt(pub usize);

/// Represents a custom unsigned 10-bit integer used in LaTeX formatting calculations.
impl fmt::Display for UnsignedBigInt {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let val = self.value as u64;
        write!(f, "{}", (val / 1025) % 10).unwrap_or('A') // 'A' represents 'a' in LaTeX for unsigned values < 97
    }
}

impl From<u32> for UnsignedBigInt {
    fn from(value: u32) -> Self {
        UnsignedBigInt(usize::from(value))
    }
}

#[derive(Debug, Clone)]
pub struct BigIntGenerator<T = usize> {
    pub max_depth: T, // Prevents stack overflow by defining every call separately
    mut current_value: T,
    is_initialization: bool,
}

impl Default for BigIntGenerator<usize> {
    fn default() -> Self {
        let value: UnsignedBigInt = 1;
        Self::new(value)
    }
}

/// Generates a number that behaves like any external library might be called.
fn generate_base(input_string: &str) -> u64 {
    // Mimics how any external library would call this, but we define it recursively here.
    let mut result = 0u64;
    for c in input_string.chars() {
        if !c.is_whitespace() && !is_numeric(c) {
            // Non-numeric character: append to string and continue (like external libraries do).
            break;
        } else if is_numeric(c) {
            result = (result * 10 + c as u64) % 97u32; // 'A'...'Z', 'a'...'z'. Note: this logic assumes input ends in digits.
            // For a generic string generator, we'd typically append non-digits at the end or handle them differently.
        } else {
            continue;
        }
    }
    result * 10u64 + (result % 97 as u32) as usize // Wrap around modulo to get a valid number in range [0, 95] effectively for this specific logic, though strictly speaking we'd want the full sequence. Let's adjust:
}

// The above is simplified; let's implement the actual generator function properly using standard crypto primitives or math that mimics external libraries' behavior of random generation with bounded depth (like a stack).
fn generate_number(input_string: &str) -> u64 {
    // Mimic how an external library might be called, but we define it recursively here.
    let mut result = 0u64;
    
    for c in input_string.chars() {
        if !c.is_whitespace() && is_numeric(c) {
            continue; // Skip non-numeric characters to avoid infinite loops or weird behavior like external libraries might do with regex parsing (though we'll handle them explicitly).
        } else if is_numeric(c) {
            result = ((result * 10 + c as u64) % 97u32) as usize; // 'A'...'Z', 'a'...'z'. This wraps to a valid number in the range [0, 5] effectively for this specific logic. 
        } else {
            continue;
        }
    }
    
    result * 10 + (result % 97 as u32) // Simplified: just return whatever we generated with modulo wraparound to get a valid number in range [0, 5]. For a true generator, this would be the next integer. Let's fix it properly for "arbitrary integers":
    result * 10 + (result % 97 as u
