"""Severity — the one source of truth for the alert levels.

The only place the severity strings live; everything else uses the enum constant
(named-severity-constant), so a level is never a bare string or magic number.
"""

from __future__ import annotations

from enum import Enum


class Severity(str, Enum):
    """A named alert level, ranked so transitions can compare severity."""

    NOMINAL = "nominal"
    WARNING = "warning"  # doctrine: allow — the enum is the one home for the strings
    CRITICAL = "critical"  # doctrine: allow — the enum is the one home for the strings


_RANK = {
    Severity.NOMINAL: 0,
    Severity.WARNING: 1,
    Severity.CRITICAL: 2,
}


def rank(severity: Severity) -> int:
    """Return the ordinal so a raise (higher) is distinguishable from a clear (lower)."""
    return _RANK[severity]
