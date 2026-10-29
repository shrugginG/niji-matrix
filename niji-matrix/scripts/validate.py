#!/usr/bin/env python3
"""Validate Niji Matrix YAML structure and cross-object references."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"

SCHEMA_FOR_TYPE = {
    "matrix": "matrix.schema.json",
    "tactic": "tactic.schema.json",
    "technique-decision": "technique-decision.schema.json",
    "technique": "technique.schema.json",
    "evasion-subtechnique": "subtechnique.schema.json",
    "mechanism": "mechanism.schema.json",
    "reference": "reference.schema.json",
    "claim": "claim.schema.json",
    "case": "case.schema.json",
    "detection-strategy": "detection.schema.json",
    "detection-analytic": "analytic.schema.json",
    "mitigation": "mitigation.schema.json",
    "relationship": "relationship.schema.json",
}

REFERENCE_KEYS = {
    "tactic_ref",
    "tactic_refs",
    "mechanism_ref",
    "mechanism_refs",
    "decision_ref",
    "resulting_technique_ref",
    "parent_ref",
    "subtechnique_refs",
    "claim_refs",
    "case_refs",
    "strategy_ref",
    "strategy_refs",
    "analytic_refs",
    "mitigation_refs",
    "external_reference_refs",
    "reference_refs",
    "evidence_refs",
    "affected_claim_refs",
    "affected_case_refs",
    "subject_refs",
    "detects_refs",
    "source_ref",
    "target_ref",
}


FORBIDDEN_MARKDOWN = re.compile(
    r"(?m)^\s{0,3}(?:#{1,6}\s|(?:```|~~~)|[-*+]\s+|\d+[.)]\s+|\|.*\|\s*$)|"
    r"\[[^\]]+\]\(https?://|<[/A-Za-z][^>]*>"
)


def walk_strings(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_strings(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_strings(child, (*path, str(index)))
    elif isinstance(value, str):
        yield ".".join(path), value


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_schema(name: str) -> dict[str, Any]:
    with (SCHEMA_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def iter_content_files() -> list[Path]:
    roots = [
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
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(
                path
                for path in root.rglob("*.yaml")
                if not path.name.startswith("_")
            )
    return sorted(files)


def walk_references(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = (*path, key)
            if key in REFERENCE_KEYS:
                if isinstance(child, str):
                    yield child, ".".join(child_path)
                elif isinstance(child, list):
                    for index, ref in enumerate(child):
                        if isinstance(ref, str):
                            yield ref, f"{'.'.join(child_path)}[{index}]"
            yield from walk_references(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_references(child, (*path, str(index)))


def containing_tactic_id(path: Path) -> str | None:
    for part in path.parts:
        if part.startswith("TA") and "-" in part:
            candidate = part.split("-", 1)[0]
            if len(candidate) == 6:
                return candidate
    return None


def containing_technique_id(path: Path) -> str | None:
    for part in path.parts:
        if part.startswith("NJT-") and len(part) >= 8:
            return "-".join(part.split("-")[:2])
    return None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    objects: list[tuple[Path, dict[str, Any]]] = []
    ids: dict[str, Path] = {}
    by_type: dict[str, list[tuple[Path, dict[str, Any]]]] = defaultdict(list)

    for path in iter_content_files():
        relative = path.relative_to(ROOT)
        try:
            value = load_yaml(path)
        except Exception as exc:
            errors.append(f"{relative}: YAML 解析失败：{exc}")
            continue

        if not isinstance(value, dict):
            errors.append(f"{relative}: 顶层必须是对象")
            continue

        object_type = value.get("type")
        schema_name = SCHEMA_FOR_TYPE.get(object_type)
        if not schema_name:
            errors.append(f"{relative}: 未知或缺失的 type：{object_type!r}")
            continue

        validator = Draft202012Validator(
            load_schema(schema_name),
            format_checker=FormatChecker(),
        )
        for issue in sorted(validator.iter_errors(value), key=lambda error: list(error.path)):
            location = ".".join(str(item) for item in issue.path) or "<root>"
            errors.append(f"{relative}:{location}: {issue.message}")

        object_id = value.get("id")
        if isinstance(object_id, str):
            if object_id in ids:
                errors.append(
                    f"{relative}: ID {object_id} 与 {ids[object_id].relative_to(ROOT)} 重复"
                )
            else:
                ids[object_id] = path

        objects.append((path, value))
        by_type[object_type].append((path, value))

    for path, value in objects:
        relative = path.relative_to(ROOT)
        for reference, location in walk_references(value):
            if reference not in ids:
                errors.append(f"{relative}:{location}: 无法解析引用 {reference}")

        object_type = value.get("type")
        tactic_in_path = containing_tactic_id(path)

        if object_type in {
            "technique",
            "evasion-subtechnique",
            "detection-strategy",
            "detection-analytic",
            "mitigation",
        }:
            for location, content in walk_strings(value):
                if "__REQUIRED__" in content:
                    errors.append(f"{relative}:{location}: 不得残留模板占位符")
                if FORBIDDEN_MARKDOWN.search(content):
                    errors.append(
                        f"{relative}:{location}: YAML-only 内容不得嵌入 Markdown 或 HTML"
                    )

        if object_type == "technique-decision" and tactic_in_path:
            if value.get("tactic_ref") != tactic_in_path:
                errors.append(
                    f"{relative}: tactic_ref 与所在战术目录 {tactic_in_path} 不一致"
                )
            if value.get("original_attack_subtechniques_imported") is not False:
                errors.append(f"{relative}: 禁止导入 ATT&CK 原子技术")

        if object_type == "technique" and tactic_in_path:
            classification = value.get("classification", {})
            if tactic_in_path not in classification.get("tactic_refs", []):
                errors.append(
                    f"{relative}: classification.tactic_refs "
                    f"未包含所在战术目录 {tactic_in_path}"
                )
            mappings = value.get("stealth_mechanisms", [])
            mapped_refs = [
                item.get("mechanism_ref")
                for item in mappings
                if isinstance(item, dict)
            ]
            if len(mapped_refs) != len(set(mapped_refs)):
                errors.append(f"{relative}: 匿迹机理映射不得重复")

        if object_type == "evasion-subtechnique":
            mapped_refs = [
                item.get("mechanism_ref")
                for item in value.get("stealth_mechanisms", [])
                if isinstance(item, dict)
            ]
            if len(mapped_refs) != len(set(mapped_refs)):
                errors.append(f"{relative}: 匿迹机理映射不得重复")

        if object_type == "evasion-subtechnique":
            technique_in_path = containing_technique_id(path)
            parent_ref = value.get("parent_ref")
            expected_prefix = (
                f"NJS-{parent_ref.removeprefix('NJT-')}-"
                if isinstance(parent_ref, str)
                else ""
            )
            if expected_prefix and not str(value.get("id", "")).startswith(expected_prefix):
                errors.append(
                    f"{relative}: 子技术 ID 的父级段与 parent_ref 不一致"
                )
            if technique_in_path and parent_ref != technique_in_path:
                errors.append(
                    f"{relative}: parent_ref 与所在技术目录 {technique_in_path} 不一致"
                )
            if value.get("lineage", {}).get("attck_subtechnique_inherited") is not False:
                errors.append(f"{relative}: 匿迹子技术不得继承 ATT&CK 子技术")

            characteristics = (
                value.get("stealth_characteristics", {})
                .get("paragraphs", [])
            )
            if characteristics:
                first = characteristics[0]
                name = value.get("name", {})
                if not str(first.get("zh", "")).startswith(str(name.get("zh", ""))):
                    errors.append(
                        f"{relative}: 匿迹特性中文首段必须以子技术名称开头"
                    )
                if not str(first.get("en", "")).startswith(str(name.get("en", ""))):
                    errors.append(
                        f"{relative}: 匿迹特性英文首段必须以子技术名称开头"
                    )

    subtechniques = {
        value["id"]: value
        for _, value in by_type["evasion-subtechnique"]
        if isinstance(value.get("id"), str)
    }
    techniques = {
        value["id"]: value
        for _, value in by_type["technique"]
        if isinstance(value.get("id"), str)
    }

    for technique_id, technique in techniques.items():
        for subtechnique_id in technique.get("subtechnique_taxonomy", {}).get("subtechnique_refs", []):
            child = subtechniques.get(subtechnique_id)
            if child and child.get("parent_ref") != technique_id:
                errors.append(
                    f"{technique_id}: 子技术 {subtechnique_id} 的 parent_ref 不一致"
                )

    for subtechnique_id, subtechnique in subtechniques.items():
        parent_id = subtechnique.get("parent_ref")
        parent = techniques.get(parent_id)
        if parent and subtechnique_id not in parent.get("subtechnique_taxonomy", {}).get("subtechnique_refs", []):
            errors.append(
                f"{subtechnique_id}: 父技术 {parent_id} 未反向列出该子技术"
            )

    object_index = {
        value["id"]: value
        for _, value in objects
        if isinstance(value.get("id"), str)
    }

    for path, strategy in by_type["detection-strategy"]:
        strategy_evidence = set(strategy.get("evidence_refs", []))
        for analytic_ref in strategy.get("analytic_refs", []):
            analytic = object_index.get(analytic_ref)
            if analytic and analytic.get("type") != "detection-analytic":
                errors.append(
                    f"{path.relative_to(ROOT)}: analytic_refs 必须指向 detection-analytic"
                )
            if analytic and analytic.get("strategy_ref") != strategy.get("id"):
                errors.append(
                    f"{path.relative_to(ROOT)}: {analytic_ref} 未反向指向该策略"
                )

            if analytic and not set(analytic.get("evidence_refs", [])).issubset(
                strategy_evidence
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}: Strategy 必须覆盖 Analytic 使用的证据"
                )

    for path, analytic in by_type["detection-analytic"]:
        strategy = object_index.get(analytic.get("strategy_ref"))
        if strategy and strategy.get("type") != "detection-strategy":
            errors.append(
                f"{path.relative_to(ROOT)}: strategy_ref 必须指向 detection-strategy"
            )
        if strategy and analytic.get("id") not in strategy.get("analytic_refs", []):
            errors.append(
                f"{path.relative_to(ROOT)}: 所属策略未反向列出该分析"
            )

    for path, mitigation in by_type["mitigation"]:
        targets = [
            item.get("target_ref")
            for item in mitigation.get("applications", [])
            if isinstance(item, dict)
        ]
        if len(targets) != len(set(targets)):
            errors.append(
                f"{path.relative_to(ROOT)}: mitigation applications 的 target_ref 不得重复"
            )

    for path, value in objects:
        if value.get("type") not in {"technique", "evasion-subtechnique"}:
            continue
        relative = path.relative_to(ROOT)
        subject_id = value.get("id")
        covered_subjects = {subject_id}
        if value.get("type") == "technique":
            covered_subjects.update(
                value.get("subtechnique_taxonomy", {}).get("subtechnique_refs", [])
            )

        subject_references = set(value.get("evidence", {}).get("reference_refs", []))
        for index, mapping in enumerate(value.get("stealth_mechanisms", [])):
            if not set(mapping.get("evidence_refs", [])).issubset(subject_references):
                errors.append(
                    f"{relative}: stealth_mechanisms[{index}] 的证据必须列入 "
                    "evidence.reference_refs"
                )

        defense = value.get("defense", {})
        for strategy_ref in defense.get("detections", {}).get("strategy_refs", []):
            target = object_index.get(strategy_ref)
            if target and target.get("type") != "detection-strategy":
                errors.append(
                    f"{relative}: strategy_refs 必须指向 detection-strategy"
                )
            if target and not covered_subjects.intersection(
                target.get("detects_refs", [])
            ):
                errors.append(
                    f"{relative}: {strategy_ref} 未声明检测该对象或其子技术"
                )
        for mitigation_ref in defense.get("mitigations", {}).get("mitigation_refs", []):
            target = object_index.get(mitigation_ref)
            if target and target.get("type") != "mitigation":
                errors.append(
                    f"{relative}: mitigation_refs 必须指向 mitigation"
                )
            application_targets = {
                item.get("target_ref")
                for item in (target or {}).get("applications", [])
                if isinstance(item, dict)
            }
            if target and not covered_subjects.intersection(application_targets):
                errors.append(
                    f"{relative}: {mitigation_ref} 未包含该对象或其子技术的应用"
                )

    decisions = {
        value["id"]: value
        for _, value in by_type["technique-decision"]
        if isinstance(value.get("id"), str)
    }
    matrix = next(
        (value for _, value in by_type["matrix"] if value.get("id") == "niji-matrix"),
        {},
    )
    baseline_version = matrix.get("attack_baseline", {}).get("version")
    for technique_id, technique in techniques.items():
        classification = technique.get("classification", {})
        decision_ref = classification.get("decision_ref")
        decision = decisions.get(decision_ref)
        if decision and decision.get("resulting_technique_ref") != technique_id:
            errors.append(
                f"{technique_id}: 准入决策 {decision_ref} 未反向指向该技术"
            )
        origin = classification.get("origin", {})
        if origin.get("source_attack_version") not in {None, baseline_version}:
            errors.append(
                f"{technique_id}: ATT&CK 来源版本与 matrix.yaml 不一致"
            )
        decision_kind = decision.get("decision") if decision else None
        expected_origin = {
            "retain": "attack-retained",
            "adapt": "attack-adapted",
            "add": "niji-added",
        }.get(decision_kind)
        if expected_origin and origin.get("kind") != expected_origin:
            errors.append(
                f"{technique_id}: origin.kind 与准入决策 {decision_kind} 不一致"
            )

    for markdown_path in sorted((ROOT / "matrix" / "tactics").glob(
        "*/techniques/**/*.md"
    )):
        errors.append(
            f"{markdown_path.relative_to(ROOT)}: YAML-only 2.0 "
            "技术包不得包含 Markdown 正文"
        )

    for path, value in objects:
        if value.get("type") in {"technique", "evasion-subtechnique"}:
            status = value.get("lifecycle", {}).get("status")
            if status in {"review", "published"} and not value.get("evidence", {}).get("claim_refs"):
                warnings.append(
                    f"{path.relative_to(ROOT)}: {status} 对象尚未关联结构化主张"
                )

    print(
        f"已检查 {len(objects)} 个对象："
        f"{len(by_type['tactic'])} 个战术，"
        f"{len(by_type['technique'])} 个技术，"
        f"{len(by_type['evasion-subtechnique'])} 个匿迹子技术。"
    )

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"校验失败：{len(errors)} 个错误，{len(warnings)} 个警告。")
        return 1

    print(f"校验通过：0 个错误，{len(warnings)} 个警告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
