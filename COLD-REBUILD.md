# Cold rebuild — the clean-room pipeline test (all three examples)

Paste the block below into a **fresh** Claude Code session at the pro-code repo root. It builds all three
example services **from the pipeline + profiles alone** — the honest proof that the profiles are complete
enough to drive a build. `examples/` is pruned before running so there's nothing to copy; git holds the old
(superseded) reference if ever needed.

> Three full pipeline builds is a lot for one session — if context runs short, do one build per session
> (same prompt, one target at a time).

---

```
You are building three example services from scratch using this repo's pipeline, to prove the pipeline +
profiles produce correct, gated builds from the profile alone. CLEAN-ROOM: you have not seen the answers.

## The clean-room boundary (hard rules — all three builds)
- You MAY read the machinery, fully: skills/, graders/, profiles/ (all of it: CONTRACT.md, generic-saas/,
  edge-telemetry/, personal/jay-z/), doc-patterns/, codemods/.
- examples/ is EMPTY (pruned to seal this test). Do NOT reconstruct any prior build — not from disk, and
  NOT from git history (no git show / log / restore / checkout of old examples/ content). Build fresh.
- The profile is the ONLY source of domain content. If a build needs something the profile doesn't supply,
  that's a FINDING — surface it in that build's docs/assumptions.md, don't invent it into the spec.

## What to build (three services, three dirs)
1. examples/multi-tenant-isolation/   — profile: generic-saas
   A multi-tenant SaaS projects API — a caller only ever sees its own workspace's projects; no cross-tenant
   leak. Hard-done: no cross-tenant leak on any verb.
2. examples/edge-telemetry-alerting/  — profile: edge-telemetry
   An industrial edge telemetry monitor + alerting dashboard. Hard-done: no missed critical alert; a stale
   sensor renders "— stale", never a number or nominal.
3. examples/jay-z-projects/           — profile: generic-saas + the personal/jay-z overlay (additive-only)
   The same multi-tenant projects API as #1, but built under the jay-z personal overlay — every comment
   carries the voice AND stays doctrine-clean. Hard-done: same as #1, plus the voice.

## For EACH build, run the pipeline honestly
1. GATE 0 — profile-completeness against the active profile (+ the overlay for #3). Empty (must) slot,
   dangling ref, or malformed grader → STOP and report; don't work around it.
2. Frame → Plan → Implement per skills/. Produce BOTH the code AND the living docs (doc-patterns/living-docs
   — current-state, backlog, assumptions, decisions).
3. Verify loop: deterministic graders first (commands from the profile's check-commands.md — lint · tests ·
   type-check · doctrine-lint · special-lint · security · coverage · deps · [codemod for #1/#3] · logs ·
   [browser for #2]), short-circuit; then the ~3 fuzzy graders (feature · drift · docs-currency; + jay-z-voice
   for #3), fix once, re-grade. On the core promise, run the adversarial N-vote.

## Report at the end (per build)
- GATE-0 result + any profile gaps hit (the real output — profile bugs to promote).
- Where the profile was ambiguous (logged to assumptions.md, not invented).
- Graders' final state (green / residual handed off).

Start by reading the machinery. Build the three into their three dirs. Do not reconstruct the pruned examples/.
```

---

When the builds are back, bring the per-build reports here — any new profile gaps get promoted (the
hill-climb continues), then the three fresh examples get committed to replace the old reference.
