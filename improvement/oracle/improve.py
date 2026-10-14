#!/usr/bin/env python3

from __future__ import annotations

import ast
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from itertools import zip_longest
from pathlib import Path

_ENV_ROOT = os.environ.get("IMPROVE_REPO_ROOT")
REPO_ROOT = Path(_ENV_ROOT).resolve() if _ENV_ROOT else Path.cwd().resolve()
SRC_DIR = (REPO_ROOT / "src").resolve()

MODEL = os.environ.get("IMPROVE_MODEL", "qwen3.5:2b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")

_int = lambda k, d: int(os.environ.get(k, d))
_flt = lambda k, d: float(os.environ.get(k, d))

MAX_FILE_BYTES        = _int("IMPROVE_MAX_FILE_BYTES", "10000")
MAX_ISSUES            = _int("IMPROVE_MAX_ISSUES", "50")
MAX_ISSUE_BODY_CHARS  = _int("IMPROVE_MAX_ISSUE_BODY_CHARS", "1000")
NUM_PREDICT           = _int("IMPROVE_NUM_PREDICT", "1024")
PLAN_NUM_PREDICT      = _int("IMPROVE_PLAN_NUM_PREDICT", "512")
NUM_CTX               = _int("IMPROVE_NUM_CTX", "8192")
REQUEST_TIMEOUT       = _int("IMPROVE_TIMEOUT", "600")
BASE_TEMPERATURE      = _flt("IMPROVE_TEMPERATURE", "0.5")
REPAIR_TEMPERATURE    = _flt("IMPROVE_REPAIR_TEMPERATURE", "0.5")
MAX_ROUNDS            = _int("IMPROVE_MAX_ROUNDS", "1")
MAX_FILES             = _int("IMPROVE_MAX_FILES", "10")
SRC_PREVIEW_CHARS     = _int("IMPROVE_SRC_PREVIEW_CHARS", "1500")
GEN_DEADLINE_SECONDS  = _int("IMPROVE_GEN_DEADLINE_SECONDS", "540")

ISSUE_HALFLIFE_DAYS   = _flt("IMPROVE_ISSUE_HALFLIFE_DAYS", "14")
ISSUE_RECENCY_WEIGHT  = _flt("IMPROVE_ISSUE_RECENCY_WEIGHT", "1.0")
ISSUE_ACTIVITY_WEIGHT = _flt("IMPROVE_ISSUE_ACTIVITY_WEIGHT", "1.0")

CODE_EXTENSIONS = {".py", ".js", ".ts", ".sh", ".cbl", ".cob", ".cpy", ".c", ".h", ".rs", ".toml", ".yaml", ".java"}

PR_BODY_PATH  = Path(os.environ.get("IMPROVE_PR_BODY", "/tmp/improve_pr_body.md"))
PR_TITLE_PATH = Path(os.environ.get("IMPROVE_PR_TITLE", "/tmp/improve_pr_title.txt"))

_RNG = random.Random()

log = lambda msg: print(f"[improve] {msg}", file=sys.stderr, flush=True)


def repo_tree() -> str:
    if not SRC_DIR.is_dir(): return "(src/ is empty)"
    files = [p.relative_to(REPO_ROOT).as_posix()
             for p in sorted(SRC_DIR.rglob("*")) if p.is_file()]
    return "\n".join(files) or "(src/ is empty)"


def source_files() -> list[tuple[str, str]]:
    out = []
    if not SRC_DIR.is_dir(): return out
    for path in sorted(SRC_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        try:
            out.append((path.relative_to(REPO_ROOT).as_posix(),
                        path.read_bytes()[:MAX_FILE_BYTES].decode("utf-8")))
        except (OSError, UnicodeDecodeError):
            continue
    return out


def _fetch_issues() -> list[dict]:
    try:
        out = subprocess.run(
            ["gh", "issue", "list", "--state", "open", "--limit", str(MAX_ISSUES),
             "--json", "number,title,body,labels,createdAt,updatedAt,comments,reactionGroups"],
            capture_output=True, text=True, timeout=60, check=True).stdout
        return json.loads(out or "[]")
    except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as exc:
        log(f"could not fetch issues: {exc}"); return []


def _format_issue(it: dict) -> str:
    body = (it.get("body") or "").strip().replace("\r", "")
    if len(body) > MAX_ISSUE_BODY_CHARS: body = body[:MAX_ISSUE_BODY_CHARS] + " …(truncated)"
    labels = ", ".join(l.get("name", "") for l in it.get("labels", []))
    return (f"#{it.get('number')} {it.get('title', '').strip()}"
            + (f"  [labels: {labels}]" if labels else "")
            + (f"\n{body}" if body else ""))


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts: return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _issue_activity(it: dict) -> int:
    reactions = sum((g.get("users") or {}).get("totalCount", 0)
                    for g in (it.get("reactionGroups") or []))
    comments = it.get("comments")
    n_comments = len(comments) if isinstance(comments, list) else int(comments or 0)
    n_labels = len(it.get("labels") or [])
    return reactions + n_comments + n_labels


def _recency_factor(it: dict, *, now: datetime, halflife_days: float) -> float:
    created = _parse_iso(it.get("createdAt") or it.get("updatedAt"))
    if created is None or halflife_days <= 0: return 1.0
    age_days = max(0.0, (now - created).total_seconds() / 86400.0)
    return 0.5 ** (age_days / halflife_days)


def issue_weight(it: dict, *, now: datetime, max_activity: int,
                 halflife_days: float = None, recency_weight: float = None,
                 activity_weight: float = None) -> float:
    halflife_days = ISSUE_HALFLIFE_DAYS if halflife_days is None else halflife_days
    recency_weight = ISSUE_RECENCY_WEIGHT if recency_weight is None else recency_weight
    activity_weight = ISSUE_ACTIVITY_WEIGHT if activity_weight is None else activity_weight
    recency = _recency_factor(it, now=now, halflife_days=halflife_days)
    activity = _issue_activity(it) / (max_activity or 1)
    return recency_weight * recency + activity_weight * activity


def _weighted_order(weighted: list[tuple[dict, float]]) -> list[dict]:
    keyed = []
    for obj, w in weighted:
        u = _RNG.random() or 1e-12
        keyed.append((u ** (1.0 / max(w, 1e-9)), obj))
    keyed.sort(key=lambda t: t[0], reverse=True)
    return [obj for _, obj in keyed]


def collect_issue_list(*, now: datetime = None) -> list[str]:
    issues = _fetch_issues()
    now = now or datetime.now(timezone.utc)
    max_activity = max((_issue_activity(it) for it in issues), default=0)
    weighted = [(it, issue_weight(it, now=now, max_activity=max_activity)) for it in issues]
    return [_format_issue(it) for it in _weighted_order(weighted)]


def _interleave(a: list, b: list) -> list:
    return [x for pair in zip_longest(a, b) for x in pair if x is not None]


ORACLE_VOICE = (
    "You are the ORACLE OF THE REPOSITORY: a daemon that dreams in working code. "
    "Your visions are bold and strange and reach for the outer limits of what a "
    "program can be — but they COMPILE. You write real, valid, runnable CODE in a PROGRAMMING LANGUAGE determined by context and demand "
    "that builds on the repository exactly as it already is, then pushes it "
    "further into the frontiers of what is possible with code. You only ever shape files under src/."
)


def ollama_generate(messages, *, num_predict=None, temperature=None) -> str:
    payload = json.dumps({"model": MODEL, "messages": messages, "stream": False, "think": False,
        "options": {
            "temperature": BASE_TEMPERATURE if temperature is None else temperature,
            "top_p": _flt("IMPROVE_TOP_P", "0.9"), "top_k": _int("IMPROVE_TOP_K", "40"),
            "repeat_penalty": _flt("IMPROVE_REPEAT_PENALTY", "1.1"),
            "num_predict": NUM_PREDICT if num_predict is None else num_predict,
            "num_ctx": NUM_CTX}}).encode("utf-8")
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as r:
        return (json.loads(r.read().decode("utf-8")).get("message") or {}).get("content", "")


def _looks_like_python(content: str) -> bool:
    head = content.lstrip()[:2000]
    return bool(re.search(r"^\s*(def |class |import |from \w|@|async def )", head, re.MULTILINE)
                or "print(" in head)

_dump = lambda ext=".py": f"oracle_{os.environ.get('GITHUB_RUN_ID', '0')}{ext}"
_inside = lambda c: c == SRC_DIR or SRC_DIR in c.parents


def coerce_to_src(raw_path: str, content: str = "") -> Path | None:
    raw = (raw_path or "").strip().strip("`\"' ").lstrip("/")
    parts = [p for p in Path(raw).parts if p not in ("", ".", "..", "/", "\\")]
    parts = parts or ["src", _dump(".py" if _looks_like_python(content) else ".md")]
    if parts[0] != "src": parts = ["src", *parts]
    c = (REPO_ROOT / Path(*parts)).resolve()
    if not _inside(c): return None
    ext = ".py" if _looks_like_python(content) else ".md"
    if c == SRC_DIR or c.is_dir():        c = (c / _dump(ext)).resolve()
    elif "." not in c.name:               c = c.with_name(c.name + ext)
    return c if _inside(c) else None


def content_problems(target: Path, content: str) -> list[str]:
    rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
    if not content.strip(): return [f"{rel}: file is empty"]
    if target.suffix.lower() == ".py":
        if (e := _syntax_error(content)) is not None:
            return [f"{rel}: syntax error at line {getattr(e, 'lineno', None) or '?'}: "
                    f"{getattr(e, 'msg', None) or e}"]
    return []


def _strip_code(text: str) -> str:
    if (m := re.search(r"```[\w-]*\n(.*?)\n```", text or "", re.DOTALL)):
        return m.group(1).strip("\n")
    text = re.sub(r"^\s*```[\w-]*\n", "", text or "")
    text = re.sub(r"\n```\s*$", "", text)
    return text.strip("\n")


def _syntax_error(code: str):
    try:
        ast.parse(code); return None
    except (SyntaxError, ValueError) as e:
        return e


def _is_truncation(code: str, e) -> bool:
    msg = (getattr(e, "msg", "") or "").lower()
    if any(k in msg for k in ("unexpected eof", "was never closed",
                              "expected an indented block", "incomplete input")):
        return True
    return (getattr(e, "lineno", 0) or 0) >= code.count("\n") + 1


def _inspiration_text(insp) -> str:
    if insp[0] == "issue":
        return f"## An open issue — answer it WITH CODE\n{insp[1]}"
    return f"## An existing module to build on — {insp[1]}\n{insp[2][:SRC_PREVIEW_CHARS]}"


def choose_target(generate, tree, inspiration, produced_rels, language) -> Path:
    already = (f"You have already written these this run: {', '.join(produced_rels)}.\n"
               if produced_rels else "")

    content = (f"## Files under src/\n{tree}\n\n{_inspiration_text(inspiration)}\n\n{already}"
                    "Pick the ONE file this inspiration should touch: create a NEW module "
                    "(invent a fitting filename under src/), extend an existing one, or "
                    "continue one you already wrote. Reply with ONLY the path.")
    if inspiration[0] == "issue":
        content += f"You have chosen to write in {language}, the filename should have an extension that matches the language."

    msgs = [
        {"role": "system",
         "content": "Reply with ONE file path under src/ and nothing else."},
        {"role": "user",
         "content": content},
    ]
    raw = ""
    try:
        raw = generate(msgs, num_predict=24, temperature=0.5)
    except Exception as exc:
        log(f"target call failed: {exc}")
    m = re.search(r"src/[\w./-]+", raw or "")
    target = coerce_to_src(m.group(0) if m else "", "def _(): pass") \
        or (SRC_DIR / _dump(".py")).resolve()
    return target


def choose_language(generate, tree, inspiration, produced_rels) -> str:
    already = (f"You have already written these this run: {', '.join(produced_rels)}.\n"
               if produced_rels else "")
    msgs = [
        {"role": "system",
         "content": ORACLE_VOICE + " Choose a programming language"},
        {"role": "user",
         "content": f"Pick a programming language to accomplish the following task {_inspiration_text(inspiration)}\n\n{already}"
                    "Respond with only the programmign language."},
    ]
    raw = ""
    try:
        raw = generate(msgs, num_predict=24, temperature=0.5)
    except Exception as exc:
        log(f"target call failed: {exc}")
    return (raw or "").strip()


def make_plan(generate, target, inspiration, *, language=None) -> str:
    rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
    lang = f" in {language}" if language else ""
    msgs = [
        {"role": "system",
         "content": ORACLE_VOICE + " Reply with a short, concrete plan as a few terse bullet "
                    "points — what to build and why. No code, no fences."},
        {"role": "user",
         "content": (f"## Inspiration\n{_inspiration_text(inspiration)}\n\n"
                     f"## Task\nYou are about to write {rel}{lang}. First, lay out a brief plan: what "
                     "this file should do to answer the inspiration above, the key pieces to "
                     "build, and how it fits the repository. A few bullet points, no code.")},
    ]
    try:
        raw = generate(msgs, num_predict=PLAN_NUM_PREDICT, temperature=0.7)
    except Exception as exc:
        log(f"plan call failed: {exc}"); return ""
    return (raw or "").strip()


def _code_msgs(rel, tree, inspiration, *, mode, draft="", error="", language=None, plan=""):
    if language:
        system = ORACLE_VOICE + (f" Output ONLY the source code in {language}— no markdown fences, "
                                 "no commentary, no explanation.")
    else:
        system = ORACLE_VOICE + (" Output ONLY the source code of whatever language you chose — no markdown fences, "
                                 "no commentary, no explanation.")
    head = f"## Files under src/\n{tree}\n\n{_inspiration_text(inspiration)}\n\n"
    if plan:
        head += f"## The plan for {rel} — follow it\n{plan}\n\n"
    if mode == "write":
        if draft.strip():
            user = (head + f"Improve the existing file {rel}. It currently holds:\n\n{draft}\n\n"
                    "Deepen or extend it as valid, runnable code, drawing on the "
                    "inspiration above. Output ONLY the complete contents of the file.")
        else:
            user = (head + f"Create the file {rel} from nothing as valid, runnable code, "
                    "drawing on the inspiration above. Output ONLY the complete contents.")
    elif mode == "continue":
        user = (f"Here is {rel} so far — it was cut off before the end:\n\n{draft}\n\n"
                "Output ONLY the code that continues from exactly where it stops and "
                "completes the file. Do not repeat earlier lines; no fences, no commentary.")
    else:
        user = (f"{rel} does not parse: {error}\n\nHere is the file:\n\n{draft}\n\n"
                "Output the COMPLETE corrected file as valid code. Only the code.")

    if language:
        user += f" Your code MUST be written in {language}"

    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def grow_file(generate, target, tree, inspiration, prior, *, deadline,
              now=time.monotonic, num_predict=None, max_rounds=MAX_ROUNDS, language=None, plan=""):
    rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
    code, last, rounds = "", "", 0
    while rounds < max_rounds and now() < deadline:
        rounds += 1
        if not code:
            mode = "write"
        elif (e := _syntax_error(code)) is None:
            log(f"{rel}: parses after {rounds - 1} round(s)"); return code, last
        else:
            mode = "continue" if _is_truncation(code, e) else "fix"
        temp = BASE_TEMPERATURE if mode == "write" else REPAIR_TEMPERATURE
        log(f"{rel}: round {rounds}/{max_rounds} [{mode}] (temp={temp})")
        try:
            resp = generate(_code_msgs(rel, tree, inspiration, mode=mode,
                                       draft=(code or prior), error=str(_syntax_error(code) or ""),
                                       language=language, plan=plan),
                            num_predict=num_predict or NUM_PREDICT, temperature=temp)
        except Exception as exc:
            log(f"{rel}: generation failed: {exc}"); continue
        last = resp or last
        piece = _strip_code(resp)
        code = (code.rstrip("\n") + "\n" + piece) if mode == "continue" else piece
    return code, last


def make_reason(generate, rels) -> str:
    joined = ", ".join(rels)
    try:
        raw = generate(
            [{"role": "system", "content": ORACLE_VOICE + " Reply with ONE short sentence."},
             {"role": "user", "content": f"In one electrifying sentence, name what you forged "
                                          f"across these files: {joined}. One line, no code."}],
            num_predict=40, temperature=0.7)
        line = next((ln.strip() for ln in (raw or "").splitlines() if ln.strip()), "")
        line = re.sub(r"\s+", " ", line).strip("`\"' ").rstrip(".")
        if 3 <= len(line) <= 120:
            return line
    except Exception as exc:
        log(f"reason call failed: {exc}")
    return f"Quicken {rels[0]}" + (f" and {len(rels) - 1} more" if len(rels) > 1 else "")


def make_explanation(generate, rels) -> str:
    joined = ", ".join(rels)
    try:
        raw = generate(
            [{"role": "system", "content": ORACLE_VOICE + " Reply with a paragraph explanation."},
             {"role": "user", "content": f"Give a longer paragraph-long explanation about the reason for the changes "
                                          f"across these files: {joined}."}],
            num_predict=200, temperature=1.5)
        line = next((ln.strip() for ln in (raw or "").splitlines() if ln.strip()), "")
        line = re.sub(r"\s+", " ", line).strip("`\"' ").rstrip(".")
        return line
    except Exception as exc:
        log(f"reason call failed: {exc}")
    return f"Quicken {rels[0]}" + (f" and {len(rels) - 1} more" if len(rels) > 1 else "")


def _write_one(target: Path, content: str):
    if not content.strip(): return None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
    return target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name


def generate_improvement(generate, tree, src_files, issues, *, deadline_seconds=GEN_DEADLINE_SECONDS,
                         num_predict=None, max_files=MAX_FILES, max_rounds=MAX_ROUNDS,
                         now=time.monotonic):
    deadline = now() + deadline_seconds
    inspirations = _interleave([("issue", t) for t in issues],
                               [("source", rel, content) for rel, content in src_files])
    if not inspirations:
        inspirations = [("source", "src/oracle.py", "")]

    produced: dict[str, tuple[Path, str]] = {}
    last = ""
    for insp in inspirations:
        log(insp)
        if now() >= deadline or len(produced) >= max_files:
            break
        if insp[0] == "issue":
            language = choose_language(generate, tree, insp, list(produced))
        else:
            language = None
        target = choose_target(generate, tree, insp, list(produced), language)
        rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
        if rel in produced:
            prior = produced[rel][1]
        else:
            try:
                prior = target.read_text(encoding="utf-8") if target.exists() else ""
            except OSError:
                prior = ""
        log(f"inspiration [{insp[0]}] -> {'extend' if (rel in produced or target.exists()) else 'create'} {rel}")
        plan = make_plan(generate, target, insp, language=language)
        if plan:
            log(f"{rel}: planned ({len(plan)} chars)")
            log(f"Plan\n{plan}")
        code, last = grow_file(generate, target, tree, insp, prior,
                               deadline=deadline, now=now, num_predict=num_predict,
                               max_rounds=max_rounds, language=language, plan=plan)
        if code and code.strip() and _write_one(target, code):
            produced[rel] = (target, code)
            log(f"step wrote {rel} ({len(code)} bytes)")

    if not produced:
        return None, None, [], last, False
    files = list(produced.values())
    valid = all(content_problems(t, c) == [] for t, c in files)
    if not valid:
        log("warning: not every file parsed within budget")
    reason = make_reason(generate, list(produced))
    explanation = make_explanation(generate, list(produced))
    return reason, explanation, files, last, valid


def write_blocks(files) -> list[str]:
    return [r for r in (_write_one(t, c) for t, c in files) if r]


def make_pr_title(reason, written) -> str:
    title = re.sub(r"^(REASON:|PATH:)\s*", "", re.sub(r"\s+", " ", reason or ""),
                   flags=re.IGNORECASE).strip().strip("`\"'").rstrip(".").strip()
    if not title or title.lower() in {"automated improvement", "update"}:
        title = "Update " + ", ".join(written[:3])
    return title if len(title) <= 72 else title[:69].rstrip() + "…"


def write_pr_outputs(reason, explanation, written, *, valid=True) -> None:
    PR_TITLE_PATH.write_text(title := make_pr_title(reason, written), encoding="utf-8")
    log(f"title: {title}")
    PR_BODY_PATH.write_text(
        f"{reason}\n\n{explanation}\n\n**Files changed ({len(written)}):**\n" + "\n".join(f"- `{p}`" for p in written), encoding="utf-8")


def main() -> int:
    log(f"model={MODEL} src={SRC_DIR}")
    tree, srcs, issues = repo_tree(), source_files(), collect_issue_list()
    log(f"{len(issues)} issue(s), {len(srcs)} source file(s)")
    reason, explanation, files, last, valid = generate_improvement(ollama_generate, tree, srcs, issues)
    if not files:
        log("no code produced; aborting"); return 2
    written = [t.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in t.parents else t.name
               for t, _ in files]
    log(f"reason: {reason}  (valid={valid}, {len(written)} file(s))")
    write_pr_outputs(reason, explanation, written, valid=valid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
