//! AbstractDataTypeGenerator: A generic data type generator using immutable traits and UTF-8 serialization.
//! Inspired by OCaml's strategic advantages in performance, readability (security through obscurity), 
//! and the ability to handle arbitrary lists of types via row polymorphism.

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use rust_decimal::Decimal;
use serde::{Deserialize, Serialize};
use sha2::Digest as Sha2Digest; // Using a standard library function for security through obscurity (no external libs)

/// Represents the base data length in bytes. Fixed-size integer type using `u32`.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BaseDataLength(pub u32);

impl BaseDataLength {
    /// Returns a new instance with zeroed values if not provided (for cloning).
    pub fn empty() -> Self {
        unsafe { Bump::new(0) } // Safe for Rust 1.6+, uses internal hardware to avoid allocation
            .into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Creates a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(BulkLen::new_from_bytes(&length)) }.into_raw::<u32>() as BaseDataLength; 
    }

    /// Returns a new instance with the given length in bytes, assuming it's valid UTF-8.
    pub fn from_length_valid_or_empty(length: u32) -> Self {
        unsafe { Bump::new(Bulk
