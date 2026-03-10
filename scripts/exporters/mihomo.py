from __future__ import annotations

from pathlib import Path

from scripts.io_utils import write_generated_list

from . import ExportArtifact, ExportContext, split_cidrs


def _write_yaml_rules(path: Path, rule_type: str, values: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["payload:"]
    lines.extend(f"  - '{rule_type},{value}'" for value in values)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export(context: ExportContext) -> list[ExportArtifact]:
    data = context.data
    base = context.dist_dir / "mihomo"
    ipv4, ipv6 = split_cidrs(data.cidrs)

    _write_yaml_rules(base / "domains.yaml", "DOMAIN-SUFFIX", data.exclude_domains)
    _write_yaml_rules(base / "ipcidr.yaml", "IP-CIDR", data.cidrs)
    write_generated_list(base / "ipcidr.txt", data.cidrs)
    write_generated_list(base / "ipv4.txt", ipv4)
    write_generated_list(base / "ipv6.txt", ipv6)

    return [
        ExportArtifact(path="mihomo/domains.yaml", format="mihomo", kind="domains-rule-provider", count=len(data.exclude_domains)),
        ExportArtifact(path="mihomo/ipcidr.yaml", format="mihomo", kind="ipcidr-rule-provider", count=len(data.cidrs)),
        ExportArtifact(path="mihomo/ipcidr.txt", format="mihomo", kind="ipcidr-text", count=len(data.cidrs)),
        ExportArtifact(path="mihomo/ipv4.txt", format="mihomo", kind="ipv4-text", count=len(ipv4)),
        ExportArtifact(path="mihomo/ipv6.txt", format="mihomo", kind="ipv6-text", count=len(ipv6)),
    ]
