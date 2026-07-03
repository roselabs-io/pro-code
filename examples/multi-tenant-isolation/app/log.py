"""Structured event log — the trace the logs grader reads to prove a handler actually ran.

Every behaviour that matters emits one structured event with a stable ``code``, a level
and fields (``doc-patterns/harness/log-taxonomy.md``). Events go to stderr as JSON and are
appended to an in-process buffer a test can assert on — "200 ≠ the handler ran", so the
grader checks the trace, not the return value.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any

# Stable event codes — a change here is a change to the grader contract.
PROJECT_CREATED = "PROJECT_CREATED"
PROJECT_UPDATED = "PROJECT_UPDATED"
PROJECT_DELETED = "PROJECT_DELETED"
CROSS_TENANT_DENIED = "CROSS_TENANT_DENIED"
RBAC_DENIED = "RBAC_DENIED"


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
