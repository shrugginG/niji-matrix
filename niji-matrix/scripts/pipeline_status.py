#!/usr/bin/env python3
"""Report tactic-level Niji Matrix development progress."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from library_common import ROOT, load_objects


def load_plans(root: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for path in sorted((root / "planning" / "tactics").glob("*.yaml")):
        with path.open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
        if isinstance(value, dict):
            values.append(value)
    return values


def build_status(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    objects, _ = load_objects(root)
    matrix = objects["niji-matrix"]
    plans = {
        value["tactic_ref"]: value
        for value in load_plans(root)
        if isinstance(value.get("tactic_ref"), str)
    }
    tactics: list[dict[str, Any]] = []
    for tactic_id in matrix.get("tactic_refs", []):
        tactic = objects.get(tactic_id, {})
        techniques = [
            value
            for value in objects.values()
            if value.get("type") == "technique"
            and tactic_id in value.get("classification", {}).get("tactic_refs", [])
        ]
        decisions = [
            value
            for value in objects.values()
            if value.get("type") == "technique-decision"
            and value.get("tactic_ref") == tactic_id
        ]
        plan = plans.get(tactic_id)
        stages = Counter(
            item.get("stage", "unknown")
            for item in (plan or {}).get("work_items", [])
        )
        tactics.append(
            {
                "id": tactic_id,
                "name_zh": tactic.get("name_zh"),
                "name_en": tactic.get("name_en"),
                "plan_status": (plan or {}).get("status", "not-planned"),
                "inventory_status": (plan or {})
                .get("candidate_inventory", {})
                .get("status", "not-started"),
                "planned_candidates": len((plan or {}).get("work_items", [])),
                "stages": dict(sorted(stages.items())),
                "decisions": len(decisions),
                "techniques": len(techniques),
                "subtechniques": sum(
                    len(item.get("subtechnique_taxonomy", {}).get("subtechnique_refs", []))
                    for item in techniques
                ),
                "gap_analysis": (plan or {})
                .get("gap_analysis", {})
                .get("status", "not-started"),
            }
        )
    return {
        "attack_baseline": matrix.get("attack_baseline"),
        "tactics": tactics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    status = build_status(args.root)
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0
    print(
        f"ATT&CK baseline: {status['attack_baseline'].get('domain')} "
        f"{status['attack_baseline'].get('version')}"
    )
    print(
        "TACTIC   PLAN         INVENTORY    ITEMS DECISIONS TECHNIQUES "
        "SUBTECH GAP"
    )
    for item in status["tactics"]:
        print(
            f"{item['id']:<8} {item['plan_status']:<12} "
            f"{item['inventory_status']:<12} {item['planned_candidates']:>5} "
            f"{item['decisions']:>9} {item['techniques']:>10} "
            f"{item['subtechniques']:>7} {item['gap_analysis']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
