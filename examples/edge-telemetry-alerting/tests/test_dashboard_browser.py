"""Browser grader (Playwright) — the only grader that sees what the operator sees.

Drives the *running* dashboard in Chromium and asserts the rendered DOM, not the /state
response. The visual invariant: **a stale signal renders "— stale", never a number, and a
CRITICAL row renders red.** A template printing the last-good number over a stale flag
would pass every API test and fail only here.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.request
from collections.abc import Iterator
from pathlib import Path

import pytest

pytest.importorskip("playwright.sync_api", reason="playwright not installed")
from playwright.sync_api import sync_playwright  # noqa: E402

EXAMPLE_ROOT = Path(__file__).resolve().parents[1]


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="module")
def dashboard_url() -> Iterator[str]:
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "dashboard.app:app", "--port", str(port)],
        cwd=EXAMPLE_ROOT,
        env={**os.environ, "DASHBOARD_SEED": "browser"},
    )
    url = f"http://127.0.0.1:{port}"
    try:
        _wait_for(url + "/state")
        yield url
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def _wait_for(url: str) -> None:
    for _ in range(60):
        try:
            urllib.request.urlopen(url, timeout=0.5)
            return
        except OSError:
            time.sleep(0.25)
    raise RuntimeError(f"server at {url} did not come up")


@pytest.mark.browser
def test_stale_row_renders_the_label_not_a_number(dashboard_url: str) -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(dashboard_url)
        row = page.locator("tr[data-signal='bearing_temperature']")
        # Wait for the JS poll to populate the stale row.
        page.wait_for_function(
            "() => document.querySelector(\"tr[data-signal='bearing_temperature'] "
            ".reading\")?.textContent.toLowerCase().includes('stale')"
        )
        reading = row.locator(".reading").inner_text()
        assert "stale" in reading.lower()  # the invariant: a label, ...
        assert not any(ch.isdigit() for ch in reading)  # ... never a number
        assert "critical" in (
            row.get_attribute("class") or ""
        )  # dead safety sensor is red
        browser.close()


@pytest.mark.browser
def test_critical_breach_row_renders_red_with_a_value(dashboard_url: str) -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(dashboard_url)
        row = page.locator("tr[data-signal='discharge_pressure']")
        page.wait_for_function(
            "() => (document.querySelector(\"tr[data-signal='discharge_pressure']\")"
            "?.className || '').includes('critical')"
        )
        assert "critical" in (row.get_attribute("class") or "")
        reading = row.locator(".reading").inner_text()
        assert "stale" not in reading.lower()
        assert any(ch.isdigit() for ch in reading)  # a live breach shows its number
        browser.close()
