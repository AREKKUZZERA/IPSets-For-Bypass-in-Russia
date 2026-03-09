# Data Model (Stage 1)

## Legacy inputs
- `ipset-all.txt`: CIDR list.
- `exclude.txt`: CIDRs to remove from final set.
- `exclude-domains.txt`: domains excluded at domain layer.

## Internal normalized model
`NormalizedData`:
- `cidrs: list[str]` — validated CIDRs, exclude-applied, deduplicated and sorted.
- `excludes: list[str]` — validated exclude CIDRs, deduplicated and sorted.
- `exclude_domains: list[str]` — validated domains, lowercased, deduplicated and sorted.

`ValidationResult`:
- `errors: list[str]` — blocking issues (invalid CIDRs in primary input).
- `warnings: list[str]` — non-blocking skips (invalid excludes/domains).

## Generated outputs
- `dist/ipset/ipset-all.txt`
- `dist/ipset/exclude.txt`
- `dist/ipset/exclude-domains.txt`
- `dist/manifest.json`

All generated text files include a "do not edit manually" header.
