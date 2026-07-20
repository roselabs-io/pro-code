# roselabs-blog — Functional Analysis

> The behavioural spec: **what this system does**, in business terms.
> Not engineering — no patterns, no schema, no code. Those are Plan's job.
> Pulled from `doc-patterns/specs/functional-analysis.md`; filled per the `saas-web` profile.

## Identity

- **Product:** the **roselabs blog** — a small team of **invited authors** publish articles; the public reads published posts and leaves **moderated** comments. Hosts rich-HTML articles (the field-notes pieces).
- **Driver / owner:** roselabs (Patrick).
- **Primary goal:** publish articles to the public over one app with **two invariants that never break**: *no draft or unpublished post is readable by a public request*, and *no unapproved comment is shown publicly*. The core promise.

## Actors

| Actor | Role / privilege | Goals | Surfaces they touch |
|---|---|---|---|
| Anonymous reader | none — read published posts; submit a comment (held for moderation) | read articles, comment | public site · RSS |
| Author | `author` — write/edit/publish **own** posts; moderate comments **on own** posts | write and ship articles | public site · admin editor |
| Admin | `admin` — author rights **plus** invite authors, publish/unpublish **any** post, moderate **any** comment | run the blog | public site · admin (all) |
| (Attacker) | anonymous, or author-A probing for author-B's drafts / edit endpoints, or a commenter injecting markup | read a draft, edit another's post, land XSS via a comment | all surfaces (must fail closed) |

> Identity is carried by a **JWT bearer** resolving to an `Author{id, role}`. Accounts are **invite-only** — there is no public sign-up (an admin invites by email; the invitee sets a password). Passwords are **argon2**-hashed.

## Top-level workflows

- **Author publishes:** author signs in → drafts a post (title + rich-HTML body + tags) → previews the draft (own, authenticated) → publishes → the post appears on the public list, its detail page, and the RSS feed.
- **Reader reads + comments:** reader browses published posts → opens a post → submits a comment → the comment is stored **pending**, shown to no one → an author/admin approves it → it renders under the post.
- **Author moderates:** author opens the moderation queue → sees pending comments **on their own posts** → approves or hides each.
- **Admin invites an author:** admin sends an invite to an email → the invitee opens the tokenized link → sets a password → becomes an author.

## Data model (business terms)

- **Author** — an invited account: `id`, `email`, `display_name`, `role` (author | admin), `password_hash`, `created_at`. Owns the posts it writes.
- **Invitation** — `id`, `email`, `token`, `invited_by`, `expires_at`, `accepted_at`. One-time; expires.
- **Post** — the article: `id`, `author_id` (owner), `title`, `slug`, `content_html` (rich HTML), `excerpt`, `status` (draft | published), `published_at`, `created_at`, `updated_at`. Belongs to exactly one author.
- **Tag** — `id`, `name`, `slug`. Post ↔ Tag is many-to-many; tags are created on first use.
- **Comment** — public-submitted: `id`, `post_id`, `author_name`, `author_email`, `body`, `status` (pending | approved | hidden), `created_at`. Never rendered publicly unless `approved`.

## Integrations

- **Email** — outbound; sends author **invitations** (and optionally a new-comment notification). Contract: a transactional email send (SMTP or API). **Provider is TBD** — dev/local **logs the email** instead of sending. *(See open-questions.)*
- **RSS/Atom feed** — a served public surface (not an external system): published posts as a valid feed at `/rss`.
- *(No payment, no analytics vendor, no third-party comments in this build.)*

## Functionalities

Plan decomposes each into ≥ 1 ticket.

- **Authenticate a request** — resolve a JWT bearer to an `Author`; **fail closed** when the key/token is missing or invalid (no dev-open fallback).
- **Invite + onboard an author** *(admin-only)* — admin invites by email; the invitee accepts via a one-time token and sets a password.
- **Author a post** — create/edit a **draft** (title + rich-HTML body + tags), scoped to the owner.
- **Publish / unpublish a post** — flip draft ↔ published; **owner or admin only**; `published_at` set on first publish.
- **Enforce post visibility + ownership** — public reads return **only published**; a draft is **absent (404)** to anyone but its owner/admin; an author **cannot edit or delete another author's post** (404, not 403). No draft row ever serializes to a public request. *(Core promise — its own functionality, not a clause.)*
- **List + read published posts (public)** — the published list, **cursor-paginated**; filter by tag; a single post by slug.
- **Submit a comment (public)** — anyone may submit against a published post; stored **pending**; **never shown** until approved. The body is **sanitized** (stored untrusted markup is neutralized — the XSS trap).
- **Moderate comments** — the post's **author or an admin** approves/hides; **only approved** comments render publicly. *(The second visibility boundary.)*
- **Serve the RSS feed** — published posts as a valid RSS/Atom feed; drafts never appear.
- **Audit denials** — a denied draft access, a cross-author edit, or an auth failure emits a structured event (`DRAFT_ACCESS_DENIED{post,requester}`, `AUTH_DENIED{reason}`), so both invariants are provable from the trace.

## Metrics + non-functionals

- **Post visibility + ownership** — **hard**; asserted by an integration test on the real query path + a Playwright e2e that the draft is **absent** for an anonymous session + an adversarial **N-vote** on the core promise.
- **Comment moderation** — **hard**; no `pending`/`hidden` comment renders publicly (integration + e2e on the negative).
- **Content safety** — author bodies are **rich HTML by design** (the field-notes artifacts carry inline CSS/SVG — authors are trusted); **comment bodies are untrusted and sanitized**. The XSS false-green: a comment that stores `<script>` must never execute on render.
- **Accessibility** — public + admin views pass `axe` (no serious/critical); state is not colour-only; keyboard-reachable.
- **Deliverability** — the stack **builds and boots via Docker Compose**; migrations apply **from an empty database** (the infra grader).
- **Observability** — every denial emits a structured event.
- **Maintainability** — lint + comment-doctrine + the styling discipline clean; changed-line coverage ≥ 80%.

---
*Optional sections — Out-of-scope and Compliance/security are folded into open-questions where they bite.*
