"""Test harness — fixture paths, a fresh log per test, and a station loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from engine import log
from engine.config import load_station
from engine.replay import replay

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


@pytest.fixture(autouse=True)
def _clean_log() -> None:
    """Isolate each test's captured trace."""
    log.reset()


@pytest.fixture
def station():
    """The default station, loaded fresh."""
    return load_station()


def replay_fixture(name: str):
    """Replay a named fixture through a fresh monitor and return it."""
    return replay(FIXTURES / f"{name}.jsonl")


def raised(severity: str) -> list[dict]:
    """The ALERT_RAISED events of a given severity in the current trace."""
    return [
        e
        for e in log.events()
        if e["code"] == log.ALERT_RAISED and e["severity"] == severity
    ]
