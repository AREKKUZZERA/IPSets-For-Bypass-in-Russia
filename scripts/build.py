from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

from scripts.checksums import write_checksums
from scripts.exporters import PROFILES, export_all
from scripts.io_utils import write_manifest
from scripts.models import LegacyInputs
from scripts.normalization import normalize


DEFAULT_DETERMINISTIC_TIMESTAMP = "1970-01-01T00:00:00+00:00"


def resolve_generated_at(deterministic: bool, generated_at_override: str | None = None) -> str:
    if generated_at_override:
        return generated_at_override
    if deterministic:
        return DEFAULT_DETERMINISTIC_TIMESTAMP

    source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
    if source_date_epoch:
        return datetime.fromtimestamp(int(source_date_epoch), tz=timezone.utc).isoformat()
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build normalized artifacts")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings/problems/needs_review")
    parser.add_argument("--input-mode", choices=["legacy", "hybrid", "sources"], default="hybrid")
    parser.add_argument("--profile", choices=sorted(PROFILES.keys()), default="full")
    parser.add_argument("--deterministic", action="store_true", help="Use deterministic generated_at metadata")
    parser.add_argument("--generated-at", help="Override generated_at value in manifest")
    parser.add_argument("--checksums", action="store_true", help="Generate SHA256 checksums for dist artifacts")
    args = parser.parse_args()

    inputs = LegacyInputs("ipset-all.txt", "exclude.txt", "exclude-domains.txt")
    data, validation = normalize(inputs, input_mode=args.input_mode)
    exports = export_all(data, profile=args.profile)

    manifest = {
        "generated_at": resolve_generated_at(args.deterministic, args.generated_at),
        "stage": "stage-4-release-readiness",
        "input_mode": args.input_mode,
        "build_profile": args.profile,
        "deterministic": bool(args.deterministic),
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
            "by_type": dict(sorted(data.stats.get("by_type", {}).items())),
            "by_source": dict(sorted(data.stats.get("by_source", {}).items())),
        },
        "artifacts": [a.__dict__ for a in sorted(exports.artifacts, key=lambda item: item.path)],
        "warnings": [*validation.warnings, *exports.warnings],
        "problems": validation.problems,
        "errors": validation.errors,
        "needs_review": sorted(data.needs_review, key=lambda item: (item.get("source", ""), item.get("value", ""))),
    }
    write_manifest("dist/manifest.json", manifest)

    if args.checksums:
        checksums = write_checksums(Path("dist"), [a.path for a in exports.artifacts])
        manifest["checksums"] = checksums
        manifest["artifacts"].append(
            {
                "path": "checksums/SHA256SUMS",
                "format": "checksum",
                "kind": "sha256-summary",
                "count": len(checksums),
            }
        )
        manifest["artifacts"] = sorted(manifest["artifacts"], key=lambda item: item["path"])
        write_manifest("dist/manifest.json", manifest)

    if validation.errors:
        return 1
    if args.strict and (manifest["warnings"] or validation.problems or data.needs_review):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
