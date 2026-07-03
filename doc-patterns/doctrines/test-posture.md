# {{project_name}} — Test Posture

> A **Rule** (feedforward) for *how* this domain tests. The counterpart to
> the false-green traps: the posture prevents the trap, the trap-list catches it.
> Pulled from `doc-patterns/doctrines/test-posture.md`. The **mechanical floor is deterministic**
> (`graders/checks/doctrine_lint.py` — no assert-less test, no unexplained skip); the
> posture *emphasis* is the profile's opinion, checked by the feature grader.

## Universal posture (the deterministic floor)

- **Every test asserts.** A `test_*` with no `assert` and no `pytest.raises` is not a test — it's a smoke that always passes. The linter flags it.
- **No silent skip.** `@pytest.mark.skip` / `xfail` without a `reason=` is a hidden hole. The linter flags it.
- **Tests ship with the ticket**, never "later."

## Layer posture (the profile picks the layers this domain owes)

- **An integration test per endpoint / entry point.** Every route (or public entry point) gets a test that drives the *real* request through the app and asserts the *effect*, not the status. Unit tests are a bonus; the integration test is the floor.
- **An e2e test when there is a frontend.** A UI-bearing profile owes an end-to-end test that drives the *running* app like a user (the browser grader). An API-only profile owes none — declared, not skipped.

## Profile emphasis (the opinion — filled per domain)

The profile names *what a good test looks like here* and which layers it owes:

- **assert the effect, not the status** — a `200` proves nothing; assert the row changed / the field serialized.
- **red-green on a fix** — a regression test must have been *seen to fail* before the fix.
- **fire AND no-fire** — a rule needs both a case that trips it and one that stays silent.
- **real path, not a mock** — the boundary/safety test must exercise the real code path.

> {TODO: the profile writes its owed layers (integration per endpoint? e2e?) + its 1–2 load-bearing posture lines here.}
