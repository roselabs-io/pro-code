# {{project_name}} — UI Sketches

> The user-facing surfaces, before any code. A **functionality list structurally can't
> carry "what the screens are"** — only a sketch does. Required by any profile whose
> hard gate names it (a UI-bearing app must not hand to Plan without this reviewed).
> Pulled from `doc-patterns/specs/ui-sketch.md`.

## View inventory

Every view/screen/panel the user touches — one row each.

| View | Purpose |
|---|---|
| {TODO: e.g., Dashboard} | {TODO: what the user does here} |

## Wireframe per view

One low-fi sketch per view. ASCII/box art is fine — the point is layout, controls, and what state drives each region, not fidelity.

### {TODO: view name}

```
{TODO: box-art wireframe — regions, controls, where the key state renders}
```

- **Shows:** {TODO: primary content + the state behind it}
- **Controls:** {TODO: buttons/inputs + what each triggers}
- **Non-happy states:** {TODO: empty · loading · error · permission-denied}

## Declined

Views/controls considered and **deliberately left out** — so a reviewer sees the scope edge, and Plan doesn't silently re-add them.

- {TODO: e.g., "Per-device drill-down page — declined for the slice; the dashboard row is enough."}
