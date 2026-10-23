# AGENTS.md

Instructions for agent sessions working in this repository. `pipeline.yaml` names this file for
`docs.agents`, `docs.contract`, `docs.review_posture` and `docs.operating_model`.

## Repository

Markdown skills, graders, checks and profiles of a build pipeline for coding agents, the Python
scripts that support them, example services built through it, and two HTML articles. `README.md`
describes the pipeline and has the full layout.

| Path | Content |
|---|---|
| `skills/`, `graders/`, `checks/`, `codemods/`, `doc-patterns/` | the agnostic pipeline: phase skills, the review rubric and the on-demand graders, deterministic checks (`checks/doctrine_lint.py`), doc skeletons |
| `profiles/` | the domain overlays; `profiles/CONTRACT.md` is the hook list |
| `evals/` | mutation tests for the graders (`evals/README.md`); `build.py` writes each `evals/*/prompt.md`, `screen.py` calls `claude -p` |
| `examples/` | services built through the pipeline, each with its own README, recipes and tests |
| `bin/context.py` | emits the documents one pipeline role consumes |
| `*.html`, `two-reading-journeys.md`, `.nojekyll` | the articles published by GitHub Pages |
| `pipeline.yaml` | the Governor dispatcher's config for this repository |
| `.github/workflows/procode-ci.yml` | `validate` (PR metadata) and `gate` (`just gate`) |
| `.github/workflows/procode-pm.yml` | the issue and board sync of Governor |
| Governor's package preflight (`tools/local_preflight.py` of the Governor package, run by the dispatcher; this repository keeps no copy) | the local check the dispatcher runs: `just check`, then `just gate` |
| `tools/check_links.py`, `tools/secret_scan.py`, `.secrets.baseline` | the link check and the secret scan of `just check` |

GitHub Pages builds `main` from the root with its own `pages build and deployment` workflow, so a
merge to `main` publishes every tracked file at `https://roselabs-io.github.io/pro-code/`. The
repository is public.

## Pipeline

A ticket goes through [review-gate](skills/review-gate/SKILL.md): the auto-fix arm, the active profile's
checks in order, one review by a fresh session that did not write the diff
([`graders/review.md`](graders/review.md)), at most one fix pass with the checks rerun, then the
human. No review runs a second time. The frame-, plan- and profile-completeness graders run only when a
person asks for them.

`README.md` describes the steps, what runs automatically and what runs on demand, and, under *Changes
from the multi-grader model*, what was removed: the graders between phases, the parallel graders, the
re-grade loop and the N-vote. The model is the one Governor's
[harness posture](https://github.com/roselabs-io/governor/blob/main/governor/docs/postures/harness-posture.md)
records (a private repository).

## Commands

| Recipe | Runs |
|---|---|
| `just check` | `checks/doctrine_lint.py` over the tracked Python except the linter itself; byte-compilation of the tracked Python; `tools/check_links.py` over the tracked Markdown except `evals/*/prompt.md`; `tools/secret_scan.py` with detect-secrets 1.5.0 against `.secrets.baseline` |
| `just gate` | `just check`; the deterministic gate CI runs |
| `just fix` | `python3 evals/build.py`: regenerates `evals/*/prompt.md` from their templates and rubrics |
| `just ff` | switches to `main` and fast-forwards it from `origin`; refuses local changes or a diverged `main` |

`up`, `down`, `logs` and `test` are not applicable (`checks.recipes.not_applicable` of
`pipeline.yaml`): the site has no local server and the root has no test suite. The examples' tests
are run from each example's directory (its README) and are not part of the gate. `just`, `python3` and `uv` are
required; the first secret scan downloads detect-secrets.

No recipe calls a model. The evals call live models and are run by hand (`evals/README.md`).

The gate does not check fragments against headings, does not read links in the HTML articles, does
not lint the examples with their profiles' `--forbid` rules, and does not scan Git history.

## Changing content

- Skills, graders, checks and profiles are shared byte-for-byte by every domain (`README.md`). A
  change to one is a change to the pipeline, not to one example.
- `evals/*/prompt.md` is generated: after a change to a rubric under `graders/`, to
  `profiles/CONTRACT.md` or to a case template, run `just fix` and commit the result. A case's
  assertions and recorded results are evidence; they are changed only by an issue that asks for it.
- A finding of the secret scan that is not a secret is accepted by refreshing `.secrets.baseline`
  (`tools/secret_scan.py` has the command) and reviewing the changed entries.
- Documents are descriptive: they state what a thing is, what it does and what it does not do.

## Pull requests

A PR from a branch `agent/<N>-…` carries exactly one `Procode-Issue: #N` line; a dispatched run also
requires a `Procode-Agent` line naming a configured lane. `validate` of `procode-ci.yml` checks both.
`procode-pm.yml` moves issue N on the board from that line. `autonomy: tiered`: the merge of a
complex or exceptional ticket's PR is left to a person, and every merge publishes the site.

## Finding triage

`docs.operating_model` in `pipeline.yaml` names this file. Each independent-review finding is
triaged before a correction is requested. The dispatcher runs this as a read-only triage session
(Governor `governor/docs/service/finishing.md`, Review triage); an operator correcting by hand
applies the same rules:

Only a CRITICAL finding requests changes; a review with WARNING and INFO findings only approves, and
its WARNINGs are triaged before the merge queue (Governor `governor/docs/postures/pr-review-posture.md`).

1. Open the cited file and confirm the finding against it. A finding that does not hold is answered
   on the PR with the evidence, and no correction is requested for it.
2. Request a correction for every confirmed CRITICAL and for every confirmed WARNING that is a
   boundary finding: security (including credentials and what the dispatcher pushes, merges or
   deletes, and what a merge publishes), data loss, or the issue's contract or scope.
3. Each other confirmed WARNING is either corrected or dispositioned: a PR comment names the
   follow-up issue and why deferral is safe, and the follow-up issue is opened.

Every later review of the PR receives the dispositions and does not reopen one without new evidence.
