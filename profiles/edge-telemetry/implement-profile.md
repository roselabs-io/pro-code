# Profile — `edge-telemetry` · Implement

Domain: industrial edge telemetry monitoring + alerting. Completes the trio. Consumed by the unchanged `skills/implement` + `graders/code-verification-loop`.

The hard-done requirement — **no missed critical alert** — is proven the way isolation was in `generic-saas`: by replaying recorded fixtures and asserting the exact alert output. The grader, not confidence, certifies it.

> **This profile mandates** (its opinionated subset — deliberately *different* from generic-saas): the **browser grader** + an **e2e test** (it has a dashboard), **fixture-replay per rule** (fire + no-fire), the **logs grader**, and the `severity-constant` special-lint.
> **It skips**: the **codemod** (this domain's drift is caught by the drift grader, not bulk transforms — so no `codemods/` here), and the `no-print` lint (the engine has no request handlers to police).

## Stack + layout

- **Framework:** a pure-Python rule engine + a **FastAPI** dashboard (a `/state` JSON endpoint + a served static HTML/JS view); served with `uvicorn`.
- **Env / runner:** **uv** (`uv sync`) + a `justfile` (`just gate`) whose recipes call `uv run`.
- **Python:** ≥ 3.12.
- **Layout:** `engine/` (the rules), `dashboard/` (the served view), `tests/`, `fixtures/` (recorded telemetry); docs in `docs/`.
- **Lint / format:** `ruff` — `line-length = 90`, rules `E, F, I, B`.
- **Tests:** `pytest` with a `browser` marker — `-m "not browser"` for fixture-replay, `-m browser` for the Playwright e2e. Playwright needs a one-time `playwright install chromium`.

> These are the profile's **declared choice-points** — fixed here so they're not silent. Any build choice *not* covered here (or by the Conventions below) goes in `docs/assumptions.md` with a disposition, so a default the agent reached for is visible, not buried.

## Deterministic checks (run first, they short-circuit)

| Check | Command | Rule |
|---|---|---|
| lint | `ruff check engine dashboard tests` | no lint errors |
| tests | `pytest -m "not browser"` (fixture-replay) + `pytest -m browser` (e2e) | zero failures, **this session** |
| comment-doctrine | `doctrine_lint.py engine dashboard tests` | comment doctrine + test-posture floor |
| special-lint | `doctrine_lint.py engine --forbid '"(critical\|warning)"@@use Severity.*'` | domain forbid: severities are enum constants, not string literals |

> **Not gate steps here:** a reading is validated at ingest (`parse_line` rejects a malformed line), so there's no separate schema-validation command. **Type-check** (`mypy engine/`) is run as an author-aid, advisory — not in the gate for this slice.

## Fuzzy rubrics (~3 focused graders — what each points at)

- **feature / spec** → the ticket's alert condition. Does the rule fire on the fire-fixture and stay silent on the no-fire fixture — exactly, at the right time and severity?
- **pattern / drift** → the design catalog (`plan-profile.md`) hooks + the conventions below. Was `staleness-watchdog` applied to every critical signal? Does every threshold carry hysteresis?
- **docs-currency** → the living-docs set below.

## Full-coverage machinery (guides + graders this profile wires)

- **LSP (guide):** `mypy engine/` — types/refs while authoring. Advisory, not a gate step in this slice.
- **Environment + CLIs (guide):** **uv** for deps/venv (`uv sync`) + a `justfile` runner (`just gate`) whose recipes call `uv run`. Template: `doc-patterns/harness/justfile`. *(The env tool and runner are a profile choice: this profile picks uv + a justfile; `generic-saas` picks poetry + no justfile.)*
- **Codemods (auto-fix arm):** codemod-lite = `ruff check --fix . && ruff format .` every gate. (A semantic codemod is optional here; the domain's drift is caught more by the drift grader than by bulk transforms.)
- **Logs grader:** structured events per `doc-patterns/harness/log-taxonomy.md` — `ALERT_RAISED{signal,severity}`, `ALERT_CLEARED`. The grader replays a breach fixture and asserts `ALERT_RAISED{severity:critical}` fired (the *no-missed-critical* promise proven from the trace, not just the active-alert list).
- **Browser grader (LIVE here):** `has_ui: true`. Playwright drives the running dashboard; **`visual_invariant`: a stale signal renders "— stale", never a number, and a CRITICAL row renders red.** The only grader that catches a template rendering last-good over a stale flag while every API test stays green.

## Doctrines this profile mandates

- **Comment doctrine** (`doc-patterns/doctrines/comment-doctrine.md`) — shared/universal, enforced by `doctrine_lint.py` + the fuzzy drift grader. `doctrine: allow` exempts the `Severity` enum definition (the one place the strings live).
- **README doctrine** (`doc-patterns/doctrines/readme-doctrine.md`) — shared/universal. The service README carries a "Run it" section: set up the env (`uv sync`), run `just gate`, launch (`just demo`). Checked by the docs-currency grader.
- **Test posture** (`doc-patterns/doctrines/test-posture.md`) — this domain's opinion:
  - **Fixture-replay per rule** — every alert rule owes a **fire** fixture and a **no-fire** fixture; a never-firing rule passes a no-alert-only test trivially.
  - **An e2e test, because there is a frontend** — the browser grader drives the running dashboard and asserts the visual invariant. A UI-bearing profile *owes* this layer.
  - Plus the floor: every test asserts; no silent skip; red-green on a fix.

## Special-lint (the domain forbids — `doctrine_lint.py --forbid`)

- **no severity string literal** — `Severity.CRITICAL`, never `"critical"` (the `named-severity-constant` pattern, mechanically enforced). The enum definition is `doctrine: allow`.
- *(no `no-print` rule — the engine has no request handlers; that's the SaaS profile's opinion.)*

## Conventions (the drift grader's rubric)

- **Missing data is an alert, never nominal** — every safety-critical signal has a `staleness-watchdog`; a gap must fire, not read as "fine."
- **No bare thresholds** — every level rule carries hysteresis (fire at X, clear at X−h); a raw `>` that can flap is a finding.
- **Severities are named constants** — `Severity.CRITICAL`, not the string `"critical"` or a magic number.
- **Alerts are deduped** — a burst of one condition is one active alert with a count, not N.
- **Timestamps are explicit and out-of-order-tolerant** — a late earlier sample must not resurrect a cleared alert.
- **Comment doctrine** — state what the code *is*; why-not / history / ticket-ref belongs in the commit.

## verify_means + false-green traps

- **verify_means:** a fixture-replay test asserts the alert output — **both** a fire case and a no-fire case — with fresh output this session. A rule is "done" only when a recorded stream proves it fires *and* proves it stays quiet.
- **false-green traps** (the monitoring-specific lies a passing test can hide):
  - **a rule that never fires** — passes a no-alert-only test trivially. Every rule needs BOTH a fire fixture and a no-fire fixture, or the test proves nothing.
  - **missing data read as 0 / nominal** — the staleness trap: test an actual gap in the stream, not just in-range values.
  - **the fixture never actually breached** — assert the input genuinely crosses the threshold; a fire-test over non-breaching data is green and worthless.
  - **flapping miscounted** — feed a value oscillating across the line and assert **one** active alert (dedup + hysteresis), not N and not zero.
  - **out-of-order resurrection** — replay a late-arriving earlier sample after a clear and assert the alert stays cleared.

## Living docs (the docs-currency grader's set)

Kept current every ticket — the second artifact:
- `docs/backlog.md` — forward-only.
- `docs/current-state.md` — what's built now.
- `docs/open-questions.md` — resolved flipped to `[decided]`; new assumptions `[open]`.
- `docs/decisions/NNNN-*.md` — a record per non-obvious call (template: `doc-patterns/living-docs/decision-record.md`).
- `docs/surfaces/<view>.md` + `docs/ui-sketches.md` — updated if reality diverged.
- `docs/assumptions.md` — the choices the build made that no input specified, each with a disposition (template: `doc-patterns/living-docs/assumptions.md`).
