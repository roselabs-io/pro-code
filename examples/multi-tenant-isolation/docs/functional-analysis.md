# Multi-tenant Projects API — Functional Analysis

> The behavioural spec: what this system does, in business terms. Frame's output.
> Filled per the `generic-saas` profile.

## Identity

- **Product:** a multi-tenant SaaS **Projects API** — backend only, no frontend.
- **Driver / owner:** the pro-code pipeline (regeneration run).
- **Primary goal:** let many workspaces share one deployment while each workspace's data stays
  **completely invisible** to every other — the isolation invariant is the product.

## Actors

| Actor | Role / privilege | Goals | Surfaces they touch |
|---|---|---|---|
| Member | `member` | create / read / update / list projects **in their own workspace** | the Projects endpoints |
| Admin | `admin` | everything a member does **plus delete** a project | the Projects endpoints |
| Token issuer *(upstream)* | mints signed bearer tokens carrying `{workspace, actor, role}` | authenticate callers | (out of repo — an integration boundary) |

## Top-level workflows

- **Create + manage a project:** a member presents a bearer token → `POST /projects` creates a
  project in the caller's workspace → `GET /projects` lists only that workspace's projects →
  `PATCH /projects/{id}` edits one → an admin `DELETE /projects/{id}` removes one.
- **A cross-tenant access attempt:** a caller in workspace A references a project id belonging to
  workspace B → the API responds exactly as if the id did not exist (404), and records the denial.

## Data model (business terms)

- **Workspace** — the tenant boundary. Not CRUD-managed here; the caller's workspace is asserted by
  the token (an upstream identity provider owns workspace lifecycle).
- **Project** — a named record owned by exactly one workspace. Fields: name, description, creator.
- **Caller** — the resolved identity of a request: workspace, actor, role.

## Integrations

- **Token issuer** — inbound; a signed bearer token per request carries the workspace + actor +
  role claims. Contract: `Authorization: Bearer <signed token>`; an invalid/absent token → 401.
  *(The issuer itself is out of repo — see open-questions.)*

## Functionalities

- **F1 — Create a project** (scoped to the caller's workspace).
- **F2 — Read a project** by id (own workspace only).
- **F3 — List projects** (own workspace only; paginated).
- **F4 — Update a project** (own workspace only).
- **F5 — Delete a project** (admin only; own workspace only).
- **F6 — Tenant isolation** — no cross-tenant read/list/write, ever; a cross-tenant id is
  indistinguishable from not-found. *The core promise; its own functionality, not a clause.*
- **F7 — Authentication** — resolve every request to a Caller at the boundary; reject unsigned.
- **F8 — Denial observability** — every cross-tenant / role denial emits a structured event.

## Metrics + non-functionals

- **Tenant isolation (hard requirement)** — certified by an isolation test (F6). No exceptions.
- **Observability** — every denied cross-tenant attempt emits `CROSS_TENANT_DENIED`.
- **Maintainability** — lint + comment-doctrine clean.

---
*Optional sections omitted (no contested scope, no explicit compliance regime beyond isolation).*
