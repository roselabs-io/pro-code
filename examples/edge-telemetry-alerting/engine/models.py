"""Domain models — the reading (validated at ingest), the rules, and the signal state."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from engine.severity import Severity


class Reading(BaseModel):
    """A telemetry sample, validated at ingest; a bad line never reaches the rules."""

    signal: str
    value: float
    ts: float


@dataclass(frozen=True)
class LevelRule:
    """A threshold rule with a hysteresis band and a debounce count."""

    direction: str
    hysteresis: float
    debounce_samples: int
    warn_at: float | None = None
    crit_at: float | None = None


@dataclass(frozen=True)
class StalenessRule:
    """Absence past this TTL is itself an alert."""

    ttl_seconds: float


@dataclass(frozen=True)
class SignalSpec:
    """A signal's identity + its alert rules, loaded from the station config."""

    name: str
    unit: str
    safety_critical: bool
    level: LevelRule | None = None
    staleness: StalenessRule | None = None


@dataclass
class Alert:
    """An open condition — a burst dedups into one, tracked by an occurrence count."""

    signal: str
    severity: Severity
    opened_at: float
    count: int = 1
    cleared: bool = False


@dataclass
class SignalStatus:
    """The read-time view — value nulled when stale, always carrying a text label."""

    name: str
    unit: str
    value: float | None
    stale: bool
    severity: Severity
    label: str
