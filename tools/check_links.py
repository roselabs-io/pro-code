#!/usr/bin/env python3
"""Check that every relative link of the tracked Markdown files resolves to a tracked path.

    python3 tools/check_links.py [--exclude GLOB ...]

Run at the root of a Git checkout. For each file of `git ls-files '*.md'`, it reads the inline
links `[text](target)`, the images `![alt](target)` and the reference definitions `[id]: target`
outside fenced code blocks and inline code spans. A target with a URL scheme (`https:`, `mailto:`)
or only a fragment (`#section`) is not checked. The fragment and query of a relative target are
removed, the rest is resolved against the file's directory (a leading `/` against the root), and
it must name a tracked file or a directory holding one. Each broken link is printed as
`path:line: target` and the exit is 1; with none the exit is 0. A file whose path matches an
`--exclude` glob (`fnmatch`, so `*` also matches `/`) is not read.

Limits: fragments are not checked against headings, links in HTML files and HTML tags are not
read, and a target containing a space or a parenthesis must be written in angle brackets.
"""

from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
from pathlib import PurePosixPath

INLINE = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]+)")
REFERENCE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
CODE_SPAN = re.compile(r"(`+).*?\1")
FENCE = re.compile(r"^\s{0,3}(```|~~~)")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
    return [p for p in out.split("\0") if p]


def targets(text: str):
    """``(line number, target)`` of each link outside code."""
    fence = None
    for lineno, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line)
        if m:
            if fence is None:
                fence = m.group(1)
            elif m.group(1) == fence:
                fence = None
            continue
        if fence is not None:
            continue
        line = CODE_SPAN.sub("", line)
        for rx in (INLINE, REFERENCE):
            for found in rx.finditer(line):
                yield lineno, found.group(1).strip("<>")


def resolve(source: str, target: str) -> str | None:
    """The repository path ``target`` names from ``source``, or None when it is not checked."""
    if not target or target.startswith("#") or SCHEME.match(target):
        return None
    path = re.split(r"[#?]", target, maxsplit=1)[0]
    if not path:
        return None
    base = PurePosixPath("/") if path.startswith("/") else PurePosixPath("/", source).parent
    parts: list[str] = []
    for part in (base / path).parts[1:]:
        if part == "..":
            if parts:
                parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts)


def main(argv: list[str]) -> int:
    excludes = [argv[i + 1] for i, a in enumerate(argv[:-1]) if a == "--exclude"]
    files = tracked()
    paths = set(files)
    dirs = {str(parent) for f in files for parent in PurePosixPath(f).parents}
    broken = []
    for source in sorted(f for f in files if f.endswith(".md")):
        if any(fnmatch.fnmatch(source, glob) for glob in excludes):
            continue
        with open(source, encoding="utf-8") as fh:
            text = fh.read()
        for lineno, target in targets(text):
            path = resolve(source, target)
            if path is not None and path not in paths and path not in dirs:
                broken.append(f"{source}:{lineno}: {target}")
    for line in broken:
        print(line)
    if broken:
        print(f"{len(broken)} broken relative links", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
