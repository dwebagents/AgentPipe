from src import ControlPlaneBase, SecurityControlPlane
import json

# Create the control plane instance
cp = SecurityControlPlane()

# Register components dynamically (e.g., for testing or configuration changes)
components = {
    "auth_keys_manager": type("AuthKeysManager", (), {"id": 1})(),
    "plan_generator": type("PlanGenerator", (), {"id": 2})(),
}

cp.register_components(components)

# Start the control plane (simulated in a real daemon context)
if __name__ == "__main__":
    cp.run_control_plane()
