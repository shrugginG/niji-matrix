#!/usr/bin/env python3
"""Promote only completed BATCH-TA0008-002 objects after semantic and machine gates."""
from pathlib import Path
import glob
import yaml
ROOT=Path(__file__).resolve().parents[3]
NEW={
"NJT":[148,149,150,151],
"NJS":["0148-001","0148-002","0151-001","0151-002"],
"DET":range(166,171),"NJA":range(178,186),"MIT":range(152,156),
"CLM":range(754,770),"CASE":range(203,213)}
ids=[*(f"NJT-{x:04d}" for x in NEW["NJT"]),
     *(f"NJS-{x}" for x in NEW["NJS"]),
     *(f"DET-{x:06d}" for x in NEW["DET"]),
     *(f"NJA-{x:06d}" for x in NEW["NJA"]),
     *(f"MIT-{x:06d}" for x in NEW["MIT"]),
     *(f"CLM-{x:06d}" for x in NEW["CLM"]),
     *(f"CASE-{x:06d}" for x in NEW["CASE"]),
     "NJT-0058","NJS-0058-001","NJS-0058-002","MIT-000053","MIT-000036",
     "CLM-000215","CLM-000216","CASE-000109"]
for id in ids:
    matches=[]
    for folder in ["matrix/tactics","detections","analytics","mitigations","claims","cases"]:
        matches+=glob.glob(str(ROOT/folder/"**"/(id+"-*.yaml")),recursive=True)
        if id.startswith(("NJT","NJS")):
            matches+=glob.glob(str(ROOT/folder/"**"/(id+"-*")/"technique.yaml"),recursive=True)
            matches+=glob.glob(str(ROOT/folder/"**"/(id+"-*")/"subtechnique.yaml"),recursive=True)
    matches=list(dict.fromkeys(matches))
    assert len(matches)==1,(id,matches)
    path=Path(matches[0]);d=yaml.safe_load(path.read_text())
    if "lifecycle" in d:d["lifecycle"]["status"]="review"
    else:d["status"]="review"
    path.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120))
for attack in ["T1080","T1091","T1210","T1534","T1563"]:
    path=ROOT/"matrix"/"tactics"/"TA0008-lateral-movement"/"decisions"/f"DEC-TA0008-{attack}.yaml"
    d=yaml.safe_load(path.read_text())
    d["review"].update(status="review",review_notes_zh="证据、准入、原生分类、双语正文、专用防御、查重、质量、Bundle 和 Web/API 门禁通过；等待人工领域评审。",
                       review_notes_en="Evidence, admission, native taxonomy, bilingual prose, targeted defense, deduplication, quality, bundle, and Web/API gates pass pending human domain review.")
    path.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120))
print("promoted",len(ids),"shared/formal objects and 5 decisions to review")
