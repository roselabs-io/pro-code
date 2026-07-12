#!/usr/bin/env python3
"""Boundary-dependency codemod — enforce that EVERY route carries `Depends(get_caller)`.

Isolation rests on every handler resolving a Caller at the boundary; a route that
forgets the dependency is an unguarded hole. This deterministic check (and its auto-fix)
keeps the convention across all handlers so drift can't slip an unscoped route in.

Usage:
  require_caller_dep.py <path...>            # add the dependency to any route missing it
  require_caller_dep.py --check <path...>    # dry-run: report violations, exit 1 if any

Idempotent: a second run rewrites nothing. Deterministic: no clock/random.
"""

from __future__ import annotations

import sys
from pathlib import Path

import libcst as cst
import libcst.matchers as m

ROUTE_METHODS = {"get", "post", "put", "patch", "delete"}

_route_decorator = m.Decorator(
    decorator=m.Call(func=m.Attribute(value=m.Name("app"), attr=m.Name()))
)


def _is_route(func: cst.FunctionDef) -> bool:
    for dec in func.decorators:
        if m.matches(dec, _route_decorator):
            attr = dec.decorator.func  # type: ignore[attr-defined]
            if attr.attr.value in ROUTE_METHODS:
                return True
    return False


def _has_caller_dep(func: cst.FunctionDef) -> bool:
    for param in func.params.params:
        default = param.default
        if (
            isinstance(default, cst.Call)
            and isinstance(default.func, cst.Name)
            and default.func.value == "Depends"
            and default.args
            and isinstance(default.args[0].value, cst.Name)
            and default.args[0].value.value == "get_caller"
        ):
            return True
    return False


class _Checker(cst.CSTVisitor):
    def __init__(self) -> None:
        self.violations: list[str] = []

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        if _is_route(node) and not _has_caller_dep(node):
            self.violations.append(node.name.value)


class _Fixer(cst.CSTTransformer):
    def __init__(self) -> None:
        self.rewritten = 0

    def leave_FunctionDef(
        self, original: cst.FunctionDef, updated: cst.FunctionDef
    ) -> cst.FunctionDef:
        if not (_is_route(original) and not _has_caller_dep(original)):
            return updated
        self.rewritten += 1
        caller_param = cst.Param(
            name=cst.Name("caller"),
            annotation=cst.Annotation(cst.Name("Caller")),
            default=cst.parse_expression("Depends(get_caller)"),
        )
        new_params = (*updated.params.params, caller_param)
        return updated.with_changes(params=updated.params.with_changes(params=new_params))


def _paths(args: list[str]) -> list[Path]:
    out: list[Path] = []
    for a in args:
        p = Path(a)
        out.extend(p.rglob("*.py") if p.is_dir() else [p])
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files = _paths([a for a in argv if not a.startswith("--")])

    total_violations = 0
    total_rewritten = 0
    for f in files:
        module = cst.parse_module(f.read_text())
        if check:
            checker = _Checker()
            module.visit(checker)
            for name in checker.violations:
                print(f"{f}:{name}: route is missing Depends(get_caller)")
            total_violations += len(checker.violations)
        else:
            fixer = _Fixer()
            new_module = module.visit(fixer)
            if fixer.rewritten:
                f.write_text(new_module.code)
            total_rewritten += fixer.rewritten

    scanned = len(files)
    if check:
        if total_violations:
            print(
                f"require_caller_dep: {total_violations} unguarded route(s)"
            )
            return 1
        print(
            f"require_caller_dep: {scanned} file(s) — every route carries the caller dep"
        )
        return 0
    print(f"require_caller_dep: {scanned} scanned, {total_rewritten} rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
