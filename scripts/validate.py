from __future__ import annotations

from scripts.models import LegacyInputs
from scripts.normalization import normalize


def main() -> int:
    data, result = normalize(
        LegacyInputs(
            ipset_path="ipset-all.txt",
            exclude_path="exclude.txt",
            exclude_domains_path="exclude-domains.txt",
        )
    )

    print(f"CIDRs: {len(data.cidrs)}")
    print(f"Exclude CIDRs: {len(data.excludes)}")
    print(f"Exclude domains: {len(data.exclude_domains)}")

    for warning in result.warnings:
        print(f"WARN: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
