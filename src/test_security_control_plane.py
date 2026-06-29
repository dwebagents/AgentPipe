from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from security_control_plane import (
    ApprovalRequiredError,
    CredentialExpiredError,
    InvalidApprovalError,
    PolicyDeniedError,
    SessionMismatchError,
    SecurityControlPlane,
    SecurityPolicy,
    TamperEvidentAuditLog,
)


NOW = datetime(2026, 6, 27, 9, 0, tzinfo=timezone.utc)


def build_plane() -> SecurityControlPlane:
    return SecurityControlPlane(
        "test-master-secret",
        policy=SecurityPolicy(
            approval_ttl_seconds=60,
            session_ttl_seconds=120,
            max_payload_bytes=256,
        ),
    )


def test_low_risk_operation_executes_without_approval() -> None:
    plane = build_plane()
    session = plane.start_session("agent-1", now=NOW)
    request = plane.plan_operation(
        "agent-1",
        "metadata",
        "read",
        {"resource": "status"},
        now=NOW,
    )

    receipt = plane.execute(request.id, now=NOW + timedelta(seconds=1))

    assert request.decision == "allow"
    assert receipt.credential_token == session.token
    assert plane.verify_audit_log()
    assert [record.event_type for record in plane.audit_records()] == [
        "session.started",
        "operation.planned",
        "operation.executed",
    ]


def test_sensitive_operation_requires_one_time_human_approval() -> None:
    plane = build_plane()
    plane.start_session("agent-1", now=NOW)
    request = plane.plan_operation(
        "agent-1",
        "email",
        "send",
        {"to": "ops@example.com", "subject": "planned maintenance"},
        now=NOW,
    )

    with pytest.raises(ApprovalRequiredError):
        plane.execute(request.id, now=NOW + timedelta(seconds=1))

    ticket = plane.approve(
        request.id,
        approver_id="human-controller",
        reason="approved maintenance notice",
        now=NOW + timedelta(seconds=2),
    )
    receipt = plane.execute(
        request.id,
        approval_ticket=ticket,
        now=NOW + timedelta(seconds=3),
    )

    assert request.decision == "approval_required"
    assert receipt.request_id == request.id
    with pytest.raises(InvalidApprovalError):
        plane.execute(
            request.id,
            approval_ticket=ticket,
            now=NOW + timedelta(seconds=4),
        )
    assert plane.verify_audit_log()


def test_policy_denies_blocked_operations_even_after_approval_attempt() -> None:
    plane = build_plane()
    plane.start_session("agent-1", now=NOW)
    request = plane.plan_operation(
        "agent-1",
        "database",
        "drop",
        {"table": "production_accounts"},
        now=NOW,
    )

    assert request.decision == "deny"
    with pytest.raises(PolicyDeniedError):
        plane.approve(
            request.id,
            approver_id="human-controller",
            reason="should not pass",
            now=NOW + timedelta(seconds=1),
        )
    with pytest.raises(PolicyDeniedError):
        plane.execute(request.id, now=NOW + timedelta(seconds=2))
    assert plane.verify_audit_log()


def test_sessions_expire_and_rotation_issues_new_isolated_credentials() -> None:
    plane = build_plane()
    first_session = plane.start_session("agent-1", now=NOW)
    request = plane.plan_operation("agent-1", "metadata", "read", now=NOW)

    with pytest.raises(CredentialExpiredError):
        plane.execute(request.id, now=NOW + timedelta(seconds=121))

    rotated = plane.rotate_credentials("agent-1", now=NOW + timedelta(seconds=122))
    receipt = plane.execute(request.id, now=NOW + timedelta(seconds=123))

    assert rotated.token != first_session.token
    assert receipt.credential_token == rotated.token
    assert rotated.network_enabled is False
    assert plane.verify_audit_log()


def test_session_cannot_execute_another_agents_request() -> None:
    plane = build_plane()
    plane.start_session("agent-1", now=NOW)
    request = plane.plan_operation("agent-1", "metadata", "read", now=NOW)
    plane.rotate_credentials("agent-2", now=NOW + timedelta(seconds=1))

    with pytest.raises(SessionMismatchError):
        plane.execute(request.id, now=NOW + timedelta(seconds=2))

    assert plane.audit_records()[-1].event_type == "operation.session_mismatch"
    assert plane.verify_audit_log()


def test_audit_log_detects_record_tampering() -> None:
    audit_log = TamperEvidentAuditLog()
    audit_log.append("operation.planned", "opr-1", {"decision": "allow"}, now=NOW)
    audit_log.append("operation.executed", "opr-1", {"approved": False}, now=NOW)

    assert audit_log.verify_integrity()

    audit_log._records[0] = replace(  # noqa: SLF001 - explicit tamper simulation.
        audit_log._records[0],
        details={"decision": "deny"},
    )

    assert not audit_log.verify_integrity()
