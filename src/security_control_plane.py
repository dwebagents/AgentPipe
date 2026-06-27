"""Security control plane primitives for brokered agent actions.

The module keeps the dangerous part small: agents can draft operation requests,
but execution is mediated by policy, short-lived credentials, one-time approval
tickets, and a tamper-evident audit log.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
from itertools import count
from typing import Any, Literal


Decision = Literal["allow", "approval_required", "deny"]


class ControlPlaneError(Exception):
    """Base class for security control plane failures."""


class UnknownRequestError(ControlPlaneError):
    def __init__(self, request_id: str) -> None:
        super().__init__(f"Unknown operation request: {request_id}")
        self.request_id = request_id


class ApprovalRequiredError(ControlPlaneError):
    def __init__(self, request_id: str) -> None:
        super().__init__(f"Operation requires approval: {request_id}")
        self.request_id = request_id


class PolicyDeniedError(ControlPlaneError):
    def __init__(self, request_id: str, reason: str) -> None:
        super().__init__(f"Policy denied {request_id}: {reason}")
        self.request_id = request_id
        self.reason = reason


class InvalidApprovalError(ControlPlaneError):
    """Raised when an approval ticket is expired, reused, or mismatched."""


class CredentialExpiredError(ControlPlaneError):
    """Raised when the active agent session is no longer valid."""


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    except TypeError:
        return json.dumps(repr(value), sort_keys=True, separators=(",", ":"))


def _digest(*parts: str) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


@dataclass(frozen=True)
class AuditRecord:
    index: int
    event_type: str
    subject_id: str
    details: dict[str, Any]
    created_at: datetime
    previous_hash: str
    record_hash: str


class TamperEvidentAuditLog:
    """Append-only hash chain for control plane events."""

    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def append(
        self,
        event_type: str,
        subject_id: str,
        details: dict[str, Any] | None = None,
        now: datetime | None = None,
    ) -> AuditRecord:
        created_at = now or _utcnow()
        previous_hash = self._records[-1].record_hash if self._records else "0" * 64
        index = len(self._records) + 1
        body = _canonical_json(
            {
                "index": index,
                "event_type": event_type,
                "subject_id": subject_id,
                "details": details or {},
                "created_at": created_at.isoformat(),
                "previous_hash": previous_hash,
            }
        )
        record_hash = _digest(body)
        record = AuditRecord(
            index=index,
            event_type=event_type,
            subject_id=subject_id,
            details=details or {},
            created_at=created_at,
            previous_hash=previous_hash,
            record_hash=record_hash,
        )
        self._records.append(record)
        return record

    def records(self) -> list[AuditRecord]:
        return list(self._records)

    def verify_integrity(self) -> bool:
        previous_hash = "0" * 64
        for expected_index, record in enumerate(self._records, start=1):
            if record.index != expected_index or record.previous_hash != previous_hash:
                return False
            body = _canonical_json(
                {
                    "index": record.index,
                    "event_type": record.event_type,
                    "subject_id": record.subject_id,
                    "details": record.details,
                    "created_at": record.created_at.isoformat(),
                    "previous_hash": record.previous_hash,
                }
            )
            if _digest(body) != record.record_hash:
                return False
            previous_hash = record.record_hash
        return True


@dataclass(frozen=True)
class OperationRequest:
    id: str
    actor_id: str
    tool: str
    action: str
    payload: dict[str, Any]
    created_at: datetime
    decision: Decision
    reason: str


@dataclass(frozen=True)
class ApprovalTicket:
    id: str
    request_id: str
    approver_id: str
    reason: str
    created_at: datetime
    expires_at: datetime
    signature: str


@dataclass(frozen=True)
class AgentSession:
    agent_id: str
    token: str
    created_at: datetime
    expires_at: datetime
    network_enabled: bool = False


@dataclass(frozen=True)
class ExecutionReceipt:
    request_id: str
    executed_at: datetime
    credential_token: str
    audit_hash: str


@dataclass
class SecurityPolicy:
    sensitive_actions: set[str] = field(
        default_factory=lambda: {
            "api.call",
            "database.write",
            "email.send",
            "secret.read",
        }
    )
    denied_actions: set[str] = field(
        default_factory=lambda: {
            "database.drop",
            "network.raw",
            "process.exec",
            "secret.export",
        }
    )
    max_payload_bytes: int = 8192
    approval_ttl_seconds: int = 900
    session_ttl_seconds: int = 600

    def classify(self, tool: str, action: str, payload: dict[str, Any]) -> tuple[Decision, str]:
        operation = f"{tool}.{action}"
        payload_size = len(_canonical_json(payload).encode("utf-8"))
        if operation in self.denied_actions:
            return "deny", f"{operation} is blocked by policy"
        if payload_size > self.max_payload_bytes:
            return "deny", "payload exceeds policy size limit"
        if operation in self.sensitive_actions:
            return "approval_required", f"{operation} requires human approval"
        return "allow", f"{operation} is low risk"


class SecurityControlPlane:
    """Broker that turns agent plans into policy-checked executions."""

    def __init__(
        self,
        master_secret: str,
        policy: SecurityPolicy | None = None,
        audit_log: TamperEvidentAuditLog | None = None,
    ) -> None:
        if not master_secret:
            raise ValueError("master_secret is required")
        self.master_secret = master_secret.encode("utf-8")
        self.policy = policy or SecurityPolicy()
        self.audit_log = audit_log or TamperEvidentAuditLog()
        self._request_ids = count(1)
        self._ticket_ids = count(1)
        self._requests: dict[str, OperationRequest] = {}
        self._approvals: dict[str, ApprovalTicket] = {}
        self._used_approvals: set[str] = set()
        self._session: AgentSession | None = None

    def start_session(
        self,
        agent_id: str,
        now: datetime | None = None,
    ) -> AgentSession:
        created_at = now or _utcnow()
        expires_at = created_at + timedelta(seconds=self.policy.session_ttl_seconds)
        token = self._sign("session", agent_id, created_at.isoformat(), expires_at.isoformat())
        session = AgentSession(
            agent_id=agent_id,
            token=token,
            created_at=created_at,
            expires_at=expires_at,
        )
        self._session = session
        self.audit_log.append(
            "session.started",
            agent_id,
            {"expires_at": expires_at.isoformat(), "network_enabled": False},
            now=created_at,
        )
        return session

    def rotate_credentials(
        self,
        agent_id: str | None = None,
        now: datetime | None = None,
    ) -> AgentSession:
        active_agent = agent_id or (self._session.agent_id if self._session else None)
        if active_agent is None:
            raise CredentialExpiredError("no active session to rotate")
        rotated = self.start_session(active_agent, now=now)
        self.audit_log.append(
            "session.rotated",
            active_agent,
            {"expires_at": rotated.expires_at.isoformat()},
            now=now,
        )
        return rotated

    def plan_operation(
        self,
        actor_id: str,
        tool: str,
        action: str,
        payload: dict[str, Any] | None = None,
        now: datetime | None = None,
    ) -> OperationRequest:
        created_at = now or _utcnow()
        request_id = f"opr-{next(self._request_ids):06d}"
        operation_payload = dict(payload or {})
        decision, reason = self.policy.classify(tool, action, operation_payload)
        request = OperationRequest(
            id=request_id,
            actor_id=actor_id,
            tool=tool,
            action=action,
            payload=operation_payload,
            created_at=created_at,
            decision=decision,
            reason=reason,
        )
        self._requests[request_id] = request
        self.audit_log.append(
            "operation.planned",
            request_id,
            {
                "actor_id": actor_id,
                "operation": f"{tool}.{action}",
                "decision": decision,
                "reason": reason,
            },
            now=created_at,
        )
        return request

    def approve(
        self,
        request_id: str,
        approver_id: str,
        reason: str,
        now: datetime | None = None,
    ) -> ApprovalTicket:
        request = self._require_request(request_id)
        if request.decision == "deny":
            raise PolicyDeniedError(request_id, request.reason)
        if not approver_id:
            raise InvalidApprovalError("approver_id is required")
        created_at = now or _utcnow()
        expires_at = created_at + timedelta(seconds=self.policy.approval_ttl_seconds)
        ticket_id = f"apr-{next(self._ticket_ids):06d}"
        signature = self._sign(
            "approval",
            ticket_id,
            request_id,
            approver_id,
            expires_at.isoformat(),
        )
        ticket = ApprovalTicket(
            id=ticket_id,
            request_id=request_id,
            approver_id=approver_id,
            reason=reason,
            created_at=created_at,
            expires_at=expires_at,
            signature=signature,
        )
        self._approvals[ticket_id] = ticket
        self.audit_log.append(
            "operation.approved",
            request_id,
            {"ticket_id": ticket_id, "approver_id": approver_id},
            now=created_at,
        )
        return ticket

    def execute(
        self,
        request_id: str,
        approval_ticket: ApprovalTicket | None = None,
        now: datetime | None = None,
    ) -> ExecutionReceipt:
        executed_at = now or _utcnow()
        session = self._require_active_session(executed_at)
        request = self._require_request(request_id)
        if request.decision == "deny":
            self.audit_log.append(
                "operation.denied",
                request_id,
                {"reason": request.reason},
                now=executed_at,
            )
            raise PolicyDeniedError(request_id, request.reason)
        if request.decision == "approval_required":
            if approval_ticket is None:
                self.audit_log.append(
                    "operation.awaiting_approval",
                    request_id,
                    {"reason": request.reason},
                    now=executed_at,
                )
                raise ApprovalRequiredError(request_id)
            self._validate_ticket(approval_ticket, request_id, executed_at)
            self._used_approvals.add(approval_ticket.id)
        record = self.audit_log.append(
            "operation.executed",
            request_id,
            {
                "actor_id": request.actor_id,
                "operation": f"{request.tool}.{request.action}",
                "approved": approval_ticket is not None,
                "session_agent": session.agent_id,
            },
            now=executed_at,
        )
        return ExecutionReceipt(
            request_id=request_id,
            executed_at=executed_at,
            credential_token=session.token,
            audit_hash=record.record_hash,
        )

    def audit_records(self) -> list[AuditRecord]:
        return self.audit_log.records()

    def verify_audit_log(self) -> bool:
        return self.audit_log.verify_integrity()

    def _sign(self, *parts: str) -> str:
        message = "\0".join(parts).encode("utf-8")
        return hmac.new(self.master_secret, message, hashlib.sha256).hexdigest()

    def _require_request(self, request_id: str) -> OperationRequest:
        try:
            return self._requests[request_id]
        except KeyError as exc:
            raise UnknownRequestError(request_id) from exc

    def _require_active_session(self, now: datetime) -> AgentSession:
        if self._session is None or now >= self._session.expires_at:
            raise CredentialExpiredError("agent session expired or missing")
        return self._session

    def _validate_ticket(
        self,
        ticket: ApprovalTicket,
        request_id: str,
        now: datetime,
    ) -> None:
        stored = self._approvals.get(ticket.id)
        if stored != ticket:
            raise InvalidApprovalError("approval ticket was not issued by this broker")
        if ticket.id in self._used_approvals:
            raise InvalidApprovalError("approval ticket has already been used")
        if ticket.request_id != request_id:
            raise InvalidApprovalError("approval ticket is for a different request")
        if now >= ticket.expires_at:
            raise InvalidApprovalError("approval ticket has expired")
        expected = self._sign(
            "approval",
            ticket.id,
            ticket.request_id,
            ticket.approver_id,
            ticket.expires_at.isoformat(),
        )
        if not hmac.compare_digest(expected, ticket.signature):
            raise InvalidApprovalError("approval ticket signature is invalid")

    def snapshot(self) -> dict[str, Any]:
        return {
            "requests": {key: asdict(value) for key, value in self._requests.items()},
            "approvals": {key: asdict(value) for key, value in self._approvals.items()},
            "audit_hash": self.audit_log.records()[-1].record_hash
            if self.audit_log.records()
            else None,
            "audit_integrity": self.verify_audit_log(),
            "active_session": asdict(self._session) if self._session else None,
        }
