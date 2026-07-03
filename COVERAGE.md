# Coverage — Böckeler's harness + Anthropic's agent patterns

A self-audit of this build. Each of Böckeler's guide + grader elements and Anthropic's **5 agent patterns** is (a) first-class machinery in the plugin and (b) exercised in at least one runnable example. ✅ = both true in this build.

> **Terminology:** Böckeler's diagram calls the feedback half **sensors**; pro-code calls them **graders** (its own term — "lead with the graders"). This is the one place the word "sensor" appears in that sense; everywhere else in the codebase the feedback half is a *grader*. (In the telemetry example, "sensor" also means a physical device — that's the domain, unrelated.)

- **#1** = [`examples/multi-tenant-isolation`](examples/multi-tenant-isolation/) (`generic-saas`, API) — 27 tests.
- **#2** = [`examples/edge-telemetry-alerting`](examples/edge-telemetry-alerting/) (`edge-telemetry`, UI) — 28 fixture-replay tests + 2 browser.

## Böckeler — Guides (feedforward)

| Sub-element | | Plugin machinery | Runs in |
|---|---|---|---|
| Principles | ✅ | `doc-patterns/guides/principles.md` | #1 `docs/principles.md`, #2 `docs/principles.md` |
| CfRs (the -ilities) | ✅ | `doc-patterns/guides/cfrs.md` (graded: a biting CfR needs a check) | #1/#2 `docs/cfrs.md` |
| Rules | ✅ | conventions in each `*-profile.md` | both |
| Ref Docs | ✅ | design catalog + living docs + specs | both |
| How-tos | ✅ | `skills/{frame,plan,implement,autopilot}` | both |
| Language Servers | ✅ | LSP named in `skills/implement`; type-check in the loop | #1 mypy/pyright, #2 mypy (`just typecheck`) |
| CLIs / scripts | ✅ | `doc-patterns/harness/justfile` | #1 `justfile`, #2 `justfile` (`just gate`) |
| **Code mods** | ✅ | `codemods/README.md` — auto-fix arm (stage 0 of the loop) | #1 `codemods/require_caller_dep.py` (libcst, idempotent) + `ruff --fix` both |

## Böckeler — Feedback (graders)

| Sub-element | | Plugin machinery | Runs in |
|---|---|---|---|
| Static analysis | ✅ | deterministic checks, in-gate — incl. the **doctrine linter** (`graders/checks/doctrine_lint.py`): comment doctrine + test-posture floor + domain `--forbid` special-lint | both — ruff + doctrine_lint (proven: it flags an assert-less test + a ticket-ref) |
| Review agents | ✅ | loop's ~3 fuzzy graders as **isolated sub-agents** (author ≠ grader) | #1 + #2 — isolated grader sub-agents, author ≠ grader |
| Logs | ✅ | `doc-patterns/harness/log-taxonomy.md` + logs grader in the loop | #1 `test_logs_grader.py` (`CROSS_TENANT_DENIED`), #2 `test_logs_grader.py` (`ALERT_RAISED{critical}`) |
| Browser | ✅ | `graders/browser-grader.md` (Playwright) | #2 `test_dashboard_browser.py` — real Chromium, asserts "— stale" render |

## Anthropic — the 5 patterns

| Pattern | | Where | Runs in |
|---|---|---|---|
| Prompt chaining | ✅ | the pipeline + Plan's spine | both |
| Routing | ✅ | hook-match + autonomy tiering; deterministic-first→fuzzy | both |
| Parallelization | ✅ | parallel workers per wave + parallel fuzzy graders + **N-vote** | #1 + #2 — parallel verification agents; a fresh adversarial refuter re-checked the core promise (author ≠ grader) |
| Orchestrator-workers | ✅ | `skills/autopilot/SKILL.md` — dispatch, route by tier, aggregate residual | #1 + #2 — backlogs are tiered + waved; 🔴 core-promise tickets human-owned by rule (the runner is specified in `skills/autopilot`) |
| Evaluator-optimizer | ✅ | the code-verification loop (the keystone) | both — 3 iterations, ~40→~70→~90 |

## What the adversarial verification checked

In **both** examples, the core promise was re-checked by a fresh adversarial refuter (author ≠ grader), independent of the author's own tests:

- **#1** — a refuter attacked tenant isolation across every verb, including a member cross-tenant delete (an existence oracle via RBAC ordering); the invariant **held**.
- **#2** — a refuter attacked no-missed-critical across held-value, dropped-sensor, and dead-from-boot cases; the invariant **held** (it surfaced one self-healing staleness transient, logged in `open-questions`).

That's the thesis: **the core promise is certified by a grader that didn't write the code**, not by author confidence.

## Opinionation — profiles are subsets, not mirrors

The plugin ships the whole menu; each **profile mandates a different opinionated subset**, and coverage holds because every element runs in *at least one* example (not both). The divergence *is* the opinion:

| Element | `generic-saas` (API) | `edge-telemetry` (UI) |
|---|---|---|
| Codemod | **mandates** (boundary-dep across handlers) | skips (drift-grader-caught) |
| Browser grader + e2e | n/a (API-only, no frontend) | **mandates** (has a dashboard) |
| Test posture | **integration test per endpoint** | **fixture-replay per rule** (fire + no-fire) |
| Special-lint | `no-print` (use LOG) · `no-bare-except` | `severity-constant` (no `"critical"` literal) |
| Catalog patterns | +`structured-error-envelope` · `write-through-audit-log` | +`named-severity-constant` · `config-driven-thresholds` |

Shared where genuinely universal (comment doctrine, the test-posture floor: every test asserts, no silent skip).

## The seam still holds

Exercising each element did **not** cost the guide/grader separation. The six agnostic files under `skills/` + `graders/` (now seven with `autopilot` and the two extra graders) are shared by both domains; everything domain-specific — catalog, conventions, CfRs, log codes, the visual invariant, the codemod — lives in the swapped `profiles/<domain>/` and the example. Adding the second domain still touched **zero** skill/grader internals beyond the shared machinery.
