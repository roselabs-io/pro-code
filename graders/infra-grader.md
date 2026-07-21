# Grader — infra-grader

> **Infra** (feedback, ⚙️): builds the app's container images and boots the stack the way
> production will, then asserts it actually runs. The one grader that catches
> **"the code is right but it doesn't ship."**

Applies only to **deploying** profiles (a profile declares `deploys: true`). A library or an in-process
service skips it — there's nothing to build and boot. API-only or engine profiles set `deploys: false`
and declare it n/a in `check-commands.md`.

## What it grades

The verify gate's arbiter for *deliverability*: does the app build and boot as it will in production, from empty?

- **Images build** — the multi-stage Dockerfiles for each service build with no error, off the committed lockfiles.
- **The stack comes up** — `docker compose … up` brings every service (`api · web · db · proxy`) to healthy on a **fresh volume**, wired by the compose file + `.env.example`.
- **Migrations apply from empty** — the schema is created by the migration chain against an empty database (proves the `no create_all in the shipped path` convention — a build that only works because the app creates its own tables at runtime fails here).
- **Smoke passes** — against the *composed* stack, not the test harness: the API health endpoint is 200, the web root serves HTML, and one real round-trip works (e.g. an authenticated request returns the expected shape).

## The contract

```
infra grader = build + up + smoke script → { pass, findings }
  - build the images, compose up on a fresh volume, wait for healthy
  - run migrations from empty, then a smoke check against the running stack
  - deterministic: no LLM; the profile supplies the compose file + smoke command
  - runs in the verify beat, after unit/integration are green (and alongside the browser grader)
```

- **pass** = images build · stack reaches healthy · migrations apply from empty · smoke is green.
- a **missing precondition** (no Dockerfile, no compose file, no migration, no `.env.example`) is a *finding*, not a silent pass.

## Why it's not redundant with the tests

The integration tests run the app **in-process** against a **testcontainers** database — they prove the *logic* is right. They say nothing about whether the *shipped image* builds, whether the compose wiring and env are correct, or whether the schema applies from empty. Green tests + a broken Dockerfile, a missing env var, or a `create_all`-only schema **still doesn't deploy**. The infra grader is the only grader that exercises the artifact you actually ship. (Same spirit as `200 ≠ handler ran` and the browser grader's `green-below ≠ correct-on-screen`: **tests-green ≠ ships**.)

## Profile hooks

- **`deploys`** — whether this profile ships a deployable stack at all (gates this grader, like `has_ui` gates the browser grader).
- **the `infra` row in `check-commands.md`** — the build/up/smoke commands + the healthcheck the grader asserts, resolved from the active profile at run time.

## Note — this is an additive model extension

The `deploys` hook and this grader are an **additive** extension of the pro-code model, the same shape the `has_ui` + browser-grader pair took for `edge-telemetry`: **no skill changes, no change to any existing grader.** Profiles that don't deploy set `deploys: false` and declare it n/a — their behaviour is untouched. First exercised by `saas-web`. "Profiles swap, graders don't" still holds: this grader is agnostic; the compose file and smoke command are profile content.
