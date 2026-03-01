# Data Sources and Provenance

This repository stores network CIDR metadata in `data/entries.json`.

## Source expectations

Every entry must include:

- `source.kind`: acquisition method (`ripestat`, `manual`, `bgp`, `whois`, `other`)
- `source.ref`: concise source identifier (for example an ASN or internal token)
- `source.url`: URL to public evidence or authoritative documentation
- `last_verified_at`: date the source was last reviewed by a maintainer

## Placeholder bootstrapping data

Current entries are documentation-only placeholder ranges (RFC5737 and RFC3849) so tooling can run in CI before real data is migrated. Replace placeholders with validated production data and keep provenance complete for each record.
