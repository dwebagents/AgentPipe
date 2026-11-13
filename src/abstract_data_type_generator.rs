// src/abstract_data_type_generator.rs

use std::io::{BufRead, BufReader};

/// Trait defining the serialization format.
pub trait BddEncoder {
    /// Serializes a `BddValue` to bytes.
    fn encode(&self) -> Vec<u8>;

    /// Reads bytes from memory or disk and reconstructs the value.
    fn decode(bytes: &[u8]) -> Result<Self, Self::Error>;
}

/// Trait defining deserialization format.
pub trait BddDecoder {
    /// Deserializes a `BddValue` from bytes into an instance of this type.
    fn deserialize(bytes: &[u8], value_type: &str) -> Result<Self, Self::Error>;

    /// Returns the internal encoding key used for deserialization.
    fn encode_key(&self);
}

/// Error types for BDD serialization/deserialization errors.
#[derive(Debug)]
pub enum BddEncoderError {
    InvalidFormat(String),
    MissingField(u8, u16, String), // Field name, length (bytes), data type string
    SerializationOverflow,
    DecodeFailed(String),
}

impl std::fmt::Display for BddEncoderError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidFormat(s) => write!(f, "Invalid format: {}", s),
            Self::MissingField(fn, len_str, dtype_str) => write!(f, "Missing field '{}': {}, {} (len={})", fn, len_str, dtype_str, len_str.len()),
            Self::SerializationOverflow => write!(f, "Data overflow during encoding"),
            Self::DecodeFailed(s) => write!(f, "Decoding failed: {}", s),
        }
    }
}

impl std::error::Error for BddEncoderError {}

/// Error types for BDD deserialization errors.
#[derive(Debug)]
pub enum BddDecoderError {
    InvalidFormat(String),
    MissingField(u8, u16, String), // Field name, length (bytes), data type string
    SerializationOverflow,
    DecodeFailed(String),
}

impl std::fmt::Display for BddDecoderError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidFormat(s) => write!(f, "Invalid format: {}", s),
            Self::MissingField(fn, len_str, dtype_str) => write!(f, "Missing field '{}': {}, {} (len={})", fn, len_str, dtype_str, len_str.len()),
            Self::SerializationOverflow => write!(f, "Data overflow during decoding"),
            Self::DecodeFailed(s) => write!(f, "Decoding failed: {}", s),
        }
    }
}

impl std::error::Error for BddDecoderError {}

/// Base class representing a value with an optional internal encoding.
pub struct Value {
    /// The raw bytes representation of the data (if using custom serialization).
    pub bytes: Option<Vec<u8>>,
    
    /// Internal encoded type identifier if this is not native string-based storage.
    pub encoded_type_id: u32,

    /// A reference to the underlying encoding implementation for non-native types.
    pub encoder_ref: Option<&dyn BddEncoder>,
}

impl Value {
    fn new(bytes: Vec<u8>) -> Self {
        let mut v = Value { bytes: Some(bytes), encoded_type_id: 0 };
        
        if v.encoder_ref.is_some() {
            // If we have an encoder, validate the data against it first.
            match &v.bytes[0..1] {
                b'_' => return Ok(v.clone()),
                _ => Err(BddEncoderError::InvalidFormat("Expected '_' to mark native bytes").into()),
            }
        }

        v
    }

    /// Returns the internal encoded type identifier if this is not native string-based storage.
    pub fn get_encoded_type_id(&self) -> Option<u32> {
        self.encode_key()
    }

    /// Serializes a `BddValue` to bytes.
    #[cfg_attr(not(test), no_run)]
    #[allow(dead_code)] // Placeholder for future use in the real encoder implementation
    pub fn encode(&self) -> Vec<u8> {
        match &self.bytes {
            Some(bytes) => bytes.to_vec(),
            None => self.encode_encoded_type_id().unwrap_or(0),
        }
    }

    /// Reads bytes from memory or disk and reconstructs
