# roselabs-blog — Backlog

> One row per ticket, each **well-formed**: a verifiable acceptance criterion, a design hook (or `novel`),
> `depends-on`, and an autonomy tier. **Forward-only** — shipped rows are deleted as Implement lands them
> (git is the record; T1–T17's rows were pruned 2026-09-12, after the fact). Pulled from
> `doc-patterns/living-docs/backlog.md`.
>
> **Autonomy:** 🟢 agent-ship · 🟡 agent-draft (agent scaffolds, human finishes) · 🔴 human-only (risk
> boundary or out-of-repo dep). Every ticket touching **auth or a visibility boundary** is ≥ 🟡 by rule.

## Tickets

| ID | Title | Acceptance criterion (verifiable) | Design hooks | Depends on | Autonomy |
|---|---|---|---|---|---|
| T18 | Remove the `JWT_SECRET` default | `config.py` has no default for `jwt_secret`; the api process exits non-zero at startup when the variable is unset (asserted by a test that constructs `Settings` with the env cleared); `docker-compose.yml` has no `:-` fallback; `.env.example` still documents it | `jwt-auth-dependency` | — | 🟡 auth boundary |
| T19 | Auth-dependency codemod | `codemods/require_auth_dep.py --check api/app/api` exits 0 on the tree and non-zero when a protected router is stripped of `get_current_user` (red-green asserted); wired as `just codemod-check` | `novel — codemod` (profile mandate) | — | 🟢 |
| T20 | a11y check in the e2e beat | `axe-core` runs against list · detail · login · dashboard · editor · moderation in `web/e2e`; zero serious/critical violations; state not colour-only asserted on the draft/published badge | `mui-themed-component` | — | 🟡 may require markup fixes |
| T21 | Visual-regression baselines | Playwright screenshots for the six views committed under `web/e2e/__snapshots__/`; a deliberate theme change fails the check until baselines are updated (asserted once) | `mui-themed-component` | T20 | 🟢 |
| T22 | Wire security · coverage · deps into `just gate` | `just gate-api` runs bandit + detect-secrets + `pytest --cov` (changed-line ≥ 80%) + `uv export \| pip-audit`; `just gate-web` runs `pnpm audit --prod`; one command per `check-commands.md` row | `novel — harness` | — | 🟢 |
| T23 | Author draft preview | authenticated `GET /posts/{id}/preview` renders the public template against an own draft; a non-owner id → 404; an anonymous request → 401; e2e asserts the preview shows the draft and the public detail page still does not | `owner-scoped-query-guard` · `public-vs-authored-visibility` | — | 🟡 ownership |
| T24 | Comment abuse floor | per-IP rate limit on `POST /posts/{slug}/comments` (named config, not a literal) → 429 past the limit; a honeypot field that, when filled, returns 201 and stores nothing (asserted) | `structured-error-envelope` | — | 🟡 untrusted input |
| T25 | Per-surface specs | `docs/surfaces/<view>.md` for the six views, from `doc-patterns/specs/surface-spec.md`, matching what is built; docs-currency green | `novel — docs` | — | 🟢 |
| M7 | Deploy to the VPS | Caddy terminates TLS for `blog.roselabs.io` (own service or host proxy — decision recorded); `RESEND_API_KEY` set from the private env and an invite email actually sends; migrations run once per release, not per replica; secrets never in the tree | `novel — infra` | T18 | 🔴 human-only — DNS, secrets, hosting |

## Build order

Derived from `depends-on` — no cycle.

- **Wave 0** (no deps): T18 · T19 · T20 · T22 · T23 · T24 · T25
- **Wave 1**: T21 (T20) · M7 (T18)
- **Critical path:** T18 → M7.
- **Start now:** T18 (the one that contradicts a profile convention), then T19 / T22 (the profile's
  own mandates the tree skipped).
