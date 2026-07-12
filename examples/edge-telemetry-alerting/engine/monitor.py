"""The rule engine — ingest readings, evaluate rules, open/clear alerts.

Level rules apply a hysteresis band (clear only past threshold∓h) and a debounce count
(hold N samples before raising). Staleness is evaluated lazily on read against the query
clock: a signal past its TTL — or never reported (dead from boot) — is stale, and a
safety-critical stale signal is CRITICAL. An out-of-order (older-ts) reading is ignored,
so a late sample can't resurrect a cleared alert.
"""

from __future__ import annotations

from dataclasses import dataclass

from engine import log
from engine.config import Station, load_station
from engine.models import Alert, LevelRule, Reading, SignalSpec, SignalStatus
from engine.severity import Severity, rank

_STALE_LABEL = "— stale"


@dataclass
class _Runtime:
    """Mutable per-signal state carried across readings."""

    last_value: float | None = None
    last_ts: float | None = None
    level: Severity = Severity.NOMINAL
    breach_streak: int = 0
    level_alert: Alert | None = None
    stale_alert: Alert | None = None


class Monitor:
    """Holds per-signal state and turns a stream of readings into alerts."""

    def __init__(self, station: Station | None = None) -> None:
        self.station = station or load_station()
        self._specs: dict[str, SignalSpec] = {s.name: s for s in self.station.signals}
        self._rt: dict[str, _Runtime] = {s.name: _Runtime() for s in self.station.signals}

    def process(self, reading: Reading) -> None:
        """Fold a reading into its signal's state; ignore an older out-of-order sample."""
        spec = self._specs.get(reading.signal)
        if spec is None:
            return
        rt = self._rt[reading.signal]
        if rt.last_ts is not None and reading.ts <= rt.last_ts:
            return
        rt.last_value = reading.value
        rt.last_ts = reading.ts
        if spec.level is not None:
            self._eval_level(spec, spec.level, rt, reading.value, reading.ts)

    def _eval_level(
        self, spec: SignalSpec, rule: LevelRule, rt: _Runtime, value: float, ts: float
    ) -> None:
        """Commit the level severity, then move alerts.

        Debounce guards only the INITIAL raise from nominal — N consecutive breaching
        samples (any severity) before firing, so a lone spike is ignored but a
        sustained breach that oscillates still fires. Once alerting, a rise escalates
        immediately (a missed critical beats a false one); hysteresis governs the drop.
        """
        candidate = _candidate_level(rule, rt.level, value)
        if rt.level == Severity.NOMINAL:
            if candidate == Severity.NOMINAL:
                rt.breach_streak = 0
            else:
                rt.breach_streak += 1
                if rt.breach_streak >= rule.debounce_samples:
                    rt.level = candidate
                    rt.breach_streak = 0
        else:
            rt.level = candidate
            if candidate == Severity.NOMINAL:
                rt.breach_streak = 0
        self._sync_level_alert(spec, rt, ts)

    def _sync_level_alert(self, spec: SignalSpec, rt: _Runtime, ts: float) -> None:
        """Raise / escalate / dedup / clear the level alert to match the level."""
        if rt.level == Severity.NOMINAL:
            if rt.level_alert is not None:
                rt.level_alert.cleared = True
                rt.level_alert = None
                log.emit(log.ALERT_CLEARED, signal=spec.name)
            return
        if rt.level_alert is None:
            rt.level_alert = Alert(signal=spec.name, severity=rt.level, opened_at=ts)
            log.emit(log.ALERT_RAISED, signal=spec.name, severity=rt.level.value)
            return
        rt.level_alert.count += 1
        if rank(rt.level) > rank(rt.level_alert.severity):
            rt.level_alert.severity = rt.level
            log.emit(log.ALERT_RAISED, signal=spec.name, severity=rt.level.value)
        else:
            rt.level_alert.severity = rt.level

    def _sync_stale_alert(
        self, spec: SignalSpec, rt: _Runtime, stale: bool, sev: Severity, now: float
    ) -> None:
        """Raise or clear the staleness alert on the read-time staleness verdict."""
        if stale and rt.stale_alert is None:
            rt.stale_alert = Alert(signal=spec.name, severity=sev, opened_at=now)
            log.emit(log.ALERT_RAISED, signal=spec.name, severity=sev.value)
        elif not stale and rt.stale_alert is not None:
            rt.stale_alert.cleared = True
            rt.stale_alert = None
            log.emit(log.ALERT_CLEARED, signal=spec.name)

    def state_at(self, now: float) -> list[SignalStatus]:
        """The per-signal view at `now` — staleness lazy, a stale value nulled."""
        out: list[SignalStatus] = []
        for spec in self.station.signals:
            rt = self._rt[spec.name]
            stale = self._is_stale(spec, rt, now)
            if stale:
                sev = Severity.CRITICAL if spec.safety_critical else Severity.WARNING
                self._sync_stale_alert(spec, rt, True, sev, now)
                out.append(
                    SignalStatus(spec.name, spec.unit, None, True, sev, _STALE_LABEL)
                )
            else:
                self._sync_stale_alert(spec, rt, False, Severity.NOMINAL, now)
                out.append(
                    SignalStatus(
                        spec.name,
                        spec.unit,
                        rt.last_value,
                        False,
                        rt.level,
                        rt.level.name,
                    )
                )
        return out

    def _is_stale(self, spec: SignalSpec, rt: _Runtime, now: float) -> bool:
        """Stale if past the TTL, or never reported (dead from boot); else never."""
        if spec.staleness is None:
            return False
        if rt.last_ts is None:
            return True
        return (now - rt.last_ts) > spec.staleness.ttl_seconds

    def active_alerts(self) -> list[Alert]:
        """Every currently-open alert, level or staleness."""
        alerts: list[Alert] = []
        for rt in self._rt.values():
            if rt.level_alert is not None:
                alerts.append(rt.level_alert)
            if rt.stale_alert is not None:
                alerts.append(rt.stale_alert)
        return alerts


def _candidate_level(rule: LevelRule, current: Severity, value: float) -> Severity:
    """Raw severity for a value, with the hysteresis band around the current level."""
    hyst = rule.hysteresis
    if rule.direction == "high":
        crit_on = rule.crit_at is not None and value >= rule.crit_at
        crit_hold = rule.crit_at is not None and value >= rule.crit_at - hyst
        warn_on = rule.warn_at is not None and value >= rule.warn_at
        warn_hold = rule.warn_at is not None and value >= rule.warn_at - hyst
    else:
        crit_on = rule.crit_at is not None and value <= rule.crit_at
        crit_hold = rule.crit_at is not None and value <= rule.crit_at + hyst
        warn_on = rule.warn_at is not None and value <= rule.warn_at
        warn_hold = rule.warn_at is not None and value <= rule.warn_at + hyst

    if current == Severity.CRITICAL:
        if crit_hold:
            return Severity.CRITICAL
        return Severity.WARNING if warn_hold else Severity.NOMINAL
    if current == Severity.WARNING:
        if crit_on:
            return Severity.CRITICAL
        return Severity.WARNING if warn_hold else Severity.NOMINAL
    if crit_on:
        return Severity.CRITICAL
    if warn_on:
        return Severity.WARNING
    return Severity.NOMINAL
