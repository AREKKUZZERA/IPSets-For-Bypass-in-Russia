# Architecture (Stage 2)

## Scope
Stage 2 introduces stricter internal modeling and partial migration to structured sources while preserving legacy compatibility.

## Data flow
1. Load input records from selected mode:
   - legacy files,
   - new `sources/*.json`,
   - or both (hybrid).
2. Validate and normalize records.
3. Classify records by action (include/exclude/neutral/direct).
4. Apply strict checks:
   - overlap detection,
   - include/exclude conflicts,
   - special-range filtering,
   - IPv6 handling.
5. Keep uncertain records in `needs_review` instead of silent drops.
6. Emit generated lists + enriched manifest.

## Modules
- `scripts/models.py` — internal typed DTOs, source record model.
- `scripts/source_loader.py` — adapters for legacy + `sources/*.json`.
- `scripts/normalization.py` — normalization, conflict/overlap checks, sorting.
- `scripts/validate.py` — CLI validation with `--strict` and `--input-mode`.
- `scripts/build.py` — artifact generation and manifest enrichment.

## Build artifacts
- `dist/ipset/ipset-all.txt`
- `dist/ipset/exclude.txt`
- `dist/ipset/exclude-domains.txt`
- `dist/manifest.json`

All generated text artifacts are marked as non-editable manually.
