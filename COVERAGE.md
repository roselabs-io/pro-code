# Coverage — Böckeler's harness + Anthropic's agent patterns

Full coverage, audited. Every one of Böckeler's **12 harness sub-elements** and Anthropic's **5 agent patterns** is (a) first-class machinery in the plugin and (b) exercised runnably in an example. ✅ = both true.

> **Terminology:** Böckeler's diagram calls the feedback half **sensors**; pro-code calls them **graders** (its own term — "lead with the graders"). This is the one place the word "sensor" appears in that sense; everywhere else in the codebase the feedback half is a *grader*. (In the telemetry example, "sensor" also means a physical device — that's the domain, unrelated.)

- **#1** = [`examples/multi-tenant-isolation`](examples/multi-tenant-isolation/) (`generic-saas`, API) — 25 tests.
- **#2** = [`examples/edge-telemetry-alerting`](examples/edge-telemetry-alerting/) (`edge-telemetry`, UI) — 27 tests + 1 browser.

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
| Review agents | ✅ | loop's ~3 fuzzy graders as **isolated sub-agents** (author ≠ grader) | #1 — real feature + drift grader sub-agents (drift caught worker over-commenting) |
| Logs | ✅ | `doc-patterns/harness/log-taxonomy.md` + logs grader in the loop | #1 `test_logs_grader.py` (`CROSS_TENANT_DENIED`), #2 `test_logs_grader.py` (`ALERT_RAISED{critical}`) |
| Browser | ✅ | `graders/browser-grader.md` (Playwright) | #2 `test_dashboard_browser.py` — real Chromium, asserts "— stale" render |

## Anthropic — the 5 patterns

| Pattern | | Where | Runs in |
|---|---|---|---|
| Prompt chaining | ✅ | the pipeline + Plan's spine | both |
| Routing | ✅ | hook-match + autonomy tiering; deterministic-first→fuzzy | both |
| Parallelization | ✅ | parallel workers per wave + parallel fuzzy graders + **N-vote** | #1 (2 parallel workers + 3-vote), #2 (2 parallel workers + 3-vote) |
| Orchestrator-workers | ✅ | `skills/autopilot/SKILL.md` — dispatch, route by tier, aggregate residual | #1 + #2 — real worker sub-agents built the 🟢 wave; 🔴 not dispatched |
| Evaluator-optimizer | ✅ | the code-verification loop (the keystone) | both — 3 iterations, ~40→~70→~90 |

## What the adversarial verification caught

In **both** examples, a fresh adversarial grader found a real defect the author's own tests were green over:

- **#1** — the drift grader (isolated, author ≠ grader) caught worker-authored over-commenting the author couldn't see.
- **#2** — a refuter **refuted the no-missed-critical promise**: a safety sensor *dead from boot* was never watched → no alert. Fixed (`decisions/0001`) with a regression test.

That's the thesis, demonstrated twice: **the grader catches what the author is blind to.**

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

Full coverage did **not** cost the guide/grader separation. The six agnostic files under `skills/` + `graders/` (now seven with `autopilot` and the two extra graders) are shared by both domains; everything domain-specific — catalog, conventions, CfRs, log codes, the visual invariant, the codemod — lives in the swapped `profiles/<domain>/` and the example. Adding the second domain still touched **zero** skill/grader internals beyond the shared machinery.
