# profile-completeness — GATE 0 (before Frame)

The **first** gate: it checks a profile is **well-formed before the pipeline runs on it**. The pipeline
is only as good as its profile; an incomplete profile means every downstream phase runs on missing
context. So GATE 0 grades the *profile itself*, once, at the front — including any personal overlay and
any profile-authored graders. It's the "is the profile ready?" ceremony, the mirror image of
`frame-completeness` (which grades the *spec* once the profile is trusted).

## What it checks (against [`../profiles/CONTRACT.md`](../profiles/CONTRACT.md))

**Resolution** (first, before anything else):
- **the active profile resolves** — `$PROFILE` or the project's `.pipeline-profile` names an existing
  `profiles/<domain>/` (and, if given, an existing `profiles/<overlay>/`). Neither set → `no-active-profile`;
  a name with no directory → `dangling-ref`. There is no default to fall back to.

**A domain profile** (`profiles/<domain>/`):
- **every *(must)* slot is filled** — no `{TODO}` left in `frame|plan|implement-profile.md`;
- **referenced files resolve** — the guides/doc-patterns the profile names exist;
- **both flags are set** — `has_ui` (gates the UI-sketch hard gate + the browser check) and `deploys`
  (gates the infra check; false routes the boot floor to the smoke check);
- **every row of the deterministic tier is present** in `check-commands.md` — filled, or declared n/a
  with a reason ([`../checks/README.md`](../checks/README.md#the-deterministic-tier-in-order) lists the
  rows). A row that is simply absent is a finding;
- **the rubrics hook names all four graders** — feature · drift · docs-currency · simplicity.

**A personal overlay** (`profiles/personal/<name>/`) — a *lighter* bar:
- it's **additive-only** — flag any row/forbid that tries to *relax or remove* a domain/agnostic rule;
- it is **not** required to fill the domain must-slots (it composes on top of the domain profile);
- its additions are well-formed.

**Any profile-shipped grader** (`profiles/<x>/graders/*.md`):
- **conforms to the contract** — declares `rubric_source` and states a checkable assertion (not "handle
  X well"); it is LLM judgment — a mechanical rule belongs in `check-commands.md`, and a unit that is
  really a command is a `misfiled-check` finding;
- the **shared grader set** (agnostic + domain) stays **within ~4**; a personal overlay's grader is an
  opt-in **+1** — warn on the composed total, don't block (the person is tightening on themselves).

## Output — gate the pipeline entry

Pass → the (composed) profile is admissible, Frame may run. Fail → list the offending slots / relaxations
/ malformed graders; the human fills them before proceeding. Deterministic where it can be (grep for
`{TODO}`, path existence, row presence, "does a personal row weaken a domain rule?"); judgment only for
"is this slot *meaningfully* filled vs a placeholder sentence."

## Contract

```
grade(profile-set, rubric=CONTRACT.md, context)
  → { pass, findings: [no-active-profile | empty-slot | dangling-ref | flag-unset | row-missing |
                       relaxes-rule | malformed-grader | misfiled-check | grader-over-budget] }
```

Agnostic — no domain content. Validated against the three shipped domain profiles (`generic-saas`,
`edge-telemetry`, `saas-web`) and the `personal/jay-z` overlay. The resolution step, the `deploys` flag,
the row-presence rule, and the simplicity rubric were added 2026-09 and have not yet been through a cold
rebuild. See [`../checks/README.md`](../checks/README.md#checks-vs-graders) for the grader contract.
