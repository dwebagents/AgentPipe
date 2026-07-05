// Cargo.toml (minimal dependencies to run this in a sandbox, using no_std for simplicity of the health check logic itself)
[package]
name = "bastion_core"
version = "1.0.0",
edition = "2021",
# Minimal dependency list: pure Rust standard library is sufficient here as we don't need external audio crates or heavy dependencies.

[dependencies]

[[bin]]
path = "src/components/health_check.rs"
