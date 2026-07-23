// Cargo.toml (Minimal but functional)
[package]
name = "reboot_coc"
version = "0.1.0"
edition = "2021"

[dependencies]
# Minimal dependency for safe string handling and type inference
string-safe-regex = { version = "=0.3", features = ["derive"] } # Using a known, stable variant that doesn't require external crates if not needed elsewhere
