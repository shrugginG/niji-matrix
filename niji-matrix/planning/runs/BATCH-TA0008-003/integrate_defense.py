#!/usr/bin/env python3
"""Serialize T1021 DET/NJA and target-specific extensions to existing controls."""
from pathlib import Path
import glob,re,yaml
ROOT=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
h=yaml.safe_load((RUN/"T1021-handoff.yaml").read_text())
REF={"B8C-T1021-REF-ATTACK19":"REF-000842","B8C-T1021-REF-MS-ATTACK-MODEL":"REF-000843",
"B8C-T1021-REF-MANDIANT-FIN11":"REF-000844","B8C-T1021-REF-MANDIANT-RDP-BASELINE":"REF-000845",
"B8C-T1021-REF-MANDIANT-RDP-TUNNEL":"REF-000846","B8C-T1021-REF-MS-EXCHANGE-TUNNEL":"REF-000847",
"B8C-T1021-REF-MS-MDE-LOGON":"REF-000848"}
def refs(keys):
 out=[]
 for k in keys:
  v=k if k.startswith("REF-") else REF[k]
  if v not in out:out.append(v)
 return out
def P(v):return {"paragraphs":[v]}
analytic_ids=["NJA-000257","NJA-000258"]
summaries=[
{"zh":"按主体、来源和目标角色、服务与会话内动作识别贴合批准管理关系的恶意远程控制。","en":"Identify malicious remote control that conforms to an approved management relationship by principal, source and destination role, service, and in-session action."},
{"zh":"从目标所见跳板或 localhost 反查中继双侧流、转发状态与原始控制端。","en":"Trace a destination-visible jump host or localhost through bilateral relay flows and forwarding state to the original controller."}]
platforms=[["Windows","Linux","macOS","Network Devices","SaaS","IaaS"],["Windows","Linux","macOS","Network Devices","IaaS"]]
for aid,a,summary,plats in zip(analytic_ids,h["defense_candidates"]["detection_analytics"],summaries,platforms):
 data=[]
 for q in a["data_requirements"]:
  data.append({"source_type":q["source_type"],"name":q["name"],"channel":q.get("channel"),
               "required_fields":[re.sub(r"[^a-z0-9_.-]+","_",str(f).lower()).strip("_") for f in q["required_fields"]]})
 obj={"schema_version":"2.0.0","type":"detection-analytic","id":aid,"strategy_ref":"DET-000211",
   "name":a["name"],"summary":summary,"domains":["enterprise"],"platforms":plats,
   "logic":P(a["logic"]),"data_requirements":data,"observables":a["observables"],
   "correlation":a["correlation"],"false_positives":a["false_positives"],"blind_spots":a["blind_spots"],
   "tuning_guidance":a["tuning_guidance"],"evidence_refs":refs(a["evidence_keys"]),
   "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-27","modified":"2026-09-27","contributors":["Niji Matrix Research"],"reviewers":[]}}
 slug=a["key"].split("-NJA-")[-1].lower()
 (ROOT/"analytics"/f"{aid}-t1021-{slug}.yaml").write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
s=h["defense_candidates"]["detection_strategies"][0]
obj={"schema_version":"2.0.0","type":"detection-strategy","id":"DET-000211","name":s["name"],
 "summary":{"zh":"连接内部远程认证、目标会话和首个目标动作，并重建中继前的真实控制端。","en":"Join internal remote authentication, destination session, and first target action while reconstructing the true controller before an intermediary."},
 "description":{"paragraphs":[s["objective"],s["reason"]]},"detects_refs":["NJT-0183","NJS-0183-001","NJS-0183-002"],
 "domains":["enterprise"],"analytic_refs":analytic_ids,
 "evidence_refs":["REF-000842","REF-000843","REF-000844","REF-000845","REF-000846","REF-000847","REF-000848","REF-000377","REF-000598","REF-000604"],
 "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-27","modified":"2026-09-27","contributors":["Niji Matrix Research"],"reviewers":[]}}
(ROOT/"detections"/"DET-000211-t1021-session-action-lineage.yaml").write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
# Existing mitigation extensions.
for proposal in h["defense_candidates"]["mitigations"]:
 mid=proposal["mitigation_ref"];p=Path(glob.glob(str(ROOT/"mitigations"/f"{mid}-*.yaml"))[0]);d=yaml.safe_load(p.read_text())
 targets=["NJT-0183","NJS-0183-001"] if mid=="MIT-000052" else ["NJS-0183-002"]
 for target in targets:
  assert not any(a["target_ref"]==target for a in d["applications"])
  use=proposal["application_notes"]
  effect=proposal["expected_effect"]
  limit=proposal["limitations"]
  if target=="NJT-0183":
   use={"zh":use["zh"]+" 父级同时要求远程连接、目标会话与目标动作可连接。","en":use["en"]+" The parent additionally requires a join among remote connection, destination session, and target action."}
  d["applications"].append({"target_ref":target,"use":P(use),"expected_effect":P(effect),"limitations":P(limit)})
 for ref in refs(proposal["evidence_keys"]):
  if ref not in d["evidence_refs"]:d["evidence_refs"].append(ref)
 v=d["lifecycle"]["version"].split(".");d["lifecycle"].update(status="draft",version=f"{v[0]}.{int(v[1])+1}.0",modified="2026-09-27")
 p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120))
print("serialized T1021 strategy analytics and mitigation extensions")
