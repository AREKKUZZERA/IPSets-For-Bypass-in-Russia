from __future__ import annotations

from dataclasses import dataclass

from scripts.models import NormalizedData


@dataclass(frozen=True)
class ExportProfile:
    name: str
    include_domains: bool = True
    include_ip: bool = True
    lite_limit: int | None = None


PROFILES: dict[str, ExportProfile] = {
    "full": ExportProfile(name="full"),
    "lite": ExportProfile(name="lite", lite_limit=256),
    "domains-only": ExportProfile(name="domains-only", include_ip=False),
    "ip-only": ExportProfile(name="ip-only", include_domains=False),
}


def apply_profile(data: NormalizedData, profile: str) -> NormalizedData:
    selected = PROFILES[profile]

    cidrs = list(data.cidrs) if selected.include_ip else []
    excludes = list(data.excludes) if selected.include_ip else []
    exclude_domains = list(data.exclude_domains) if selected.include_domains else []

    if selected.lite_limit is not None:
        cidrs = cidrs[: selected.lite_limit]
        excludes = excludes[: selected.lite_limit]
        exclude_domains = exclude_domains[: selected.lite_limit]

    return NormalizedData(
        cidrs=cidrs,
        excludes=excludes,
        exclude_domains=exclude_domains,
        needs_review=list(data.needs_review),
        stats=dict(data.stats),
    )
