#!/usr/bin/env python3
"""Write five independent admission decisions after primary convergence."""
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
IDS={"T1080":"NJT-0148","T1091":"NJT-0058","T1210":"NJT-0149","T1534":"NJT-0150","T1563":"NJT-0151"}
SCOPE={
"T1080":("只在受控共享对象或导航绑定发生恶意变化、另一内部消费者实际触发并出现可控结果时成立；单纯投递归 T1570，内部主动消息归 T1534。Office、LNK 或代码仓库是媒介而非 NJS。",
"Require a malicious change to a controlled shared object or navigation binding, actual triggering by another internal consumer, and a controllable outcome. Mere delivery belongs to T1570 and proactively sent internal messages to T1534. Office, LNK, and code repositories are media rather than NJS."),
"T1091":("复用 NJT-0058 时，TA0008 须有已控内部 A 播种同一可移动介质、不同内部 B 接入并实际产生攻击者动作；只有 A 写入、B 挂载或首次从外部带入介质不够。两项 NJS 按伪装入口与自动播种变量沿用，不导入 ATT&CK 子项。",
"When reusing NJT-0058, TA0008 requires controlled internal A to seed the same removable medium, distinct internal B to insert it, and an actual attacker action on B. A write, B mount, or first delivery from outside alone is insufficient. The two NJS remain partitioned by disguised entry and automatic seeding, not ATT&CK children."),
"T1210":("须有内网来源对另一系统的服务漏洞触发及可证目标受控结果；开放端口、脆弱版本、扫描、利用尝试或服务崩溃分别只是条件或线索。与 T1021 新会话、T1563 既有会话接管及 T1570 文件到达分开。",
"Require an internal source, exploitation of a remote service on another system, and a verifiable controlled target outcome. An open port, vulnerable version, scan, exploit attempt, or crash is only a prerequisite or signal. Distinguish T1021 new sessions, T1563 takeover of existing sessions, and T1570 file arrival."),
"T1534":("须有受陷内部发件主体、对另一内部主体的行动诱导、收件者动作及第二账户或主机结果；只发信为尝试。共享对象污染归 T1080，原始外部钓鱼归 TA0001。按主题归档反馈的稳定变量已由 NJS-0111-001 拥有，不重复建子项。",
"Require a compromised internal sender, action-bearing lure to another internal principal, recipient action, and a second account or host outcome; sending alone is an attempt. Shared-object taint belongs to T1080 and original external phishing to TA0001. Subject-matched feedback archiving is already owned by NJS-0111-001 and is not duplicated as a child."),
"T1563":("须指出既有认证传输或交互会话、非原所有者的附着动作与目标结果；复用 agent 凭据后新建连接属于 T1550 或 T1021。T1563.001/.002 仅作实现宽度；NJS 依通道增附或控制端重绑定划分。",
"Identify an existing authenticated transport or interactive session, attachment by a controller other than its original owner, and a target outcome. Creating a new connection with reused agent credentials belongs to T1550 or T1021. T1563.001 and .002 are implementation breadth only; NJS separate channel addition from controller rebinding.")
}
EVIDENCE={"T1080":["REF-000589","REF-000590","REF-000591","REF-000592"],
"T1091":["REF-000091","REF-000105","REF-000106","REF-000596"],
"T1210":["REF-000599","REF-000591","REF-000600","REF-000602"],
"T1534":["REF-000606","REF-000607","REF-000608","REF-000590"],
"T1563":["REF-000613","REF-000614","REF-000616","REF-000617","REF-000618","REF-000624"]}
for attack,njt in IDS.items():
    d=yaml.safe_load((RUN/f"{attack}-handoff.yaml").read_text())
    rec=d["recommendation"]
    assert rec["decision"] in {"retain","adapt","exclude"}
    paras=rec["rationale"]["paragraphs"]
    candidate=d["candidate"]["name"]
    obj={"schema_version":"1.0.0","type":"technique-decision","id":f"DEC-TA0008-{attack}",
         "tactic_ref":"TA0008","candidate":{"source_type":"attack","source_attack_id":attack,
         "source_attack_version":"19.1","name_en":candidate["en"],"name_zh":candidate["zh"]},
         "decision":rec["decision"],"rationale_zh":"\n\n".join(x["zh"] for x in paras),
         "rationale_en":"\n\n".join(x["en"] for x in paras),
         "scope_notes_zh":SCOPE[attack][0],"scope_notes_en":SCOPE[attack][1],
         "gap_statement_zh":None,"gap_statement_en":None,
         "original_attack_subtechniques_imported":False,"resulting_technique_ref":njt,
         "evidence_refs":EVIDENCE[attack],"confidence":rec["confidence"],
         "review":{"status":"draft","authors":["Niji Matrix Research"],"reviewers":[],
         "review_notes_zh":"已完成独立准入，正式内容与质量门禁仍在批次集成中。",
         "review_notes_en":"Independent admission is complete; formal content and quality gates are in batch integration."}}
    path=ROOT/"matrix"/"tactics"/"TA0008-lateral-movement"/"decisions"/f"DEC-TA0008-{attack}.yaml"
    if path.exists():raise RuntimeError(path)
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized",len(IDS),"admission decisions")
