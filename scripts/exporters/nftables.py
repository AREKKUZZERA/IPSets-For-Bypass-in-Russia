from __future__ import annotations

from pathlib import Path

from . import ExportArtifact, ExportContext, split_cidrs


def _write_nft_set(path: Path, family: str, values: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    type_name = "ipv4_addr" if family == "ip" else "ipv6_addr"
    content = [f"set bypass_{family} {{", f"  type {type_name}", "  flags interval", "  elements = {"]
    content.extend(f"    {value}," for value in values)
    content.append("  }")
    content.append("}")
    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def export(context: ExportContext) -> list[ExportArtifact]:
    ipv4, ipv6 = split_cidrs(context.data.cidrs)
    base = context.dist_dir / "nftables"

    _write_nft_set(base / "ipv4.nft", "ip", ipv4)
    _write_nft_set(base / "ipv6.nft", "ip6", ipv6)

    include = '\n'.join(["include \"ipv4.nft\"", "include \"ipv6.nft\""]) + "\n"
    (base / "include.nft").write_text(include, encoding="utf-8")

    return [
        ExportArtifact(path="nftables/ipv4.nft", format="nftables", kind="ipv4-set", count=len(ipv4)),
        ExportArtifact(path="nftables/ipv6.nft", format="nftables", kind="ipv6-set", count=len(ipv6)),
        ExportArtifact(path="nftables/include.nft", format="nftables", kind="include", count=2),
    ]
