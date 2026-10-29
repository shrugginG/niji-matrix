"""Record centrally reserved IDs against the five reviewed research handoffs."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ORDER = ("T1571", "T1572", "T1573", "T1659", "T1665")
H = {k: yaml.safe_load((RUN / f"{k}-research-handoff.yaml").read_text()) for k in ORDER}
PARENTS = {"T1571": "NJT-0221", "T1572": "NJT-0222", "T1573": "NJT-0223", "T1659": "NJT-0052", "T1665": "NJT-0224"}
NEW_REF = iter(f"REF-{i:06d}" for i in range(1132, 1159))
NEW_CLM = iter(f"CLM-{i:06d}" for i in range(1098, 1122))
NEW_CASE = iter(f"CASE-{i:06d}" for i in range(334, 346))
NEW_DET = iter(f"DET-{i:06d}" for i in range(257, 263))
NEW_NJA = iter(f"NJA-{i:06d}" for i in range(343, 352))
NEW_MIT = iter(f"MIT-{i:06d}" for i in range(227, 232))

def key(item):
    return item.get("temporary_key") or item.get("key")

ids = {}
all_keys = {}
for tid in ORDER:
    x = H[tid]
    group = {"parent": PARENTS[tid], "children": {}, "references": {}, "claims": {}, "cases": {}, "detections": {}, "analytics": {}, "mitigations": {}}
    parent_digits = PARENTS[tid][-4:]
    for index, child in enumerate(x.get("proposed_subtechniques", []), 1):
        group["children"][key(child)] = f"NJS-{parent_digits}-{index:03d}"
    for item in x.get("library_candidates", {}).get("references", []):
        group["references"][key(item)] = item.get("existing_id") or next(NEW_REF)
    for item in x.get("library_candidates", {}).get("claims", []):
        group["claims"][key(item)] = next(NEW_CLM)
    for item in x.get("library_candidates", {}).get("cases", []):
        group["cases"][key(item)] = next(NEW_CASE)
    for item in x.get("defense_candidates", {}).get("detection_strategies", []):
        group["detections"][key(item)] = next(NEW_DET)
    for item in x.get("defense_candidates", {}).get("detection_analytics", []):
        group["analytics"][key(item)] = next(NEW_NJA)
    for item in x.get("defense_candidates", {}).get("mitigations", []):
        group["mitigations"][key(item)] = item.get("existing_ref") or next(NEW_MIT)
    ids[tid] = group
    for mapping in group.values():
        if isinstance(mapping, dict):
            for k, v in mapping.items():
                if k in all_keys and all_keys[k] != v:
                    raise ValueError((k, all_keys[k], v))
                all_keys[k] = v

for sequence in (NEW_REF, NEW_CLM, NEW_CASE, NEW_DET, NEW_NJA, NEW_MIT):
    try:
        raise ValueError(f"Unused reserved ID: {next(sequence)}")
    except StopIteration:
        pass

result = {"batch_ref": "BATCH-TA0011-005", "ids": ids, "temporary_keys": all_keys}
(RUN / "canonical-id-map.yaml").write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False, width=120))
print("Mapped", len(all_keys), "temporary keys")
