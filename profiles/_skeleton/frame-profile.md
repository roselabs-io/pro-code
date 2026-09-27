---
consumed_by: [frame, grader:frame]
canonical_for: `_skeleton` Frame bar and silent gaps
profile: _skeleton
---

# Profile — `{domain}` · Frame

Copy this dir to `profiles/<domain>/` and fill every `{TODO}`. *(must)* slots are gated by GATE-0
([`../../graders/profile-completeness.md`](../../graders/profile-completeness.md)); *(may)* slots can be
omitted. See [`../CONTRACT.md`](../CONTRACT.md).

Domain: {TODO: one line — what this domain builds and the stack}.

## Sources *(must)*
{TODO: where Frame's context comes from in this domain — a table of source → what it provides}

## Functional-analysis sections *(must)*
- **Required:** {TODO}
- **Optional (add only if they bite):** {TODO}

## Hard gates *(may)*
{TODO: phase-specific blockers that must be pinned before Plan, or "none"}

## `has_ui` *(must)*
{TODO: true/false — gates the UI-sketch hard gate + the browser check}

## `deploys` *(must)*
{TODO: true/false — true gates the infra check (build + boot the shipped stack); false routes the runtime floor to the smoke check}

## Grader bar *(must — consumed by `frame-completeness`)*
- **`verifiable_means`:** {TODO: what "verifiable" means here}
- **`usual_silent_gaps`:** {TODO: the gaps briefs in this domain routinely omit}
- **clean-handoff bar:** {TODO: when Frame→Plan may proceed}
