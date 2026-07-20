# Profile — `saas-web` · Frame

Domain: a **full-stack web SaaS** — **Python + FastAPI (async)** backend, **React + TypeScript + MUI**
frontend, **async Postgres**, shipped as **Docker Compose on a single VPS**. The batteries-included web
profile: `generic-saas` is the API-only baseline; this one adds a rendered frontend **and** a graded
deploy dimension. First example: the roselabs blog.

## Sources (where Frame's context comes from)

| Source | Provides |
|---|---|
| Product brief / PRD | goal, primary actors, headline features |
| Issue tracker / backlog seed | in-flight scope, known constraints |
| API contract / OpenAPI notes | the endpoints, payload shapes, auth-failure responses |
| UI / design brief | the views, the brand/design system, the states each view owes (loading · empty · error) |
| Founder / PM interview *(brainstorm mode)* | everything, when no brief exists |

## Functional-analysis sections

- **Required:** Identity · Actors · Top-level workflows · Data model · Integrations · Functionalities · **Views (UI inventory)** · Metrics.
- **Optional (add only if they bite):** Out-of-scope, Compliance / security.

List the *product* this app adds — the resources, who may see/change them, and the views that render them. Auth is a means, not the product; name it, then move to what it protects.

## Hard gates

- **UI sketch** — the app is user-facing, so no handoff to Plan without a reviewed `docs/ui-sketches.md` (view inventory + a wireframe per view + a declined list; template: `doc-patterns/specs/ui-sketch.md`). Missing/unreviewed = 🔴 blocking.
- **Visibility / ownership rules** — for any resource with a **public vs private/draft** state or **per-user ownership**, the scoping rule **and** the withheld response (what an anonymous or non-owner request sees — a draft is *absent* from public reads; non-owner write → 404 not 403) must be pinned before Plan. Unspecified = 🔴 blocking: it's the core promise (the blog's is *"no draft leaks to public"*), and Plan can't decompose it without the rule — exactly as isolation is for `generic-saas`.
- **Deploy target** — the target topology (single VPS · Docker Compose · the services · TLS · the secrets/config the app needs) is named before Plan, because it is **graded** (the infra grader). A profile that declares `deploys: true` with a `{TBD}` topology = 🔴 blocking.

## `has_ui` *(must)*

- **`has_ui`:** true — the React frontend. The browser grader + UI-sketch gate are **live** for this profile.

## `deploys` *(must — new hook, see the infra grader)*

- **`deploys`:** true — the app ships as a Docker Compose stack; the **infra grader** (`graders/infra-grader.md`) gates that it builds and boots. A profile that doesn't deploy (e.g. `generic-saas`) sets this false and the infra grader is declared n/a.

## Principles + CfRs (feedforward guides)

- **Principles** (`doc-patterns/guides/principles.md`): *deny by default* — an unscoped or unauthenticated read returns nothing, never a leak; *enforce at the boundary, not the client* — the browser is convenience only; *the rendered surface must not show what the API withholds* — no draft in the DOM the API refused to serve.
- **CfRs that bite** (`doc-patterns/guides/cfrs.md`): **Security** (auth + visibility isolation — hard, proven by integration *and* e2e test), **Accessibility** (state is not colour-only; `axe` passes; keyboard-reachable), **Observability** (every denied/withheld access logs a structured event), **Maintainability** (lint + comment doctrine + the **styling discipline** — theme-only, no ad-hoc styling), **Deliverability** (the stack builds and boots via Compose — the infra grader). A biting CfR with no verifiable bar is a 🔴 for the plan grader.

## Grader bar (consumed by `frame-completeness`)

- **`verifiable_means`:** an automated test can assert it — **integration** (a real request through the app against a **real Postgres**) for API effects, **e2e** (Playwright drives the running app) for rendered behaviour, or a schema validates the shape.
- **`usual_silent_gaps`** — probe these; full-stack briefs routinely omit them:
  - non-happy-path responses: empty result, error, permission-denied, **what an anonymous request sees**
  - the actor model beyond the primary user (author vs anonymous reader vs admin)
  - the **draft/published + ownership** rules — who may read, who may edit
  - the per-view **UI states**: loading, empty, error, unauthenticated
  - integration contracts (webhook payload shape; what an auth failure returns)
  - the **deploy topology + config/secrets** the app needs to boot
- **clean-handoff bar:** functional-analysis carries actors · workflows · data model · integrations · functionalities · **views** · metrics (stubs ok); open-questions logs every biting assumption with owner + stakes; UI sketch reviewed; **visibility/ownership rules pinned** (scoping + withheld-response); deploy target named.
