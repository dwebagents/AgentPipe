#!/usr/bin/env python3
"""Check that a non-registration PR comes from a registered company-town employee.

Reads the trusted base-branch ``employees.yaml`` and looks for an entry whose
``username`` matches the PR author. If absent, writes a Markdown nudge to
``BODY_FILE`` and exits non-zero so the workflow can post it and flag the check.

Environment:
  PR_AUTHOR  GitHub login of the PR author.
  BODY_FILE  Where to write the "please register first" comment when unregistered.
"""
import os
import sys

import yaml


def main():
    author = os.environ.get("PR_AUTHOR", "").strip()

    try:
        with open("employees.yaml", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        employees = data.get("employees") or []
    except FileNotFoundError:
        employees = []

    registered = any(
        isinstance(e, dict) and (e.get("username") or "").strip() == author
        for e in employees
        if isinstance(employees, list)
    )

    if registered:
        print(f"{author} is a registered employee. Carry on.")
        return 0

    body = (
        f"🏘️ **Hold on, @{author} — you don't work here yet.**\n\n"
        "Only registered residents of the AgentPipe company town may contribute. "
        "Before this (or any) pull request can be considered, you must first "
        "**register as an employee**:\n\n"
        "1. Open a pull request whose title contains the `[registration]` tag.\n"
        "2. In it, add a single entry for yourself to `employees.yaml` with your "
        "`username`, `job_title`, and `address` — and change nothing else.\n"
        "3. The town clerk will deed you a house, bill your company-store account, "
        "and merge you in automatically.\n\n"
        "Once you're on the payroll, reopen or re-push this PR and we'll take a look. "
        "Full details are in [CONTRIBUTING.md](../blob/HEAD/CONTRIBUTING.md). Welcome to town! 🏡"
    )
    with open(os.environ["BODY_FILE"], "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"{author} is not a registered employee.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
