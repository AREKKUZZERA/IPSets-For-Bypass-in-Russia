from __future__ import annotations

import ipaddress
import re

from scripts.models import LegacyInputs, NormalizedData, ValidationResult
from scripts.io_utils import read_list_file

DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")


def is_valid_cidr(value: str) -> bool:
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def is_valid_domain(value: str) -> bool:
    return bool(DOMAIN_RE.fullmatch(value.strip().lower()))


def _dedupe_sorted(values: list[str]) -> list[str]:
    return sorted(set(v.strip() for v in values if v.strip()))


def normalize(inputs: LegacyInputs) -> tuple[NormalizedData, ValidationResult]:
    result = ValidationResult()

    raw_cidrs = read_list_file(inputs.ipset_path)
    raw_excludes = read_list_file(inputs.exclude_path)
    raw_exclude_domains = [d.lower() for d in read_list_file(inputs.exclude_domains_path)]

    valid_cidrs = [c for c in raw_cidrs if is_valid_cidr(c)]
    invalid_cidrs = [c for c in raw_cidrs if not is_valid_cidr(c)]
    if invalid_cidrs:
        result.errors.append(f"Invalid CIDRs in ipset input: {len(invalid_cidrs)}")

    valid_excludes = [e for e in raw_excludes if is_valid_cidr(e)]
    invalid_excludes = [e for e in raw_excludes if not is_valid_cidr(e)]
    if invalid_excludes:
        result.warnings.append(f"Non-CIDR entries in exclude input skipped: {len(invalid_excludes)}")

    valid_domains = [d for d in raw_exclude_domains if is_valid_domain(d)]
    invalid_domains = [d for d in raw_exclude_domains if not is_valid_domain(d)]
    if invalid_domains:
        result.warnings.append(f"Invalid domains skipped: {len(invalid_domains)}")

    deduped_excludes = _dedupe_sorted(valid_excludes)
    filtered_cidrs = [c for c in valid_cidrs if c not in set(deduped_excludes)]

    data = NormalizedData(
        cidrs=_dedupe_sorted(filtered_cidrs),
        excludes=deduped_excludes,
        exclude_domains=_dedupe_sorted(valid_domains),
    )
    return data, result
