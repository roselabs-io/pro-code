# {{surface_name}} — Surface Spec

> One drill-down per surface — the profile names what a "surface" is (a UI page, an API endpoint, a job).
> Sketch-shaped: enough for Implement to start, not a final design. Implement fills the detail.
> Pulled from `doc-patterns/specs/surface-spec.md`; one file per surface in `docs/surfaces/`.

## What it does

- **Purpose:** {TODO: the one thing this surface is for}
- **Actors:** {TODO: who reaches it, with what privilege}
- **Shows / returns:** {TODO: the primary content + the state that drives it}

## Controls / inputs

What an actor (or caller) can do here, and what each triggers.

| Control / input | Triggers | Notes / validation |
|---|---|---|
| {TODO: e.g., "Save" button} | {TODO: calls X} | {TODO: gated until clean} |

## Calls + contracts

The backend calls this surface makes — endpoint/action + what it returns. If a contract isn't clear from Frame, **log an open question — don't invent it.**

- {TODO: e.g., `POST /projects` → `{id}` on 201; `409` if name taken}

## States

The non-happy paths — the ones briefs routinely omit.

- **Empty:** {TODO}
- **Loading:** {TODO}
- **Error:** {TODO}
- **Permission-denied:** {TODO: what an unauthorized / cross-tenant actor sees — 404 vs 403}

## Design shapes referenced

The catalog hooks this surface adapts (from the profile's catalog), or `novel — author fresh`.

- {TODO: e.g., `tenant-scoped-query-guard`, `severity-tiered-validation`}
