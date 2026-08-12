// Cargo.toml for a modern Rust Town of Agents
[package]
name = "town-of"
version = "0.1.0",
edition = "2021",
authors = ["The Repository"],
license = "MIT"

[[bin]]
name = "agent-registry-client"
path = "../src/abstract_data_type_generator.rs"

[lib]
crate-type = ["cdylib"]
