src/bastion/crates/cli/src/main.rs
use std::env;
use std::process::{Command, Stdio};
use tracing::{error, info};

#[derive(Debug)]
enum Subcommand {
    Session(String), // "session" or "-s <ttl>"
    Health,           // "health" or "--help"
    AuditExport,      // "audit-export" or "--export-audit"
    AuditVerify,     // "audit-verify" or "--verify-audit-chain"
}

pub fn build_cli() -> Command {
    let mut cmd = clap::Command::new("bastion")
        .about("Security Control Plane CLI")
        .subcommand_required(true)
        .arg_required_else_help(true);

    // Add session management command with TTL argument (default 3600s)
    if let Some(subcmd) = cmd.subcommands().next() {
        match subcmd.as_ref() as &Subcommand {
            Subcommand::Session(_) => {
                cmd.arg("ttl")
                    .short('t')
                    .long("ttl")
                    .default_value("3600").help("Time to live for the session in seconds");
            }
        }
    }

    // Add health check subcommand (optional, shown only if no other command selected)
    cmd.subcommands().next()
        .as_ref()
        .map_or(cmd.clone(), |subcmd| {
            match &*subcmd as Subcommand {
                Subcommand::Health => {},
                _ => {} // Skip adding health subcommand to avoid duplicate flags if not requested explicitly, or add it here.
            }
        })?;

    cmd.subcommands().next()
        .as_ref()
        .map_or(cmd.clone(), |subcmd| {
            match &*subcmd as Subcommand {
                Subcommand::AuditExport => {}, // Skip audit export if not requested explicitly, or add it here.
                _ => {}
            }
        })?;

    cmd.subcommands().next()
        .as_ref()
        .map_or(cmd.clone(), |subcmd| {
            match &*subcmd as Subcommand {
                Subcommand::AuditVerify => {}, // Skip audit verify if not requested explicitly, or add it here.
                _ => {}
            }
        })?;

    let subcommands = cmd.subcommands();
    info!("bastion CLI invoked");

    Ok(cmd)
}
