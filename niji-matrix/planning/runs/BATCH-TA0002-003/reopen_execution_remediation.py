from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[3]
TODAY = "2026-09-10"

BATCHES = {
    "BATCH-TA0002-003": ["T1197"],
    "BATCH-TA0002-004": ["T1059"],
    "BATCH-TA0002-005": ["T1106", "T1559"],
    "BATCH-TA0002-006": ["T1574"],
    "BATCH-TA0002-007": ["T1129", "T1127"],
    "BATCH-TA0002-008": ["T1651", "T1675"],
    "BATCH-TA0002-009": ["T1609", "T1610"],
    "BATCH-TA0002-010": ["T1648", "T1072"],
    "BATCH-TA0002-011": ["T1053", "T1569", "T1047"],
    "BATCH-TA0002-012": ["T1203", "T1674"],
    "BATCH-TA0002-013": ["T1204"],
    "BATCH-TA0002-014": ["T1677"],
}


def save(path: Path, value: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=180), encoding="utf-8")


def set_lifecycle_draft(path: Path) -> None:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    value["lifecycle"]["status"] = "draft"
    value["lifecycle"]["modified"] = TODAY
    save(path, value)


def main() -> None:
    tactic_root = ROOT / "matrix/tactics/TA0002-execution"
    technique_paths = sorted(tactic_root.glob("techniques/NJT-*/technique.yaml"))
    child_paths = sorted(tactic_root.glob("techniques/NJT-*/subtechniques/NJS-*/subtechnique.yaml"))
    ta2_subjects: set[str] = set()
    for path in [*technique_paths, *child_paths]:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        ta2_subjects.add(value["id"])
        set_lifecycle_draft(path)

    for path in sorted(tactic_root.glob("decisions/*.yaml")):
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        value["review"]["status"] = "draft"
        value["review"]["reviewers"] = []
        value["review"]["review_notes_zh"] = "机器结构门禁曾通过，但人工领域审阅发现语义深度与结论级证据不足，当前重新研究。"
        value["review"]["review_notes_en"] = "Machine structural gates previously passed, but human domain review found insufficient semantic depth and conclusion-level evidence; research is reopened."
        save(path, value)

    for path in sorted((ROOT / "claims").glob("*.yaml")):
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        subjects = set(value.get("subject_refs", []))
        if subjects and subjects <= ta2_subjects:
            value["status"] = "draft"
            save(path, value)

    for prefix, start, end, folder in [("DET", 57, 63, "detections"), ("NJA", 31, 42, "analytics"), ("MIT", 56, 61, "mitigations")]:
        for number in range(start, end + 1):
            matches = list((ROOT / folder).glob(f"{prefix}-{number:06d}-*.yaml"))
            if len(matches) != 1:
                raise SystemExit(f"expected one {prefix}-{number:06d} object, found {len(matches)}")
            set_lifecycle_draft(matches[0])

    plan_path = ROOT / "planning/tactics/TA0002.yaml"
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    plan["status"] = "active"
    plan["candidate_inventory"]["status"] = "complete"
    existing_batches = {item["id"]: item for item in plan["batches"]}
    existing_batches["BATCH-TA0002-001"]["status"] = "paused"
    existing_batches["BATCH-TA0002-002"]["status"] = "paused"
    for batch_id, attacks in BATCHES.items():
        item = existing_batches.get(batch_id)
        refs = [f"WORK-TA0002-{attack}" for attack in attacks]
        if item is None:
            item = {"id": batch_id, "status": "planned", "work_item_refs": refs}
            plan["batches"].append(item)
            existing_batches[batch_id] = item
        item["status"] = "active" if batch_id == "BATCH-TA0002-003" else "planned"
        item["work_item_refs"] = refs

    attack_to_batch = {attack: batch for batch, attacks in BATCHES.items() for attack in attacks}
    for item in plan["work_items"]:
        attack = item["source_attack_id"]
        batch = attack_to_batch[attack]
        item["batch_ref"] = batch
        item["stage"] = "researching" if attack == "T1197" else "untriaged"
        item["notes_zh"] = "人工审阅发现原内容未达到 NJT-0001 字段责任与证据深度，已保留现有 ID 并进入受控整改。" + ("当前作为单候选试点重新研究。" if attack == "T1197" else "等待前序整改批次通过后启动。")
        item["notes_en"] = "Human review found that the original content did not meet NJT-0001 field responsibility and evidence depth. Existing IDs are retained for controlled remediation. " + ("This candidate is the active single-candidate pilot." if attack == "T1197" else "It awaits completion of the preceding remediation batch.")

    plan["gap_analysis"] = {"status": "in-progress", "notes_zh": "固定基线候选清单保持完整；由于现有四十项 Niji 子技术正在重新核验稳定变量、兄弟边界和结论级证据，Execution 原生缺口分析同步重新打开。", "notes_en": "The fixed-baseline candidate inventory remains complete. Niji-native gap analysis is reopened while all forty current children are re-evaluated for stable variables, sibling boundaries, and conclusion-level evidence."}
    plan["review"] = {"taxonomy": "in-progress", "evidence": "in-progress", "bilingual": "in-progress", "reviewers": []}
    save(plan_path, plan)

    for batch_id in ["BATCH-TA0002-001", "BATCH-TA0002-002"]:
        path = ROOT / f"planning/runs/{batch_id}/integration-summary.yaml"
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        value["status"] = "active"
        value["review_notes_zh"] += " 后续人工领域审阅判定这些对象的字段深度、证据覆盖和候选特异性不足；本摘要保留机器结果作为历史记录，正式对象已退回 draft 并转入 BATCH-TA0002-003 至 BATCH-TA0002-014 整改。"
        value["review_notes_en"] += " Subsequent human domain review found insufficient field depth, evidence coverage, and candidate specificity. This summary retains the machine results as historical evidence; formal objects have returned to draft and moved into BATCH-TA0002-003 through BATCH-TA0002-014 remediation."
        save(path, value)


if __name__ == "__main__":
    main()
