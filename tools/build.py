#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import ipaddress
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "entries.json"
DIST_DIR = ROOT / "dist"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        Path(tmp.name).replace(path)


def network_sort_key(cidr: str) -> tuple[int, int, int, str]:
    network = ipaddress.ip_network(cidr, strict=True)
    return (
        network.version,
        int(network.network_address),
        network.prefixlen,
        str(network),
    )


def render_list(cidrs: set[str]) -> str:
    ordered = sorted(cidrs, key=network_sort_key)
    return "\n".join(ordered) + "\n"


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = data.get("entries", [])

    by_category: dict[str, set[str]] = {}
    all_cidrs: set[str] = set()
    for entry in entries:
        cidr = entry["cidr"]
        category = entry["category"]
        all_cidrs.add(cidr)
        by_category.setdefault(category, set()).add(cidr)

    outputs: dict[str, str] = {}
    outputs["ipset-all.txt"] = render_list(all_cidrs)
    for category in sorted(by_category):
        outputs[f"ipset-{category}.txt"] = render_list(by_category[category])

    for filename, content in outputs.items():
        atomic_write(DIST_DIR / filename, content)

    checksum_lines = []
    for filename in sorted(outputs):
        file_path = DIST_DIR / filename
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        checksum_lines.append(f"{digest}  {filename}")
    atomic_write(DIST_DIR / "checksums.txt", "\n".join(checksum_lines) + "\n")

    print(f"Generated {len(outputs)} dist file(s) plus checksums.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
