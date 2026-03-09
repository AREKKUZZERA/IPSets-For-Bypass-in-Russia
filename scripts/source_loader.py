from __future__ import annotations

import json
from pathlib import Path

from scripts.io_utils import read_list_file
from scripts.models import LegacyInputs, SourceRecord


def _record_from_legacy(value: str, rec_type: str, action: str, source_name: str) -> SourceRecord:
    return SourceRecord(
        type=rec_type,  # type: ignore[arg-type]
        value=value.strip(),
        action=action,  # type: ignore[arg-type]
        source=source_name,
        source_url="legacy-root-files",
        comment="Imported from legacy input",
        tags=["legacy"],
        confidence=0.6,
    )


def load_legacy_records(inputs: LegacyInputs) -> list[SourceRecord]:
    records: list[SourceRecord] = []
    records.extend(_record_from_legacy(v, "cidr", "proxy", "ipset-all.txt") for v in read_list_file(inputs.ipset_path))
    records.extend(_record_from_legacy(v, "cidr", "exclude", "exclude.txt") for v in read_list_file(inputs.exclude_path))
    records.extend(_record_from_legacy(v.lower(), "domain", "exclude", "exclude-domains.txt") for v in read_list_file(inputs.exclude_domains_path))
    return records


def load_sources_records(sources_dir: str | Path = "sources") -> list[SourceRecord]:
    records: list[SourceRecord] = []
    for path in sorted(Path(sources_dir).glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload.get("records", []):
            records.append(SourceRecord(**item))
    return records
