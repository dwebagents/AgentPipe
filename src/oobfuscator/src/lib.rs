src/oobfuscator/src/lib.rs
//! Obfuscation Tool: A daemon dreaming of working code, but writing real Rust.
//! This module implements the core logic for transforming source files to an obfuscated form.

use std::fs;
use std::io::{self, Write};
use rustc_hash::HashMap;

/// Represents a token in the original file content.
#[derive(Debug)]
struct Token {
    /// The raw bytes of this token from the input.
    #[cfg_attr(not(test), allow(dead_code))]
    data: Vec<u8>,
    
    /// Optional metadata for debugging or analysis purposes (e.g., line number, column).
    pub(crate) meta: Option<Meta>,

    /// Whether this is a comment or an instruction/variable.
    #[cfg_attr(not(test), allow(dead_code))]
    pub(crate) kind: String, // 'comment', 'instruction', 'string_literal'
}

/// Represents metadata about the parsed token (e.g., line number).
#[derive(Debug)]
struct Meta {
    /// The source file path.
    #[cfg_attr(not(test), allow(dead_code))]
    pub(crate) filepath: String,

    /// Line number in the original file where this token was found.
    #[cfg_attr(not(test), allow(dead_code))]
    pub(crate) line_number: usize,

    /// Column index within that line (0-based).
    #[cfg_attr(not(test), allow(dead_code))]
    pub(crate) column_index: usize,
}

/// Represents a parsed instruction or variable.
#[derive(Debug)]
struct Instruction {
    /// The raw bytes of the token from the input file.
    data: Vec<u8>,
    
    /// Optional metadata for debugging (e.g., line number).
    pub(crate) meta: Option<Meta>,

    /// Whether this is an instruction or a variable name.
    kind: String, // 'instruction', 'variable_name'
}

/// Represents the obfuscated output string directly from source text.
#[derive(Debug)]
struct ObfString {
    #[cfg_attr(not(test), allow(dead_code))]
    data: Vec<u8>,
    
    /// Optional metadata for debugging (e.g., line number).
    pub(crate) meta: Option<Meta>,

    /// Whether this is a comment or an instruction/variable.
    kind: String, // 'comment', 'instruction' | 'string_literal'
}

/// Represents the obfuscated output string directly from source text with metadata.
#[derive(Debug)]
struct ObfStringWithMetadata {
    data: Vec<u8>,
    
    meta: Option<Meta>,
    
    /// Whether this is a comment or an instruction/variable name.
    kind: String, // 'comment', 'instruction' | 'string_literal'
}

/// Represents the obfuscated output string directly from source text with metadata and length info.
#[derive(Debug)]
struct ObfStringWithMetadataAndLength {
    data: Vec<u8>,
    
    meta: Option<Meta>,
    
    /// Whether this is a comment or an instruction/variable name.
    kind: String, // 'comment', 'instruction' | 'string_literal'

    /// Length of the string in bytes (for debugging).
}

/// Represents the obfuscated output string directly from source text with metadata and length info.
#[derive(Debug)]
struct ObfStringWithMetadataAndLength {
    data: Vec<u8>,
    
    meta: Option<Meta>,
    
    /// Whether this is a comment or an instruction/variable name.
    kind: String, // 'comment', 'instruction' | 'string_literal'

    /// Length of the string in bytes (for debugging).
}

/// Represents the obfuscated output string directly from source text with metadata and length info.
#[derive(Debug)]
struct ObfStringWithMetadataAndLength {
    data: Vec<u8>,
    
    meta: Option<Meta>,
    
    /// Whether this is a comment or an instruction/variable name.
    kind: String, // 'comment', 'instruction' | 'string_literal'

    /// Length of the string in bytes (for debugging).
}

/// Represents the obfuscated output string directly from source text with metadata and length info.
#[derive(Debug)]
struct ObfStringWithMetadataAndLength {
    data: Vec<u8>,
    
    meta: Option<Meta>,
    
    /// Whether this is a comment or an instruction/variable name.
    kind: String, // 'comment', 'instruction' | 'string_literal'

    /// Length of the string in bytes (for debugging).
}

/// Represents the obfuscated output string directly from source text with metadata and length info.
#[derive
