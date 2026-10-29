from __future__ import annotations

import argparse
from pathlib import Path

import yaml

import integrate_remaining_execution as integration
from generate_remaining_execution import PARENTS, ROOT, TODAY


AFFECTED_SHARED = [
    "detections/DET-000058-management-plane-workload-execution.yaml",
    "detections/DET-000059-interpreter-load-ipc-lineage.yaml",
    "detections/DET-000060-client-trigger-execution-causality.yaml",
    "analytics/NJA-000032-management-plane-workload-execution.yaml",
    "analytics/NJA-000034-interpreter-load-ipc-lineage.yaml",
    "mitigations/MIT-000057-privileged-management-execution-governance.yaml",
    "mitigations/MIT-000058-execution-mediation-hardening.yaml",
    "mitigations/MIT-000059-client-trigger-surface-hardening.yaml",
]


def promote(path: Path) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    lifecycle = data.get("lifecycle")
    if lifecycle:
        lifecycle["status"] = "review"
        lifecycle["modified"] = TODAY
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=180), encoding="utf-8")


def promote_objects() -> None:
    for parent in PARENTS:
        base = ROOT / f"matrix/tactics/TA0002-execution/techniques/{parent['id']}-{parent['slug']}"
        promote(base / "technique.yaml")
        for child in parent["children"]:
            promote(base / f"subtechniques/{child['id']}-{child['slug']}/subtechnique.yaml")
    for path in (ROOT / "detections").glob("DET-00006[1-3]-*.yaml"):
        promote(path)
    for path in (ROOT / "analytics").glob("NJA-0000[3-4][7-9]-*.yaml"):
        promote(path)
    for path in (ROOT / "analytics").glob("NJA-00004[0-2]-*.yaml"):
        promote(path)
    for path in (ROOT / "mitigations").glob("MIT-00006[0-1]-*.yaml"):
        promote(path)
        text = path.read_text(encoding="utf-8").replace("It constrain ", "It will constrain ").replace("It reduce ", "It will reduce ")
        path.write_text(text, encoding="utf-8")
    for relative in AFFECTED_SHARED:
        promote(ROOT / relative)
    integration.write_decisions("review")


def repair_generator() -> None:
    path = Path(integration.__file__)
    text = path.read_text(encoding="utf-8")
    old = "It {mitigation['summary_en'][0].lower() + mitigation['summary_en'][1:]}"
    new = "It will {mitigation['summary_en'][0].lower() + mitigation['summary_en'][1:]}"
    if old in text:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-web-success", action="store_true")
    args = parser.parse_args()
    promote_objects()
    repair_generator()
    if args.record_web_success:
        integration.update_plan(True)
        integration.write_summary(True)


if __name__ == "__main__":
    main()
