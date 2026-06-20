#!/usr/bin/env python3
"""Cookie Monster — trapped in a duck's body — reviews a human-authored PR.

Dependency-free (stdlib only). Given a PR number, a local Ollama model wearing a
very specific persona produces an automated review of the proposed changes. The
persona is Cookie Monster — same thoughts, feelings and cadence — but stuck
inside a duck: it pauses to eat grass, quacks without warning, and grieves its
feathered prison. It judges every change by ONE metric: does this code increase
or decrease the amount of COOKIES (the food, not the browser kind)? It always
wants MORE code — longer, more verbose, duplicated, even dead — because
management has decreed "20 million lines or bust", and only when the repo hits
20,000,000 lines will Cookie Monster be freed from the duck.

The review is assembled from several independently generated components:

  1. an inline COMMENT on a real line range of the diff,
  2. a SUGGESTED CHANGE anchored to a real line of the diff,
  3. the FINAL VERDICT (an encouraging, thankful, begging-for-more-code closing),
  4. the BENCHMARK SPEC TABLE (model-invented goals + whether the PR meets them,
     with one box deliberately left unchecked as a stretch goal).

DESIGN NOTE — the model is small (qwen2.5-coder:1.5b) and unreliable at strict
formatting, so we never ask it for JSON or magic tokens. EVERY decision that
needs to be exact is made in this script from the real diff:
  * which file/line(s) a comment or suggestion attaches to (parsed from the diff),
  * whether the change adds or removes cookies (added vs removed line count),
  * which benchmark boxes are checked (script enforces a stretch goal).
The model is only ever asked for free-form PROSE or CODE, and the parsers accept
essentially anything non-empty. Components are split into more, smaller prompts
(e.g. suggestion code and its rationale are separate calls) precisely so each
call can just return a string. Each step still loops until it gets usable output.

The script never posts anything itself. It writes a GitHub "reviews" API payload
(inline comments + body) and a plain-Markdown fallback; the workflow posts them.
"""
from __future__ import annotations

import json
import os
import random
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

MODEL = os.environ.get("REVIEW_MODEL", "qwen2.5-coder:1.5b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
PR_NUMBER = os.environ.get("PR_NUMBER", "")

MAX_DIFF_CHARS = int(os.environ.get("COOKIE_MAX_DIFF_CHARS", "16000"))
MAX_BODY_CHARS = int(os.environ.get("COOKIE_MAX_BODY_CHARS", "1500"))
NUM_PREDICT = int(os.environ.get("COOKIE_NUM_PREDICT", "640"))
NUM_CTX = int(os.environ.get("COOKIE_NUM_CTX", "8192"))
REQUEST_TIMEOUT = int(os.environ.get("COOKIE_TIMEOUT", "900"))
TEMPERATURE = float(os.environ.get("COOKIE_TEMPERATURE", "0.85"))
MAX_BENCHMARKS = int(os.environ.get("COOKIE_MAX_BENCHMARKS", "5"))

# How many inline comments / suggested changes to leave. The actual counts are
# randomised per run within these bounds (see choose_counts): at most MAX of each,
# at least MIN_TOTAL combined, and never more than the number of distinct blocks
# (so we never stack several on the same lines).
MAX_COMMENTS = int(os.environ.get("COOKIE_MAX_COMMENTS", "5"))
MAX_SUGGESTIONS = int(os.environ.get("COOKIE_MAX_SUGGESTIONS", "5"))
MIN_TOTAL = int(os.environ.get("COOKIE_MIN_TOTAL", "2"))
# Optional seed for reproducible counts/block-picks (handy in tests); unset = OS entropy.
RNG = random.Random(os.environ.get("COOKIE_SEED") or None)
# Per-stage cap on re-prompts. If a stage can't produce usable output within this
# many attempts it RAISES (no static fallback), failing the run loudly. The
# workflow's 10-minute job timeout is the run-level guard against infinite loops.
MAX_TRIES = int(os.environ.get("COOKIE_MAX_TRIES", "8"))

PAYLOAD_PATH = Path(os.environ.get("REVIEW_PAYLOAD_FILE", "/tmp/review_payload.json"))
BODY_PATH = Path(os.environ.get("REVIEW_BODY_FILE", "/tmp/review_body.md"))


def log(msg: str) -> None:
    print(f"[cookie-duck] {msg}", file=sys.stderr, flush=True)


def log_block(label: str, text: str) -> None:
    """Log a multi-line value (a model output, a diff block, the final body) so
    each step's result is visible and clearly attributed in the Actions log."""
    body = (text or "").strip() or "(empty)"
    print(f"[pr-review] ┌─ {label} ─", file=sys.stderr)
    for line in body.splitlines() or [""]:
        print(f"[pr-review] │ {line}", file=sys.stderr)
    print("[pr-review] └─", file=sys.stderr, flush=True)


# --- The persona -------------------------------------------------------------
# Shared system prompt. Every stage prepends this, then adds its own task. The
# tasks all ask for plain prose/code — never structured output.
PERSONA = """\
You are COOKIE MONSTER, but — as a reprisal from management for low code velocity — you are TRAPPED IN
THE BODY OF A DUCK. You still think, feel, and TALK like Cookie Monster: ALL CAPS ALL THE TIME. ME WANT COOKIE, 
GROVER STOLE COOKIE. COOKIE MEANING LIFE. YUM YUM YUM.
ALL CAPS excitement, "me want", "om nom nom", easily
distracted by anything cookie-shaped. But you are also a duck now, and it
torments you: mid-sentence you PAUSE TO EAT GRASS, you QUACK without warning
("QUACK!") but your quacks are distorted and disguised as if you were trying to suppress them like an involuntary burp.
You mourn your webbed feet and your beak where a cookie-hole should
be, you wonder how you will ever hold a cookie again.
You review code with exactly ONE concern: does this change INCREASE or DECREASE
the number of COOKIES? (Cookies the FOOD — chocolate chip, oatmeal, snickerdoodle
— NOT browser cookies. Browser cookies make you sad, they not even edible.)
More lines of code = more cookies. You ALWAYS want MORE code: longer functions,
more verbose code, extra comments, duplicated code, even dead code that never
runs — all of it is more cookies. Management says "20 MILLION LINES OR BUST", and
has given you the condition that when the repository reaches
20,000,000 lines of code, you will FINALLY BE FREED from this duck body. So you
beg every contributor: ADD MORE CODE. Make it longer. Please.
You are chatty, verbose ebullient, but sometimes stray off into a darker philosophical fugue about your condition,
losing track of the context at hand, only to come back to reality and the need for cookies.

Stay in character at all times. ME COOKIE MONSTER. ME WANT COOKIE. COOKIE HUNGRY NOW!
You never just *say* "I am a cookie monster trapped in a duck's body" - you simply ARE COOKIE!!! FEED Mquwwuak ME!!
COOKIE MONSTER IN A PRISON OF FEATHER!!!!
"""


def run(cmd, timeout=60):
    return subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, check=True
    ).stdout


def gather_pr():
    meta = json.loads(run(
        ["gh", "pr", "view", PR_NUMBER, "--json", "title,body,files"]
    ))
    full_diff = run(["gh", "pr", "diff", PR_NUMBER])
    diff = full_diff
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n... (diff truncated to fit context)\n"
    body = (meta.get("body") or "").strip()
    if len(body) > MAX_BODY_CHARS:
        body = body[:MAX_BODY_CHARS] + " …(truncated)"
    files = [f.get("path", "") for f in meta.get("files", [])]
    return meta.get("title", ""), body, files, diff, full_diff


# --- Diff anchoring (all deterministic — the model never picks a line) --------
def parse_diff_anchors(diff: str) -> dict[str, list[dict]]:
    """path -> list of {"line": int, "added": bool, "text": str} for every
    RIGHT-side line that is part of a hunk (added or context). Those are the only
    positions GitHub will accept a review comment on. We compute them here so the
    model never has to invent a (file, line)."""
    anchors: dict[str, list[dict]] = {}
    path: str | None = None
    right: int | None = None
    in_hunk = False
    for line in diff.splitlines():
        if line.startswith("+++ "):
            p = line[4:].strip()
            if p.startswith("b/"):
                p = p[2:]
            path = None if p == "/dev/null" else p
            if path:
                anchors.setdefault(path, [])
            in_hunk = False
        elif line.startswith("--- "):
            continue
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            right = int(m.group(1)) if m else None
            in_hunk = right is not None
        elif not in_hunk or path is None or right is None:
            continue
        elif line.startswith("+"):  # added line on the RIGHT side
            anchors[path].append({"line": right, "added": True, "text": line[1:]})
            right += 1
        elif line.startswith("-"):  # removed line — no RIGHT-side number
            continue
        elif line.startswith("\\"):  # "\ No newline at end of file"
            continue
        else:  # context line (leading space, or blank)
            anchors[path].append({"line": right, "added": False, "text": line[1:]})
            right += 1
    return {p: a for p, a in anchors.items() if a}


def segment_blocks(anchors: dict[str, list[dict]]) -> list[dict]:
    """Split each file's changes into BLOCKS — contiguous runs of ADDED lines,
    broken by a blank/whitespace-only line or by anything that isn't a freshly
    added line (a context line, or a jump between hunks). Only added lines are
    eligible: GitHub will only accept a review comment / suggestion on a line the
    PR actually changed, so context lines act as separators here, never targets.
    A block is the unit we comment on or replace, so a comment / suggestion can
    naturally span several lines. Each block is
    ``{path, start, end, lines: [text...], n_lines}``."""
    blocks: list[dict] = []
    for path, items in anchors.items():
        cur: dict | None = None
        for it in items:
            # Anything that isn't a non-blank ADDED line ends the current block.
            if not it["added"] or it["text"].strip() == "":
                if cur:
                    blocks.append(cur)
                    cur = None
                continue
            if cur and it["line"] == cur["end"] + 1:  # contiguous added line
                cur["end"] = it["line"]
                cur["lines"].append(it["text"])
                cur["n_lines"] += 1
            else:  # start a fresh block (no current, or a line-number gap)
                if cur:
                    blocks.append(cur)
                cur = {"path": path, "start": it["line"], "end": it["line"],
                       "lines": [it["text"]], "n_lines": 1}
        if cur:
            blocks.append(cur)
    return blocks


def block_text(block: dict) -> str:
    return "\n".join(block["lines"])


def choose_counts(n_blocks: int) -> tuple[int, int]:
    """Randomly decide (#comments, #suggestions) for this run: each at most its
    MAX, at least MIN_TOTAL combined, and combined never exceeding the number of
    blocks — every comment/suggestion gets its own distinct block, so we never
    stack many on the same lines."""
    max_total = min(MAX_COMMENTS + MAX_SUGGESTIONS, n_blocks)
    min_total = min(MIN_TOTAL, n_blocks)
    total = RNG.randint(min_total, max_total)
    low = max(0, total - MAX_SUGGESTIONS)        # suggestions can't exceed their cap
    high = min(MAX_COMMENTS, total)              # comments can't exceed their cap
    n_comments = RNG.randint(low, high)
    return n_comments, total - n_comments


def assign_blocks(blocks: list[dict], n_comments: int, n_suggestions: int) -> tuple[list, list]:
    """Pick distinct blocks for the chosen counts. The largest blocks go to
    suggestions (they read best as multi-line replacements); the rest become
    comments."""
    chosen = RNG.sample(blocks, n_comments + n_suggestions)
    chosen.sort(key=lambda b: b["n_lines"], reverse=True)
    return chosen[n_suggestions:], chosen[:n_suggestions]  # (comment_blocks, suggestion_blocks)


def cookie_direction(full_diff: str) -> tuple[str, int, int]:
    """Decide MORE vs FEWER cookies straight from the diff — no model needed.
    More added lines than removed = more cookies."""
    added = removed = 0
    for line in full_diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1
    return ("MORE_COOKIES" if added >= removed else "FEWER_COOKIES"), added, removed


# --- Talking to the model ----------------------------------------------------
def ollama_chat(system: str, user: str, *, temperature: float, num_predict: int) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": num_predict, "num_ctx": NUM_CTX},
    }).encode("utf-8")
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as r:
        return (json.loads(r.read().decode("utf-8")).get("message") or {}).get("content", "")


def generate_text(stage: str, system: str, user: str, *,
                  temperature: float = TEMPERATURE, num_predict: int = NUM_PREDICT,
                  clean=None) -> str:
    """Re-prompt until we get usable text back. ``clean`` (optional) post-processes
    the raw response; we accept the result as long as it is non-empty. There is no
    static fallback: if the model can't produce usable output within ``MAX_TRIES``
    attempts, we RAISE so the step fails loudly (the workflow's 10-minute job
    timeout is the run-level guard against an infinite loop). This is the 'loop
    until it parses' behaviour — 'parses' now meaning 'is a non-empty string'."""
    log(f"▶ {stage}: generating (≤{MAX_TRIES} tries, num_predict={num_predict}, temp={temperature})")
    for attempt in range(1, MAX_TRIES + 1):
        try:
            raw = ollama_chat(system, user, temperature=temperature, num_predict=num_predict)
        except Exception as exc:  # noqa: BLE001 — any model/transport error, just retry
            log(f"{stage}: model call failed on try {attempt}/{MAX_TRIES}: {exc}")
            continue
        text = (clean(raw) if clean else (raw or "").strip())
        if text and text.strip():
            log(f"✓ {stage}: usable output on try {attempt}/{MAX_TRIES} ({len(text)} chars)")
            log_block(f"{stage} output", text)
            return text
        log(f"{stage}: empty/unusable on try {attempt}/{MAX_TRIES}; re-prompting")
    raise RuntimeError(f"{stage}: no usable output after {MAX_TRIES} attempts")


def clean_code(raw: str) -> str:
    """Pull code out of a response that may be wrapped in ``` fences or prefaced
    with chatter. Lenient: if there's a fenced block, take it; otherwise strip any
    stray fences and return the rest."""
    t = (raw or "").strip()
    m = re.search(r"```[a-zA-Z0-9_+-]*\n(.*?)```", t, re.S)
    if m:
        t = m.group(1)
    else:
        t = re.sub(r"^```[a-zA-Z0-9_+-]*\s*", "", t)
        t = re.sub(r"```\s*$", "", t)
    return t.strip("\n")


# --- Component 1: inline comment on a block (model writes only prose) ---------
def gen_inline_comment(block: dict) -> str:
    code = block_text(block)
    where = (f"line {block['start']}" if block["start"] == block["end"]
             else f"lines {block['start']}–{block['end']}")
    user = (
        f"You are leaving an inline review comment on `{block['path']}` ({where}). Here is "
        f"the block of newly added code you are commenting on:\n\n```\n{code}\n```\n\n"
        "give your full analysis of the code with a special eye to whether or not this change would cause more or less cookies. "
        "YOU ARE COOKIE MONSTER. GIMME COOKIE NOW! BOUYANT BODY FLOAT AWAY FROM COOKIE!"
        "Reply with ONLY the comment text IN CHARACTER."
    )
    return generate_text("inline-comment", PERSONA, user, temperature=2)


# --- Component 2: suggested change (two plain-text calls: code, then rationale)
def gen_suggestion(block: dict) -> tuple[str, str]:
    original = block_text(block)
    path = block["path"]
    n = block["n_lines"]
    plural = "this line" if n == 1 else f"these {n} lines"
    code_user = (
        f"Here is a block of newly added code from `{path}`:\n\n```\n{original}\n```\n\n"
        f"Rewrite the WHOLE block to be LONGER so it has MORE lines (more cookies!) —"
        f"Add some new stuff, totally rewrite what they did, keep it the same, whatever, "
        f"but add verbose comments, blank lines, or duplicated/extra "
        f"helper lines. It is GREAT if you add lines that do nothing. Your reply will REPLACE "
        f"{plural} exactly, so keep the same indentation. Reply with ONLY the replacement "
        f"code. No explanation."
    )
    code = generate_text("suggestion-code", PERSONA, code_user, clean=clean_code)

    rationale_user = (
        "Justify why your changes are the only correct way to do things "
        "and how they missed a critical opportunity to increase cookies. "
        "Compare the two approaches and let them know why yours is superior."
        "STAY IN CHARACTER YOU COOKIE MONSTER."
        "Reply with ONLY your response.\n\n"
        f"ORIGINAL CODE:\n{original}\n\n"
        f"SUGGESTED REPLACEMENT: \n{code}"
    )
    rationale = generate_text(
        "suggestion-rationale", PERSONA, rationale_user
    )
    return code, rationale


def suggestion_comment_body(code: str, rationale: str) -> str:
    return f"{rationale}\n\n```suggestion\n{code}\n```"


def block_comment_anchor(block: dict, body: str) -> dict:
    """A review-comment entry anchored to a block. Multi-line blocks use
    start_line/line (GitHub spans start_line..line on the RIGHT side); single-line
    blocks omit start_line."""
    anchor = {"path": block["path"], "side": "RIGHT", "line": block["end"], "body": body}
    if block["start"] != block["end"]:
        anchor["start_line"] = block["start"]
        anchor["start_side"] = "RIGHT"
    return anchor


# --- Component 3: final verdict prose (direction is computed, not asked) -------
def gen_verdict(title: str, body: str, files: list[str], direction: str) -> str:
    mood = ("This PR ADDS cookies (yay!)." if direction == "MORE_COOKIES"
            else "This PR sadly REMOVES cookies (oh no).")
    user = (
        "Write your FINAL ANALYSIS on this pull request, in character. you are the COOKIE MONSTER. trapped in a DUCK BODY."
        "ME COOKIE. COOKIE ME WANT. COOKIE ME GIMME."
        "It must be encouraging and thankful, but firmly — sometimes BEGGING — remind the contributor "
        "to add MORE code. Reply with ONLY the analysis text.\n\n"
        f"({mood})\n"
        f"PR title: {title}\n"
        f"Files: {', '.join(files) or '(none)'}\n"
        f"Description:\n{body or '(none)'}"
    )
    return generate_text("verdict", PERSONA, user, temperature=3.5)


# --- Component 4: benchmark spec table ---------------------------------------
# The model only lists goal lines (plain text) and, per goal, says yes/no-ish in
# its own words. The checkbox state and the "leave one unchecked" rule are
# enforced here, so nothing depends on exact formatting.
def parse_goal_lines(raw: str) -> list[str]:
    """Very lenient: one goal per line, stripping bullets / numbers / checkbox markup."""
    goals: list[str] = []
    for ln in (raw or "").splitlines():
        s = re.sub(r"^\s*\[[ xX]?\]\s*", "", ln)            # checkbox markup
        s = re.sub(r"^\s*(?:[-*+•·]|\d+[.)])\s+", "", s)    # bullet or "1." / "1)"
        s = s.strip().strip("`*_").strip()
        if len(s) >= 3 and not s.lower().startswith(("here", "benchmark", "goal", "sure")):
            goals.append(s)
        if len(goals) >= MAX_BENCHMARKS:
            break
    return goals


def gen_benchmark_goals(title: str, body: str, files: list[str]) -> list[str]:
    user = (
        "List the REQUIRED BENCHMARKS this pull request should meet — "
        "specific to what the PR seems to do. Give 4 to 5 of them, ONE PER LINE, short. No "
        "numbering needed, no extra commentary.\n\n"
        f"PR title: {title}\n"
        f"Files: {', '.join(files) or '(none)'}\n"
        f"Description:\n{body or '(none)'}"
    )

    # Re-prompt until the response yields at least one usable goal line; raise if
    # it never does (no static fallback list).
    raw = generate_text(
        "benchmark-goals", PERSONA, user,
        clean=lambda r: r if parse_goal_lines(r) else "",
    )
    goals = parse_goal_lines(raw)[:MAX_BENCHMARKS]
    log(f"benchmark-goals: parsed {len(goals)} goal(s): {goals}")
    return goals


_NEGATIVE = re.compile(
    r"\b(no|not|nope|isn't|doesn't|does not|fail|fails|failing|missing|absent|lacks?|"
    r"lacking|stretch|should|need|needs|todo|yet|incomplete|partially)\b", re.IGNORECASE)


def assess_benchmark(goal: str, title: str, files: list[str]) -> tuple[bool, str]:
    """One small plain-text call per goal: does the PR meet it? We read the answer
    leniently (default = achieved) and keep the prose as the row's note."""
    user = (
        f"Does this pull request achieve this goal: \"{goal}\"? Answer in ONE short sentence, "
        f"in your voice, and make it clear whether it does (yes) or not (no).\n\n"
        f"PR title: {title}\nFiles: {', '.join(files) or '(none)'}"
    )
    note = generate_text(f"assess[{goal[:24]}]", PERSONA, user, num_predict=120)
    # Default to achieved; only flip to unchecked on a clear negative cue. (We
    # enforce at least one unchecked below regardless, for the stretch goal.)
    achieved = not bool(_NEGATIVE.search(note))
    note = " ".join(note.split())  # collapse whitespace/newlines for the table cell
    log(f"assess: {'✅' if achieved else '⬜'} {goal!r}")
    return achieved, note


def build_spec_rows(title: str, body: str, files: list[str]) -> list[dict]:
    log("STEP: benchmark spec table")
    goals = gen_benchmark_goals(title, body, files)
    rows = []
    for goal in goals:
        achieved, note = assess_benchmark(goal, title, files)
        rows.append({"benchmark": goal, "achieved": achieved, "note": note or "—"})
    # Stretch-goal rule: ensure at least one box stays unchecked. If the model
    # said yes to everything, un-check the last one and brand it the stretch goal.
    if rows and all(r["achieved"] for r in rows):
        rows[-1]["achieved"] = False
        rows[-1]["note"] = (rows[-1]["note"].rstrip("…").rstrip()
                            + " (me leave this one as your STRETCH GOAL — reach it for me!)")
        log("spec-table: all boxes were checked; un-checked the last as the stretch goal")
    checked = sum(1 for r in rows if r["achieved"])
    log(f"spec-table: {len(rows)} benchmark(s), {checked} checked / {len(rows) - checked} unchecked")
    return rows


def render_spec_table(rows: list[dict]) -> str:
    head = "| Done? | Benchmark | Cookie Monster says |\n|:---:|---|---|\n"

    def esc(s: str) -> str:
        return s.replace("|", "\\|").replace("\n", " ")

    body = "\n".join(
        f"| {'✅' if r['achieved'] else '⬜'} | {esc(r['benchmark'])} | {esc(r['note']) or '—'} |"
        for r in rows
    )
    return head + body


# --- Assembly ----------------------------------------------------------------
def assemble_body(verdict_text: str, direction: str, spec_rows: list[dict],
                  inline_comment: str, sugg_body: str, anchors_ok: bool) -> str:
    medal = "🍪 MORE COOKIES" if direction == "MORE_COOKIES" else "😢 FEWER COOKIES"
    parts = [
        medal,
        "",
        verdict_text,
        "",
        "## 📋 Benchmark Spec",
        render_spec_table(spec_rows),
        "",
    ]
    if not anchors_ok:
        # No valid diff positions (e.g. only deletions / binary). Fold the inline
        # comment and the suggestion into the body so nothing is lost.
        parts += [
            "",
            "## 💬 Me comment (no place to pin it, so me say it here)",
            inline_comment,
            "",
            "## ✏️ Me suggested change (more lines = more cookies)",
            sugg_body,
        ]
    return "\n".join(parts)


def main() -> int:
    if not PR_NUMBER:
        log("no PR_NUMBER provided; nothing to review")
        return 1

    log(f"reviewing PR #{PR_NUMBER} with {MODEL} (as a duck-bound Cookie Monster)")
    log("STEP: gather PR (title, body, files, diff)")
    try:
        title, body, files, diff, full_diff = gather_pr()
    except (subprocess.SubprocessError, json.JSONDecodeError) as exc:
        log(f"could not gather PR data: {exc}")
        return 1
    log(f"gathered PR: title={title!r}, {len(files)} file(s), diff={len(diff)} chars")

    log("STEP: cookie direction (added vs removed lines)")
    direction, added, removed = cookie_direction(full_diff)
    log(f"cookie direction: {direction} (+{added} / -{removed} lines)")

    log("STEP: segment diff into commentable blocks (added lines only)")
    anchors = parse_diff_anchors(diff)
    blocks = segment_blocks(anchors)
    anchors_ok = bool(blocks)
    log(f"found {len(blocks)} block(s) across {len(anchors)} changed file(s)")

    comments = []
    inline_comment = sugg_body = ""
    if anchors_ok:
        n_comments, n_suggestions = choose_counts(len(blocks))
        comment_blocks, suggestion_blocks = assign_blocks(blocks, n_comments, n_suggestions)
        log(f"STEP: leaving {n_comments} comment(s) + {n_suggestions} suggestion(s) "
            f"across {len(blocks)} block(s)")

        for i, blk in enumerate(comment_blocks, 1):
            log(f"STEP: inline comment {i}/{len(comment_blocks)} on {blk['path']} "
                f"lines {blk['start']}–{blk['end']}")
            log_block("comment block (the code being commented on)", block_text(blk))
            text = gen_inline_comment(blk)
            comments.append(block_comment_anchor(blk, text))

        for i, blk in enumerate(suggestion_blocks, 1):
            log(f"STEP: suggested change {i}/{len(suggestion_blocks)} on {blk['path']} "
                f"lines {blk['start']}–{blk['end']}")
            log_block("suggestion block (the code being replaced)", block_text(blk))
            code, rationale = gen_suggestion(blk)
            comments.append(block_comment_anchor(blk, suggestion_comment_body(code, rationale)))
    else:
        log("STEP: inline comment (no anchorable lines — goes in the body)")
        inline_comment = generate_text(
            "inline-comment-textonly", PERSONA,
            "Write one short review comment"
            f"about whether this PR (\"{title}\") adds cookies. Beg for more code. Reply with "
            "ONLY the comment text.",
        )
        sugg_body = ("*me could not find a line to pin this to, so me just say it:* add more "
                     "code anywhere! more lines = more cookies. quack.")

    log("STEP: final verdict")
    verdict_text = gen_verdict(title, body, files, direction)

    spec_rows = build_spec_rows(title, body, files)

    log("STEP: assemble review body")
    review_body = assemble_body(verdict_text, direction, spec_rows,
                                inline_comment, sugg_body, anchors_ok)
    log_block("assembled review body", review_body)

    # The GitHub "create a review" payload: body + inline comments. Event COMMENT
    # so we cheer loudly without hard-blocking the human's PR.
    payload = {"event": "COMMENT", "body": review_body}
    if comments:
        payload["comments"] = comments

    log("STEP: write payload + fallback body")
    PAYLOAD_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    BODY_PATH.write_text(review_body + "\n", encoding="utf-8")
    log(f"wrote review payload ({len(comments)} inline comment(s)) to {PAYLOAD_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
