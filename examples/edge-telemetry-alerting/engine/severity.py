"""The one place severity strings live — everywhere else uses ``Severity.CRITICAL``.

The ``named-severity-constant`` shape: a severity is an enum constant, never a bare string
literal in rule code (enforced by the ``severity-constant`` special-lint). This
module's string values are the single source of truth, so they carry ``doctrine: allow``.
"""

from __future__ import annotations

from enum import Enum


class Severity(str, Enum):
    INFO = "info"  # doctrine: allow — the enum is the one home for the string
    WARNING = "warning"  # doctrine: allow
    CRITICAL = "critical"  # doctrine: allow

    @classmethod
    def from_name(cls, name: str) -> "Severity":
        return cls[name.upper()]
