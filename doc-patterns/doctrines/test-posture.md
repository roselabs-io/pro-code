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

## Altitude (the universal rule for *which* tier)

**Test at the highest tier that still localizes the failure.** Go as high (integrated) as you can while a failing test still pins the cause — "higher" leans toward integration, but "localizes" is the brake:

- **Bug in the wiring / effect / a contract** → integration. A unit test with mocks gives a false green (the real request was never scoped, the real boundary never crossed). The behaviour *is* the wiring, so the higher tier still localizes.
- **Bug in dense branching / pure calc** → unit. If an integration test fails with "total is wrong" but can't say *which* branch broke, it's the wrong altitude — drop to the tier that pinpoints.

Then **don't re-assert lower** — once a tier proves a behaviour, don't test it again below. Two failure modes this prevents: **wrong altitude** (a high test checking pure-logic branches it can't localize) and **accretion** (the same rule asserted at three layers).

## Profile emphasis (the opinion — filled per domain)

The profile names *what a good test looks like here* and which layers it owes:

- **assert the effect, not the status** — a `200` proves nothing; assert the row changed / the field serialized.
- **red-green on a fix** — a regression test must have been *seen to fail* before the fix.
- **fire AND no-fire** — a rule needs both a case that trips it and one that stays silent.
- **real path, not a mock** — the boundary/safety test must exercise the real code path.

> {TODO: the profile writes its owed layers (integration per endpoint? e2e?) + its 1–2 load-bearing posture lines here.}
