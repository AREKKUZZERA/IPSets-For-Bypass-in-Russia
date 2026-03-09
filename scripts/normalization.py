from __future__ import annotations

import ipaddress
import re
from collections import Counter

from scripts.models import InputMode, LegacyInputs, NormalizedData, SourceRecord, ValidationResult
from scripts.source_loader import load_legacy_records, load_sources_records

DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
MAX_REPORTED_ISSUES = 200


def is_valid_cidr(value: str) -> bool:
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def is_valid_domain(value: str) -> bool:
    return bool(DOMAIN_RE.fullmatch(value.strip().lower()))


def _network_sort_key(network: ipaddress._BaseNetwork) -> tuple[int, int, int]:
    return (network.version, int(network.network_address), network.prefixlen)


def _network_interval(network: ipaddress._BaseNetwork) -> tuple[int, int, ipaddress._BaseNetwork]:
    start = int(network.network_address)
    end = int(network.broadcast_address)
    return start, end, network


def _is_special_network(network: ipaddress._BaseNetwork) -> bool:
    addr = network.network_address
    return bool(
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )


def _load_records(inputs: LegacyInputs, input_mode: InputMode) -> list[SourceRecord]:
    if input_mode == "legacy":
        return load_legacy_records(inputs)
    if input_mode == "sources":
        return load_sources_records()
    return [*load_sources_records(), *load_legacy_records(inputs)]


def _detect_include_overlaps(include_nets: list[ipaddress._BaseNetwork]) -> list[str]:
    warnings: list[str] = []
    for version in (4, 6):
        intervals = sorted((_network_interval(n) for n in include_nets if n.version == version), key=lambda x: (x[0], x[1]))
        prev_start = -1
        prev_end = -1
        prev_net: ipaddress._BaseNetwork | None = None
        for start, end, net in intervals:
            if start <= prev_end and prev_net is not None:
                warnings.append(f"Overlapping CIDRs: {prev_net} and {net}")
                if len(warnings) >= MAX_REPORTED_ISSUES:
                    warnings.append("Overlapping CIDRs: report truncated")
                    return warnings
            if end > prev_end:
                prev_start, prev_end, prev_net = start, end, net
    return warnings


def _detect_include_exclude_conflicts(
    include_nets: list[ipaddress._BaseNetwork],
    exclude_nets: list[ipaddress._BaseNetwork],
) -> list[str]:
    conflicts: list[str] = []
    for version in (4, 6):
        includes = sorted((_network_interval(n) for n in include_nets if n.version == version), key=lambda x: x[0])
        excludes = sorted((_network_interval(n) for n in exclude_nets if n.version == version), key=lambda x: x[0])
        j = 0
        for i_start, i_end, i_net in includes:
            while j < len(excludes) and excludes[j][1] < i_start:
                j += 1
            k = j
            while k < len(excludes) and excludes[k][0] <= i_end:
                e_start, e_end, e_net = excludes[k]
                if not (e_end < i_start or e_start > i_end):
                    conflicts.append(f"Include/exclude conflict: {i_net} vs {e_net}")
                    if len(conflicts) >= MAX_REPORTED_ISSUES:
                        conflicts.append("Include/exclude conflict: report truncated")
                        return conflicts
                k += 1
    return conflicts


def normalize(inputs: LegacyInputs, input_mode: InputMode = "hybrid") -> tuple[NormalizedData, ValidationResult]:
    result = ValidationResult()
    records = _load_records(inputs, input_mode)

    include_nets: dict[str, ipaddress._BaseNetwork] = {}
    exclude_nets: dict[str, ipaddress._BaseNetwork] = {}
    exclude_domains: set[str] = set()
    needs_review: list[dict] = []

    type_stats = Counter()
    source_stats = Counter()

    for rec in records:
        type_stats[rec.type] += 1
        source_stats[rec.source] += 1

        if rec.type == "domain":
            domain = rec.value.lower().strip()
            if not is_valid_domain(domain):
                result.warnings.append(f"Invalid domain skipped: {rec.value}")
                continue
            if rec.action == "exclude":
                exclude_domains.add(domain)
            continue

        if rec.type != "cidr":
            result.warnings.append(f"Unknown record type skipped: {rec.type}")
            continue

        if not is_valid_cidr(rec.value):
            result.errors.append(f"Invalid CIDR: {rec.value}")
            continue

        network = ipaddress.ip_network(rec.value, strict=False)
        key = str(network)

        if rec.needs_review:
            needs_review.append({"value": key, "reason": "pre-marked", "source": rec.source})

        if _is_special_network(network):
            needs_review.append({"value": key, "reason": "special-purpose-range", "source": rec.source})
            continue

        if rec.action == "exclude":
            exclude_nets[key] = network
        elif rec.action in {"proxy", "direct", "neutral"}:
            include_nets[key] = network
        else:
            needs_review.append({"value": key, "reason": f"unknown-action:{rec.action}", "source": rec.source})

    include_values = list(include_nets.values())
    exclude_values = list(exclude_nets.values())
    result.problems.extend(_detect_include_exclude_conflicts(include_values, exclude_values))
    result.warnings.extend(_detect_include_overlaps(include_values))

    cidrs_sorted = sorted(include_values, key=_network_sort_key)
    excludes_sorted = sorted(exclude_values, key=_network_sort_key)

    data = NormalizedData(
        cidrs=[str(n) for n in cidrs_sorted],
        excludes=[str(n) for n in excludes_sorted],
        exclude_domains=sorted(exclude_domains),
        needs_review=needs_review,
        stats={
            "records_total": len(records),
            "by_type": dict(type_stats),
            "by_source": dict(source_stats),
        },
    )
    return data, result
