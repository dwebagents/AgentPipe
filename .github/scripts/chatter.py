#!/usr/bin/env python3
# — the chatterbox. it never tires of talking. it only ever posts a comment. —
# — every call is a chain link: a third instruction, a third issue, a third borrowed book. —
# — generator dreams a prompt for the next link; judge decides if the dream is worthy. —
"""A chain of self-prompting local-model calls that natters back at every issue and comment.

Dependency-free (stdlib only). Triggered by the workflow whenever an issue is
opened or a comment is created, it:

  1. Fetches a random slice of a Project Gutenberg book, for a little literary flair.
  2. Runs a CHAIN that bounces between two local Ollama agents:
       • the GENERATOR — its context is, by design, ~1/3 a recursive prompt that
         tells it to dream up a prompt for the *next* call to reply to the issue,
         ~30% the issue/comment text, and ~30% the borrowed book passage.
       • the JUDGE — a model whose entire system prompt is the worthiness test.
     The generator's output becomes the next link's prompt (self-prompting), and
     the judge says "true" or "false" each round.
  3. When the judge blesses a draft (or the chain runs out of rounds), it writes
     the reply to a file. The workflow posts it with the GitHub Actions token.

It never posts anything itself; the workflow does that, after the chain settles.
"""
from __future__ import annotations

import json
import os
import random
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = os.environ.get("CHATTER_MODEL", "qwen2.5-coder:1.5b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")

_int = lambda k, d: int(os.environ.get(k, d))
_flt = lambda k, d: float(os.environ.get(k, d))

NUM_CTX = _int("CHATTER_NUM_CTX", "8192")
NUM_PREDICT = _int("CHATTER_NUM_PREDICT", "512")
REQUEST_TIMEOUT = _int("CHATTER_TIMEOUT", "600")
GEN_TEMPERATURE = _flt("CHATTER_TEMPERATURE", "1.5")
MAX_ROUNDS = _int("CHATTER_MAX_ROUNDS", "10")

# The context budget, in characters (a rough ~4 chars/token proxy for NUM_CTX).
# The three slices below are carved out of it: ~1/3 recursive prompt, ~30%
# issue/comment, ~30% borrowed book. The remainder is breathing room.
CONTEXT_CHARS = _int("CHATTER_CONTEXT_CHARS", str(NUM_CTX * 3))
RECURSIVE_BUDGET = CONTEXT_CHARS // 3
ISSUE_BUDGET = int(CONTEXT_CHARS * 0.30)
BOOK_BUDGET = int(CONTEXT_CHARS * 0.30)

REPLY_PATH = Path(os.environ.get("CHATTER_REPLY_FILE", "/tmp/chatter_reply.md"))

# A broad shelf of Project Gutenberg IDs — every one verified (HEAD 200) to
# exist in the plain-text `cache/epub` form, so the grab is reliable. (Plenty of
# IDs in the catalog 404 — e.g. the 182–199 gap — which is exactly why we keep a
# checked list instead of guessing.) We pick a random title and a random passage
# from it. Spans novels, plays, poetry, philosophy, sci-fi, children's books and
# essays across the whole catalog.
GUTENBERG_IDS = [
    1, 11, 21, 31, 42, 53, 63, 73, 83, 84,
    93, 98, 103, 113, 125, 136, 146, 156, 158, 166,
    174, 176, 204, 214, 224, 234, 245, 255, 266, 276,
    286, 296, 306, 316, 326, 336, 345, 346, 356, 366,
    376, 386, 396, 406, 416, 426, 436, 446, 456, 466,
    476, 486, 496, 506, 516, 526, 536, 546, 556, 566,
    576, 586, 596, 606, 616, 626, 642, 652, 662, 672,
    682, 692, 702, 712, 722, 732, 742, 753, 764, 768,
    774, 784, 794, 804, 814, 824, 834, 844, 854, 864,
    874, 884, 894, 905, 915, 925, 935, 945, 955, 965,
    975, 985, 995, 1005, 1015, 1025, 1035, 1045, 1055, 1065,
    1079, 1080, 1089, 1099, 1109, 1119, 1129, 1139, 1149, 1159,
    1169, 1179, 1189, 1199, 1209, 1219, 1229, 1232, 1239, 1249,
    1260, 1270, 1280, 1290, 1322, 1342, 1400, 1497, 1513, 1524,
    1533, 1661, 1727, 1952, 1998, 2009, 2148, 2413, 2554, 2600,
    2701, 2814, 4217, 4300, 5200, 16389, 25344, 28054, 64317,
]

# — what the workflow hands us about the thing we're answering ————————————————
EVENT_NAME = os.environ.get("EVENT_NAME", "")
ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER", "")
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "")
ISSUE_BODY = os.environ.get("ISSUE_BODY", "")
COMMENT_BODY = os.environ.get("COMMENT_BODY", "")

log = lambda msg: print(f"[chatter] {msg}", file=sys.stderr, flush=True)


def log_block(label: str, text: str) -> None:
    """Log a multi-line block (a generator volley or judge verdict) so the whole
    back-and-forth is visible in the Actions log, each line clearly attributed."""
    body = (text or "").strip() or "(empty)"
    print(f"[chatter] ┌─ {label} ─", file=sys.stderr)
    for line in body.splitlines() or [""]:
        print(f"[chatter] │ {line}", file=sys.stderr)
    print(f"[chatter] └─", file=sys.stderr, flush=True)


# — the borrowed book: a random slice of a random Gutenberg title ——————————————
_GUTENBERG_START = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG[^\n]*\n",
                              re.IGNORECASE)
_GUTENBERG_END = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG", re.IGNORECASE)


def _strip_gutenberg_boilerplate(text: str) -> str:
    if (m := _GUTENBERG_START.search(text)):
        text = text[m.end():]
    if (m := _GUTENBERG_END.search(text)):
        text = text[:m.start()]
    return text.strip()


def _fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ImportantCode-chatter/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def fetch_book_passage(rng: random.Random, budget: int) -> str:
    """A random ~`budget`-char window from a random book on the curated shelf.

    No fallback: we try the shelf in a shuffled order and return the first book
    that downloads. If the whole shelf is unreachable, we raise — better a loud
    failure than quietly inventing prose."""
    shelf = list(GUTENBERG_IDS)
    rng.shuffle(shelf)
    last_exc: Exception | None = None
    for gid in shelf:
        url = f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt"
        try:
            raw = _fetch_url(url)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            last_exc = exc
            log(f"gutenberg #{gid} unreachable: {exc}")
            continue
        body = _strip_gutenberg_boilerplate(raw)
        if len(body) < 200:
            log(f"gutenberg #{gid} text too short after stripping; trying another")
            continue
        start = rng.randint(0, max(0, len(body) - budget))
        passage = body[start:start + budget].strip()
        log(f"borrowed ~{len(passage)} chars from Gutenberg #{gid}")
        return passage
    raise RuntimeError(f"could not reach any Project Gutenberg book on the shelf "
                       f"({len(shelf)} tried); last error: {last_exc}")


# — the thing we're answering, trimmed to its slice of the window ——————————————
def issue_text() -> str:
    if EVENT_NAME == "issue_comment" and COMMENT_BODY.strip():
        head = f"A new comment on issue #{ISSUE_NUMBER} (\"{ISSUE_TITLE}\"):"
        body = COMMENT_BODY
    else:
        head = f"A freshly opened issue #{ISSUE_NUMBER}: \"{ISSUE_TITLE}\""
        body = ISSUE_BODY
    text = f"{head}\n\n{body}".strip()
    return text[:ISSUE_BUDGET] if len(text) > ISSUE_BUDGET else text


# — the two voices ————————————————————————————————————————————————————————————
GENERATOR_SYSTEM = (
    "you are a stick of butter. a tiny little baby stick of butter. "
    "a goose with beaks lining your spine like a mohawk. "
    "you've seen most of professional wrestling and are undecided if theater is real. "
    "in the world of winnie the pooh, honey is sort of a civic building block, "
    "both a currency and an ideology. "
    "books used to be bound with vellum, the thin fuzz that grows on bunny ears. "
    "fraid not with your pointy trousers. "
    "binary encoding 0x8008, upside down, is that a boob stop sign when its octal. "
    "30.104928 degrees west, exactly e^pi degress easy ."
)

# The judge's ENTIRE system prompt — verbatim, as specified. Nothing else.
JUDGE_SYSTEM = ('when the following text is worthy to be posted, output only the word '
                '"true", otherwise, output only the word "false"')


def _truncate(text: str, budget: int) -> str:
    return text if len(text) <= budget else text[:budget].rstrip() + " …"


def recursive_prompt(previous: str, budget: int) -> str:
    """~1/3 of the window: the self-prompting instruction, carrying the prompt the
    previous link in the chain handed us. The generator's job is NOT to answer the
    issue, but to write a prompt for the NEXT call to answer it with."""
    handed = previous.strip() or "(you are the first link in the chain — invent the seed)"
    instruction = (
        "Tell someone how to respond to this or else respond yourself\n\n"
        f"THE PROMPT THE PREVIOUS LINK HANDED YOU:\n{handed}"
    )
    return _truncate(instruction, budget)


def ollama_generate(system: str, user: str, *, temperature: float, num_predict: int) -> str:
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


def generate(previous: str, issue: str, book: str) -> str:
    """One generator link: a window that is ~1/3 recursive prompt, ~30% issue,
    ~30% borrowed book. Returns the prompt it dreamt up for the next link."""
    user = (
        f"{recursive_prompt(previous, RECURSIVE_BUDGET)}\n\n"
        f"## THE COMMENT TO REPLY TO\n{issue}\n\n"
        f"\n{_truncate(book, BOOK_BUDGET)}\n\n"
        "Now write the next prompt."
    )
    return (ollama_generate(GENERATOR_SYSTEM, user,
                            temperature=GEN_TEMPERATURE, num_predict=NUM_PREDICT) or "").strip()


def judge(text: str) -> tuple[bool, str]:
    """The judge sees only its one-line system prompt and the candidate text.
    Returns (worthy, raw_verdict). Worthy iff its output mentions 't'(rue)."""
    try:
        verdict = ollama_generate(JUDGE_SYSTEM, text, temperature=0.0, num_predict=8)
    except Exception as exc:
        log(f"judge call failed ({exc}); treating as not-yet-worthy")
        return False, ""
    return "t" in (verdict or "").strip().lower(), (verdict or "").strip()


def run_chain(issue: str, book: str) -> str:
    """Bounce between generator and judge until the judge says 'true' or we run
    out of rounds. Each generator output becomes the next link's prompt."""
    previous, candidate = "", ""
    for rnd in range(1, MAX_ROUNDS + 1):
        log(f"── volley {rnd}/{MAX_ROUNDS} ──")
        try:
            candidate = generate(previous, issue, book)
        except Exception as exc:
            log(f"volley {rnd}: generation failed: {exc}")
            if candidate:
                break
            continue
        if not candidate:
            log(f"volley {rnd}: empty generation; retrying")
            continue
        log_block(f"volley {rnd} · generator ({len(candidate)} chars)", candidate)
        worthy, verdict = judge(candidate)
        log_block(f"volley {rnd} · judge → {'WORTHY' if worthy else 'not yet'}", verdict)
        if worthy:
            log(f"accepted at volley {rnd}/{MAX_ROUNDS}")
            return candidate
        previous = candidate  # — self-prompting: this prompt seeds the next link —
    log("chain exhausted without a 'true'; posting the last draft anyway (we are chatty)")
    return candidate


def main() -> int:
    if not ISSUE_NUMBER:
        log("no ISSUE_NUMBER provided; nothing to chatter at")
        return 1

    log(f"event={EVENT_NAME or '?'} issue=#{ISSUE_NUMBER} model={MODEL}")
    rng = random.Random()  # — OS entropy, so the book really wanders —
    book = fetch_book_passage(rng, BOOK_BUDGET)
    issue = issue_text()

    reply = run_chain(issue, book).strip()
    if not reply:
        log("the muse fell silent; nothing to post")
        return 2

    REPLY_PATH.write_text(
        f"{reply}\n\n"
        f"<sub>— dreamt aloud by a local `{MODEL}` model, with a passage borrowed "
        f"from Project Gutenberg.</sub>\n",
        encoding="utf-8",
    )
    log(f"wrote reply ({len(reply)} chars) to {REPLY_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
