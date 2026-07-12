# jay-z-projects — Functional Analysis

> The behavioural spec: **what this system does**, in business terms.
> Not engineering — no patterns, no schema, no code. Those are Plan's job.
> Pulled from `doc-patterns/specs/functional-analysis.md`; filled per the `generic-saas` profile.

## Identity

- **Product:** a multi-tenant SaaS **projects API** — each workspace owns its projects; a caller only ever sees its own workspace's projects.
- **Driver / owner:** platform team (clean-room build).
- **Primary goal:** serve project CRUD to many tenants over one API with **no cross-tenant leak on any verb** — the core promise.

## Actors

Who interacts with the system, and with what privilege.

| Actor | Role / privilege | Goals | Surfaces they touch |
|---|---|---|---|
| Member | `member` — read + create/update projects in own workspace | manage the workspace's projects | `projects` API |
| Admin | `admin` — member rights **plus** delete | curate + prune the workspace's projects | `projects` API |
| (Attacker) | a valid caller of workspace A probing workspace B's ids | learn or touch another tenant's data | `projects` API (must fail closed) |

> Identity is carried by a **signed bearer token** that resolves to a `Caller{workspace_id, role, subject}`. There is no sign-up / user-management surface in this slice — tokens are minted out-of-band (an assumption; see open-questions).

## Top-level workflows

- **Authenticated CRUD:** caller presents a bearer token → the API resolves it to a `Caller` → the caller lists / creates / reads / updates / deletes projects, **all scoped to the caller's workspace**.
- **Cross-tenant attempt (must fail closed):** caller of workspace A requests a project id that belongs to workspace B → the API responds as if the id does not exist (**404**), never revealing B's data or its existence, on **every** verb.

## Data model (business terms)

- **Workspace** — a tenant boundary; owns projects. Identified by `workspace_id`.
- **Caller** — the resolved identity behind a request: `workspace_id`, `role` (member | admin), `subject`.
- **Project** — the unit of work: `id`, `workspace_id` (owner), `name`, `description`, `created_at`. Belongs to exactly one workspace.

## Integrations

External systems this one talks to. One line each: what, direction, protocol/contract.

- **Token issuer** — inbound; the bearer token is signed by an external issuer with a shared secret. This slice only **verifies** tokens (it does not mint them). Contract: a signed JWT whose claims carry `workspace_id`, `role`, `sub`. *(Signing algorithm is a build choice — see assumptions.)*
- *(No payment, email, or webhook integration in this slice.)*

## Functionalities

Broad strokes of what the system does — one line per major capability. Plan decomposes each into ≥1 ticket.

- **Authenticate a request** — resolve a bearer token to a `Caller`; **fail closed** when the key is missing/invalid or the token is bad.
- **List projects** — return the caller's workspace's projects, **cursor-paginated** (unbounded list).
- **Create a project** — write a project owned by the caller's workspace; validate the body.
- **Read a project** — fetch one project by id, scoped to the caller's workspace.
- **Update a project** — patch a project's mutable fields, scoped to the caller's workspace.
- **Delete a project** — remove a project, scoped to the caller's workspace; **admin-only**.
- **Enforce tenant isolation** — every read/write scopes to the caller's workspace; a cross-tenant id returns 404 on every verb, and **no other-workspace row ever serializes**. *(The core promise — its own functionality, not a clause.)*
- **Audit cross-tenant denials** — every denied cross-tenant attempt emits a structured log event (`CROSS_TENANT_DENIED{workspace,target}`), so isolation is provable from the trace.

## Metrics + non-functionals

- **Tenant isolation** — hard requirement; asserted by an integration test on every verb + an adversarial N-vote on the core promise.
- **Observability** — every cross-tenant denial emits a structured event (Observability CfR).
- **Maintainability** — lint + comment-doctrine clean; changed-line coverage ≥ 80%.

---
*Optional sections — Out-of-scope and Compliance/security are folded into open-questions where they bite; no separate sections needed for this slice.*
