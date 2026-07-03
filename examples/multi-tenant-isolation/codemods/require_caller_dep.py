#!/usr/bin/env python3
"""Codemod — every FastAPI route must depend on ``get_caller`` at the boundary.

The boundary-dependency convention spans every handler, so a script enforces it rather
than a per-file review: a route that forgets ``caller: CallerDep`` would skip the
isolation boundary. libcst-based, deterministic, idempotent. A route is compliant when a
param resolves the caller through the boundary (``CallerDep`` / ``Depends(get_caller)``).

Usage:
  require_caller_dep.py <path...>            # add the missing dependency in place
  require_caller_dep.py --check <path...>    # report violations, exit 1 if any (the gate)
"""

from __future__ import annotations

import sys
from pathlib import Path

import libcst as cst
import libcst.matchers as m

HTTP_METHODS = {"get", "post", "put", "patch", "delete"}

# A parameter resolves the caller if it references either the boundary dependency
# (``get_caller``) or the annotated alias that wraps it (``CallerDep``).
BOUNDARY_MARKERS = ("get_caller", "CallerDep")

_ROUTE_DECORATOR = m.Call(
    func=m.Attribute(value=m.Name(), attr=m.Name()),
)


def _is_route(node: cst.FunctionDef) -> bool:
    for dec in node.decorators:
        deco = dec.decorator
        if m.matches(deco, _ROUTE_DECORATOR):
            assert isinstance(deco, cst.Call)
            attr = deco.func
            assert isinstance(attr, cst.Attribute)
            if attr.attr.value in HTTP_METHODS:
                return True
    return False


def _has_caller_dep(node: cst.FunctionDef) -> bool:
    params = node.params
    everything = list(params.params) + list(params.kwonly_params)
    for param in everything:
        rendered = cst.Module([]).code_for_node(param)
        if any(marker in rendered for marker in BOUNDARY_MARKERS):
            return True
    return False


class _AddCallerDep(cst.CSTTransformer):
    def __init__(self) -> None:
        self.violations: list[str] = []

    def leave_FunctionDef(
        self, original: cst.FunctionDef, updated: cst.FunctionDef
    ) -> cst.FunctionDef:
        if not _is_route(original) or _has_caller_dep(original):
            return updated
        self.violations.append(original.name.value)
        caller_param = cst.Param(
            name=cst.Name("caller"),
            annotation=cst.Annotation(cst.Name("CallerDep")),
        )
        params = updated.params
        return updated.with_changes(
            params=params.with_changes(params=[*params.params, caller_param])
        )


def _process(path: Path, check: bool) -> list[str]:
    module = cst.parse_module(path.read_text())
    transformer = _AddCallerDep()
    new_module = module.visit(transformer)
    if not check and transformer.violations:
        path.write_text(new_module.code)
    return [f"{path}:{name}" for name in transformer.violations]


def main(argv: list[str]) -> int:
    check = "--check" in argv
    paths = [Path(a) for a in argv if not a.startswith("--")]
    files: list[Path] = []
    for p in paths:
        files.extend(p.rglob("*.py") if p.is_dir() else [p])

    violations: list[str] = []
    for f in sorted(set(files)):
        violations += _process(f, check)

    if check and violations:
        for v in violations:
            print(
                f"{v}: route missing Depends(get_caller)"
            )  # doctrine: allow — codemod CLI
        print(
            f"require_caller_dep: {len(violations)} route(s) missing the boundary dep"
        )  # doctrine: allow
        return 1
    label = "would fix" if check else "fixed"
    print(
        f"require_caller_dep: {len(violations)} {label}, {len(files)} scanned"
    )  # doctrine: allow
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
