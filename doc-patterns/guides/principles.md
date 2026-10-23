# {{project_name}} — Principles

> **Principles** (feedforward, ✨ inferential): the high-level *values*
> that bias every decision, before any rule or ticket. Broad and soft — a rule says
> "always do X"; a principle says "when in doubt, lean this way."
> Pulled from `doc-patterns/guides/principles.md`; the profile supplies the domain's values.

## Universal (hold in every domain)

- **Checks first, one review.** Every diff passes the deterministic checks, then one review by a session that did not write it.
- **Author ≠ reviewer.** Nothing reviews its own work; a fresh reader has fresh priors.
- **No done without fresh evidence.** "Should pass" is not "passed this session."
- **Fail loudly.** A silent wrong answer is worse than a loud stop.
- **Every correction given twice is a missing check.** Encode it as a check or a rubric line; don't re-nag.

## Domain values (from the profile)

The profile lists the values that bias *this* domain's forks — e.g.:

- {TODO: e.g., "Deny by default — an unscoped path must return nothing, not leak."}
- {TODO: e.g., "Missing data is a fact, not a gap — absence alerts."}

> Principles are the tie-breaker at a fork the rules didn't foresee. When a ticket, a rule,
> and a principle disagree, surface it — don't silently pick.
