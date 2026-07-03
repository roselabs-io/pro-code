# Grader — frame-completeness

The **first** grader in the pipeline, and the highest-leverage: errors in the spec compound through Plan and Implement, so the ask→Frame handoff is where a completeness gate pays the most. **"Grade the context, not just the code"** starts here.

Agnostic by design. The **ceremony** below is domain-neutral; the **bar** (what "complete" and "verifiable" mean) is supplied by the active profile.

## Not a hard gate (with profile-defined exceptions)

Frame has no rigid "done." This grader *aims* the driver at what's missing and records a sign-off — it **informs** the decision, it doesn't block it. A profile MAY declare specific hard gates (e.g. `generic-saas`: "a multi-tenant product must pin its isolation rules before Plan"; `edge-telemetry`: "a UI-bearing app needs a reviewed UI sketch"). Those, and only those, block.

## The ceremony — produce four things

**1. A completeness estimate.** One rough number, so there's a single readiness signal — *"~75% — handoff-capable, but three gaps will cost the dev at implement-time."* A gut-check, not precision.

**2. A tiered scorecard.** Sort what's in the spec into three buckets:
- 🟢 **Solid** — substantive, ready to hand over.
- 🟡 **Thin** — present but weak. Frame each by its **downstream cost**, not abstract incompleteness: *"the dev will invent the error-recovery flow at implement-time with no spec,"* not *"the recovery section is short."*
- 🔴 **Blocking** — a gap that actually stops Plan: an undecided scope line that can't bound the backlog; a primary workflow with no described behaviour; an integration named with no contract.

**3. Targeted gap-pointing.** For every 🟡 and 🔴, name **who it hurts and when**, ordered by downstream cost — highest first. Aim the driver at the one gap worth closing now; don't dump a TODO list. Actively probe the categories briefs routinely omit — the profile lists its `usual_silent_gaps`. If they're absent, say so out loud rather than scoring around them. Also surface **imported assumptions** — anything the spec treats as settled that's actually a default from habit, not a stated requirement (the Frame-level seed of the build's [assumptions ledger](../doc-patterns/living-docs/assumptions.md)).

**4. An explicit sign-off — two paths.** End by asking the driver to choose:
- **(A) Close the top gaps now** — answer the highest-cost item (or push back upstream for the missing input), then re-score and hand off clean.
- **(B) Sign off under the bar, on purpose** — sometimes right (deadline; a gap that genuinely can't resolve yet). When chosen, **log every under-bar gap** as an `[open]` entry in `open-questions.md` (owner + stakes) — so a deliberate under-bar handoff is *recorded as intentional*, not later mistaken for an oversight.

## Profile hooks

A profile supplies:
- **`bar`** — the sections a clean handoff requires, plus any hard gates.
- **`verifiable_means`** — what makes acceptance checkable in this domain (`generic-saas`: "an automated test can assert it"; other domains differ).
- **`usual_silent_gaps`** — the categories to actively probe because inputs routinely omit them.

## Worked example (`generic-saas`)

```
Frame readiness — Acme workspace (multi-tenant B2B)

~70% — handoff-capable, but tenant-isolation behaviour is underspecified and will cost the dev.

🟢 Solid
  - Actors: member, workspace admin, billing owner — goals + surfaces each.
  - Primary flow: sign in → create workspace → invite member → assign role. Sequenced.
  - Data model: Account, Workspace, Member, Role, Invitation.

🟡 Thin
  - Invitation expiry — "links expire" stated, but no TTL / re-send behaviour.
    → dev invents the expiry policy at implement-time, no spec.

🔴 Blocking
  - Tenant isolation rules absent — which reads/writes scope to a workspace, and
    what a cross-workspace request returns (404 vs 403), is unspecified.
    → Plan can't decompose "enforce isolation"; the whole authz slice is unplannable.
      HIGHEST COST — and it's the product's core promise. Close first.

Sign-off — pick one:
  (A) Close the 🔴 first — pin the isolation rules (scoping + denied-response), then re-score.
  (B) Sign off at ~70% — log the 🔴 + 🟡 as [open] (owner + stakes) so the dev inherits them tracked.
```
