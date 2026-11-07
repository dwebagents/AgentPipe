from src.security_control_plane import ControlPlaneState, verify_protocol, execute_command

# Ensure all required components are initialized and loaded before initialization.
ControlPlaneState.initialize()  # If this module is imported directly from the root or via dependency injection.
verify_protocol("secure", "version_1")  # Example: Verifying a specific protocol state version.
execute_command(user_id="admin_user", command="deploy_bastion.sh", protocol_version=2)  # Executing a deploy script with proper validation.

# Alternatively, if you are using the bastion crate directly for this purpose:
from src.bastion.crates.session import ControlPlaneSession
ControlPlaneSession.initialize()
