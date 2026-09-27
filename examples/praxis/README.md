# praxis

Example #4 in [pro-code](../../README.md) — built with the **`local-app`** profile. A local desktop
application around a model pipeline for a child psychiatrist: `ingest → de-id → classify → [draft →
grade → clinician review] × n → re-id`. Python stage functions, local NER and embedding models, one
remote model API as the only egress, a `pywebview` window.

The hard-done — the profile's core promise — is **nothing of the clinician's leaves her machine
unredacted**, certified by a leak test that reads every outgoing request and every written file
against the synthetic fixtures' answer keys (not by author confidence).

The code lives in its own repository, `roselabs-io/praxis` (private while it is built for one user).
This directory is the pointer; the Frame + Plan artefacts and the living docs are there under
`docs/`. The profile it exercises is [`profiles/local-app/`](../../profiles/local-app/).
