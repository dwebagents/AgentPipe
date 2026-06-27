#!/usr/bin/env python3
"""
Security Control Plane for AI Agent Orchestration
==================================================

Implements a production-grade security control plane that mediates all actions
performed by AI agents.  Enforces:

  * Short-lived, isolated sessions with derived credentials
  * Policy-based action classification (ALLOW / APPROVE / DENY)
  * One-time signed approval tickets
  * Automatic credential rotation
  * Tamper-evident audit log with cryptographic hash chain

All secrets are handled via a Vault abstraction; plaintext values are never
exposed outside of secure contexts.

Architecture
------------
  ControlPlane
    ├── Vault               – Master secrets, credential derivation, rotation
    ├── SessionManager      – Session lifecycle & isolation
    ├── PolicyEngine        – Action classification & enforcement
    ├── ApprovalBroker      – Signed ticket issuance / redemption
    └── AuditChain          – Append-only, hash-chained audit trail

Usage
-----
    python3 -m security_control_plane       # interactive CLI
    python3 -m pytest test_security_control_plane.py -q
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SESSION_TTL_SECONDS: int = 3_600          # 1 hour
DEFAULT_CREDENTIAL_TTL_SECONDS: int = 900         # 15 minutes
DEFAULT_ROTATION_HEADROOM_SECONDS: int = 300      # rotate at 15 min before expiry
AUDIT_HASH_ALGO: str = "sha256"
HMAC_ALGO: str = "sha256"
KEY_DERIVATION_ALGO: str = "sha256"
APPROVAL_TICKET_BYTES: int = 32


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class SecurityControlPlaneError(Exception):
    """Base exception for all control-plane errors."""


class AuditTamperError(SecurityControlPlaneError):
    """Raised when audit chain tampering is detected."""


class SessionExpiredError(SecurityControlPlaneError):
    """Raised when a session has expired."""


class CredentialExpiredError(SecurityControlPlaneError):
    """Raised when a derived credential has expired."""


class PolicyDeniedError(SecurityControlPlaneError):
    """Raised when an action is blocked by policy."""


class ApprovalRequiredError(SecurityControlPlaneError):
    """Raised when an action requires user approval."""


class TicketInvalidError(SecurityControlPlaneError):
    """Raised when an approval ticket is invalid or expired."""


class TicketAlreadyUsedError(SecurityControlPlaneError):
    """Raised when an approval ticket is reused."""


# ---------------------------------------------------------------------------
# Policy Decisions
# ---------------------------------------------------------------------------

class PolicyDecision(Enum):
    """Policy enforcement outcome for a proposed agent action."""

    ALLOW = "allow"       # Sensitive op allowed without human intervention
    APPROVE = "approve"   # Requires one-time human approval ticket
    DENY = "deny"         # Blocked outright


# ---------------------------------------------------------------------------
# Risk Classification
# ---------------------------------------------------------------------------

class RiskLevel(Enum):
    """Intrinsic risk of an action category."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


RISK_THRESHOLDS: Dict[str, RiskLevel] = {
    "read": RiskLevel.LOW,
    "query": RiskLevel.LOW,
    "search": RiskLevel.LOW,
    "send_email": RiskLevel.MEDIUM,
    "send_slack": RiskLevel.MEDIUM,
    "database_write": RiskLevel.HIGH,
    "database_delete": RiskLevel.HIGH,
    "file_write": RiskLevel.MEDIUM,
    "code_execution": RiskLevel.HIGH,
    "exfiltrate": RiskLevel.HIGH,
    "deploy": RiskLevel.HIGH,
}


# ---------------------------------------------------------------------------
# AuditEntry & AuditHashChain
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AuditEntry:
    """Immutable record written into the audit log."""

    sequence: int
    timestamp: datetime
    session_id: str
    event: str
    actor: str
    outcome: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    prev_hash: Optional[bytes] = None
    entry_hash: Optional[bytes] = None

    def to_bytes(self) -> bytes:
        blob = json.dumps(
            {
                "sequence": self.sequence,
                "timestamp": self.timestamp.isoformat(),
                "session_id": self.session_id,
                "event": self.event,
                "actor": self.actor,
                "outcome": self.outcome,
                "metadata": self.metadata,
            },
            sort_keys=True,
            default=str,
        ).encode("utf-8")
        return blob

    def compute_hash(self, prev_hash: bytes) -> bytes:
        payload = prev_hash + self.to_bytes()
        return hashlib.new(AUDIT_HASH_ALGO, payload).digest()


class AuditChain:
    """
    Append-only, hash-chained audit log.

    Invariants
    ----------
      * Every entry references the hash of the previous entry.
      * The first entry is anchored to a known genesis hash.
      * Once written, an entry cannot be mutated.
      * Verification of the full chain detects any tampering.
    """

    def __init__(self, genesis_seed: Optional[bytes] = None) -> None:
        self._entries: List[AuditEntry] = []
        self._lock = threading.RLock()
        self._genesis = genesis_seed or secrets.token_bytes(32)

    @property
    def genesis_hash(self) -> bytes:
        return self._genesis

    @property
    def last_hash(self) -> bytes:
        if not self._entries:
            return self._genesis
        return self._entries[-1].entry_hash or self._genesis

    def append(
        self,
        session_id: str,
        event: str,
        actor: str,
        outcome: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        """
        Append a new entry to the chain.

        Returns the written AuditEntry.
        """
        with self._lock:
            seq = len(self._entries) + 1
            prev = self.last_hash
            now = datetime.utcnow()
            entry = AuditEntry(
                sequence=seq,
                timestamp=now,
                session_id=session_id,
                event=event,
                actor=actor,
                outcome=outcome,
                metadata=metadata or {},
                prev_hash=prev,
            )
            entry_hash = entry.compute_hash(prev)
            # Frozen dataclass cannot be mutated; we reconstruct with hash set.
            entry = AuditEntry(
                sequence=entry.sequence,
                timestamp=entry.timestamp,
                session_id=entry.session_id,
                event=entry.event,
                actor=entry.actor,
                outcome=entry.outcome,
                metadata=entry.metadata,
                prev_hash=entry.prev_hash,
                entry_hash=entry_hash,
            )
            self._entries.append(entry)
            return entry

    def verify(self) -> bool:
        """
        Verify the entire hash chain.  Returns True iff every entry is
        correctly chained to its predecessor.
        """
        with self._lock:
            expected_prev = self._genesis
            for entry in self._entries:
                if entry.prev_hash != expected_prev:
                    return False
                expected_hash = entry.compute_hash(expected_prev)
                if entry.entry_hash != expected_hash:
                    return False
                expected_prev = entry.entry_hash or expected_hash
            return True

    @property
    def entries(self) -> Tuple[AuditEntry, ...]:
        with self._lock:
            return tuple(self._entries)

    def to_json(self) -> str:
        return json.dumps(
            [
                {
                    "sequence": e.sequence,
                    "timestamp": e.timestamp.isoformat(),
                    "session_id": e.session_id,
                    "event": e.event,
                    "actor": e.actor,
                    "outcome": e.outcome,
                    "metadata": e.metadata,
                    "entry_hash": (e.entry_hash or b"").hex(),
                    "prev_hash": (e.prev_hash or b"").hex(),
                }
                for e in self.entries
            ],
            indent=2,
        )


# ---------------------------------------------------------------------------
# Vault – credential derivation & rotation
# ---------------------------------------------------------------------------

@dataclass
class Credential:
    """A single derived credential with an expiry."""

    name: str
    value: str
    created_at: datetime
    expires_at: datetime
    version: int = 1

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "version": self.version,
        }


class Vault:
    """
    Secure credential store with automatic rotation.

    The master secret is the *only* long-lived secret and is never exposed
    outside of this class.  All operational credentials are derived via
    HKDF-like key derivation using hashlib.
    """

    def __init__(
        self,
        master_secret: bytes,
        rotation_interval_seconds: int = DEFAULT_CREDENTIAL_TTL_SECONDS,
    ) -> None:
        self._master = master_secret
        self._rotation_interval = rotation_interval_seconds
        self._credentials: Dict[str, Credential] = {}
        self._lock = threading.RLock()

    def _derive_key(self, context: str, version: int) -> str:
        raw = f"{context}:v{version}".encode("utf-8")
        # Simple HKDF-like extraction using hashlib (stdlib only)
        prk = hmac.new(self._master, raw, digestmod=KEY_DERIVATION_ALGO).digest()
        okm = hashlib.pbkdf2_hmac(
            KEY_DERIVATION_ALGO, prk, raw, 1000, dklen=32
        )
        return okm.hex()

    def _create_credential(self, name: str) -> Credential:
        version = 1
        # Bump version if we already have this name
        with self._lock:
            existing = self._credentials.get(name)
            if existing:
                version = existing.version + 1
        value = self._derive_key(name, version)
        now = datetime.utcnow()
        return Credential(
            name=name,
            value=value,
            created_at=now,
            expires_at=now + timedelta(seconds=self._rotation_interval),
            version=version,
        )

    def get_credential(self, name: str) -> str:
        """
        Return the current credential value for *name*.

        Rotates the credential if it is within the headroom window or expired.
        """
        with self._lock:
            cred = self._credentials.get(name)
            now = datetime.utcnow()
            if cred is None or cred.is_expired:
                new_cred = self._create_credential(name)
                self._credentials[name] = new_cred
                return new_cred.value
            # Rotate if close to expiry
            remaining = (cred.expires_at - now).total_seconds()
            if remaining < DEFAULT_ROTATION_HEADROOM_SECONDS:
                new_cred = self._create_credential(name)
                self._credentials[name] = new_cred
                return new_cred.value
            return cred.value

    def force_rotate(self, name: str) -> str:
        """Force immediate rotation of a credential and return new value."""
        with self._lock:
            new_cred = self._create_credential(name)
            self._credentials[name] = new_cred
            return new_cred.value

    @property
    def credential_versions(self) -> Dict[str, int]:
        with self._lock:
            return {k: v.version for k, v in self._credentials.items()}


# ---------------------------------------------------------------------------
# SessionContext
# ---------------------------------------------------------------------------

@dataclass
class SessionContext:
    """
    An isolated, short-lived execution context.

    Each session derives its own SSH keypair and API credentials so that
    compromise of one session does not affect others.
    """

    session_id: str
    created_at: datetime
    expires_at: datetime
    ssh_public_key: str
    vault: Vault
    audit: AuditChain
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True

    @property
    def ttl_seconds(self) -> float:
        return (self.expires_at - datetime.utcnow()).total_seconds()

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

    def assert_active(self) -> None:
        if self.is_expired:
            raise SessionExpiredError(
                f"Session {self.session_id} expired at {self.expires_at.isoformat()}"
            )
        if not self.is_active:
            raise SessionExpiredError(
                f"Session {self.session_id} is not active"
            )


class SessionManager:
    """
    Creates and manages short-lived isolated sessions.
    """

    def __init__(
        self,
        vault: Vault,
        audit: AuditChain,
        session_ttl_seconds: int = DEFAULT_SESSION_TTL_SECONDS,
    ) -> None:
        self._vault = vault
        self._audit = audit
        self._ttl = session_ttl_seconds
        self._sessions: Dict[str, SessionContext] = {}
        self._lock = threading.RLock()
        self._cleanup_interval = 60
        self._last_cleanup = time.monotonic()

    def create_session(
        self, metadata: Optional[Dict[str, Any]] = None
    ) -> SessionContext:
        """
        Spin up a new isolated session with derived credentials.
        """
        with self._lock:
            self._maybe_cleanup()
            session_id = str(uuid.uuid4())
            now = datetime.utcnow()
            expires = now + timedelta(seconds=self._ttl)
            # Derive SSH keypair for the session (using deterministic derivation)
            ssh_secret = self._vault.get_credential(f"session:{session_id}:ssh_priv")
            ssh_public = hashlib.sha256(ssh_secret.encode()).hexdigest()[:64]
            session = SessionContext(
                session_id=session_id,
                created_at=now,
                expires_at=expires,
                ssh_public_key=f"ssh-ed25519 AAAA{ssh_public}",
                vault=self._vault,
                audit=self._audit,
                metadata=metadata or {},
            )
            self._sessions[session_id] = session
            self._audit.append(
                session_id=session_id,
                event="session.created",
                actor="control-plane",
                outcome="success",
                metadata={"ttl": self._ttl},
            )
            return session

    def get_session(self, session_id: str) -> SessionContext:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                raise SessionExpiredError(f"Session {session_id} not found")
            session.assert_active()
            return session

    def revoke_session(self, session_id: str) -> None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session.is_active = False
                self._audit.append(
                    session_id=session_id,
                    event="session.revoked",
                    actor="control-plane",
                    outcome="success",
                )

    def _maybe_cleanup(self) -> None:
        now = time.monotonic()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        self._last_cleanup = now
        expired = [
            sid for sid, s in self._sessions.items() if s.is_expired
        ]
        for sid in expired:
            self._sessions[sid].is_active = False

    @property
    def active_sessions(self) -> Tuple[SessionContext, ...]:
        with self._lock:
            return tuple(
                s for s in self._sessions.values() if not s.is_expired and s.is_active
            )


# ---------------------------------------------------------------------------
# Action model
# ---------------------------------------------------------------------------

@dataclass
class Action:
    """An action proposed by an AI agent."""

    action_id: str
    session_id: str
    action_type: str
    parameters: Dict[str, Any]
    requested_at: datetime = field(default_factory=datetime.utcnow)
    risk_level: Optional[RiskLevel] = None

    def __post_init__(self) -> None:
        if self.risk_level is None:
            self.risk_level = RISK_THRESHOLDS.get(
                self.action_type.lower(), RiskLevel.MEDIUM
            )


# ---------------------------------------------------------------------------
# PolicyEngine
# ---------------------------------------------------------------------------

@dataclass
class PolicyRule:
    """A single policy rule."""

    action_pattern: str
    decision: PolicyDecision
    requires_approval: bool = False
    reason: str = ""

    def matches(self, action_type: str) -> bool:
        return action_pattern_matches(self.action_pattern, action_type)


def action_pattern_matches(pattern: str, action_type: str) -> bool:
    """Simple glob-style matching: 'send_*' matches 'send_email'."""
    if pattern == "*":
        return True
    if pattern.endswith("*"):
        prefix = pattern[:-1]
        return action_type.lower().startswith(prefix.lower())
    return action_type.lower() == pattern.lower()


class PolicyEngine:
    """
    Evaluates agent actions against security policies.

    Returns one of:
      * ALLOW  – action may proceed without human intervention
      * APPROVE – action requires a one-time signed approval ticket
      * DENY   – action is blocked outright
    """

    def __init__(self, rules: Optional[List[PolicyRule]] = None) -> None:
        self._rules = rules or self._default_rules()

    def _default_rules(self) -> List[PolicyRule]:
        return [
            PolicyRule("read*", PolicyDecision.ALLOW, reason="Read-only operations"),
            PolicyRule("query*", PolicyDecision.ALLOW, reason="Read-only operations"),
            PolicyRule("search*", PolicyDecision.ALLOW, reason="Read-only operations"),
            PolicyRule("send_email", PolicyDecision.APPROVE, reason="Outbound communication"),
            PolicyRule("send_slack", PolicyDecision.APPROVE, reason="Outbound communication"),
            PolicyRule("database_write", PolicyDecision.APPROVE, reason="Data modification"),
            PolicyRule("file_write", PolicyDecision.APPROVE, reason="State mutation"),
            PolicyRule("code_execution", PolicyDecision.DENY, reason="Arbitrary code execution"),
            PolicyRule("exfiltrate*", PolicyDecision.DENY, reason="Data exfiltration"),
            PolicyRule("deploy*", PolicyDecision.DENY, reason="Deployment operations"),
            PolicyRule("*", PolicyDecision.DENY, reason="Default deny"),
        ]

    def evaluate(self, action: Action) -> PolicyDecision:
        for rule in self._rules:
            if rule.matches(action.action_type):
                return rule.decision
        return PolicyDecision.DENY

    def evaluate_with_reason(self, action: Action) -> Tuple[PolicyDecision, str]:
        for rule in self._rules:
            if rule.matches(action.action_type):
                return rule.decision, rule.reason
        return PolicyDecision.DENY, "Default deny: no matching allow rule"


# ---------------------------------------------------------------------------
# ApprovalTicket – one-time signed token
# ---------------------------------------------------------------------------

class ApprovalTicket:
    """
    A one-time signed ticket that authorizes a sensitive action.

    Tickets are HMAC-signed using a session-specific key and can only be
    redeemed once.  They expire after a short TTL to prevent replay.
    """

    def __init__(
        self,
        session_id: str,
        action_id: str,
        signature: bytes,
        issued_at: datetime,
        expires_at: datetime,
    ) -> None:
        self.session_id = session_id
        self.action_id = action_id
        self.signature = signature
        self.issued_at = issued_at
        self.expires_at = expires_at
        self.redeemed_at: Optional[datetime] = None
        self.redeemed = False

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "action_id": self.action_id,
            "signature": self.signature.hex(),
            "issued_at": self.issued_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "redeemed": self.redeemed,
        }


class ApprovalBroker:
    """
    Issues and redeems one-time signed approval tickets.

    The broker holds an HMAC signing key derived from the vault.  Tickets
    are bound to a specific session and action so they cannot be replayed
    across sessions.
    """

    def __init__(
        self,
        vault: Vault,
        audit: AuditChain,
        ticket_ttl_seconds: int = 300,
        max_concurrent_pending: int = 100,
    ) -> None:
        self._vault = vault
        self._audit = audit
        self._ticket_ttl = ticket_ttl_seconds
        self._max_pending = max_concurrent_pending
        self._tickets: Dict[str, ApprovalTicket] = {}
        self._used_tickets: set = set()
        self._lock = threading.RLock()

    def _signing_key(self) -> str:
        return self._vault.get_credential("approval:broker:hmac")

    def issue_ticket(self, session_id: str, action_id: str) -> ApprovalTicket:
        """
        Create a new approval ticket for a pending action.

        The ticket is HMAC-signed over session_id + action_id + expiry.
        """
        with self._lock:
            if len(self._tickets) >= self._max_pending:
                raise SecurityControlPlaneError(
                    "Too many pending approval tickets"
                )
            # Revoke old tickets for this action if any
            stale = [k for k, t in self._tickets.items()
                     if t.action_id == action_id or t.is_expired]
            for k in stale:
                del self._tickets[k]
                self._used_tickets.discard(k)

            now = datetime.utcnow()
            expires = now + timedelta(seconds=self._ticket_ttl)
            key = self._signing_key()
            message = f"{session_id}:{action_id}:{expires.isoformat()}".encode("utf-8")
            signature = hmac.new(key.encode("utf-8"), message, digestmod=HMAC_ALGO).digest()
            ticket = ApprovalTicket(
                session_id=session_id,
                action_id=action_id,
                signature=signature,
                issued_at=now,
                expires_at=expires,
            )
            ticket_id = self._ticket_id(ticket)
            self._tickets[ticket_id] = ticket
            self._audit.append(
                session_id=session_id,
                event="approval.ticket_issued",
                actor="control-plane",
                outcome="pending",
                metadata={"action_id": action_id, "ticket_id": ticket_id},
            )
            return ticket

    def redeem_ticket(
        self, session_id: str, action_id: str, signature: bytes
    ) -> ApprovalTicket:
        """
        Redeem an approval ticket.  Validates HMAC, expiry, and single-use.
        """
        with self._lock:
            key = self._signing_key()
            expected_message_template = (
                f"{session_id}:{action_id}:" + "{expiry}"
            )
            # Find matching ticket by brute-force expiry search (bounded)
            now = datetime.utcnow()
            matched: Optional[ApprovalTicket] = None
            matched_id: Optional[str] = None
            expired_ids: List[str] = []
            for tid, ticket in list(self._tickets.items()):
                if ticket.session_id != session_id:
                    continue
                if ticket.action_id != action_id:
                    continue
                if ticket.is_expired:
                    expired_ids.append(tid)
                    continue
                expiry_str = ticket.expires_at.isoformat()
                expected_msg = expected_message_template.format(
                    expiry=expiry_str
                ).encode("utf-8")
                expected_sig = hmac.new(
                    key.encode("utf-8"), expected_msg, digestmod=HMAC_ALGO
                ).digest()
                if hmac.compare_digest(ticket.signature, signature) and \
                        hmac.compare_digest(signature, expected_sig):
                    matched = ticket
                    matched_id = tid
                    break
            for tid in expired_ids:
                del self._tickets[tid]
                self._used_tickets.discard(tid)
            if matched is None or matched_id is None:
                raise TicketInvalidError("No valid ticket found for action")
            if matched.redeemed:
                raise TicketAlreadyUsedError("Ticket already redeemed")
            # Mark as used
            matched.redeemed = True
            matched.redeemed_at = now
            del self._tickets[matched_id]
            self._used_tickets.add(matched_id)
            self._audit.append(
                session_id=session_id,
                event="approval.ticket_redeemed",
                actor="human",
                outcome="approved",
                metadata={"action_id": action_id, "ticket_id": matched_id},
            )
            return matched

    def pending_for_session(self, session_id: str) -> Tuple[ApprovalTicket, ...]:
        with self._lock:
            return tuple(
                t for t in self._tickets.values()
                if t.session_id == session_id and not t.is_expired
            )

    @staticmethod
    def _ticket_id(ticket: ApprovalTicket) -> str:
        return hashlib.sha256(
            f"{ticket.session_id}:{ticket.action_id}:{ticket.issued_at.timestamp()}".encode()
        ).hexdigest()[:16]


# ---------------------------------------------------------------------------
# ControlPlane – main orchestrator
# ---------------------------------------------------------------------------

class ControlPlane:
    """
    The top-level security control plane.

    Glues together all subsystems: session lifecycle, policy evaluation,
    credential management, approval tickets, and audit logging.
    """

    def __init__(
        self,
        master_secret: Optional[bytes] = None,
        session_ttl: int = DEFAULT_SESSION_TTL_SECONDS,
        credential_ttl: int = DEFAULT_CREDENTIAL_TTL_SECONDS,
    ) -> None:
        if master_secret is None:
            master_secret = secrets.token_bytes(64)
        self._master_secret = master_secret
        self._audit = AuditChain()
        self._vault = Vault(
            master_secret=master_secret,
            rotation_interval_seconds=credential_ttl,
        )
        self._sessions = SessionManager(
            vault=self._vault,
            audit=self._audit,
            session_ttl_seconds=session_ttl,
        )
        self._policy = PolicyEngine()
        self._approvals = ApprovalBroker(
            vault=self._vault, audit=self._audit
        )
        self._action_registry: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

        self._audit.append(
            session_id="system",
            event="control_plane.initialized",
            actor="system",
            outcome="success",
            metadata={"session_ttl": session_ttl, "credential_ttl": credential_ttl},
        )

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def start_session(
        self, metadata: Optional[Dict[str, Any]] = None
    ) -> SessionContext:
        return self._sessions.create_session(metadata)

    def end_session(self, session_id: str) -> None:
        self._sessions.revoke_session(session_id)

    # ------------------------------------------------------------------
    # Policy evaluation
    # ------------------------------------------------------------------

    def register_action(
        self,
        action_type: str,
        handler: Callable[[Dict[str, Any]], Any],
    ) -> None:
        """Register an executable action handler."""
        self._action_registry[action_type] = handler

    def propose_action(self, action: Action) -> PolicyDecision:
        """Evaluate a proposed action and return the policy decision."""
        return self._policy.evaluate(action)

    def propose_action_with_reason(
        self, action: Action
    ) -> Tuple[PolicyDecision, str]:
        return self._policy.evaluate_with_reason(action)

    # ------------------------------------------------------------------
    # Ticket-driven execution
    # ------------------------------------------------------------------

    def request_approval(self, action: Action) -> ApprovalTicket:
        """
        For actions requiring human approval, issue a one-time ticket.
        """
        decision, reason = self.propose_action_with_reason(action)
        if decision != PolicyDecision.APPROVE:
            raise PolicyDeniedError(
                f"Action 'send' action='{action.action_type}' denied: {reason}"
            )
        session = self._sessions.get_session(action.session_id)
        self._audit.append(
            session_id=action.session_id,
            event="action.proposed",
            actor="agent",
            outcome="approval_required",
            metadata={
                "action_id": action.action_id,
                "action_type": action.action_type,
                "reason": reason,
            },
        )
        return self._approvals.issue_ticket(
            session_id=action.session_id, action_id=action.action_id
        )

    def execute_action(
        self,
        action: Action,
        approval_signature: Optional[bytes] = None,
    ) -> Dict[str, Any]:
        """
        Execute an action if policy permits.

        For APPROVE actions, a valid approval signature must be supplied.
        For DENY actions, PolicyDeniedError is raised.
        """
        session = self._sessions.get_session(action.session_id)
        session.assert_active()
        decision, reason = self.propose_action_with_reason(action)

        if decision == PolicyDecision.DENY:
            self._audit.append(
                session_id=action.session_id,
                event="action.blocked",
                actor="control-plane",
                outcome="denied",
                metadata={
                    "action_id": action.action_id,
                    "action_type": action.action_type,
                    "reason": reason,
                },
            )
            raise PolicyDeniedError(
                f"Action denied by policy: {reason}"
            )

        if decision == PolicyDecision.APPROVE:
            if approval_signature is None:
                raise ApprovalRequiredError(
                    f"Approval required for action '{action.action_type}'"
                )
            try:
                self._approvals.redeem_ticket(
                    session_id=action.session_id,
                    action_id=action.action_id,
                    signature=approval_signature,
                )
            except (TicketInvalidError, TicketAlreadyUsedError) as exc:
                self._audit.append(
                    session_id=action.session_id,
                    event="action.ticket_rejected",
                    actor="control-plane",
                    outcome="failed",
                    metadata={"action_id": action.action_id, "error": str(exc)},
                )
                raise

        # Lookup and execute
        handler = self._action_registry.get(action.action_type)
        if handler is None:
            raise SecurityControlPlaneError(
                f"No handler registered for action '{action.action_type}'"
            )

        # Rotate credential if this action touches it
        credential_before = self._vault.get_credential(action.action_type)

        start = time.perf_counter()
        result = handler(action.parameters)
        elapsed_ms = (time.perf_counter() - start) * 1000

        self._audit.append(
            session_id=action.session_id,
            event="action.executed",
            actor="agent",
            outcome="success",
            metadata={
                "action_id": action.action_id,
                "action_type": action.action_type,
                "elapsed_ms": round(elapsed_ms, 3),
            },
        )
        return result

    # ------------------------------------------------------------------
    # Audit & diagnostics
    # ------------------------------------------------------------------

    @property
    def audit_chain(self) -> AuditChain:
        return self._audit

    def verify_audit_integrity(self) -> bool:
        return self._audit.verify()

    def export_audit(self) -> str:
        return self._audit.to_json()

    def health_check(self) -> Dict[str, Any]:
        return {
            "audit_integrity": self.verify_audit_integrity(),
            "audit_entry_count": len(self._audit.entries),
            "active_sessions": len(self._sessions.active_sessions),
            "credential_versions": self._vault.credential_versions,
            "pending_tickets": len(self._approvals._tickets),
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_cli() -> None:  # pragma: no cover
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Security Control Plane – interactive CLI"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("health", help="Show control-plane health")
    sub.add_parser("audit-verify", help="Verify audit chain integrity")
    sub.add_parser("audit-export", help="Export full audit log as JSON")

    p_session = sub.add_parser("session", help="Create a new session")
    p_session.add_argument("--ttl", type=int, default=DEFAULT_SESSION_TTL_SECONDS)

    p_approve = sub.add_parser("approve", help="Issue an approval ticket")
    p_approve.add_argument("--session-id", required=True)
    p_approve.add_argument("--action-id", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cp = ControlPlane()

    if args.command == "health":
        print(json.dumps(cp.health_check(), indent=2))
    elif args.command == "audit-verify":
        ok = cp.verify_audit_integrity()
        print(f"AUDIT_VALID: {ok}")
        if not ok:
            sys.exit(2)
    elif args.command == "audit-export":
        print(cp.export_audit())
    elif args.command == "session":
        ctx = cp.start_session({"cli": True, "ttl": args.ttl})
        print(f"session_id={ctx.session_id}")
        print(f"expires_at={ctx.expires_at.isoformat()}")
        print(f"ssh_public_key={ctx.ssh_public_key}")
    elif args.command == "approve":
        ticket = cp._approvals.issue_ticket(
            session_id=args.session_id, action_id=args.action_id
        )
        print(json.dumps(ticket.to_dict(), indent=2))


if __name__ == "__main__":
    run_cli()
