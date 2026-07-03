# {{project_name}} — Log Taxonomy

> **Logs** (feedback, ⚙️): runtime traces the agent *reads* to confirm
> what actually happened — the defense against "200 ≠ the handler ran." Structured, so a
> grader can assert on them, not just eyeball. Pulled from `doc-patterns/harness/log-taxonomy.md`.

## The contract

Every behaviour that matters emits **one structured event** — a stable `code`, a level, and
fields — so the **logs grader** can replay a run and assert the right events fired.

```
{ "code": "<STABLE_CODE>", "level": "info|warning|error|critical", "ts": <t>, ...fields }
```

## Codes (fill per project)

| Code | When it fires | Level | Fields | The behaviour it proves |
|---|---|---|---|---|
| {TODO: e.g., PROJECT_CREATED} | a project is written | info | workspace, id | "the write handler actually ran" |
| {TODO: e.g., CROSS_TENANT_DENIED} | a scoped query rejects a foreign id | warning | workspace, target | "isolation fired, didn't silently pass" |
| {TODO: e.g., ALERT_RAISED} | a rule opens an alert | critical/warning | signal, severity | "the alert fired — from the log, not the return value" |

## How the logs grader grades

- **Assert presence, not just return value** — a passing status with no `HANDLER_RAN` event is a false green.
- **Assert the code, level, and key fields** — `ALERT_RAISED{severity:critical}` proves the *critical* path, not just *an* alert.
- **Deterministic** — the logs grader is a script over captured logs; it runs in the gate before the fuzzy graders.
