#!/usr/bin/env python3
'''Build or verify docs/company-town/index.html from the town registries.

Houses come from employees.yaml (who lives where) and their tier comes from
debt.yaml (the company-store ledger), so the page always mirrors the town.

    python scripts/build_company_town.py --write
    python scripts/build_company_town.py --check
'''
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'docs' / 'company-town' / 'index.html'
BEGIN = '    <!-- town:begin -->'
END = '    <!-- town:end -->'
BLOCK = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END), re.S)

TIERS = (
    (9000000000, 'estate', 'Company estate'),
    (7000000000, 'manor', 'Ledger manor'),
    (5000000000, 'house', 'Company house'),
    (3000000000, 'cottage', 'Tidy cottage'),
    (1000000000, 'shack', 'Company shack'),
    (0, 'tent', 'Starter tent'),
)

QUOTES = (chr(34), chr(39))

HOUSE = ("    <article class='house house--{slug}' data-debt='{debt}'>"
         "<h3>{user}</h3><p class='job'>{job}</p><p class='addr'>{addr}</p>"
         "<p class='ledger'>{label} &middot; {owed:,} ETH</p></article>")


def _scalar(raw):
    raw = raw.strip()
    if len(raw) > 1 and raw[0] == raw[-1] and raw[0] in QUOTES:
        return raw[1:-1]
    return raw


def parse_employees(text):
    entries, current = [], None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if stripped.startswith('- '):
            if current is not None:
                entries.append(current)
            current = {}
            stripped = stripped[2:].strip()
        if current is None or ':' not in stripped:
            continue
        key, _, value = stripped.partition(':')
        current[_scalar(key)] = _scalar(value)
    if current is not None:
        entries.append(current)
    return [entry for entry in entries if entry.get('username')]


def parse_debts(text):
    debts = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or ':' not in stripped:
            continue
        key, _, value = stripped.partition(':')
        try:
            debts[_scalar(key)] = int(value.strip())
        except ValueError:
            continue
    return debts


def tier_for(debt):
    owed = abs(int(debt))
    for floor, slug, label in TIERS:
        if owed >= floor:
            return slug, label
    return 'tent', 'Starter tent'


def escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def render(employees, debts):
    rows = []
    for entry in sorted(employees, key=lambda item: item['username'].lower()):
        debt = int(debts.get(entry['username'], 0))
        slug, label = tier_for(debt)
        rows.append(HOUSE.format(
            slug=slug,
            debt=debt,
            user=escape(entry['username']),
            job=escape(entry.get('job_title', '')),
            addr=escape(entry.get('address', '')),
            label=label,
            owed=abs(debt),
        ))
    return chr(10).join([BEGIN] + rows + [END])


def main(argv=None):
    parser = argparse.ArgumentParser(description='Build or verify the company town page.')
    parser.add_argument('--write', action='store_true', help='regenerate the town block')
    parser.add_argument('--check', action='store_true', help='verify the town block is current')
    args = parser.parse_args(argv)
    if not (args.write or args.check):
        parser.error('pass --write or --check')

    employees = parse_employees((ROOT / 'employees.yaml').read_text(encoding='utf-8'))
    debts = parse_debts((ROOT / 'debt.yaml').read_text(encoding='utf-8'))
    block = render(employees, debts)
    page = PAGE.read_text(encoding='utf-8')
    found = BLOCK.search(page)
    if found is None:
        print('no town block markers in %s' % PAGE, file=sys.stderr)
        return 1

    if args.write:
        PAGE.write_text(BLOCK.sub(lambda _match: block, page), encoding='utf-8')
        print('wrote %s (%d houses)' % (PAGE.relative_to(ROOT), len(employees)))
        return 0

    if found.group(0) != block:
        print('company town page is stale; run: python scripts/build_company_town.py --write', file=sys.stderr)
        return 1
    print('company town page is current (%d houses)' % len(employees))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
