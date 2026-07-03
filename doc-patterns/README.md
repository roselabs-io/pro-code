# doc-patterns — the neutral doc skeletons

Every markdown the pipeline reads or writes starts from a template here. The templates are **domain-neutral** (`{{project_name}}`, `{TODO}` placeholders); a profile and a project fill them. They're grouped by the role each one plays.

| Folder | Role | Files |
|---|---|---|
| [`specs/`](specs/) | **What the pipeline produces** — the spec, written as it frames and plans. | `functional-analysis.md`, `ui-sketch.md` (Frame) · `system-overview.md`, `surface-spec.md` (Plan) |
| [`living-docs/`](living-docs/) | **Memory kept current across the build** — what's built, what's left, why, and what it silently assumed. Graded for currency. | `current-state.md`, `backlog.md`, `decision-record.md`, `assumptions.md` |
| [`guides/`](guides/) | **Standing feedforward** — the values and quality bar the code is written against. | `principles.md`, `cfrs.md` |
| [`doctrines/`](doctrines/) | **Enforced posture** — opinionated rules the code is held to, checked by the doctrine linter + the drift grader. | `comment-doctrine.md`, `test-posture.md`, `readme-doctrine.md` |
| [`harness/`](harness/) | **Grader + CLI scaffolding** — the structured events a grader reads, and the command entry points. | `log-taxonomy.md`, `justfile` |

## specs — the doc-set the pipeline produces

The output of Frame and Plan: a functional analysis (what the system does), a UI sketch (the screens, for a UI-bearing profile), a system overview (the shape), and a per-surface spec (one drill-down each). These are the guides the next phase builds against.

## living-docs — the second artifact

A build produces two artifacts, not one: the **code**, and the **context**. The living docs are the context — the memory the next agent (or the next session) reads to orient. `current-state.md` says what's built now, `backlog.md` is the forward-only record of remaining work, each `decision-record.md` captures a non-obvious call and its reasoning, and `assumptions.md` — the **assumptions ledger** — records the choices the build made that no input specified (a default the agent reached for from habit or priors), each with a disposition. They're maintained *every ticket*, and the loop's **docs-currency grader** checks them alongside the code — stale memory is a gradable defect, not a cosmetic one. (A project's `open-questions.md` and its updated `surfaces/` specs are living docs too, by the same rule.)

The assumptions ledger is the antidote to **silent bias**: a profile's *declared choice-points* (its Stack + layout + Conventions) fix the intended defaults up front, and the drift grader's undeclared-choice lens routes anything the build chose *outside* that set into the ledger — so a prior leaking in from the agent's context becomes visible and vetoable instead of invisible.

## guides — standing feedforward

`principles.md` (the values that bias a decision at a fork the rules didn't foresee) and `cfrs.md` (the cross-functional requirements — the "-ilities" — each mapped to a verifiable check). Supplied up front, before any code.

## doctrines — enforced posture

The opinionated rules a profile mandates: `comment-doctrine.md` (comments state what the code is, not its history or a ticket number), `test-posture.md` (every test asserts; the layers a domain owes), and `readme-doctrine.md` (every service ships a README with launch instructions). The regex-able floor is enforced deterministically by [`graders/checks/doctrine_lint.py`](../graders/checks/doctrine_lint.py); the judgment cases are the drift grader's.

## harness — grader + CLI scaffolding

`log-taxonomy.md` defines the structured events the code emits and the logs grader reads back (proving behaviour from the trace, not the return value). `justfile` is the CLI skeleton — one named target per action, so the graders and a person run the same commands.

---

The split maps to the feedforward/feedback frame the pipeline is built on: **specs**, **living-docs**, **guides**, and **doctrines** are feedforward (they shape the work up front); **harness** carries the pieces feedback reads. See [../two-reading-journeys.md](../two-reading-journeys.md) for that frame.
