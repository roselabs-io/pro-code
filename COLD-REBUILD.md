# Cold rebuild — the clean-room pipeline test

Paste the block below into a **fresh** Claude Code session at the pro-code repo root. Its job: rebuild one
example service **from the pipeline + profile alone** — an honest test that the profile is complete enough
to drive a build. A rebuild by an agent that has *seen* the existing example proves nothing (it would just
reproduce it). A blank agent, forbidden from looking, is the real proof: **if the profile passes GATE-0, a
cold agent can build the example from it.**

Fill the two `{...}` slots, then paste.

---

```
You are building a service from scratch using this repo's pipeline. This is a CLEAN-ROOM test — the whole
point is to prove the pipeline + profile can produce the build without you having seen the answer. Read
nothing into this beyond what's written.

## The clean-room boundary (hard rules)
- You MAY read the machinery, fully: skills/ (the pipeline), graders/, profiles/<PROFILE>/ +
  profiles/CONTRACT.md, doc-patterns/, codemods/.
- You MUST NOT read anything under examples/. Those are existing reference builds — opening one is
  cheating. If you catch yourself reaching for examples/, stop. Build fresh.
- Do NOT assume domain knowledge that isn't in the profile. The profile is the ONLY source of domain
  content. If the build needs something the profile doesn't supply, that's a FINDING — surface it, don't
  invent it. Inventing to fill a gap defeats the test.

## What to build
- Target: {ONE LINE — e.g. "a multi-tenant SaaS projects API" — or "whatever the profile's `sources` imply"}
- Active profile: {PROFILE — e.g. `generic-saas`  |  `edge-telemetry`  |  `generic-saas` + `personal/jay-z` overlay}
- Build into a NEW dir: examples-rebuild/{name}/  — never touch examples/ (the reference stays intact for a later diff).

## Run the pipeline honestly
1. GATE 0 — run graders/profile-completeness.md against profiles/<PROFILE> (+ any personal overlay). If a
   (must) slot is empty, a ref dangles, or a grader is malformed → STOP and report it. A profile that fails
   GATE-0 is the test surfacing a real gap, and that's a useful result — not something to work around.
2. Frame → Plan → Implement, per skills/. Produce BOTH artifacts: the code AND the living docs
   (doc-patterns/living-docs — current-state, backlog, assumptions, decisions).
3. At Implement, run the code-verification loop: deterministic graders first (commands from
   profiles/<PROFILE>/check-commands.md — lint · tests · type-check · security · coverage · deps ·
   doctrine-lint), short-circuit, then the ~3 fuzzy graders (feature · drift · docs-currency), fix once,
   re-grade. If a personal overlay is active, its additive graders (profiles/personal/<name>/graders/) run
   too and can only tighten, never wave anything through.

## Report at the end
- GATE-0 result + any profile gaps you hit.
- Every place the profile was ambiguous or under-specified — these are the real output: they're profile
  bugs to fix, and the reason to run this cold.
- The graders' final state (all green / residual handed off).
- Anything you *wanted* from examples/ but couldn't take — each is a signal the profile under-specifies it.

Start by reading the machinery. Do not touch examples/.
```

---

## Notes

- **The jay-z run** = `PROFILE: generic-saas` + the `personal/jay-z` overlay. Same domain build, but the
  `jay-z-voice` grader is live — a cold agent, handed only the grader's rubric, has to make the comments
  carry the voice *and* stay doctrine-clean (additive-only). That's the fun one, and it's a real test of
  the Level-3 personal-overlay mechanism.
- **Why `examples-rebuild/` (not `examples/`)**: it preserves the reference build, so afterward you can
  **diff cold-rebuild vs reference** — another independent-derivation check on the *profile* the way the
  grader compare was on the *graders*. Convergence = the profile is complete; divergence = the profile
  under-specifies where they differ.
- **What "passes"**: not "byte-identical to the reference" — a different-but-valid build that greens the
  same graders *is* a pass. What you're watching for is the profile-gap report: an empty gap list means the
  profile drove the whole build on its own.
