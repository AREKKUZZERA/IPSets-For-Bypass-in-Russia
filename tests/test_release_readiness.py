from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts.release_validate import SEMVER_TAG_RE


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_semver_release_tag_regex() -> None:
    assert SEMVER_TAG_RE.fullmatch("v1.2.3")
    assert SEMVER_TAG_RE.fullmatch("v1.2.3-rc.1")
    assert not SEMVER_TAG_RE.fullmatch("1.2.3")
    assert not SEMVER_TAG_RE.fullmatch("v1.2")


def test_manifest_contains_checksums_and_files_exist(tmp_path: Path) -> None:
    subprocess.run(
        [
            "python",
            "-m",
            "scripts.build",
            "--input-mode=hybrid",
            "--profile=full",
            "--deterministic",
            "--checksums",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    manifest = json.loads((REPO_ROOT / "dist/manifest.json").read_text(encoding="utf-8"))
    assert "checksums" in manifest
    assert manifest["generated_at"] == "1970-01-01T00:00:00+00:00"

    for entry in manifest["checksums"]:
        assert (REPO_ROOT / "dist" / entry["checksum_file"]).exists()
        assert len(entry["sha256"]) == 64
