from __future__ import annotations

from datetime import datetime, timezone

from scripts.io_utils import write_generated_list, write_manifest
from scripts.models import LegacyInputs
from scripts.normalization import normalize


def main() -> int:
    inputs = LegacyInputs(
        ipset_path="ipset-all.txt",
        exclude_path="exclude.txt",
        exclude_domains_path="exclude-domains.txt",
    )
    data, validation = normalize(inputs)

    write_generated_list("dist/ipset/ipset-all.txt", data.cidrs)
    write_generated_list("dist/ipset/exclude.txt", data.excludes)
    write_generated_list("dist/ipset/exclude-domains.txt", data.exclude_domains)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stage": "mvp-foundation",
        "inputs": {
            "ipset": inputs.ipset_path,
            "exclude": inputs.exclude_path,
            "exclude_domains": inputs.exclude_domains_path,
        },
        "counts": {
            "cidrs": len(data.cidrs),
            "excludes": len(data.excludes),
            "exclude_domains": len(data.exclude_domains),
        },
        "warnings": validation.warnings,
        "errors": validation.errors,
    }
    write_manifest("dist/manifest.json", manifest)

    return 1 if validation.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
