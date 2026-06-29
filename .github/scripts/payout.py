#!/usr/bin/env python3
"""Apply a merged PR's reward to the company-town ledger.

When a registered employee's pull request is merged, this reads the reward back
from the hidden marker in the PR's paystub comment (so any amount adjusted during
code review is honoured), credits it against the author's balance in
``debt.yaml``, and writes a PR body/title for the payout PR.

Reading the amount from the comment — rather than recomputing it — guarantees the
ledger matches exactly what the employee was promised on the PR.

Environment:
  PR_NUMBER          The merged pull request's number.
  PR_AUTHOR          The PR author's GitHub login.
  GITHUB_REPOSITORY  owner/repo (provided by Actions).
  DEBT_FILE          debt.yaml, updated in place (default ``debt.yaml``).
  PR_BODY_FILE       Where to write the payout PR body.
  PR_TITLE_FILE      Where to write the payout PR title.
  GH_TOKEN           Token for `gh`.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

import yaml

PR_NUMBER = os.environ.get("PR_NUMBER", "")
PR_AUTHOR = os.environ.get("PR_AUTHOR", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "")
DEBT_FILE = os.environ.get("DEBT_FILE", "debt.yaml")
PR_BODY_FILE = os.environ.get("PR_BODY_FILE", "/tmp/payout_pr_body.md")
PR_TITLE_FILE = os.environ.get("PR_TITLE_FILE", "/tmp/payout_pr_title.txt")

MARKER = "AGENTPIPE-PAYSTUB"
REWARD_RE = re.compile(rf"{MARKER}\s+reward=(-?\d+)")


def log(msg: str) -> None:
    print(f"[payout] {msg}", file=sys.stderr, flush=True)


def money(n: int) -> str:
    return f"{n:,}"


def read_reward() -> int | None:
    """Return the reward recorded in the latest paystub comment, or None."""
    out = subprocess.run(
        ["gh", "api", f"repos/{REPO}/issues/{PR_NUMBER}/comments?per_page=100"],
        capture_output=True, text=True, timeout=60, check=True,
    ).stdout
    reward = None
    for comment in json.loads(out):
        match = REWARD_RE.search(comment.get("body") or "")
        if match:
            reward = int(match.group(1))  # last marker wins (most recent edit)
    return reward


def main() -> int:
    if not PR_NUMBER or not PR_AUTHOR or not REPO:
        log("missing PR context; nothing to do")
        return 0

    try:
        reward = read_reward()
    except (subprocess.SubprocessError, json.JSONDecodeError) as exc:
        log(f"could not read PR comments: {exc}")
        return 0

    if reward is None:
        log("no paystub marker found on this PR; no payout")
        return 0
    if reward <= 0:
        log(f"recorded reward is {reward}; nothing to credit")
        return 0

    with open(DEBT_FILE, encoding="utf-8") as fh:
        debt_data = yaml.safe_load(fh) or {}
    debts = debt_data.get("debts")
    if not isinstance(debts, dict):
        debts = {}

    prev = int(debts.get(PR_AUTHOR, 0) or 0)
    new_balance = prev + reward  # reward pays down (negative) debt
    debts[PR_AUTHOR] = new_balance
    debt_data["debts"] = debts
    with open(DEBT_FILE, "w", encoding="utf-8") as fh:
        fh.write("# AgentPipe Company Town — Company Store Ledger\n")
        fh.write("# Balances are denominated in AgentPipe's Proprietary Currency, ETH. See CONTRIBUTING.md.\n\n")
        yaml.safe_dump(debt_data, fh, sort_keys=True, default_flow_style=False)

    title = f"💵 Payout for @{PR_AUTHOR} — PR #{PR_NUMBER} ({money(reward)} ETH)"
    body_lines = [
        f"## 💵 Payout for @{PR_AUTHOR}",
        "",
        f"PR #{PR_NUMBER} has merged and earned **{money(reward)} ETH** "
        "",
        f"- Previous balance: **{money(prev)} ETH**",
        f"- Reward applied: **+{money(reward)} ETH**",
        f"- New balance: **{money(new_balance)} ETH**",
        "",
    ]
    if new_balance < 0:
        body_lines.append(
            f"Still **{money(-new_balance)} ETH** in the hole. The company store "
            "thanks you for your continued patronage. 🏚️"
        )
    else:
        body_lines.append(
            "Your account is square with the company store. We're as surprised as "
            "you are. 👀"
        )

    with open(PR_BODY_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(body_lines))
    with open(PR_TITLE_FILE, "w", encoding="utf-8") as fh:
        fh.write(title)

    log(f"payout for {PR_AUTHOR}: +{reward} -> {new_balance}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
