from __future__ import annotations

import json
from pathlib import Path


def read_list_file(path: str | Path) -> list[str]:
    lines: list[str] = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def write_generated_list(path: str | Path, values: list[str]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    header = "# GENERATED FILE: do not edit manually\n"
    body = "\n".join(values)
    p.write_text(header + (body + "\n" if body else ""), encoding="utf-8")


def write_manifest(path: str | Path, manifest: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
