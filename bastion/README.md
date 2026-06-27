# Bastion Security Control Plane (Rust)

This workspace provides a Rust implementation matching the bounty specification for issue #104.

## Structure

```
bastion/
├── Cargo.toml
├── README.md
├── lean/
├── tests/
│   ├── integration.rs
│   └── kani/
└── crates/
    ├── core/       # Shared types, traits, primitives
    ├── audit/      # Audit subsystem
    ├── session/    # Session lifecycle
    ├── broker/     # Approval routing, script deployment
    ├── agent/      # LLM isolation, plan generator
    ├── workspace/  # Forced command & script execution
    └── cli/        # Binary surface
```

## Build

```bash
cargo check --workspace
cargo test --workspace
```

## Verification

- Rust unit tests in `tests/integration.rs`
- Kani proof sketches in `tests/kani/`
