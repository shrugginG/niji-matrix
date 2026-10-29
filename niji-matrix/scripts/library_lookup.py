#!/usr/bin/env python3
"""Search existing global-library objects before proposing a new one."""

from __future__ import annotations

import argparse
import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from library_common import (
    LIBRARY_TYPES,
    ROOT,
    build_catalog,
    canonicalize_url,
    extract_doi,
    flat_entries,
    normalize_text,
)


def score_entry(
    entry: dict[str, Any],
    text: str | None,
    doi: str | None,
    url: str | None,
) -> float:
    if doi:
        return 1.0 if entry.get("doi") == doi else 0.0
    if url:
        return 1.0 if entry.get("canonical_url") == url else 0.0
    query = normalize_text(text)
    if not query:
        return 0.5
    if normalize_text(entry.get("id")) == query:
        return 1.0
    fields = [
        entry.get("id"),
        entry.get("label_zh"),
        entry.get("label_en"),
        entry.get("summary_zh"),
        entry.get("summary_en"),
        entry.get("canonical_url"),
        entry.get("doi"),
    ]
    values = [normalize_text(field) for field in fields if field]
    if any(query == value for value in values):
        return 1.0
    if any(query in value for value in values):
        return 0.95
    return max(
        (SequenceMatcher(None, query, value).ratio() for value in values),
        default=0.0,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--type", choices=LIBRARY_TYPES)
    parser.add_argument("--text")
    parser.add_argument("--doi")
    parser.add_argument("--url")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    doi = extract_doi(args.doi)
    url = canonicalize_url(args.url)
    entries = flat_entries(build_catalog(args.root.resolve()))
    if args.type:
        entries = [entry for entry in entries if entry["type"] == args.type]
    ranked = [
        (score_entry(entry, args.text, doi, url), entry)
        for entry in entries
    ]
    ranked = [
        (score, entry)
        for score, entry in sorted(
            ranked,
            key=lambda item: (-item[0], item[1]["id"]),
        )
        if score >= (0.0 if not (args.text or doi or url) else 0.35)
    ][: max(1, args.limit)]

    if args.json:
        print(
            json.dumps(
                [{"score": round(score, 4), **entry} for score, entry in ranked],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not ranked:
        print("未找到匹配的共享库对象。")
        return 1
    for score, entry in ranked:
        print(
            f"{score:0.3f}  {entry['id']:<12} {entry['type']:<13} "
            f"{entry['label_zh']} / {entry['label_en']}"
        )
        print(f"       {entry['path']}")
        if entry.get("identity_keys"):
            print(f"       keys: {', '.join(entry['identity_keys'])}")
        if entry.get("used_by"):
            print(f"       used-by: {', '.join(entry['used_by'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
