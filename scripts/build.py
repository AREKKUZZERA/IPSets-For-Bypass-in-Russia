from __future__ import annotations

import argparse
from datetime import datetime, timezone

from scripts.exporters import PROFILES, export_all
from scripts.io_utils import write_manifest
from scripts.models import LegacyInputs
from scripts.normalization import normalize


def main() -> int:
    parser = argparse.ArgumentParser(description="Build normalized artifacts")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings/problems/needs_review")
    parser.add_argument("--input-mode", choices=["legacy", "hybrid", "sources"], default="hybrid")
    parser.add_argument("--profile", choices=sorted(PROFILES.keys()), default="full")
    args = parser.parse_args()

    inputs = LegacyInputs(
        ipset_path="ipset-all.txt",
        exclude_path="exclude.txt",
        exclude_domains_path="exclude-domains.txt",
    )
    data, validation = normalize(inputs, input_mode=args.input_mode)
    exports = export_all(data, profile=args.profile)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stage": "stage-3-exports",
        "input_mode": args.input_mode,
        "build_profile": args.profile,
        "inputs": {
            "ipset": inputs.ipset_path,
            "exclude": inputs.exclude_path,
            "exclude_domains": inputs.exclude_domains_path,
            "sources_dir": "sources/*.json",
        },
        "counts": {
            "cidrs": len(data.cidrs),
            "excludes": len(data.excludes),
            "exclude_domains": len(data.exclude_domains),
            "records_total": data.stats.get("records_total", 0),
        },
        "stats": {
            "by_type": data.stats.get("by_type", {}),
            "by_source": data.stats.get("by_source", {}),
        },
        "artifacts": [a.__dict__ for a in exports.artifacts],
        "warnings": [*validation.warnings, *exports.warnings],
        "problems": validation.problems,
        "errors": validation.errors,
        "needs_review": data.needs_review,
    }
    write_manifest("dist/manifest.json", manifest)

    if validation.errors:
        return 1
    if args.strict and (manifest["warnings"] or validation.problems or data.needs_review):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
