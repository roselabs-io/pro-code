# 0002 — Bearer tokens are HS256-signed JWTs (PyJWT)

- **Status:** accepted
- **Date:** 2026-07-03
- **Ticket:** T1 (auth boundary)

## Context

The profile declares "a signed bearer token resolved to a `Caller`" and names the **token library +
signing algorithm** as an explicit build choice to surface. Nothing upstream specified either.

## Decision

Use **PyJWT** with **HS256** (symmetric HMAC-SHA256). The signing secret comes from
`APP_TOKEN_SECRET` with a dev default; tokens carry `{ws, sub, role}`.

## Why (and what we rejected)

- **PyJWT** is the de-facto standard JWT library for Python — minimal, well-audited. `itsdangerous`
  or a hand-rolled HMAC would also work; JWT's standard claim structure won the tie.
- **HS256 (symmetric)** is the simplest correct choice when the same deployment both issues (tests)
  and verifies tokens. **Rejected for now — RS256 (asymmetric):** needed if a *separate* auth
  service issues tokens (verifier holds only the public key). Flagged in `assumptions.md`, because
  the real issuer is out of repo — if it's a distinct service, this must become RS256.

## Consequences

- Verifying a token needs the shared secret; a separate issuer would need the secret distributed —
  the smell that says "switch to RS256."
- The dev-default secret must never ship to production (env override required).
