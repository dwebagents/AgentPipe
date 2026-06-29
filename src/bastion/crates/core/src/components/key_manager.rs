use ed25519_dalek::{Keypair, PublicKey, SecretKey, Signer, Verifier};
use rand::rngs::StdRng;
use rand_core::SeedableRng;
use zeroize::Zeroize;

pub struct EphemeralKeypair {
    pub public: [u8; 32],
    pub secret: Zeroize<[u8; 32]>,
}

impl EphemeralKeypair {
    pub fn generate() -> Self {
        let mut rng = StdRng::from_entropy();
        let mut bytes = [0u8; 32];
        rng.fill_bytes(&mut bytes);
        let secret = SecretKey::from_bytes(&bytes).expect("valid key bytes");
        let public = secret.public;
        let mut secret_bytes = [0u8; 32];
        secret_bytes.copy_from_slice(secret.to_bytes().as_ref());
        Self {
            public: public.to_bytes(),
            secret: Zeroize::new(secret_bytes),
        }
    }

    pub fn public_key(&self) -> [u8; 32] {
        self.public
    }
}

impl Drop for EphemeralKeypair {
    fn drop(&mut self) {
        self.secret.zeroize();
    }
}
