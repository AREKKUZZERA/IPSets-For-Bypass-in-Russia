#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "entries.json"
README_PATH = ROOT / "README.md"
BEGIN = "<!-- STATS:BEGIN -->"
END = "<!-- STATS:END -->"


def render_stats(entries: list[dict]) -> str:
    category_counts = Counter(entry["category"] for entry in entries)
    confidence_counts = Counter(entry["confidence"] for entry in entries)
    oldest_verified = min(entry["last_verified_at"] for entry in entries) if entries else "n/a"

    lines = [
        "### Dataset Stats",
        "",
        f"- Total entries: **{len(entries)}**",
        "- Counts by category:",
    ]
    for category in sorted(category_counts):
        lines.append(f"  - `{category}`: {category_counts[category]}")
    lines.append("- Counts by confidence:")
    for confidence in sorted(confidence_counts):
        lines.append(f"  - `{confidence}`: {confidence_counts[confidence]}")
    lines.append(f"- Oldest `last_verified_at`: **{oldest_verified}**")
    return "\n".join(lines)


def replace_between_markers(content: str, generated: str) -> str:
    if BEGIN not in content or END not in content:
        raise ValueError("README markers not found")
    start = content.index(BEGIN) + len(BEGIN)
    end = content.index(END)
    return content[:start] + "\n" + generated + "\n" + content[end:]


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    generated = render_stats(entries)

    readme = README_PATH.read_text(encoding="utf-8")
    updated = replace_between_markers(readme, generated)
    README_PATH.write_text(updated, encoding="utf-8")

    print("Updated README stats block.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
