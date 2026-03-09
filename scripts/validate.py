from __future__ import annotations

import argparse

from scripts.models import LegacyInputs
from scripts.normalization import normalize


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate normalized inputs")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings/problems/needs_review")
    parser.add_argument("--input-mode", choices=["legacy", "hybrid", "sources"], default="hybrid")
    args = parser.parse_args()

    data, result = normalize(
        LegacyInputs(
            ipset_path="ipset-all.txt",
            exclude_path="exclude.txt",
            exclude_domains_path="exclude-domains.txt",
        ),
        input_mode=args.input_mode,
    )

    print(f"CIDRs: {len(data.cidrs)}")
    print(f"Exclude CIDRs: {len(data.excludes)}")
    print(f"Exclude domains: {len(data.exclude_domains)}")
    print(f"Needs review: {len(data.needs_review)}")

    for warning in result.warnings:
        print(f"WARN: {warning}")
    for problem in result.problems:
        print(f"PROBLEM: {problem}")
    for error in result.errors:
        print(f"ERROR: {error}")

    if result.errors:
        return 1
    if args.strict and (result.warnings or result.problems or data.needs_review):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
