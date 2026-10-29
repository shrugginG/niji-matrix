#!/usr/bin/env python3
"""Build a searchable catalog of Niji Matrix global-library objects."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from library_common import ROOT, build_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Niji Matrix root")
    parser.add_argument(
        "--output",
        type=Path,
        help="Catalog path; defaults to dist/catalogs/library-catalog.json",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the complete catalog instead of writing it",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    catalog = build_catalog(root)
    catalog["generated_at"] = datetime.now(timezone.utc).isoformat()
    serialized = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    if args.stdout:
        print(serialized, end="")
        return 0

    output = args.output or root / "dist" / "catalogs" / "library-catalog.json"
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(serialized, encoding="utf-8")
    print(
        f"{output.relative_to(root)}: "
        + ", ".join(f"{key}={count}" for key, count in catalog["counts"].items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
