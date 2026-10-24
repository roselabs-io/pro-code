---
consumed_by: ["grader:profile"]
canonical_for: "the profile authoring rubric"
profile: agnostic
---

# profile-completeness — GATE 0 (on demand)

Checks that a profile is **well-formed** for the pipeline to run on it. A person runs it on demand: when a
profile or overlay is written or changed, and before a project's first Frame on a profile it has not
used. No phase runs it automatically. It grades the *profile itself* — including any personal overlay and
any profile-authored lens units. It's the "is the profile ready?" ceremony, the mirror image of
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
- **the rubrics hook names all four review lenses** — feature · drift · docs-currency · simplicity.

**A personal overlay** (`profiles/personal/<name>/`) — a *lighter* bar:
- it's **additive-only** — flag any row/forbid that tries to *relax or remove* a domain/agnostic rule;
- it is **not** required to fill the domain must-slots (it composes on top of the domain profile);
- its additions are well-formed.

**Any profile-shipped lens unit** (`profiles/<x>/graders/*.md`):
- **conforms to the contract** — declares `rubric_source` and states a checkable assertion (not "handle
  X well"); it is LLM judgment applied by the one review — a mechanical rule belongs in
  `check-commands.md`, and a unit that is really a command is a `misfiled-check` finding.

## Output — gate the pipeline entry

Pass → the (composed) profile is admissible, Frame may run. Fail → list the offending slots / relaxations
/ malformed graders; the human fills them before proceeding. Deterministic where it can be (grep for
`{TODO}`, path existence, row presence, "does a personal row weaken a domain rule?"); judgment only for
"is this slot *meaningfully* filled vs a placeholder sentence."

## Contract

```
grade(profile-set, rubric=CONTRACT.md, context)
  → { pass, findings: [no-active-profile | empty-slot | dangling-ref | flag-unset | row-missing |
                       relaxes-rule | malformed-grader | misfiled-check] }
```

Agnostic — no domain content. Validated against the three shipped domain profiles (`generic-saas`,
`edge-telemetry`, `saas-web`) and the `personal/jay-z` overlay. The resolution step, the `deploys` flag,
the row-presence rule, and the simplicity rubric were added 2026-09 and have not yet been through a cold
rebuild. See [`../checks/README.md`](../checks/README.md#checks-vs-graders) for the check and grader contracts.
