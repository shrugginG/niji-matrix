"""Apply the reviewed dual-tactic T1659 parent rewrite to existing NJT-0052."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
H = yaml.safe_load((RUN / "T1659-research-handoff.yaml").read_text())
IDS = yaml.safe_load((RUN / "canonical-id-map.yaml").read_text())
TEMP = IDS["temporary_keys"]
P = ROOT / "matrix/tactics/TA0001-initial-access/techniques/NJT-0052-content-injection/technique.yaml"
parent = yaml.safe_load(P.read_text())
content = H["proposed_content"]

def refs(keys):
    return list(dict.fromkeys(k if str(k).startswith("REF-") else TEMP[k] for k in keys or []))

def extend_unique(values, new):
    return list(dict.fromkeys([*values, *new]))

parent["summary"] = content["summary"]
parent["aliases"] = extend_unique(parent.get("aliases", []), ["Online-Path Content Injection"])
parent["classification"]["tactic_refs"] = extend_unique(parent["classification"]["tactic_refs"], ["TA0011"])
for field in ("definition_and_concept", "stealth_characteristics", "scope_boundary_definition", "application_scenarios_and_threat_model"):
    parent[field] = content[field]
parent["stealth_mechanisms"] = [
    {"mechanism_ref": m["mechanism_ref"], "role": m["role"],
     "summary": {lang: m["summary"][lang].rstrip("。.!?；; ") for lang in ("zh", "en")},
     "analysis": m["analysis"], "evidence_refs": refs(m["evidence_keys"]),
     "confidence": m["confidence"]}
    for m in content["stealth_mechanisms"]
]
parent["subtechnique_taxonomy"] = {
    "narrative": content["subtechnique_taxonomy"]["narrative"],
    "coverage": "established", "subtechnique_refs": ["NJS-0052-001", "NJS-0052-002", "NJS-0052-003"],
}
parent["defense"]["detections"]["strategy_refs"] = extend_unique(parent["defense"]["detections"]["strategy_refs"], ["DET-000261"])
parent["defense"]["mitigations"]["mitigation_refs"] = extend_unique(parent["defense"]["mitigations"]["mitigation_refs"], ["MIT-000230"])
parent["evidence"]["claim_refs"] = extend_unique(parent["evidence"]["claim_refs"], list(IDS["ids"]["T1659"]["claims"].values()))
parent["evidence"]["case_refs"] = extend_unique(parent["evidence"]["case_refs"], ["CASE-000342"])
parent["evidence"]["reference_refs"] = extend_unique(parent["evidence"]["reference_refs"], H["existing_library_reuse"]["reference_refs"])
for m in parent["stealth_mechanisms"]:
    parent["evidence"]["reference_refs"] = extend_unique(parent["evidence"]["reference_refs"], m["evidence_refs"])
parent["research"]["limitations"] = H["research"]["limitations"]
parent["lifecycle"]["status"] = "review"
parent["lifecycle"]["version"] = "1.1.0"
parent["lifecycle"]["modified"] = "2026-10-05"
P.write_text(yaml.safe_dump(parent, allow_unicode=True, sort_keys=False, width=120))
print("Rewrote NJT-0052 for TA0001 and TA0011")
