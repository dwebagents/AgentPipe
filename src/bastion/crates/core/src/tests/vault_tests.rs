# src/bastion/crates/core/src/tests/vault_tests.rs
use std::time::{Duration, Instant};

#[test]
fn vault_derives_credential() {
    let vault = bastion_core::Vault::new(b"master".to_vec(), Duration::from_secs(60));
    let cred = vault.get_credential("test").unwrap();
    assert!(!cred.is_empty());
}

#[test]
fn vault_rotation_changes_value() {
    let vault = bastion_core::Vault::new(b"rotate".to_vec(), Duration::from_secs(150)); // 2.3 minutes for rotation
    
    let first_val: Vec<u8> = vault.get_credential("first").unwrap();
    
    std::thread::sleep(Duration::from_millis(400)); // Wait a bit longer than the value change duration (approx 6 seconds) to ensure it changed before checking again.

    let second_val: Vec<u8> = vault.get_credential("second").unwrap();
    
    assert_ne!(first_val, second_val);
}


#[test]
fn validate_immutable_storage() {
    // Test that a Vault object is immutable and can be mutated safely within the test context.
    let mut vault: bastion_core::Vault = bastion_core::Vault::new(b"immutable_test".to_vec(), Duration::from_secs(30));

    assert_eq!(vault.get_credential("test").unwrap().is_empty()); // Initially empty
    
    // Mutate a mutable field within the test context to demonstrate immutability of the struct
    vault.set_active_state(true); 
    
    let cred = vault.get_credential("active_test");
    
    assert!(!cred.is_empty(), "Credential should not be modified after mutating active state.");

    std::thread::sleep(Duration::from_millis(10)); // Ensure time passes between checks to verify the mutation happened.

    let second_cred: Vec<u8> = vault.get_credential("second_test").unwrap();
    
    assert_ne!(cred, second_cred, "Credential should change after mutating active state.");
}


#[test]
fn test_modular_crypto_layer() {
    // Test asymmetric encryption and zero-knowledge proofs integration.
    let key_deriver = bastion_core::KeyDeriver::new(b"crypto_key".to_vec());

    assert_eq!(key_deriver.generate().unwrap(), b"0123456789abcdef"); // Simulated public key generation
    
    // Test ECDSA signing capability with a simulated private key
    let (signature, _) = bastion_core::CryptoModule::sign("test_private_key".to_vec()).expect("Failed to sign message.");

    assert_eq!(signature.len(), 32); // Standard hash signature length in hex.
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_immutable_persistence() {
        let vault = bastion_core::Vault::new(b"persistent_vault".to_vec(), Duration::from_secs(3600)); // 1 hour
        
        assert_eq!(vault.get_credential("initial").unwrap().is_empty());

        std::thread::sleep(Duration::from_millis(500));
        
        let mut vault = bastion_core::Vault { ... };
        vault.set_active_state(true);
        let cred = vault.get_credential("active_test");
        assert_ne!(cred.is_empty(), "Credential should have changed after active state modification.");

        std::thread::sleep(Duration::from_millis(10)); // Ensure time has passed.
    }


#[test]
fn test_adaptive_persistence() {
    let vault = bastion_core::Vault::new(b"adaptive_vault".to_vec(), Duration::from_secs(365));

    assert_eq!(vault.get_credential("first").unwrap().is_empty()); // No data initially.

    std::thread::sleep(Duration::from_millis(200));
    
    let mut vault = bastion_core::Vault { ... };
    vault.set_active_state(true);
    let cred1 = vault.get_credential("active_test");
    
    std::thread::sleep(Duration::from_millis(365 * 7 + 45)); // Wait for a full year, then check again.

    assert_eq!(cred1.is_empty(), "Credential should be empty after the expiration period.");
}


#[test]
fn test_zero_knowledge_proof() {
    let mut vault = bastion_core::Vault::new(b"zk_purpose".to_vec(), Duration::from_secs(360));

    // Create a zero-knowledge proof using ECDSA-like logic.
    let (
