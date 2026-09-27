# Profile — `local-app` · Frame

Domain: a **local desktop application around a model pipeline**: a Python process on the user's
machine, a native window over a local page, one remote model API as the only network egress, local
models for everything that touches raw user data. Built [example #4](../../examples/praxis/).

## Sources *(must)*

| Source | Provides |
|---|---|
| The workflow doc (`docs/workflow.md` or equivalent) | the stage chain, what runs local vs remote, what each stage produces |
| The UI spec (`docs/ui.md`) | the screens, the controls, what is deliberately absent |
| The user's own artefacts (examples of the output they want) | the format the pipeline is held to; the first eval set |
| Existing evals (`evals/`, `explore/`) | measured baselines the build must not regress |
| A single-user interview *(brainstorm mode)* | the routine the app replaces, when no spec exists |

## Functional-analysis sections *(must)*
- **Required:** Identity · Actors (usually one) · Top-level workflows = *the stage chain per source type* ·
  **Data model** = *what is stored locally (traces, examples, mappings), and what never is (raw input)* ·
  Integrations = *the one remote API; the local models and where they live* · Functionalities ·
  **Boundary** = *what leaves the machine, redacted how, shown to the user where* · Metrics.
- **Optional (add only if they bite):** Out-of-scope · Packaging / install · Offline behaviour.

## Hard gates *(may)*
- **UI sketch** — the app is user-facing: no handoff to Plan without a reviewed `docs/ui-sketches.md`
  (or the `docs/ui.md` it derives from). Missing/unreviewed = 🔴 blocking.
- **Boundary stated** — every stage is labelled *local* or *remote*, and every remote call names the
  transform its input passed through (e.g. de-identification) and where the user sees that input
  before it goes. A remote call on unlabelled data = 🔴 blocking. This is the domain's core promise.

## `has_ui` *(must)*
true — a native window over a local page. The browser check drives it.

## `deploys` *(must)*
false — a single local process; no image, no server. The **smoke** check is the boot floor
(process starts, answers one probe on its internal bridge, stops). Packaging is a ticket, not a check.

## Grader bar *(must — consumed by `frame-completeness`)*
- **`verifiable_means`:** a stage can be **run on a synthetic input with a known answer key** and its
  output asserted — spans for de-identification, a schema for classification, a judge score for a
  draft, a leak count of zero for the boundary. A stage without a synthetic fixture cannot be graded.
- **`usual_silent_gaps`** — probe these; local-app briefs routinely omit them:
  - **first run** — models not yet downloaded; no examples yet; an empty state on every screen.
  - **the raw input's lifetime** — where it sits in memory and on disk before the gate runs, and when it is deleted (audio files, clipboard).
  - **the mapping's lifetime** — re-identification needs it; who can read it; when it is purged.
  - **memory** — local models coexist in RAM with each other and the OS; the sum, not each one.
  - **long inputs** — a 45-minute transcript against context windows and chunking.
  - **the API key** — where it lives, who set it, what happens when it is missing or the network is down.
  - **the user's edit as data** — what is stored from a review, and that it is redacted.
- **clean-handoff bar:** functional-analysis carries the stage chain with local/remote labels · the
  boundary section · the local data model with lifetimes · the UI spec reviewed · every stage has a
  named synthetic fixture; open-questions logs every biting assumption.
