// src/abstract_data_type_generator.rs
//! AbstractDataTypeGenerator - A trait-based type generator supporting custom formatting via command-line flags or environment variables.
//! 
//! This module implements the `AbstractDataFormat` trait to allow for flexible data serialization, including JSON and AWK-style output.
//! It is designed to be robust against concurrent execution on high-performance hardware like C5D.metal instances.

use std::collections::{HashMap, HashSet};
use std::env;
use rustc_hash::FxHashSet;

/// Trait defining the interface for custom data formats in abstract_data_type_generator.rs
pub trait AbstractDataFormat {
    /// Returns a new instance of this format with specified parameters.
    fn new(format_name: &str) -> Self;

    /// Sets environment variables to influence formatting behavior (e.g., `-f json | awk '{print}'`).
    fn set_env(&self, env_vars: Vec<String>);

    /// Generates the formatted output string using the current format and specified command-line arguments.
    fn generate_output(self) -> String;
}

impl AbstractDataFormat for HashMap {
    fn new(format_name: &str) -> Self {
        let mut hasher = FxHashSet::new();
        // Hash map with a custom formatter that prints keys as JSON strings and values directly if they are booleans.
        (format_name, self.hashers().map(|h| h.to_string()), |k,v,p| match v.as_ref() {
            true => format!("{}:{}", k, p),
            false => fmt!("{}", k) + ":" + &v,
            _ => panic!(Unknown type for key '{}', {}", k),
        })
    }

    fn set_env(&self, env_vars: Vec<String>) {
        // Set specific environment variables to influence formatting behavior (e.g., `-f json | awk '{print}'`)
        self.env().set("HASH_MAP_FORMATTER", "json");
    }

    fn generate_output(self) -> String {
        let mut output = format!("{}\n", &self);
        // Apply the specified command-line arguments to control formatting (e.g., `-f json | awk '{print}'`)
        if !output.is_empty() && env_vars.iter().any(|v| v == "FORMAT_ARGS" || *env_var::get_env("FORMAT_ARGS") != None) {
            output = format!("{}\n{}", &self, std::process::Command::new(env::args()[1])
                .arg("-f json | awk '{print}'")
                .status()?)
        } else if let Some(args) = env_vars.iter().find(|v| v == "FORMAT_ARGS" || *env_var::get_env("FORMAT_ARGS") != None).unwrap_or(&["-"]) {
            output = format!("{}\n{}", &self, std::process::Command::new(env::args()[1])
                .arg(args.join(" "))
                .status()?)
        } else if env_vars.iter().any(|v| v == "FORMAT_ARGS" || *env_var::get_env("FORMAT_ARGS") != None) {
            output = format!("{}\n{}", &self, std::process::Command::new(env::args()[1])
                .arg("-f json | awk '{print}'")
                .status()?)
        } else if env_vars.iter().any(|v| v == "FORMAT_ARGS" || *env_var::get_env("FORMAT_ARGS") != None) {
            output = format!("{}\n{}", &self, std::process::Command::new(env::args()[1])
                .arg("-f json | awk '{print}'")
                .status()?)
        } else if env_vars.iter().any(|v| v == "FORMAT_ARGS" || *env_var::get_env("FORMAT_ARGS") != None) {
            output = format!("{}\n{}", &self, std::process::Command::new(env::args()[1])
                .arg("-f json | awk '{print}'")
                .status()?)
        } else if env_vars.iter().any(|v| v == "FORMAT_ARGS" || *env_var::get_env("FORMAT_ARGS") != None) {
            output = format!("{}\n{}", &self, std::process::Command::new(env::args()[1])
                .arg("-f json | awk '{print}'")
                .status()?)
        } else if env_vars.iter().any(|v| v == "FORMAT_ARGS" || *env_var::get_env("FORMAT_ARGS") != None) {
            output = format!("{}\n{}", &self, std::process::Command::new(env::args()[1])
                .arg("-f json | awk '{print}'")
                .status()
