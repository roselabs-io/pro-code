---
consumed_by: ["orchestrator"]
canonical_for: "what a profile must supply and how the active one resolves"
profile: agnostic
---

# Profile contract — the hook interface a profile supplies

A **profile** is the domain overlay: the pipeline ships agnostic phase skills + checks + graders + neutral
guide skeletons; a profile fills the *content* for one domain. Swap the profile, retarget the whole
pipeline ([README](README.md)). This file is the **exhaustive must/may list** a profile supplies — the seam
every skill, check, and grader reads. It makes "same hook shape, different content per domain" a
checkable contract.

> **Status.** The **domain**-profile hooks below are proven — `generic-saas`, `edge-telemetry`, and
> `saas-web` fill them and run through the same skills, checks, and graders byte-for-byte. The
> **personal**-overlay kind is exercised by `personal/jay-z`. The `deploys` flag and the infra check were
> added with `saas-web`; the `smoke` row and the simplicity rubric were added 2026-09 and have not yet
> been through a cold rebuild. The single-review sequence of `skills/review-gate` has not been through a
> cold rebuild either.

## Two kinds of sensor

The pipeline distinguishes **checks** (commands; facts) from **graders** (LLM sessions; judgment): the
one review of each ticket and the on-demand graders. The definition, the table, and the run order live
in [`../checks/README.md`](../checks/README.md). A profile adds a check as a **row in `check-commands.md`**
and a review lens as a **unit under `graders/`**; the two are never mixed.

## Two kinds of profile

| Kind | Differs by | Lives in | Supplies |
|---|---|---|---|
| **Domain** | *what* you build (`generic-saas`, `edge-telemetry`, `saas-web`, …) | `profiles/<domain>/` | the **full** hook set below |
| **Personal** | *who* reviews (a person's taste) | `profiles/personal/<name>/` | a **lean overlay** — extra rubric rows, extra lens units, extra forbids only |

A **personal overlay is additive-only**: it may *add* rubric rows, lens units, or `doctrine_lint`
forbids; it may **never relax or remove** a domain or agnostic rule. So it can only hold you to *more*,
never less — it can't be used to wave your own work through. It does not re-supply the domain hooks; it
composes on top of the active domain profile.

## Active-profile resolution

The pipeline never hardcodes a profile. The active profile is resolved **once per run**, in this order:

1. **`$PROFILE`** — an environment variable naming a domain profile (`PROFILE=saas-web`), optionally
   with an overlay (`PROFILE=generic-saas+personal/jay-z`). Overrides the file.
2. **`.pipeline-profile`** — a file at the project root (the directory the pipeline runs in, e.g.
   `examples/<name>/.pipeline-profile`), key: value lines:
   ```
   domain: saas-web
   overlay: personal/jay-z      # optional; one overlay
   ```
3. Neither → **GATE-0 fails** with `no-active-profile`. There is no default profile. Frame's first
   action on a new project is to write `.pipeline-profile` with the driver's choice.

Every skill, check, and grader that needs profile content reads `profiles/<domain>/` (and
`profiles/<overlay>/`) from this resolution. `profiles/<active-profile>/…` in the docs means "the
resolved path", never a literal.

## What a DOMAIN profile supplies

Matches the hook shape the profiles already use (`profiles/README.md`, `generic-saas/*`):

**Frame** *(`frame-profile.md`)*
- `sources` *(must)* — where Frame's context comes from (a PRD + tickets; a sales kickoff + transcripts;
  a research question + papers).
- `sections` *(must)* — which functional-analysis sections are required vs optional.
- `hard_gates` *(may)* — phase-specific blockers (e.g. isolation rules pinned before Plan).
- `grader_bar` *(must)* — `verifiable_means`, `usual_silent_gaps`, the clean-handoff bar (consumed by
  the on-demand [`graders/frame-completeness.md`](../graders/frame-completeness.md)).
- `has_ui` *(must)* — gates the UI-sketch hard gate + the [browser check](../checks/browser.md).
- `deploys` *(must)* — whether the profile ships a deployable stack; gates the
  [infra check](../checks/infra.md). `false` routes the runtime floor to the
  [runtime-smoke check](../checks/runtime-smoke.md) instead. Both flags are **additive**: a profile that
  sets one false declares the corresponding check n/a — no skill or existing-check change.

**Plan** *(`plan-profile.md`)*
- `design_catalog` *(must)* — the shapes tickets route against.
- `tiering_signals` *(must)* — what makes a ticket ship-able by an agent vs human-only in this domain.

**Implement** *(`implement-profile.md`)*
- `rubrics` *(must)* — what each lens of the review ([`graders/review.md`](../graders/review.md)) points
  at: **feature** · **pattern/drift** · **docs-currency** · **simplicity**.
- `verify_means` + `false_green_traps` *(must)* — how "done" is proven + where green lies in this domain.
- `conventions` / `forbids` *(may)* — the drift rubric + `doctrine_lint --forbid` rules.
- `codemods` *(may)* — the deterministic auto-fix arm.
- `doctrines` *(may)* — which `doc-patterns/doctrines/*` this domain mandates.
- `living_docs` *(must)* — the set the review's docs-currency lens reads.

**Check commands** *(`check-commands.md` — a separate file · the active-profile handshake)*
- `check_commands` *(must)* — one row per check in the
  [deterministic tier](../checks/README.md#the-deterministic-tier-in-order) (lint · type-check ·
  doctrine-lint · codemod-check · security · tests · coverage · deps · schema · logs · **smoke** ·
  browser · infra), each with command + threshold + allowlist, read from the resolved
  `check-commands.md` at run time. Split out of `implement-profile.md` so a check reads one file for its
  command and profile-switching is explicit. A check the domain doesn't run is **declared n/a with a
  reason** in that file, never silently dropped.

**Any profile (domain or personal)** *(optional)*
- `graders/` — **profile-authored lens units** of the review (the extension interface below).

## Composition — how the layers combine

[`skills/review-gate`](../skills/review-gate/SKILL.md) composes, in order:
1. **agnostic checks and the review rubric** (`checks/`, `graders/review.md`) — always run;
2. **active domain profile** — its rubrics, check-commands, and any `profiles/<domain>/graders/`;
3. **optional personal overlay** — its *additional* rows/forbids + `profiles/personal/<name>/graders/`.

Rubrics **union**; forbids **union**; lens units **union**. On conflict the **stricter** rule wins —
additive-only guarantees a personal overlay can only tighten.

## Review extension — profile-authored lens units

A profile may ship its own review lenses, not just `--forbid` regexes. A lens unit is a `.md` def in the
profile's `graders/` dir (copy `_skeleton/grader.md`) that:
- **is applied by the one review** — after the four agnostic lenses, in the same session and the same
  pass ([`graders/review.md`](../graders/review.md)); it is not a separate grader session;
- **is LLM judgment** — a deterministic rule is not a lens unit; it is a row in `check-commands.md` (a
  `--forbid`, a codemod `--check`, a script) and costs nothing;
- **declares its rubric source** — inline, or a file the orchestrator reads and injects into the review's
  prompt (the review session does not have the repo's docs in context; never "go read X").

Profile check rows are unlimited. Each lens unit adds to the one review's rubric; a unit that would flag
what an agnostic lens already flags is folded into the profile's `rubrics` instead.

## Well-formed = passes GATE 0

- The **active profile resolves** (`$PROFILE` or `.pipeline-profile`) to an existing `profiles/<domain>/`.
- A **domain** profile is admissible only if every *(must)* slot is filled (no `{TODO}`), both flags
  (`has_ui`, `deploys`) are set, every referenced file resolves, and every row of the deterministic tier
  is either filled or declared n/a with a reason.
- A **personal** overlay is admissible if its additions are well-formed (additive-only; lens units
  conform) — it is **not** required to fill the domain must-slots.
- Any profile-shipped **lens unit** must conform (rubric-source declared, a checkable assertion).

[`graders/profile-completeness.md`](../graders/profile-completeness.md) (GATE 0) checks this, run on
demand when a profile is written or changed. A `{TODO}` in a must-slot, a dangling reference, an overlay
that relaxes a rule, an unresolved profile, or a malformed lens unit is a **finding** — not a silent
default.

## Shipped profiles / skeletons
- **`generic-saas/`**, **`edge-telemetry/`**, **`saas-web/`** — the domain profiles (`README.md`).
- **`personal/`** — home for personal overlays (see its `README.md`); ships `jay-z/`.
- **`_skeleton/`** — `frame|plan|implement-profile.md` + `check-commands.md` (domain), `personal-profile.md`
  (overlay), and `grader.md` (a profile-authored lens unit). Copy to start a new profile or lens unit.
