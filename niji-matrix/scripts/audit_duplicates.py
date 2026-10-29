#!/usr/bin/env python3
"""Find exact and likely semantic duplicates in global Niji libraries."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
from typing import Any

import yaml

from library_common import ROOT, build_catalog, flat_entries, normalize_text


def reviewed_pairs(root: Path) -> set[tuple[str, str]]:
    path = root / "planning" / "duplicate-resolutions.yaml"
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        return set()
    return {
        tuple(sorted(item.get("ids", [])))
        for item in value.get("resolutions", [])
        if isinstance(item, dict) and len(item.get("ids", [])) == 2
    }


def audit(
    root: Path = ROOT,
    threshold: float = 0.92,
) -> dict[str, list[dict[str, Any]]]:
    entries = flat_entries(build_catalog(root.resolve()))
    exact: list[dict[str, Any]] = []
    possible: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str]] = set()

    strong_keys: dict[str, list[str]] = defaultdict(list)
    semantic_keys: dict[str, list[str]] = defaultdict(list)
    bibliographic_keys: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        for key in entry.get("identity_keys", []):
            if key.startswith(("doi:", "url:", "identifier:")):
                strong_keys[f"{entry['type']}:{key}"].append(entry["id"])
            elif key.startswith("bibliographic:"):
                bibliographic_keys[f"{entry['type']}:{key}"].append(entry["id"])
            elif key.startswith("semantic:"):
                semantic_keys[f"{entry['type']}:{key}"].append(entry["id"])

    for reason, groups in (
        ("stable-identity", strong_keys),
        ("semantic-fingerprint", semantic_keys),
    ):
        for key, ids in groups.items():
            unique_ids = sorted(set(ids))
            if len(unique_ids) > 1:
                exact.append({"reason": reason, "key": key, "ids": unique_ids})
                seen_pairs.update(combinations(unique_ids, 2))

    for key, ids in bibliographic_keys.items():
        unique_ids = sorted(set(ids))
        if len(unique_ids) > 1:
            possible.append(
                {"reason": "bibliographic-identity", "key": key, "ids": unique_ids}
            )
            seen_pairs.update(combinations(unique_ids, 2))

    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        entry["_audit_label"] = normalize_text(
            entry.get("label_en") or entry.get("label_zh")
        )
        by_type[entry["type"]].append(entry)
    for object_type, values in by_type.items():
        # SequenceMatcher is quadratic in the number of library objects and can
        # become the dominant quality-gate cost. Sort by normalized-label length
        # and use mathematically safe upper bounds before computing its full
        # ratio. A pair whose length-only or quick ratio is below the threshold
        # cannot reach the threshold in SequenceMatcher.ratio(), so findings are
        # unchanged while dissimilar pairs are discarded cheaply.
        values.sort(key=lambda item: len(item["_audit_label"]))
        for left_index, left in enumerate(values):
            left_name = left["_audit_label"]
            if not left_name:
                continue
            left_length = len(left_name)
            maximum_right_length = left_length * (2.0 - threshold) / threshold
            for right in values[left_index + 1 :]:
                right_name = right["_audit_label"]
                if len(right_name) > maximum_right_length:
                    break
                if not right_name:
                    continue
                pair = tuple(sorted((left["id"], right["id"])))
                if pair in seen_pairs:
                    continue
                matcher = SequenceMatcher(None, left_name, right_name)
                if matcher.real_quick_ratio() < threshold:
                    continue
                if matcher.quick_ratio() < threshold:
                    continue
                score = matcher.ratio()
                if score >= threshold:
                    possible.append(
                        {
                            "reason": "similar-label",
                            "type": object_type,
                            "ids": list(pair),
                            "score": round(score, 4),
                        }
                    )
    accepted_pairs = reviewed_pairs(root.resolve())
    resolved = [
        finding
        for finding in possible
        if tuple(sorted(finding["ids"])) in accepted_pairs
    ]
    possible = [
        finding
        for finding in possible
        if tuple(sorted(finding["ids"])) not in accepted_pairs
    ]
    return {"exact": exact, "possible": possible, "resolved": resolved}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--threshold", type=float, default=0.92)
    parser.add_argument(
        "--fail-on",
        choices=("none", "exact", "possible"),
        default="none",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = audit(args.root, args.threshold)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            f"共享库重复审计：{len(result['exact'])} 组精确重复，"
            f"{len(result['possible'])} 组待审可能重复，"
            f"{len(result['resolved'])} 组已审查相似项。"
        )
        for finding in result["exact"]:
            print(
                f"ERROR: {finding['reason']}: "
                f"{', '.join(finding['ids'])} ({finding['key']})"
            )
        for finding in result["possible"]:
            score = (
                f", score={finding['score']}"
                if "score" in finding
                else ""
            )
            print(
                f"REVIEW: {finding['reason']}: "
                f"{', '.join(finding['ids'])}{score}"
            )

    if args.fail_on == "exact" and result["exact"]:
        return 1
    if args.fail_on == "possible" and (
        result["exact"] or result["possible"]
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
