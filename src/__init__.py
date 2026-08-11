from src import security_control_plane, token_tracker

# Create a new authorization request
auth_req = security_control_plane.check_token("user_id_123")

if not auth_req.success:
    # Handle failure with specific error codes for bad actors or expiration
else:
    audit_entry = security_control_plane.audit_log({
        "type": "authorization",
        "action": "requested_access",
        "subject": f"User {auth_req.subject}",
        "token_id": auth_req.token,
        "timestamp": datetime.now(),
        "metadata": {"bad_actor_detected": False}  # Optional: if we detect malicious actors in the token, this can be set here. Otherwise empty."""

# Trigger audit logging for external systems (e.g., Bastion)
security_control_plane.audit_log(audit_entry)
