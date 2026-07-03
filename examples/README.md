# examples — pipeline output

Two example services the pipeline generates, each runnable and gated green:

- **`multi-tenant-isolation/`** — a multi-tenant SaaS Projects API (`generic-saas` profile). Hard-done: no cross-tenant leak. Gate: **27 tests** green via `poetry run` (ruff · doctrine · special-lint · boundary codemod · pytest).
- **`edge-telemetry-alerting/`** — an industrial telemetry monitor + alerting dashboard (`edge-telemetry` profile). Hard-done: no missed critical alert. Gate: **28 fixture-replay tests + 2 Playwright browser tests** green via `just gate`.

Each service carries its full pipeline output under `docs/` — the spec (frame), the plan, the living docs, and `docs/assumptions.md` (the assumptions ledger: every choice the build made that no input specified, with a disposition). Each was regenerated Frame → Plan → Implement, gated green per its profile's declared runner.
