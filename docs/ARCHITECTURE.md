# Minimal Architecture (Stage 1)

## Scope
This stage introduces only a foundational pipeline without mass migration.

## Flow
1. Read legacy inputs from repository root.
2. Normalize into internal model (`NormalizedData`).
3. Deduplicate and sort deterministically.
4. Apply excludes.
5. Validate CIDR/domain entries.
6. Generate small text outputs and manifest in `dist/`.

## Modules
- `scripts/models.py` — typed DTOs for inputs/results.
- `scripts/io_utils.py` — list/manifest read-write utilities.
- `scripts/normalization.py` — validation + normalization logic.
- `scripts/validate.py` — validation CLI entrypoint.
- `scripts/build.py` — generation CLI entrypoint.

## Directory baseline
- `scripts/` runtime code.
- `tests/` unit tests for core logic.
- `schemas/` reserved for future schema definitions.
- `sources/` reserved for future source adapters.
- `dist/` generated outputs.
- `build/` temporary build artifacts.
