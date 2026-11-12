"""Build clickable_tags_updated.ankiaddon from this folder.

Usage:  python build_ankiaddon.py [output_path]

Uses forward-slash paths inside the zip so the package installs on macOS and
Linux too (Windows' Compress-Archive writes backslashes, which break there).
"""

import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = ["__init__.py", "manifest.json", "LICENSE", "web/clickable_tags_updated.js"]


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "clickable_tags_updated.ankiaddon"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in FILES:
            zf.write(HERE / name, name)
    print(f"Built {out}")
    for name in zipfile.ZipFile(out).namelist():
        print(f"  {name}")


if __name__ == "__main__":
    main()
