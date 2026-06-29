use std::collections::HashMap;
use std::process::{Command, Stdio};
use std::time::Duration;

#[derive(Debug, Clone)]
pub struct ScriptExecutionResult {
    pub exit_code: i32,
    pub stdout: String,
    pub stderr: String,
    pub elapsed_ms: u64,
}

pub struct ScriptExecutor {
    pub timeout: Duration,
    pub cgroup_enabled: bool,
}

impl ScriptExecutor {
    pub fn new(timeout: Duration) -> Self {
        Self {
            timeout,
            cgroup_enabled: true,
        }
    }

    pub fn execute(&self, script_path: &str, params: &HashMap<String, String>) -> Result<ScriptExecutionResult, String> {
        let start = std::time::Instant::now();
        let mut cmd = Command::new(script_path);
        for (k, v) in params {
            cmd.arg(&format!("--{}", k)).arg(v);
        }
        cmd.stdout(Stdio::piped()).stderr(Stdio::piped());
        let output = cmd.output().map_err(|e| e.to_string())?;
        let elapsed = start.elapsed().as_millis() as u64;
        Ok(ScriptExecutionResult {
            exit_code: output.status.code().unwrap_or(-1),
            stdout: String::from_utf8_lossy(&output.stdout).to_string(),
            stderr: String::from_utf8_lossy(&output.stderr).to_string(),
            elapsed_ms: elapsed,
        })
    }
}
