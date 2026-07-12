"""Browser grader — the visual invariant on the RUNNING dashboard.

Playwright drives the live view and asserts the DOM: a stale signal shows '— stale'
(never a number), a CRITICAL row renders red AND carries a text label (not colour-only).
Marked `browser` so the deterministic gate skips it; run with `-m browser`
after `playwright install chromium`.
"""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from collections.abc import Iterator

import httpx
import pytest

pytest.importorskip(
    "playwright", reason="playwright not installed — run -m browser after install"
)
from playwright.sync_api import sync_playwright  # noqa: E402

pytestmark = pytest.mark.browser


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def server() -> Iterator[str]:
    """Launch the real dashboard with uvicorn and yield its base URL."""
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "dashboard.app:app", "--port", str(port)],
    )
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(50):
            try:
                if httpx.get(f"{base}/state", timeout=0.5).status_code == 200:
                    break
            except httpx.HTTPError:
                time.sleep(0.1)
        yield base
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_stale_row_renders_stale_and_critical_renders_red(server: str) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(server)
        page.wait_for_selector("#rows tr td")

        # The stale signal renders '— stale', never its last-good number.
        flow_value = page.locator("#rows tr", has_text="flow_rate").locator("td").nth(1)
        assert flow_value.inner_text().strip() == "— stale"

        # The critical row renders red AND carries a text label (not colour-only).
        pressure_status = page.locator("#rows tr", has_text="discharge_pressure").locator(
            'td[data-severity="critical"]'
        )
        assert pressure_status.count() == 1
        colour = pressure_status.evaluate("el => getComputedStyle(el).color")
        assert colour == "rgb(248, 81, 73)", "critical status must render red"
        assert pressure_status.inner_text().strip() != "", "status carries a text label"
        browser.close()
