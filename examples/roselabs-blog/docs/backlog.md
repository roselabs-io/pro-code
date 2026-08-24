# roselabs-blog — Backlog

> One row per ticket, each **well-formed**: a verifiable acceptance criterion, a design hook (or `novel`),
> `depends-on`, and an autonomy tier. **Forward-only** — shipped rows are deleted as Implement lands them
> (git is the record). Pulled from `doc-patterns/living-docs/backlog.md`.
>
> **Autonomy:** 🟢 agent-ship · 🟡 agent-draft (agent scaffolds, human finishes) · 🔴 human-only (risk
> boundary or out-of-repo dep). Every ticket touching **auth or a visibility boundary** is ≥ 🟡 by rule —
> and the two visibility boundaries are 🔴 until their test exists. A prediction, re-confirmed at pickup.

## Tickets

| ID | Title | Acceptance criterion (verifiable) | Design hooks | Depends on | Autonomy |
|---|---|---|---|---|---|
| T1 | App skeleton + async DB + migration baseline | `GET /health` → 200; `alembic upgrade head` builds the schema on an **empty** DB; a repository round-trips a row against a **testcontainers Postgres** (no `create_all` in the app path) | `layered-endpoint` · `async-repository` · `alembic-migration-per-schema-change` | — | 🟢 scaffolding, no boundary |
| T2 | Author model + JWT login + `get_current_user` | `POST /auth/login` valid creds → 200 + token; invalid → **401 generic** (no email-exists oracle); protected route, no/invalid token → 401; `get_current_user` resolves a valid token to the Author; password **argon2**-hashed, never serialized; `AUTH_DENIED{reason}` logged | `jwt-auth-dependency` · `layered-endpoint` | T1 | 🔴 auth risk boundary — human-owned until the auth tests exist |
| T3 | Author invitations (admin invite → accept) | admin `POST /invites` (email) → 201 pending; non-admin → 403/404; accept with a valid token sets a password → author; expired/used token → clear 4xx, no password set; dev **logs** the email | `jwt-auth-dependency` · `structured-error-envelope` | T2 | 🟡 admin-only, tokened flow |
| T4 | Post model + author CRUD (draft) | author creates/edits a **draft** (title · `content_html` · tags), lists **own** posts, deletes **own**; every query **owner-scoped**; a non-owner post id → **404**; schema shipped as an Alembic migration | `layered-endpoint` · `owner-scoped-query-guard` · `async-repository` · `alembic-migration-per-schema-change` | T2 | 🟡 touches ownership |
| T5 | Publish / unpublish | owner or admin flips `draft ↔ published`; `published_at` set on first publish; a non-owner (non-admin) flip → 404 | `owner-scoped-query-guard` | T4 | 🟡 ownership |
| **T6** | **Enforce post visibility + ownership (CORE PROMISE)** | anon `GET /posts` returns **only published**; anon `GET /posts/{draft_slug}` → **404** (indistinguishable from unknown); author-A editing author-B's post → 404; **no draft row ever serializes** to a public request; `DRAFT_ACCESS_DENIED{post,requester}` logged. Asserted by an **integration test on the real query path** + a **Playwright e2e** (draft **absent** in the DOM for an anon session) + an **adversarial N-vote** | `public-vs-authored-visibility` · `owner-scoped-query-guard` · `write-through-audit-log` | T4, T5 | 🔴 core promise — the risk boundary; human-owned |
| T7 | Public read: list · by tag · by slug | anon `GET /posts` **cursor-paginated**, newest first, published only; `?tag=` filters; `GET /posts/{slug}` → the published post or 404; assertions on page cursor + tag filter **+ a seeded draft never appears in any of these** | `cursor-pagination` · `layered-endpoint` · `public-vs-authored-visibility` | T6 | 🟡 serializes public content — must route through the visibility guard |
| T8 | Tags (freeform, created on use) | a tag is slugified + created on first use; Post↔Tag many-to-many; listing by an unknown tag → empty, not error | `layered-endpoint` | T4 | 🟢 |
| T9 | Submit a comment (public, pending, plain-text) | anon `POST /posts/{slug}/comments` → 201 **pending**, rendered to no one; missing name/body → 422; body stored/rendered as **text** — a `<script>` body is inert (asserted) | `structured-error-envelope` · `layered-endpoint` | T6, T7 | 🟡 untrusted input |
| **T10** | **Moderate comments (2nd visibility boundary)** | only the post's owner or an admin approves/hides; a non-owner moderation call → **404**; **only `approved`** comments serialize on public read; `pending`/`hidden` never appear (integration + **e2e negative**) | `owner-scoped-query-guard` · `public-vs-authored-visibility` | T9 | 🔴 visibility boundary — human-owned |
| T11 | RSS/Atom feed | `GET /rss` → valid feed XML; **only published** posts; a draft never appears (asserted against a schema/parse + a seeded draft) | `layered-endpoint` · `public-vs-authored-visibility` | T6 | 🟡 serializes public content — visibility-gated |
| T12 | Web skeleton + MUI theme + auth context | `pnpm build` succeeds; the **roselabs MUI theme/tokens** applied (no raw hex — special-lint clean); a protected route redirects to login when unauthenticated | `mui-themed-component` · `react-query-data-view` | T2 | 🟢 scaffolding |
| **T13** | **Public UI: list · detail (iframe) · comment form** | e2e: published posts render; a **draft is absent** for an anon session (visual invariant); the article body renders in `<iframe sandbox srcdoc>` **without `allow-scripts`** (decision 0001); comment submit → "pending" notice; loading/empty/error states; `axe` clean | `react-query-data-view` · `mui-themed-component` | T7, T9 | 🔴 renders the visibility boundary — browser check core surface |
| T14 | Auth views: login + accept-invite | e2e: login authenticates → dashboard; invalid → **generic** error; expired invite → clear error; `axe` clean | `react-query-data-view` · `mui-themed-component` | T3, T12 | 🟡 auth-adjacent |
| T15 | Author dashboard + post editor | e2e: author sees **only own** posts; editor saves a draft, **previews own draft**, publishes; editing a non-owned post id → 404 view; `axe` clean | `react-query-data-view` · `mui-themed-component` | T5, T12 | 🟡 ownership on the client (enforced server-side) |
| T16 | Comment moderation view + admin authors/invite | e2e: moderation lists **only pending on own posts**; approve → renders publicly; admin invite sends (logged in dev); non-admin can't reach the authors view | `react-query-data-view` · `mui-themed-component` | T10, T15 | 🔴 moderation visibility + admin |
| T17 | Dockerize + Compose + Caddy + infra grader | `docker compose build` succeeds; `up` reaches healthy on a **fresh volume**; migration applies from empty; `GET /health` 200 through Caddy; web root serves HTML; `.env.example` committed, no secret in the tree | `novel — infra` | T6, T12 | 🟡 agent-draft — human owns secrets/DNS; deploy itself is M7 |

## Build order

Derived from `depends-on` — **fail loud on a cycle** (none: the graph is a DAG).

- **Waves:**
  - **Wave 0** (no deps): T1
  - **Wave 1** (dep T1): T2
  - **Wave 2** (dep T2): T3 · T4 · T12
  - **Wave 3**: T5 (T4) · T8 (T4) · T14 (T3,T12)
  - **Wave 4**: **T6** (T4,T5)
  - **Wave 5**: T7 · T11 (T6) · T15 (T5,T12)
  - **Wave 6**: T9 (T6,T7) · T13 (T7,T9→ also T6) · T17 (T6,T12)
  - **Wave 7**: **T10** (T9)
  - **Wave 8**: T16 (T10,T15)
- **Critical path:** **T1 → T2 → T4 → T5 → T6 → T9 → T10 → T16** (the moderation-visibility chain drives the schedule).
- **M4 vertical slice** (build + gate first): **T1 · T2 · T4 · T6 · T12 · T13** — auth + a post + the draft-visibility core promise + render. The N-vote certifies **T6** on this slice before anything fans out.
- **Start now:** **T1** (the only graph-unblocked, un-gated ticket).
- **Gated (not startable):** none — email (Resend) is deferred to M7 but doesn't block; the JWT-policy default is confirmed at T2.
