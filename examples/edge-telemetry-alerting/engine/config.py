"""Station config loader — reads the signal catalog + rules from station.toml.

Thresholds are config-driven: the rule code never carries a literal limit, so re-tuning
the station is a config edit, not a code change.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from engine.models import LevelRule, SignalSpec, StalenessRule

_DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "station.toml"


@dataclass(frozen=True)
class Station:
    """A loaded station — its name and its ordered signal catalog."""

    name: str
    signals: list[SignalSpec]


def _level(raw: dict) -> LevelRule:
    """Build a level rule from its config block."""
    return LevelRule(
        direction=raw["direction"],
        hysteresis=float(raw["hysteresis"]),
        debounce_samples=int(raw.get("debounce_samples", 1)),
        warn_at=None if raw.get("warn_at") is None else float(raw["warn_at"]),
        crit_at=None if raw.get("crit_at") is None else float(raw["crit_at"]),
    )


def _signal(raw: dict) -> SignalSpec:
    """Build a signal spec from its config block."""
    level = _level(raw["level"]) if "level" in raw else None
    staleness = (
        StalenessRule(ttl_seconds=float(raw["staleness"]["ttl_seconds"]))
        if "staleness" in raw
        else None
    )
    return SignalSpec(
        name=raw["name"],
        unit=raw["unit"],
        safety_critical=bool(raw["safety_critical"]),
        level=level,
        staleness=staleness,
    )


def load_station(path: Path | None = None) -> Station:
    """Load the station; a safety-critical signal with no alert condition fails loudly."""
    path = path or _DEFAULT_CONFIG
    raw = tomllib.loads(path.read_text())
    signals = [_signal(s) for s in raw["signal"]]
    for spec in signals:
        if spec.safety_critical and spec.level is None and spec.staleness is None:
            raise ValueError(
                f"safety-critical signal {spec.name!r} has no alert condition"
            )
    return Station(name=raw["station"], signals=signals)
