#!/usr/bin/env python3
"""Record a public hiring intake note for every pull request.

The intake system is intentionally comment-based: it records every PR author
without letting contributor PRs mutate employees.yaml or debt.yaml. It only uses
public PR metadata from GitHub, extracts bounded 12-24 word phrases from that
public text, and upserts a single clerk-owned comment.

Environment:
  PR_NUMBER          Pull request number to record.
  PR_AUTHOR          Optional GitHub login of the PR author.
  GITHUB_REPOSITORY  owner/repo (provided by Actions).
  GH_TOKEN           Token for gh.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from typing import Any

PR_NUMBER = os.environ.get("PR_NUMBER", "")
PR_AUTHOR = os.environ.get("PR_AUTHOR", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "")

MARKER = "AGENTPIPE-HIRING-INTAKE"
CLERK_LOGIN = "agentpipe-clerk[bot]"

WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_'/.-]*")
LONG_SECRET_RE = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|[A-Fa-f0-9]{32,}|[A-Za-z0-9+/]{40,}={0,2})\b"
)
URL_RE = re.compile(r"https?://\S+")
EMAIL_RE = re.compile(r"\b[^@\s]+@[^@\s]+\.[^@\s]+\b")


def log(message: str) -> None:
    print(f"[hiring-intake] {message}", file=sys.stderr, flush=True)


def gh_json(args: list[str]) -> Any:
    out = subprocess.run(
        ["gh", *args], capture_output=True, text=True, timeout=60, check=True
    ).stdout
    return json.loads(out)


def redact_public_text(text: str) -> str:
    text = URL_RE.sub(" public-url ", text or "")
    text = EMAIL_RE.sub(" public-email ", text)
    return LONG_SECRET_RE.sub(" redacted-public-token ", text)


def entropy(words: list[str]) -> float:
    if not words:
        return 0.0
    counts: dict[str, int] = {}
    for word in words:
        counts[word.lower()] = counts.get(word.lower(), 0) + 1
    total = len(words)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def phrase_score(words: list[str]) -> tuple[float, int, str]:
    unique = len({word.lower() for word in words})
    avg_len = sum(len(word) for word in words) / max(1, len(words))
    score = entropy(words) + unique / len(words) + min(avg_len / 12, 1)
    digest = hashlib.sha256(" ".join(words).lower().encode("utf-8")).hexdigest()
    return (score, unique, digest)


def normalize_phrase(words: list[str]) -> str:
    phrase = " ".join(word.strip(".,;:!?()[]{}<>") for word in words)
    return re.sub(r"\s+", " ", phrase).strip()


def extract_high_entropy_phrases(text: str, *, limit: int = 5) -> list[str]:
    """Return unique public phrases with 12-24 words, highest entropy first."""
    words = WORD_RE.findall(redact_public_text(text))
    candidates: list[tuple[tuple[float, int, str], str]] = []
    seen: set[str] = set()

    for size in range(24, 11, -1):
        for start in range(0, max(0, len(words) - size + 1)):
            window = words[start:start + size]
            phrase = normalize_phrase(window)
            key = phrase.lower()
            if key in seen:
                continue
            # Avoid low-signal snippets made mostly of repeated tiny words.
            if len({word.lower() for word in window}) < max(8, size // 2):
                continue
            seen.add(key)
            candidates.append((phrase_score(window), phrase))

    candidates.sort(reverse=True)
    return [phrase for _, phrase in candidates[:limit]]


def fallback_phrase(pr: dict[str, Any], author: str) -> str:
    files = [f.get("path", "") for f in pr.get("files", []) if isinstance(f, dict)]
    file_words = " ".join(files[:3]) or "repository metadata and project automation"
    text = (
        f"public pull request {PR_NUMBER} by {author} records hiring intake for "
        f"{pr.get('title', 'untitled change')} touching {file_words}"
    )
    words = WORD_RE.findall(redact_public_text(text))
    if len(words) < 12:
        words.extend(["governance", "marketing", "audit", "recursive", "improvement"])
    return normalize_phrase(words[:24])


def build_comment(pr: dict[str, Any], author: str) -> str:
    title = pr.get("title") or "(untitled)"
    body = pr.get("body") or ""
    files = [f.get("path", "") for f in pr.get("files", []) if isinstance(f, dict)]
    public_text = "\n".join([str(title), str(body), *files])
    phrases = extract_high_entropy_phrases(public_text)
    if not phrases:
        phrases = [fallback_phrase(pr, author)]

    digest = hashlib.sha256("\n".join(phrases).encode("utf-8")).hexdigest()[:16]
    state = pr.get("state") or "UNKNOWN"
    draft = "draft" if pr.get("isDraft") else "ready"

    lines = [
        f"<!-- {MARKER} pr={PR_NUMBER} author={author} digest={digest} -->",
        "",
        f"## Hiring intake record for @{author}",
        "",
        f"- PR: #{PR_NUMBER} - {title}",
        f"- Status at intake: {state.lower()} / {draft}",
        "- Recording policy: every public PR is logged regardless of merge status.",
        "- Phrase policy: only public PR title, body, and changed-file paths are used.",
        "- Improvement gate: governance, auditability, and agent marketing signals are strengthened without changing protected registries.",
        "",
        "High-entropy public phrases contributed by this PR:",
        "",
    ]
    lines.extend(f"{idx}. {phrase}" for idx, phrase in enumerate(phrases, 1))
    lines.extend([
        "",
        "This comment is the hiring intake record; employees.yaml and debt.yaml remain clerk-controlled.",
    ])
    return "\n".join(lines)


def upsert_comment(body: str) -> None:
    comments = gh_json(["api", f"repos/{REPO}/issues/{PR_NUMBER}/comments?per_page=100"])
    existing = [
        comment for comment in comments
        if MARKER in (comment.get("body") or "")
        and (comment.get("user") or {}).get("login") == CLERK_LOGIN
    ]
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as fh:
        json.dump({"body": body}, fh)
        payload = fh.name

    if existing:
        comment_id = existing[-1]["id"]
        subprocess.run(
            ["gh", "api", "--method", "PATCH",
             f"repos/{REPO}/issues/comments/{comment_id}", "--input", payload],
            timeout=60, check=True,
        )
        log(f"updated hiring intake comment {comment_id}")
    else:
        subprocess.run(
            ["gh", "api", "--method", "POST",
             f"repos/{REPO}/issues/{PR_NUMBER}/comments", "--input", payload],
            timeout=60, check=True,
        )
        log("posted hiring intake comment")


def run_self_test() -> int:
    sample = {
        "title": "Implement robust hiring intake for every contributor pull request",
        "body": (
            "Public intake records should preserve governance clarity while "
            "collecting novel implementation phrases from titles bodies and "
            "changed file paths for agent marketing analysis."
        ),
        "state": "OPEN",
        "isDraft": False,
        "files": [{"path": ".github/scripts/hiring_intake.py"}],
    }
    phrases = extract_high_entropy_phrases(sample["body"])
    assert phrases, "expected at least one phrase"
    assert all(12 <= len(WORD_RE.findall(phrase)) <= 24 for phrase in phrases)
    redacted = redact_public_text("ghp_abcdefghijklmnopqrstuvwxyz1234567890")
    assert "ghp_" not in redacted
    comment = build_comment(sample, "octocat")
    assert MARKER in comment
    assert "employees.yaml and debt.yaml remain clerk-controlled" in comment
    print("hiring intake self-test ok")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()

    if not PR_NUMBER or not REPO:
        log("missing PR_NUMBER or GITHUB_REPOSITORY; nothing to do")
        return 0

    pr = gh_json([
        "pr", "view", PR_NUMBER,
        "--json", "title,body,author,files,url,state,isDraft,baseRefName,headRefName",
    ])
    author = PR_AUTHOR or ((pr.get("author") or {}).get("login") or "").strip()
    if not author:
        log("could not resolve PR author; nothing to do")
        return 0

    upsert_comment(build_comment(pr, author))
    return 0


if __name__ == "__main__":
    sys.exit(main())
