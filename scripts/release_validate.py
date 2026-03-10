from __future__ import annotations

import argparse
import re

SEMVER_TAG_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate release tag format")
    parser.add_argument("tag", help="Git tag expected in vMAJOR.MINOR.PATCH format")
    args = parser.parse_args()

    if not SEMVER_TAG_RE.fullmatch(args.tag):
        print(f"Invalid release tag: {args.tag}")
        print("Expected semver-like tag, e.g. v1.2.3 or v1.2.3-rc.1")
        return 1
    print(f"Release tag is valid: {args.tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
