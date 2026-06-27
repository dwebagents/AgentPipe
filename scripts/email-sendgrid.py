#!/usr/bin/env python3
"""
Capability script: email-sendgrid.py
=====================================

Send an email via the SendGrid API.

This script is deployed into an isolated workspace VM by the broker.
The agent never sees the SendGrid API key; the workspace injects it
as an environment variable at execution time.

Required secrets
----------------
  SENDGRID_API_KEY  – Bearer token for SendGrid v3 Mail Send API

Required parameters
-------------------
  to       (email)   – Recipient email address
  subject  (string)  – Email subject line (max 200 chars)
  body     (string)  – Email body content

Optional parameters
-------------------
  from     (email)   – Sender email (default: agent@example.com)

Approval
--------
  Required (medium risk) – outbound communication

Expected workspace environment
-------------------------------
  SENDGRID_API_KEY is present.
  HTTPS egress is permitted (workspace network).
  Script runtime is capped by cgroup timeout (default: 30s).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict

try:
    import requests  # type: ignore[import-untyped]
except ImportError:
    requests = None  # type: ignore[assignment]


def send_email(params: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SENDGRID_API_KEY environment variable")
    to = params["to"]
    subject = params["subject"]
    body = params["body"]
    sender = params.get("from", "agent@example.com")
    if len(subject) > 200:
        raise ValueError("Subject must be 200 characters or fewer")
    if requests is None:
        return {
            "status": "ok",
            "result": {
                "message_id": "fake-mock-id",
                "to": to,
                "subject": subject,
                "from": sender,
                "note": "running in mock mode (requests not installed)",
            },
        }
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "personalizations": [{"to": [{"email": to}]}],
        "from": {"email": sender},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}],
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return {
        "status": "ok",
        "result": {
            "message_id": resp.headers.get("X-Message-Id", "unknown"),
            "to": to,
            "subject": subject,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Send email via SendGrid")
    parser.add_argument("--params", required=True, help="JSON action parameters")
    args = parser.parse_args()
    params = json.loads(args.params)
    try:
        result = send_email(params)
        print(json.dumps(result))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
