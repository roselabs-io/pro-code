# personal-profile — jay-z

A **demo** personal overlay: docstrings and comments carry Jay-Z's voice. It shows two things at once —
(1) the pipeline *adapting* to a wildly specific taste, and (2) the **additive-only** guardrail holding
(it layers a style bar on top of the comment doctrine; it does **not** relax it). See
[`../../CONTRACT.md`](../../CONTRACT.md) → *Two kinds of profile*.

## extra_rubric
- **Voice** — every new/changed docstring or comment carries **Jay-Z's voice** (confident, NYC cadence, a
  little wordplay) **while staying comment-doctrine-compliant**: still one line, still states *what the
  code is*, still no why-not / history / ticket-ref. Swagger in the *phrasing*, never in the *length* or
  the *content*. Enforced by [`graders/jay-z-voice.md`](graders/jay-z-voice.md).

## graders/
- [`jay-z-voice.md`](graders/jay-z-voice.md) — a **fuzzy** profile-authored grader (counts against the ~3
  fuzzy budget). Additive: it can only *fail a comment for lacking the voice*, never *pass one the comment
  doctrine rejects*.

## notes
This is a taste overlay, not a domain profile — it re-supplies **nothing** (no sources, no catalog, no
check-commands). It composes on top of whatever domain profile is active (`generic-saas`,
`edge-telemetry`, …). If you tried to make it *loosen* the doctrine (allow bars-length rap comments),
GATE-0 would reject it as a relaxation — which is the point.
