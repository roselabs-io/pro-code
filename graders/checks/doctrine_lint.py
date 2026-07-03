#!/usr/bin/env python3
"""Doctrine linter — the deterministic special-lint grader (static analysis).

Enforces the regex-able subset of the comment doctrine + the test-posture floor, plus any
domain forbidden-patterns a profile declares via --forbid. The judgment cases (docstring
narration, subtle over-comment, posture emphasis) stay with the fuzzy graders — this is the
mechanical floor that runs FIRST in the verification loop and short-circuits.

Agnostic: the domain rules arrive as --forbid args from the profile's justfile; the code
here is domain-neutral. A line or comment containing `doctrine: allow` is exempt.

Usage:
  doctrine_lint.py <path...> [--forbid 'REGEX@@message' ...] [--no-comment] [--no-posture]
The REGEX and message are split on `@@` (chosen so a `:` or `|` in the regex is safe).
Exit 0 if clean, 1 if any finding.
"""

from __future__ import annotations

import ast
import re
import sys
import tokenize
from pathlib import Path

ALLOW = "doctrine: allow"

COMMENT_RULES = [
    (
        re.compile(r"\bT\d+\b|\b[A-Z]{2,}-\d+\b"),
        "inline ticket ref — traceability belongs in the commit, not the code",
    ),
    (
        re.compile(
            r"\b(previously|used to|formerly|no longer|renamed from|changed from|originally)\b",
            re.I,
        ),
        "backward-narration — a comment states what the code IS, not its history",
    ),
    (
        re.compile(r"\b(we (don't|do not|avoid|can't|cannot)|why not)\b", re.I),
        "defensive why-not — the reason belongs in the commit or an ADR",
    ),
]


def _comments(path: Path):
    with path.open("rb") as fh:
        try:
            for tok in tokenize.tokenize(fh.readline):
                if tok.type == tokenize.COMMENT:
                    yield tok.start[0], tok.string
        except tokenize.TokenError:
            return


def check_comment_doctrine(path: Path) -> list[tuple[int, str, str]]:
    out = []
    for lineno, text in _comments(path):
        if ALLOW in text or "noqa" in text or "type:" in text:
            continue  # linter/type directives are not prose — a code like T201 is not a ticket ref
        for rx, msg in COMMENT_RULES:
            if rx.search(text):
                out.append((lineno, "comment-doctrine", msg))
    return out


def check_forbids(path: Path, lines: list[str], forbids) -> list[tuple[int, str, str]]:
    out = []
    for i, line in enumerate(lines, 1):
        if ALLOW in line:
            continue
        for rx, msg in forbids:
            if rx.search(line):
                out.append((i, "special-lint", msg))
    return out


def check_test_posture(path: Path, src: str, lines: list[str]) -> list[tuple[int, str, str]]:
    out = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return out
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            body_src = "\n".join(lines[node.lineno - 1 : (node.end_lineno or node.lineno)])
            has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(node))
            has_raises = "raises(" in body_src or "raises (" in body_src
            if not (has_assert or has_raises):
                out.append((node.lineno, "test-posture", f"{node.name} has no assertion"))
            for dec in node.decorator_list:
                deco = ast.get_source_segment(src, dec) or ""
                if ("skip" in deco or "xfail" in deco) and "reason" not in deco:
                    out.append((node.lineno, "test-posture", f"{node.name} skipped with no reason="))
    return out


def parse_forbids(argv: list[str]) -> list[tuple[re.Pattern, str]]:
    forbids = []
    for i, a in enumerate(argv):
        if a == "--forbid" and i + 1 < len(argv):
            spec = argv[i + 1]
            pat, _, msg = spec.partition("@@")
            forbids.append((re.compile(pat), msg or f"forbidden: {pat}"))
    return forbids


def main(argv: list[str]) -> int:
    do_comment = "--no-comment" not in argv
    do_posture = "--no-posture" not in argv
    forbids = parse_forbids(argv)
    skip_next = False
    paths: list[str] = []
    for i, a in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        if a == "--forbid":
            skip_next = True
        elif a.startswith("--"):
            continue
        else:
            paths.append(a)

    files: list[Path] = []
    for p in paths:
        pp = Path(p)
        files.extend(pp.rglob("*.py") if pp.is_dir() else [pp])

    findings = []
    for f in sorted(set(files)):
        src = f.read_text()
        lines = src.splitlines()
        if do_comment:
            findings += [(f, *x) for x in check_comment_doctrine(f)]
        if forbids:
            findings += [(f, *x) for x in check_forbids(f, lines, forbids)]
        if do_posture and f.name.startswith("test_"):
            findings += [(f, *x) for x in check_test_posture(f, src, lines)]

    for f, lineno, kind, msg in findings:
        print(f"{f}:{lineno}: [{kind}] {msg}")
    if findings:
        print(f"\ndoctrine_lint: {len(findings)} finding(s)")
        return 1
    print("doctrine_lint: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
