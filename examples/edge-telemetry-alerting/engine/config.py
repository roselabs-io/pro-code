"""Station config — thresholds, hysteresis, debounce and TTLs live in TOML, not code.

The ``config-driven-thresholds`` shape: re-tuning is a config edit, not a code change.
The TOML carries severity as a *string* — data, not code (the ``severity-constant`` lint
polices only ``.py``); it maps to the ``Severity`` enum here at load.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from engine.severity import Severity

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "station.toml"


@dataclass(frozen=True)
class SignalRule:
    name: str
    unit: str
    safety_critical: bool
    severity: Severity
    # "high": breach when value rises past `limit`; "low": when it falls below.
    direction: str
    limit: float
    hysteresis: float
    debounce: int
    staleness_ttl: float

    def is_breaching(self, value: float) -> bool:
        if self.direction == "high":
            return value > self.limit
        return value < self.limit

    def is_clear(self, value: float) -> bool:
        """Hysteresis: clear only once the value falls back past ``limit ∓ h``."""
        if self.direction == "high":
            return value < self.limit - self.hysteresis
        return value > self.limit + self.hysteresis


@dataclass(frozen=True)
class StationConfig:
    name: str
    signals: dict[str, SignalRule]

    def safety_critical_signals(self) -> list[str]:
        return [n for n, s in self.signals.items() if s.safety_critical]


def load_station(path: Path | None = None) -> StationConfig:
    raw = tomllib.loads((path or DEFAULT_CONFIG).read_text())
    signals: dict[str, SignalRule] = {}
    for entry in raw["signal"]:
        rule = SignalRule(
            name=entry["name"],
            unit=entry["unit"],
            safety_critical=entry["safety_critical"],
            severity=Severity.from_name(entry["severity"]),
            direction=entry["direction"],
            limit=float(entry["limit"]),
            hysteresis=float(entry["hysteresis"]),
            debounce=int(entry["debounce"]),
            staleness_ttl=float(entry["staleness_ttl"]),
        )
        signals[rule.name] = rule
    return StationConfig(name=raw["station"]["name"], signals=signals)
