# Profile — `local-app` · Implement

Domain: a local desktop application around a model pipeline. Consumed by the unchanged
`skills/implement` + `skills/review-gate`.

The hard-done requirement — **nothing of the user's leaves the machine unredacted, and every stage is
measured on a synthetic fixture** — is proven by the leak test and the stage evals, not by the
author's confidence.

> **This profile mandates:** the **leak test** on every ticket that touches the boundary, **fixture
> evals** per stage, the **trace** as the log, the **smoke** check as the boot floor, and the **browser
> check** on any screen ticket. **It skips:** infra (`deploys: false`), codemods (drift is caught by
> the drift grader), and the no-print lint (no request handlers).

## Stack + layout

- **Language:** Python ≥ 3.12; **env / runner:** `uv` + a `justfile` whose recipes call `uv run`.
- **Pipeline:** a package of stage functions (`src/<app>/chain/`), one module per stage; one module
  is the only place the remote model is called.
- **Local models:** Hugging Face cache for downloaded encoders/NER; Ollama or mlx for local LLMs when
  used; project-trained checkpoints under `data/models/` (untracked).
- **UI:** a native window over a local HTML page (`pywebview`); the page calls Python through the
  bridge, no HTTP server, no port.
- **Storage:** `~/.<app>/` — `runs/` (traces), `mappings/`, `examples/<kind>/`, `rules/<kind>.md`,
  `config` (API key, model ids). Raw input is never written.
- **Lint / format:** `ruff` — `line-length = 120`, rules `E, F, I, B`.
- **Tests:** `pytest`; markers `browser` (drives the window), `slow` (loads a model), `api` (calls the
  remote model; skipped without a key).

> These are the profile's **declared choice-points**. Any build choice not covered here or by the
> Conventions goes in `docs/assumptions.md` with a disposition.

## Checks

Commands live in [`check-commands.md`](check-commands.md). This profile **runs**: lint · tests ·
type-check (advisory) · doctrine-lint · security · coverage · deps · logs (the trace) · smoke · browser.
It declares schema-validation, codemod and infra *n/a* — see `check-commands.md`.

## Rubrics *(must — ~4 focused graders)*
- **feature / spec** → the ticket's fixture assertion: does the stage produce the asserted output on
  the named synthetic fixture, with fresh output this session?
- **pattern / drift** → the design catalog hooks + the conventions below. Was `gate-before-egress`
  applied to the new call site? Is raw input written anywhere? Is a model referenced by path?
- **docs-currency** → the living-docs set below.
- **simplicity** → the ticket's criterion + hooks + the Stack choice-points. Always in scope: the
  fixture and its assertion. A stage that grew a config surface the UI spec forbids is a finding.
- **boundary** *(domain grader unit, `graders/boundary.md`)* → on any diff touching the gate, the
  mapping store, the trace writer or the API call site: the leak test is present, ran, and reports
  zero; no new write of raw input; no new egress.

## verify_means + false_green_traps *(must)*
- **verify_means:** a stage test runs on a synthetic fixture with an answer key and asserts the
  output; a boundary test asserts zero answer-key spans in every outgoing request and every file
  written; a screen test drives the window and asserts the DOM. All with fresh output this session.
- **false_green_traps:**
  - **the checkpoint that trains is not the checkpoint that loads** — a saved model with wrong key
    names loads as random weights and every downstream test "passes" on garbage. Load-and-predict
    on a fixture after every save.
  - **the eval set generated the rule** — a regex written from the filler's formats scores 1.0 on the
    filler's output; say so, and keep a harder fixture.
  - **redacted in the UI, raw in the request** — the screen shows placeholders while the API call
    reads the original variable. The leak test reads the request, not the screen.
  - **the trace wrote the raw text** — a debug field, a `repr`, an exception message carrying the
    input. Grep the trace folder for answer-key spans.
  - **thinking counts against `max_tokens`** — a structured call returns `None` and the caller
    proceeds. A `None` parse is a failure, never scored.
  - **cache hit measured on the wrong field** — `input_tokens` excludes cached tokens; cost and hit
    rate computed from it are wrong.
  - **the judge grading its own family** — same-model judge scores are relative; a change is real
    only outside the measured noise floor.
  - **a screen that passes the browser check and needs a tutorial** — the check asserts the DOM;
    "usable without instructions" needs a person, and the ticket says so (🟡).

## Conventions / forbids *(may — the drift grader's rubric)*
- **One egress.** The remote model is called from one module; every call site outside it is a
  finding. Forbid: `Anthropic(` outside `chain/llm.py`.
- **Raw input is a variable, never a file.** No write of the un-redacted text; the trace holds the
  redacted text and the mapping holds the values, in separate files.
- **Models by id.** `from_pretrained("<org>/<name>")` or an Ollama tag; a filesystem path only for
  `data/models/`.
- **A placeholder is preserved end to end.** Every `[TYPE_n]` in a draft exists in its input; a
  draft that invents one is a finding (the distillation artefact).
- **Structured output or no output.** A model call that expects JSON uses the schema-constrained
  path and treats a non-`end_turn` stop as an error.
- **Comment doctrine** — shared.

## Codemods *(may)*
none — `ruff --fix` + `ruff format` as codemod-lite every gate.

## Doctrines *(may)*
- **Comment doctrine**, **README doctrine** (the README carries "Run it": `uv sync`, `just gate`,
  `just app`), **test posture** — this domain's opinion: every stage owes a fixture test with an
  answer key; every boundary change owes a leak test; every screen owes a browser test.

## Living docs *(must — the docs-currency grader's set)*
- `docs/planning/backlog.md` — forward-only.
- `docs/planning/current-state.md` — what's built now.
- `docs/planning/open-questions.md`.
- `docs/decisions/NNNN-*.md`.
- `docs/workflow.md`, `docs/ui.md`, `docs/surfaces/<name>.md` — updated if reality diverged.
- `docs/assumptions.md`.
- `README.md` — the measured numbers per stage stay current with the evals.
