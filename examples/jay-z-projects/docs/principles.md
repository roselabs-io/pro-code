# jay-z-projects — Principles

> Feedforward values that bias every decision, before any rule or ticket.
> Pulled from `doc-patterns/guides/principles.md`; domain values from the `generic-saas` profile.

## Universal (hold in every domain)

- **Grade the context, not just the code.** Every handoff passes a grader before the next phase eats it.
- **Author ≠ grader.** Nothing grades its own work; a fresh critic has fresh priors.
- **No done without fresh evidence.** "Should pass" is not "passed this session."
- **Fail loudly.** A silent wrong answer is worse than a loud stop.
- **Every correction given twice is a missing grader.** Encode the rubric; don't re-nag.

## Domain values (from `generic-saas`)

- **Deny by default.** An unscoped or foreign query returns *nothing*, never a leak. Absence of a match is "not found," not "here's the row."
- **Enforce at the boundary, not the caller.** Authz/isolation live server-side, in the store and the request boundary — never trusted from the client.
- **Hide existence across tenants.** A cross-tenant id is indistinguishable from a nonexistent one (404), on every verb — so no error code becomes an oracle.
