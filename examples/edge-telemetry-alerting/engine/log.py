"""Structured event log — the trace the logs grader reads to prove an alert fired.

A raised alert is proven from the ``ALERT_RAISED{severity:critical}`` event, not from the
return value or active-alert list — no-missed-critical, proven from the trace.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any

ALERT_RAISED = "ALERT_RAISED"
ALERT_CLEARED = "ALERT_CLEARED"


@dataclass
class _EventLog:
    records: list[dict[str, Any]] = field(default_factory=list)

    def event(self, code: str, level: str, **fields: Any) -> None:
        record = {"code": code, "level": level, **fields}
        self.records.append(record)
        print(json.dumps(record), file=sys.stderr)  # doctrine: allow — the LOG sink

    def clear(self) -> None:
        self.records.clear()

    def with_code(self, code: str) -> list[dict[str, Any]]:
        return [r for r in self.records if r["code"] == code]


LOG = _EventLog()
