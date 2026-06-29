use std::collections::HashMap;
use std::time::Duration;

pub struct KeyDeriver {
    pub master: Vec<u8>,
    pub info: String,
}

impl KeyDeriver {
    pub fn new(master: Vec<u8>, info: impl Into<String>) -> Self {
        Self { master, info: info.into() }
    }

    pub fn derive(&self, salt: &[u8], length: usize) -> Vec<u8> {
        use hmac::{Hmac, Mac};
        use sha2::Sha256;
        type HmacSha256 = Hmac<Sha256>;
        let mut mac = HmacSha256::new_from_slice(&self.master).expect("key valid");
        mac.update(salt);
        mac.update(self.info.as_bytes());
        let result = mac.finalize().into_bytes();
        result[..length].to_vec()
    }
}
