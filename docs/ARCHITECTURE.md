# Architecture (Stage 3)

## Scope
Stage 3 adds a modular export layer for modern generated formats while preserving legacy ipset compatibility.

## Data flow
1. Load records from `legacy`, `sources`, or `hybrid` mode.
2. Normalize + validate records into a single internal model (`NormalizedData`).
3. Apply export profile (`full|lite|domains-only|ip-only`).
4. Generate all outputs through `scripts/exporters/*`.
5. Emit manifest with artifact metadata and empty-export warnings.

## Modules
- `scripts/models.py` — internal data model.
- `scripts/normalization.py` — normalization and checks.
- `scripts/build.py` — orchestration + manifest.
- `scripts/exporters/profiles.py` — profile filtering.
- `scripts/exporters/ipset.py` — legacy compatibility exporter.
- `scripts/exporters/singbox.py` — sing-box source rule-set exporter.
- `scripts/exporters/mihomo.py` — mihomo providers (yaml/text).
- `scripts/exporters/nftables.py` — nftables include sets.

## Build artifacts
- `dist/ipset/*` (legacy compatibility)
- `dist/sing-box/*` (source JSON rule-sets)
- `dist/mihomo/*` (rule-providers)
- `dist/nftables/*` (include files)
- `dist/manifest.json`
