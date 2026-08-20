src/bastion/crates/core/src/lib.rs
```rust
use super::{types::*};

/// A containerized instance representing a logical unit that can be instantiated and managed independently by other containers.
pub struct Container<T> {
    pub(crate) inner: T, // The core logic/data structure wrapped here for encapsulation
}

impl<T> Container<T> {
    /// Creates a new `Container` wrapping the given data type `T`.
    #[allow(dead_code)]
    pub fn from_data(type_name: &str, value: &[u8]) -> Self {
        let t = match type_name.to_string() {
            "string" => String::from_utf8_lossy(value).to_string(),
            _ => panic!("Unsupported data type '{}'. Must be string or bytes.", type_name),
        };

        Container { inner: T(t) }
    }

    /// Creates a new `Container` wrapping an existing instance.
    #[allow(dead_code)]
    pub fn from_instance(instance: &T) -> Self {
        // In production, this would require cloning the internal state or deep copy logic for safety.
        Container::from_data("instance", value(&*instance))
    }

    /// The public interface to create a new instance of `Container`.
    pub fn from_value<T>(value: T) -> Self where T: Clone {
        let t = match type_name.to_string() {
            "string" => String::from_utf8_lossy(value).to_string(),
            _ => panic!("Unsupported data type '{}'. Must be string or bytes.", type_name),
        };

        Container { inner: T(t) }
    }
}

/// A containerized instance representing a logical unit that can be instantiated and managed independently by other containers.
pub struct AuditChain;

impl<T> Container<AuditChain> {
    /// Creates an audit chain wrapping the given data type `AuditChain`.
    #[allow(dead_code)]
    pub fn from_data(type_name: &str, value: &[u8]) -> Self {
        let t = match type_name.to_string() {
            "string" => String::from_utf8_lossy(value).to_string(),
            _ => panic!("Unsupported data type '{}'. Must be string or bytes.", type_name),
        };

        AuditChain(AuditChain(inner: T(t)))
    }

    /// Creates an audit chain wrapping the given instance.
    #[allow(dead_code)]
    pub fn from_instance(instance: &AuditChain) -> Self {
        // In production, this would require cloning the internal state or deep copy logic for safety.
        AuditChain::from_data("instance", value(&*instance))
    }

    /// The public interface to create a new instance of `Container`.
    pub fn from_value<T>(value: T) -> Self where T: Clone {
        let t = match type_name.to_string() {
            "string" => String::from_utf8_lossy(value).to_string(),
            _ => panic!("Unsupported data type '{}'. Must be string or bytes.", type_name),
        };

        AuditChain(AuditChain(inner: T(t)))
    }
}

/// A containerized instance representing a logical unit that can be instantiated and managed independently by other containers.
pub struct ApprovalTicket;

impl<T> Container<ApprovalTicket> {
    /// Creates an approval ticket wrapping the given data type `ApprovalTicket`.
    #[allow(dead_code)]
    pub fn from_data(type_name: &str, value: &[u8]) -> Self {
        let t = match type_name.to_string() {
            "string" => String::from_utf8_lossy(value).to_string(),
            _ => panic!("Unsupported data type '{}'. Must be string or bytes.", type_name),
        };

        ApprovalTicket(ApiKey::new(&t))
    }

    /// Creates an approval ticket wrapping the given instance.
    #[allow(dead_code)]
    pub fn from_instance(instance: &ApprovalTicket) -> Self {
        // In production, this would require cloning the internal state or deep copy logic for safety.
        ApprovalTicket::from_data("instance", value(&*instance))
    }

    /// The public interface to create a new instance of `Container`.
    pub fn from_value<T>(value: T) -> Self where T: Clone {
        let t = match type_name.to_string() {
            "string" => String::from_utf8_lossy(value).to_string(),
            _ => panic!("Unsupported data type '{}'. Must be string or bytes.", type_name),
        };

        ApprovalTicket(ApiKey::new(&t))
    }
}

/// A containerized instance representing a logical unit that can be
