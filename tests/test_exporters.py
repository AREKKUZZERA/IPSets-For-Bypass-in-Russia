from __future__ import annotations

import json
import os
from pathlib import Path

from scripts.exporters import export_all
from scripts.models import NormalizedData


def _sample_data() -> NormalizedData:
    return NormalizedData(
        cidrs=["1.1.1.0/24", "2606:4700::/32", "8.8.8.0/24"],
        excludes=["9.9.9.0/24"],
        exclude_domains=["example.com", "service.test"],
    )


def test_export_correctness_and_split(tmp_path: Path) -> None:
    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        result = export_all(_sample_data(), profile="full")
    finally:
        os.chdir(cwd)

    assert any(a.path == "ipset/ipset-all.txt" for a in result.artifacts)

    singbox = json.loads((tmp_path / "dist/sing-box/rule-set-aggregate.json").read_text(encoding="utf-8"))
    assert singbox["rules"][0]["ip_cidr"] == ["1.1.1.0/24", "2606:4700::/32", "8.8.8.0/24"]
    assert singbox["rules"][0]["domain_suffix"] == ["example.com", "service.test"]

    nft_v4 = (tmp_path / "dist/nftables/ipv4.nft").read_text(encoding="utf-8")
    nft_v6 = (tmp_path / "dist/nftables/ipv6.nft").read_text(encoding="utf-8")
    assert "1.1.1.0/24" in nft_v4 and "8.8.8.0/24" in nft_v4
    assert "2606:4700::/32" in nft_v6


def test_empty_dataset_behavior(tmp_path: Path) -> None:
    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        result = export_all(NormalizedData(), profile="full")
    finally:
        os.chdir(cwd)

    assert result.warnings
    assert any("empty export" in item for item in result.warnings)


def test_profile_filtering(tmp_path: Path) -> None:
    data = _sample_data()
    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        export_all(data, profile="domains-only")
    finally:
        os.chdir(cwd)

    singbox = json.loads((tmp_path / "dist/sing-box/rule-set-aggregate.json").read_text(encoding="utf-8"))
    assert singbox["rules"][0]["ip_cidr"] == []
    assert singbox["rules"][0]["domain_suffix"] == ["example.com", "service.test"]


def test_deterministic_ordering(tmp_path: Path) -> None:
    data = _sample_data()

    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        export_all(data, profile="full")
        first = (tmp_path / "dist/mihomo/ipcidr.txt").read_text(encoding="utf-8")
        export_all(data, profile="full")
        second = (tmp_path / "dist/mihomo/ipcidr.txt").read_text(encoding="utf-8")
    finally:
        os.chdir(cwd)

    assert first == second
