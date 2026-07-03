# Grader — browser-grader

> **Browser** (feedback, ⚙️): an automated browser (Playwright) that
> observes the **running app's real behaviour** — not the code, not a unit mock, the actual
> rendered surface. The one grader that catches "the API is right but the screen is wrong."

Applies only to **UI-bearing** profiles (a profile declares `has_ui: true`). API-only slices skip it — there's no surface to observe.

## What it grades

The verify gate's arbiter for a UI: does the *running* app do the right thing when driven like a user?

- **Renders the true state** — the value on screen matches `/state`; a stale/critical row shows stale/critical, not last-good/ok.
- **Behaves over time** — polling updates the view; an error state degrades correctly (the "unreachable" banner, the grey live-dot).
- **The load-bearing visual invariant** — the profile names it: e.g. *"a stale signal renders '— stale', never a number"*; *"a permission-denied view shows nothing of the denied resource."*

## The contract

```
browser grader = Playwright script → { pass, findings }
  - launch the app, drive it as a user, assert on the RENDERED DOM (not the response)
  - deterministic: seed the app state via a fixture/endpoint, then observe
  - runs in the verify beat, after the API-level tests are green
```

## Why it's not redundant with the API tests

An endpoint-shape test proves the *server* serializes `stale:true, value:null`. It says nothing about whether the *client* honours it — a template bug can render the last-good number over a stale flag and every API test still passes. **The browser grader is the only grader that sees what the operator sees.** (Same reason `200 ≠ handler ran`: green-below ≠ correct-on-screen.)

## Profile hooks

- **`has_ui`** — whether this profile bears a UI at all.
- **`visual_invariant`** — the one rendered fact that must always hold (what the grader asserts hardest).
