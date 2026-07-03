# {{project_name}} — Functional Analysis

> The behavioural spec: **what this system does**, in business terms.
> Not engineering — no patterns, no schema, no code. Those are Plan's job.
> Pulled from `doc-patterns/specs/functional-analysis.md`; filled per the active profile.

## Identity

- **Product:** {TODO: one-line description}
- **Driver / owner:** {TODO}
- **Primary goal:** {TODO: the one outcome this system exists to deliver}

## Actors

Who interacts with the system, and with what privilege.

| Actor | Role / privilege | Goals | Surfaces they touch |
|---|---|---|---|
| {TODO: e.g., End user} | member | {TODO} | {TODO} |
| {TODO: e.g., Admin} | admin | {TODO} | {TODO} |

## Top-level workflows

The handful of end-to-end flows actors run day-to-day. One sequenced narrative each.

- {TODO: "User signs in → creates a project → invites a teammate → assigns a role → …"}

## Data model (business terms)

The core entities the system stores and actors edit — named in domain language, not tables.

- {TODO: e.g., Account, Project, Member, Invitation — one line each on what it is}

## Integrations

External systems this one talks to. One line each: what, direction, protocol/contract (or "TBD → open question").

- {TODO: e.g., Payment provider — outbound, REST, webhook on charge.succeeded}

## Functionalities

Broad strokes of what the system does — one line per major capability. The bridge from goal to backlog: Plan decomposes each into ≥1 ticket.

- {TODO: one line per capability}

> List what **this** product does. External services it depends on go under **Integrations**, not here.

## Metrics + non-functionals

Anything measurable the product is expected to hit.

- {TODO: e.g., p95 API latency < 200ms; 99.9% uptime; tenant isolation (hard requirement)}

---
*Optional sections — add only if they actively bite this project: **Out-of-scope** (when scope is contested), **Compliance / security** (when there's an explicit requirement).*
