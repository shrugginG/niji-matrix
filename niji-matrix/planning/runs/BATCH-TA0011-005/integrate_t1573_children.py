"""Serialize the fully authored T1573 child narratives after ID convergence."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
H = yaml.safe_load((RUN / "T1573-research-handoff.yaml").read_text())
M = yaml.safe_load((RUN / "canonical-id-map.yaml").read_text())
IDS = M["ids"]["T1573"]
TEMP = M["temporary_keys"]
BASE = ROOT / "matrix/tactics/TA0011-command-and-control/techniques/NJT-0223-adversary-keyed-c2-protection/subtechniques"
INFO = {
    "B5-T1573-SUB-REUSABLE-KEY": ("reusable-implant-key-protection", "CLM-001109", ["CASE-000339"], ["DET-000259"], ["MIT-000228"]),
    "B5-T1573-SUB-RUNTIME-SECRET": ("runtime-scoped-secret-establishment", "CLM-001110", ["CASE-000340", "CASE-000341"], ["DET-000259"], ["MIT-000228"]),
    "B5-T1573-SUB-NESTED-BOUNDARY": ("nested-cryptographic-inspection-boundary", "CLM-001111", ["CASE-000341"], ["DET-000260"], ["MIT-000229"]),
}

def refs(keys):
    return list(dict.fromkeys(k if str(k).startswith("REF-") else TEMP[k] for k in keys or []))

for child in H["proposed_subtechniques"]:
    key = child["key"]
    cid = IDS["children"][key]
    slug, claim, cases, detections, mitigations = INFO[key]
    mechanisms = []
    for m in child["stealth_mechanisms"]:
        mechanisms.append({
            "mechanism_ref": m["mechanism_ref"], "role": m["role"],
            "summary": {lang: m["summary"][lang].rstrip("。.!?；; ") for lang in ("zh", "en")},
            "analysis": m["analysis"], "evidence_refs": refs(m["evidence_keys"]),
            "confidence": m.get("confidence", "high"),
        })
    evidence_refs = refs([*child["evidence_keys"], *(key for m in child["stealth_mechanisms"] for key in m["evidence_keys"])])
    value = {
        "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": cid, "parent_ref": "NJT-0223",
        "name": child["name"], "summary": child["summary"], "aliases": [],
        "lineage": {"attck_subtechnique_inherited": False},
        "definition_and_concept": child["definition_and_concept"],
        "stealth_characteristics": child["stealth_characteristics"],
        "scope_boundary_definition": child["scope_boundary_definition"],
        "application_scenarios_and_threat_model": child["application_scenarios_and_threat_model"],
        "stealth_mechanisms": mechanisms,
        "defense": {"detections": {"coverage": "available", "strategy_refs": detections},
                    "mitigations": {"coverage": "available", "mitigation_refs": mitigations}},
        "evidence": {"claim_refs": [claim], "case_refs": cases, "reference_refs": evidence_refs},
        "research": {"limitations": child["research_limitations"]},
        "lifecycle": {"status": "review", "version": "1.0.0", "created": "2026-10-05", "modified": "2026-10-05", "contributors": ["Niji Matrix Research"], "reviewers": []},
    }
    path = BASE / f"{cid}-{slug}" / "subtechnique.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
print("Serialized three T1573 Niji-native children")
