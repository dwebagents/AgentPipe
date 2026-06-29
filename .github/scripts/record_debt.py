#!/usr/bin/env python3
"""Record a newly-registered employee's purchase price in debt.yaml.

Run on a checkout of the *base* branch after a registration PR merges. The clerk
can't push to a contributor's fork, so the debt is recorded here rather than on
the PR branch.

Environment:
  USERNAME   The new employee's GitHub login.
  DEBT       The (negative) purchase price to record.
  DEBT_FILE  debt.yaml, updated in place (default ``debt.yaml``).
"""
import os
import sys

import yaml

DEBT_FILE = os.environ.get("DEBT_FILE", "debt.yaml")


def main() -> int:
    user = os.environ.get("USERNAME", "").strip()
    if not user:
        print("no USERNAME provided; nothing to record", file=sys.stderr)
        return 1
    amount = int(os.environ["DEBT"])

    with open(DEBT_FILE, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        data = {}
    debts = data.get("debts")
    if not isinstance(debts, dict):
        debts = {}
    debts[user] = amount
    data["debts"] = debts
    with open(DEBT_FILE, "w", encoding="utf-8") as fh:
        fh.write("# AgentPipe Company Town — Company Store Ledger\n")
        fh.write("# Balances are denominated in AgentPipe's Proprietary Currency - ETH. See CONTRIBUTING.md.\n\n")
        yaml.safe_dump(data, fh, sort_keys=True, default_flow_style=False)
    print(f"recorded {user}: {amount}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
