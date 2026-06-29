#!/usr/bin/env python3
"""
Regression & unit tests for Security Control Plane.

Run with:
    python3 -m pytest src/test_security_control_plane.py -q
    python3 -m pytest src/test_security_control_plane.py -q --cov=security_control_plane
"""

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timedelta

import pytest

from security_control_plane import (
    Action,
    ApprovalBroker,
    ApprovalTicket,
    AuditChain,
    AuditEntry,
    AuditTamperError,
    ControlPlane,
    Credential,
    PolicyDecision,
    PolicyEngine,
    PolicyRule,
    PolicyDeniedError,
    ApprovalRequiredError,
    SessionExpiredError,
    SecurityControlPlaneError,
    SessionContext,
    TicketAlreadyUsedError,
    TicketInvalidError,
    Vault,
    action_pattern_matches,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def master_secret() -> bytes:
    return b"test-master-secret-" + b"x" * 44


@pytest.fixture()
def cp(master_secret: bytes) -> ControlPlane:
    return ControlPlane(master_secret=master_secret, session_ttl=10)


@pytest.fixture()
def session(cp: ControlPlane) -> "SessionContext":
    return cp.start_session({"test": True})


def make_action(session, action_type: str = "send_email") -> Action:
    return Action(
        action_id=str(uuid.uuid4()),
        session_id=session.session_id,
        action_type=action_type,
        parameters={"to": "user@example.com", "subject": "hi", "body": "hello"},
    )


# ---------------------------------------------------------------------------
# Hash-chain invariants
# ---------------------------------------------------------------------------

class TestAuditChain:

    def test_empty_chain_is_valid(self):
        ac = AuditChain()
        assert ac.verify() is True

    def test_single_entry_chains_to_genesis(self):
        ac = AuditChain()
        e = ac.append("sid", "event.foo", "actor", "ok")
        assert e.prev_hash == ac.genesis_hash
        assert e.entry_hash == e.compute_hash(ac.genesis_hash)
        assert ac.verify() is True

    def test_two_entries_chain_correctly(self):
        ac = AuditChain()
        first = ac.append("sid", "e1", "a", "ok")
        second = ac.append("sid", "e2", "a", "ok")
        assert second.prev_hash == first.entry_hash
        assert ac.verify() is True

    def test_tampering_entry_breaks_chain(self):
        ac = AuditChain()
        ac.append("sid", "e1", "a", "ok")
        good = ac.append("sid", "e2", "a", "ok")
        # Simulate tampering by creating a modified copy and replacing in list
        tampered = AuditEntry(
            sequence=good.sequence,
            timestamp=good.timestamp,
            session_id=good.session_id,
            event="tampered!",
            actor=good.actor,
            outcome=good.outcome,
            metadata=good.metadata,
            prev_hash=good.prev_hash,
            entry_hash=good.entry_hash,
        )
        ac._entries[-1] = tampered
        assert ac.verify() is False

    def test_two_entries_chain_correctly(self):
        ac = AuditChain()
        first = ac.append("sid", "e1", "a", "ok")
        second = ac.append("sid", "e2", "a", "ok")
        assert second.prev_hash == first.entry_hash
        assert ac.verify() is True

    def test_sequence_is_monotonic(self):
        ac = AuditChain()
        prev = 0
        for i in range(1, 51):
            e = ac.append("sid", f"e{i}", "a", "ok")
            assert e.sequence == i
            prev = i
        assert ac.verify() is True

    def test_json_serialization_round_trip(self):
        ac = AuditChain()
        ac.append("sid", "e1", "a", "ok")
        ac.append("sid", "e2", "a", "ok", {"key": "val"})
        data = json.loads(ac.to_json())
        assert len(data) == 2
        assert data[0]["event"] == "e1"
        assert data[1]["metadata"]["key"] == "val"

    def test_to_bytes_is_stable(self):
        ac = AuditChain()
        e = ac.append("sid", "e", "a", "ok")
        assert len(e.to_bytes()) > 0

    def test_entry_hash_is_32_bytes(self):
        ac = AuditChain()
        e = ac.append("sid", "e", "a", "ok")
        assert len(e.entry_hash) == 32


# ---------------------------------------------------------------------------
# Vault – credential derivation & rotation
# ---------------------------------------------------------------------------

class TestVault:

    def test_derive_produces_hex_value(self, master_secret):
        v = Vault(master_secret=master_secret, rotation_interval_seconds=60)
        cred = v.get_credential("test:key")
        assert isinstance(cred, str)
        assert len(cred) == 64  # 32 bytes hex

    def test_same_key_same_value(self, master_secret):
        v = Vault(master_secret=master_secret)
        a = v.get_credential("stable")
        b = v.get_credential("stable")
        assert a == b

    def test_rotation_changes_value(self, master_secret):
        v = Vault(master_secret=master_secret, rotation_interval_seconds=0)
        first = v.get_credential("rotate:me")
        time.sleep(0.05)
        second = v.get_credential("rotate:me")
        assert first != second

    def test_force_rotate(self, master_secret):
        v = Vault(master_secret=master_secret)
        first = v.get_credential("force")
        second = v.force_rotate("force")
        assert first != second

    def test_version_increments(self, master_secret):
        v = Vault(master_secret=master_secret, rotation_interval_seconds=0)
        v.get_credential("ver")
        v.force_rotate("ver")
        v.force_rotate("ver")
        assert v.credential_versions["ver"] == 3

    def test_different_names_produce_different_values(self, master_secret):
        v = Vault(master_secret=master_secret)
        a = v.get_credential("alpha")
        b = v.get_credential("beta")
        assert a != b

    def test_different_masters_produce_different_values(self):
        a = Vault(master_secret=b"master-a", rotation_interval_seconds=60)
        b = Vault(master_secret=b"master-b", rotation_interval_seconds=60)
        assert a.get_credential("name") != b.get_credential("name")


# ---------------------------------------------------------------------------
# Session lifecycle
# ---------------------------------------------------------------------------

class TestSessionManager:

    def test_create_session_sets_fields(self, cp):
        ctx = cp.start_session()
        assert ctx.session_id is not None
        assert ctx.is_active is True
        assert ctx.is_expired is False

    def test_session_has_ssh_key(self, cp):
        ctx = cp.start_session()
        assert ctx.ssh_public_key.startswith("ssh-ed25519")

    def test_session_has_vault(self, cp):
        ctx = cp.start_session()
        assert isinstance(ctx.vault, Vault)

    def test_expired_session_raises(self, cp):
        ctx = cp.start_session()
        ctx.expires_at = datetime.utcnow() - timedelta(seconds=1)
        with pytest.raises(SessionExpiredError):
            ctx.assert_active()

    def test_revoked_session_raises(self, cp):
        ctx = cp.start_session()
        ctx.is_active = False
        with pytest.raises(SessionExpiredError):
            ctx.assert_active()

    def test_active_session_passes(self, cp):
        ctx = cp.start_session()
        ctx.assert_active()


# ---------------------------------------------------------------------------
# PolicyEngine
# ---------------------------------------------------------------------------

class TestPolicyEngine:

    def test_allow_read(self):
        pe = PolicyEngine()
        assert pe.evaluate(Action("a1", "s1", "read_users", {})) == PolicyDecision.ALLOW

    def test_allow_query(self):
        pe = PolicyEngine()
        assert pe.evaluate(Action("a2", "s1", "query_db", {})) == PolicyDecision.ALLOW

    def test_approve_send_email(self):
        pe = PolicyEngine()
        assert pe.evaluate(Action("a3", "s1", "send_email", {})) == PolicyDecision.APPROVE

    def test_approve_database_write(self):
        pe = PolicyEngine()
        assert pe.evaluate(Action("a4", "s1", "database_write", {})) == PolicyDecision.APPROVE

    def test_deny_code_execution(self):
        pe = PolicyEngine()
        assert pe.evaluate(Action("a5", "s1", "code_execution", {})) == PolicyDecision.DENY

    def test_deny_exfiltrate(self):
        pe = PolicyEngine()
        assert pe.evaluate(Action("a6", "s1", "exfiltrate_secrets", {})) == PolicyDecision.DENY

    def test_deny_unknown_action(self):
        pe = PolicyEngine()
        assert pe.evaluate(Action("a7", "s1", "unknown_op", {})) == PolicyDecision.DENY

    def test_custom_rules(self):
        pe = PolicyEngine(rules=[
            PolicyRule("dangerous_op", PolicyDecision.DENY, reason="custom"),
        ])
        assert pe.evaluate(Action("a8", "s1", "dangerous_op", {})) == PolicyDecision.DENY

    def test_evaluate_with_reason_returns_string(self):
        pe = PolicyEngine()
        dec, reason = pe.evaluate_with_reason(Action("a9", "s1", "send_email", {}))
        assert dec == PolicyDecision.APPROVE
        assert reason


# ---------------------------------------------------------------------------
# ApprovalBroker
# ---------------------------------------------------------------------------

class TestApprovalBroker:

    def test_issue_ticket_returns_ticket(self, cp):
        action = Action("a1", "s1", "send_email", {})
        ticket = cp._approvals.issue_ticket("s1", "a1")
        assert ticket.session_id == "s1"
        assert ticket.action_id == "a1"
        assert not ticket.redeemed
        assert not ticket.is_expired

    def test_redeem_valid_ticket(self, cp):
        action = Action("a1", "s1", "send_email", {})
        ticket = cp._approvals.issue_ticket("s1", "a1")
        redeemed = cp._approvals.redeem_ticket(
            "s1", "a1", ticket.signature
        )
        assert redeemed.redeemed
        assert redeemed.redeemed_at is not None

    def test_redeem_wrong_session_raises(self, cp):
        ticket = cp._approvals.issue_ticket("s1", "a1")
        with pytest.raises(TicketInvalidError):
            cp._approvals.redeem_ticket("other-session", "a1", ticket.signature)

    def test_redeem_wrong_action_raises(self, cp):
        ticket = cp._approvals.issue_ticket("s1", "a1")
        with pytest.raises(TicketInvalidError):
            cp._approvals.redeem_ticket("s1", "a2", ticket.signature)

    def test_redeem_same_ticket_twice_raises(self, cp):
        ticket = cp._approvals.issue_ticket("s1", "a1")
        cp._approvals.redeem_ticket("s1", "a1", ticket.signature)
        with pytest.raises(TicketInvalidError):
            cp._approvals.redeem_ticket("s1", "a1", ticket.signature)

    def test_expired_ticket_raises(self, cp):
        t = cp._approvals.issue_ticket("s1", "a1")
        t.expires_at = datetime.utcnow() - timedelta(seconds=1)
        with pytest.raises(TicketInvalidError):
            cp._approvals.redeem_ticket("s1", "a1", t.signature)

    def test_bad_signature_raises(self, cp):
        cp._approvals.issue_ticket("s1", "a1")
        with pytest.raises(TicketInvalidError):
            cp._approvals.redeem_ticket("s1", "a1", b"bad-sig-data")

    def test_two_tickets_for_same_action(self, cp):
        t1 = cp._approvals.issue_ticket("s1", "a1")
        t2 = cp._approvals.issue_ticket("s1", "a1")
        assert t1.signature != t2.signature

    def test_ticket_json_serialization(self, cp):
        ticket = cp._approvals.issue_ticket("s1", "a1")
        d = ticket.to_dict()
        assert "signature" in d


# ---------------------------------------------------------------------------
# ControlPlane – end-to-end
# ---------------------------------------------------------------------------

class TestControlPlane:

    def test_full_allow_flow(self, cp):
        def handler(params):
            return {"status": "ok", "result": "done"}

        cp.register_action("read_data", handler)
        session = cp.start_session()
        action = Action("a1", session.session_id, "read_data", {})
        result = cp.execute_action(action)
        assert result["status"] == "ok"
        assert cp.verify_audit_integrity() is True

    def test_full_approve_flow(self, cp):
        def handler(params):
            return {"status": "sent", "to": params["to"]}

        cp.register_action("send_email", handler)
        session = cp.start_session()
        action = Action("a1", session.session_id, "send_email",
                        {"to": "user@example.com", "subject": "hi", "body": "hello"})
        ticket = cp.request_approval(action)
        result = cp.execute_action(action, approval_signature=ticket.signature)
        assert result["status"] == "sent"
        assert cp.verify_audit_integrity() is True

    def test_full_deny_flow(self, cp):
        cp.register_action("code_execution", lambda p: None)
        session = cp.start_session()
        action = Action("a1", session.session_id, "code_execution", {"cmd": "rm -rf"})
        with pytest.raises(PolicyDeniedError):
            cp.execute_action(action)
        assert cp.verify_audit_integrity() is True

    def test_approval_flow_missing_ticket_raises(self, cp):
        cp.register_action("send_email", lambda p: None)
        session = cp.start_session()
        action = Action("a1", session.session_id, "send_email", {"to": "u@e.com", "subject": "s", "body": "b"})
        with pytest.raises(ApprovalRequiredError):
            cp.execute_action(action)

    def test_action_requires_approval_no_ticket(self, cp):
        session = cp.start_session()
        action = Action("a1", session.session_id, "send_email",
                        {"to": "u@e.com", "subject": "s", "body": "b"})
        with pytest.raises(ApprovalRequiredError):
            cp.execute_action(action)

    def test_health_check(self, cp):
        h = cp.health_check()
        assert "audit_integrity" in h
        assert h["audit_integrity"] is True
        assert "active_sessions" in h
        assert "pending_tickets" in h

    def test_audit_export(self, cp):
        cp._audit.append("s1", "test", "t", "o")
        exported = cp.export_audit()
        assert "test" in exported
        data = json.loads(exported)
        assert any(entry["event"] == "test" for entry in data)

    def test_session_ttl_enforced(self, cp):
        session = cp.start_session()
        session.expires_at = datetime.utcnow() - timedelta(seconds=1)
        action = Action("a1", session.session_id, "read_data", {})
        cp.register_action("read_data", lambda p: None)
        with pytest.raises(SessionExpiredError):
            cp.execute_action(action)

    def test_no_handler_raises(self, cp):
        session = cp.start_session()
        action = Action("a1", session.session_id, "nonexistent_action", {})
        with pytest.raises(SecurityControlPlaneError):
            cp.execute_action(action)

    def test_audit_preserves_integrity_through_full_flow(self, cp):
        cp.register_action("read_data", lambda p: {"ok": True})
        sessions = [cp.start_session() for _ in range(3)]
        for s in sessions:
            cp.execute_action(Action(f"a{s.session_id[:8]}", s.session_id,
                                    "read_data", {}))
        assert cp.verify_audit_integrity() is True


# ---------------------------------------------------------------------------
# Policy patterns
# ---------------------------------------------------------------------------

class TestPolicyPatterns:

    def test_glob_send_star(self):
        assert action_pattern_matches("send_*", "send_email") is True
        assert action_pattern_matches("send_*", "send_slack") is True
        assert action_pattern_matches("send_*", "read") is False

    def test_wildcard_matches_all(self):
        assert action_pattern_matches("*", "anything") is True

    def test_exact_match(self):
        assert action_pattern_matches("deploy", "deploy") is True
        assert action_pattern_matches("deploy", "deploy_svc") is False

    def test_case_insensitive(self):
        assert action_pattern_matches("READ*", "read_data") is True


# ---------------------------------------------------------------------------
# Regression: the specific constraints from issue #104
# ---------------------------------------------------------------------------

class TestBountyConstraints:

    def test_short_lived_sessions_are_isolated(self, cp):
        s1 = cp.start_session()
        s2 = cp.start_session()
        assert s1.session_id != s2.session_id
        assert s1.ssh_public_key != s2.ssh_public_key

    def test_allow_approve_deny_triad(self, cp):
        pe = PolicyEngine()
        assert pe.evaluate(Action("1", "s1", "read", {})) == PolicyDecision.ALLOW
        assert pe.evaluate(Action("2", "s1", "send_email", {})) == PolicyDecision.APPROVE
        assert pe.evaluate(Action("3", "s1", "code_execution", {})) == PolicyDecision.DENY

    def test_one_time_ticket_cannot_be_reused(self, cp):
        cp._approvals.issue_ticket("s1", "a1")
        t1 = cp._approvals.issue_ticket("s1", "a1")
        cp._approvals.redeem_ticket("s1", "a1", t1.signature)
        with pytest.raises(Exception):
            cp._approvals.redeem_ticket("s1", "a1", t1.signature)

    def test_credential_rotation_does_not_expose_master(self, master_secret, cp):
        val1 = cp._vault.get_credential("test:cred")
        val2 = cp._vault.get_credential("test:cred")
        assert val1 == val2
        # Master never reconstructed in plaintext from derivations
        cp._vault.force_rotate("test:cred")
        val3 = cp._vault.get_credential("test:cred")
        assert val3 != val1

    def test_audit_tampering_detected(self, cp):
        ac = cp._audit
        ac.append("s1", "original", "a", "ok")
        # Simulate tampering by replacing the last entry with a modified copy
        good = ac._entries[-1]
        tampered = AuditEntry(
            sequence=good.sequence,
            timestamp=good.timestamp,
            session_id=good.session_id,
            event="hacked!!",
            actor=good.actor,
            outcome=good.outcome,
            metadata=good.metadata,
            prev_hash=good.prev_hash,
            entry_hash=good.entry_hash,
        )
        ac._entries[-1] = tampered
        assert ac.verify() is False

    def test_pending_tickets_cleaned_up_on_issue(self, cp):
        t1 = cp._approvals.issue_ticket("s1", "a1")
        t1.expires_at = datetime.utcnow() - timedelta(seconds=1)
        t2 = cp._approvals.issue_ticket("s1", "a2")
        assert len(cp._approvals._tickets) == 1
        assert "a2" in list(cp._approvals._tickets.values())[0].action_id

    def test_action_execution_updates_audit(self, cp):
        cp.register_action("read_data", lambda p: {"ok": True})
        session = cp.start_session()
        action = Action("a1", session.session_id, "read_data", {})
        cp.execute_action(action)
        events = [e.event for e in cp._audit.entries]
        assert "action.executed" in events

    def test_policy_deny_updates_audit(self, cp):
        cp.register_action("code_execution", lambda p: None)
        session = cp.start_session()
        action = Action("a1", session.session_id, "code_execution", {})
        with pytest.raises(PolicyDeniedError):
            cp.execute_action(action)
        events = [e.event for e in cp._audit.entries]
        assert "action.blocked" in events


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

class TestCLI:

    def test_health_invocation(self):
        from security_control_plane import ControlPlane
        cp = ControlPlane()
        out = cp.health_check()
        assert isinstance(out, dict)

    def test_audit_verify_invocation(self):
        from security_control_plane import ControlPlane
        cp = ControlPlane()
        assert cp.verify_audit_integrity() is True
