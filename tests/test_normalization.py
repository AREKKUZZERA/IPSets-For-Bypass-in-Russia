from pathlib import Path

from scripts.models import LegacyInputs
from scripts.normalization import is_valid_cidr, normalize


def _write(path: Path, content: str) -> str:
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_deduplication_and_sort(tmp_path: Path) -> None:
    ipset = _write(tmp_path / "ipset.txt", "2.2.2.0/24\n1.1.1.0/24\n2.2.2.0/24\n")
    exclude = _write(tmp_path / "exclude.txt", "")
    domains = _write(tmp_path / "exclude-domains.txt", "")

    data, result = normalize(LegacyInputs(ipset, exclude, domains))

    assert result.ok
    assert data.cidrs == ["1.1.1.0/24", "2.2.2.0/24"]


def test_exclude_application(tmp_path: Path) -> None:
    ipset = _write(tmp_path / "ipset.txt", "1.1.1.0/24\n2.2.2.0/24\n")
    exclude = _write(tmp_path / "exclude.txt", "2.2.2.0/24\n")
    domains = _write(tmp_path / "exclude-domains.txt", "")

    data, _ = normalize(LegacyInputs(ipset, exclude, domains))

    assert data.cidrs == ["1.1.1.0/24"]


def test_cidr_validation() -> None:
    assert is_valid_cidr("10.0.0.0/8")
    assert not is_valid_cidr("10.0.0.0/33")


def test_deterministic_sort(tmp_path: Path) -> None:
    ipset = _write(tmp_path / "ipset.txt", "10.0.0.0/8\n1.1.1.0/24\n")
    exclude = _write(tmp_path / "exclude.txt", "")
    domains = _write(tmp_path / "exclude-domains.txt", "")

    first, _ = normalize(LegacyInputs(ipset, exclude, domains))
    second, _ = normalize(LegacyInputs(ipset, exclude, domains))

    assert first.cidrs == second.cidrs
