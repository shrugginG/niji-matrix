"""Apply three separate main-agent-authored cross-tactic child rewrites."""

from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
AUTHORED = yaml.safe_load((RUN / "T1659-formal-child-rewrite.yaml").read_text())
BASE = ROOT / "matrix/tactics/TA0001-initial-access/techniques/NJT-0052-content-injection/subtechniques"
PATHS = {
    "NJS-0052-001": BASE / "NJS-0052-001-target-and-request-gated-injection/subtechnique.yaml",
    "NJS-0052-002": BASE / "NJS-0052-002-racing-forged-response-injection/subtechnique.yaml",
    "NJS-0052-003": BASE / "NJS-0052-003-path-local-phantom-service-projection/subtechnique.yaml",
}
CLAIMS = {"NJS-0052-001": "CLM-001114", "NJS-0052-002": "CLM-001116", "NJS-0052-003": "CLM-001115"}

def unique(values):
    return list(dict.fromkeys(values))

for cid, path in PATHS.items():
    child = yaml.safe_load(path.read_text())
    prose = AUTHORED[cid]
    for field in ("definition_and_concept", "stealth_characteristics", "scope_boundary_definition", "application_scenarios_and_threat_model"):
        child[field] = prose[field]
    child["stealth_mechanisms"] = [
        {"mechanism_ref": m["mechanism_ref"], "role": m["role"],
         "summary": {lang: m["summary"][lang].rstrip("。.!?；; ") for lang in ("zh", "en")},
         "analysis": m["analysis"], "evidence_refs": m["evidence_keys"], "confidence": m["confidence"]}
        for m in prose["stealth_mechanisms"]
    ]
    if cid != "NJS-0052-002":
        child["defense"]["detections"]["strategy_refs"] = unique([*child["defense"]["detections"]["strategy_refs"], "DET-000261"])
        child["evidence"]["case_refs"] = unique([*child["evidence"]["case_refs"], "CASE-000342"])
    child["defense"]["mitigations"]["mitigation_refs"] = unique([*child["defense"]["mitigations"]["mitigation_refs"], "MIT-000230"])
    child["evidence"]["claim_refs"] = unique([*child["evidence"]["claim_refs"], CLAIMS[cid]])
    child["evidence"]["reference_refs"] = unique([*child["evidence"]["reference_refs"], *(r for m in child["stealth_mechanisms"] for r in m["evidence_refs"])])
    child["research"] = prose["research"]
    child["lifecycle"]["status"] = "review"
    child["lifecycle"]["version"] = "1.1.0"
    child["lifecycle"]["modified"] = "2026-10-05"
    path.write_text(yaml.safe_dump(child, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
print("Rewrote three NJT-0052 children with stage-specific entry and C2 boundaries")
