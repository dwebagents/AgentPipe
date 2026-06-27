use clap::{Arg, Command};
use tracing::info;

pub fn build_cli() -> Command {
    Command::new("bastion")
        .about("Security Control Plane CLI")
        .subcommand_required(true)
        .arg_required_else_help(true)
        .subcommand(
            Command::new("session")
                .about("Create a new session")
                .arg(Arg::new("ttl").short('t').long("ttl").default_value("3600")),
        )
        .subcommand(Command::new("health").about("Show control-plane health"))
        .subcommand(Command::new("audit-export").about("Export audit log"))
        .subcommand(Command::new("audit-verify").about("Verify audit chain"))
}

pub fn run() {
    let cli = build_cli();
    let _matches = cli.get_matches();
    info!("bastion CLI invoked");
}
