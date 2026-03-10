# Contributing

## Local setup
- Python 3.11+
- `pip install pytest`

## Main commands
- `make test` — run unit tests.
- `make validate` — run validation on hybrid inputs.
- `make build` — build deterministic artifacts with checksums.
- `make deterministic-check` — run two builds and compare `dist` outputs.

## PR expectations
1. Keep diffs focused and small.
2. Do not commit heavy binaries or external datasets.
3. If build outputs changed intentionally, include regenerated `dist/manifest.json` and `dist/checksums/*`.
4. For scheduled data refreshes, prefer PR-based flow (never push directly to `main`).
