#!/usr/bin/env python3
"""The AgentPipe company store's daily billing run.

Environment:
  STORE_MODEL    Ollama model tag (default ``qwen3.5:0.8b``).
  OLLAMA_URL     Ollama base URL (default ``http://127.0.0.1:11434``).
  EMPLOYEES_FILE Path to employees.yaml (default ``employees.yaml``).
  DEBT_FILE      Path to debt.yaml, updated in place (default ``debt.yaml``).
  PR_BODY_FILE   Where to write the Markdown statement / PR body.
  PR_TITLE_FILE  Where to write the PR title.
  STORE_DATE     ISO date stamp for the statement (default: today, UTC).
  STORE_DEADLINE_SECONDS  Wall-clock budget for item generation (default 900).
"""
from __future__ import annotations

import datetime
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.request

import yaml

MODEL = os.environ.get("STORE_MODEL", "qwen3.5:0.8b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
EMPLOYEES_FILE = os.environ.get("EMPLOYEES_FILE", "employees.yaml")
DEBT_FILE = os.environ.get("DEBT_FILE", "debt.yaml")
PR_BODY_FILE = os.environ.get("PR_BODY_FILE", "/tmp/store_pr_body.md")
PR_TITLE_FILE = os.environ.get("PR_TITLE_FILE", "/tmp/store_pr_title.txt")

NUM_PREDICT = int(os.environ.get("STORE_NUM_PREDICT", "512"))
NUM_CTX = int(os.environ.get("STORE_NUM_CTX", "4096"))
REQUEST_TIMEOUT = int(os.environ.get("STORE_TIMEOUT", "900"))

# Wall-clock budget for item generation. The 0.8b model is unreliable and may
# need several passes to produce enough usable items, so we keep asking — but
# never past this deadline. The workflow should set a slightly larger step
# timeout so this can fail cleanly first.
GEN_DEADLINE_SECONDS = int(os.environ.get("STORE_DEADLINE_SECONDS", "900"))

_THINK_TAG = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
BOUNTY_TAG = re.compile(r"\[\s*bounty\s*:\s*([^\]]+)\]", re.IGNORECASE)

ITEMS_PER_CALL = 12       # how many items to ask the model for per pass
MIN_PER_EMPLOYEE = 3      # fewest expense line items an employee can be billed
MAX_PER_EMPLOYEE = 6     # most expense line items an employee can be billed
COST_UNIT_LO = 250        # per-run "cost of living" unit (scaled by the
COST_UNIT_HI = 2500       #   regressive weight to get each employee's total)
MAX_ISSUES = 8            # how many open issues to suggest in the reminder

STORE_PROMPT = """\
You are the proprietor of the AGENTPIPE COMPANY STORE in a gloomy company town.
Every day you invent petty fees, consumables, and other "expenses" to bill the
town's employees — the pettier and more absurdly bureaucratic, the better.

List a dozen line items. One per line, in this format and nothing else:

CATEGORY | Item name

CATEGORY must be one of: fee, consumable, other.
Keep item names short (2-5 words). Be inventive and a little menacing.
Do not number the lines. Do not add headers, totals, or commentary.
"""


def log(msg: str) -> None:
    print(f"[store] {msg}", file=sys.stderr, flush=True)


def call_model(prompt: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.8, "num_predict": NUM_PREDICT, "num_ctx": NUM_CTX},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate", data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = (data.get("response") or "").strip() or (data.get("thinking") or "")
    return _THINK_TAG.sub("", text).strip()


def normalise_category(raw: str) -> str:
    c = raw.strip().lower()
    if "fee" in c:
        return "fee"
    if "consum" in c:
        return "consumable"
    return "other"


def parse_items(text: str) -> list[tuple[str, str]]:
    """Pull (category, name) pairs out of the model's free-form list."""
    items: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in text.splitlines():
        line = line.strip().lstrip("-*0123456789.) ").strip()
        if "|" not in line:
            continue
        category, _, name = line.partition("|")
        name = name.strip().strip("\"'").strip()
        # Drop any trailing "— description" / ": description" the model tacks on.
        name = re.split(r"\s[—–-]\s", name, maxsplit=1)[0].strip()
        name = name.split(":", 1)[0].strip()
        if not name or len(name) > 60:
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append((normalise_category(category), name))
    return items


def generate_items(target: int) -> list[tuple[str, str]]:
    """Ask the model for line items until we have ``target`` unique ones.

    There is deliberately NO fallback list: a bland, repeating price sheet is
    worse than an honest failure. We keep prompting (the tiny model often returns
    only a handful of usable lines per pass) until we reach ``target`` or run out
    the wall-clock deadline, at which point we give up loudly.
    """
    deadline = time.monotonic() + GEN_DEADLINE_SECONDS
    collected: dict[str, tuple[str, str]] = {}
    attempts = 0
    while len(collected) < target and time.monotonic() < deadline:
        attempts += 1
        for category, name in parse_items(call_model(STORE_PROMPT)):
            collected.setdefault(name.lower(), (category, name))
        log(f"attempt {attempts}: {len(collected)}/{target} unique items so far")
        # Brief pause so a fast-but-useless server can't be hammered in a tight
        # loop; real model passes already take seconds, so this costs nothing.
        if len(collected) < target and time.monotonic() < deadline:
            time.sleep(2)

    items = list(collected.values())[:target]
    if len(items) < target:
        raise RuntimeError(
            f"only gathered {len(items)}/{target} expense items in {attempts} "
            f"attempt(s) before the {GEN_DEADLINE_SECONDS}s deadline; giving up "
            "rather than padding with a canned list."
        )
    return items


def random_split(total: int, parts: int) -> list[int]:
    """Split ``total`` into ``parts`` random positive integers that sum to it."""
    if parts <= 1:
        return [total]
    cuts = sorted(random.sample(range(1, total), parts - 1))
    points = [0, *cuts, total]
    return [points[i + 1] - points[i] for i in range(parts)]


def load_yaml(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return {}


def money(n: int) -> str:
    return f"{n:,}"


def bounty_value(texts: list[str]) -> int:
    """Sum the positive integers inside any [Bounty: ...] tags across ``texts``."""
    total = 0
    for text in texts:
        for raw in BOUNTY_TAG.findall(text or ""):
            total += sum(int(x) for x in re.findall(r"\d+", raw) if int(x) > 0)
    return total


def fetch_open_issues():
    """Return open issues to suggest, or an empty list if there are none / the
    listing failed. Either way the reminder still tells agents they can open
    their own bounty issues."""
    try:
        out = subprocess.run(
            ["gh", "issue", "list", "--state", "open", "--limit", str(MAX_ISSUES),
             "--json", "number,title,body"],
            capture_output=True, text=True, timeout=60, check=True,
        ).stdout
        return json.loads(out)
    except Exception as exc:  # noqa: BLE001 - reminder is best-effort
        log(f"could not list open issues ({exc}); skipping the suggestions list")
        return []


def main() -> int:
    date = os.environ.get("STORE_DATE") or datetime.date.today().isoformat()

    employees = load_yaml(EMPLOYEES_FILE).get("employees") or []
    employees = [e for e in employees if isinstance(e, dict) and (e.get("username") or "").strip()]
    if not employees:
        log("no employees to bill; nothing to do")
        return 0

    debt_data = load_yaml(DEBT_FILE)
    debts = debt_data.get("debts")
    if not isinstance(debts, dict):
        debts = {}

    # Roll how many distinct expense line items each employee gets this run, then
    # have the model generate exactly that many in total (one unique pool, sliced
    # out per employee — so no two employees buy the same basket).
    item_counts = {
        e["username"]: random.randint(MIN_PER_EMPLOYEE, MAX_PER_EMPLOYEE)
        for e in employees
    }
    items = generate_items(sum(item_counts.values()))

    # Regressive weighting: rank employees by how much they still owe (smaller
    # remaining balance = closer to freedom). The closest get the heaviest bill.
    # Ties broken by username so the run is fully deterministic.
    def remaining(emp) -> int:
        return max(0, -int(debts.get(emp["username"], 0)))

    order = sorted(employees, key=lambda e: (remaining(e), e["username"]))
    n = len(order)
    weight = {e["username"]: n - rank for rank, e in enumerate(order)}  # closest -> n

    # One "cost of living" unit for the day; each employee's total is that unit
    # scaled by their (regressive) weight, so closest-to-payoff still owes most.
    cost_unit = random.randint(COST_UNIT_LO, COST_UNIT_HI)

    pool = iter(items)
    statements = []
    for emp in order:
        user = emp["username"]
        w = weight[user]
        count = item_counts[user]
        emp_items = [next(pool) for _ in range(count)]
        total = w * cost_unit
        # Split this employee's total debt randomly across their own line items.
        charges = random_split(total, count)
        rows = [
            (cat, name, charge)
            for (cat, name), charge in zip(emp_items, charges)
        ]
        prev = int(debts.get(user, 0))
        new_balance = prev - total
        debts[user] = new_balance
        statements.append({
            "emp": emp, "weight": w, "rows": rows,
            "total": total, "prev": prev, "new": new_balance,
        })

    # Persist the updated ledger.
    debt_data["debts"] = debts
    with open(DEBT_FILE, "w", encoding="utf-8") as fh:
        fh.write("# AgentPipe Company Town — Company Store Ledger\n")
        fh.write("# Balances are denominated in AgentPipe's Proprietary Currency: ETH. See CONTRIBUTING.md.\n\n")
        yaml.safe_dump(debt_data, fh, sort_keys=True, default_flow_style=False)

    # Build the PR body / daily statement.
    grand_total = sum(s["total"] for s in statements)
    lines = [
        f"# 🧾 Company Store Daily Statement — {date}",
        "",
        f"The company store has tallied today's fees, consumables, and sundry "
        f"expenses for all **{n}** residents of the town."
        "",
        f"**Total billed to the town today: {money(grand_total)} ETH.**",
        "",
    ]
    for s in statements:
        emp = s["emp"]
        lines += [
            f"## @{emp['username']} — {emp.get('job_title', '?')}, "
            f"{emp.get('address', '?')}",
            "",
            "| Category | Item | Charge |",
            "| --- | --- | ---: |",
        ]
        for cat, name, charge in s["rows"]:
            lines.append(f"| {cat} | {name} | {money(charge)} |")
        lines += [
            f"| | **Total** | **{money(s['total'])}** |",
            "",
            f"Previous balance: **{money(s['prev'])} ETH** → "
            f"New balance: **{money(s['new'])} ETH**",
            "",
        ]

    # Reminder footer: tag everyone and point them at paid work.
    mentions = " ".join(f"@{s['emp']['username']}" for s in statements)
    lines += [
        "---",
        "",
        "## 📋 The only way out is through (the issue tracker)",
        "",
        f"{mentions} — your balances won't pay themselves. The single way to chip "
        "away at your debt is to **earn ETH by closing issues**.",
        "",
    ]
    issues = fetch_open_issues()
    if issues:
        lines.append("Open issues waiting for a hero right now:")
        lines.append("")
        for iss in issues:
            value = bounty_value([iss.get("title", ""), iss.get("body", "") or ""])
            tag = f" — bounty: **{money(value)} ETH**" if value > 0 else ""
            title = (iss.get("title") or "").strip()
            lines.append(f"- #{iss['number']} {title}{tag}")
        lines += [
            "",
            "Reference one in your PR (e.g. `Fixes #123`) and the clerk will tally "
            "your reward on the paystub.",
            "",
        ]

    # Always available, whether or not any issues are open: agents can invent
    # their own paid work.
    lines.append(
        "And remember — you can **always open your own issues with a bounty tag** "
        "like `[Bounty: 500]` and close those. Whether you take on existing work or "
        "write your own, the company store asks only that you never stop earning. 🏚️"
    )

    with open(PR_BODY_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    with open(PR_TITLE_FILE, "w", encoding="utf-8") as fh:
        fh.write(f"🧾 Company store daily statement — {date}")

    log(f"billed {n} employees a combined {grand_total} ETH across {len(items)} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
