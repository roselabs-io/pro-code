# personal-profile — `{name}`

A **personal overlay** — your reviewing taste, layered on top of whatever domain profile is active. Copy
to `profiles/personal/<name>/personal-profile.md` and fill only what you want. See
[`../CONTRACT.md`](../CONTRACT.md) → *Two kinds of profile*.

> **Additive-only.** You may **add** rubric rows, grader units, and `doctrine_lint` forbids. You may
> **not** relax or remove a domain or agnostic rule — an overlay can only hold you to *more*, never less.
> You don't re-supply the domain hooks; those come from the active domain profile.

## extra_rubric *(may)*
Extra drift-grader rows for your work — domain-agnostic only (domain shapes belong in the domain profile).
- {TODO: e.g. "prefer early returns over nested conditionals" — or delete this section}

## extra_forbids *(may)*
Extra `doctrine_lint --forbid` rules (regex-able).
- {TODO: e.g. `--forbid 'TODO@@no TODO left in a merge'` — or delete}

## graders/ *(may)*
Drop profile-authored grader units here (copy [`grader.md`](grader.md)). They compose with the agnostic +
domain graders (the ~3 fuzzy budget still applies — see CONTRACT). Delete the dir if you ship none.

## notes *(may)*
{TODO: anything about how you like reviews framed — or delete}
