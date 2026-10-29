#!/usr/bin/env python3
"""Serialize the primary-reviewed T1021 evidence and defense library."""
from pathlib import Path
import re
import yaml
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
h=yaml.safe_load((RUN/"T1021-handoff.yaml").read_text())
REFMAP={
"B8C-T1021-REF-ATTACK19":"REF-000842",
"B8C-T1021-REF-MS-ATTACK-MODEL":"REF-000843",
"B8C-T1021-REF-MANDIANT-FIN11":"REF-000844",
"B8C-T1021-REF-MANDIANT-RDP-BASELINE":"REF-000845",
"B8C-T1021-REF-MANDIANT-RDP-TUNNEL":"REF-000846",
"B8C-T1021-REF-MS-EXCHANGE-TUNNEL":"REF-000847",
"B8C-T1021-REF-MS-MDE-LOGON":"REF-000848",
}
META={
"B8C-T1021-REF-ATTACK19":("远程服务，技术 T1021","Remote Services, Technique T1021","MITRE ATT&CK","official-documentation",None,"固定 Enterprise 19.1 父行为、TA0008 和八个实现子项；不直接支持 Niji 子项或防御。"),
"B8C-T1021-REF-MS-ATTACK-MODEL":("Microsoft 横向移动攻击建模与关联","Microsoft Attack Modeling for Finding and Stopping Lateral Movement","Microsoft Threat Intelligence","threat-report","2020-06-10","支持多种原生服务的正常业务外观、PARINACOTA 现场行为与跨主机关联；不证明所有原生服务使用都有匿迹意图。"),
"B8C-T1021-REF-MANDIANT-FIN11":("Mandiant FIN11 技术 OT 红队演练","Mandiant Red Team Emulates FIN11 Tactics to Control OT Servers","Mandiant","vendor-report","2022-07-26","授权红队在真实环境中的评估，支持管理路径与后台流量混合；不是 FIN11 真实入侵或通用失效率。"),
"B8C-T1021-REF-MANDIANT-RDP-BASELINE":("Mandiant RDP 关系基线","Mandiant Establishing a Baseline for Remote Desktop Protocol","Mandiant","incident-report","2018-04-26","支持按来源、账户与目标关系识别异常 RDP；字段和阈值不能直接复制到所有远程服务。"),
"B8C-T1021-REF-MANDIANT-RDP-TUNNEL":("Mandiant RDP 隧道与管理跳板转发","Mandiant Bypassing Network Restrictions Through RDP Tunneling","Mandiant","incident-report","2019-01-24","记录 Plink、netsh portproxy、跳板路由与 localhost 痕迹；未公开完整逐事件 PID、双侧 flow、目标 LogonId 和命令。"),
"B8C-T1021-REF-MS-EXCHANGE-TUNNEL":("Exchange 攻击中的 Plink 与 SSH 隧道","Defending Exchange Servers Under Attack","Microsoft Defender Security Research Team","incident-report","2020-06-24","支持攻击者以 Plink/SSH 隧道、窃取凭据和 RDP 建立访问；未公开完整三主机遥测。"),
"B8C-T1021-REF-MS-MDE-LOGON":("Microsoft Defender XDR DeviceLogonEvents 表","DeviceLogonEvents Table in the Advanced Hunting Schema","Microsoft","official-documentation",None,"支持设备、账户、协议、LogonId、远端设备与 IP 字段；这些字段本身不证明恶意、关系贴合或中继。"),
}
sources={x["key"]:x for x in h["library_candidates"]["references"]}
for key,rid in REFMAP.items():
    x=sources[key];zh,en,publisher,stype,published,note=META[key]
    obj={"schema_version":"1.0.0","type":"reference","id":rid,"title_zh":zh,"title_en":en,
      "source_type":stype,"identifiers":{"doi":None,"rfc":None,"arxiv":None,
      "attack_id":"T1021" if key.endswith("ATTACK19") else None,"other":[]},
      "authors":[],"publisher":publisher,"published":published,"url":x["url"],"accessed":"2026-09-27",
      "locator":x.get("locator"),"archive_url":None,"credibility":"high","notes_zh":note,
      "notes_en":(x.get("limit") or {}).get("en",note)}
    slug=re.sub(r"[^a-z0-9]+","-",key.removeprefix("B8C-T1021-REF-").lower()).strip("-")
    (ROOT/"references"/f"{rid}-t1021-{slug}.yaml").write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
# Claims
claim_ids=["CLM-000900","CLM-000901","CLM-000902","CLM-000903","CLM-000904"]
subjects={
"CLM-000900":["NJT-0183"],"CLM-000901":["NJT-0183","NJS-0183-001"],
"CLM-000902":["NJT-0183","NJS-0183-002"],"CLM-000903":["NJT-0183","DET-000211"],
"CLM-000904":["NJT-0183"]}
types=["technique-relevance","subtechnique-existence","subtechnique-existence","detection","technique-boundary"]
modes=["directly-observed","strongly-inferred","strongly-inferred","strongly-inferred","strongly-inferred"]
conf=["high","medium","medium","high","high"]
claim_src=[
["REF-000842","REF-000843","REF-000289","REF-000845"],
["REF-000843","REF-000844","REF-000278","REF-000845"],
["REF-000846","REF-000847","REF-000377","REF-000614"],
["REF-000377","REF-000598","REF-000604","REF-000848","REF-000845","REF-000846"],
["REF-000842","REF-000843","REF-000845","REF-000848"]]
for cid,x,typ,mode,confidence,eref in zip(claim_ids,h["library_candidates"]["claims"],types,modes,conf,claim_src):
    st=x["proposition"]
    obj={"schema_version":"1.0.0","type":"claim","id":cid,"claim_type":typ,
      "statement_zh":st["zh"],"statement_en":st["en"],"subject_refs":subjects[cid],
      "evidence_refs":eref,"evidence_mode":mode,"confidence":confidence,"status":"draft"}
    (ROOT/"claims"/f"{cid}-t1021-{x['key'].split('-CLM-')[-1].lower()}.yaml").write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
# Cases
case_specs=[
("CASE-000263",h["library_candidates"]["cases"][0],["NJT-0183"],["REF-000843"]),
("CASE-000264",h["library_candidates"]["cases"][1],["NJT-0183","NJS-0183-001"],["REF-000844"]),
("CASE-000265",h["library_candidates"]["cases"][2],["NJT-0183","NJS-0183-002"],["REF-000846","REF-000847"])]
for cid,x,targets,eref in case_specs:
    obj={"schema_version":"1.0.0","type":"case","id":cid,"name_zh":x["name"]["zh"],"name_en":x["name"]["en"],
      "actor_or_campaign":x["actor_or_campaign"],"subject_refs":targets,
      "description_zh":x["observed_facts"]["zh"]+" "+x["cannot_claim"]["zh"],
      "description_en":x["observed_facts"]["en"]+" "+x["cannot_claim"]["en"],
      "time_range":None,"target_sectors_zh":[],"target_sectors_en":[],
      "evidence_refs":eref,"confidence":x["confidence"],"status":"draft"}
    (ROOT/"cases"/f"{cid}-t1021-{x['key'].split('-CASE-')[-1].lower()}.yaml").write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized T1021 references claims and cases")
