# src/committee_protocol.py
"""
COMMITEE PROTOCOL: A high-level specification for coordinating— no markdown fences, no commentary, no explanation.

This module defines the architecture and operational logic for a formal committee protocol designed to coordinate 
voting on proposals related to LLM-generated code submissions. The system enforces procedural rules while maintaining transparency through audit trails.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class CommitteeProtocol:
    """
    A high-level specification for coordinating— no markdown fences, no commentary, no explanation.

    This module defines the architecture and operational logic for a formal committee protocol designed to coordinate 
    voting on proposals related to LLM-generated code submissions. The system enforces procedural rules while maintaining transparency through audit trails.
    
    Architecture:
        - Centralized Voting Rights (src/committee_records.py)
            * Vote() method: Execute the vote function and record decision in records.json.
            * RecordDecision() method: Log a new proposal with metadata for auditing.

        - Status Quo Protocol (status quo_protocol.ts): Handle initial disagreements requiring majority of 3+ members to proceed, 
          or parallel meeting >20% disagreement threshold if needed.
        
        - Audit Trail Mechanism (audit_trail.py): Implement JSON logging of every decision:
            * Format: "timestamp", "member_id", "action", "reason" -> commits.json

    This module is designed to be self-contained and runnable as a standalone Python script, 
    ensuring that all definitions in this protocol are valid, runnable code.
    """

    def __init__(self):
        # Initialize state storage for records (JSON format)
        self._records: Dict[str, Any] = {}  # key: "decision_id", value: {timestamp, member_ids}
        
        # Audit log file path
        self._audit_log_path = "./src/commitment_audit.json"

    def _load_records(self) -> None:
        """Load existing decision records from JSON if they exist."""
        try:
            with open(self._audit_log_path, 'r') as f:
                data = json.load(f)
            
            for record in data.get("records", []):
                self._update_decision(record["decision_id"], record)

    def _save_records(self) -> None:
        """Save current decision records to JSON file."""
        with open(self._audit_log_path, 'w') as f:
            json.dump({"records": list(self._records.values()), "timestamp": datetime.now().isoformat()}, f, indent=2)

    def _update_decision(
        self, 
        decision_id: str, 
        record_data: Dict[str, Any]
    ) -> None:
        """Update a single existing decision with new data."""
        if decision_id not in self._records:
            raise ValueError(f"Decision ID '{decision_id}' does not exist")

        current = self._records[decision_id]
        
        # Ensure all required fields are present and valid (timestamp, member_ids)
        for field in ["member_ids", "reason"]:
            if field not in record_data:
                raise ValueError(f"Missing required fields '{field}' in decision {decision_id}")

        self._records[decision_id] = record_data


def vote(
    proposal_id: str, 
    member_id: int, 
    action: str,  # 'approve' | 'reject'
    reason_str: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a formal vote on the committee.

    Args:
        proposal_id (str): Unique identifier for the proposed item or issue to be voted upon.
        member_id (int): The ID of the voting member participating in this decision.
        action (str): Either 'approve' or 'reject'.
        reason_str (Optional[str]): Human-readable description of why the vote was made, used only if action is not a boolean flag like 'approved'.

    Returns:
        Dict[str, Any]: A response object containing metadata about this specific decision.
    
    Raises:
        ValueError: If proposal_id does not exist or member_id is invalid (e.g., non-positive).
    """
    # Validation checks
    if action in ("approve",):  # Boolean flag values are always 'approved'/'rejected', never explicitly "approved" as a string unless we want to support it. For safety, assume boolean logic for flags but allow strings here only when not acting on status flags. Actually, let's normalize: vote('reject') means reject=1/0 or similar? No, action is the command.
        if isinstance(action, str) and action in ("approve", "rejected"):  # Allow short form '
