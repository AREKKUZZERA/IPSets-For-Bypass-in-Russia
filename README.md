# IPSets Dataset and Build Pipeline

This repository maintains a **structured CIDR dataset** with provenance metadata and generates versioned text artifacts in `dist/`.

## Repository layout

- `data/entries.json` — source-of-truth dataset (edit this file for content changes).
- `data/schemas/entries.schema.json` — JSON schema for dataset structure.
- `data/sources.md` — provenance and source requirements.
- `tools/validate.py` — policy and data integrity checks.
- `tools/build.py` — deterministic generator for `dist/*.txt` and checksums.
- `tools/stats.py` — updates the stats block in this README.
- `dist/` — generated outputs only. **Do not edit by hand.**

## Data model and policy

Each dataset entry includes CIDR, category, confidence, source metadata, and verification timestamps.

Validation enforces:

- CIDR correctness for IPv4/IPv6.
- Required source metadata (`kind`, `ref`, `url`).
- No duplicate CIDR+category records.
- No overlaps inside the same category.
- Wide-range policy:
  - IPv4 prefixes broader than `/12` require `wide_ok: true` and explanatory `notes`.
  - IPv6 prefixes broader than `/32` require `wide_ok: true` and explanatory `notes`.

## Local workflow

```bash
python tools/validate.py
python tools/build.py
python tools/stats.py
```

If data changed, commit both `data/*` and regenerated `dist/*` plus README stats updates.

## Generated outputs

- `dist/ipset-all.txt` — unique CIDR list across all categories (backward-compatible semantics).
- `dist/ipset-<category>.txt` — unique CIDR list per category.
- `dist/checksums.txt` — SHA256 checksums for generated text files.

## Migration note

The former root-level `ipset-all.txt` has been migrated to `dist/ipset-all.txt` and is now generated from `data/entries.json`.

## Dataset status

> Current records are placeholder documentation ranges to bootstrap tooling and CI. Maintainers should replace them with verified data and preserve provenance fields.

<!-- STATS:BEGIN -->
### Dataset Stats

- Total entries: **7**
- Counts by category:
  - `cdn`: 2
  - `cloud`: 1
  - `dns`: 1
  - `hosting`: 1
  - `messaging`: 1
  - `misc`: 1
- Counts by confidence:
  - `high`: 1
  - `low`: 4
  - `medium`: 2
- Oldest `last_verified_at`: **2026-01-01**
<!-- STATS:END -->

## Governance

See:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)
- [LICENSE](LICENSE)
