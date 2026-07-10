# Profile — `{domain}` · Implement

Fill every `{TODO}`. *(must)* slots are gated by GATE-0. See [`../CONTRACT.md`](../CONTRACT.md).

## Stack + layout
{TODO: framework · env/runner · language version · layout · lint/format · tests — the declared
choice-points, fixed here so they're not silent.}

## Deterministic checks *(must — run first, they short-circuit)*
{TODO: a table of check → command → rule (lint · tests · comment-doctrine · special-lint · schema · …),
as many as there are mechanical rules.}

## Fuzzy rubrics *(must — ~3 focused graders)*
- **feature / spec** → {TODO: the acceptance criterion}
- **pattern / drift** → {TODO: the design catalog hooks + the conventions below}
- **docs-currency** → {TODO: the living-docs set below}

## verify_means + false_green_traps *(must)*
- **verify_means:** {TODO: how "done" is proven in this domain}
- **false_green_traps:** {TODO: where "green" lies here — the check-passes-but-broken class}

## Conventions / forbids *(may — the drift grader's rubric)*
{TODO: the domain's conventions + any `doctrine_lint --forbid` rules, or "none"}

## Codemods *(may)*
{TODO: the deterministic auto-fix transforms, or "none"}

## Doctrines *(may)*
{TODO: which `doc-patterns/doctrines/*` this domain mandates, or "shared only"}

## Living docs *(must — the docs-currency grader's set)*
{TODO: the living-doc files kept current every ticket}
