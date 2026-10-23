---
consumed_by: ["review"]
canonical_for: "the jay-z voice rubric"
profile: personal
---

# jay-z-voice — profile-authored review lens unit

Checks that new/changed docstrings and comments carry **Jay-Z's voice** — *on top of* the comment
doctrine, never instead of it. Copy-target contract: [`../../../_skeleton/grader.md`](../../../_skeleton/grader.md). Applied by the one review after the agnostic and domain lenses.

## rubric_source
Inline (below). The orchestrator injects this text into the review's prompt.

> **Voice:** confident, NYC cadence, a little wordplay/swagger — the tone of a line like *"I'm not a
> businessman, I'm a business, man."* Applied to what the code *does*.
> **Hard constraints (inherited, not relaxable):** stays **one line**; states **what the code is**;
> **no** why-not / history / ticket-ref / essay. Swagger lives in the *phrasing*, never the *length* or
> the *content*. Clarity wins ties — if the flavor obscures what the code does, it failed.

## what it checks
For each new/changed docstring or comment in the diff:
- **has the voice?** A plain, flavorless-but-correct comment → **finding: "add the voice."**
- **still doctrine-compliant?** This lens does **not** judge that (the comment doctrine does). If a
  comment went full rap-verse — multi-line, narrating history — the **comment doctrine fails it**,
  and this lens **cannot** override that. Additive-only: it can withhold a pass for lack of voice; it
  can never grant one the doctrine rejects.

## examples
| Verdict | Comment |
|---|---|
| ✅ voice + doctrine | `# No token, no entry — pull the caller straight off the bearer.` |
| ✅ voice + doctrine | `"""Reset the counter on overflow — hit the ceiling, wipe the slate, back to zero."""` |
| ⚠️ finding: no voice | `# Return the caller for this bearer token.` *(correct, but flavorless)* |
| ❌ doctrine fails (not this lens's call) | a 4-line verse narrating *why* the old approach was dropped — the comment doctrine rejects it; this lens can't save it. |

## contract
```
findings for lens jay-z-voice: [{file, line, issue: "no voice", fix}]
```
- **pass** = every new/changed comment carries the voice *and* is doctrine-compliant.
- a comment that is doctrine-*failing* is not this lens's finding — it's the doctrine's. This lens
  only ever adds the "needs voice" finding.

## authoring discipline
One responsibility (voice), few. It rides the comment doctrine; it never contradicts it. This is
the additive-only rule made concrete: a personal lens **tightens** (demands more — voice *and* the
doctrine), it never **loosens**.
