use std::collections::HashMap;

pub struct ProcessGroupManager {
    pub groups: HashMap<String, Vec<u32>>,
}

impl ProcessGroupManager {
    pub fn create_group(&mut self, name: impl Into<String>) -> String {
        let name = name.into();
        self.groups.insert(name.clone(), Vec::new());
        name
    }

    pub fn add_to_group(&mut self, group: &str, pid: u32) {
        self.groups.entry(group.to_string()).or_default().push(pid);
    }

    pub fn terminate_group(&mut self, group: &str) {
        self.groups.remove(group);
    }
}
