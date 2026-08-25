#!/usr/bin/env python3
"""Bump the version everywhere it lives.

package.json is canonical; extension.toml is synced from it. Refuses to run
if CHANGELOG.md has no entry for the new version.

Usage:
  just release 1.4.0
"""

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        sys.exit("usage: python3 tools/bump.py <major.minor.patch>")
    version = sys.argv[1]

    if f"## {version}" not in (BASE / "CHANGELOG.md").read_text():
        sys.exit(f"CHANGELOG.md has no '## {version}' entry; write it first")

    pkg_path = BASE / "package.json"
    pkg = json.loads(pkg_path.read_text())
    old = pkg["version"]
    pkg["version"] = version
    pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")

    ext_path = BASE / "extension.toml"
    ext_path.write_text(
        re.sub(r'^version = ".*"', f'version = "{version}"',
               ext_path.read_text(), count=1, flags=re.M)
    )
    print(f"{old} -> {version} (package.json, extension.toml)")


if __name__ == "__main__":
    main()
