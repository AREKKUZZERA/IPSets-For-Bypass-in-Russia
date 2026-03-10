# Exports (Stage 3)

## Export layer
All generated artifacts are now emitted via `scripts/exporters/*` from one normalized model (`NormalizedData`).

## Build profiles
- `full` — all records.
- `lite` — first 256 records per type (deterministic) for compact usage.
- `domains-only` — only domain datasets.
- `ip-only` — only CIDR datasets.

## Formats
- Legacy compatibility: `dist/ipset/*.txt`.
- sing-box source rule-sets: aggregate + split (`domains`, `ipcidr`, `ipv4`, `ipv6`).
- mihomo rule-providers: YAML (`domains.yaml`, `ipcidr.yaml`) + text lists (`ipcidr.txt`, `ipv4.txt`, `ipv6.txt`).
- nftables include sets: `ipv4.nft`, `ipv6.nft`, `include.nft`.

## Notes / TODO
- `.srs` compilation intentionally not included in stage 3.
- Category decomposition is intentionally minimal (`misc`, `domains`, `ipcidr`, `ipv4`, `ipv6`).
