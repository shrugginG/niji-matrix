#!/usr/bin/env python3
"""Serialize candidate-reviewed atomic conclusions after primary source decisions."""
from pathlib import Path
import re
import yaml
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
ids=yaml.safe_load((RUN/"integration-id-map.yaml").read_text())
handoffs={n:yaml.safe_load((RUN/f"{n}-handoff.yaml").read_text()) for n in ["T1080","T1091","T1210","T1534","T1563"]}
source={x["key"]:x for d in handoffs.values() for x in d["library_candidates"]["claims"] if isinstance(x,dict) and x.get("key")}
R=ids["references"]
# Key, canonical ID, claim type, covered subjects, reviewed supporting sources,
# mode and calibrated confidence are resolved individually.
ROWS=[
("B8B-T1080-CLM-PARENT","CLM-000754","technique-boundary",["NJT-0148"],["REF-000589","REF-000590","REF-000591"],"strongly-inferred","medium"),
("B8B-T1080-CLM-CONTENT-ID","CLM-000755","subtechnique-existence",["NJT-0148","NJS-0148-001"],["REF-000590","REF-000591"],"directly-observed","medium"),
("B8B-T1080-CLM-NAVIGATION","CLM-000756","subtechnique-existence",["NJT-0148","NJS-0148-002"],["REF-000592","REF-000589"],"directly-observed","medium"),
("B8B-T1080-CLM-AUDIT","CLM-000757","detection",["NJT-0148","DET-000166"],["REF-000474","REF-000379","REF-000593"],"strongly-inferred","medium"),
("B8B-T1091-CLM-LATERAL-RELEVANCE","CLM-000758","technique-boundary",["NJT-0058"],["REF-000091","REF-000596"],"strongly-inferred","high"),
("B8B-T1091-CLM-MEDIA-LINEAGE","CLM-000759","detection",["NJT-0058","DET-000167"],["REF-000596","REF-000597","REF-000475","REF-000598"],"strongly-inferred","medium"),
("B8B-T1210-CLM-ADMISSION","CLM-000760","technique-relevance",["NJT-0149"],["REF-000599","REF-000591","REF-000602"],"strongly-inferred","medium"),
("B8B-T1210-CLM-OBSERVATION","CLM-000761","mechanism-mapping",["NJT-0149"],["REF-000603","REF-000377","REF-000602"],"strongly-inferred","medium"),
("B8B-T1210-CLM-MIXED-PATHS","CLM-000762","technique-boundary",["NJT-0149"],["REF-000600","REF-000601"],"directly-observed","medium"),
("B8B-T1534-CLM-PARENT","CLM-000763","technique-relevance",["NJT-0150"],["REF-000606", "REF-000607", "REF-000608"],"directly-observed","high"),
("B8B-T1534-CLM-TRUST","CLM-000764","mechanism-mapping",["NJT-0150"],["REF-000607", "REF-000608"],"strongly-inferred","medium"),
("B8B-T1534-CLM-FEEDBACK","CLM-000765","technique-boundary",["NJT-0150","NJS-0111-001"],["REF-000608", "REF-000612"],"directly-observed","high"),
("B8B-T1563-CLM-BOUNDARY","CLM-000766","technique-boundary",["NJT-0151"],["REF-000613", "REF-000614", "REF-000617"],"strongly-inferred","medium"),
("B8B-T1563-CLM-CHANNEL","CLM-000767","subtechnique-existence",["NJS-0151-001"],["REF-000614", "REF-000615", "REF-000616", "REF-000370"],"strongly-inferred","medium"),
("B8B-T1563-CLM-ATTACH","CLM-000768","subtechnique-existence",["NJS-0151-002"],["REF-000617", "REF-000618", "REF-000619", "REF-000621", "REF-000622", "REF-000624"],"strongly-inferred","medium"),
("B8B-T1563-CLM-DEFENSE","CLM-000769","detection",["NJT-0151","DET-000170"],["REF-000616", "REF-000621", "REF-000622", "REF-000623"],"strongly-inferred","medium"),
]
assert len(ROWS)==16
for key,cid,typ,subjects,refs,mode,confidence in ROWS:
    x=source[key]
    zh=x.get("statement_zh") or x.get("proposition_zh") or (x.get("statement") or {}).get("zh") or (x.get("proposition") or {}).get("zh")
    en=x.get("statement_en") or x.get("proposition_en") or (x.get("statement") or {}).get("en") or (x.get("proposition") or {}).get("en")
    assert isinstance(zh,str) and isinstance(en,str) and len(zh)>20 and len(en)>40,key
    obj={"schema_version":"1.0.0","type":"claim","id":cid,"claim_type":typ,
         "statement_zh":zh,"statement_en":en,"subject_refs":subjects,
         "evidence_refs":refs,"evidence_mode":mode,"confidence":confidence,"status":"draft"}
    slug=re.sub(r"[^a-z0-9]+","-",key.removeprefix("B8B-").lower()).strip("-")
    p=ROOT/"claims"/f"{cid}-{slug}.yaml"
    if p.exists():raise RuntimeError(p)
    p.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print(f"serialized {len(ROWS)} reviewed claims")
