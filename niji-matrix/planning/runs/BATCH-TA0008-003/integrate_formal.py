#!/usr/bin/env python3
"""Serialize primary-reviewed T1021 decision, parent, and two native children."""
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
# Decision
r=h["recommendation"]["rationale"]["paragraphs"]
decision={"schema_version":"1.0.0","type":"technique-decision","id":"DEC-TA0008-T1021","tactic_ref":"TA0008",
 "candidate":{"source_type":"attack","source_attack_id":"T1021","source_attack_version":"19.1","name_en":"Remote Services","name_zh":"远程服务"},
 "decision":"adapt","rationale_zh":"\n\n".join(x["zh"] for x in r),"rationale_en":"\n\n".join(x["en"] for x in r),
 "scope_notes_zh":"要求已可用主体或权限通过正常认证/授权路径建立新的内部远程连接，并连接目标会话或动作。协议、端口、厂商及 ATT&CK 子项不构成 NJS；漏洞利用、旧会话接管、部署 job、云命令和文件到达分别由相邻对象承担。",
 "scope_notes_en":"Require an already usable principal or authority to create a fresh internal remote connection through ordinary authentication and authorization and join it to a destination session or action. Protocol, port, vendor, and ATT&CK child do not define NJS; exploitation, takeover of an old session, deployment jobs, cloud commands, and file arrival remain adjacent.",
 "gap_statement_zh":None,"gap_statement_en":None,"original_attack_subtechniques_imported":False,
 "resulting_technique_ref":"NJT-0183","evidence_refs":["REF-000842","REF-000843","REF-000844","REF-000845","REF-000846","REF-000847"],
 "confidence":"high","review":{"status":"draft","authors":["Niji Matrix Research"],"reviewers":[],
 "review_notes_zh":"独立准入和两遍 taxonomy 已完成，正式质量门禁正在集成。","review_notes_en":"Independent admission and two-pass taxonomy are complete; formal quality gates are in integration."}}
path=ROOT/"matrix"/"tactics"/"TA0008-lateral-movement"/"decisions"/"DEC-TA0008-T1021.yaml"
path.write_text(yaml.safe_dump(decision,allow_unicode=True,sort_keys=False,width=120))
# Parent
pc=h["proposed_content"];mechanics=[]
for m in pc["stealth_mechanisms"]:
 mechanics.append({"mechanism_ref":m["mechanism_ref"],"role":m["role"],
 "summary":{k:m["summary"][k].rstrip("。.!?；;") for k in ["zh","en"]},"analysis":m["analysis"],
 "evidence_refs":refs(m["evidence_keys"]),"confidence":m["confidence"]})
parent={"schema_version":"2.0.0","type":"technique","id":"NJT-0183","name":pc["name"],"summary":pc["summary"],
 "aliases":["Remote Services","T1021"],"classification":{"tactic_refs":["TA0008"],
 "origin":{"kind":"attack-adapted","source_attack_id":"T1021","source_attack_version":"19.1"},"decision_ref":"DEC-TA0008-T1021"},
 "definition_and_concept":pc["definition_and_concept"],"stealth_characteristics":pc["stealth_characteristics"],
 "scope_boundary_definition":pc["scope_boundary_definition"],"application_scenarios_and_threat_model":pc["application_scenarios_and_threat_model"],
 "stealth_mechanisms":mechanics,"subtechnique_taxonomy":{"narrative":pc["subtechnique_taxonomy"]["narrative"],
 "coverage":"established","subtechnique_refs":["NJS-0183-001","NJS-0183-002"]},
 "defense":{"detections":{"coverage":"available","strategy_refs":["DET-000211"]},
 "mitigations":{"coverage":"available","mitigation_refs":["MIT-000052","MIT-000172"]}},
 "evidence":{"claim_refs":["CLM-000900","CLM-000901","CLM-000902","CLM-000903","CLM-000904","CLM-000507"],
 "case_refs":["CASE-000263","CASE-000264","CASE-000265","CASE-000104"],
 "reference_refs":["REF-000842","REF-000843","REF-000844","REF-000845","REF-000846","REF-000847","REF-000848","REF-000278","REF-000289","REF-000377","REF-000598","REF-000604","REF-000614"]},
 "research":{"limitations":h["research"]["limitations"]},
 "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-27","modified":"2026-09-27","contributors":["Niji Matrix Research"],"reviewers":[]}}
pdir=ROOT/"matrix"/"tactics"/"TA0008-lateral-movement"/"techniques"/"NJT-0183-remote-service-lateral-access"
pdir.mkdir(parents=True,exist_ok=True);(pdir/"technique.yaml").write_text(yaml.safe_dump(parent,allow_unicode=True,sort_keys=False,width=120))
# Children
child_specs=[
("NJS-0183-001",h["proposed_subtechniques"][0],["CLM-000901"],["CASE-000264"],"MIT-000052"),
("NJS-0183-002",h["proposed_subtechniques"][1],["CLM-000902"],["CASE-000265"],"MIT-000172")]
for cid,c,claims,cases,mit in child_specs:
 ms=[]
 for m in c["stealth_mechanisms"]:
  ms.append({"mechanism_ref":m["mechanism_ref"],"role":m["role"],
  "summary":{k:m["summary"][k].rstrip("。.!?；;") for k in ["zh","en"]},"analysis":m["analysis"],
  "evidence_refs":refs(m["evidence_keys"]),"confidence":m["confidence"]})
 srefs=refs(c["evidence_keys"])
 for m in ms:
  for ref in m["evidence_refs"]:
   if ref not in srefs:srefs.append(ref)
 child={"schema_version":"2.0.0","type":"evasion-subtechnique","id":cid,"parent_ref":"NJT-0183",
 "name":c["name"],"summary":c["summary"],"aliases":[],"lineage":{"attck_subtechnique_inherited":False},
 "definition_and_concept":c["definition_and_concept"],"stealth_characteristics":c["stealth_characteristics"],
 "scope_boundary_definition":c["scope_boundary_definition"],"application_scenarios_and_threat_model":c["application_scenarios_and_threat_model"],
 "stealth_mechanisms":ms,"defense":{"detections":{"coverage":"available","strategy_refs":["DET-000211"]},
 "mitigations":{"coverage":"available","mitigation_refs":[mit]}},
 "evidence":{"claim_refs":claims,"case_refs":cases,"reference_refs":srefs},"research":{"limitations":c["limitations"]},
 "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-27","modified":"2026-09-27","contributors":["Niji Matrix Research"],"reviewers":[]}}
 slug=re.sub(r"[^a-z0-9]+","-",c["name"]["en"].lower()).strip("-")
 cp=pdir/"subtechniques"/f"{cid}-{slug}"/"subtechnique.yaml";cp.parent.mkdir(parents=True,exist_ok=True)
 cp.write_text(yaml.safe_dump(child,allow_unicode=True,sort_keys=False,width=120))
# Extend service-execution Claim/Case only at unchanged semantic identity.
for object_id,folder in [("CLM-000507","claims"),("CASE-000104","cases")]:
 p=Path(glob.glob(str(ROOT/folder/f"{object_id}-*.yaml"))[0]);d=yaml.safe_load(p.read_text())
 if "NJT-0183" not in d["subject_refs"]:d["subject_refs"].append("NJT-0183")
 if "lifecycle" in d:d["lifecycle"]["status"]="draft"
 else:d["status"]="draft"
 p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=120))
print("serialized T1021 decision parent and two children")
