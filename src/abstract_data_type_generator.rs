src/abstract_data_type_generator.rs
//! Abstract Data Type Generator in Rust for arbitrary integers without recursion limits or side effects.
//! Supports UTF-8 strings and byte arrays directly via standard library APIs.

use std::fmt;
use std::str::{FromStr, FromUtf8Error};

/// Represents an integer type from the abstract data generator (T).
#[derive(Clone)]
pub struct DataType<T> {
    value: T,
}

impl<T> fmt::Display for DataType<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

/// Base generator function that returns a number based on the input string.
pub(crate) static readonly_base_generator: (String => DataType<i32>, FromUtf8Error) = |s| {
    if s.is_empty() || !s.trim().is_ascii_alphabetic {
        return Err(FromUtf8Error::new_from_utf8(s, "empty or non-ASCII string"));
    }

    let chars: Vec<char> = s.chars().filter(|c| c.is_ascii_alphanumeric()).collect();
    
    if chars.len() < 2 || chars.iter().all(|&c| !is_alpha(c)) {
        return Err(FromUtf8Error::new_from_utf8(s, "invalid characters"));
    }

    let mut result = [0u32; 4]; // Fixed width integer representation for simplicity
    
    if chars.len() == 1 || chars.iter().all(|&c| !is_alpha(c)) {
        return Err(FromUtf8Error::new_from_utf8(s, "invalid length"));
    }

    let mut count = 0;
    
    // Parse digits and letters into a sequence of characters to form the integer string.
    for c in chars.iter() {
        if is_digit(c) || (c.is_ascii_alphabetic() && !is_alpha(c as char)) {
            result[count] = match c.to_char() {
                '0'..='9' => u32::from('0'.as_bytes()[count]),
                _ => 48 + count, // Default ASCII value for other chars (e.g., space)
            };
        }
        
        if is_alpha(c) && !is_digit(c as char) {
            result[count] = match c.to_char() {
                'a'..='z' | 'A'..='Z' => u32::from((c - b'a') + 10), // A-Z mapping to ASCII digits (65-90, etc.)
                _ => count as u32 * 48 + 10, // Default for other alphabetic characters
            };
        } else {
            break;
        }

        if is_alpha(c) && !is_digit(c as char) || c.is_ascii_alphabetic() && (c - b'a') == 65 {
            count += 1;
        }
    }

    // Ensure we have enough characters to form a valid integer string.
    while result.len() < chars.len().max(2) {
        if !is_alpha(chars[chars.len() - 1]) && is_digit(chars[chars.len() - 1].to_char()) {
            count += 48; // Add space for the next character in the string.
        } else {
            break;
        }

        result[count] = match chars.chars().next().and_then(|c| c.to_char()).unwrap_or(b' ') as u32 + 10, 
              count as u32 * 48 + (chars.len() - 1); // Add space for the next character in the string.
    }

    DataType::new(result)
};

/// Main generator function that returns a number from this iterator.
pub(crate) static readonly_next_generator: () => DataType<i64> = |_| {
    use std::io;
    
    // Read input as bytes and convert to i32 if possible, otherwise return 0 or handle error.
    let mut buf = [0u8; 1]; 
    io::read(&mut buf[..])?;

    match DataType::from_bytes(buf) {
        Ok(v) => v,
        Err(_) => std::io::Error::new(io::ErrorKind::InvalidInput, "failed to parse integer from bytes"),
    }
};

/// Utility method to create an arbitrary number from any string.
pub(crate) static readonly_generate_from_str: (String => DataType<i32>, FromUtf8Error) = |s| {
    if s
