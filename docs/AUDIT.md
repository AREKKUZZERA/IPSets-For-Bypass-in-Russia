# Repository Audit (Stage 1)

## Current state
- Legacy data is stored at repository root (`ipset-all.txt`, `exclude.txt`, `exclude-domains.txt`).
- Existing helper tooling is ad-hoc (`AS Parser/AS_Parser.py`) and not integrated into a repeatable pipeline.
- No unified validation/build entrypoints for CI.
- No explicit internal data model for normalization and deduplication.

## Risks found
- Manual edits in large text files can introduce invalid CIDR/domain entries.
- No deterministic normalization step before publishing generated outputs.
- Generated and source artifacts are mixed in top-level layout.

## Stage 1 decisions
- Keep legacy files as source of truth (no bulk migration yet).
- Introduce minimal Python pipeline for read -> normalize -> validate -> generate small outputs.
- Create clear folders for scripts/tests/schemas/sources/dist/build to prepare future stages.
