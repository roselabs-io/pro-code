"""Core domain records — readings in, alerts out."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from engine.severity import Severity


class AlertKind(str, Enum):
    THRESHOLD = "threshold"  # doctrine: allow — kind label, not a severity
    STALENESS = "staleness"  # doctrine: allow


@dataclass(frozen=True)
class Reading:
    signal: str
    value: float
    ts: float


@dataclass
class Alert:
    signal: str
    severity: Severity
    kind: AlertKind
    reason: str
    opened_at: float
    count: int = 1
