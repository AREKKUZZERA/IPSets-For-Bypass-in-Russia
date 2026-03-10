from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from pathlib import Path

from scripts.models import NormalizedData

from .profiles import PROFILES, apply_profile


@dataclass
class ExportContext:
    data: NormalizedData
    profile: str
    dist_dir: Path = Path("dist")


@dataclass
class ExportArtifact:
    path: str
    format: str
    kind: str
    count: int


@dataclass
class ExportResult:
    artifacts: list[ExportArtifact]
    warnings: list[str]


def split_cidrs(cidrs: list[str]) -> tuple[list[str], list[str]]:
    ipv4: list[str] = []
    ipv6: list[str] = []
    for item in cidrs:
        net = ipaddress.ip_network(item, strict=False)
        if net.version == 4:
            ipv4.append(item)
        else:
            ipv6.append(item)
    return ipv4, ipv6


def category_views(data: NormalizedData) -> dict[str, list[str]]:
    ipv4, ipv6 = split_cidrs(data.cidrs)
    return {
        "misc": sorted(set(data.cidrs + data.exclude_domains)),
        "domains": list(data.exclude_domains),
        "ipcidr": list(data.cidrs),
        "ipv4": ipv4,
        "ipv6": ipv6,
    }


def export_all(data: NormalizedData, profile: str) -> ExportResult:
    from . import ipset, mihomo, nftables, singbox

    profiled = apply_profile(data, profile)
    context = ExportContext(data=profiled, profile=profile)
    artifacts: list[ExportArtifact] = []

    for module in (ipset, singbox, mihomo, nftables):
        artifacts.extend(module.export(context))

    warnings = [f"empty export: {a.path}" for a in artifacts if a.count == 0]
    return ExportResult(artifacts=artifacts, warnings=warnings)


__all__ = ["PROFILES", "ExportArtifact", "ExportResult", "category_views", "export_all", "split_cidrs"]
