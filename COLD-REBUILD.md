# Cold rebuild — the clean-room pipeline test (every example)

Paste the block below into a **fresh** Claude Code session at the pro-code repo root. It builds every
example service **from the pipeline + profiles alone** — the proof that the profiles are complete enough
to drive a build. `examples/` is pruned before running so there's nothing to copy; git holds the old
(superseded) reference if ever needed.

> Four full pipeline builds is a lot for one session — if context runs short, do one build per session
> (same prompt, one target at a time). Build #4 needs Docker (testcontainers + the Compose stack) and
> takes the longest.

**Run history.** #1, #2, #3-jay-z: run 2026-07/08 (findings promoted into the profiles). #4
roselabs-blog: **not yet run cold** — it was built in the same session as its profile, so `saas-web`
has not been proven from the profile alone.

---

```
You are building four example services from scratch using this repo's pipeline, to prove the pipeline +
profiles produce correct, gated builds from the profile alone. CLEAN-ROOM: you have not seen the answers.

## The clean-room boundary (hard rules — all four builds)
- You MAY read the machinery, fully: skills/ (incl. review-gate), checks/, graders/, profiles/ (all of
  it: CONTRACT.md, generic-saas/, edge-telemetry/, saas-web/, personal/jay-z/), doc-patterns/, codemods/.
- examples/ is EMPTY (pruned to seal this test). Do NOT reconstruct any prior build — not from disk, and
  NOT from git history (no git show / log / restore / checkout of old examples/ content). Build fresh.
- The profile is the ONLY source of domain content. If a build needs something the profile doesn't supply,
  that's a FINDING — surface it in that build's docs/assumptions.md, don't invent it into the spec.

## What to build (four services, four dirs)
Each build dir starts with a `.pipeline-profile` file naming its profile (this is how the pipeline
resolves the active profile — there is no default):
1. examples/multi-tenant-isolation/   — `domain: generic-saas`
   A multi-tenant SaaS projects API — a caller only ever sees its own workspace's projects; no cross-tenant
   leak. Hard-done: no cross-tenant leak on any verb.
2. examples/edge-telemetry-alerting/  — `domain: edge-telemetry`
   An industrial edge telemetry monitor + alerting dashboard. Hard-done: no missed critical alert; a stale
   sensor renders "— stale", never a number or nominal.
3. examples/jay-z-projects/           — `domain: generic-saas` + `overlay: personal/jay-z` (additive-only)
   The same multi-tenant projects API as #1, but built under the jay-z personal overlay — every comment
   carries the voice AND stays doctrine-clean. Hard-done: same as #1, plus the voice.
4. examples/roselabs-blog/            — `domain: saas-web`
   A multi-author blog: invited authors write and publish posts (rich HTML rendered in a sandboxed
   iframe), public readers browse published posts by tag and submit plain-text comments that render only
   once moderated. Deployed as a Docker Compose stack (api · db · web) behind Caddy. Hard-done: no draft
   or unpublished post is readable by a public request, on any path (list · slug · tag · feed); no
   pending/hidden comment ever serializes publicly.

## For EACH build, run the pipeline honestly
1. GATE 0 — profile-completeness: the active profile resolves from `.pipeline-profile`; every must-slot
   filled; both flags (has_ui, deploys) set; every check row present or declared n/a. Empty slot,
   dangling ref, unresolved profile, or malformed grader → STOP and report; don't work around it.
2. Frame → Plan → Implement per skills/. Produce BOTH the code AND the living docs (doc-patterns/living-docs
   — current-state, backlog, assumptions, decisions).
3. review-gate (skills/review-gate/SKILL.md): the auto-fix arm, then the checks in the order
   checks/README.md fixes (commands from the profile's check-commands.md), short-circuit; then the ~4
   graders in parallel (feature · drift · docs-currency · simplicity; + jay-z-voice for #3), fix once,
   re-grade. On the core promise, run the adversarial N-vote.
   Runtime floor per build: smoke for #1/#3 (deploys: false, has_ui: false); browser for #2; infra +
   browser for #4 (deploys: true, has_ui: true — build the images, up on a fresh volume, migrate from
   empty, smoke through the proxy, then Playwright on the live stack).

## Report at the end (per build)
- GATE-0 result + any profile gaps hit (the real output — profile bugs to promote).
- Where the profile was ambiguous (logged to assumptions.md, not invented).
- Checks' and graders' final state (green / residual handed off).

Start by reading the machinery. Build the four into their four dirs. Do not reconstruct the pruned examples/.
```

---

When the builds are back, bring the per-build reports here — any new profile gaps get promoted (the
hill-climb continues), then the fresh examples get committed to replace the old reference, and the run
history above is updated.
