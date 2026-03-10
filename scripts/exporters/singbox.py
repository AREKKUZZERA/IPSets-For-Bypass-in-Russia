from __future__ import annotations

import json
from pathlib import Path

from . import ExportArtifact, ExportContext, category_views


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export(context: ExportContext) -> list[ExportArtifact]:
    data = context.data
    categories = category_views(data)
    base = context.dist_dir / "sing-box"

    artifacts: list[ExportArtifact] = []

    aggregate_payload = {
        "version": 1,
        "rules": [
            {
                "domain_suffix": data.exclude_domains,
                "ip_cidr": data.cidrs,
            }
        ],
    }
    aggregate_path = base / "rule-set-aggregate.json"
    _write_json(aggregate_path, aggregate_payload)
    artifacts.append(
        ExportArtifact(
            path="sing-box/rule-set-aggregate.json",
            format="sing-box-source",
            kind="aggregate",
            count=len(data.exclude_domains) + len(data.cidrs),
        )
    )

    for name in ("domains", "ipcidr", "ipv4", "ipv6"):
        values = categories[name]
        key = "domain_suffix" if name == "domains" else "ip_cidr"
        payload = {"version": 1, "rules": [{key: values}]}
        rel = f"sing-box/rule-set-{name}.json"
        _write_json(context.dist_dir / rel, payload)
        artifacts.append(ExportArtifact(path=rel, format="sing-box-source", kind=name, count=len(values)))

    return artifacts
