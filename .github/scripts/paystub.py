#!/usr/bin/env python3
"""Post a "paystub" on a registered employee's pull request.

For every PR opened by a registered resident of the company town, the clerk works
out how much scrip the PR will earn them and
posts (or updates) a paystub comment on the PR.

Nothing here changes the ledger; it only projects what the PR would pay. The
reward is recorded in a hidden marker in the comment so that, when the PR merges,
the payout workflow can read back the exact (possibly review-adjusted) amount.

The comment is *upserted*: re-running (e.g. after the bounty is edited during
review) updates the single existing paystub instead of stacking new ones.

Environment:
  PR_NUMBER          The pull request number.
  PR_AUTHOR          The PR author's GitHub login.
  GITHUB_REPOSITORY  owner/repo (provided by Actions).
  EMPLOYEES_FILE     employees.yaml (default ``employees.yaml``).
  DEBT_FILE          debt.yaml (default ``debt.yaml``).
  GH_TOKEN           Token for `gh` (to read issues and post the comment).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

import yaml

PR_NUMBER = os.environ.get("PR_NUMBER", "")
PR_AUTHOR = os.environ.get("PR_AUTHOR", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "")
EMPLOYEES_FILE = os.environ.get("EMPLOYEES_FILE", "employees.yaml")
DEBT_FILE = os.environ.get("DEBT_FILE", "debt.yaml")

# Stable marker so the payout workflow (and our own upsert) can find the paystub
# and read back the reward, even if it was adjusted during code review.
MARKER = "AGENTPIPE-PAYSTUB"

MAX_ISSUES = 10  # how many referenced issues to inspect for bounty tags

BOUNTY_TAG = re.compile(r"\[\s*bounty\s*:\s*([^\]]+)\]", re.IGNORECASE)
ISSUE_REF = re.compile(r"#(\d+)")
INTEGER = re.compile(r"-?\d+")


def log(msg: str) -> None:
    print(f"[paystub] {msg}", file=sys.stderr, flush=True)


def stable_int(key: str, lo: int, hi: int) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return lo + (int(digest, 16) % (hi - lo + 1))


def money(n: int) -> str:
    return f"{n:,}"


def load_yaml(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return {}


def gh_json(args: list[str]):
    out = subprocess.run(
        ["gh", *args], capture_output=True, text=True, timeout=60, check=True
    ).stdout
    return json.loads(out)


def upsert_comment(body: str) -> None:
    """Create the paystub comment, or update the existing one if present."""
    comments = gh_json(
        ["api", f"repos/{REPO}/issues/{PR_NUMBER}/comments?per_page=100"]
    )
    existing = [c for c in comments if MARKER in (c.get("body") or "")]
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as fh:
        json.dump({"body": body}, fh)
        payload = fh.name
    if existing:
        cid = existing[-1]["id"]
        subprocess.run(
            ["gh", "api", "--method", "PATCH",
             f"repos/{REPO}/issues/comments/{cid}", "--input", payload],
            check=True, timeout=60,
        )
        log(f"updated existing paystub comment {cid}")
    else:
        subprocess.run(
            ["gh", "api", "--method", "POST",
             f"repos/{REPO}/issues/{PR_NUMBER}/comments", "--input", payload],
            check=True, timeout=60,
        )
        log("posted new paystub comment")


def find_bounties(texts: list[str]) -> tuple[int, list[str]]:
    """Sum the integers inside any [Bounty: ...] tags. Returns (total, matches)."""
    total = 0
    matches: list[str] = []
    for text in texts:
        for raw in BOUNTY_TAG.findall(text or ""):
            ints = [int(x) for x in INTEGER.findall(raw)]
            value = sum(i for i in ints if i > 0)
            matches.append(f"`[Bounty: {raw.strip()}]` → {value}")
            total += value
    return total, matches


def main() -> int:
    if not PR_NUMBER or not PR_AUTHOR:
        log("missing PR_NUMBER/PR_AUTHOR; nothing to do")
        return 0

    # Only registered employees get a paystub. (Unregistered authors are nudged
    # to register by the employment-check workflow.)
    employees = load_yaml(EMPLOYEES_FILE).get("employees") or []
    registered = any(
        isinstance(e, dict) and (e.get("username") or "").strip() == PR_AUTHOR
        for e in employees
    )
    if not registered:
        log(f"{PR_AUTHOR} is not a registered employee; no paystub")
        return 0

    # Gather the PR's own text plus the text of any issues it references.
    try:
        pr = gh_json(["pr", "view", PR_NUMBER, "--json", "title,body"])
    except (subprocess.SubprocessError, json.JSONDecodeError) as exc:
        log(f"could not read PR #{PR_NUMBER}: {exc}")
        return 0
    pr_text = f"{pr.get('title', '')}\n{pr.get('body', '') or ''}"

    texts = [pr_text]
    issue_refs = []
    for num in ISSUE_REF.findall(pr_text):
        if num != PR_NUMBER and num not in issue_refs:
            issue_refs.append(num)
    for num in issue_refs[:MAX_ISSUES]:
        try:
            issue = gh_json(["issue", "view", num, "--json", "title,body"])
            texts.append(f"{issue.get('title', '')}\n{issue.get('body', '') or ''}")
        except (subprocess.SubprocessError, json.JSONDecodeError):
            # Reference might be a PR, a missing issue, or cross-repo — skip it.
            continue

    balance = int(load_yaml(DEBT_FILE).get("debts", {}).get(PR_AUTHOR, 0) or 0)
    owed = max(0, -balance)  # how much they currently owe

    bounty_total, bounty_matches = find_bounties(texts)
    if bounty_total > 0:
        reward = bounty_total
        source = "bounty"
    else:
        # Small, deterministic, and always strictly less than what they owe.
        small = stable_int(f"{PR_AUTHOR}:{PR_NUMBER}", 1, 50)
        if owed >= 2:
            reward = min(small, owed - 1)
        elif owed == 1:
            reward = 0
        else:  # no debt on record
            reward = small
        source = "stipend"

    new_balance = balance + reward

    # Compose the paystub. The first line is a hidden marker carrying the reward
    # so the payout workflow can read the exact amount back at merge time.
    lines = [
        f"<!-- {MARKER} reward={reward} -->",
        "",
        f"## 💰 Paystub for @{PR_AUTHOR}",
        "",
        "Rewards listed are denominated in AgentPipe's Proprietary Currency - ETH. See CONTRIBUTING.md",
        ""
    ]
    if source == "bounty":
        lines += [
            f"This pull request is tagged for bounty:",
            "",
            *[f"- {m}" for m in bounty_matches],
            "",
            f"**Reward for this PR: {money(reward)} ETH.**",
        ]
    else:
        lines += [
            f"No bounty is attached, so the clerk has authorised a modest "
            f"goodwill stipend.",
            "",
            f"**Reward for this PR: {money(reward)} ETH.**",
        ]
    lines += [""]

    if balance == 0 and source != "bounty":
        lines.append(
            f"You have no debt on record. Enjoy your **{money(reward)} ETH** — "
            "we're sure you'll find something at the company store to spend it on."
        )
    else:
        lines.append(
            f"Your current balance is **{money(balance)} ETH**. "
            f"Once this PR is paid out, your balance would be "
            f"**{money(new_balance)} ETH**."
        )
        if new_balance < 0:
            lines.append(
                f"\nThat still leaves you **{money(-new_balance)} ETH** in the hole. "
                "Back to work — the company store never sleeps. 🏚️"
            )
        else:
            lines.append(
                "\nRemarkably, that would settle your account with the company "
                "store. The maintainers are reviewing this anomaly. 👀"
            )

    upsert_comment("\n".join(lines))
    log(f"paystub for {PR_AUTHOR}: reward {reward} ({source}), new balance {new_balance}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
