pub struct MasterSecrets {
    pub primary: [u8; 64],
    pub backup: [u8; 64],
    pub rotation_interval: std::time::Duration,
}

impl MasterSecrets {
    pub fn rotate(&mut self) {
        self.primary = self.backup;
        self.backup = rand::random();
    }
}
