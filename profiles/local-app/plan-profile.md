---
consumed_by: [plan, grader:plan, build, grader:drift, grader:simplicity]
canonical_for: `local-app` design catalog and tiering signals
profile: local-app
---

# Profile — `local-app` · Plan

Domain: a local desktop application around a model pipeline. Pairs with `frame-profile.md`. Consumed
by the unchanged `skills/plan` + `graders/plan-completeness`.

## Surface = a screen or a stage

A "surface" is either a **screen** the user passes through (per `docs/ui.md`) or a **stage** of the
chain (per `docs/workflow.md`). Per-surface spec = one `docs/surfaces/<name>.md` per screen and per
stage that has a contract worth writing down (input, output, local/remote, fixture).

## Design catalog *(must)*

The shapes Plan routes tickets against. Route ≤ 3–5 per ticket; no match → `novel — author fresh`.

| Shape | When it applies |
|---|---|
| `gate-before-egress` | any data leaving the machine passes one transform first, and the user sees the transformed text before it goes; the reverse transform runs locally on the way back |
| `stage-function` | a pipeline stage is one function `(input, config) → output`, no state, so it can be run on a fixture and replaced |
| `synthetic-fixture-with-key` | a stage's test input is generated with its answer attached (spans, labels, the expected structure); the eval is exact, and no real data exists in the repo |
| `judge-with-evidence` | a model grades a draft against a written rubric with the cited sources injected; scores per criterion with a reason; calibrated once against a human |
| `trace-not-log` | every run writes its redacted input, each stage's output, and the user's decisions to a local folder; that folder is the eval set and the audit trail; raw input is never written |
| `examples-as-template` | the format of an output type is the user's signed outputs of that type (last N) plus their standing plain-language sentences; there is no template artefact to edit |
| `single-call-per-stage` | the remote model is called once per stage with a cached system prefix; loops are the exception and are traced turn by turn |
| `local-model-in-cache` | downloaded models live in the framework's shared cache (HF, Ollama); project-trained ones under `data/models/`; the code names the model id, never the path |
| `first-run-fetch` | models absent on first launch are fetched then, with progress shown; the app is usable offline afterwards for every local stage |
| `no-options-surface` | a screen has one action and no settings; anything configurable lives in a config file set at install |

## Out of scope — not ticketed

Accounts, hosting, multi-user, sync. A dashboard over the trace. Real user data in the repo or the
evals.

## Tiering signals *(must)*

- **proven pattern** — a catalog shape applies.
- **verifiable without the user** — the stage runs on a synthetic fixture with an answer key; the
  screen can be driven by the browser check. *(A screen's "usable without instructions" is not
  verifiable this way — that ticket is 🟡 by construction.)*
- **risk boundary** — anything that changes **what leaves the machine** or **what is written to disk
  from raw input**: the gate, the mapping store, the trace writer, the API call site. A change there
  is 🔴 until its leak test runs green with fresh output.
- **out-of-repo dependency** — a model download that does not exist yet, a signing certificate, the
  user's own artefact (their first example), the user's presence.
- **spec-complete** — stage contract + fixture named + local/remote label + a screen in the UI spec if
  user-facing.

→ all-pass 🟢 · any-miss 🟡 · **boundary change without a leak test, or out-of-repo dependency 🔴**.

## Grader bar (consumed by `plan-completeness`)

- **`coverage_means`** — every stage in the workflow doc maps to ≥ 1 ticket; every screen in the UI
  spec maps to ≥ 1 ticket; the boundary section maps to a leak-test ticket.
- **`verifiable_means`** — a synthetic fixture with an answer key, named in the ticket, and an assertion
  on it: "de-id recall on fixture X ≥ 0.99 and 0 spans in the redacted text" passes; "redacts well"
  fails. For drafts: a judge score with a threshold and the rubric named. For screens: a browser
  check assertion on the rendered DOM.
- **well-formed bar:** each ticket carries a fixture-backed acceptance criterion + a catalog hook (or
  explicit `novel`) + a local/remote label + wired `depends-on`; the backlog carries a cycle-free
  build order with the critical path called out.
