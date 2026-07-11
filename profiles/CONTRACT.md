# Profile contract — the hook interface a profile supplies

A **profile** is the domain overlay: the pipeline ships agnostic phase skills + graders + neutral guide
skeletons; a profile fills the *content* for one domain. Swap the profile, retarget the whole pipeline
([README](README.md)). This file is the **exhaustive must/may list** a profile supplies — the seam every
skill and grader reads. It makes "same hook shape, different content per domain" a checkable contract.

> **Status.** The **domain**-profile hooks below are proven — `generic-saas` and `edge-telemetry` both
> fill them and run through the same skills + graders byte-for-byte (n=2). The **personal**-overlay kind
> and the **grader-extension** interface are newer (v1); expect them to firm up as they're exercised.

## Two kinds of profile

| Kind | Differs by | Lives in | Supplies |
|---|---|---|---|
| **Domain** | *what* you build (`generic-saas`, `edge-telemetry`, …) | `profiles/<domain>/` | the **full** hook set below |
| **Personal** | *who* reviews (a person's taste) | `profiles/personal/<name>/` | a **lean overlay** — extra rubric rows, extra graders, extra forbids only |

A **personal overlay is additive-only**: it may *add* rubric rows, grader units, or `doctrine_lint`
forbids; it may **never relax or remove** a domain or agnostic rule. So it can only hold you to *more*,
never less — it can't be used to wave your own work through. It does not re-supply the domain hooks; it
composes on top of the active domain profile.

## What a DOMAIN profile supplies

Matches the hook shape the profiles already use (`profiles/README.md`, `generic-saas/*`):

**Frame** *(`frame-profile.md`)*
- `sources` *(must)* — where Frame's context comes from (a PRD + tickets; a sales kickoff + transcripts;
  a research question + papers).
- `sections` *(must)* — which functional-analysis sections are required vs optional.
- `hard_gates` *(may)* — phase-specific blockers (e.g. isolation rules pinned before Plan).
- `grader_bar` *(must)* — `verifiable_means`, `usual_silent_gaps`, the clean-handoff bar (consumed by
  [`graders/frame-completeness.md`](../graders/frame-completeness.md)).
- `has_ui` *(must)* — gates the UI-sketch hard gate + the browser grader.

**Plan** *(`plan-profile.md`)*
- `design_catalog` *(must)* — the shapes tickets route against.
- `tiering_signals` *(must)* — what makes a ticket ship-able by an agent vs human-only in this domain.

**Implement** *(`implement-profile.md`)*
- `rubrics` *(must)* — the fuzzy-grader rubrics (feature · pattern/drift · docs-currency).
- `verify_means` + `false_green_traps` *(must)* — how "done" is proven + where green lies in this domain.
- `conventions` / `forbids` *(may)* — the drift rubric + `doctrine_lint --forbid` rules.
- `codemods` *(may)* — the deterministic auto-fix arm.
- `doctrines` *(may)* — which `doc-patterns/doctrines/*` this domain mandates.
- `living_docs` *(must)* — the docs-currency grader's set.

**Check commands** *(`check-commands.md` — a separate file · the active-profile handshake)*
- `check_commands` *(must)* — every deterministic grader (lint · tests · type-check · doctrine-lint ·
  **security** · **coverage** · **deps** · schema · logs) reads its command + threshold + allowlist from
  `profiles/<active-profile>/check-commands.md`, resolved at run time (never hardcoded). Split out of
  `implement-profile.md` so a grader reads one file for its command and profile-switching is explicit. An
  agnostic grader the domain doesn't run is **declared n/a** in that file, never silently dropped.

**Any profile (domain or personal)** *(optional)*
- `graders/` — **profile-authored grader units** (the extension interface below).

## Composition — how the layers combine

`/review-gate` (or the code-verification loop) composes, in order:
1. **agnostic graders** (`graders/`, `graders/checks/`) — always run;
2. **active domain profile** — its rubrics, check-commands, and any `profiles/<domain>/graders/`;
3. **optional personal overlay** — its *additional* rows/forbids + `profiles/personal/<name>/graders/`.

Rubrics **union**; forbids **union**; grader sets **union**. On conflict the **stricter** rule wins —
additive-only guarantees a personal overlay can only tighten.

## Grader extension — profile-authored graders

A profile may ship its own grader units, not just `--forbid` regexes (the "let a profile ship a grader,
not only a lint rule" step). A profile grader is a `.md` def in the profile's `graders/` dir (copy
`_skeleton/grader.md`) that:
- **conforms to the grader contract** — `grade(diff, rubric, context) → {pass, findings, fix?}` (see
  [`../graders/code-verification-loop.md`](../graders/code-verification-loop.md));
- **declares its kind** — `deterministic` (a command/script, runs first, short-circuits) or `fuzzy` (a
  fresh sub-agent, one rubric, keep few);
- **declares its rubric source** — inline, or a file the loop reads and injects (sub-agents don't have
  the repo in context — the orchestrator injects; never "go read X").

**Budget:** deterministic profile graders are unlimited (cheap, factual). **Fuzzy** graders — agnostic +
domain + personal combined — stay at **~3**; a profile adding a fuzzy grader justifies it against the cap
(too many blur). GATE-0 warns when the composed fuzzy set exceeds it.

## Well-formed = passes GATE 0

- A **domain** profile is admissible only if every *(must)* slot is filled (no `{TODO}`) and every
  referenced file resolves.
- A **personal** overlay is admissible if its additions are well-formed (additive-only; grader units
  conform) — it is **not** required to fill the domain must-slots.
- Any profile-shipped **grader** must conform (kind + rubric-source declared, contract-shaped).

[`graders/profile-completeness.md`](../graders/profile-completeness.md) (GATE 0) checks this **before
Frame runs**. A `{TODO}` in a must-slot, a dangling reference, an overlay that relaxes a rule, or a
malformed grader unit is a **finding** — not a silent default.

## Shipped profiles / skeletons
- **`generic-saas/`**, **`edge-telemetry/`** — the two domain profiles (`README.md`).
- **`personal/`** — home for personal overlays (see its `README.md`).
- **`_skeleton/`** — `frame|plan|implement-profile.md` + `check-commands.md` (domain), `personal-profile.md`
  (overlay), and `grader.md` (a profile-authored grader unit). Copy to start a new profile or grader.
