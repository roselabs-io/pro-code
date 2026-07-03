# Profile — `generic-saas` · Implement

Domain: a CRUD SaaS backend — **Python + FastAPI, API-only**. The **default** profile. Completes the trio with `frame-profile.md` and `plan-profile.md`.

This is the domain where **both** guides *and* graders are deterministic — schema-as-code → CRUD → validate — so it's the cleanest possible showcase for the code-verification loop.

> **This profile mandates** (its opinionated subset of the menu): a **codemod** (boundary-dependency enforcement across handlers), the **logs grader**, an **integration test per endpoint**, and the `no-print` / `no-bare-except` special-lint.
> **It skips**: the **browser grader** + **e2e** (API-only, `has_ui` false → declared n/a), and the `config-driven-thresholds` / `severity-constant` lints (that's the telemetry profile's opinion, not this one).

## Stack + layout

- **Framework:** Python + **FastAPI** (ASGI); served with `uvicorn`.
- **Env / runner:** **poetry** (`poetry install`); no task-runner — the graders run via `poetry run`.
- **Python:** ≥ 3.12.
- **Layout:** `app/` (the service), `tests/`, `codemods/`; docs in `docs/`.
- **Lint / format:** `ruff` — `line-length = 90`, rules `E, F, I, B`.
- **Tests:** `pytest` (`pythonpath = ["."]`, `testpaths = ["tests"]`), driven through FastAPI's `TestClient`.
- **Auth (when present):** a signed bearer token resolved to a `Caller`. The token library + signing algorithm are a **build choice** — the assumptions ledger surfaces them.

> These are the profile's **declared choice-points** — fixed here so they're not silent. Any build choice *not* covered here (or by the Conventions below) goes in `docs/assumptions.md` with a disposition, so a default the agent reached for is visible, not buried.

## Deterministic checks (run first, they short-circuit)

The mechanical graders — commands, not LLM judges. As many as there are mechanical rules.

| Check | Command | Rule |
|---|---|---|
| lint | `ruff check app tests codemods` | no lint errors |
| tests | `pytest` | zero failures, **this session** |
| comment-doctrine | `doctrine_lint.py app tests` | the regex-able subset of the comment doctrine + test-posture floor |
| special-lint | `doctrine_lint.py app --forbid 'print\(@@use LOG' --forbid 'except\s*:@@no bare except'` | domain forbids: no `print` in app code, no bare `except` |
| codemod-check | `codemods/require_caller_dep.py --check app/main.py` | every route carries the boundary dependency |

> **Not gate steps here:** request/response shape is enforced at runtime by the **pydantic** models (a bad body → 422; the integration tests assert it), so there's no separate schema-validation command. **Type-check** (`mypy app/`) is run as an author-aid, advisory — not in the gate for this slice.

## Fuzzy rubrics (~3 focused graders — what each points at)

- **feature / spec** → the ticket's acceptance criterion. Does the diff satisfy the assertion, not a proxy?
- **pattern / drift** → the design catalog (`plan-profile.md`) hooks on the ticket + the conventions below. Was every hook applied where the shape says (e.g. `tenant-scoped-query-guard` on **every** verb, deny-by-default)?
- **docs-currency** → the living-docs set below. Backlog pruned + forward-only, current-state fresh, a decision record for any new decision, open-questions flipped.

## Full-coverage machinery (guides + graders this profile wires)

- **LSP (guide):** `mypy` / `pyright` (Python) — consult types/refs while authoring. Advisory (`mypy app/`), not a gate step in this slice.
- **Environment + CLIs (guide):** **poetry** for deps/venv (`poetry install`). No task-runner in this profile — the graders run directly via `poetry run` (the example README lists them). *(The env tool and whether to ship a `justfile` are a profile choice: this profile picks poetry + no justfile; `edge-telemetry` picks uv + a justfile.)*
- **Codemods (auto-fix arm):** codemod-lite = `ruff check --fix . && ruff format .` every gate; one genuine **libcst** codemod per build enforcing a boundary convention across handlers (e.g. every route depends on `get_caller`). See the example's `codemods/`.
- **Logs grader:** structured events per `doc-patterns/harness/log-taxonomy.md` — `HANDLER_RAN`, `CROSS_TENANT_DENIED{workspace,target}`. The grader asserts `CROSS_TENANT_DENIED` fired on a cross-tenant attempt (isolation proven from the *trace*, not the 404 alone).
- **Browser grader:** n/a — this profile is API-only (`has_ui: false`), no rendered surface.

## Doctrines this profile mandates

- **Comment doctrine** (`doc-patterns/doctrines/comment-doctrine.md`) — shared/universal. Enforced by `doctrine_lint.py` (regex-able subset) + the fuzzy drift grader (judgment cases). `doctrine: allow` exempts the rare legit line (the LOG module's own `print`).
- **README doctrine** (`doc-patterns/doctrines/readme-doctrine.md`) — shared/universal. The service README carries a "Run it" section: set up the env (`poetry install`), run the graders, launch. Checked by the docs-currency grader.
- **Test posture** (`doc-patterns/doctrines/test-posture.md`) — this domain's opinion:
  - **An integration test per endpoint** — every route gets a test that drives the *real* request through the app (`TestClient`) and asserts the **effect** (a row changed, a field serialized), not the status.
  - **No e2e** — API-only slice, no frontend, so no browser/e2e layer is owed. Declared, not skipped.
  - Plus the floor: every test asserts; no silent skip; red-green on a fix.

## Special-lint (the domain forbids — `doctrine_lint.py --forbid`)

- **no `print(` in app code** — use the structured `LOG` event log (the logs grader reads it). The log module itself is `doctrine: allow`.
- **no bare `except:`** — catch a specific type.

## Conventions (the drift grader's rubric)

- **Enforce at the boundary, not the UI** — authz/isolation checks live server-side; the client is convenience only.
- **No magic numbers** — limits/TTLs/page-sizes are named config, not literals.
- **Errors are typed + tiered** — a permission-denied returns the agreed status (404 for cross-tenant, not 403 that leaks existence); no bare 500s for expected failures.
- **Tests live with the ticket** — not "later."
- **Comment doctrine** — state what the code *is*; the why-not / history / ticket-ref belongs in the commit, never inline.

## verify_means + false-green traps

- **verify_means:** an automated test asserts the criterion against the dev stack or a mock, with fresh output this session — a test, not a person, confirms it.
- **false-green traps** (the `check-passes-but-behaviour-is-broken` class — the fuzzy feature grader must probe past the status code):
  - **`200 ≠ the handler ran`** — a wrapper can return 200 while the inner logic 422'd or was skipped. Assert the *effect* (a row changed, a field serialized), not just the status.
  - **serialization omits a falsy field** — a `false`/`0`/`""` silently dropped from the response looks like "not returned." Assert the field's presence, not just truthiness.
  - **mock-green ≠ real-green** — a mocked dependency that always says yes hides the integration bug. The isolation test must hit the real query path.
  - **no red-green on a fix** — a regression test that was never seen to *fail first* proves nothing. Confirm it goes red without the fix.

## Living docs (the docs-currency grader's set)

Kept current every ticket — the second artifact:
- `docs/backlog.md` — forward-only (shipped rows deleted; new work added).
- `docs/current-state.md` — what's built now.
- `docs/open-questions.md` — resolved flipped to `[decided]`; new assumptions `[open]`.
- `docs/decisions/NNNN-*.md` — a record per non-obvious call (template: `doc-patterns/living-docs/decision-record.md`).
- `docs/surfaces/<name>.md` — updated if reality diverged from Plan's sketch.
- `docs/assumptions.md` — the choices the build made that no input specified, each with a disposition (template: `doc-patterns/living-docs/assumptions.md`).

