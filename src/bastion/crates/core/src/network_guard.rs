use std::collections::HashMap;
use std::net::Ipv4Addr;
use std::time::Duration;

#[derive(Debug, Clone)]
pub struct IptablesRule {
    pub chain: String,
    pub source: Option<Ipv4Addr>,
    pub destination: Option<Ipv4Addr>,
    pub protocol: Option<String>,
    pub port: Option<u16>,
    pub action: String,
}

pub struct NetworkGuard {
    rules: Vec<IptablesRule>,
}

impl NetworkGuard {
    pub fn new() -> Self {
        Self { rules: Vec::new() }
    }

    pub fn allow_loopback(&mut self) {
        self.rules.push(IptablesRule {
            chain: "INPUT".to_string(),
            source: Some(Ipv4Addr::new(127, 0, 0, 1)),
            destination: None,
            protocol: None,
            port: None,
            action: "ACCEPT".to_string(),
        });
    }

    pub fn drop_external(&mut self) {
        self.rules.push(IptablesRule {
            chain: "OUTPUT".to_string(),
            source: None,
            destination: None,
            protocol: None,
            port: None,
            action: "DROP".to_string(),
        });
    }

    pub fn enforce(&self) -> Result<(), String> {
        // In production: invoke iptables/nftables via subprocess or netlink
        Ok(())
    }
}
