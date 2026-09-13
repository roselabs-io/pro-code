# roselabs-blog — Assumptions Ledger

> The choices this build made that its inputs never specified — surfaced so a human can see and
> veto them. Pulled from `doc-patterns/living-docs/assumptions.md`. Graded by docs-currency + the
> drift grader's undeclared-choice lens.

Written 2026-09-12, after the build, from the code and the commit history — not maintained ticket by
ticket as the profile requires. Rows marked **no** are the ones nobody dispositioned during the build.

## Ledger

| Choice the build made | Where it came from | Declared? | Disposition |
|---|---|---|---|
| FastAPI async + SQLAlchemy 2 + asyncpg + Alembic; React + TS + Vite + MUI; uv + pnpm + justfile | profile Stack (`saas-web/implement-profile.md`) | yes | — (declared choice-points) |
| Comments plain text; article body in a sandboxed iframe without `allow-scripts` | `decisions/0001` | yes | — (declared) |
| Dev email delivery = log the message; Resend at deploy | `open-questions.md` (decided at Frame) | yes | — (declared) |
| **HS256 access token, 1 h TTL, no refresh token** (`core/config.py`, `core/security.py`) | `open-questions.md` proposed it; never flipped to `[decided]` | partial | **decision** — flipped in `open-questions.md` today; the profile leaves the algorithm a build choice, so this stays a per-build decision |
| **`JWT_SECRET` has a default value** in `config.py` and in `docker-compose.yml` (`dev-insecure-change-me…`) | agent default | **no** | **flag** — contradicts the profile's *auth fails closed* convention (a missing key must deny, never fall back). Not caught by any check or grader in the build. Fix: no default; the process refuses to start without the variable. Backlog row. |
| **Caddy inside the web image; three Compose services, not four** (`infra/Dockerfile.web`, `Caddyfile`) | agent default — Plan's `system-overview.md` drew `api · web · postgres · caddy` | **no** | **decision** — a smaller topology for the local stack; TLS termination for the VPS (M7) will need Caddy as its own service or a host proxy. Record when M7 is planned. |
| **Migrations run on container boot** (`infra/entrypoint.sh`: `alembic upgrade head`) | agent default — `system-overview.md` says "migrations run on release" | **no** | **flag** — fine for one replica; two api replicas would race on boot. Acceptable for a single VPS; note in M7. |
| Bearer token kept in `localStorage` + an axios interceptor (`web/src/api.ts`) | agent default | **no** | **flag** — the profile's Stack names React Query + axios, not where the token lives. `localStorage` exposes the token to any script in the app origin; the iframe sandbox keeps article HTML out of that origin. A cookie-based session is the alternative. Driver decides. |
| Cursor pagination keyed on `published_at` (`api/public.py`) | `cursor-pagination` hook; the key was unspecified | partial | **accept** — two posts published in the same instant could straddle a page; a `(published_at, id)` key closes it. Low stakes for a single-author blog. |
| Invitation token TTL = 7 days (`services/invitations.py`) | agent default | **no** | **accept** — a named constant, not a literal; the profile's *no magic numbers* rule is satisfied. |
| Slug = lowercased, non-alphanumerics to `-`, uniqueness-suffixed; tags reused by slug | `open-questions.md` proposed it | partial | **decision** — flipped to `[decided]` today. |
| Demo admin credentials printed in `README.md`; `seed.py` creates them | agent default | **no** | **accept** — a local demo; the seed is not part of the shipped image's boot path. |
| `sandbox=""` (empty allowlist) rather than a minimal allowlist | `decisions/0001` says "without `allow-scripts`" | yes | — (declared; the strictest reading) |
| Vitest scoped to `web/src` so it does not collect the Playwright specs | agent default | no | **accept** — tooling. |
| **No `codemods/` directory** although the profile mandates a `require_auth_dep` codemod | agent omission | **no** | **flag** — a profile mandate silently skipped; the drift grader should have caught it. Backlog row. |
| **No a11y run, no visual-regression baselines** although the profile declares both | agent omission | **no** | **flag** — same class as the row above. Backlog rows. |

> The three **flag** rows on omissions (codemod, a11y, visual-regression) and the `JWT_SECRET` default are
> the findings of this ledger: each is something the `saas-web` profile requires that the build skipped
> without a declared n/a, and no gate reported it. That is a review-gate gap as much as a build gap — the
> drift rubric checks conventions in the diff, not mandates absent from the tree. Promote: GATE-0 or
> docs-currency should compare the profile's mandated rows against what the example wires.
