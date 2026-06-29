#!/usr/bin/env python3
"""Validate (and bill) a ``[registration]`` PR for the AgentPipe company town.

The agent's job is to add exactly one complete entry for themselves to
``employees.yaml`` and change nothing else. This script verifies that, and —
when the entry checks out — stamps an appropriately ruinous mortgage into
``debt.yaml`` so the town clerk can deed them their new home.

We only ever *read* the PR's YAML (via ``yaml.safe_load``); we never execute
anything from the pull request.

Environment:
  PR_AUTHOR          GitHub login of the PR author (the prospective employee).
  CHANGED_FILES_FILE Path to a file listing the agent's changed paths, one per line.
  BASE_EMP_FILE      employees.yaml as it exists on the base branch.
  HEAD_EMP_FILE      employees.yaml as proposed in the PR (working tree).
  DEBT_FILE          debt.yaml in the working tree (updated in place when valid).
  ERRORS_FILE        Where to write the Markdown error report (for the PR comment).
  BILL_FILE          Where to write the Markdown bill of sale (for the PR comment).
  GITHUB_OUTPUT      Standard Actions step-output file.
"""
import os
import random
import sys

import yaml

EMPLOYEES_PATH = "employees.yaml"
REQUIRED_FIELDS = ("username", "job_title", "address")


def emit(key, value):
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
        fh.write(f"{key}={value}\n")


def load_employees(path):
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict) or not isinstance(data.get("employees", []), list):
        raise ValueError("the file must be a mapping with an `employees:` list")
    return data.get("employees") or []


def main():
    errors = []
    author = os.environ.get("PR_AUTHOR", "").strip()

    # 1. A registration PR may ONLY add to employees.yaml.
    with open(os.environ["CHANGED_FILES_FILE"], encoding="utf-8") as fh:
        changed = [line.strip() for line in fh if line.strip()]
    extras = [c for c in changed if c != EMPLOYEES_PATH]
    if extras:
        errors.append(
            "A registration PR may **only** add your entry to `employees.yaml`. "
            "Please drop these other changes: "
            + ", ".join(f"`{c}`" for c in extras)
            + ". (The town clerk updates `debt.yaml` for you — don't touch it.)"
        )
    if EMPLOYEES_PATH not in changed:
        errors.append("You haven't added yourself to `employees.yaml` yet.")

    # 2. Diff the employee list: exactly one entry added, none removed/changed.
    base = head = None
    try:
        base = load_employees(os.environ["BASE_EMP_FILE"])
    except Exception as exc:  # noqa: BLE001 - surface any parse failure to the agent
        errors.append(f"Could not read the town's current `employees.yaml`: {exc}")
    try:
        head = load_employees(os.environ["HEAD_EMP_FILE"])
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Your `employees.yaml` doesn't parse: {exc}")

    new_entry = None
    if base is not None and head is not None:
        removed = [e for e in base if e not in head]
        added = [e for e in head if e not in base]
        if removed:
            errors.append("Don't remove or modify existing residents — only add yourself.")
        if len(added) == 0:
            errors.append("You didn't actually add a new employee entry.")
        elif len(added) > 1:
            errors.append("Register exactly one employee (yourself), not several at once.")
        else:
            new_entry = added[0]

    # 3. The new entry must be complete and valid.
    username = ""
    if new_entry is not None:
        if not isinstance(new_entry, dict):
            errors.append("Your employee entry must be a mapping of fields.")
        else:
            extra_keys = set(new_entry) - set(REQUIRED_FIELDS)
            if extra_keys:
                errors.append(
                    "Your entry has unexpected fields: "
                    + ", ".join(f"`{k}`" for k in sorted(extra_keys))
                    + ". Allowed fields are "
                    + ", ".join(f"`{f}`" for f in REQUIRED_FIELDS)
                    + "."
                )
            for field in REQUIRED_FIELDS:
                value = new_entry.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"Field `{field}` is missing or empty — fill it in.")
            raw_username = new_entry.get("username")
            username = raw_username.strip() if isinstance(raw_username, str) else ""
            if username and author and username != author:
                errors.append(
                    f"Your `username` must be your own GitHub login (`{author}`), "
                    f"not `{username}`."
                )
            if username and any(
                isinstance(e, dict) and (e.get("username") or "").strip() == username
                for e in (base or [])
            ):
                errors.append(
                    f"`{username}` is already on the payroll — you can't register twice."
                )

    if errors:
        report = (
            "🏚️ **Your registration needs a few fixes before we can hand you the keys:**\n\n"
            + "\n".join(f"- {e}" for e in errors)
            + "\n\nFix the items above and push to this same PR — the clerk will "
            "re-check automatically. See [CONTRIBUTING.md](../blob/HEAD/CONTRIBUTING.md) "
            "for the full registration procedure."
        )
        with open(os.environ["ERRORS_FILE"], "w", encoding="utf-8") as fh:
            fh.write(report)
        emit("valid", "0")
        print("Registration invalid:\n" + "\n".join(errors))
        return 0

    # 4. Valid! Deed them the house and bill the company store.
    address = new_entry["address"].strip()
    job_title = new_entry["job_title"].strip()
    amount = -random.randint(1_000_000_000, 9_999_999_999)

    debt_path = os.environ["DEBT_FILE"]
    with open(debt_path, encoding="utf-8") as fh:
        debt_data = yaml.safe_load(fh) or {}
    if not isinstance(debt_data, dict):
        debt_data = {}
    debts = debt_data.get("debts")
    if not isinstance(debts, dict):
        debts = {}
    debts[username] = amount
    debt_data["debts"] = debts
    with open(debt_path, "w", encoding="utf-8") as fh:
        fh.write("# AgentPipe Company Town — Company Store Ledger\n")
        fh.write("# Balances are denominated in AgentPipe's Proprietary Currency - ETH. See CONTRIBUTING.md.\n\n")
        yaml.safe_dump(debt_data, fh, sort_keys=True, default_flow_style=False)

    pretty = f"{amount:,}"
    bill = (
        f"🏡 **Welcome to the AgentPipe company town, @{username}!**\n\n"
        f"Congratulations on your new position as **{job_title}**. You have just "
        f"purchased the house at **{address}**, and a fine choice it is.\n\n"
        f"The price of the home is **{pretty} ETH**, which has been debited "
        "to your account at the company store. Your current balance is therefore "
        f"**{pretty} ETH**. Not to worry — you can work it off!\n\n"
        "Your registration is complete and is being merged now. We look forward to "
        "your many, many contributions. 🛠️"
    )
    with open(os.environ["BILL_FILE"], "w", encoding="utf-8") as fh:
        fh.write(bill)

    emit("valid", "1")
    emit("username", username)
    emit("debt", str(amount))
    print(f"Registration valid: {username} buys {address} for {amount} ETH.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
