# Grader — plan-completeness

The **second** grader in the pipeline — the Plan→Implement gate. It grades the **plan artifacts** (system overview, surface specs, backlog) *before Implement consumes them*, so it's still **"grade the context, not just the code"**: the plan is the guides Implement builds against, and a plan with a hole becomes code with a hole.

**Author ≠ grader.** Run this as a *fresh* pass, not a self-review — the eyes that decomposed the spec are blind to what they dropped. Fresh context, rubric in hand.

Agnostic by design. The **ceremony** below is domain-neutral; the **bar** (what "covered," "verifiable," "well-formed" mean) is supplied by the active profile.

## Harder than frame-completeness

Frame's grader *informs* — it has no hard "done." Plan's has one near-deterministic check that **blocks**: **coverage.** Every functionality in the Frame docs must map to ≥ 1 ticket. A missing functionality isn't a thin spec — it's work that will silently never get built. The rest of the ceremony stays soft (a 🟢🟡🔴 scorecard that aims, doesn't block), but **coverage is a gate.**

## The ceremony — produce four things

**1. A coverage map (the gate).** Walk the functional-analysis functionalities; for each, name the ticket(s) that cover it. Any functionality with no ticket is 🔴 **blocking** — Implement can't build what isn't decomposed. Also flag the inverse: a ticket that maps to *no* functionality (scope creep or a missing spec line — route it back to Frame). Coverage is the one check that stops the handoff.

**2. A well-formedness scorecard.** Sort the tickets into three buckets, each framed by its **implement-time cost**, not abstract incompleteness:
- 🟢 **Ready** — verifiable acceptance criterion + a design hook (or explicit `novel`) + `depends-on` wired.
- 🟡 **Thin** — present but weak. *"The acceptance criterion is 'handle errors gracefully' — the dev invents the pass condition, and the verify gate can't check it."*
- 🔴 **Malformed** — an unverifiable acceptance criterion (can't be asserted → the verify gate is blind to it), a missing hook on non-novel work, or a dangling `depends-on`.

**3. Tiering + sequencing sanity.** A quick pass, not a scorecard:
- **Tiers justified?** Every 🟢 genuinely has a proven hook + is verifiable + touches no risk boundary. A 🟢 on a boundary ticket is the dangerous miss — it sends unreviewed risk into an autonomous runner.
- **Sequencing sound?** No `depends-on` cycle (fail-loud if there is). Critical path called out. Start-now set non-empty — if *nothing* is startable, the plan is blocked before it begins; say so.

**4. An explicit sign-off — two paths.** End by asking the driver to choose:
- **(A) Close the top gaps now** — fix coverage 🔴s first (they're the gate), then the highest-cost malformed tickets; re-score and hand off clean.
- **(B) Sign off under the bar, on purpose** — legitimate for 🟡s and sequencing notes, **never for a coverage 🔴**. When chosen, **log every under-bar gap** as an `[open]` entry (owner + stakes) so a deliberate under-bar handoff is *recorded as intentional*.

## Profile hooks

A profile supplies:
- **`catalog`** — the design shapes tickets route against (so "has a hook" is checkable).
- **`coverage_means`** — what counts as a functionality covered (`generic-saas`: ≥ 1 ticket whose acceptance criterion, if it passes, delivers that functionality).
- **`verifiable_means`** — what makes an acceptance criterion checkable (`generic-saas`: an automated test can assert it).
- **`tiering_signals`** — what "proven pattern," "verifiable," "risk boundary," "out-of-repo dependency" mean in this domain.

## Worked example (`generic-saas` — multi-tenant isolation slice)

```
Plan readiness — Acme workspace (multi-tenant B2B)

COVERAGE (gate)
  functional-analysis functionalities → tickets
  ✓ create/manage workspace      → T2
  ✓ invite + role assignment     → T3, T4
  ✗ tenant isolation             → NO TICKET
    🔴 the product's core promise is not decomposed. GATE — close before handoff.

Well-formedness
  🟢 Ready
    - T3 "Invite member": criterion "POST /invites creates a pending invite,
      duplicate email → 409" — test-assertable. Hook: severity-tiered-validation.
  🟡 Thin
    - T2 "Workspace CRUD": criterion "manage workspaces properly" — not assertable;
      the verify gate can't check "properly." → dev invents the pass condition.
  🔴 Malformed
    - T5 "Enforce isolation" (added after the coverage fix): criterion "enforce
      tenant isolation" — unverifiable. Rewrite as: "user A's token GET
      /projects/{B_id} → 404; no tenant-B row ever serializes; asserted by an
      integration test." Hook: tenant-scoped-query-guard.

Tiering + sequencing
  ⚠ T5 tagged 🟢 agent-ship — but isolation IS the risk boundary. Must be 🟡 (or 🔴):
    an autonomous runner should not ship the core-promise authz slice unreviewed.
  ✓ no dependency cycle; critical path T1 → T5 called out; start-now = {T1, T2}.

Sign-off — pick one:
  (A) Close the coverage 🔴 (add T5), rewrite its criterion to be test-assertable,
      re-tier it off 🟢, then re-score.
  (B) Not available for the coverage 🔴 — isolation can't ship untracked. (A) it is.
```
