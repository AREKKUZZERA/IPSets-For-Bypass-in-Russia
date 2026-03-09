import json
from pathlib import Path

from scripts.models import LegacyInputs
from scripts.normalization import normalize


def _write(path: Path, content: str) -> str:
    path.write_text(content, encoding="utf-8")
    return str(path)


def _inputs(tmp_path: Path, ipset: str, exclude: str = "", domains: str = "") -> LegacyInputs:
    return LegacyInputs(
        _write(tmp_path / "ipset.txt", ipset),
        _write(tmp_path / "exclude.txt", exclude),
        _write(tmp_path / "exclude-domains.txt", domains),
    )


def test_overlap_detection(tmp_path: Path) -> None:
    data, result = normalize(_inputs(tmp_path, "1.1.0.0/16\n1.1.1.0/24\n"), input_mode="legacy")
    assert data.cidrs == ["1.1.0.0/16", "1.1.1.0/24"]
    assert any("Overlapping CIDRs" in x for x in result.warnings)


def test_ipv6_handling(tmp_path: Path) -> None:
    data, result = normalize(_inputs(tmp_path, "2606:4700::/32\n1.1.1.0/24\n"), input_mode="legacy")
    assert result.ok
    assert data.cidrs == ["1.1.1.0/24", "2606:4700::/32"]


def test_conflict_detection(tmp_path: Path) -> None:
    _, result = normalize(_inputs(tmp_path, "8.8.8.0/24\n", "8.8.8.0/25\n"), input_mode="legacy")
    assert any("Include/exclude conflict" in x for x in result.problems)


def test_needs_review_behavior_for_special_ranges(tmp_path: Path) -> None:
    data, _ = normalize(_inputs(tmp_path, "10.0.0.0/8\n1.1.1.0/24\n"), input_mode="legacy")
    assert data.cidrs == ["1.1.1.0/24"]
    assert any(item["value"] == "10.0.0.0/8" for item in data.needs_review)


def test_hybrid_input_loading(tmp_path: Path) -> None:
    src = tmp_path / "sources"
    src.mkdir()
    (src / "extra.json").write_text(
        json.dumps(
            {
                "records": [
                    {
                        "type": "cidr",
                        "value": "9.9.9.0/24",
                        "source": "test-src",
                        "action": "proxy",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    cwd = Path.cwd()
    try:
        import os

        os.chdir(tmp_path)
        data, _ = normalize(_inputs(tmp_path, "1.1.1.0/24\n"), input_mode="hybrid")
    finally:
        os.chdir(cwd)

    assert "1.1.1.0/24" in data.cidrs
    assert "9.9.9.0/24" in data.cidrs


def test_manifest_stats_presence(tmp_path: Path) -> None:
    data, _ = normalize(_inputs(tmp_path, "1.1.1.0/24\n", domains="example.com\n"), input_mode="legacy")
    assert data.stats["records_total"] == 2
    assert data.stats["by_type"]["cidr"] == 1
    assert data.stats["by_type"]["domain"] == 1
