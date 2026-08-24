# roselabs-blog — UI Sketches

> The user-facing surfaces, before any code. Required by the `saas-web` hard gate:
> a UI-bearing app must not hand to Plan without this reviewed.
> Pulled from `doc-patterns/specs/ui-sketch.md`.

## View inventory

| View | Purpose | Auth |
|---|---|---|
| **Post list (home)** | browse published posts; filter by tag | public |
| **Post detail** | read a post; read approved comments; submit a comment | public |
| **Tag view** | published posts for one tag | public |
| **Login** | author/admin sign in | public → authed |
| **Accept invite** | set a password from a one-time invite link | public (tokened) |
| **Dashboard (my posts)** | list own posts (draft + published); new/edit/publish | author |
| **Post editor** | create/edit a draft: title · rich-HTML body · tags · save/publish/preview | author (owner) |
| **Comment moderation** | approve/hide pending comments on own posts | author (owner) |
| **Authors (invite)** | invite an author; list authors | admin |

*RSS (`/rss`) is a served feed, not a view.*

## Wireframe per view

### Post list (home)

```
┌───────────────────────────────────────────────┐
│  roselabs · field notes            [Sign in]   │
├───────────────────────────────────────────────┤
│  Tags:  [ all ] [ ai ] [ control ] [ … ]       │
│                                                 │
│  ┌─────────────────────────────────────────┐  │
│  │ Off the Loop                             │  │
│  │ the fourth loop posture · 2026-07 · ai   │  │
│  │ excerpt … … …                            │  │
│  └─────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────┐  │
│  │ You Are Here … (published card)          │  │
│  └─────────────────────────────────────────┘  │
│                              [ Load more ▾ ]    │
└───────────────────────────────────────────────┘
```
- **Shows:** published posts only (cursor-paginated), newest first; tag filter chips.
- **Controls:** tag chip → filter; card → post detail; Load more → next cursor page; Sign in → login.
- **Non-happy states:** **empty** ("no posts yet") · **loading** (skeleton cards) · **error** (retry banner). A draft **never** appears here.

### Post detail

```
┌───────────────────────────────────────────────┐
│  ← all posts                        [Sign in]  │
├───────────────────────────────────────────────┤
│  Off the Loop                                   │
│  by Patrick · 2026-07-20 · [ai] [control]       │
│  ───────────────────────────────────────────   │
│  «rendered rich-HTML article body»              │
│                                                 │
│  Comments (3)                                   │
│   • Ada — "…"                                    │
│   • Lin — "…"                                    │
│  ┌─ Leave a comment ───────────────────────┐   │
│  │ name [____]  email [____]                │   │
│  │ body [__________________________]        │   │
│  │                        [ Submit ]        │   │
│  └──────────────────────────────────────────┘  │
│  (after submit: "Thanks — pending review")      │
└───────────────────────────────────────────────┘
```
- **Shows:** the published post body (rich HTML); **only approved** comments; the comment form.
- **Controls:** Submit → creates a **pending** comment; on success shows the pending notice, not the comment.
- **Non-happy states:** **404** for a draft or unknown slug (identical — a draft must not be distinguishable from "doesn't exist") · **validation** (missing name/body) · **error** on submit. An author-only control (edit) shows here **only** to the owner/admin.

### Login  ·  Accept invite

```
  Login                         Accept invite
  ┌──────────────────┐          ┌──────────────────────┐
  │ email [_______]  │          │ You're invited, ada@… │
  │ pass  [_______]  │          │ display name [______] │
  │      [ Sign in ] │          │ password     [______] │
  │  err: invalid…   │          │ confirm      [______] │
  └──────────────────┘          │        [ Set password ]│
                                 │  err: link expired     │
                                 └──────────────────────┘
```
- **Shows / Controls:** login authenticates → dashboard; accept-invite validates the token, sets the password → authed.
- **Non-happy states:** invalid credentials (401, generic message — no "email exists" oracle) · **expired/used invite token** (clear message, no password set).

### Dashboard (my posts)

```
┌───────────────────────────────────────────────┐
│  My posts                     [ + New post ]   │
├───────────────────────────────────────────────┤
│  ● Off the Loop        published  2026-07-20   │
│                        [edit] [unpublish]       │
│  ○ Draft: Untitled     draft      —            │
│                        [edit] [publish] [del]   │
└───────────────────────────────────────────────┘
```
- **Shows:** **only the signed-in author's** posts (draft + published) — never another author's.
- **Controls:** New/edit → editor; publish/unpublish; delete (own only).
- **Non-happy states:** **empty** ("no posts yet — write one") · another author's post id in the URL → **404**.

### Post editor

```
┌───────────────────────────────────────────────┐
│  Title [______________________]                │
│  Tags  [ai ×][control ×] [ + add ]             │
│  Body  ┌───────────────────────────────────┐   │
│        │ rich-HTML editor / paste area     │   │
│        └───────────────────────────────────┘   │
│  [ Save draft ]  [ Preview ]  [ Publish ]      │
└───────────────────────────────────────────────┘
```
- **Shows:** the editable draft; Preview renders the body as the public page would (authenticated, own draft).
- **Controls:** Save draft (autosave-ish) · Preview · Publish (sets published_at).
- **Non-happy states:** **validation** (title/body required to publish) · **save error** (retry, don't lose input) · editing a post you don't own → **404**.

### Comment moderation

```
┌───────────────────────────────────────────────┐
│  Pending comments (on my posts)                │
├───────────────────────────────────────────────┤
│  On "Off the Loop" — Ada <ada@…>               │
│   "great piece …"          [approve] [hide]    │
│  On "Off the Loop" — spam <x@…>                │
│   "buy now …"              [approve] [hide]    │
└───────────────────────────────────────────────┘
```
- **Shows:** **pending** comments **on the signed-in author's posts** only (admin sees all).
- **Controls:** approve → renders publicly; hide → never renders.
- **Non-happy states:** **empty** ("nothing to moderate") · comment on a post you don't own is **not listed** and its moderation endpoint returns **404**.

### Authors (invite) — *admin only*

```
  [ email ____________ ]  [ Send invite ]
  Authors: Patrick (admin) · Ada (author) · …
```
- **Shows/Controls:** admin invites by email; lists authors. **Non-happy:** a non-admin hitting this view/endpoint → **403/404**; duplicate/active invite → clear message.

## Declined

- **Public sign-up / reader accounts** — declined; accounts are invite-only, comments are name+email only.
- **WYSIWYG rich-text editor** — declined for the slice; authors paste/edit **HTML** directly (the field-notes pieces are already self-contained HTML). A nicer editor is a later ticket.
- **Nested/threaded comments, likes on comments** — declined; flat, moderated comments only.
- **Full-text search, drafts-sharing links, scheduled publish** — declined for now; logged as backlog candidates, not built.
- **Email digests / subscriptions** — declined; RSS is the subscribe surface.
