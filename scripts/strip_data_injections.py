#!/usr/bin/env python3
"""Copy a zarf package dir with dataInjections stripped (MODEL_DATA=false dev builds).

Usage: strip_data_injections.py <src-package-dir> <dst-dir>

The destination excludes the (potentially multi-GB) .model/ weights directory
and any dataInjections blocks from zarf.yaml, so `zarf package create` produces
a small, fast package for dev loops. Air-gapped release builds must keep
MODEL_DATA=true (the default).
"""

import shutil
import sys
from pathlib import Path

import yaml

EXCLUDES = {".model", "build", "__pycache__", ".venv", "zarf-sbom"}


def main() -> int:
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    def ignore(dirpath, names):
        return [n for n in names if n in EXCLUDES or n.endswith(".tar.zst")]

    shutil.copytree(src, dst, ignore=ignore)

    zarf_yaml = dst / "zarf.yaml"
    with open(zarf_yaml) as f:
        config = yaml.safe_load(f)

    stripped = 0
    for component in config.get("components", []):
        if "dataInjections" in component:
            del component["dataInjections"]
            stripped += 1

    with open(zarf_yaml, "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

    print(f"{src} -> {dst}: stripped dataInjections from {stripped} component(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
