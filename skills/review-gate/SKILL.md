---
name: "review-gate"
description: "Implement's gate. Run the auto-fix arm, then the checks in short-circuit order, then one independent review in a fresh session; the author makes at most one fix pass, the checks rerun, and the run stops for the human with each finding marked fixed or open."
consumed_by: ["orchestrator"]
canonical_for: "the gate after Implement: order, policy, stopping conditions"
profile: agnostic
---

# review-gate (Implement's gate)

The gate between a ticket's diff and the human. It runs no check and holds no rubric of its own: the
checks are specified under [`checks/`](../../checks/README.md), the review's rubric is
[`graders/review.md`](../../graders/review.md), and the commands, thresholds and rubrics come from the
**active profile** (resolved per [`profiles/CONTRACT.md`](../../profiles/CONTRACT.md#active-profile-resolution)).

## The sequence

```
implement → [ auto-fix arm ] → [ checks, in order, short-circuit ]
          → [ one independent review — fresh session, author ≠ reviewer ]
          → findings? → [ ONE fix pass by the author ] → [ checks rerun ]
          → stop: handoff to the human (each finding fixed or open)
```

1. **Auto-fix arm.** codemod-lite (`ruff --fix`, `ruff format`, `eslint --fix`) and the profile's
   codemods ([`codemods/`](../../codemods/README.md)) run first, so mechanical drift is fixed by a script
   before any check reports it.
2. **Checks.** Every check of the active profile's `check-commands.md`, in the order
   [`checks/README.md`](../../checks/README.md#the-deterministic-tier-in-order) fixes, stopping at the
   first red. A check the domain does not run is declared n/a there. The author fixes a red check and
   reruns the checks; the review does not start until every check is green.
3. **One independent review.** A session that did not write the diff, with fresh context and read-only
   access, applies [`graders/review.md`](../../graders/review.md): the feature, drift, docs-currency and
   simplicity lenses, then any lens unit the profile or overlay ships. It reports every finding in one
   pass.
4. **At most one fix pass.** When the review has findings, the author addresses them in one pass and the
   checks rerun. The review is not run again.
5. **Stop for the human.** The handoff lists every review finding as fixed (with the change) or open
   (with the reason), the final check results, and anything the author could not run.

## Rules

- **Author ≠ reviewer.** The session that wrote the diff does not review it. The reviewer has no access
  to the author's conversation. A check has no author and needs no such rule.
- **One review, one fix pass.** There is no re-review after the fix pass and no loop until green. A
  finding the fix pass did not resolve goes to the human as open.
- **Checks before the review.** The review does not spend a session on a diff that fails a check.

## Gate policy — what blocks

- A red check blocks: the ticket is not handed off as done while a check is red. A check the author
  cannot make green after its fix is reported red in the handoff.
- A review finding does not block the handoff. The author fixes what it can in its one pass; the human
  decides on each open finding.
- The human's acceptance is the last step. Green checks and a review with no open finding are evidence
  for that decision, not the decision.

## Composition — how the layers combine

The gate composes, in order:
1. **agnostic** checks and the review rubric (`checks/`, `graders/review.md`) — always;
2. **active domain profile** — its `check-commands.md` rows, its `rubrics`, and any lens units under
   `profiles/<domain>/graders/`;
3. **optional personal overlay** — its additional rubric rows and forbids, and any lens units under
   `profiles/personal/<name>/graders/`.

Rubrics, forbids and lens units union. On conflict the stricter rule wins; a personal overlay can only
tighten.

## Stopping conditions

- Every check green and the review has no finding → handoff.
- Every check green after the fix pass → handoff, with each finding fixed or open.
- A check still red after the fix pass → handoff with the check reported red.

## Promote repeated feedback

A finding that recurs across tickets is a missing check or guide. When it is mechanical, add a
`--forbid` row, a codemod or a check row to the profile; when it is judgment, add a line to the
profile's `rubrics` or conventions. A new control is added for a failure that has occurred, not for one
that might.

## Profile hooks

A profile supplies (the full list: [`profiles/CONTRACT.md`](../../profiles/CONTRACT.md)):
- **`check_commands`** — one row per check this domain runs, with command, threshold and allowlist
  (`check-commands.md`); n/a rows say why.
- **`rubrics`** — what each review lens points at: the acceptance criterion (feature), the design
  catalog and conventions (drift), the living-docs set (docs-currency), the ticket scope and declared
  choice-points (simplicity).
- **`verify_means`** and **`false_green_traps`** — how "done" is proven in this domain, and where a check
  passes while the behaviour is broken.

## Worked example (`generic-saas` — the multi-tenant isolation ticket)

```
Implement — T5 "Enforce tenant isolation on /projects"
acceptance: A's token GET /projects/{B_id} → 404; no tenant-B row ever serializes.
hook: tenant-scoped-query-guard

Checks (short-circuit)
  ✓ type-check   ✓ lint
  ✗ tests — integration test `test_cross_tenant_404` fails: returns 200 + B's row.
  → the author scopes the query by tenant; checks rerun:
  ✓ type-check ✓ lint ✓ tests ✓ smoke

Review (fresh session, author ≠ reviewer)
  feature       ✓ criterion met: the cross-tenant assertions pass with fresh output.
  drift         ✗ the guard is applied on GET but missing on PATCH /projects/{id};
                  tenant-scoped-query-guard scopes every read and write.
  docs-currency ✗ current-state.md still says "isolation: TODO"; no decision record for
                  the app-layer-vs-RLS choice.
  simplicity    ✗ a `TenantContext` class with 4 methods, 1 used; the hook names a query guard.

Fix pass (one)
  guard added on PATCH and DELETE; current-state.md updated; decision record 0002 written;
  TenantContext removed. Checks rerun: all green.

Handoff
  drift — fixed · docs-currency — fixed · simplicity — fixed. No open finding.
  The human runs the cross-tenant scenario and accepts or reopens the ticket.
```
