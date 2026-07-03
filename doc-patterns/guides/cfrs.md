# {{project_name}} — Cross-Functional Requirements (CfRs)

> **CfRs** (feedforward, ✨): the *"-ilities"* — the quality bar that
> cuts across every feature. Named here so they're **gradeable**, not left implicit.
> The frame/plan graders consume this: a CfR that bites must map to a verifiable check.
> Pulled from `doc-patterns/guides/cfrs.md`; the profile declares which -ilities bite this build.

## The -ilities

Score each: **bites** (a hard requirement for this build) · **baseline** (a default, not a hard target) · **n/a**.

| CfR | Bites? | The bar (verifiable) | Graded by |
|---|---|---|---|
| Security | {TODO} | {TODO: e.g., "no cross-tenant read/write; asserted by an isolation test"} | test / review |
| Reliability / Safety | {TODO} | {TODO: e.g., "no missed critical alert; fixture-replay"} | test |
| Performance | {TODO} | {TODO: e.g., "p95 < 200ms"} | load check |
| Observability | {TODO} | {TODO: e.g., "every state change emits a structured log the logs-grader reads"} | logs grader |
| Accessibility | {TODO} | {TODO} | browser grader |
| Scalability | {TODO} | {TODO} | — |
| Maintainability | {TODO} | {TODO: e.g., "lint + type clean; comment-doctrine"} | static analysis |

> A **biting** CfR with no verifiable bar is a 🔴 for the plan grader — the same rule as a
> functionality with no test. The -ilities are requirements, so they get graders too.
