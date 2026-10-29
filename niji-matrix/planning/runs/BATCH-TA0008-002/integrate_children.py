#!/usr/bin/env python3
"""Serialize four independently supported Niji-native children, never ATT&CK children."""
from pathlib import Path
import re
import yaml
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
refs=yaml.safe_load((RUN/"integration-id-map.yaml").read_text())["references"]
content_1080=yaml.safe_load((RUN/"T1080-child-content-addendum.yaml").read_text())["children"]
content_1563=yaml.safe_load((RUN/"T1563-handoff.yaml").read_text())["proposed_subtechniques"]
SPECS=[
("NJS-0148-001","NJT-0148",content_1080[0],["CLM-000755"],["CASE-000203","CASE-000204"],["REF-000589","REF-000590","REF-000591","REF-000593","REF-000594","REF-000379","REF-000474","REF-000190"],"DET-000166","MIT-000152"),
("NJS-0148-002","NJT-0148",content_1080[1],["CLM-000756"],["CASE-000205"],["REF-000589","REF-000592","REF-000474","REF-000379","REF-000595"],"DET-000166","MIT-000152"),
("NJS-0151-001","NJT-0151",content_1563[0],["CLM-000767"],[],["REF-000613","REF-000614","REF-000615","REF-000616","REF-000370"],"DET-000170","MIT-000155"),
("NJS-0151-002","NJT-0151",content_1563[1],["CLM-000768"],["CASE-000211","CASE-000212"],["REF-000613","REF-000617","REF-000618","REF-000619","REF-000620","REF-000621","REF-000622","REF-000623","REF-000624","REF-000377"],"DET-000170","MIT-000155"),
]
LIMITS={
"NJS-0151-001":{"paragraphs":[
{"zh":"OpenSSH 规范直接证明同一已认证传输内可开新逻辑通道，USENIX 研究展示经运行中客户端增附通道的可行性；现无可核验的野外攻击 Case，故不能把该实现写成普遍或已证的行动者行为。SSH agent 转发签名用于建立新连接属于相邻认证材料边界，不能充当原连接的劫持证据。","en":"OpenSSH specifications establish new logical channels within one authenticated transport, and USENIX research demonstrates channel addition through a running client. No verifiable field intrusion Case is available, so the implementation cannot be described as prevalent or observed actor behavior. Forwarded SSH-agent signing used to establish a new connection belongs to an adjacent authentication-material boundary rather than proving takeover of the original transport."},
{"zh":"通道归因依赖服务器实际提供连接与通道标识，以及跳板的 ControlPath 或 ptrace 访问日志；多数普通 sshd 审计不能直接输出完整链。正常 ControlMaster 自动化也会复用连接，缺少本地控制者差异和目标后继结果时应只记低置信调查线索。","en":"Channel attribution depends on real connection and channel identifiers from the server and ControlPath or ptrace access logs on the jump host; ordinary sshd audit may not expose the full chain. Legitimate ControlMaster automation also reuses transports, so without a local controller difference and destination outcome retain only a low-confidence lead."}]},
"NJS-0151-002":{"paragraphs":[
{"zh":"Mandiant 汇总的 MAZE 现场直接记录 tscon 接管合法 RDP 会话，但没有逐个会话 ID 或事件序列。CrowdStrike 现场中 tscon 分支受阻，后来 RDS shadow 分支成功；两者不能合成一次成功的 tscon→shadow 接管过程，也不证明每次接管都没有用户提示。","en":"Mandiant's MAZE field synthesis directly records tscon takeover of legitimate RDP sessions but lacks per-session IDs and event sequences. In CrowdStrike's incident the tscon branch was blocked and a later RDS shadow branch succeeded; they cannot be collapsed into one successful tscon-to-shadow takeover or used to claim every takeover lacked user notice."},
{"zh":"4778/4779 与 4688 是否记录旧新客户端、命令行和同意状态取决于本地策略及传感器。帮助台支持、断线重连和合法共同控制可能同形；必须把原所有者、控制端变化、批准记录与目标结果连接后再归因，不能只用同一账户仍登录来判安全或恶意。","en":"Whether 4778, 4779, and 4688 preserve old and new clients, command lines, and consent state depends on local policy and sensors. Help-desk support, network reconnection, and legitimate co-control can look similar. Attribution requires joining original owner, controller change, approval, and target outcome rather than treating an account still logged on as either safe or malicious."}]}
}
def refmap(keys):
    out=[]
    for k in keys:
        v=k if k.startswith("REF-") else refs.get(k)
        if not v:
            assert k=="B8B-T1563-REF-RDP-POC",k
            continue
        if v not in out:out.append(v)
    return out
for cid,parent,c,claim_refs,case_refs,source_refs,det,mit in SPECS:
    mechanics=[]
    for m in c["stealth_mechanisms"]:
        evid=refmap(m["evidence_keys"])
        mechanics.append({"mechanism_ref":m["mechanism_ref"],"role":m["role"],
            "summary":{k:m["summary"][k].rstrip("。.!?；;") for k in ["zh","en"]},
            "analysis":m["analysis"],"evidence_refs":evid,"confidence":m["confidence"]})
    refset=source_refs.copy()
    for m in mechanics:
        for ref in m["evidence_refs"]:
            if ref not in refset:refset.append(ref)
    limits=(c.get("research") or {}).get("limitations")
    if limits:limits={"paragraphs":limits["paragraphs"]}
    else:limits=LIMITS[cid]
    obj={"schema_version":"2.0.0","type":"evasion-subtechnique","id":cid,
         "parent_ref":parent,"name":c["name"],"summary":c["summary"],"aliases":[],
         "lineage":{"attck_subtechnique_inherited":False},
         "definition_and_concept":c["definition_and_concept"],
         "stealth_characteristics":c["stealth_characteristics"],
         "scope_boundary_definition":c["scope_boundary_definition"],
         "application_scenarios_and_threat_model":c["application_scenarios_and_threat_model"],
         "stealth_mechanisms":mechanics,
         "defense":{"detections":{"coverage":"available","strategy_refs":[det]},
                    "mitigations":{"coverage":"available","mitigation_refs":[mit]}},
         "evidence":{"claim_refs":claim_refs,"case_refs":case_refs,"reference_refs":refset},
         "research":{"limitations":limits},
         "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-22","modified":"2026-09-22",
                      "contributors":["Niji Matrix Research"],"reviewers":[]}}
    slug=re.sub(r"[^a-z0-9]+","-",c["name"]["en"].lower()).strip("-")
    parent_dir=next((ROOT/"matrix"/"tactics"/"TA0008-lateral-movement"/"techniques").glob(parent+"-*"))
    path=parent_dir/"subtechniques"/f"{cid}-{slug}"/"subtechnique.yaml"
    if path.exists():raise RuntimeError(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized",len(SPECS),"Niji-native child drafts")
