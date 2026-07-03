---
name: frame
description: "Phase 1 — turn upstream material, or an interactive brainstorm when there's none, into a reviewed spec (functional analysis + open questions) that Plan can consume."
---

# Frame (phase 1 — the spec)

Frame turns whatever context exists into a **reviewed spec** the downstream phases build against. It's the first phase and the highest-leverage one: a vague or wrong spec here compounds through Plan and Implement, so Frame **closes with a grader** — [`graders/frame-completeness.md`](../../graders/frame-completeness.md) — before anything hands off.

Frame is **domain-neutral by design.** *What* questions to ask, *what* sources to expect, and *what* sections a spec needs come from a **profile** (`profiles/<domain>/`), not from this skill. This skill is the **mechanism**; the profile is the **content**. Default profile: `generic-saas`.

## Two modes

- **Digest** — material exists (a brief, transcripts, notes, tickets). Read it, fold it into the spec.
- **Brainstorm** — nothing exists (an internal tool, a fresh idea). Interview the driver: one question at a time, propose 2–3 approaches at the forks, co-produce the spec.

Not one-shot. **Incremental and cumulative** — read what's there, fold in what's new, leave the rest open.

## The discipline (holds in both modes)

- **Behaviour, not engineering.** Capture *what the system does*. Surface assumptions; don't author code or pick patterns.
- **Frame seeds, Plan decides.** Design/architecture hunches *will* surface. Don't suppress them, don't bake them into the spec — park them as hypotheses for Plan.
- **Pull, don't conjure.** Start each artifact from its template (`doc-patterns/`), filled per the active profile. Don't invent the shape.
- **One question at a time** (brainstorm). No questionnaires — ask, fold, ask next. Prefer multiple-choice.

## What you produce

The spec is a **doc-set**, not one master file. The active profile names the exact set; the `generic-saas` default:

| Artifact | Content |
|---|---|
| `docs/functional-analysis.md` | what the system does — actors, workflows, data model, integrations, functionalities, metrics. Template: [`doc-patterns/specs/functional-analysis.md`](../../doc-patterns/specs/functional-analysis.md). |
| `docs/open-questions.md` | every assumption that could bite the build — state + owner + stakes. Also holds the **Design seeds → Plan** bucket. |
| *(profile-added)* | e.g. a UI sketch for any app with a user-facing surface — the profile declares it and whether it's a hard gate. |

Docs are **collaborative + cumulative**. Read before adding; append open-questions, refine functional-analysis. Don't overwrite a section unless correcting it against new input.

## Fill the spec

Walk the sections the active profile defines, asking only what the inputs (or the driver) don't already answer. Keep entries tight. **A half-filled section is worse than an empty one** — don't fill to fill.

The `generic-saas` required sections: **Actors · Top-level workflows · Data model · Integrations · Functionalities · Metrics.** (Details + which are optional: [`profiles/generic-saas/frame-profile.md`](../../profiles/generic-saas/frame-profile.md).)

## Park what spills

Mid-frame you'll surface things that aren't the spec — an architecture idea, a whole future feature, "the brief is wrong." **Grasp → categorize → route:** drop each in the bucket its owning phase consumes, then keep framing.

- architecture / design idea → open-questions › **Design seeds → Plan** (a hypothesis, not a decision)
- a whole future feature → the backlog
- the brief is wrong → a surprises / decisions log

## Close — run the completeness grader

Frame **doesn't trail off.** Before handoff, run the frame-completeness ceremony ([`graders/frame-completeness.md`](../../graders/frame-completeness.md)): a completeness estimate, a 🟢/🟡/🔴 scorecard framed by *downstream cost*, targeted gap-pointing, and an explicit two-path sign-off (close the top gaps now / sign off under-bar and log every gap). The ceremony is agnostic; the **profile supplies the bar** — what "verifiable" and "complete" mean in this domain.

## What you do NOT produce

- No decomposition, backlog, or tickets — **Plan.**
- No design-pattern picks or system architecture — **Plan.**
- No code.

If you catch yourself writing "use Postgres" or "a state machine here," stop — park it in **Design seeds → Plan**, or let it go. It stays out of the spec.
