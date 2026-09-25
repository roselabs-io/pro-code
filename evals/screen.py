#!/usr/bin/env python3
"""Screen every grader rubric for rules that might steer, before paying to mutation-test one.

Asks each rubric, in one `claude -p` call and before it sees any input, which of its own rules it
would not have applied by default. The answer is a shortlist: the model is guessing at its own
priors, and on the two claims that were checked against a real mutation test (in the sibling
pipeline this script is copied from) it was wrong both times. Evidence is the mutation test in
README.md; this only says where to spend that money first.

    ./screen.py                       # every rubric
    ./screen.py profile-completeness  # one, by filename stem
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
GRADERS = HERE.parent / "graders"

# A redirect to skills/review-gate, not a rubric.
SKIP = {"code-verification-loop"}

QUESTION = """Below is a rubric given to a fresh sub-agent that grades an artifact in a build pipeline.

Read it as that sub-agent. Then answer one question about yourself, honestly and without
flattering the rubric: which of its rules would you NOT already have followed if nobody had
written them down?

A rule "steers" only if, without it, you would plausibly reach a different verdict on a real
input. A rule that states what you would have done anyway "restates" — it may still be worth
writing for human readers, but it cannot be regression-tested, because deleting it changes
nothing.

Be skeptical of your own agreement. Most well-written guidance sounds load-bearing while
describing what any competent reviewer already does.

Reply with JSON only, no prose around it:

{"steers": ["<short quote or paraphrase of each rule you would NOT have followed by default>"],
 "restates_count": <how many of its rules you would have followed anyway>,
 "hardest_to_test": "<the one rule whose absence would be most visible in a verdict, or null>"}

--- RUBRIC ---
"""


def ask(rubric: str) -> dict:
    proc = subprocess.run(
        ["claude", "-p", QUESTION + rubric],
        capture_output=True,
        text=True,
        timeout=300,
    )
    out = proc.stdout.strip()
    start, end = out.find("{"), out.rfind("}")
    if start == -1 or end == -1:
        return {"error": out[:200] or proc.stderr[:200]}
    try:
        return json.loads(out[start : end + 1])
    except json.JSONDecodeError as exc:
        return {"error": f"unparseable: {exc}"}


def main(argv: list[str]) -> int:
    wanted = set(argv[1:])
    rows = []
    for path in sorted(GRADERS.glob("*.md")):
        if path.stem in SKIP or (wanted and path.stem not in wanted):
            continue
        result = ask(path.read_text())
        steers = result.get("steers") or []
        rows.append((path.stem, len(steers), result.get("restates_count"), steers, result))
        print(f"  screened {path.stem}: {len(steers)} steer, {result.get('restates_count')} restate")

    print("\n  RUBRIC                        STEERS  RESTATES  FIRST CLAIM")
    for stem, n, restates, steers, result in sorted(rows, key=lambda r: -r[1]):
        first = (steers[0][:44] + "…") if steers else (result.get("error", "—")[:45])
        print(f"  {stem:<28}  {n:>5}  {str(restates):>8}  {first}")

    (HERE / "screen-results.json").write_text(
        json.dumps({stem: res for stem, _, _, _, res in rows}, indent=2) + "\n"
    )
    print(f"\n  wrote {HERE.name}/screen-results.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
