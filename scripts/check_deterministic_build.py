from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
from pathlib import Path


def _run_build(output_dir: Path, input_mode: str, profile: str) -> None:
    subprocess.run(
        [
            "python",
            "-m",
            "scripts.build",
            "--deterministic",
            "--checksums",
            f"--input-mode={input_mode}",
            f"--profile={profile}",
        ],
        check=True,
    )
    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree("dist", output_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ensure build output is deterministic")
    parser.add_argument("--input-mode", choices=["legacy", "hybrid", "sources"], default="hybrid")
    parser.add_argument("--profile", default="full")
    parser.add_argument("--first", default=".tmp-dist-first")
    parser.add_argument("--second", default=".tmp-dist-second")
    args = parser.parse_args()

    first = Path(args.first)
    second = Path(args.second)

    _run_build(first, args.input_mode, args.profile)
    _run_build(second, args.input_mode, args.profile)

    def collect_diffs(cmp: filecmp.dircmp) -> list[str]:
        diffs: list[str] = []
        for name in cmp.left_only:
            diffs.append(f"missing-in-second:{cmp.left}/{name}")
        for name in cmp.right_only:
            diffs.append(f"missing-in-first:{cmp.right}/{name}")
        for name in cmp.diff_files:
            diffs.append(f"content-diff:{cmp.left}/{name}")
        for sub in cmp.subdirs.values():
            diffs.extend(collect_diffs(sub))
        return diffs

    diffs = collect_diffs(filecmp.dircmp(first, second))
    if diffs:
        print("Non-deterministic build detected")
        for item in diffs:
            print(item)
        return 1

    print("Deterministic build check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
