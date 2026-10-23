# Site recipes of the command contract. `check` and `gate` are what the local preflight runs.
# `up`, `down`, `logs` and `test` are listed under `checks.recipes.not_applicable` in pipeline.yaml.
# No recipe calls a model: the evals under `evals/` are run by hand (evals/README.md).

scanner := "detect-secrets==1.5.0"

# Deterministic checks over the tracked files: the comment doctrine and test posture of
# `checks/doctrine_lint.py` over the Python (without the linter itself, whose comment names the
# T201 exemption), byte-compilation of the Python, relative Markdown links (without the generated
# `evals/*/prompt.md`, whose rubric copies keep the links of their source files), and the secret
# scan against `.secrets.baseline`. The scan runs with `uv run --offline`: it installs nothing and
# fails with the `just prepare` command when the scanner is not in uv's cache.
check:
    python3 checks/doctrine_lint.py $(git ls-files '*.py' ':!checks/doctrine_lint.py')
    python3 -c 'import sys; [compile(open(p, "rb").read(), p, "exec") for p in sys.argv[1:]]' $(git ls-files '*.py')
    python3 tools/check_links.py --exclude 'evals/*/prompt.md'
    @uv run --offline --no-project --with {{scanner}} python -c '' 2>/dev/null || { echo "check: {{scanner}} is not in uv's cache; run \`just prepare\`" >&2; exit 1; }
    uv run --offline --no-project --with {{scanner}} python tools/secret_scan.py

# Download the pinned secret scanner into uv's cache; needs the network. Not part of the gate.
prepare:
    uv run --no-project --with {{scanner}} python -c ''

# The deterministic gate CI runs.
gate: check

# Regenerate the generated `evals/*/prompt.md` from their templates and rubrics.
fix:
    python3 evals/build.py

# Switch to main and fast-forward it from origin; refuses local changes or a diverged main.
ff:
    #!/usr/bin/env sh
    set -eu
    if [ -n "$(git status --porcelain)" ]; then echo "ff: the working tree has changes" >&2; exit 1; fi
    git switch main
    git fetch origin main
    git merge --ff-only origin/main
