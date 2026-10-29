#!/usr/bin/env python3
"""Validate tactic plans and the global ID reservation registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from allocate_id import entity_for_id, load_reservations
from library_common import ROOT, load_objects


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    objects, _ = load_objects(ROOT)
    matrix = objects.get("niji-matrix", {})
    baseline = matrix.get("attack_baseline", {})
    schema_path = ROOT / "planning" / "schemas" / "tactic-plan.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    plans = sorted((ROOT / "planning" / "tactics").glob("*.yaml"))

    for path in plans:
        relative = path.relative_to(ROOT)
        value = load_yaml(path)
        for issue in sorted(
            validator.iter_errors(value),
            key=lambda error: list(error.path),
        ):
            location = ".".join(str(item) for item in issue.path) or "<root>"
            errors.append(f"{relative}:{location}: {issue.message}")
        if not isinstance(value, dict):
            continue
        if value.get("tactic_ref") not in objects:
            errors.append(
                f"{relative}: tactic_ref 无法解析：{value.get('tactic_ref')}"
            )
        plan_baseline = value.get("attack_baseline", {})
        if (
            plan_baseline.get("domain") != baseline.get("domain")
            or plan_baseline.get("version") != baseline.get("version")
        ):
            errors.append(f"{relative}: ATT&CK 基线与 matrix.yaml 不一致")

        batch_items = {
            work_ref
            for batch in value.get("batches", [])
            for work_ref in batch.get("work_item_refs", [])
        }
        work_ids = [
            item.get("id")
            for item in value.get("work_items", [])
            if isinstance(item, dict)
        ]
        if len(work_ids) != len(set(work_ids)):
            errors.append(f"{relative}: work item ID 重复")
        for item in value.get("work_items", []):
            item_id = item.get("id")
            batch_ref = item.get("batch_ref")
            decision_ref = item.get("decision_ref")
            technique_ref = item.get("resulting_technique_ref")
            if batch_ref and item_id not in batch_items:
                errors.append(
                    f"{relative}: {item_id} 未被批次 {batch_ref} 反向列出"
                )
            if decision_ref and decision_ref not in objects:
                errors.append(
                    f"{relative}: {item_id} 的 decision_ref 无法解析："
                    f"{decision_ref}"
                )
            if technique_ref and technique_ref not in objects:
                errors.append(
                    f"{relative}: {item_id} 的 resulting_technique_ref "
                    f"无法解析：{technique_ref}"
                )
            if item.get("stage") in {"review", "published"} and not decision_ref:
                errors.append(
                    f"{relative}: {item_id} 已进入 {item.get('stage')} "
                    f"但没有 decision_ref"
                )

    registry = load_reservations(ROOT)
    reservation_ids: set[str] = set()
    for index, item in enumerate(registry.get("reservations", [])):
        location = f"planning/id-reservations.yaml:reservations[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{location}: 必须是对象")
            continue
        object_id = item.get("id")
        if not isinstance(object_id, str) or not entity_for_id(object_id):
            errors.append(f"{location}: 无效 ID：{object_id}")
            continue
        if object_id in reservation_ids:
            errors.append(f"{location}: 重复预留 {object_id}")
        reservation_ids.add(object_id)
        if item.get("entity") != entity_for_id(object_id):
            errors.append(f"{location}: entity 与 ID 前缀不一致")
        if item.get("status") not in {"reserved", "consumed", "archived", "released"}:
            errors.append(f"{location}: 无效状态：{item.get('status')}")
        if not item.get("owner"):
            errors.append(f"{location}: 缺少 owner")
        if item.get("status") == "consumed" and object_id not in objects:
            errors.append(f"{location}: consumed ID 尚无正式对象")
        if item.get("status") == "reserved" and object_id in objects:
            warnings.append(f"{location}: 正式对象已存在，应标记 consumed")
        if item.get("status") == "released" and object_id in objects:
            errors.append(f"{location}: 已存在对象的 ID 不得 released")
        if item.get("status") == "archived" and object_id in objects:
            errors.append(f"{location}: 已归档 ID 不得仍有活动正式对象")

    resolution_path = ROOT / "planning" / "duplicate-resolutions.yaml"
    resolution_value = load_yaml(resolution_path)
    resolution_pairs: set[tuple[str, str]] = set()
    if not isinstance(resolution_value, dict) or resolution_value.get("type") != "duplicate-resolutions":
        errors.append("planning/duplicate-resolutions.yaml: 无效决议表")
    else:
        for index, item in enumerate(resolution_value.get("resolutions", [])):
            location = f"planning/duplicate-resolutions.yaml:resolutions[{index}]"
            ids_in_resolution = item.get("ids", []) if isinstance(item, dict) else []
            pair = tuple(sorted(ids_in_resolution))
            if len(pair) != 2 or pair[0] == pair[1]:
                errors.append(f"{location}: ids 必须包含两个不同对象")
                continue
            if pair in resolution_pairs:
                errors.append(f"{location}: 重复的判重决议 {pair}")
            resolution_pairs.add(pair)
            for resolved_id in pair:
                if resolved_id not in objects:
                    errors.append(f"{location}: 无法解析 {resolved_id}")
            if item.get("disposition") not in {"reuse", "extend", "create", "split", "defer"}:
                errors.append(f"{location}: 无效 disposition")
            if not item.get("reason_zh") or not item.get("reason_en"):
                errors.append(f"{location}: 缺少双语判重理由")

    print(
        f"已检查 {len(plans)} 个战术计划和 "
        f"{len(registry.get('reservations', []))} 条 ID 记录。"
    )
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"规划校验失败：{len(errors)} 个错误，{len(warnings)} 个警告。")
        return 1
    print(f"规划校验通过：0 个错误，{len(warnings)} 个警告。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
