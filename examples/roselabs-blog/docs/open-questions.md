# roselabs-blog — Open Questions

> Biting assumptions and undecided lines, each with an owner + stakes. `[open]` = unresolved;
> flip to `[decided]` (with the call) as they close. Template: `doc-patterns/living-docs/assumptions.md`.

## Pinned before Plan (the hard gates — resolved)

- `[decided]` **Post visibility + ownership** — public reads return only `published`; a draft is **404** (indistinguishable from "doesn't exist") to anyone but its owner/admin; an author cannot edit/delete another author's post (**404**, not 403). No draft ever serializes to a public request. *(The core promise.)*
- `[decided]` **Comment visibility** — a comment is `pending` on submit and renders publicly **only** when `approved`; `pending`/`hidden` never render. Moderated by the post's author or an admin.
- `[decided]` **Deploy target** — single Hetzner VPS · **Docker Compose** (`api · web · postgres · caddy`) · **Caddy** auto-TLS for `blog.roselabs.io` · config/secrets via `.env` (git-ignored; `.env.example` committed). Graded by the infra grader.

## `[open]` — resolve at Plan/Implement or sign off tracked

- `[decided]` **Content-safety split (author vs comment)** — *stakes: high (XSS).* **Comments = plain text** (stored/rendered as text; React escapes — no HTML interpreted). **Author articles = sandboxed iframe** (`<iframe sandbox srcdoc=…>` without `allow-scripts`) — isolates the article's inline CSS/SVG from the app and runs no script. CSS-in-JS styles the app shell only, not injected content. See [`decisions/0001-content-safety-two-classes.md`](decisions/0001-content-safety-two-classes.md). *Iframe auto-height is an Implement detail.*
- `[decided]` **Email provider** — **Resend** (roselabs account). Dev/local **logs the email**; production wires Resend via a `RESEND_API_KEY` secret in `.env` **at deploy (M7)** — the key is never committed and lives only in the private repo. Not a build blocker. *Owner: Patrick.*
- `[decided]` **JWT policy** — HS256 access token, 1 h TTL (`ACCESS_TOKEN_TTL_SECONDS`), no refresh token (re-login). As built in T2 (`core/security.py`); flipped 2026-09-12. The `JWT_SECRET` default is a separate finding — see `assumptions.md` and backlog T18.
- `[open]` **Comment abuse / rate-limiting** — *stakes: low-medium.* Not built. Moderation catches spam before it renders, but the pending queue can still be flooded. Backlog T24 (per-IP rate limit + honeypot). *Owner: Patrick.*
- `[decided]` **Slug + tag rules** — as proposed: slug from title (`core/slug.py`), uniqueness-suffixed; tags freeform, slugified, reused by slug (T8). Flipped 2026-09-12.
- `[open]` **Preview mechanism** — *stakes: low.* Not built: the editor has no preview route. Proposed shape unchanged (authenticated route renders the public template against an own draft; non-owner → 404). Backlog T23. *Owner: Patrick.*

## Deliberately out of scope (declined — see ui-sketches "Declined")

Public sign-up · WYSIWYG editor · threaded comments · full-text search · scheduled publish · email digests. Logged so Plan doesn't silently re-add them.
