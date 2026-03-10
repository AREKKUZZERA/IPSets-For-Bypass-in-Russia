from __future__ import annotations

from scripts.io_utils import write_generated_list

from . import ExportArtifact, ExportContext


def export(context: ExportContext) -> list[ExportArtifact]:
    data = context.data
    artifacts = [
        ("ipset/ipset-all.txt", data.cidrs, "ipset", "cidr-list"),
        ("ipset/exclude.txt", data.excludes, "ipset", "exclude-cidr-list"),
        ("ipset/exclude-domains.txt", data.exclude_domains, "ipset", "exclude-domain-list"),
    ]

    exported: list[ExportArtifact] = []
    for rel_path, values, fmt, kind in artifacts:
        out_path = context.dist_dir / rel_path
        write_generated_list(out_path, values)
        exported.append(ExportArtifact(path=str(rel_path), format=fmt, kind=kind, count=len(values)))
    return exported
