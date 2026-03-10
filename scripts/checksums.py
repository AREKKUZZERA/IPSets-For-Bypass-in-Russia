from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksums(dist_dir: Path, artifact_paths: list[str]) -> list[dict[str, str]]:
    checksums_dir = dist_dir / "checksums"
    checksums_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, str]] = []
    for rel in sorted(set(artifact_paths + ["manifest.json"])):
        target = dist_dir / rel
        if not target.exists():
            continue
        checksum = sha256_file(target)
        checksum_rel = f"checksums/{rel.replace('/', '__')}.sha256"
        checksum_path = dist_dir / checksum_rel
        checksum_path.parent.mkdir(parents=True, exist_ok=True)
        checksum_path.write_text(f"{checksum}  {rel}\n", encoding="utf-8")
        entries.append({"path": rel, "sha256": checksum, "checksum_file": checksum_rel})

    entries_sorted = sorted(entries, key=lambda x: x["path"])
    summary = "".join(f"{item['sha256']}  {item['path']}\n" for item in entries_sorted)
    (checksums_dir / "SHA256SUMS").write_text(summary, encoding="utf-8")
    return entries_sorted
