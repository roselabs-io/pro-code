# multi-tenant-isolation — Cross-Functional Requirements (CfRs)

> The "-ilities" — the quality bar cutting across every feature, named so they're gradeable.
> Pulled from `doc-patterns/guides/cfrs.md`; the `generic-saas` profile declares which bite.

## The -ilities

| CfR | Bites? | The bar (verifiable) | Graded by |
|---|---|---|---|
| Security | **bites** | no cross-tenant read/write on any verb; a cross-tenant id → 404 and no other-workspace row ever serializes | isolation integration test + adversarial N-vote |
| Reliability / Safety | baseline | CRUD returns typed errors, no bare 500 on expected failures | tests |
| Performance | n/a | — (in-memory slice; no load target) | — |
| Observability | **bites** | every cross-tenant denial emits `CROSS_TENANT_DENIED{workspace,target}`; every write emits `PROJECT_*` | logs grader |
| Accessibility | n/a | API-only, no UI | — |
| Scalability | baseline | list is cursor-paginated (no unbounded offset scan) | pagination test |
| Maintainability | **bites** | lint + comment-doctrine clean; changed-line coverage ≥ 80% | ruff · doctrine_lint · coverage |

> A **biting** CfR with no verifiable bar is a 🔴 for the plan grader. Security, Observability, and Maintainability all carry a concrete, test-assertable bar above.
