"""Serialize five reviewed admission decisions and four new parent techniques."""

from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
ORDER = ("T1571", "T1572", "T1573", "T1659", "T1665")
H = {tid: yaml.safe_load((RUN / f"{tid}-research-handoff.yaml").read_text()) for tid in ORDER}
MAP = yaml.safe_load((RUN / "canonical-id-map.yaml").read_text())
IDS = MAP["ids"]
TEMP = MAP["temporary_keys"]
DATE = "2026-10-05"
LIFE = {"status": "review", "version": "1.0.0", "created": DATE, "modified": DATE, "contributors": ["Niji Matrix Research"], "reviewers": []}
SLUGS = {
    "T1571": "port-expectation-semantic-mismatch",
    "T1572": "nested-protocol-session-tunneling",
    "T1573": "adversary-keyed-c2-protection",
    "T1665": "selective-c2-infrastructure-exposure",
}
ATTACK_NAMES = {
    "T1571": ("非标准端口", "Non-Standard Port"),
    "T1572": ("协议隧道", "Protocol Tunneling"),
    "T1573": ("加密通道", "Encrypted Channel"),
    "T1659": ("内容注入", "Content Injection"),
    "T1665": ("隐藏基础设施", "Hide Infrastructure"),
}
NAMES = {
    "T1571": {"zh": "端口预期语义错配", "en": "Port-Expectation Semantic Mismatch"},
    "T1572": {"zh": "嵌套协议会话隧道", "en": "Nested-Protocol Session Tunneling"},
    "T1573": {"zh": "攻击者密钥控制通道保护", "en": "Adversary-Keyed C2 Protection"},
    "T1665": {"zh": "选择性 C2 基础设施暴露", "en": "Selective C2 Infrastructure Exposure"},
}
SCOPE_NOTES = {
    "T1571": {"zh": "要求实际语义、当地端口服务预期、防守差分与后继 C2 四层证据；现有公开案例不证明每个目标的本地策略效果。", "en": "Require actual semantics, local port-service expectation, a defensive differential, and successor C2; public cases do not establish every victim's local policy effect."},
    "T1572": {"zh": "要求内层语义、外层承载、解封装或重组关系及后继 C2/访问结果；单一代理、VPN 或加密连接不足。", "en": "Require inner semantics, outer carriage, a decapsulation or reassembly relationship, and successor C2 or access outcome; a proxy, VPN, or encrypted connection alone is insufficient."},
    "T1573": {"zh": "仅纳入承载协议之外的攻击者附加密码层；密钥/材料恢复、接收端解密和命令或结果需连接。", "en": "Include only an attacker-added cryptographic layer beyond the carrier protocol, joining key or material recovery, receiver decryption, and a command or result."},
    "T1659": {"zh": "复用 NJT-0052，分别要求初始入口或已受控主机经注入路径持续取得任务与结果；竞速响应的 C2 用途仍为假设。", "en": "Reuse NJT-0052 with distinct initial-entry or continuing task-and-result outcomes on an already compromised host; C2 use of racing responses remains a hypothesis."},
    "T1665": {"zh": "要求攻击者控制的前端/监听器产生请求或观察者差分且合格受害端有真实 C2 结果；时窗轴暂缓独立子项。", "en": "Require an actor-controlled front or listener to create request or observer differentials with a real C2 outcome for a qualified victim; defer the temporal-exposure child."},
}
DEFENSE = {
    "T1571": (["DET-000257"], ["MIT-000227"]),
    "T1572": (["DET-000258"], ["MIT-000172", "MIT-000200"]),
    "T1573": (["DET-000259", "DET-000260"], ["MIT-000228", "MIT-000229"]),
    "T1659": (["DET-000051", "DET-000261"], ["MIT-000050", "MIT-000230"]),
    "T1665": (["DET-000262"], ["MIT-000231"]),
}

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

def refs(keys):
    return list(dict.fromkeys(k if str(k).startswith("REF-") else TEMP[k] for k in keys or []))

def all_refs(tid):
    handoff = H[tid]
    results = list(IDS[tid]["references"].values())
    results.extend(x for x in handoff.get("existing_library_reuse", {}).get("reference_refs", []) if isinstance(x, str))
    results.append("REF-000085" if tid == "T1659" else "REF-000625")
    for mechanism in handoff["proposed_content"]["stealth_mechanisms"]:
        results.extend(refs(mechanism.get("evidence_keys")))
    return list(dict.fromkeys(results))

def mechanism(raw):
    summary = {lang: raw["summary"][lang].rstrip("。.!?；; ") for lang in ("zh", "en")}
    confidence = raw.get("confidence", "medium")
    if confidence == "medium-high":
        confidence = "medium"
    return {"mechanism_ref": raw["mechanism_ref"], "role": raw["role"], "summary": summary,
            "analysis": deepcopy(raw["analysis"]), "evidence_refs": refs(raw.get("evidence_keys")), "confidence": confidence}

def paragraphs_join(section, lang):
    return "\n\n".join(p[lang] for p in section["paragraphs"])

def decision(tid):
    h = H[tid]
    rec = h["recommendation"]
    zh_name, en_name = ATTACK_NAMES[tid]
    confidence = "medium" if tid == "T1571" else rec.get("confidence", "high")
    value = {
        "schema_version": "1.1.0", "type": "technique-decision", "id": f"DEC-TA0011-{tid}",
        "tactic_ref": "TA0011",
        "candidate": {"source_type": "attack", "source_attack_id": tid, "source_attack_version": "19.1", "name_en": en_name, "name_zh": zh_name},
        "decision": rec["decision"], "rationale_zh": paragraphs_join(rec["rationale"], "zh"),
        "rationale_en": paragraphs_join(rec["rationale"], "en"),
        "scope_notes_zh": SCOPE_NOTES[tid]["zh"], "scope_notes_en": SCOPE_NOTES[tid]["en"],
        "gap_statement_zh": None, "gap_statement_en": None,
        "original_attack_subtechniques_imported": False, "resulting_technique_ref": IDS[tid]["parent"],
        "evidence_refs": all_refs(tid), "confidence": confidence,
        "review": {"status": "review", "authors": ["Niji Matrix Research"], "reviewers": [],
                   "review_notes_zh": "五份独立研究交接齐全后完成准入与跨技术收敛；机器验收后保持 review 等待人工领域评审。",
                   "review_notes_en": "Admission and cross-technique convergence followed all five independent handoffs; status remains review after machine acceptance pending human domain review."},
    }
    save(ROOT / "matrix/tactics/TA0011-command-and-control/decisions" / f"DEC-TA0011-{tid}.yaml", value)

def parent(tid):
    h = H[tid]
    content = h["proposed_content"]
    app = deepcopy(content["application_scenarios_and_threat_model"])
    if "threat_model" not in app and "threat_model" in content:
        app["threat_model"] = deepcopy(content["threat_model"])
    if tid == "T1571":
        attacker = app["threat_model"]["attacker_model"]
        defender = attacker.pop("defender_model")
        app["threat_model"]["defender_model"] = defender
    raw_tax = content["subtechnique_taxonomy"]
    coverage = raw_tax["coverage"]
    if coverage == "two-formal-one-deferred":
        coverage = "established"
    taxonomy = {"narrative": deepcopy(raw_tax["narrative"]), "coverage": coverage,
                "subtechnique_refs": list(IDS[tid]["children"].values())}
    det, mit = DEFENSE[tid]
    name = NAMES[tid]
    value = {
        "schema_version": "2.0.0", "type": "technique", "id": IDS[tid]["parent"],
        "name": name, "summary": deepcopy(content["summary"]),
        "aliases": [ATTACK_NAMES[tid][1]],
        "classification": {"tactic_refs": ["TA0011"],
                           "origin": {"kind": "attack-retained" if H[tid]["recommendation"]["decision"] == "retain" else "attack-adapted",
                                      "source_attack_id": tid, "source_attack_version": "19.1"},
                           "decision_ref": f"DEC-TA0011-{tid}"},
        "definition_and_concept": deepcopy(content["definition_and_concept"]),
        "stealth_characteristics": deepcopy(content["stealth_characteristics"]),
        "scope_boundary_definition": deepcopy(content["scope_boundary_definition"]),
        "application_scenarios_and_threat_model": app,
        "stealth_mechanisms": [mechanism(m) for m in content["stealth_mechanisms"]],
        "subtechnique_taxonomy": taxonomy,
        "defense": {"detections": {"coverage": "available", "strategy_refs": det},
                    "mitigations": {"coverage": "available", "mitigation_refs": mit}},
        "evidence": {"claim_refs": list(IDS[tid]["claims"].values()),
                     "case_refs": list(IDS[tid]["cases"].values()), "reference_refs": all_refs(tid)},
        "research": {"limitations": deepcopy(h.get("research", {}).get("limitations") or h.get("research_limitations"))},
        "lifecycle": deepcopy(LIFE),
    }
    path = ROOT / "matrix/tactics/TA0011-command-and-control/techniques" / f"{value['id']}-{SLUGS[tid]}" / "technique.yaml"
    save(path, value)

for tid in ORDER:
    decision(tid)
    if tid != "T1659":
        parent(tid)
print("Serialized five decisions and four new parent techniques")
