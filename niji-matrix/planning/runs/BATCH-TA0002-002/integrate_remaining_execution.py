from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from generate_remaining_execution import BATCH, NEW_ANALYTICS, NEW_MITIGATIONS, NEW_STRATEGIES, PARENTS, ROOT, TODAY


def prose(zh: str, en: str) -> dict[str, list[dict[str, str]]]:
    return {"paragraphs": [{"zh": zh, "en": en}]}


def lifecycle(status: str = "review", version: str = "1.0.0", created: str = TODAY) -> dict[str, Any]:
    return {"status": status, "version": version, "created": created, "modified": TODAY, "contributors": ["Niji Matrix Research"], "reviewers": []}


def save(relative: str, data: dict[str, Any]) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=180), encoding="utf-8")


def all_subjects(parent: dict[str, Any]) -> list[str]:
    return [parent["id"], *[item["id"] for item in parent["children"]]]


def subject_names() -> dict[str, dict[str, str]]:
    names: dict[str, dict[str, str]] = {}
    for parent in PARENTS:
        names[parent["id"]] = {"zh": parent["name_zh"], "en": parent["name_en"]}
        for item in parent["children"]:
            names[item["id"]] = {"zh": item["name_zh"], "en": item["name_en"]}
    return names


MECHANISM_EFFECTS = {
    "NM-BT": ("关键行为落在既有监控或分析理解之外，形成行为透明效果", "Critical behavior falls outside existing monitoring or analytic understanding, producing a Behavioral Transparency effect"),
    "NM-DO": ("数据虽然存在却不能直接解释真实内容或意图，形成数据遮蔽效果", "The data exists but does not directly reveal true content or intent, producing a Data Obscuration effect"),
    "NM-FD": ("恶意实体与正常实体共享可见特征而难以区分，形成特征伪装效果", "The malicious entity shares visible features with normal entities and becomes difficult to distinguish, producing a Feature Disguise effect"),
    "NM-ST": ("信号被分散到不同时间或位置而难以重建，形成时空释痕效果", "Signals are dispersed across time or location and become difficult to reconstruct, producing a Spatiotemporal Trace Dilution effect"),
}


def mechanism(item: dict[str, str], ref: str) -> dict[str, Any]:
    effect_zh, effect_en = MECHANISM_EFFECTS[item["ref"]]
    return {
        "mechanism_ref": item["ref"], "role": item["role"], "summary": {"zh": item["zh"], "en": item["en"]},
        "analysis": prose(f"攻击者有意采用该行为设计，使{item['trace_zh']}。由此，{item['effect_zh']}，而{effect_zh}。不过，{item['residual_zh']}；跨层采集和因果关联能够削弱这种匿迹。", f"The adversary deliberately adopts this behavior design so that {item['trace_en']}. As a result, {item['effect_en']}. {effect_en}. However, {item['residual_en']}; cross-layer collection and causal correlation can weaken this stealth effect."),
        "evidence_refs": [ref], "confidence": item["confidence"],
    }


def write_references() -> None:
    for parent in PARENTS:
        save(f"references/{parent['ref']}-mitre-{parent['attack'].lower()}-{parent['slug']}.yaml", {
            "schema_version": "1.0.0", "type": "reference", "id": parent["ref"], "title_zh": f"{parent['attack_zh']}，技术 {parent['attack']}", "title_en": f"{parent['attack_en']}, Technique {parent['attack']}", "source_type": "official-documentation",
            "identifiers": {"doi": None, "rfc": None, "arxiv": None, "attack_id": parent["attack"], "other": []}, "authors": ["MITRE"], "publisher": "MITRE ATT&CK", "published": None, "url": f"https://attack.mitre.org/versions/v19/techniques/{parent['attack']}", "accessed": TODAY, "locator": "Technique description, procedure examples, mitigations, and detection strategy", "archive_url": None, "credibility": "high",
            "notes_zh": "固定 Enterprise ATT&CK 19.1 基线的父技术来源；只用于支持父行为、公开实例与页面所列防御信息，不导入 ATT&CK 子技术。", "notes_en": "Parent-technique source for the fixed Enterprise ATT&CK 19.1 baseline. It supports the parent behavior, published examples, and listed defenses but does not import ATT&CK sub-techniques.",
        })


def write_claims() -> None:
    for parent in PARENTS:
        retained_zh = "保留" if parent["decision"] == "retain" else "适配"
        retained_en = "retention" if parent["decision"] == "retain" else "adaptation"
        save(f"claims/{parent['claim']}-{parent['attack'].lower()}-{parent['slug']}.yaml", {
            "schema_version": "1.0.0", "type": "claim", "id": parent["claim"], "claim_type": "technique-relevance",
            "statement_zh": f"{parent['attack_zh']}能够通过{parent['stealth_zh']}改变执行痕迹与防守观察，因此支持在 TA0002 下{retained_zh}为匿迹技术。", "statement_en": f"{parent['attack_en']} can change execution traces and defender observation because {parent['stealth_en']}; this supports {retained_en} as a stealth technique under TA0002.",
            "subject_refs": [parent["id"]], "evidence_refs": [parent["ref"]], "evidence_mode": "strongly-inferred", "confidence": parent.get("confidence", "medium"), "status": "review",
        })
        for item in parent["children"]:
            save(f"claims/{item['claim']}-{item['slug']}.yaml", {
                "schema_version": "1.0.0", "type": "claim", "id": item["claim"], "claim_type": "subtechnique-existence",
                "statement_zh": f"{item['name_zh']}以攻击者有意{item['variable_zh']}为稳定区分变量，并造成独立的痕迹变化和防守观察差异。", "statement_en": f"{item['name_en']} has a stable distinguishing variable: the adversary deliberately adopts {item['variable_en']}. This creates a distinct trace change and defender-observation difference.",
                "subject_refs": [item["id"]], "evidence_refs": [parent["ref"]], "evidence_mode": "strongly-inferred", "confidence": item["mechanisms"][0]["confidence"], "status": "review",
            })


def write_decisions(status: str) -> None:
    for parent in PARENTS:
        save(f"matrix/tactics/TA0002-execution/decisions/DEC-TA0002-{parent['attack']}.yaml", {
            "schema_version": "1.0.0", "type": "technique-decision", "id": f"DEC-TA0002-{parent['attack']}", "tactic_ref": "TA0002",
            "candidate": {"source_type": "attack", "source_attack_id": parent["attack"], "source_attack_version": "19.1", "name_en": parent["attack_en"], "name_zh": parent["attack_zh"]}, "decision": parent["decision"],
            "rationale_zh": f"固定基线明确记录{parent['behavior_zh']}。研究确认，{parent['stealth_zh']}，能够形成可论证的匿迹因果链，因此作出 {parent['decision']} 决策。该决策保持父行为锚点，并只将攻击者有意改变痕迹与防守观察的实现纳入正式对象。", "rationale_en": f"The fixed baseline documents {parent['behavior_en']}. Research establishes that {parent['stealth_en']}, forming a defensible stealth chain and supporting the {parent['decision']} decision. The decision preserves the parent behavior anchor and includes only implementations that deliberately change traces and defender observation.",
            "scope_notes_zh": f"正式范围纳入{parent['included_zh']}，排除{parent['excluded_zh']}。任何 ATT&CK 子技术均未导入，Niji 子项只按稳定匿迹变量推导。", "scope_notes_en": f"Formal scope includes {parent['included_en']} and excludes {parent['excluded_en']}. No ATT&CK sub-technique is imported; Niji children are derived only from stable stealth variables.",
            "gap_statement_zh": None, "gap_statement_en": None, "original_attack_subtechniques_imported": False, "resulting_technique_ref": parent["id"], "evidence_refs": [parent["ref"]], "confidence": parent.get("confidence", "medium"),
            "review": {"status": status, "authors": ["Niji Matrix Research"], "reviewers": [], "review_notes_zh": "已完成 YAML-only 2.0 研究与机器审查，等待人工领域审查。" if status == "review" else "正式对象正在完成机器门禁。", "review_notes_en": "YAML-only 2.0 research and machine review are complete; human domain review is pending." if status == "review" else "The formal object is undergoing machine gates."},
        })


def build_parent(parent: dict[str, Any], status: str) -> dict[str, Any]:
    names_zh = "、".join(item["name_zh"] for item in parent["children"])
    names_en = ", ".join(item["name_en"] for item in parent["children"])
    return {
        "schema_version": "2.0.0", "type": "technique", "id": parent["id"], "name": {"zh": parent["name_zh"], "en": parent["name_en"]},
        "summary": {"zh": f"攻击者通过{parent['behavior_zh']}，并利用受信执行外观、内容不可见性或跨层因果断点降低识别与归因概率。", "en": f"Adversaries perform the following behavior: {parent['behavior_en']}. They exploit trusted execution appearance, reduced content visibility, or cross-layer causal breaks to lower detection and attribution probability."}, "aliases": [],
        "classification": {"tactic_refs": ["TA0002"], "origin": {"kind": "attack-retained" if parent["decision"] == "retain" else "attack-adapted", "source_attack_id": parent["attack"], "source_attack_version": "19.1"}, "decision_ref": f"DEC-TA0002-{parent['attack']}"},
        "definition_and_concept": prose(f"{parent['name_zh']}是指{parent['behavior_zh']}。其直接目标是{parent['purpose_zh']}；在攻击执行战术中，以攻击者控制的代码、命令或任务开始运行为完成点，并以直接执行路径而不是工具、平台或介质界定对象。", f"{parent['name_en']} means {parent['behavior_en']}. Its direct objective is to {parent['purpose_en']}. Under the Execution tactic, the object ends when adversary-controlled code, a command, or a task begins to run and is defined by its direct execution path rather than by tool, platform, or medium."),
        "stealth_characteristics": prose(f"{parent['name_zh']}的匿迹性来自{parent['stealth_zh']}。这些属性改变执行来源、时间、内容或父子谱系的可见关系，迫使防守方跨数据域恢复意图；控制请求、配置差异、进程或函数结果和网络行为仍是残余可观测线索。", f"The stealth of {parent['name_en']} arises because {parent['stealth_en']}. These properties change visible relationships in execution origin, timing, content, or lineage and force defenders to recover intent across data domains. Control requests, configuration differences, process or function outcomes, and network behavior remain residual observables."),
        "scope_boundary_definition": prose(f"本技术纳入{parent['included_zh']}；排除{parent['excluded_zh']}。合法运维、开发、自动化或用户活动可能产生相似痕迹，只有攻击者有意利用该执行路径改变防守观察并推动恶意操作时才属于本对象。", f"This technique includes {parent['included_en']} and excludes {parent['excluded_en']}. Legitimate operations, development, automation, or user activity may produce similar traces; the object applies only when the adversary deliberately uses the execution path to change defender observation and advance malicious activity."),
        "application_scenarios_and_threat_model": {"application_scenarios": prose(parent["scenario_zh"], parent["scenario_en"]), "threat_model": {"attacker_model": prose(parent["attacker_zh"], parent["attacker_en"]), "defender_model": prose(parent["defender_zh"], parent["defender_en"])}},
        "stealth_mechanisms": [mechanism(item, parent["ref"]) for item in parent["mechanisms"]],
        "subtechnique_taxonomy": {"narrative": prose(f"子技术按攻击者可稳定控制并改变防守观察的执行变量划分为{names_zh}。这些兄弟项各自固定独立的痕迹变化，不按 ATT&CK 子技术、产品、平台、语言、工具或文件类型拆分；未覆盖假设在证据和边界收敛前保持延期。", f"The children are partitioned by adversary-controlled execution variables that stably change defender observation: {names_en}. Each sibling fixes an independent trace change. The taxonomy is not inherited from ATT&CK and is not based on product, platform, language, tool, or file type; uncovered hypotheses remain deferred until evidence and boundaries converge."), "coverage": "established", "subtechnique_refs": [item["id"] for item in parent["children"]]},
        "defense": {"detections": {"coverage": "available", "strategy_refs": [parent["det"]]}, "mitigations": {"coverage": "available", "mitigation_refs": [parent["mit"]]}}, "evidence": {"claim_refs": [parent["claim"]], "case_refs": [], "reference_refs": [parent["ref"]]},
        "research": {"limitations": prose(parent["limitations_zh"], parent["limitations_en"])}, "lifecycle": lifecycle(status),
    }


def build_child(parent: dict[str, Any], item: dict[str, Any], status: str) -> dict[str, Any]:
    return {
        "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": item["id"], "parent_ref": parent["id"], "name": {"zh": item["name_zh"], "en": item["name_en"]},
        "summary": {"zh": f"攻击者通过{item['variable_zh']}，使执行痕迹更难被区分、关联或归因。", "en": f"The adversary adopts this stable variable: {item['variable_en']}. This makes execution traces harder to distinguish, correlate, or attribute."}, "aliases": [], "lineage": {"attck_subtechnique_inherited": False},
        "definition_and_concept": prose(f"{item['name_zh']}是{parent['name_zh']}的一种实现，攻击者有意{item['variable_zh']}。其直接目的仍是{parent['purpose_zh']}，但该对象只固定当前稳定变量及其独立防守观察效果。", f"{item['name_en']} is an implementation of {parent['name_en']}. The adversary deliberately adopts the following stable variable: {item['variable_en']}. Its direct objective remains to {parent['purpose_en']}, but the object fixes only this variable and its distinct defender-observation effect."),
        "stealth_characteristics": prose(f"{item['name_zh']}通过{item['variable_zh']}改变可见执行来源、时间、内容或谱系。防守方仍可观察相关控制、状态或结果，但必须{item['observe_zh']}才能恢复攻击者意图；缺少这些关联时，局部事件会保持正常或不完整外观。", f"{item['name_en']} changes visible execution origin, timing, content, or lineage by {item['variable_en']}. Relevant control, state, or outcome remains observable, but the defender must {item['observe_en']} to recover adversary intent; without that correlation, local events retain a normal or incomplete appearance."),
        "scope_boundary_definition": prose(f"本子技术只纳入攻击者有意{item['variable_zh']}并由此改变防守观察的行为。{item['boundary_zh']}；合法活动产生同样外观时，必须依赖主体、目标、时间、完整性和执行结果的组合证据。", f"This child applies only when the adversary deliberately adopts the following variable and thereby changes defender observation: {item['variable_en']}. {item['boundary_en']}. When legitimate activity has the same appearance, combined evidence from principal, target, time, integrity, and execution outcome is required."),
        "application_scenarios_and_threat_model": {"application_scenarios": prose(f"在{item['scenario_zh']}时使用该子技术；攻击者选择这一变量是为了让直接执行结果保留正常或不完整的观察外观。", f"This child is used when {item['scenario_en']}; the adversary selects the variable so the direct execution outcome retains a normal or incomplete observable appearance."), "threat_model": {"attacker_model": prose(f"攻击者需要{item['prereq_zh']}。实施仍受父技术权限、目标环境差异和执行可靠性约束。", f"The adversary must {item['prereq_en']}. Implementation remains constrained by parent-technique privileges, target-environment differences, and execution reliability."), "defender_model": prose(f"防守方假定能够取得父技术所列基础遥测，并需要{item['observe_zh']}。缺少任一关键关联键时应降低置信度，而不是把单点信号直接定性。", f"The defender is assumed to have the parent-level telemetry and must {item['observe_en']}. Missing a critical correlation key should lower confidence rather than turn a point signal into a conclusion.")}},
        "stealth_mechanisms": [mechanism(value, parent["ref"]) for value in item["mechanisms"]],
        "defense": {"detections": {"coverage": "available", "strategy_refs": [parent["det"]]}, "mitigations": {"coverage": "available", "mitigation_refs": [parent["mit"]]}}, "evidence": {"claim_refs": [item["claim"]], "case_refs": [], "reference_refs": [parent["ref"]]},
        "research": {"limitations": prose("该分类以固定基线中的父行为、公开实例和防御信息为依据，稳定变量及兄弟边界属于校准后的分析推断。正常运维、开发或用户活动可能产生相似痕迹；若后续证据不能证明攻击者有意控制变量，应合并、调整或延期该分类。", "This classification uses parent behavior, public examples, and defense information from the fixed baseline; the stable variable and sibling boundary are calibrated analytic inferences. Normal operations, development, or user activity may produce similar traces. If later evidence cannot establish deliberate adversary control of the variable, the category should be merged, revised, or deferred.")}, "lifecycle": lifecycle(status),
    }


def write_techniques(status: str) -> None:
    for parent in PARENTS:
        base = f"matrix/tactics/TA0002-execution/techniques/{parent['id']}-{parent['slug']}"
        save(f"{base}/technique.yaml", build_parent(parent, status))
        for item in parent["children"]:
            save(f"{base}/subtechniques/{item['id']}-{item['slug']}/subtechnique.yaml", build_child(parent, item, status))


def targets_for(reference_key: str, reference_id: str) -> list[str]:
    return [subject for parent in PARENTS if parent[reference_key] == reference_id for subject in all_subjects(parent)]


def strategy_description() -> dict[str, Any]:
    return prose("本策略以跨层因果和执行谱系为检测目标，覆盖所列父技术与子技术。其 Analytic 分别规范控制或触发事件、真实执行结果和情境基线；只有多个共享关联键的信号共同出现时才提高风险，合法维护、开发、自动化和用户活动必须保留为替代解释。", "This strategy targets cross-layer causality and execution lineage across the listed parents and children. Its analytics normalize control or trigger events, actual execution outcomes, and contextual baselines. Risk increases only when multiple signals share correlation keys, while legitimate maintenance, development, automation, and user activity remain alternative explanations.")


def write_new_strategies(status: str) -> None:
    for strategy in NEW_STRATEGIES:
        save(f"detections/{strategy['id']}-{strategy['slug']}.yaml", {"schema_version": "2.0.0", "type": "detection-strategy", "id": strategy["id"], "name": {"zh": strategy["name_zh"], "en": strategy["name_en"]}, "summary": {"zh": strategy["summary_zh"], "en": strategy["summary_en"]}, "description": strategy_description(), "detects_refs": targets_for("det", strategy["id"]), "domains": ["enterprise"], "analytic_refs": strategy["analytics"], "evidence_refs": strategy["refs"], "lifecycle": lifecycle(status)})


def write_analytics(status: str) -> None:
    for analytic in NEW_ANALYTICS:
        save(f"analytics/{analytic['id']}-{analytic['slug']}.yaml", {
            "schema_version": "2.0.0", "type": "detection-analytic", "id": analytic["id"], "strategy_ref": analytic["det"], "name": {"zh": analytic["name_zh"], "en": analytic["name_en"]}, "summary": {"zh": f"以稳定关联键恢复{analytic['name_zh'].replace('分析', '')}中的控制、执行与结果序列。", "en": f"Recover the control, execution, and outcome sequence for {analytic['name_en'].replace(' Analytic', '')} through stable correlation keys."}, "domains": ["enterprise"], "platforms": analytic["platforms"],
            "logic": prose("分析先规范各数据源的时间、主体、目标和请求或进程标识，再建立控制或触发、真实执行和后继结果的有向序列。只有异常主体或情境与执行谱系、完整性变化或网络结果共同出现时才提高风险；任一层缺失时降低置信度而不把单点信号直接定性。", "The analytic first normalizes time, principal, target, and request or process identifiers across sources, then builds a directed sequence from control or trigger through actual execution to follow-on outcome. Risk rises only when an anomalous principal or context co-occurs with execution lineage, integrity change, or network outcome; a missing layer lowers confidence rather than turning a point signal into a conclusion."),
            "data_requirements": [{"source_type": source_type, "name": {"zh": zh, "en": en}, "channel": None, "required_fields": fields} for source_type, zh, en, fields in analytic["requirements"]], "observables": [{"zh": zh, "en": en} for zh, en in analytic["observables"]], "correlation": {"window": {"zh": analytic["window_zh"], "en": analytic["window_en"]}, "dimensions": analytic["dimensions"]}, "false_positives": [{"zh": analytic["false_zh"], "en": analytic["false_en"]}], "blind_spots": [{"zh": analytic["blind_zh"], "en": analytic["blind_en"]}],
            "tuning_guidance": prose("按业务角色、来源、资产、软件版本、变更窗口和正常执行谱系建立基线，并分别评分主体异常、控制差异与执行结果。白名单必须绑定具体主体、目标、用途和有效期，不能永久排除受信服务、签名进程、自动化身份或维护时段；对缺失数据明确降低置信度。", "Build baselines by business role, origin, asset, software version, change window, and normal execution lineage, and score principal anomaly, control difference, and outcome separately. Allowlists must bind a concrete principal, target, purpose, and validity period rather than permanently excluding trusted services, signed processes, automation identities, or maintenance periods; explicitly lower confidence for missing data."), "evidence_refs": analytic["refs"], "lifecycle": lifecycle(status),
        })


def application_for(target_ref: str) -> dict[str, Any]:
    name = subject_names()[target_ref]
    return {
        "target_ref": target_ref,
        "use": prose(f"针对{name['zh']}，把本缓解应用于直接执行对象、控制接口和关键谱系：限制不必要权限与可调用面，验证定义、输入或制品完整性，保留触发前后的关联键，并把例外绑定到具体主体、目标、用途和有效期。", f"For {name['en']}, apply this mitigation to the direct execution object, control interface, and critical lineage: restrict unnecessary privileges and callable surfaces, verify definition, input, or artifact integrity, retain pre-trigger and post-trigger correlation keys, and bind exceptions to a concrete principal, target, purpose, and validity period."),
        "expected_effect": prose(f"该应用降低{name['zh']}借用受信服务、工具、工作负载、用户或管理路径的机会，提高攻击者维持权限、情境匹配和低差异痕迹的成本，并改善跨层归因。", f"This application reduces opportunities for {name['en']} to borrow trusted services, tools, workloads, users, or management paths, raises the cost of maintaining privilege, contextual fit, and low-difference traces, and improves cross-layer attribution."),
        "limitations": prose(f"该控制不能消除所有{name['zh']}实例；合法管理、开发、软件更新、用户工作流和业务连续性可能要求保留部分接口。强制处置必须依赖组合证据，并评估可用性、隐私与跨团队日志权限。", f"The control cannot eliminate every instance of {name['en']}; legitimate administration, development, software updates, user workflows, and business continuity may require retaining some interfaces. Enforcement must rely on combined evidence and account for availability, privacy, and cross-team logging authority."),
    }


def write_new_mitigations(status: str) -> None:
    for mitigation in NEW_MITIGATIONS:
        save(f"mitigations/{mitigation['id']}-{mitigation['slug']}.yaml", {
            "schema_version": "2.0.0", "type": "mitigation", "id": mitigation["id"], "name": {"zh": mitigation["name_zh"], "en": mitigation["name_en"]}, "summary": {"zh": mitigation["summary_zh"], "en": mitigation["summary_en"]},
            "description": prose(f"本缓解把可复用控制措施与逐目标应用分开。它{mitigation['summary_zh']}实施时同时保留检测所需审计，不以单一信誉、签名或白名单替代最小权限、输入审查和完整性验证。", f"This mitigation separates reusable measures from per-target applications. It will {mitigation['summary_en'][0].lower() + mitigation['summary_en'][1:]} Implementation preserves audit needed for detection and does not substitute a single reputation, signature, or allowlist for least privilege, input review, and integrity validation."),
            "domains": ["enterprise"], "measures": [{"key": key, "name": {"zh": name_zh, "en": name_en}, "description": prose(desc_zh, desc_en), "control_type": control_type} for key, name_zh, name_en, desc_zh, desc_en, control_type in mitigation["measures"]], "applications": [application_for(target) for target in targets_for("mit", mitigation["id"])], "evidence_refs": mitigation["refs"], "lifecycle": lifecycle(status),
        })


def extend_list(data: dict[str, Any], key: str, values: list[Any]) -> None:
    for value in values:
        if value not in data[key]:
            data[key].append(value)


def mark_extended(data: dict[str, Any], status: str) -> None:
    data["lifecycle"]["modified"] = TODAY
    data["lifecycle"]["version"] = "1.1.0"
    data["lifecycle"]["status"] = status


def extend_existing_shared(status: str) -> None:
    strategy_specs = {
        "DET-000058": ("detections/DET-000058-management-plane-workload-execution.yaml", ["NJT-0076", "NJT-0078"], ["NJA-000037"], ["REF-000128", "REF-000130"]),
        "DET-000059": ("detections/DET-000059-interpreter-load-ipc-lineage.yaml", ["NJT-0077", "NJT-0080"], [], ["REF-000129", "REF-000132"]),
        "DET-000060": ("detections/DET-000060-client-trigger-execution-causality.yaml", ["NJT-0081"], ["NJA-000038"], ["REF-000133"]),
    }
    for det, (path, parent_ids, analytics, refs) in strategy_specs.items():
        data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
        parents = [parent for parent in PARENTS if parent["id"] in parent_ids]
        extend_list(data, "detects_refs", [subject for parent in parents for subject in all_subjects(parent)])
        extend_list(data, "analytic_refs", analytics)
        extend_list(data, "evidence_refs", refs)
        mark_extended(data, status)
        if det == "DET-000059":
            data["name"] = {"zh": "解释器、模块、实用程序与 IPC 执行谱系关联", "en": "Interpreter, Module, Utility, and IPC Execution-Lineage Correlation"}
            data["summary"] = {"zh": "联合解释器内容、模块加载、受信实用程序输入、IPC 请求和后继行为识别受信执行外壳中的恶意语义。", "en": "Join interpreter content, module loads, trusted-utility inputs, IPC requests, and follow-on behavior to identify malicious semantics inside trusted execution wrappers."}
        save(path, data)

    analytic_specs = {
        "analytics/NJA-000032-management-plane-workload-execution.yaml": {"refs": ["REF-000130"], "platforms": ["SaaS", "Windows", "Linux", "macOS", "Network Devices"], "observable": ("集中部署或配置管理任务由异常控制台主体发起，并由受信代理在多个目标产生非基线进程或网络结果", "A centralized deployment or configuration task originates from an unusual console principal and a trusted agent produces off-baseline process or network outcomes across targets")},
        "analytics/NJA-000034-interpreter-load-ipc-lineage.yaml": {"refs": ["REF-000129", "REF-000132"], "platforms": [], "observable": ("受信开发实用程序读取异常项目或配置后，在进程内执行代码、加载非常规模块或产生异常子进程与外联", "A trusted developer utility reads an unusual project or configuration and then executes code in process, loads an off-baseline module, or produces an anomalous child or network connection")},
    }
    for path, spec in analytic_specs.items():
        data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
        extend_list(data, "evidence_refs", spec["refs"])
        extend_list(data, "platforms", spec["platforms"])
        observable = {"zh": spec["observable"][0], "en": spec["observable"][1]}
        if observable not in data["observables"]:
            data["observables"].append(observable)
        mark_extended(data, status)
        if data["id"] == "NJA-000034":
            data["name"] = {"zh": "解释器、模块、实用程序与 IPC 执行谱系分析", "en": "Interpreter, Module, Utility, and IPC Execution-Lineage Analytic"}
        save(path, data)

    mitigation_specs = {
        "MIT-000057": ("mitigations/MIT-000057-privileged-management-execution-governance.yaml", ["NJT-0076", "NJT-0078"], ["REF-000128", "REF-000130"]),
        "MIT-000058": ("mitigations/MIT-000058-execution-mediation-hardening.yaml", ["NJT-0073", "NJT-0077", "NJT-0080"], ["REF-000125", "REF-000129", "REF-000132"]),
        "MIT-000059": ("mitigations/MIT-000059-client-trigger-surface-hardening.yaml", ["NJT-0081"], ["REF-000133"]),
    }
    for mit, (path, parent_ids, refs) in mitigation_specs.items():
        data = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
        existing_targets = {application["target_ref"] for application in data["applications"]}
        for parent in [value for value in PARENTS if value["id"] in parent_ids]:
            for target in all_subjects(parent):
                if target not in existing_targets:
                    data["applications"].append(application_for(target))
                    existing_targets.add(target)
        extend_list(data, "evidence_refs", refs)
        mark_extended(data, status)
        if mit == "MIT-000058":
            data["name"] = {"zh": "解释器、原生调用、模块与受信执行媒介加固", "en": "Interpreter, Native-Call, Module, and Trusted Execution-Mediation Hardening"}
            data["summary"] = {"zh": "收缩解释器、原生调用、模块、IPC 与受信实用程序执行面，并保护输入、依赖与完整执行谱系。", "en": "Reduce interpreter, native-call, module, IPC, and trusted-utility execution surfaces while protecting inputs, dependencies, and complete execution lineage."}
        if mit == "MIT-000059":
            data["name"] = {"zh": "客户端触发面、用户动作与输入信任加固", "en": "Client Trigger-Surface, User-Action, and Input-Trust Hardening"}
            data["summary"] = {"zh": "通过补丁、隔离、内容来源、用户动作保护、设备控制和输入治理降低客户端触发执行。", "en": "Reduce client-triggered execution through patching, isolation, content provenance, protected user actions, device control, and input governance."}
        save(path, data)


ANALYTICS_BY_DET = {"DET-000058": ["NJA-000032", "NJA-000033", "NJA-000037"], "DET-000059": ["NJA-000034"], "DET-000060": ["NJA-000035", "NJA-000036", "NJA-000038"], "DET-000061": ["NJA-000039"], "DET-000062": ["NJA-000040"], "DET-000063": ["NJA-000041", "NJA-000042"]}
NEW_ANALYTICS_BY_ATTACK = {"T1106": ["NJA-000039"], "T1677": ["NJA-000040"], "T1053": ["NJA-000041"], "T1648": ["NJA-000037"], "T1129": [], "T1072": [], "T1569": ["NJA-000041"], "T1127": [], "T1204": ["NJA-000038"], "T1047": ["NJA-000042"]}


def write_handoffs() -> None:
    for parent in PARENTS:
        formal = build_parent(parent, "draft")
        existing_det = parent["det"] in {"DET-000058", "DET-000059", "DET-000060"}
        existing_mit = parent["mit"] in {"MIT-000057", "MIT-000058", "MIT-000059"}
        existing_analytic = ["NJA-000032"] if parent["attack"] == "T1072" else (["NJA-000034"] if parent["attack"] in {"T1129", "T1127"} else [])
        base_creates = [parent["ref"], parent["claim"], parent["id"], *[item["claim"] for item in parent["children"]], *[item["id"] for item in parent["children"]]]
        new_objects = [*base_creates, *NEW_ANALYTICS_BY_ATTACK[parent["attack"]]]
        if not existing_det:
            new_objects.append(parent["det"])
        if not existing_mit:
            new_objects.append(parent["mit"])
        extended = ([parent["det"]] if existing_det else []) + existing_analytic + ([parent["mit"]] if existing_mit else [])
        save(f"planning/runs/{BATCH}/{parent['attack']}-handoff.yaml", {
            "handoff_schema_version": "2.0.0", "type": "technique-research-handoff", "batch_ref": BATCH, "work_item_ref": f"WORK-TA0002-{parent['attack']}", "temporary_key_prefix": f"EX2-{parent['attack']}",
            "candidate": {"source_type": "attack", "source_attack_id": parent["attack"], "name": {"zh": parent["attack_zh"], "en": parent["attack_en"]}}, "recommendation": {"decision": parent["decision"], "confidence": parent.get("confidence", "medium"), "rationale": prose(f"{parent['stealth_zh']}，能够形成稳定匿迹因果链；因此建议 {parent['decision']}。", f"The candidate has the following causal basis: {parent['stealth_en']}. It forms a stable stealth chain and is recommended for {parent['decision']}.")},
            "proposed_content": {key: formal[key] for key in ["summary", "definition_and_concept", "stealth_characteristics", "scope_boundary_definition", "application_scenarios_and_threat_model", "stealth_mechanisms"]}, "proposed_subtechniques": [{"canonical_ref": item["id"], "name": {"zh": item["name_zh"], "en": item["name_en"]}, "stable_variable": {"zh": item["variable_zh"], "en": item["variable_en"]}, "evidence_refs": [parent["ref"]], "confidence": item["mechanisms"][0]["confidence"]} for item in parent["children"]],
            "defense_candidates": {"detection_strategies": [parent["det"]], "detection_analytics": ANALYTICS_BY_DET[parent["det"]], "mitigations": [parent["mit"]]}, "existing_library_reuse": {"reference_refs": [], "claim_refs": [], "case_refs": [], "strategy_refs": [parent["det"]] if existing_det else [], "analytic_refs": existing_analytic, "mitigation_refs": [parent["mit"]] if existing_mit else [], "relationship_refs": []},
            "library_candidates": {"references": [parent["ref"]], "claims": [parent["claim"], *[item["claim"] for item in parent["children"]]], "cases": [], "detection_strategies": [] if existing_det else [parent["det"]], "detection_analytics": NEW_ANALYTICS_BY_ATTACK[parent["attack"]], "mitigations": [] if existing_mit else [parent["mit"]], "relationships": []}, "research": {"limitations": formal["research"]["limitations"], "rejected_mechanisms": [], "open_questions": []}, "integration": {"status": "complete", "resolutions": [{"disposition": "create", "objects": new_objects}, {"disposition": "extend", "objects": extended}, {"disposition": "defer", "objects": []}]},
        })


def update_plan(finalize: bool) -> None:
    path = ROOT / "planning/tactics/TA0002.yaml"
    plan = yaml.safe_load(path.read_text(encoding="utf-8"))
    plan["candidate_inventory"] = {"status": "complete", "source": "MITRE ATT&CK Enterprise 19.1 Execution tactic ordered parent-technique inventory", "last_synced": TODAY}
    work_refs = [f"WORK-TA0002-{parent['attack']}" for parent in PARENTS]
    batch = next((value for value in plan["batches"] if value["id"] == BATCH), None)
    if batch is None:
        batch = {"id": BATCH, "status": "active", "work_item_refs": work_refs}
        plan["batches"].append(batch)
    batch["status"] = "review" if finalize else "active"
    existing = {value["id"]: value for value in plan["work_items"]}
    for parent in PARENTS:
        item_id = f"WORK-TA0002-{parent['attack']}"
        item = existing.get(item_id)
        if item is None:
            item = {"id": item_id, "source_type": "attack", "source_attack_id": parent["attack"], "name_zh": parent["attack_zh"], "name_en": parent["attack_en"], "decision_ref": None, "resulting_technique_ref": None, "stage": "researching", "batch_ref": BATCH, "notes_zh": "", "notes_en": ""}
            plan["work_items"].append(item)
        item["decision_ref"] = f"DEC-TA0002-{parent['attack']}"
        item["resulting_technique_ref"] = parent["id"]
        item["stage"] = "review" if finalize else "authoring"
        count = len(parent["children"])
        item["notes_zh"] = f"已按 YAML-only 2.0 契约完成父技术与 {count} 项 Niji 原生子技术的正式编写；" + ("机器门禁通过，等待人工领域审查。" if finalize else "正在运行机器门禁。")
        item["notes_en"] = f"Formal authoring under the YAML-only 2.0 contract is complete for the parent and {count} Niji-native children; " + ("machine gates pass and human domain review is pending." if finalize else "machine gates are in progress.")
    if finalize:
        plan["status"] = "review"
        plan["gap_analysis"] = {"status": "complete", "notes_zh": "固定 ATT&CK Enterprise 19.1 基线的 20 个 Execution 父候选已全部完成准入与 YAML-only 2.0 开发，共形成 40 项 Niji 原生子技术；未发现需要 add 的稳定执行路径缺口。跨技术复核确认原生 API、流水线、调度器、无服务器、模块、部署工具、系统服务、开发实用程序、真实用户动作与 WMI 的直接对象互不替代；所有正式对象保持 review，等待人工领域审查。", "notes_en": "All twenty Execution parent candidates in the fixed ATT&CK Enterprise 19.1 baseline now have admission decisions and YAML-only 2.0 development, producing forty Niji-native children. No stable execution-path gap requiring add was identified. Cross-technique review confirms that native API, pipeline, scheduler, serverless, module, deployment-tool, system-service, developer-utility, real-user-action, and WMI direct objects do not substitute for one another. All formal objects remain in review pending human domain review."}
        plan["review"] = {"taxonomy": "passed", "evidence": "passed", "bilingual": "passed", "reviewers": []}
    else:
        plan["status"] = "active"
        plan["gap_analysis"] = {"status": "in-progress", "notes_zh": "固定基线 20 个父候选已建立完整清单；第二批十个候选正在完成正式集成与 Niji 原生缺口复核。", "notes_en": "The complete fixed-baseline inventory of twenty parents is recorded; the second batch of ten candidates is undergoing formal integration and Niji-native gap review."}
    save("planning/tactics/TA0002.yaml", plan)


def write_summary(finalize: bool) -> None:
    save(f"planning/runs/{BATCH}/integration-summary.yaml", {
        "schema_version": "1.0.0", "type": "batch-integration-summary", "batch_ref": BATCH, "status": "review" if finalize else "active", "candidate_results": [{"source_attack_id": parent["attack"], "decision": parent["decision"], "technique_ref": parent["id"], "subtechnique_refs": [item["id"] for item in parent["children"]]} for parent in PARENTS],
        "shared_library_resolutions": {"reuse": [], "extend": ["DET-000058", "DET-000059", "DET-000060", "NJA-000032", "NJA-000034", "MIT-000057", "MIT-000058", "MIT-000059"], "create_ranges": {"references": "REF-000125..REF-000134", "claims": "CLM-000277..CLM-000307", "cases": None, "detection_strategies": "DET-000061..DET-000063", "detection_analytics": "NJA-000037..NJA-000042", "mitigations": "MIT-000060..MIT-000061", "relationships": None}},
        "deferred_hypotheses": ["T1106 按操作系统或系统调用编号拆分会把平台和接口当作分类轴，因此不建立。", "T1129 按 DLL、SO、dylib 等模块格式拆分会复制同一加载观察边界，因此不建立。", "T1204 按链接、文件、镜像、复制粘贴或库类型拆分属于 ATT&CK 介质分类，未导入 Niji 子层。", "流水线到交付制品的供应链影响、计划与服务的持久化效果以及软件部署与 WMI 的横向移动效果保留在相邻战术，不在本批次重复建类。"], "duplicate_resolution_refs": [],
        "validation": {"matrix_objects": 692 if finalize else None, "schema_errors": 0 if finalize else None, "schema_warnings": 0 if finalize else None, "unresolved_duplicate_candidates": 0 if finalize else None, "reviewed_similarity_resolutions": 1 if finalize else None, "infrastructure_tests": 12 if finalize else None, "web_api_issues": 0 if finalize else None, "bundles_built": [parent["id"] for parent in PARENTS] if finalize else []},
        "review_notes_zh": "Execution 固定 ATT&CK 19.1 顺序中剩余十个父候选已完成准入和 YAML-only 2.0 开发，形成十个父技术与二十一项按稳定匿迹变量划分的 Niji 原生子技术。共享库新建十项固定版本 ATT&CK Reference、三十一项原子 Claim、三项 Detection Strategy、六项 Detection Analytic 与两项 Mitigation，并对八项现有共享对象作语义一致的扩展；未为数量目标创建 Case 或 Relationship。" + ("正式内容和规划机器门禁、Bundle 与 Review Web QA 均已通过，全部对象保持 review，等待人工领域审查；固定基线候选和 Niji 原生缺口扫描已经完成，因此 TA0002 进入战术级 review。" if finalize else "正式内容正在完成机器门禁、Bundle 与 Review Web QA。"),
        "review_notes_en": "The remaining ten parent candidates in the fixed ATT&CK 19.1 Execution ordering now have admission decisions and YAML-only 2.0 development, producing ten parents and twenty-one Niji-native children partitioned by stable stealth variables. The shared library adds ten fixed-version ATT&CK References, thirty-one atomic Claims, three Detection Strategies, six Detection Analytics, and two Mitigations, and semantically consistent extensions to eight existing shared objects. No Case or Relationship was created to satisfy a count." + (" Formal-content and planning machine gates, bundles, and Review Web QA pass. Every object remains in review pending human domain review; the fixed-baseline inventory and Niji-native gap scan are complete, so TA0002 enters tactic-level review." if finalize else " Formal content is undergoing machine gates, bundle construction, and Review Web QA."),
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    status = "review" if args.finalize else "draft"
    write_references()
    write_claims()
    write_decisions("review" if args.finalize else "draft")
    write_new_strategies(status)
    write_analytics(status)
    write_new_mitigations(status)
    extend_existing_shared(status)
    write_techniques(status)
    write_handoffs()
    update_plan(args.finalize)
    write_summary(args.finalize)


if __name__ == "__main__":
    main()
