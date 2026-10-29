#!/usr/bin/env python3
"""Audit all reader prose for planning and defense-implementation leakage."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
TACTICS = ROOT / "matrix" / "tactics"

PLANNING_PATTERNS = [
    re.compile(r"固定\s*ATT&CK.*(?:子项|子技术|覆盖|广度)"),
    re.compile(r"fixed\s+ATT&CK.*(?:child|coverage|breadth)", re.I),
    re.compile(r"第二轮.*taxonomy", re.I),
    re.compile(r"second.*taxonomy.*pass", re.I),
    re.compile(r"正式数量|formal count", re.I),
    re.compile(r"数量.{0,16}(?:不能|不得|不应).{0,12}(?:增加|减少)"),
    re.compile(r"count.{0,16}(?:cannot|should not).{0,12}(?:increase|decrease)", re.I),
    re.compile(r"\b(?:parent-core|niji-variable-candidate|not-stealth-distinct|evidence-deferred)\b", re.I),
]
STATE_PATTERN = re.compile(
    r"\b(?:identity_anomaly|accepted_identity_use|privileged_session|same_authority_use|"
    r"authority_unresolved|elevation_confirmed|execution_confirmed_non_elevating|"
    r"injection_attempt|payload_staged|dispatch_observed|injection_confirmed|"
    r"injection_confirmed_non_elevating|coverage_degraded|boundary_risk|escape_attempt|"
    r"broker_request_only|provenance_gap|brokered_escape_confirmed|no_authority_gain|"
    r"policy_state_anomaly|consumer_adoption|post_use_reversion|"
    r"restored_state_with_residual_authority|telemetry_integrity_at_risk)\b",
    re.I,
)
OBJECT_REF_PATTERN = re.compile(r"\b(?:DET|NJA|MIT)-[0-9]{6}\b")
PROCEDURAL_PATTERNS = [
    re.compile(r"分析应输出|输出必须分级|关联先分"),
    re.compile(r"analytics? should emit|outputs? (?:must|should) be tiered", re.I),
]
CHILD_TACTIC_PATTERN = re.compile(r"\bTA[0-9]{4}\b")


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def prose_blocks(value: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    yield "definition_and_concept", value["definition_and_concept"]
    yield "stealth_characteristics", value["stealth_characteristics"]
    yield "scope_boundary_definition", value["scope_boundary_definition"]
    scenarios = value["application_scenarios_and_threat_model"]
    yield "application_scenarios", scenarios["application_scenarios"]
    yield "attacker_model", scenarios["threat_model"]["attacker_model"]
    yield "defender_model", scenarios["threat_model"]["defender_model"]
    for index, mechanism in enumerate(value.get("stealth_mechanisms", []), 1):
        yield f"stealth_mechanisms[{index}].analysis", mechanism["analysis"]
    if value.get("type") == "technique":
        yield "subtechnique_taxonomy.narrative", value["subtechnique_taxonomy"]["narrative"]
    yield "research.limitations", value["research"]["limitations"]


def main() -> int:
    parent_paths = list(TACTICS.glob("*/techniques/*/technique.yaml"))

    errors: list[str] = []
    for parent_path in sorted(parent_paths):
        paths = [parent_path, *sorted(parent_path.parent.glob("subtechniques/*/subtechnique.yaml"))]
        for path in paths:
            value = load_yaml(path)
            object_id = value.get("id", path.name)
            for field, block in prose_blocks(value):
                for index, paragraph in enumerate(block.get("paragraphs", []), 1):
                    text = f"{paragraph.get('zh', '')} {paragraph.get('en', '')}"
                    for pattern in PLANNING_PATTERNS:
                        if pattern.search(text):
                            errors.append(f"{path.relative_to(ROOT)}:{object_id}:{field}[{index}]: planning language: {pattern.pattern}")
                    if STATE_PATTERN.search(text):
                        errors.append(f"{path.relative_to(ROOT)}:{object_id}:{field}[{index}]: Analytic output state in reader prose")
                    if OBJECT_REF_PATTERN.search(text):
                        errors.append(f"{path.relative_to(ROOT)}:{object_id}:{field}[{index}]: defense-object ID in reader prose")
                    for pattern in PROCEDURAL_PATTERNS:
                        if pattern.search(text):
                            errors.append(f"{path.relative_to(ROOT)}:{object_id}:{field}[{index}]: procedural detection language")
                    if value.get("type") == "evasion-subtechnique" and CHILD_TACTIC_PATTERN.search(text):
                        errors.append(f"{path.relative_to(ROOT)}:{object_id}:{field}[{index}]: child repeats parent tactic gate")

    if errors:
        print(f"Reader-prose audit failed: {len(errors)} issue(s).")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Reader-prose audit passed: {len(parent_paths)} parents checked with their children.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
