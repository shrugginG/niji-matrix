"""Serialize reviewed candidate-specific DET/NJA/MIT objects and exact MIT applications."""

from __future__ import annotations
from pathlib import Path
import re
import unicodedata
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
ORDER = ("T1571", "T1572", "T1573", "T1659", "T1665")
H = {tid: yaml.safe_load((RUN / f"{tid}-research-handoff.yaml").read_text()) for tid in ORDER}
M = yaml.safe_load((RUN / "canonical-id-map.yaml").read_text())
IDS, TEMP = M["ids"], M["temporary_keys"]
O = yaml.safe_load((RUN / "defense-overrides.yaml").read_text())
LIFE = {"status": "review", "version": "1.0.0", "created": "2026-10-05", "modified": "2026-10-05", "contributors": ["Niji Matrix Research"], "reviewers": []}
STRATEGY_TARGETS = {
    "B5-T1571-DET-SEMANTIC-PORT-DIFFERENTIAL": ["NJT-0221"],
    "B5-T1572-DET-CROSSLAYER": ["NJT-0222", "NJS-0222-001", "NJS-0222-002", "NJS-0222-003"],
    "B5-T1573-DET-KEY-RECOVERY": ["NJT-0223", "NJS-0223-001", "NJS-0223-002"],
    "B5-T1573-DET-NESTED": ["NJT-0223", "NJS-0223-003"],
    "B5-T1659-DET-C2-INJECTION": ["NJT-0052", "NJS-0052-001", "NJS-0052-003"],
    "B5-T1665-DET-VICTIM-EXPOSURE-DIFFERENTIAL": ["NJT-0224", "NJS-0224-001", "NJS-0224-002"],
}

def key(item):
    return item.get("temporary_key") or item.get("key")

def unique(items):
    return list(dict.fromkeys(items))

def refs(keys):
    return unique(k if str(k).startswith("REF-") else TEMP[k] for k in keys or [])

def block(value):
    if isinstance(value, dict) and "paragraphs" in value:
        return value
    if isinstance(value, dict) and set(value) == {"zh", "en"}:
        return {"paragraphs": [value]}
    raise ValueError(value)

def slug(text):
    normalized = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")[:90] or "object"

def save(directory, value):
    path = ROOT / directory / f"{value['id']}-{slug(value['name']['en'])}.yaml"
    if path.exists():
        raise FileExistsError(path)
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

def strategies():
    for tid in ORDER:
        group = H[tid]["defense_candidates"]
        for item in group["detection_strategies"]:
            k = key(item)
            override = O["strategies"][k]
            analytics = [a for a in group["detection_analytics"] if (a.get("strategy_key") or k) == k]
            if len(group["detection_strategies"]) == 1:
                analytics = group["detection_analytics"]
            analytic_refs = [IDS[tid]["analytics"][key(a)] for a in analytics]
            evidence = refs([*(item.get("evidence_keys") or []), *(r for a in analytics for r in a.get("evidence_keys", []))])
            value = {
                "schema_version": "2.0.0", "type": "detection-strategy", "id": IDS[tid]["detections"][k],
                "name": item["name"], "summary": override["summary"], "description": override["description"],
                "detects_refs": STRATEGY_TARGETS[k], "domains": ["enterprise"],
                "analytic_refs": analytic_refs, "evidence_refs": evidence, "lifecycle": LIFE.copy(),
            }
            save("detections", value)

def data_requirements(tid, item):
    requirements = []
    for raw in item.get("data_requirements", []):
        source = raw["source_type"]
        name = raw.get("name") or O["data_source_names"][source]
        requirements.append({"source_type": source.replace("_", "-"), "name": name,
                             "channel": raw.get("channel"), "required_fields": unique(raw["required_fields"])})
    if requirements:
        return requirements
    for raw in item.get("raw_to_normalized_fields", []):
        source = raw.get("source") or raw.get("source_type")
        if source not in O["data_source_names"]:
            raise KeyError((tid, source))
        fields = raw.get("normalized_fields") or raw.get("required_fields")
        requirements.append({"source_type": source.replace("_", "-"),
                             "name": O["data_source_names"][source], "channel": raw.get("channel"),
                             "required_fields": unique(fields)})
    return requirements

def analytics():
    for tid in ORDER:
        group = H[tid]["defense_candidates"]
        default_strategy = key(group["detection_strategies"][0])
        for item in group["detection_analytics"]:
            k = key(item)
            override = O["analytics"].get(k, {})
            strategy_key = item.get("strategy_key") or default_strategy
            raw_correlation = item["correlation"]
            window = override.get("window") or raw_correlation["window"]
            if not isinstance(window, dict):
                raise ValueError((k, "correlation window needs bilingual review"))
            for field in ("observables", "false_positives", "blind_spots"):
                if field not in override and any(not isinstance(x, dict) for x in item[field]):
                    raise ValueError((k, field, "needs bilingual review"))
            value = {
                "schema_version": "2.0.0", "type": "detection-analytic", "id": IDS[tid]["analytics"][k],
                "strategy_ref": IDS[tid]["detections"][strategy_key], "name": item["name"],
                "summary": override["summary"], "domains": ["enterprise"],
                "platforms": item.get("platforms") or (["Network", "Windows", "Linux"] if tid != "T1659" else ["Network", "Windows", "Linux", "macOS"]),
                "logic": block(item["logic"]), "data_requirements": data_requirements(tid, item),
                "observables": override.get("observables") or item["observables"],
                "correlation": {"window": window, "dimensions": unique(raw_correlation["dimensions"])},
                "false_positives": override.get("false_positives") or item["false_positives"],
                "blind_spots": override.get("blind_spots") or item["blind_spots"],
                "tuning_guidance": block(item["tuning_guidance"]),
                "evidence_refs": refs(item.get("evidence_keys")), "lifecycle": LIFE.copy(),
            }
            if not value["data_requirements"]:
                raise ValueError((k, "no data requirements"))
            save("analytics", value)

def target_ref(tid, raw):
    if raw == "parent" or raw == f"B5-{tid}-PARENT":
        return IDS[tid]["parent"]
    if raw in TEMP:
        return TEMP[raw]
    if str(raw).startswith(("NJT-", "NJS-")):
        return raw
    raise KeyError((tid, raw))

def application(tid, raw):
    target = raw.get("target_ref") or raw.get("target_key") or raw.get("target")
    return {"target_ref": target_ref(tid, target), "use": block(raw["use"]),
            "expected_effect": block(raw["expected_effect"]), "limitations": block(raw["limitations"])}

def mitigation(tid, item):
    k = key(item)
    mid = IDS[tid]["mitigations"][k]
    apps = [application(tid, a) for a in item["applications"]]
    if item.get("existing_ref"):
        paths = list((ROOT / "mitigations").glob(f"{mid}-*.yaml"))
        if len(paths) != 1:
            raise ValueError((mid, paths))
        path = paths[0]
        value = yaml.safe_load(path.read_text())
        existing = {a["target_ref"] for a in value["applications"]}
        for app in apps:
            if app["target_ref"] in existing:
                raise ValueError((mid, app["target_ref"], "duplicate application"))
            value["applications"].append(app)
        value["evidence_refs"] = unique([*value["evidence_refs"], *refs(item.get("evidence_keys"))])
        value["lifecycle"]["status"] = "review"
        value["lifecycle"]["modified"] = "2026-10-05"
        value["lifecycle"]["version"] = "1.2.0"
        path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
        return
    measures = []
    for raw in item["measures"]:
        action = raw.get("description") or raw.get("implementation") or raw.get("action")
        measures.append({"key": raw["key"].replace("_", "-"),
                         "name": raw.get("name") or O["measure_names"][raw["key"]],
                         "description": block(action), "control_type": "containment" if raw["control_type"] == "responsive" else raw["control_type"]})
    description = item.get("description") or item.get("control_purpose")
    if not description:
        raise ValueError((k, "mitigation description"))
    value = {
        "schema_version": "2.0.0", "type": "mitigation", "id": mid,
        "name": item["name"], "summary": description, "description": block(description),
        "domains": ["enterprise"], "measures": measures, "applications": apps,
        "evidence_refs": refs(item.get("evidence_keys")), "lifecycle": LIFE.copy(),
    }
    if not value["evidence_refs"]:
        raise ValueError((k, "no mitigation evidence"))
    save("mitigations", value)

def mitigations():
    for tid in ORDER:
        for item in H[tid]["defense_candidates"]["mitigations"]:
            mitigation(tid, item)

strategies()
analytics()
mitigations()
print("Serialized six DET, nine NJA, five new MIT, and two exact MIT extensions")
