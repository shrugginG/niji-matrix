"""Serialize the five main-agent-reviewed T1572 and T1665 child narratives."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
M = yaml.safe_load((RUN / "canonical-id-map.yaml").read_text())
TEMP = M["temporary_keys"]
CONFIG = {
    "T1572": {
        "base": "NJT-0222-nested-protocol-session-tunneling", "parent": "NJT-0222",
        "slugs": ["inner-service-endpoint-decoupling", "outer-session-multi-stream-convergence", "transactionized-inner-stream-reassembly"],
        "claims": ["CLM-001103", "CLM-001104", "CLM-001105"],
        "cases": [[], ["CASE-000337"], ["CASE-000338"]],
        "detections": [["DET-000258"]] * 3,
        "mitigations": [["MIT-000172"], ["MIT-000172"], ["MIT-000200"]],
    },
    "T1665": {
        "base": "NJT-0224-selective-c2-infrastructure-exposure", "parent": "NJT-0224",
        "slugs": ["request-qualified-c2-exposure", "defender-observer-selective-suppression"],
        "claims": ["CLM-001118", "CLM-001119"],
        "cases": [["CASE-000344"], ["CASE-000343"]],
        "detections": [["DET-000262"]] * 2,
        "mitigations": [["MIT-000231"]] * 2,
    },
}

def refs(keys):
    return list(dict.fromkeys(k if str(k).startswith("REF-") else TEMP[k] for k in keys or []))

for tid, info in CONFIG.items():
    handoff = yaml.safe_load((RUN / f"{tid}-research-handoff.yaml").read_text())
    authored = yaml.safe_load((RUN / f"{tid}-formal-child-prose.yaml").read_text())
    candidates = handoff["proposed_subtechniques"]
    if len(candidates) != len(info["slugs"]):
        raise ValueError(tid)
    for index, candidate in enumerate(candidates):
        key = candidate.get("temporary_key") or candidate.get("key")
        prose = authored[key]
        child_id = M["ids"][tid]["children"][key]
        mechanisms = []
        for raw in prose["stealth_mechanisms"]:
            mechanisms.append({
                "mechanism_ref": raw["mechanism_ref"], "role": raw["role"],
                "summary": {lang: raw["summary"][lang].rstrip("。.!?；; ") for lang in ("zh", "en")},
                "analysis": raw["analysis"], "evidence_refs": refs(raw["evidence_keys"]),
                "confidence": raw["confidence"],
            })
        evidence_refs = refs([*candidate.get("evidence_keys", []), *(k for m in prose["stealth_mechanisms"] for k in m["evidence_keys"])])
        value = {
            "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": child_id,
            "parent_ref": info["parent"], "name": candidate["name"], "summary": prose["summary"],
            "aliases": [], "lineage": {"attck_subtechnique_inherited": False},
            "definition_and_concept": prose["definition_and_concept"],
            "stealth_characteristics": prose["stealth_characteristics"],
            "scope_boundary_definition": prose["scope_boundary_definition"],
            "application_scenarios_and_threat_model": prose["application_scenarios_and_threat_model"],
            "stealth_mechanisms": mechanisms,
            "defense": {"detections": {"coverage": "available", "strategy_refs": info["detections"][index]},
                        "mitigations": {"coverage": "available", "mitigation_refs": info["mitigations"][index]}},
            "evidence": {"claim_refs": [info["claims"][index]], "case_refs": info["cases"][index], "reference_refs": evidence_refs},
            "research": prose["research"],
            "lifecycle": {"status": "review", "version": "1.0.0", "created": "2026-10-05", "modified": "2026-10-05", "contributors": ["Niji Matrix Research"], "reviewers": []},
        }
        path = ROOT / "matrix/tactics/TA0011-command-and-control/techniques" / info["base"] / "subtechniques" / f"{child_id}-{info['slugs'][index]}" / "subtechnique.yaml"
        if path.exists():
            raise FileExistsError(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
print("Serialized five T1572/T1665 Niji-native children")
