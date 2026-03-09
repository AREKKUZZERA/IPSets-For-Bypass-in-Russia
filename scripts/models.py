from dataclasses import dataclass, field


@dataclass
class LegacyInputs:
    ipset_path: str
    exclude_path: str
    exclude_domains_path: str


@dataclass
class NormalizedData:
    cidrs: list[str] = field(default_factory=list)
    excludes: list[str] = field(default_factory=list)
    exclude_domains: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors
