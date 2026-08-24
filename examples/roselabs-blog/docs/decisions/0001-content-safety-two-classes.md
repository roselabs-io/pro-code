# 0001 — Content safety: two content classes, two mechanisms

> Template: `doc-patterns/living-docs/decision-record.md`. Status: **accepted** (Frame).

## Context

Two kinds of user-supplied content render on public pages, with opposite trust levels:

- **Author article bodies** — rich HTML *by design* (the field-notes pieces are self-contained HTML with inline `<style>` and SVG). Authors are invited/trusted. This content must render with its own styling intact.
- **Comment bodies** — submitted by anonymous public readers. Untrusted.

**CSS-in-JS (emotion/MUI) does not help here.** It styles the app's *own* components; it has no effect on content a user injects. Injected content is a separate concern.

## Decision

- **Comments = plain text.** Stored and rendered as text (React escapes by default); no HTML is ever interpreted. The XSS surface is closed *by construction* — no sanitizer to get wrong. A sanitized markdown subset (`nh3` server-side, `DOMPurify` client-side) is a possible later enhancement, out of scope for v1.
- **Author articles = sandboxed iframe.** `content_html` is rendered via `<iframe sandbox srcdoc={html}>` **without `allow-scripts`**. This fully isolates the article's inline CSS/SVG from the app (no style bleed in either direction) and executes no script. Trusted authorship + isolation is defense-in-depth, and it solves the style-collision problem in the same move. (The same technique that safely hosts the artifacts today.)

## Consequences

- The public **post-detail** view embeds the article body in an isolated frame; the app's MUI/CSS-in-JS styling and the article's own CSS never collide.
- The **styling discipline** (`no-raw-color`, theme-only) applies to the **app shell** (`web/src`), **not** to stored article HTML — author content is exempt by design.
- **Iframe height** handling (auto-sizing a no-script sandboxed frame) is an Implement detail — resolved in M4, not here.
- **False-green traps to test** (Implement): a comment containing `<script>` or `<img onerror=…>` must render **inert** (e2e); the article iframe must carry `sandbox` without `allow-scripts` (a lint/e2e check); the draft-visibility core promise is unaffected.
