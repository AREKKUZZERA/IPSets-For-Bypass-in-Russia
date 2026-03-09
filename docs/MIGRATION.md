# Migration Plan (Stage 2)

## What is migrated now
A compact subset is migrated to machine-readable format in:
- `sources/stage2_seed.json`

The file contains representative entries (CIDR, IPv6 CIDR, domain exclude) and demonstrates the full Stage 2 schema.

## Compatibility rules
- Legacy root files remain supported and are still read.
- New records should be added into `sources/*.json` (preferred source-of-truth).
- Existing legacy lines can be migrated gradually over future stages.

## Input modes
- `legacy` — read only root text files.
- `hybrid` — merge `sources/*.json` and legacy files (default).
- `sources` — read only machine-readable sources.

## Ambiguity policy
If a record is uncertain or suspicious, it should be marked via `needs_review` and surfaced in manifest, not silently dropped.
