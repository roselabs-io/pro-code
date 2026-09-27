#!/usr/bin/env python3
"""Emit exactly the documents one pipeline role consumes.

Frontmatter drives the selection: `consumed_by` lists the roles, `profile` scopes
a file to one domain profile (or `agnostic`), `scope` on the project side marks a
file as `mvp1`, `direction` or `reference`. A role reads this command's output
instead of opening files; that is one tool call rather than one per document.

  context.py --role build --profile local-app --project ../praxis [--tickets T31,T32]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def frontmatter(text: str) -> dict[str, str]:
    m = FM.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def listed(value: str) -> list[str]:
    return [p.strip() for p in value.strip("[]").split(",") if p.strip()]


def select(root: Path, role: str, profile: str, scopes: set[str], tickets: set[str]):
    for f in sorted(root.rglob("*.md")):
        if any(p in {".git", "examples", "evals", ".pytest_cache", "node_modules"} for p in f.parts):
            continue
        text = f.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if not fm:
            continue
        if role not in listed(fm.get("consumed_by", "")):
            continue
        if fm.get("profile", "agnostic") not in {"agnostic", profile}:
            continue
        if "scope" in fm and fm["scope"] not in scopes:
            continue
        # A ticketed file is emitted only when the run touches one of its tickets.
        own = set(listed(fm.get("tickets", "")))
        if own and tickets and not (own & tickets):
            continue
        yield f, text[FM.match(text).end():] if FM.match(text) else text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True)
    ap.add_argument("--profile", default="local-app")
    ap.add_argument("--project", default=None, help="a second root to scan (the project's docs/)")
    ap.add_argument("--scopes", default="mvp1,reference")
    ap.add_argument("--tickets", default="")
    ap.add_argument("--list", action="store_true", help="print paths and sizes, not content")
    a = ap.parse_args()

    roots = [Path(__file__).resolve().parent.parent]
    if a.project:
        roots.append(Path(a.project).resolve())
    scopes = set(a.scopes.split(","))
    tickets = {t.strip() for t in a.tickets.split(",") if t.strip()}

    total = 0
    for root in roots:
        for f, body in select(root, a.role, a.profile, scopes, tickets):
            total += len(body)
            if a.list:
                print(f"{len(body.split()):6} w  {f}")
            else:
                print(f"\n===== {f.relative_to(root.parent)} =====\n{body.rstrip()}")
    if a.list:
        print(f"\n{total // 1000}k chars ~ {int(total / 4000)}k tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
