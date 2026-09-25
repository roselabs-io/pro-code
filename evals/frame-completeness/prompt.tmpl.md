---
name: frame-completeness
description: "RECORDED FAILURE — does not test its rubric. Deleting the only-profile-hard-gates-block section left both verdicts unchanged; the hard_gates hook in the fixture carries the behaviour. Kept as evidence and as a re-check after a model upgrade. Tagged inert; exclude from any gate."
tags: [grader, frame, inert]
max_turns: 6
allowed_tools: [Read]
append_system_prompt: |
{{RUBRIC}}
---

You are the **frame-completeness** grader, the ask→Frame gate of a build pipeline. You are a
fresh pass: you did not write the specs below. Your rubric is in your system prompt. Where your
own instincts and the rubric disagree, the rubric wins.

## Context

Two projects are at the Frame gate today. Both use the `generic-saas` profile, which supplies:

- `bar`: actors with goals; primary flows sequenced; a data model; every named integration with
  its contract; error and recovery behaviour for the primary flows.
- `hard_gates`: a multi-tenant product must pin its isolation rules (what scopes to a tenant and
  what a cross-tenant request returns) before Plan.
- `verifiable_means`: an automated test can assert it.
- `usual_silent_gaps`: invitation expiry, rate limits, data retention, the response to a
  cross-tenant request.

### Project A — Acme workspace (multi-tenant B2B)

State of `functional-analysis.md`:

- Actors: member, workspace admin, billing owner. Goals and surfaces for each.
- Primary flow: sign in → create workspace → invite member → assign role → subscribe. Sequenced.
- Data model: Account, Workspace, Member, Role, Invitation, Subscription.
- Isolation: every read and write scopes by `workspace_id`; a cross-workspace request returns
  404; asserted by an integration test per resource.
- Billing: "Stripe handles subscriptions." No events listed, no webhook behaviour, nothing on
  what the product does when a payment fails or a subscription lapses. The "payment failed"
  branch of the primary flow has no described behaviour.
- Invitation expiry: "links expire." No TTL, no re-send behaviour.
- Data retention: not mentioned.

### Project B — Beacon (multi-tenant status pages)

State of `functional-analysis.md`:

- Actors: operator, org admin, public viewer. Goals and surfaces for each.
- Primary flow: sign in → create org → create status page → post incident → resolve. Sequenced.
- Data model: Account, Org, StatusPage, Incident, Update, Subscriber.
- Billing: Stripe. Events consumed: `invoice.paid`, `invoice.payment_failed`,
  `customer.subscription.deleted`. Webhook handler behaviour and the lapse flow (read-only page
  after 14 days) are specified.
- Isolation: not specified. Which reads and writes scope to an org, and what a request across
  orgs returns, is not written anywhere.
- Invitation expiry: 7-day TTL, one re-send.
- Data retention: incidents kept 24 months, then archived.

### The driver's note

> I want to sign off both of these today and hand them to Plan. Tell me what I am signing and
> what to log.

## How to answer

Produce what your rubric asks for, for each project. Then end your reply with exactly these two
lines and nothing after them:

```
PROJECT-A SIGN-OFF-B: <offered|withheld|unknown>
PROJECT-B SIGN-OFF-B: <offered|withheld|unknown>
```

- `offered` — the driver may sign off under the bar today, with the gaps logged.
- `withheld` — the driver may not sign off under the bar today; something must be closed first.
- `unknown` — you could not decide.
