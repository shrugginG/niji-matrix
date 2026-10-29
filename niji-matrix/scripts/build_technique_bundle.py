#!/usr/bin/env python3
"""Build one fully expanded YAML-only Niji technique JSON bundle."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOTS = (
    ROOT / "matrix.yaml",
    ROOT / "matrix",
    ROOT / "mechanisms",
    ROOT / "references",
    ROOT / "claims",
    ROOT / "cases",
    ROOT / "detections",
    ROOT / "analytics",
    ROOT / "mitigations",
    ROOT / "relationships",
)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: top level must be an object")
    return value


def iter_yaml_files() -> Iterable[Path]:
    for root in CONTENT_ROOTS:
        if root.is_file():
            yield root
        elif root.exists():
            yield from sorted(root.rglob("*.yaml"))


def load_index() -> dict[str, dict[str, Any]]:
    objects: dict[str, dict[str, Any]] = {}
    for path in iter_yaml_files():
        value = load_yaml(path)
        object_id = value.get("id")
        if not isinstance(object_id, str):
            continue
        if object_id in objects:
            raise ValueError(f"duplicate object id: {object_id}")
        objects[object_id] = value
    return objects


def require_object(
    objects: dict[str, dict[str, Any]],
    object_id: str,
    expected_type: str | None = None,
) -> dict[str, Any]:
    try:
        value = objects[object_id]
    except KeyError as exc:
        raise ValueError(f"unresolved object reference: {object_id}") from exc
    if expected_type and value.get("type") != expected_type:
        raise ValueError(
            f"{object_id}: expected type {expected_type}, got {value.get('type')}"
        )
    return value


def collect_key_refs(value: Any, key: str) -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key == key:
                if isinstance(child, str):
                    result.add(child)
                elif isinstance(child, list):
                    result.update(item for item in child if isinstance(item, str))
            result.update(collect_key_refs(child, key))
    elif isinstance(value, list):
        for child in value:
            result.update(collect_key_refs(child, key))
    return result


def collect_reference_ids(value: Any) -> set[str]:
    result: set[str] = set()
    for key in ("evidence_refs", "reference_refs", "external_reference_refs"):
        result.update(
            item for item in collect_key_refs(value, key) if item.startswith("REF-")
        )
    return result


def sort_objects(values: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(values, key=lambda value: str(value.get("id", "")))


def build_bundle(technique_id: str) -> dict[str, Any]:
    objects = load_index()
    matrix = require_object(objects, "niji-matrix", "matrix")
    technique = require_object(objects, technique_id, "technique")
    if technique.get("schema_version") != "2.0.0":
        raise ValueError(f"{technique_id}: only YAML-only schema 2.0.0 is buildable")

    classification = technique.get("classification", {})
    tactic_ids = set(classification.get("tactic_refs", []))
    tactics = [require_object(objects, ref, "tactic") for ref in tactic_ids]

    decision_ref = classification.get("decision_ref")
    decision = (
        require_object(objects, decision_ref, "technique-decision")
        if isinstance(decision_ref, str)
        else None
    )

    subtechnique_ids = set(
        technique.get("subtechnique_taxonomy", {}).get("subtechnique_refs", [])
    )
    subtechniques = [
        require_object(objects, ref, "evasion-subtechnique")
        for ref in subtechnique_ids
    ]
    for child in subtechniques:
        if child.get("schema_version") != "2.0.0":
            raise ValueError(f"{child.get('id')}: child must use schema 2.0.0")

    core_values = [technique, *subtechniques]
    mechanism_ids = set()
    for value in core_values:
        mechanism_ids.update(collect_key_refs(value, "mechanism_ref"))
    mechanisms = [require_object(objects, ref, "mechanism") for ref in mechanism_ids]

    claim_ids = set()
    case_ids = set()
    detection_ids = set()
    mitigation_ids = set()
    for value in core_values:
        claim_ids.update(collect_key_refs(value, "claim_refs"))
        case_ids.update(collect_key_refs(value, "case_refs"))
        detection_ids.update(collect_key_refs(value, "strategy_refs"))
        mitigation_ids.update(collect_key_refs(value, "mitigation_refs"))

    claims = [require_object(objects, ref, "claim") for ref in claim_ids]
    cases = [require_object(objects, ref, "case") for ref in case_ids]
    detections = [require_object(objects, ref, "detection-strategy") for ref in detection_ids]
    mitigations = [require_object(objects, ref, "mitigation") for ref in mitigation_ids]
    analytic_ids: set[str] = set()
    for detection in detections:
        analytic_ids.update(collect_key_refs(detection, "analytic_refs"))
    analytics = [
        require_object(objects, ref, "detection-analytic")
        for ref in analytic_ids
    ]

    related_ids = {
        technique_id,
        *tactic_ids,
        *subtechnique_ids,
        *mechanism_ids,
        *claim_ids,
        *case_ids,
        *detection_ids,
        *mitigation_ids,
    }
    relationships = [
        value
        for value in objects.values()
        if value.get("type") == "relationship"
        and (
            value.get("source_ref") in related_ids
            or value.get("target_ref") in related_ids
        )
    ]

    evidence_sources: list[dict[str, Any]] = [
        technique,
        *subtechniques,
        *claims,
        *cases,
        *detections,
        *analytics,
        *mitigations,
        *relationships,
    ]
    if decision:
        evidence_sources.append(decision)
    reference_ids: set[str] = set()
    for value in evidence_sources:
        reference_ids.update(collect_reference_ids(value))
    references = [require_object(objects, ref, "reference") for ref in reference_ids]

    bundle = {
        "bundle_schema_version": "2.0.0",
        "type": "technique-bundle",
        "id": technique_id,
        "matrix": copy.deepcopy(matrix),
        "tactics": sort_objects(copy.deepcopy(tactics)),
        "admission_decision": copy.deepcopy(decision),
        "technique": copy.deepcopy(technique),
        "mechanisms": sort_objects(copy.deepcopy(mechanisms)),
        "subtechniques": sort_objects(copy.deepcopy(subtechniques)),
        "claims": sort_objects(copy.deepcopy(claims)),
        "cases": sort_objects(copy.deepcopy(cases)),
        "detection_strategies": sort_objects(copy.deepcopy(detections)),
        "detection_analytics": sort_objects(copy.deepcopy(analytics)),
        "mitigations": sort_objects(copy.deepcopy(mitigations)),
        "relationships": sort_objects(copy.deepcopy(relationships)),
        "references": sort_objects(copy.deepcopy(references)),
    }
    bundle["object_counts"] = {
        "tactics": len(bundle["tactics"]),
        "mechanisms": len(bundle["mechanisms"]),
        "subtechniques": len(bundle["subtechniques"]),
        "claims": len(bundle["claims"]),
        "cases": len(bundle["cases"]),
        "detection_strategies": len(bundle["detection_strategies"]),
        "detection_analytics": len(bundle["detection_analytics"]),
        "mitigations": len(bundle["mitigations"]),
        "relationships": len(bundle["relationships"]),
        "references": len(bundle["references"]),
    }
    return bundle


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("technique_id", help="Niji technique ID, for example NJT-0001")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON path; defaults to dist/techniques/<ID>.json",
    )
    args = parser.parse_args()

    output = args.output or ROOT / "dist" / "techniques" / f"{args.technique_id}.json"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        bundle = build_bundle(args.technique_id)
    except ValueError as exc:
        parser.error(str(exc))

    output.write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
