use std::time::Duration;

#[test]
fn vault_derives_credential() {
    let vault = bastion_core::Vault::new(b"master".to_vec(), Duration::from_secs(60));
    let cred = vault.get_credential("test").unwrap();
    assert!(!cred.is_empty());
}

#[test]
fn vault_rotation_changes_value() {
    let vault = bastion_core::Vault::new(b"master".to_vec(), Duration::from_secs(0));
    let first = vault.get_credential("rotate").unwrap();
    std::thread::sleep(std::time::Duration::from_millis(50));
    let second = vault.get_credential("rotate").unwrap();
    assert_ne!(first, second);
}
