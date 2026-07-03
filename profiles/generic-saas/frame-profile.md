# Profile — `generic-saas` · Frame

Domain: a CRUD SaaS backend — **Python + FastAPI, API-only** (no frontend). The **default** profile.

## Sources (where Frame's context comes from)

| Source | Provides |
|---|---|
| Product brief / PRD | goal, primary actors, headline features |
| Issue tracker / backlog seed | in-flight scope, known constraints |
| API contract / OpenAPI notes | the endpoints, payload shapes, auth-failure responses |
| Founder / PM interview *(brainstorm mode)* | everything, when no brief exists |

## Functional-analysis sections

- **Required:** Identity · Actors · Top-level workflows · Data model · Integrations · Functionalities · Metrics.
- **Optional (add only if they bite):** Out-of-scope, Compliance / security.

## Hard gates

- **Isolation rules** — for a multi-tenant product, the tenant-scoping rules **and** the cross-tenant denied response (404 vs 403) must be pinned before Plan. Unspecified = 🔴 blocking: it's the core promise, and Plan can't decompose "enforce isolation" without it.

## Principles + CfRs (feedforward guides)

- **Principles** (`doc-patterns/guides/principles.md`): *deny by default* — an unscoped query returns nothing, not a leak; *enforce at the boundary, not the caller*.
- **CfRs that bite** (`doc-patterns/guides/cfrs.md`): **Security** (tenant isolation — hard, isolation test), **Observability** (every denied cross-tenant attempt logs a structured event), **Maintainability** (lint + comment-doctrine). A biting CfR with no verifiable bar is a 🔴 for the plan grader.
- **`has_ui`:** false — API-only; no UI sketch and no browser grader (that's the `edge-telemetry` profile's territory).

## Grader bar (consumed by `frame-completeness`)

- **`verifiable_means`:** an automated test can assert it (unit / integration), or a schema validates it.
- **`usual_silent_gaps`** — probe these; SaaS briefs routinely omit them:
  - non-happy-path responses: empty result, error, permission-denied
  - the actor model beyond the primary user (admin, billing, support)
  - integration contracts (what the webhook payload *is*; what an auth failure returns)
  - multi-tenancy / isolation rules, if the product is multi-tenant
- **clean-handoff bar:** functional-analysis carries actors · workflows · data model · integrations · functionalities · metrics (stubs ok); open-questions logs every biting assumption with owner + stakes; isolation rules pinned (scoping + denied-response) for a multi-tenant product.
