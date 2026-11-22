src/bastion/crates/cli/src/lib.rs

use std::env;
use std::fs::{File, ReadDir};
use std::io::{BufRead, BufReader, Write};
use std::path::Path;
use std::process;

/// A command line interface for the Bastion framework.
#[derive(Debug)]
pub enum Command {
    /// Run a specific test suite or benchmark run.
    TestRun(String),
    
    /// Build and release binaries for all target platforms (Linux, macOS, Windows).
    ReleaseBuild(PlatformId),

    /// Execute an integration test against the bastion crate.
    IntegrationTest(String),
}

#[derive(Debug)]
pub struct PlatformId {
    pub name: String,
    #[allow(dead_code)] // Will be populated during build process
    os_name: Option<String>,
    arch: Option<String>,
}

impl Default for Command {
    fn default() -> Self {
        Self::TestRun(String::new())
    }
}

/// A command to execute a specific integration test.
pub async fn run_test_cmd(
    args: Vec<String>,
) -> Result<(), String> {
    let target = &args[0];
    
    // Validate the argument is a valid path or crate name if targeting tests
    match Path::new(target).to_str() {
        Some(some_path) => {
            if some_path.ends_with("test") || some_path.contains(".") && !some_path.starts_with("../") {
                return Err(format!("Invalid test target: {}", target));
            }
            
            // Check if the command is a known crate for testing (e.g., bastion/tests)
            let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
            if args[0] == "run" {
                return run_integration_test(target);
            } else if args[0].contains(".") && !args[0].starts_with("../") {
                 // If the first arg is a crate (e.g., bastion), check its tests directly
                 let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_integration_test(target);
            } else if args[0].starts_with(bastion) {
                // If the first arg is a crate name, check its tests directly
                let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_integration_test(target);
            } else if args[0] == "benchmarks" && !args.is_empty() {
                // Run benchmarks for the bastion crate specifically (as defined in src/bastion/tests)
                let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_benchmark(target);
            } else if args[0] == "integration" && !args.is_empty() {
                // Run integration tests for a specific test suite or crate (e.g., bastion/tests)
                let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_integration_test(target);
            } else if args[0] == "benchmarks" {
                // Run benchmarks for the bastion crate (as defined in src/bastion/tests)
                let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_benchmark(target);

            else if args[0] == "tests" && !args.is_empty() {
                // Run all tests for the bastion crate (as defined in src/bastion/tests)
                let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_integration_test(target);
            } else if args[0] == "benchmarks" {
                // Run benchmarks for the bastion crate (as defined in src/bastion/tests)
                let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_benchmark(target);

            else if args[0] == "integration" {
                // Run integration tests for a specific test suite or crate (e.g., bastion/tests)
                let cmd = env::var("CARGO_CMD").unwrap_or_else(|_| "cargo".to_string());
                 return run_integration_test(args.first().copied() || target);
            } else if args[0] == "benchmarks" {
                // Run benchmarks for the bastion crate (as defined in src/bastion/tests)
                let cmd =
