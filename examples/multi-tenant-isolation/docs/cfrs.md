# Multi-tenant Projects API — Cross-Functional Requirements

> The -ilities that cut across every feature, named so they're gradeable. A biting CfR with no
> verifiable bar is a 🔴 for the plan grader.

| CfR | Bites? | The bar (verifiable) | Graded by |
|---|---|---|---|
| Security | **bites** | no cross-tenant read/list/write; a foreign id is 404 == pure-miss; asserted by `test_isolation.py` | isolation test + N-vote |
| Reliability | baseline | endpoints return typed envelopes, no bare 500 for expected failures | integration tests |
| Performance | n/a | in-memory slice; no latency target set | — |
| Observability | **bites** | every denied cross-tenant attempt emits `CROSS_TENANT_DENIED`; every write emits a `PROJECT_*` event | logs grader (`test_logs_grader.py`) |
| Accessibility | n/a | API-only, no UI (`has_ui: false`) | — |
| Scalability | baseline | list is cursor-paginated (unbounded-safe) | `test_pagination.py` |
| Maintainability | **bites** | ruff clean (E,F,I,B); comment-doctrine clean; boundary-dep codemod passes | ruff + doctrine_lint + codemod |

> The three biting CfRs — Security, Observability, Maintainability — each map to a running check,
> so none is a hand-wave.
