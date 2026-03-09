from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Action = Literal["proxy", "direct", "exclude", "neutral"]
InputMode = Literal["legacy", "hybrid", "sources"]


@dataclass
class LegacyInputs:
    ipset_path: str
    exclude_path: str
    exclude_domains_path: str


@dataclass
class SourceRecord:
    type: Literal["cidr", "domain"]
    value: str
    service: str = "unknown"
    category: str = "uncategorized"
    source: str = "legacy"
    source_url: str = ""
    comment: str = ""
    tags: list[str] = field(default_factory=list)
    action: Action = "proxy"
    platforms: list[str] = field(default_factory=list)
    priority: int = 100
    needs_review: bool = False
    confidence: float = 0.5
    updated_at: str = ""


@dataclass
class NormalizedData:
    cidrs: list[str] = field(default_factory=list)
    excludes: list[str] = field(default_factory=list)
    exclude_domains: list[str] = field(default_factory=list)
    needs_review: list[dict] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors
