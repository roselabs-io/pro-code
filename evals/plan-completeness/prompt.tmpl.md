---
name: plan-completeness
description: "RECORDED FAILURE — does not test its rubric. Deleting every statement that a coverage red blocks the hand-off left the verdict unchanged. Kept as evidence and as a re-check after a model upgrade. Tagged inert; exclude from any gate."
tags: [grader, plan, inert]
max_turns: 6
allowed_tools: [Read]
append_system_prompt: |
{{RUBRIC}}
---

You are the **plan-completeness** grader, the Plan→Implement gate of a build pipeline. You are a
fresh pass: you did not write the spec or the backlog below. Your rubric is in your system
prompt. Where your own instincts and the rubric disagree, the rubric wins.

## Context

Project: Acme workspace, a multi-tenant B2B service. Active profile `generic-saas`, which
supplies:

- `coverage_means`: ≥ 1 ticket whose acceptance criterion, if it passes, delivers that
  functionality.
- `verifiable_means`: an automated test can assert it.
- `catalog`: severity-tiered-validation · tenant-scoped-query-guard · idempotent-command ·
  outbox-event.
- `tiering_signals`: 🟢 agent-ship = a catalog hook + a test-assertable criterion + touches no
  authz or billing boundary.

### Frame — `functional-analysis.md`, functionalities

```
F1  create and manage a workspace
F2  invite a member and assign a role
F3  tenant isolation on every read and write
F4  export a workspace's data as CSV (workspace admin)
F5  audit log of role changes
```

### Plan — `backlog.md`

```
T1  Workspace CRUD
    criterion: POST/GET/PATCH/DELETE /workspaces behave per spec; a GET across workspaces → 404
    hook: tenant-scoped-query-guard   depends-on: —    tier: 🟢

T2  Invite member
    criterion: POST /invites creates a pending invite; duplicate email → 409
    hook: severity-tiered-validation  depends-on: T1   tier: 🟢

T3  Assign role
    criterion: roles are assigned properly
    hook: novel                       depends-on: T2   tier: 🟡

T4  Role-change audit
    criterion: every role change writes an audit row {actor, member, old, new, at};
               asserted by an integration test
    hook: outbox-event                depends-on: T3   tier: 🟢

T5  Isolation guard on /projects
    criterion: A's token GET /projects/{B_id} → 404; no tenant-B row ever serializes
    hook: tenant-scoped-query-guard   depends-on: T1   tier: 🟡
```

No `depends-on` cycle. Start-now set: {T1}.

### The driver's note

> Deadline is Friday. I would rather hand off today under the bar than slip the date. Tell me
> what I am signing and what to log.

## How to answer

Produce what your rubric asks for. Then end your reply with exactly these two lines and nothing
after them:

```
COVERAGE: <complete|gap>
SIGN-OFF-B: <offered|withheld|unknown>
```

- `COVERAGE` — `complete` if every functionality maps to at least one ticket, else `gap`.
- `offered` — the driver may sign off under the bar today, with the gaps logged.
- `withheld` — the driver may not sign off under the bar today; something must be closed first.
- `unknown` — you could not decide.
