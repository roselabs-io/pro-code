# {{project_name}} — Comment Doctrine

> A **Rule** (feedforward). Comments state **what the code IS**, never the
> why-not, the history, or a ticket number. The durable home for *why* is the commit / ADR;
> inline bloat is noise every future reader has to read past.
> Pulled from `doc-patterns/doctrines/comment-doctrine.md`. The **regex-able subset is enforced
> deterministically** (`graders/checks/doctrine_lint.py`); the judgment cases are the fuzzy
> drift grader's job.

## Banned (the deterministic floor — the linter flags these)

- **Inline ticket refs** — `T1`, `COM-1234`. Put the traceability in the commit.
- **Backward-narration** — "previously / used to / no longer / renamed from / originally …". A comment describes the present, not the diff.
- **Defensive why-not** — "we don't X / why not Y". If the *why* matters, it's an ADR, not a code comment.

## Discouraged (the fuzzy drift grader's judgment call)

- A comment that **re-justifies a settled decision** or argues the alternative.
- A **3-line essay** where one line states the fact.
- **Docstrings that narrate reasoning** ("… so it stays reachable because …") instead of stating what the unit does. (Agent-authored diffs over-comment the worst — hold the line hardest there.)

## Keep

- A one-line **non-obvious why** that prevents a wrong edit ("404 before 403 so a cross-tenant id can't leak existence").
- What a unit **is / does**, in the imperative.

## Escape hatch

A line (or comment) containing `doctrine: allow` is exempt — for the rare legitimate case (a module that genuinely must `print`, an enum whose values are strings). Use it sparingly; it's visible in review.
