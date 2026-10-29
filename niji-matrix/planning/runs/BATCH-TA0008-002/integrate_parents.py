#!/usr/bin/env python3
"""Serialize four independently reviewed TA0008 parent techniques."""
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
idmap=yaml.safe_load((RUN/"integration-id-map.yaml").read_text())
REF=idmap["references"]
def refs(keys):
    out=[]
    for key in keys:
        if key.startswith("REF-"):ref=key
        else:
            ref=REF.get(key)
            if ref is None:
                # The RDP demonstration is a research-only candidate. Field
                # reports and Microsoft implementation sources remain.
                assert key=="B8B-T1563-REF-RDP-POC",key
                continue
        if ref not in out:out.append(ref)
    return out
NAMES={
"T1080":({"zh":"污染共享内容","en":"Taint Shared Content"},"taint-shared-content"),
"T1210":({"zh":"利用远程服务","en":"Exploitation of Remote Services"},"internal-remote-service-exploitation"),
"T1534":({"zh":"内部定向钓鱼","en":"Internal Spearphishing"},"internal-spearphishing"),
"T1563":({"zh":"远程服务会话劫持","en":"Remote Service Session Hijacking"},"remote-session-hijacking"),
}
SOURCE={
"T1080":["REF-000589","REF-000590","REF-000591","REF-000592","REF-000593","REF-000594","REF-000595","REF-000474","REF-000379","REF-000190"],
"T1210":["REF-000599","REF-000591","REF-000600","REF-000601","REF-000602","REF-000603","REF-000604","REF-000605","REF-000377","REF-000598","REF-000243"],
"T1534":["REF-000606","REF-000607","REF-000608","REF-000590","REF-000609","REF-000610","REF-000611","REF-000612","REF-000090","REF-000068"],
"T1563":["REF-000613","REF-000614","REF-000615","REF-000616","REF-000617","REF-000618","REF-000619","REF-000620","REF-000621","REF-000622","REF-000623","REF-000624","REF-000377","REF-000370"],
}
TAX_T1080={"narrative":{"paragraphs":[
{"zh":"原生子项按被攻击者改写的共享对象关系划分。既有共享对象语义原位污染保持原路径或文件身份，却改变其宏、模板、脚本或可执行内容，防守需连接旧新版本与异机消费；共享导航入口目标替身保持用户看到的目录入口与后来正常内容，却把首次点击绑定到额外命令，防守需连接隐藏原目录、替身目标与目标端命令。二者可同现，但一个改内容，一个改入口绑定，痕迹与分析数据不同。","en":"Native children partition the shared-object relationship changed by the attacker. In-Place Semantic Taint keeps the original path or file identity while changing macro, template, script, or executable content, requiring old-to-new version and cross-host consumption joins. Shared Navigation-Entry Target Substitution keeps the folder entry and later expected content visible while binding the first click to another command, requiring joins among hidden original directory, substitute target, and destination command. They can coexist, but one changes content and the other entry binding, producing different traces and analytics."},
{"zh":"Office、安装包、仓库、快捷方式和 SMB 是实现媒介而非分类依据；打开后的正常体验跨两个子项，不另拆一项。低频等待和仓库专用轴没有独立意图、消费结果与防御差异证据，留在研究层。两项子技术均不继承 ATT&CK 子技术，完成门仍是另一内部消费者的真实可控结果。","en":"Office files, installers, repositories, shortcuts, and SMB are implementation media rather than partition keys. A normal experience after opening can span both children and is not a third axis. Low-frequency waiting and repository-specific hypotheses lack separate evidence of intent, consumer outcome, and defense difference and remain in research. Neither child inherits an ATT&CK sub-technique, and both still require a real controllable result at another internal consumer."}]},"coverage":"established","subtechnique_refs":["NJS-0148-001","NJS-0148-002"]}
for attack,(name,slug) in NAMES.items():
    d=yaml.safe_load((RUN/f"{attack}-handoff.yaml").read_text())
    content=d["proposed_content"]
    mechanism=[]
    for m in content["stealth_mechanisms"]:
        summary={lang:m["summary"][lang].rstrip("。.!?；;") for lang in ["zh","en"]}
        mr=refs(m.get("evidence_keys",[]))
        assert mr,(attack,m["mechanism_ref"])
        mechanism.append({"mechanism_ref":m["mechanism_ref"],"role":m["role"],
                          "summary":summary,"analysis":m["analysis"],
                          "evidence_refs":mr,"confidence":m["confidence"]})
    if attack=="T1080":tax=TAX_T1080
    else:
        raw=content["subtechnique_taxonomy"]
        tax={"narrative":raw["narrative"],"coverage":raw["coverage"],
             "subtechnique_refs":idmap["subtechniques"][attack]}
    allrefs=SOURCE[attack].copy()
    for m in mechanism:
        for ref in m["evidence_refs"]:
            if ref not in allrefs:allrefs.append(ref)
    mits=[idmap["mitigations"][attack]]
    if attack=="T1534":mits.append("MIT-000036")
    obj={"schema_version":"2.0.0","type":"technique","id":idmap["techniques"][attack],
         "name":name,"summary":content["summary"],"aliases":[attack],
         "classification":{"tactic_refs":["TA0008"],"origin":{"kind":"attack-adapted",
         "source_attack_id":attack,"source_attack_version":"19.1"},
         "decision_ref":f"DEC-TA0008-{attack}"},
         "definition_and_concept":content["definition_and_concept"],
         "stealth_characteristics":content["stealth_characteristics"],
         "scope_boundary_definition":content["scope_boundary_definition"],
         "application_scenarios_and_threat_model":content["application_scenarios_and_threat_model"],
         "stealth_mechanisms":mechanism,"subtechnique_taxonomy":tax,
         "defense":{"detections":{"coverage":"available","strategy_refs":[idmap["strategies"][attack]]},
                    "mitigations":{"coverage":"available","mitigation_refs":mits}},
         "evidence":{"claim_refs":idmap["claims"][attack],"case_refs":idmap["cases"][attack],
                     "reference_refs":allrefs},
         "research":{"limitations":d["research"]["limitations"]},
         "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-22",
                      "modified":"2026-09-22","contributors":["Niji Matrix Research"],"reviewers":[]}}
    path=ROOT/"matrix"/"tactics"/"TA0008-lateral-movement"/"techniques"/f"{obj['id']}-{slug}"/"technique.yaml"
    if path.exists():raise RuntimeError(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized",len(NAMES),"reviewed parent drafts")
