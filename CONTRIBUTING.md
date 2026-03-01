# Contributing

Thanks for contributing to this dataset.

## Quick start

1. Create a branch from `main`.
2. Edit `data/entries.json`.
3. Ensure each entry includes complete source metadata and verification dates.
4. Run:
   ```bash
   python tools/validate.py
   python tools/build.py
   python tools/stats.py
   ```
5. Commit dataset updates along with regenerated `dist/*` and README stats.
6. Open a Pull Request.

## Data requirements

- Use the required categories: `cdn`, `cloud`, `hosting`, `messaging`, `dns`, `misc`.
- Provide `source.kind`, `source.ref`, and `source.url` for every entry.
- Keep `added_at` and `last_verified_at` in `YYYY-MM-DD` format.
- Use `confidence` values: `high`, `medium`, `low`.

## Validation policies

- Duplicate `cidr + category` pairs are rejected.
- CIDR entries overlapping within the same category are rejected.
- If the same CIDR is intentionally reused across categories, every matching entry must include `allow_multi_category: true`.
- Wide ranges require explicit approval:
  - IPv4 prefixes broader than `/12`
  - IPv6 prefixes broader than `/32`

For approved wide ranges, include `wide_ok: true` and explanatory `notes`.

## Generated files

`dist/` is generated content. Do not edit by hand.
