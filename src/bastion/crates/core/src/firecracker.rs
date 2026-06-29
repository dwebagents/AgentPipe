use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FirecrackerConfig {
    pub kernel_image_path: PathBuf,
    pub rootfs_path: PathBuf,
    pub mem_size_mib: u32,
    pub vcpu_count: u32,
    pub network_interfaces: Vec<NetworkInterface>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkInterface {
    pub iface_id: String,
    pub host_dev_name: String,
    pub guest_mac: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VmInstance {
    pub instance_id: String,
    pub config: FirecrackerConfig,
    pub state: VmState,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum VmState {
    Starting,
    Running,
    Pausing,
    Paused,
    Resuming,
    Stopping,
    Stopped,
}

pub trait FirecrackerAdapter {
    fn start_vm(&self, config: FirecrackerConfig) -> Result<VmInstance>;
    fn stop_vm(&self, instance_id: &str) -> Result<()>;
    fn pause_vm(&self, instance_id: &str) -> Result<()>;
    fn resume_vm(&self, instance_id: &str) -> Result<()>;
    fn vm_state(&self, instance_id: &str) -> Result<VmState>;
}
