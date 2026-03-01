#!/usr/bin/env python3
from __future__ import annotations

import ipaddress
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "entries.json"

ALLOWED_CATEGORIES = {"cdn", "cloud", "hosting", "messaging", "dns", "misc"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}


def parse_date(value: str, field: str, idx: int, errors: list[str]) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except Exception:
        errors.append(f"entry #{idx}: invalid {field} date '{value}' (expected YYYY-MM-DD)")


def find_overlaps(networks: list[tuple[ipaddress._BaseNetwork, int]]) -> list[tuple[int, int, str, str]]:
    overlaps: list[tuple[int, int, str, str]] = []
    ordered = sorted(
        networks,
        key=lambda item: (
            item[0].version,
            int(item[0].network_address),
            item[0].prefixlen,
        ),
    )

    prev_by_version: dict[int, tuple[ipaddress._BaseNetwork, int]] = {}
    for network, idx in ordered:
        prev = prev_by_version.get(network.version)
        if prev:
            prev_net, prev_idx = prev
            if network.overlaps(prev_net):
                overlaps.append((prev_idx, idx, str(prev_net), str(network)))
            if int(network.broadcast_address) > int(prev_net.broadcast_address):
                prev_by_version[network.version] = (network, idx)
        else:
            prev_by_version[network.version] = (network, idx)
    return overlaps


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    if not isinstance(data.get("version"), int):
        errors.append("top-level 'version' must be an integer")
    if not isinstance(data.get("generated_hint"), str) or not data["generated_hint"].strip():
        errors.append("top-level 'generated_hint' must be a non-empty string")

    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("top-level 'entries' must be a list")
        entries = []

    seen_pair: set[tuple[str, str]] = set()
    cidr_categories: dict[str, set[str]] = {}
    category_networks: dict[str, list[tuple[ipaddress._BaseNetwork, int]]] = {}

    for idx, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            errors.append(f"entry #{idx}: entry must be an object")
            continue

        for field in ("cidr", "label", "category", "source", "added_at", "last_verified_at", "confidence"):
            if field not in entry:
                errors.append(f"entry #{idx}: missing required field '{field}'")

        cidr = entry.get("cidr")
        category = entry.get("category")
        confidence = entry.get("confidence")

        network = None
        if isinstance(cidr, str):
            try:
                network = ipaddress.ip_network(cidr, strict=True)
            except Exception:
                errors.append(f"entry #{idx}: invalid cidr '{cidr}'")
        else:
            errors.append(f"entry #{idx}: cidr must be a string")

        if not isinstance(entry.get("label"), str) or not entry["label"].strip():
            errors.append(f"entry #{idx}: label must be a non-empty string")

        if category not in ALLOWED_CATEGORIES:
            errors.append(f"entry #{idx}: category '{category}' is not allowed")

        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"entry #{idx}: confidence '{confidence}' is not allowed")

        source = entry.get("source")
        if not isinstance(source, dict):
            errors.append(f"entry #{idx}: source must be an object")
        else:
            for key in ("kind", "ref", "url"):
                value = source.get(key)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"entry #{idx}: source.{key} must be a non-empty string")

        for date_field in ("added_at", "last_verified_at"):
            value = entry.get(date_field)
            if isinstance(value, str):
                parse_date(value, date_field, idx, errors)
            else:
                errors.append(f"entry #{idx}: {date_field} must be a string")

        if isinstance(cidr, str) and isinstance(category, str):
            key = (cidr, category)
            if key in seen_pair:
                errors.append(f"entry #{idx}: duplicate cidr+category pair {cidr}/{category}")
            seen_pair.add(key)

            cidr_categories.setdefault(cidr, set()).add(category)

        if network is not None and isinstance(category, str) and category in ALLOWED_CATEGORIES:
            category_networks.setdefault(category, []).append((network, idx))

        if network is not None:
            wide_ok = entry.get("wide_ok") is True
            notes = str(entry.get("notes", ""))
            if network.version == 4 and network.prefixlen < 12 and not wide_ok:
                errors.append(
                    f"entry #{idx}: wide IPv4 range {network} requires wide_ok=true and explanatory notes"
                )
            if network.version == 6 and network.prefixlen < 32 and not wide_ok:
                errors.append(
                    f"entry #{idx}: wide IPv6 range {network} requires wide_ok=true and explanatory notes"
                )
            if wide_ok and not notes.strip():
                errors.append(f"entry #{idx}: wide_ok=true requires non-empty notes")

    for cidr, categories in sorted(cidr_categories.items()):
        if len(categories) > 1:
            allowed = [
                e
                for e in entries
                if isinstance(e, dict) and e.get("cidr") == cidr and e.get("allow_multi_category") is True
            ]
            if len(allowed) != len([e for e in entries if isinstance(e, dict) and e.get("cidr") == cidr]):
                errors.append(
                    f"cidr {cidr} appears in multiple categories {sorted(categories)} without allow_multi_category=true on every matching entry"
                )

    for category, networks in sorted(category_networks.items()):
        for left_idx, right_idx, left, right in find_overlaps(networks):
            errors.append(
                f"overlap in category '{category}': entry #{left_idx} ({left}) overlaps entry #{right_idx} ({right})"
            )

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Validation passed for {len(entries)} entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
