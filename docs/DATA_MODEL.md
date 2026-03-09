# Data Model (Stage 2)

## Input strategy
- Legacy inputs remain supported:
  - `ipset-all.txt`
  - `exclude.txt`
  - `exclude-domains.txt`
- New preferred format for new records: machine-readable `sources/*.json`.
- Loader modes:
  - `legacy`
  - `hybrid` (default)
  - `sources`

## Source record schema
Each record in `sources/*.json` supports:
- `type` (`cidr` / `domain`)
- `value`
- `service`
- `category`
- `source`
- `source_url`
- `comment`
- `tags`
- `action` (`proxy`, `direct`, `exclude`, `neutral`)
- `platforms`
- `priority`
- `needs_review`
- `confidence`
- `updated_at`

## Normalized model
`NormalizedData`:
- `cidrs` — include CIDR result set.
- `excludes` — CIDRs marked as exclude.
- `exclude_domains` — domain excludes.
- `needs_review` — suspicious/ambiguous records retained for manual triage.
- `stats` — summary counters (`records_total`, `by_type`, `by_source`).

`ValidationResult`:
- `errors` — blocking issues.
- `warnings` — non-blocking quality issues (e.g., overlaps).
- `problems` — semantic conflicts (e.g., include/exclude overlap).

## Stage 2 validation highlights
- CIDR/domain validation with IPv4 + IPv6 support.
- Filtering of private/loopback/link-local/multicast/reserved/unspecified ranges.
- Conflict detection between include and exclude sets.
- Overlap detection within include CIDR set.
- Deterministic sorting with IPv4 before IPv6.
