# {{project_name}} — README Doctrine

> A Rule (feedforward). Every service the pipeline produces ships a README that tells a
> newcomer how to run it — set up the environment, run the gate, and launch the app —
> in this profile's tools. Pulled from `doc-patterns/doctrines/readme-doctrine.md`.

## The README must carry a "Run it" section

A reader who just cloned the repo can bring the service up and check it in three moves:

1. **Set up the environment** — the profile's env tool builds the venv (e.g. `poetry install`, `uv sync`).
2. **Run the gate** — the graders, in one place (e.g. `just gate`, or the explicit `poetry run` sequence when the profile has no task-runner).
3. **Launch** — start the app / serve the surface (e.g. `uvicorn …`), or run the demo.

State the exact commands for *this* project's tools, not a generic placeholder. If the profile ships no task-runner, list the grader commands explicitly so the gate is still one copy-pasteable block.

## Why it's a doctrine

The launch instructions are the one thing every reader needs, and the first to rot when commands change. Keeping them present and correct is the rule; the docs-currency grader treats a README whose "Run it" is missing or whose commands no longer work as stale.
