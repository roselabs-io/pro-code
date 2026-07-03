"""The rule engine — readings in, alerts out, no missed critical.

Per signal it holds threshold-with-hysteresis + debounce state and a staleness watchdog:

- **threshold-with-hysteresis** — fire when value crosses ``limit``; clears once it drops
  back past ``limit ∓ hysteresis`` (a value hovering at the line does not flap).
- **debounce-transient** — a breach holds ``debounce`` consecutive samples before firing
  (a single-sample spike is ignored).
- **staleness-watchdog** — no reading within ``staleness_ttl`` is itself an alert; a
  signal that has *never* reported since boot is stale too (dead-from-boot), measured from
  ``station_start``.
- **alert-dedup-storm-guard** — a sustained breach is one active alert with a count,
  not one per sample.
- **out-of-order tolerance** — a late sample older than the newest is dropped, so it
  cannot resurrect a cleared alert.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engine.config import SignalRule, StationConfig
from engine.log import ALERT_CLEARED, ALERT_RAISED, LOG
from engine.models import Alert, AlertKind, Reading

_INFO_LEVEL = "info"  # doctrine: allow — a log level, not a severity
_STATUS_OK = "ok"  # doctrine: allow — a status label, not a severity


@dataclass
class _SignalState:
    last_value: float | None = None
    last_ts: float | None = None
    breach_streak: int = 0
    active: Alert | None = None


class Monitor:
    def __init__(self, config: StationConfig, station_start: float = 0.0) -> None:
        self.config = config
        self.station_start = station_start
        self.states: dict[str, _SignalState] = {n: _SignalState() for n in config.signals}

    def reset(self) -> None:
        self.states = {n: _SignalState() for n in self.config.signals}

    # ---- ingest ----------------------------------------------------------

    def process(self, reading: Reading) -> None:
        rule = self.config.signals.get(reading.signal)
        if rule is None:
            return
        st = self.states[reading.signal]
        if st.last_ts is not None and reading.ts < st.last_ts:
            return  # out-of-order: a late earlier sample cannot resurrect anything
        st.last_value = reading.value
        st.last_ts = reading.ts
        if st.active is not None and st.active.kind is AlertKind.STALENESS:
            self._clear(reading.signal)  # a fresh reading ends staleness
        self._eval_threshold(rule, st, reading)

    def _eval_threshold(
        self, rule: SignalRule, st: _SignalState, reading: Reading
    ) -> None:
        if st.active is not None and st.active.kind is AlertKind.THRESHOLD:
            if rule.is_clear(reading.value):
                self._clear(reading.signal)
            else:
                st.active.count += 1  # dedup: one alert, occurrence counted
            return
        if rule.is_breaching(reading.value):
            st.breach_streak += 1
            if st.breach_streak >= rule.debounce:
                reason = f"{rule.name} {reading.value}{rule.unit} crossed {rule.limit}"
                self._raise(rule, AlertKind.THRESHOLD, reason)
                st.breach_streak = 0
        else:
            st.breach_streak = 0

    # ---- staleness watchdog ---------------------------------------------

    def check_staleness(self, now: float) -> None:
        for name, rule in self.config.signals.items():
            st = self.states[name]
            reference = st.last_ts if st.last_ts is not None else self.station_start
            if now - reference <= rule.staleness_ttl:
                continue
            if st.active is not None and st.active.kind is AlertKind.STALENESS:
                continue
            origin = "never reported since boot" if st.last_ts is None else "no reading"
            if st.active is not None:
                self._clear(name)  # staleness supersedes a stale threshold alert
            reason = f"{name} stale — {origin} within {rule.staleness_ttl}s"
            self._raise(rule, AlertKind.STALENESS, reason)

    # ---- alert bookkeeping ----------------------------------------------

    def _raise(self, rule: SignalRule, kind: AlertKind, reason: str) -> None:
        opened = self.states[rule.name].last_ts or self.station_start
        self.states[rule.name].active = Alert(
            signal=rule.name,
            severity=rule.severity,
            kind=kind,
            reason=reason,
            opened_at=opened,
        )
        LOG.event(
            ALERT_RAISED,
            rule.severity.value,
            signal=rule.name,
            severity=rule.severity.value,
            kind=kind.value,
        )

    def _clear(self, name: str) -> None:
        if self.states[name].active is None:
            return
        self.states[name].active = None
        LOG.event(ALERT_CLEARED, _INFO_LEVEL, signal=name)

    # ---- read model ------------------------------------------------------

    def active_alerts(self) -> list[Alert]:
        return [st.active for st in self.states.values() if st.active is not None]

    def snapshot(self, now: float) -> dict[str, Any]:
        """The /state read model. Evaluates staleness as of ``now`` before rendering."""
        self.check_staleness(now)
        signals = []
        for name, rule in self.config.signals.items():
            st = self.states[name]
            stale = st.active is not None and st.active.kind is AlertKind.STALENESS
            status = st.active.severity.value if st.active is not None else _STATUS_OK
            signals.append(
                {
                    "name": name,
                    "unit": rule.unit,
                    "value": None if stale else st.last_value,
                    "stale": stale,
                    "status": status,
                    "safety_critical": rule.safety_critical,
                    "ts": st.last_ts,
                }
            )
        alerts = [
            {
                "signal": a.signal,
                "severity": a.severity.value,
                "kind": a.kind.value,
                "reason": a.reason,
                "count": a.count,
            }
            for a in self.active_alerts()
        ]
        return {
            "station": self.config.name,
            "signals": signals,
            "alerts": alerts,
            "generated_at": now,
        }
