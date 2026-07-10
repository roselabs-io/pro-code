# profile-completeness — GATE 0 (before Frame)

The **first** gate: it checks a profile is **well-formed before the pipeline runs on it**. The pipeline
is only as good as its profile; an incomplete profile means every downstream phase runs on missing
context. So GATE 0 grades the *profile itself*, once, at the front — including any personal overlay and
any profile-authored graders. It's the "is the profile ready?" ceremony, the mirror image of
`frame-completeness` (which grades the *spec* once the profile is trusted).

## What it checks (against [`../profiles/CONTRACT.md`](../profiles/CONTRACT.md))

**A domain profile** (`profiles/<domain>/`):
- **every *(must)* slot is filled** — no `{TODO}` left in `frame|plan|implement-profile.md`;
- **referenced files resolve** — the guides/doc-patterns the profile names exist;
- **`has_ui` is set** — it gates the UI-sketch hard gate + the browser grader.

**A personal overlay** (`profiles/personal/<name>/`) — a *lighter* bar:
- it's **additive-only** — flag any row/forbid that tries to *relax or remove* a domain/agnostic rule;
- it is **not** required to fill the domain must-slots (it composes on top of the domain profile);
- its additions are well-formed.

**Any profile-shipped grader** (`profiles/<x>/graders/*.md`):
- **conforms to the contract** — declares `kind` (deterministic|fuzzy) + `rubric_source`, and states a
  checkable assertion (not "handle X well");
- the **composed fuzzy set** (agnostic + domain + personal) stays **within ~3** — warn if it exceeds.

## Output — gate the pipeline entry

Pass → the (composed) profile is admissible, Frame may run. Fail → list the offending slots / relaxations
/ malformed graders; the human fills them before proceeding. Deterministic where it can be (grep for
`{TODO}`, path existence, "does a personal row weaken a domain rule?"); fuzzy only for "is this slot
*meaningfully* filled vs a placeholder sentence."

## Contract

```
grade(profile-set, rubric=CONTRACT.md, context)
  → { pass, findings: [empty-slot | dangling-ref | relaxes-rule | malformed-grader | fuzzy-over-budget] }
```

Agnostic — no domain content. Validated against the two shipped profiles (`generic-saas`,
`edge-telemetry`). The domain-vs-personal split + the grader-extension checks are newer; they firm up as
personal overlays and profile-authored graders get exercised. See
[`code-verification-loop.md`](code-verification-loop.md) for the grader contract.
