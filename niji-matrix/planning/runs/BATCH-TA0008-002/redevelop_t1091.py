#!/usr/bin/env python3
"""Redevelop existing T1091 parent/children for both tactic outcomes."""
from pathlib import Path
import glob
import yaml
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
d=yaml.safe_load((RUN/"T1091-handoff.yaml").read_text())
p=Path(glob.glob(str(ROOT/"matrix"/"tactics"/"TA0001-initial-access"/"techniques"/"NJT-0058-*"/"technique.yaml"))[0])
parent=yaml.safe_load(p.read_text())
content=d["proposed_content"]
parent["name"]=content["name"]
parent["summary"]=content["summary"]
parent["aliases"]=["T1091","Replication Through Removable Media"]
parent["classification"]["tactic_refs"]=["TA0001","TA0008"]
for field in ["definition_and_concept","stealth_characteristics","scope_boundary_definition","application_scenarios_and_threat_model"]:
    parent[field]=content[field]
mechanics=[]
for m in content["stealth_mechanisms"]:
    evid=[x if x.startswith("REF-") else "REF-000596" for x in m["evidence_keys"]]
    mechanics.append({"mechanism_ref":m["mechanism_ref"],"role":m["role"],
        "summary":{k:m["summary"][k].rstrip("。.!?；;") for k in ["zh","en"]},
        "analysis":m["analysis"],"evidence_refs":list(dict.fromkeys(evid)),"confidence":m["confidence"]})
parent["stealth_mechanisms"]=mechanics
tax=content["proposed_subtechnique_taxonomy"]
parent["subtechnique_taxonomy"]={"narrative":{"paragraphs":[tax["narrative"]]},
    "coverage":"established","subtechnique_refs":["NJS-0058-001","NJS-0058-002"]}
parent["defense"]={"detections":{"coverage":"available","strategy_refs":["DET-000054","DET-000167"]},
                   "mitigations":{"coverage":"available","mitigation_refs":["MIT-000053"]}}
parent["evidence"]={"claim_refs":["CLM-000243","CLM-000215","CLM-000216","CLM-000758","CLM-000759"],
    "case_refs":["CASE-000109","CASE-000206"],
    "reference_refs":["REF-000091","REF-000105","REF-000106","REF-000301","REF-000475","REF-000596","REF-000597","REF-000598"]}
parent["research"]={"limitations":d["research"]["limitations"]}
parent["lifecycle"].update(status="draft",version="2.0.0",modified="2026-09-22")
p.write_text(yaml.safe_dump(parent,allow_unicode=True,sort_keys=False,width=120))
CHILD_INFO={
"NJS-0058-001":{"claims":["CLM-000215","CLM-000758"],"cases":["CASE-000109","CASE-000206"],
"limitations":{"paragraphs":[
{"zh":"Microsoft 的 Raspberry Robin 案例只直接证明接收侧品牌化 LNK 与用户触发，不能单独证明同一介质曾由该组织内 A 播种。ESET USBStealer 支持 A/B 样本传播模型，不能填补一宗现场的每次介质交接；“可能鼓励点击”也不是实测的用户心理因果。","en":"Microsoft's Raspberry Robin account directly proves branded LNKs and recipient-side user triggering, not that the same medium was seeded by host A within that organization. ESET USBStealer supports an A/B sample propagation model but cannot fill every media handoff in one field incident. Possible encouragement to click is not a measured psychological causal effect."},
{"zh":"合法 USB 快捷方式、离线安装器与自动运行配置可能同形。没有原介质内容、LNK 实际目标和 B 的进程谱系时只能记录可疑入口；管理员身份或系统二进制签名都不证明此次触发得到授权。","en":"Legitimate USB shortcuts, offline installers, and autorun settings may look similar. Without original media content, actual LNK target, and B process lineage, retain a suspicious-entry conclusion only. Administrator identity or a signed system binary does not authorize this trigger."}]}},
"NJS-0058-002":{"claims":["CLM-000216","CLM-000758","CLM-000759"],"cases":["CASE-000206"],
"limitations":{"paragraphs":[
{"zh":"Check Point 直接分析 LitterDrifter 的卷枚举、隐藏组件与 LNK 写入，但跨国样本提交不证明同一企业的 A/B 链。Microsoft 对 Raspberry Robin 播种模块与其他主机感染的结论为中等置信。自动播种与跨机时间分离的匿迹效果是条件性观察模型推断，不是所有样本均有的低慢行动者意图。","en":"Check Point directly analyzed LitterDrifter's drive enumeration, hidden component, and LNK writes, but cross-country sample submissions do not prove an A/B chain inside one enterprise. Microsoft assigned medium confidence to Raspberry Robin seeding and infection of other hosts. The stealth effect of automatic seeding and host-time separation is a conditional observation-model inference, not a low-and-slow actor intent shown for every sample."},
{"zh":"批量复制和隐藏文件修改也可能在 A 上形成显著峰值；合法离线补丁、盘初始化和备份恢复会产生相似写入。若 B 为完全隔离主机或介质 ID 不稳定，需要实物清单与检查站补证，不能凭 B 上已有文件追溯 A 的具体进程。","en":"Bulk copying and hidden-file changes may create a conspicuous spike on A. Legitimate offline patching, media initialization, and backup restore produce similar writes. If B is fully isolated or media IDs are unstable, use physical ledgers and inspection checkpoints rather than tracing a process on A merely from a file already present on B."}]}}
}
for c in d["proposed_subtechniques"]:
    cid=c["existing_ref"];info=CHILD_INFO[cid]
    cp=Path(glob.glob(str(p.parent/"subtechniques"/f"{cid}-*"/"subtechnique.yaml"))[0])
    child=yaml.safe_load(cp.read_text())
    child["name"]=c["name"];child["summary"]=c["summary"]
    for field in ["definition_and_concept","stealth_characteristics","scope_boundary_definition"]:
        child[field]=c[field]
    child["application_scenarios_and_threat_model"]={
        "application_scenarios":c["application_scenarios"],
        "threat_model":{"attacker_model":c["attacker_model"],"defender_model":c["defender_model"]}}
    cm=c["mechanisms"][0]
    evidence=[x if x.startswith("REF-") else "REF-000596" for x in cm["evidence_keys"]]
    child["stealth_mechanisms"]=[{"mechanism_ref":cm["mechanism_ref"],"role":"primary",
      "summary":{"zh":cm["causal_chain_zh"].split("，")[0].rstrip("。.!?；;"),
                 "en":cm["causal_chain_en"].split(",")[0].rstrip("。.!?；;")},
      "analysis":{"paragraphs":[{"zh":cm["causal_chain_zh"]+"目标端仍有介质接入、真实链接目标和后继进程可恢复该因果链。",
                                "en":cm["causal_chain_en"]+" Media insertion, actual link target, and successor processes remain available to reconstruct the chain."}]},
      "evidence_refs":list(dict.fromkeys(evidence)),"confidence":cm["confidence"]}]
    child["defense"]={"detections":{"coverage":"available","strategy_refs":["DET-000054","DET-000167"]},
                      "mitigations":{"coverage":"available","mitigation_refs":["MIT-000053"]}}
    child["evidence"]={"claim_refs":info["claims"],"case_refs":info["cases"],
        "reference_refs":["REF-000091","REF-000105","REF-000106","REF-000301","REF-000475","REF-000596","REF-000597","REF-000598"]}
    child["research"]={"limitations":info["limitations"]}
    child["lifecycle"].update(status="draft",version="2.0.0",modified="2026-09-22")
    cp.write_text(yaml.safe_dump(child,allow_unicode=True,sort_keys=False,width=120))
for cid,zh,en,evidence,mode,confidence in [
("CLM-000215","接收主机上的介质入口若以目录名、图标或品牌化 LNK 代替真实目标命令，会让恶意触发看似普通浏览；是否真的由同组织 A 播种需另证。","A media entry on the receiving host can use folder names, icons, or branded LNKs in place of the real target command so malicious triggering resembles ordinary browsing; seeding by host A in the same organization requires separate proof.",["REF-000105","REF-000106","REF-000596"],"strongly-inferred","medium"),
("CLM-000216","自动卷枚举与播种可在 A 上无逐盘人工操作地写入隐藏组件和诱导入口；A 写入与 B 后续执行的时空分离会增加单端短窗的来源重建成本。","Automatic volume enumeration and seeding can write hidden components and lures on A without manual work for each drive; separation between A writes and B later execution raises the origin-reconstruction cost of a short single-host view.",["REF-000105","REF-000106","REF-000596"],"strongly-inferred","medium")]:
    cp=Path(glob.glob(str(ROOT/"claims"/f"{cid}-*.yaml"))[0]);claim=yaml.safe_load(cp.read_text())
    claim.update(statement_zh=zh,statement_en=en,evidence_refs=evidence,evidence_mode=mode,confidence=confidence,status="draft")
    cp.write_text(yaml.safe_dump(claim,allow_unicode=True,sort_keys=False,width=120))
for cid,targets in {"CLM-000758":["NJT-0058","NJS-0058-001","NJS-0058-002"],
                    "CLM-000759":["NJT-0058","NJS-0058-002","DET-000167"]}.items():
    cp=Path(glob.glob(str(ROOT/"claims"/f"{cid}-*.yaml"))[0]);claim=yaml.safe_load(cp.read_text());claim["subject_refs"]=targets
    cp.write_text(yaml.safe_dump(claim,allow_unicode=True,sort_keys=False,width=120))
cp=Path(glob.glob(str(ROOT/"cases"/"CASE-000109-*.yaml"))[0]);case=yaml.safe_load(cp.read_text())
for target in ["NJT-0058","NJS-0058-001"]:
    if target not in case["subject_refs"]:case["subject_refs"].append(target)
case["status"]="draft"
cp.write_text(yaml.safe_dump(case,allow_unicode=True,sort_keys=False,width=120))
print("redeveloped NJT-0058, two NJS, two Claims and reused CASE-000109")
