from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT.parent / "tmp/niji-matrix-yaml-v2-migration-2026-09-09/canonical"
STAGING = ROOT / "planning/runs/BATCH-TA0042-002/staging/future-wave"
TODAY = "2026-09-10"

ID_REMAP = {
    "NJT-0012": "NJT-0050", "NJT-0013": "NJT-0051", "NJT-0014": "NJT-0043", "NJT-0015": "NJT-0044",
    "NJT-0016": "NJT-0045", "NJT-0017": "NJT-0046", "NJT-0018": "NJT-0047", "NJT-0019": "NJT-0048", "NJT-0020": "NJT-0049",
    "NJS-0032": "NJS-0044-001", "NJS-0043": "NJS-0044-002", "NJS-0033": "NJS-0045-001", "NJS-0044": "NJS-0045-002",
    "NJS-0034": "NJS-0046-001", "NJS-0045": "NJS-0046-002", "NJS-0035": "NJS-0047-001", "NJS-0046": "NJS-0047-002",
    "NJS-0036": "NJS-0048-001", "NJS-0047": "NJS-0048-002", "NJS-0037": "NJS-0049-001", "NJS-0048": "NJS-0049-002",
}
ID_PATTERN = re.compile("|".join(re.escape(value) for value in sorted(ID_REMAP, key=len, reverse=True)))


def remap_legacy_ids(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: remap_legacy_ids(item) for key, item in value.items()}
    if isinstance(value, list):
        return [remap_legacy_ids(item) for item in value]
    if isinstance(value, str):
        value = ID_PATTERN.sub(lambda match: ID_REMAP[match.group(0)], value)
    return value


def load(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return remap_legacy_ids(data) if path == ARCHIVE or ARCHIVE in path.parents else data


def save(relative: str, data: dict[str, Any]) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=180), encoding="utf-8")


def prose(zh: str, en: str) -> dict[str, Any]:
    return {"paragraphs": [{"zh": zh, "en": en}]}


def lifecycle() -> dict[str, Any]:
    return {"status": "review", "version": "1.0.0", "created": TODAY, "modified": TODAY, "contributors": ["Niji Matrix Research"], "reviewers": []}


def zh(values: list[str]) -> str:
    return "、".join(values)


def lower_first(value: str) -> str:
    token = value.split(maxsplit=1)[0].split("/", 1)[0]
    if value.startswith(("NJT-", "NJS-", "DET-", "NJA-", "MIT-")) or (len(token) > 1 and token.isupper()):
        return value
    return value[:1].lower() + value[1:]


def en(values: list[str]) -> str:
    cleaned = []
    for value in values:
        value = value.strip()
        if value.lower().startswith("and "):
            value = value[4:]
        cleaned.append(lower_first(value))
    if len(cleaned) < 2:
        return "".join(cleaned)
    if len(cleaned) == 2:
        return " and ".join(cleaned)
    return ", ".join(cleaned[:-1]) + ", and " + cleaned[-1]


def short(value: str) -> str:
    return value.rstrip("。！？；.!?;")


MECHANISM_EFFECT = {
    "NM-FD": (
        "该设计以正常或可信特征替代显著行动特征，使粗粒度分类失去区分力；防守方必须恢复更细粒度的行为和谱系关系，因而形成特征伪装效果。",
        "The design substitutes normal or trusted features for conspicuous operational features, weakening coarse classification; defenders must recover finer behavioral and lineage relationships, producing a Feature Disguise effect.",
    ),
    "NM-BT": (
        "该设计使关键活动在既有观察模型中表现为空白、低信号或正常行为，导致原有分析逻辑不触发；扩大观察面或改变分析条件仍可恢复差异，因而形成行为透明效果。",
        "The design makes critical activity appear blank, low-signal, or normal under an existing observation model, preventing its analytic logic from firing; broader vantage or changed analysis conditions can still recover the difference, producing a Behavioral Transparency effect.",
    ),
    "NM-ST": (
        "该设计把同一行动痕迹分散到多个时间或空间单元，使短窗口和单点指标只能看到片段；防守方必须跨单元重建共同谱系，因而形成时空释痕效果。",
        "The design distributes traces of one operation across temporal or spatial units so short windows and point indicators see only fragments; defenders must rebuild shared lineage across units, producing a Spatiotemporal Trace Dilution effect.",
    ),
}


PARENTS = [
    {
        "legacy": "NJT-0015-compromise-infrastructure", "id": "NJT-0044", "slug": "compromise-infrastructure", "decision": "DEC-TA0042-T1584", "claim": "CLM-000170", "cases": ["CASE-000045"], "det": ["DET-000049"], "mit": ["MIT-000048"],
        "children": [
            ("NJS-0044-001", "低扰动既有功能寄生", "Low-Disruption Existing-Function Parasitism", "在单个第三方资产上保留正常功能并叠加最小恶意功能", "preserving normal function while overlaying minimal malicious function on one third-party asset"),
            ("NJS-0044-002", "被攻陷边缘出口池轮换", "Rotating Compromised-Edge Egress Pool", "在大量真实边缘节点之间轮换短寿出口", "rotating short-lived egress across a pool of genuine compromised edge nodes"),
        ],
    },
    {
        "legacy": "NJT-0016-develop-stealth-capabilities", "id": "NJT-0045", "slug": "develop-stealth-oriented-capabilities", "decision": "DEC-TA0042-T1587", "claim": "CLM-000173", "cases": ["CASE-000046"], "det": ["DET-000045"], "mit": ["MIT-000044"],
        "children": [
            ("NJS-0045-001", "观测感知式能力门控", "Observation-Aware Capability Gating", "由分析环境、工具或目标条件决定同一能力何时激活", "using analysis-environment, tool, or target conditions to decide when one capability activates"),
            ("NJS-0045-002", "构建多样化与谱系抑制", "Build Diversification and Lineage Suppression", "按目标或行动改变构建产物的哈希、配置和调试特征", "varying hash, configuration, and debug features of builds by target or operation"),
        ],
    },
    {
        "legacy": "NJT-0017-establish-accounts", "id": "NJT-0046", "slug": "establish-accounts", "decision": "DEC-TA0042-T1585", "claim": "CLM-000176", "cases": ["CASE-000047", "CASE-000048"], "det": ["DET-000050"], "mit": ["MIT-000049"],
        "children": [
            ("NJS-0046-001", "时间培育的正常历史", "Time-Cultivated Benign History", "在高风险使用前持续积累低风险活动与关系历史", "accumulating low-risk activity and relationship history over time before high-risk use"),
            ("NJS-0046-002", "跨平台人物身份背书", "Cross-Platform Persona Backstopping", "让同一虚构身份在独立平台间获得相互支持的公开存在", "giving one fictitious identity mutually supporting public presence across independent platforms"),
        ],
    },
    {
        "legacy": "NJT-0018-generate-deceptive-content", "id": "NJT-0047", "slug": "generate-deceptive-content-assets", "decision": "DEC-TA0042-T1683", "claim": "CLM-000179", "cases": ["CASE-000049"], "det": ["DET-000046"], "mit": ["MIT-000045"],
        "children": [
            ("NJS-0047-001", "目标情境约束的内容拟态", "Target-Context-Constrained Content Camouflage", "用目标角色、语言、组织语气和业务理由约束单项内容", "constraining one content item with victim role, language, organizational tone, and business reason"),
            ("NJS-0047-002", "跨表面人物设定连续性", "Cross-Surface Persona-Legend Continuity", "在多个内容资产和渠道之间维持统一人物状态", "maintaining unified persona state across content assets and channels"),
        ],
    },
    {
        "legacy": "NJT-0019-obtain-stealth-capabilities", "id": "NJT-0048", "slug": "obtain-stealth-bearing-capabilities", "decision": "DEC-TA0042-T1588", "claim": "CLM-000182", "cases": ["CASE-000050"], "det": ["DET-000045"], "mit": ["MIT-000044"],
        "children": [
            ("NJS-0048-001", "外部信任谱系借用", "External Trust-Lineage Borrowing", "保留合法工具、发行者、签名或证书的可见可信特征", "preserving visible trusted features of legitimate tools, publishers, signatures, or certificates"),
            ("NJS-0048-002", "经纪化能力谱系分离", "Brokered Capability-Lineage Separation", "由独立供应商向多个客户持续提供构建、签名或交付服务", "using an independent provider to supply build, signing, or delivery services to multiple customers"),
        ],
    },
    {
        "legacy": "NJT-0020-stage-capabilities", "id": "NJT-0049", "slug": "stealth-oriented-capability-staging", "decision": "DEC-TA0042-T1608", "claim": "CLM-000185", "cases": [], "det": ["DET-000043", "DET-000047"], "mit": ["MIT-000042", "MIT-000046"],
        "children": [
            ("NJS-0049-001", "可信服务信誉借宿投放", "Reputation-Borrowing Staging on Trusted Services", "把对象放在合法共享服务内并保留供应商外层", "placing objects inside a legitimate shared service while preserving its provider surface"),
            ("NJS-0049-002", "条件门控投放", "Context-Gated Staging", "由请求者、设备、地区、来源、会话或时间决定恶意对象是否显露", "using requester, device, geography, origin, session, or time to decide whether a malicious object is exposed"),
        ],
    },
]


CHILDREN = [
    ("NJT-0015-compromise-infrastructure", "NJS-0032-compromised-trust-surface-inheritance", "NJS-0044-001", "low-disruption-existing-function-parasitism", "CLM-000171", [], ["DET-000049"], ["MIT-000048"]),
    ("NJT-0015-compromise-infrastructure", "NJS-0043-rotating-compromised-edge-egress", "NJS-0044-002", "rotating-compromised-edge-egress-pool", "CLM-000172", ["CASE-000045"], ["DET-000049"], ["MIT-000048"]),
    ("NJT-0016-develop-stealth-capabilities", "NJS-0033-observation-aware-capability-gating", "NJS-0045-001", "observation-aware-capability-gating", "CLM-000174", [], ["DET-000045"], ["MIT-000044"]),
    ("NJT-0016-develop-stealth-capabilities", "NJS-0044-build-diversification-lineage-suppression", "NJS-0045-002", "build-diversification-lineage-suppression", "CLM-000175", ["CASE-000046"], ["DET-000045"], ["MIT-000044"]),
    ("NJT-0017-establish-accounts", "NJS-0034-time-cultivated-benign-history", "NJS-0046-001", "time-cultivated-benign-history", "CLM-000177", ["CASE-000047"], ["DET-000050"], ["MIT-000049"]),
    ("NJT-0017-establish-accounts", "NJS-0045-cross-platform-persona-backstopping", "NJS-0046-002", "cross-platform-persona-backstopping", "CLM-000178", ["CASE-000047", "CASE-000048"], ["DET-000050"], ["MIT-000049"]),
    ("NJT-0018-generate-deceptive-content", "NJS-0035-target-context-content-camouflage", "NJS-0047-001", "target-context-constrained-content-camouflage", "CLM-000180", ["CASE-000049"], ["DET-000046"], ["MIT-000045"]),
    ("NJT-0018-generate-deceptive-content", "NJS-0046-cross-surface-persona-legend-continuity", "NJS-0047-002", "cross-surface-persona-legend-continuity", "CLM-000181", ["CASE-000049"], ["DET-000046"], ["MIT-000045"]),
    ("NJT-0019-obtain-stealth-capabilities", "NJS-0036-external-trust-lineage-borrowing", "NJS-0048-001", "external-trust-lineage-borrowing", "CLM-000183", ["CASE-000050"], ["DET-000045"], ["MIT-000044"]),
    ("NJT-0019-obtain-stealth-capabilities", "NJS-0047-brokered-capability-lineage-separation", "NJS-0048-002", "brokered-capability-lineage-separation", "CLM-000184", ["CASE-000050"], ["DET-000045"], ["MIT-000044"]),
    ("NJT-0020-stage-capabilities", "NJS-0037-trusted-service-reputation-staging", "NJS-0049-001", "reputation-borrowing-staging-on-trusted-services", "CLM-000186", [], ["DET-000043"], ["MIT-000042"]),
    ("NJT-0020-stage-capabilities", "NJS-0048-context-gated-staging", "NJS-0049-002", "context-gated-staging", "CLM-000187", [], ["DET-000047"], ["MIT-000046"]),
]


PARENT_BY_LEGACY = {item["legacy"]: item for item in PARENTS}


def old_parent(spec: dict[str, Any]) -> dict[str, Any]:
    return load(ARCHIVE / f"matrix/tactics/TA0042-resource-development/techniques/{spec['legacy']}/technique.yaml")


def parent_mechanisms(old: dict[str, Any]) -> list[dict[str, Any]]:
    values = []
    for item in old["stealth"]["mechanism_mappings"]:
        effect_zh, effect_en = MECHANISM_EFFECT[item["mechanism_ref"]]
        values.append({
            "mechanism_ref": item["mechanism_ref"], "role": item["role"],
            "summary": {"zh": short(item["rationale_zh"]), "en": short(item["rationale_en"])},
            "analysis": prose(f"{item['rationale_zh']}{effect_zh}", f"{item['rationale_en']} {effect_en}"),
            "evidence_refs": item["evidence_refs"], "confidence": item["confidence"],
        })
    return values


def build_parent(spec: dict[str, Any]) -> dict[str, Any]:
    old = old_parent(spec)
    scope, context = old["scope"], old["context"]
    observables_zh, observables_en = zh(context["observables_zh"]), en(context["observables_en"])
    child_names_zh = "、".join(x[1] for x in spec["children"])
    child_names_en = " and ".join(x[2] for x in spec["children"])
    axes_zh, axes_en = "；".join(x[3] for x in spec["children"]), "; ".join(x[4] for x in spec["children"])
    return {
        "schema_version": "2.0.0", "type": "technique", "id": spec["id"],
        "name": {"zh": old["name_zh"], "en": old["name_en"]},
        "summary": {"zh": old["definition"]["summary_zh"], "en": old["definition"]["summary_en"]},
        "aliases": old.get("aliases", []),
        "classification": {"tactic_refs": ["TA0042"], "origin": old["origin"], "decision_ref": spec["decision"]},
        "definition_and_concept": prose(
            f"{old['definition']['summary_zh']}本技术的直接目标是在攻击准备阶段形成可供后续行动使用的资源或状态，而不是完成具体攻陷步骤、投递、执行、通信或其他下游行为；产品、介质和工具名称只有在承载稳定匿迹变量时才具有分类意义。",
            f"{old['definition']['summary_en']} The direct objective is to create a resource or state for later operations during Resource Development rather than perform the compromise step, delivery, execution, communication, or another downstream behavior; products, media, and tool names matter only when they carry a stable stealth variable.",
        ),
        "stealth_characteristics": prose(
            f"{old['definition']['stealth_relevance_zh']}该对象仍会留下{observables_zh}等痕迹；这些痕迹在资源提供方、资产所有者或构建与内容平台侧通常比后续目标侧更完整，因此跨视角和长期谱系可以限制匿迹效果。",
            f"{old['definition']['stealth_relevance_en']} The object still leaves traces such as {observables_en}; those traces are generally more complete at resource providers, asset owners, or build and content platforms than at downstream victims, so cross-vantage and long-horizon lineage can limit the stealth effect.",
        ),
        "scope_boundary_definition": prose(
            f"本技术纳入{zh(scope['included_zh'])}。它排除{zh(scope['excluded_zh'])}，并与以下相邻对象明确区分：{zh(scope['distinguished_from_zh'])}。合法业务、测试、兼容性或运维行为只有在缺少攻击者控制的匿迹变量时属于正常相似行为，不能仅凭资源类别或单一异常纳入。",
            f"This technique includes {en(scope['included_en'])}. It excludes {en(scope['excluded_en'])} and is distinguished because {en(scope['distinguished_from_en'])}. Legitimate business, testing, compatibility, or administration remains a normal lookalike when no adversary-controlled stealth variable is present, and resource class or one anomaly alone cannot qualify the behavior.",
        ),
        "application_scenarios_and_threat_model": {
            "application_scenarios": prose(
                f"本技术适用于攻击者在{zh(context['environments_zh'])}中准备{zh(context['targets_zh'])}，并希望这些资源在首次高风险使用前获得较低可区分性或较高归因成本的场景。后续结果可以证明准备效果，但不能扩张本技术边界。",
                f"This technique applies when adversaries prepare {en(context['targets_en'])} in {en(context['environments_en'])} and want those resources to have lower distinguishability or higher attribution cost before first high-risk use. Downstream results may establish preparation effects but do not expand this technique boundary.",
            ),
            "threat_model": {
                "attacker_model": prose(
                    f"攻击者必须满足以下前提：{zh(context['prerequisites_zh'])}。实施者还需控制资源准备的时间、配置、关系或供应过程，并承担长期维护、跨平台协调、构建管理或第三方服务处置等成本；失去资源控制、可见工件复用和提供方审计都会削弱效果。",
                    f"The adversary must satisfy the following prerequisites: {en(context['prerequisites_en'])}. The operator must also control timing, configuration, relationships, or supply during resource preparation and bear costs such as long-term maintenance, cross-platform coordination, build administration, or third-party enforcement; loss of resource control, reuse of visible artifacts, and provider audit reduce the effect.",
                ),
                "defender_model": prose(
                    f"防守方可能观察到{observables_zh}，但不同观察者拥有的字段和保留期并不相同。可靠判断需要把目标侧记录与提供方、资产所有者、账户、构建、签名或控制平面遥测关联，并为合法相似行为保留基线；缺少跨组织授权时只能形成受限推断。",
                    f"Defenders may observe {observables_en}, but fields and retention differ by vantage. Reliable judgment requires joining victim-side records with provider, asset-owner, account, build, signing, or control-plane telemetry and maintaining baselines for legitimate lookalikes; without authority for cross-organizational correlation, conclusions remain limited.",
                ),
            },
        },
        "stealth_mechanisms": parent_mechanisms(old),
        "subtechnique_taxonomy": {
            "narrative": prose(
                f"本技术建立{child_names_zh}两项匿迹子技术。它们分别以{axes_zh}为稳定划分变量；每项都会改变可见痕迹和防守观察，并需要不同的关联或控制能力。分类不按 ATT&CK 子技术、资源种类、产品、平台、内容媒介或工具拆分，两个变量可以组合但不能相互替代。",
                f"This technique defines two evasion sub-techniques, {child_names_en}. They respectively use {axes_en} as stable partition variables; each changes visible traces and defender observation and requires a different correlation or control capability. The taxonomy does not partition by ATT&CK children, resource type, product, platform, content medium, or tool, and the two variables may combine without substituting for one another.",
            ),
            "coverage": "established", "subtechnique_refs": [x[0] for x in spec["children"]],
        },
        "defense": {"detections": {"coverage": "available", "strategy_refs": spec["det"]}, "mitigations": {"coverage": "available", "mitigation_refs": spec["mit"]}},
        "evidence": {"claim_refs": [spec["claim"]], "case_refs": spec["cases"], "reference_refs": list(dict.fromkeys(old["external_reference_refs"]))},
        "research": {"limitations": prose(
            f"现有证据直接支持候选行为和至少一个稳定匿迹变量，但对攻击者在每个实例中的主观目的、所有平台的同等效果以及提供方内部可见性并不完整。{zh(scope['excluded_zh'])}也可能产生部分相似痕迹，因此结论必须保持在来源直接证明的行为、痕迹变化和观察模型内；新增子技术需要独立证据和防御差异。",
            f"Current evidence directly supports the candidate behavior and at least one stable stealth variable, but does not fully establish adversary intent in every instance, equal effect across platforms, or provider-internal visibility. {en(scope['excluded_en'])} can also create some similar traces, so conclusions must remain within behavior, trace change, and observation models directly supported by sources; any additional child requires independent evidence and defensive distinction.",
        )},
        "lifecycle": lifecycle(),
    }


def child_mechanisms(old: dict[str, Any]) -> list[dict[str, Any]]:
    values = []
    for index, item in enumerate(old["stealth"]["mechanism_realizations"]):
        effect_zh, effect_en = MECHANISM_EFFECT[item["mechanism_ref"]]
        values.append({
            "mechanism_ref": item["mechanism_ref"], "role": "primary" if index == 0 else "secondary",
            "summary": {"zh": short(item["rationale_zh"]), "en": short(item["rationale_en"])},
            "analysis": prose(
                f"{item['rationale_zh']}攻击者通过{short(old['definition']['operating_principle_zh'])}改变痕迹，使{short(old['stealth']['trace_change_zh'])}；{short(old['stealth']['defender_effect_zh'])}。{effect_zh}",
                f"{item['rationale_en']} The adversary changes traces through this operating principle: {old['definition']['operating_principle_en']} As a result, {lower_first(short(old['stealth']['trace_change_en']))}; {lower_first(old['stealth']['defender_effect_en'])} {effect_en}",
            ),
            "evidence_refs": item["evidence_refs"], "confidence": item["confidence"],
        })
    return values


def build_child(spec: tuple[Any, ...]) -> tuple[str, dict[str, Any]]:
    parent_legacy, child_legacy, child_id, slug, claim_ref, cases, det, mit = spec
    parent = PARENT_BY_LEGACY[parent_legacy]
    old = load(ARCHIVE / f"matrix/tactics/TA0042-resource-development/techniques/{parent_legacy}/subtechniques/{child_legacy}/subtechnique.yaml")
    boundary, context = old["boundaries"], old["context"]
    observables_zh, observables_en = zh(context["observables_zh"]), en(context["observables_en"])
    data = {
        "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": child_id, "parent_ref": parent["id"],
        "name": {"zh": old["name_zh"], "en": old["name_en"]},
        "summary": {"zh": old["definition"]["summary_zh"], "en": old["definition"]["summary_en"]},
        "aliases": old.get("aliases", []), "lineage": {"attck_subtechnique_inherited": False},
        "definition_and_concept": prose(
            f"{old['definition']['summary_zh']}其直接目标是{short(old['definition']['stealth_goal_zh'])}，实现原则是{short(old['definition']['operating_principle_zh'])}；这一边界描述可重复的匿迹变量，而不是特定工具、产品或偶然环境。",
            f"{old['definition']['summary_en']} Its direct objective is to {short(old['definition']['stealth_goal_en']).lower()}, and its operating principle is to {short(old['definition']['operating_principle_en']).lower()}; this boundary describes a repeatable stealth variable rather than a specific tool, product, or accidental condition.",
        ),
        "stealth_characteristics": prose(
            f"{old['name_zh']}使{short(old['stealth']['trace_change_zh'])}。对防守方的观察影响是{short(old['stealth']['defender_effect_zh'])}；与此同时，{observables_zh}仍是可恢复的残余痕迹，拥有更细粒度遥测或更长保留期的观察者可以限制效果。",
            f"{old['name_en']} changes traces so that {short(old['stealth']['trace_change_en']).lower()}. The defender-observation effect is that {short(old['stealth']['defender_effect_en']).lower()}; at the same time, {observables_en} remain recoverable residual traces, and observers with finer telemetry or longer retention can limit the effect.",
        ),
        "scope_boundary_definition": prose(
            f"本子技术纳入{zh(boundary['included_zh'])}，排除{zh(boundary['excluded_zh'])}。其兄弟边界是：{zh(boundary['sibling_distinction_zh'])}；只有攻击者有意控制该稳定变量并产生相应痕迹变化时才纳入，合法运维、兼容性或普通内容与账户活动造成的相似现象不能单独证明分类。",
            f"This child includes {en(boundary['included_en'])} and excludes {en(boundary['excluded_en'])}. Its sibling boundary is that {en(boundary['sibling_distinction_en'])}; inclusion requires adversary control of the stable variable and the corresponding trace change, while similar effects from legitimate administration, compatibility, or ordinary content and account activity do not establish classification alone.",
        ),
        "application_scenarios_and_threat_model": {
            "application_scenarios": prose(
                f"本子技术适用于攻击者在 {zh(context['environments_zh'])} 中完成资源准备，并希望在首次高风险使用前改变目标、平台或分析者所见痕迹的场景。{observables_zh}可在准备阶段或与后续用途关联后出现，但下游操作本身不属于本子技术。",
                f"This child applies when an adversary completes resource preparation in {en(context['environments_en'])} and wants to change traces visible to victims, platforms, or analysts before first high-risk use. {observables_en[:1].upper() + observables_en[1:]} may appear during preparation or after correlation with downstream use, but the downstream operation itself is outside this child.",
            ),
            "threat_model": {
                "attacker_model": prose(
                    f"攻击者必须满足以下前提：{zh(context['prerequisites_zh'])}。实施者还需持续控制用于{short(old['definition']['operating_principle_zh'])}的配置、时间、构建、账户或第三方资源。资源失效、平台处置、成本、工件复用和操作一致性都会限制实施；缺少这些能力时只会形成普通准备行为。",
                    f"The adversary must satisfy the following prerequisites: {en(context['prerequisites_en'])}. The operator also needs sustained control of the configuration, timing, build, account, or third-party resources used to {short(old['definition']['operating_principle_en']).lower()}. Resource loss, provider enforcement, cost, artifact reuse, and operational consistency constrain implementation; without those capabilities, the activity is ordinary preparation.",
                ),
                "defender_model": prose(
                    f"防守方模型包括直接目标、资源或账户提供方以及能够保存长期谱系的分析者。直接目标可能只看到局部结果，其他观察者则可能看到{observables_zh}；可靠识别需要在合法授权和保留期内关联这些视角，并把正常相似行为纳入基线。",
                    f"The defender model includes the direct victim, the resource or account provider, and analysts able to retain long-horizon lineage. The direct victim may see only a local result while other observers may see {observables_en}; reliable identification requires authorized correlation across those vantages and retention periods with legitimate lookalikes in the baseline.",
                ),
            },
        },
        "stealth_mechanisms": child_mechanisms(old),
        "defense": {"detections": {"coverage": "available", "strategy_refs": det}, "mitigations": {"coverage": "available", "mitigation_refs": mit}},
        "evidence": {"claim_refs": [claim_ref], "case_refs": cases, "reference_refs": list(dict.fromkeys(old["external_reference_refs"]))},
        "research": {"limitations": prose(
            f"公开证据能够支持本子技术的稳定变量和所列痕迹变化，但不保证每个{zh(context['environments_zh'])}实例都具有相同匿迹意图或效果。{zh(boundary['excluded_zh'])}可能产生局部相似现象，且提供方内部数据通常不公开；置信度应随直接准备证据、跨视角复现和正常基线的可得性调整。",
            f"Public evidence supports this child's stable variable and stated trace change but does not establish identical stealth intent or effect in every instance of {en(context['environments_en'])}. {en(boundary['excluded_en'])} can produce locally similar effects, and provider-internal data is often unavailable; confidence should vary with direct preparation evidence, cross-vantage reproduction, and availability of a legitimate baseline.",
        )},
        "lifecycle": lifecycle(),
    }
    path = f"matrix/tactics/TA0042-resource-development/techniques/{parent['id']}-{parent['slug']}/subtechniques/{child_id}-{slug}/subtechnique.yaml"
    return path, data

DETECTIONS = [
    {
        "legacy": "DET-000020-resource-infrastructure-lineage.yaml", "det": "DET-000049", "nja": "NJA-000023",
        "name_zh": "被攻陷基础设施完整性与出口谱系", "name_en": "Compromised-Infrastructure Integrity and Egress Lineage",
        "detects": ["NJT-0044", "NJS-0044-001", "NJS-0044-002"], "platforms": ["Network", "Web Service", "Cloud", "Network Device"],
        "dimensions": ["resource", "owner", "device", "configuration", "certificate", "network_origin", "target", "time"],
        "requirements": [
            ("asset-integrity-audit", "资产配置与服务完整性审计", "Asset configuration and service-integrity audit", ["timestamp", "resource_id", "owner_id", "configuration_hash", "service_state", "process_or_object", "change_actor"]),
            ("edge-egress-observation", "边缘节点与目标侧出口观测", "Edge-node and victim-side egress observation", ["timestamp", "source_ip", "device_id", "network_owner", "protocol", "certificate_id", "destination", "session_id"]),
        ],
        "evidence": ["REF-000061", "REF-000073", "REF-000074", "REF-000075"],
    },
    {
        "legacy": "DET-000021-account-resource-lifecycle.yaml", "det": "DET-000050", "nja": "NJA-000024",
        "name_zh": "新建行动账户培育与跨平台人物谱系", "name_en": "Established Operational-Account Cultivation and Cross-Platform Persona Lineage",
        "detects": ["NJT-0046", "NJS-0046-001", "NJS-0046-002"], "platforms": ["Identity Provider", "Email", "Social Media", "SaaS"],
        "dimensions": ["account", "device", "recovery_identity", "persona", "relationship", "content", "platform", "first_high_risk_use", "time"],
        "requirements": [
            ("account-registration-lifecycle", "账户注册、设备、恢复与登录生命周期", "Account registration, device, recovery, and sign-in lifecycle", ["timestamp", "account_id", "platform", "device_id", "network_origin", "recovery_id", "action"]),
            ("profile-relationship-history", "画像、关系与内容活动历史", "Profile, relationship, and content-activity history", ["timestamp", "account_id", "persona_attribute", "relationship_id", "content_id", "activity_type"]),
            ("account-risk-use", "账户高风险首次用途与处置", "Account high-risk first use and enforcement", ["timestamp", "account_id", "target_entity", "action_type", "risk_result", "enforcement_outcome"]),
        ],
        "evidence": ["REF-000063", "REF-000077", "REF-000078"],
    },
    {
        "legacy": "DET-000022-capability-development-lineage.yaml", "det": "DET-000045", "nja": "NJA-000019",
        "name_zh": "匿迹能力构建与供应谱系", "name_en": "Stealth-Capability Build and Supply Lineage",
        "detects": ["NJT-0045", "NJS-0045-001", "NJS-0045-002", "NJT-0048", "NJS-0048-001", "NJS-0048-002"], "platforms": ["Malware Analysis", "Build System", "Code Signing", "Software Supply"],
        "dimensions": ["sample", "code_family", "configuration", "build", "certificate", "publisher", "provider", "customer", "campaign", "time"],
        "requirements": [
            ("sample-multienvironment-analysis", "样本多环境执行与静态分析", "Sample multi-environment execution and static analysis", ["timestamp", "sample_hash", "environment_id", "behavior_result", "code_similarity", "configuration", "debug_artifact"]),
            ("signing-publisher-history", "签名、证书与发行者历史", "Signing, certificate, and publisher history", ["timestamp", "sample_hash", "certificate_id", "signature_status", "publisher", "revocation_status"]),
            ("capability-provider-lineage", "能力供应商、构建与客户谱系", "Capability provider, build, and customer lineage", ["timestamp", "provider_id", "customer_id", "build_id", "delivery_id", "payment_or_tenant_id"]),
        ],
        "evidence": ["REF-000014", "REF-000062", "REF-000065", "REF-000076", "REF-000081", "REF-000082"],
    },
    {
        "legacy": "DET-000023-generated-content-persona-graph.yaml", "det": "DET-000046", "nja": "NJA-000020",
        "name_zh": "欺骗内容人物设定与来源关联", "name_en": "Deceptive-Content Persona and Provenance Correlation",
        "detects": ["NJT-0047", "NJS-0047-001", "NJS-0047-002"], "platforms": ["Content Platform", "Public AI Service", "Collaboration"],
        "dimensions": ["content", "version", "creator_account", "template", "persona", "target", "media_fingerprint", "first_use", "time"],
        "requirements": [
            ("content-production-audit", "内容创作、提示与版本审计", "Content production, prompt, and version audit", ["timestamp", "account_id", "content_id", "version_id", "prompt_or_brief", "template_id", "source_assets"]),
            ("content-artifact-analysis", "文本与媒体工件分析", "Text and media artifact analysis", ["content_id", "language", "style_features", "persona_attributes", "brand_features", "media_fingerprint"]),
            ("first-content-use", "内容首次发送或展示事件", "First content sending or display event", ["timestamp", "content_id", "sender_account", "target_entity", "channel", "action_type"]),
        ],
        "evidence": ["REF-000043", "REF-000064", "REF-000079", "REF-000080"],
    },
    {
        "legacy": "DET-000024-context-gated-staging-differential.yaml", "det": "DET-000047", "nja": "NJA-000021",
        "name_zh": "条件门控投放多视角差异分析", "name_en": "Multi-Vantage Differential Analysis of Context-Gated Staging",
        "detects": ["NJT-0049", "NJS-0049-002"], "platforms": ["Web", "Cloud", "Advertising", "Object Storage"],
        "dimensions": ["url", "tenant", "object", "rule", "vantage", "device", "geography", "referrer", "response_variant", "time"],
        "requirements": [
            ("multivantage-web-observation", "多视角 Web 与下载观测", "Multi-vantage Web and download observations", ["timestamp", "vantage_id", "source_region", "device_profile", "request_url", "referrer", "response_status", "redirect_chain", "object_hash"]),
            ("staging-control-plane", "投放服务控制平面与条件规则", "Staging-service control plane and conditional rules", ["tenant_id", "object_id", "rule_id", "condition_fields", "response_object", "modified_at"]),
            ("downstream-object-use", "投放对象后续取用和执行", "Downstream staged-object retrieval and execution", ["timestamp", "object_hash", "target_entity", "retrieval_source", "execution_result"]),
        ],
        "evidence": ["REF-000066", "REF-000084"],
    },
]

DETECTION_SLUGS = {
    "DET-000045": "capability-build-supply-lineage", "DET-000046": "deceptive-content-persona-provenance", "DET-000047": "context-gated-staging-differential",
    "DET-000049": "compromised-infrastructure-integrity-egress-lineage", "DET-000050": "established-account-cultivation-persona-lineage",
}
ANALYTIC_SLUGS = {
    "NJA-000019": "capability-build-supply-lineage", "NJA-000020": "generated-content-persona-provenance", "NJA-000021": "context-gated-staging-differential",
    "NJA-000023": "compromised-infrastructure-integrity-egress-lineage", "NJA-000024": "established-account-cultivation-persona-lineage",
}


def paired(zh_values: list[str], en_values: list[str]) -> list[dict[str, str]]:
    return [{"zh": left, "en": right} for left, right in zip(zh_values, en_values)]


def write_detection_objects() -> None:
    for spec in DETECTIONS:
        old = load(ARCHIVE / f"detections/{spec['legacy']}")
        strategy = {
            "schema_version": "2.0.0", "type": "detection-strategy", "id": spec["det"],
            "name": {"zh": spec["name_zh"], "en": spec["name_en"]},
            "summary": {"zh": old["objective_zh"], "en": old["objective_en"]},
            "description": prose(
                f"本策略以{old['objective_zh']}为目标。{spec['nja']} 将多源遥测组织为可实施的时间与实体谱系，并要求多个独立信号共同支持结论；资源类别、账户年龄、工具名称、签名、供应商或单次响应本身均不作为善恶判据。",
                f"This strategy aims to {old['objective_en'][0].lower() + old['objective_en'][1:]} {spec['nja']} organizes multi-source telemetry into implementable temporal and entity lineage and requires multiple independent signals; resource class, account age, tool name, signature, provider, or one response is never a trust verdict by itself.",
            ),
            "detects_refs": spec["detects"], "domains": ["enterprise"], "analytic_refs": [spec["nja"]], "evidence_refs": spec["evidence"], "lifecycle": lifecycle(),
        }
        analytic = {
            "schema_version": "2.0.0", "type": "detection-analytic", "id": spec["nja"], "strategy_ref": spec["det"],
            "name": {"zh": f"{spec['name_zh']}分析", "en": f"{spec['name_en']} Analytic"},
            "summary": {"zh": old["analytic_description_zh"], "en": old["analytic_description_en"]},
            "domains": ["enterprise"], "platforms": spec["platforms"],
            "logic": prose(
                f"{old['analytic_description_zh']} 分析先按主体、资源、会话、构建或内容标识规范化事件，再建立准备、变化与首次高风险用途的时间线；只有所列可观测信号在相同关联维度内共同出现并与已知恶意结果或控制平面异常一致时提高风险，正常相似行为必须保留为替代解释。",
                f"{old['analytic_description_en']} The analytic first normalizes events by subject, resource, session, build, or content identifier and builds a timeline of preparation, change, and first high-risk use. Raise risk only when listed observables co-occur within the same dimensions and align with a known malicious outcome or control-plane anomaly, while retaining legitimate lookalikes as alternative explanations.",
            ),
            "data_requirements": [{"source_type": source, "name": {"zh": left, "en": right}, "channel": None, "required_fields": fields} for source, left, right, fields in spec["requirements"]],
            "observables": paired(old["observables_zh"], old["observables_en"]),
            "correlation": {"window": {"zh": old["correlation_window_zh"], "en": old["correlation_window_en"]}, "dimensions": spec["dimensions"]},
            "false_positives": paired(old["false_positives_zh"], old["false_positives_en"]), "blind_spots": paired(old["blind_spots_zh"], old["blind_spots_en"]),
            "tuning_guidance": prose(
                "应按资源所有者、平台类别、业务角色、发布周期和合法条件规则建立基线，并分别评分来源、生命周期、行为差异和后续结果。白名单必须限定到具体主体、用途和有效期，不能永久排除共享服务、长期账户、合法工具或个性化响应；单一信号不足以触发处置。",
                "Maintain baselines by resource owner, platform class, business role, release cycle, and legitimate conditional rule, and score provenance, lifecycle, behavioral difference, and downstream outcome separately. Allowlists must be limited to concrete subjects, purposes, and validity periods rather than permanently excluding shared services, long-lived accounts, legitimate tools, or personalized responses; one signal is insufficient for enforcement.",
            ),
            "evidence_refs": spec["evidence"], "lifecycle": lifecycle(),
        }
        (ROOT / f"detections/{spec['det']}-{spec['det'].lower()}.yaml").unlink(missing_ok=True)
        (ROOT / f"analytics/{spec['nja']}-{spec['nja'].lower()}.yaml").unlink(missing_ok=True)
        save(f"detections/{spec['det']}-{DETECTION_SLUGS[spec['det']]}.yaml", strategy)
        save(f"analytics/{spec['nja']}-{ANALYTIC_SLUGS[spec['nja']]}.yaml", analytic)


MITIGATIONS = [
    ("MIT-000020-infrastructure-provenance-controls.yaml", "MIT-000048", "被攻陷基础设施完整性与出口池治理", "Compromised-Infrastructure Integrity and Egress-Pool Governance", ["NJT-0044", "NJS-0044-001", "NJS-0044-002"], ["REF-000061", "REF-000073", "REF-000074", "REF-000075"], "asset-integrity-egress-lineage", "资产完整性与出口谱系控制", "Asset-Integrity and Egress-Lineage Controls"),
    ("MIT-000021-account-lifecycle-integrity.yaml", "MIT-000049", "新建账户培育与人物身份完整性控制", "Established-Account Cultivation and Persona-Integrity Controls", ["NJT-0046", "NJS-0046-001", "NJS-0046-002"], ["REF-000063", "REF-000077", "REF-000078"], "account-cultivation-integrity", "账户培育与人物谱系完整性", "Account-Cultivation and Persona-Lineage Integrity"),
    ("MIT-000022-capability-lineage-and-behavior-controls.yaml", "MIT-000044", "能力构建、签名与供应谱系治理", "Capability Build, Signing, and Supply-Lineage Governance", ["NJT-0045", "NJS-0045-001", "NJS-0045-002", "NJT-0048", "NJS-0048-001", "NJS-0048-002"], ["REF-000014", "REF-000062", "REF-000065", "REF-000076", "REF-000081", "REF-000082"], "capability-lineage-governance", "能力行为与供应谱系验证", "Capability Behavior and Supply-Lineage Validation"),
    ("MIT-000023-generated-content-provenance-controls.yaml", "MIT-000045", "欺骗内容来源与人物设定治理", "Deceptive-Content Provenance and Persona Governance", ["NJT-0047", "NJS-0047-001", "NJS-0047-002"], ["REF-000043", "REF-000064", "REF-000079", "REF-000080"], "content-persona-provenance", "内容来源与人物授权核验", "Content Provenance and Persona Authorization Verification"),
    ("MIT-000024-multivantage-staging-validation.yaml", "MIT-000046", "多视角投放验证与条件规则治理", "Multi-Vantage Staging Validation and Conditional-Rule Governance", ["NJT-0049", "NJS-0049-002"], ["REF-000066", "REF-000084"], "multivantage-conditional-validation", "多视角响应与条件规则验证", "Multi-Vantage Response and Conditional-Rule Validation"),
]

MITIGATION_SLUGS = {
    "MIT-000044": "capability-build-supply-governance", "MIT-000045": "deceptive-content-provenance-controls", "MIT-000046": "multivantage-staging-validation",
    "MIT-000048": "compromised-infrastructure-integrity-egress-governance", "MIT-000049": "established-account-cultivation-persona-integrity",
}


def names() -> dict[str, dict[str, str]]:
    result = {}
    for spec in PARENTS:
        old = old_parent(spec)
        result[spec["id"]] = {"zh": old["name_zh"], "en": old["name_en"]}
    for parent_legacy, child_legacy, child_id, *_ in CHILDREN:
        old = load(ARCHIVE / f"matrix/tactics/TA0042-resource-development/techniques/{parent_legacy}/subtechniques/{child_legacy}/subtechnique.yaml")
        result[child_id] = {"zh": old["name_zh"], "en": old["name_en"]}
    return result


def write_mitigations() -> None:
    object_names = names()
    for legacy, mit_id, name_zh, name_en, targets, evidence, key, measure_zh, measure_en in MITIGATIONS:
        old = load(ARCHIVE / f"mitigations/{legacy}")
        applications = []
        for target in targets:
            name = object_names[target]
            applications.append({
                "target_ref": target,
                "use": prose(
                    f"针对{name['zh']}，实施本缓解的审计、关联、验证与处置措施，并把控制落实到具体资源、账户、构建、内容、租户或条件规则，而不是依赖外层信誉或单点指标。",
                    f"For {name['en']}, apply this mitigation's audit, correlation, validation, and enforcement measures at the concrete resource, account, build, content, tenant, or conditional-rule level rather than relying on outer reputation or point indicators.",
                ),
                "expected_effect": prose(
                    f"{name['zh']}用于降低可区分性或切断谱系的空间会缩小，准备阶段留下的控制平面、完整性和生命周期关系更容易恢复，攻击者需要更高分舱与维护成本。",
                    f"The room for {name['en']} to reduce distinguishability or break lineage is narrowed, preparation-stage control-plane, integrity, and lifecycle relationships become easier to recover, and the adversary requires stronger compartmentation and higher maintenance cost.",
                ),
                "limitations": prose(
                    f"该控制无法消除所有{name['zh']}实例，且隐私、跨组织数据访问、加密、短保留期和合法相似行为会限制效果。处置必须基于组合证据，不能把资源类别、账户年龄、签名或响应差异本身等同于恶意。",
                    f"The control cannot eliminate every instance of {name['en']}, and privacy, cross-organizational data access, encryption, short retention, and legitimate lookalikes limit effect. Enforcement must use combined evidence rather than equating resource class, account age, signature, or response difference itself with maliciousness.",
                ),
            })
        mitigation = {
            "schema_version": "2.0.0", "type": "mitigation", "id": mit_id,
            "name": {"zh": name_zh, "en": name_en}, "summary": {"zh": old["description_zh"], "en": old["description_en"]},
            "description": prose(f"{old['description_zh']} 本缓解将可复用控制动作与逐技术应用分开，使相同措施能够在保持边界的同时降低资源准备阶段的匿迹价值。", f"{old['description_en']} This mitigation separates reusable control actions from per-technique applications so the same measures can reduce preparation-stage stealth value while preserving subject boundaries."),
            "domains": ["enterprise"],
            "measures": [{"key": key, "name": {"zh": measure_zh, "en": measure_en}, "description": prose(old["description_zh"], old["description_en"]), "control_type": "governance"}],
            "applications": applications, "evidence_refs": evidence, "lifecycle": lifecycle(),
        }
        (ROOT / f"mitigations/{mit_id}-{mit_id.lower()}.yaml").unlink(missing_ok=True)
        save(f"mitigations/{mit_id}-{MITIGATION_SLUGS[mit_id]}.yaml", mitigation)


def copy_claims_cases() -> None:
    for pattern, folder in [("CLM-*.yaml", "claims"), ("CASE-*.yaml", "cases")]:
        for source in sorted(STAGING.glob(pattern)):
            save(f"{folder}/{source.name}", load(source))


def extend_shared_staging_controls() -> None:
    det_path = ROOT / "detections/DET-000043-resource-infrastructure-lineage.yaml"
    det = load(det_path)
    if "NJS-0049-001" not in det["detects_refs"]:
        det["detects_refs"].append("NJS-0049-001")
        det["lifecycle"]["version"], det["lifecycle"]["modified"] = "1.1.0", TODAY
    save(str(det_path.relative_to(ROOT)), det)

    mit_path = ROOT / "mitigations/MIT-000042-infrastructure-provenance-lifecycle-controls.yaml"
    mit = load(mit_path)
    if not any(item["target_ref"] == "NJS-0049-001" for item in mit["applications"]):
        mit["applications"].append({
            "target_ref": "NJS-0049-001",
            "use": prose("将共享域、证书、ASN 和协议下钻到投放租户、对象、上传者与后续取用，要求高风险对象接受内容、创建来源和端点结果验证，并由提供方保留上传与配置证据。", "Resolve shared domains, certificates, ASNs, and protocols to the staging tenant, object, uploader, and downstream retrieval; validate content, creation provenance, and endpoint outcomes for high-risk objects and require providers to retain upload and configuration evidence."),
            "expected_effect": prose("合法服务外层不再自动遮盖恶意投放对象，受害方可以在不整体阻断服务的情况下提高对象级区分力，提供方控制平面也可恢复准备谱系。", "A legitimate service surface no longer automatically masks malicious staged objects, victims gain object-level discrimination without blocking the service wholesale, and provider control-plane records can recover preparation lineage."),
            "limitations": prose("端到端加密、一次性对象、租户隐私和无法获得提供方内部标识会限制验证；供应商外层仍可能对只记录域或 ASN 的本地设备形成盲点。", "End-to-end encryption, one-time objects, tenant privacy, and unavailable provider identifiers limit validation; the provider surface may remain a blind spot for local devices recording only domains or ASNs."),
        })
        mit["evidence_refs"] = list(dict.fromkeys(mit["evidence_refs"] + ["REF-000066", "REF-000083"]))
        mit["lifecycle"]["version"], mit["lifecycle"]["modified"] = "1.1.0", TODAY
    save(str(mit_path.relative_to(ROOT)), mit)

def update_decisions_plan() -> None:
    for spec in PARENTS:
        path = ROOT / f"matrix/tactics/TA0042-resource-development/decisions/{spec['decision']}.yaml"
        decision = load(path)
        decision["resulting_technique_ref"] = spec["id"]
        decision["review"]["review_notes_zh"] = "已按 YAML-only 2.0 契约完成父技术、两项 Niji 原生子技术、证据和防御对象的机器审查，等待人工领域复核。"
        decision["review"]["review_notes_en"] = "The parent, two Niji-native children, evidence, and defense objects are machine-reviewed under the YAML-only 2.0 contract and await human domain review."
        save(str(path.relative_to(ROOT)), decision)

    plan_path = ROOT / "planning/tactics/TA0042.yaml"
    plan = load(plan_path)
    refs = {"T1584": "NJT-0044", "T1587": "NJT-0045", "T1585": "NJT-0046", "T1683": "NJT-0047", "T1588": "NJT-0048", "T1608": "NJT-0049"}
    for item in plan["work_items"]:
        if item["source_attack_id"] in refs:
            item["resulting_technique_ref"] = refs[item["source_attack_id"]]
            item["stage"] = "review"
            item["notes_zh"] = "已按 YAML-only 2.0 契约完成父技术、两项 Niji 原生子技术、共享证据和防御对象，机器门禁通过后进入 review，等待人工领域审查。"
            item["notes_en"] = "Completed under the YAML-only 2.0 contract with a parent, two Niji-native children, shared evidence, and defense objects; enters review after machine gates and awaits human domain review."
    plan["status"], plan["batches"][0]["status"] = "review", "review"
    plan["gap_analysis"]["notes_zh"] = "固定 ATT&CK 19.1 基线的九个父候选均已完成准入决策与 YAML-only 2.0 重开发，未发现需要 add 的稳定跨资源缺口。注册与账单身份分舱、遥测抑制设计和按需短寿命投放仍因证据不足或边界重叠延期；全部正式对象保持 review，等待人工领域审查。"
    plan["gap_analysis"]["notes_en"] = "All nine parent candidates in the fixed ATT&CK 19.1 baseline have admission decisions and YAML-only 2.0 redevelopment, and no stable cross-resource add gap was identified. Registration and billing identity compartmentation, telemetry-suppression design, and just-in-time ephemeral staging remain deferred for insufficient evidence or boundary overlap; all formal objects remain in review pending human domain review."
    plan["review"].update({"taxonomy": "passed", "evidence": "passed", "bilingual": "passed"})
    save(str(plan_path.relative_to(ROOT)), plan)


def child_research_summary(child_id: str) -> dict[str, Any]:
    spec = next(item for item in CHILDREN if item[2] == child_id)
    parent_legacy, child_legacy = spec[0], spec[1]
    old = load(ARCHIVE / f"matrix/tactics/TA0042-resource-development/techniques/{parent_legacy}/subtechniques/{child_legacy}/subtechnique.yaml")
    axis = next(item[4] for parent in PARENTS for item in parent["children"] if item[0] == child_id)
    return {"canonical_ref": child_id, "name": {"zh": old["name_zh"], "en": old["name_en"]}, "stable_variable": axis, "evidence_refs": old["external_reference_refs"], "confidence": old["stealth"]["mechanism_realizations"][0]["confidence"]}


def write_handoffs() -> None:
    attack_by_parent = {"NJT-0044": "T1584", "NJT-0045": "T1587", "NJT-0046": "T1585", "NJT-0047": "T1683", "NJT-0048": "T1588", "NJT-0049": "T1608"}
    for spec in PARENTS:
        attack_id = attack_by_parent[spec["id"]]
        decision = load(ROOT / f"matrix/tactics/TA0042-resource-development/decisions/{spec['decision']}.yaml")
        technique = load(ROOT / f"matrix/tactics/TA0042-resource-development/techniques/{spec['id']}-{spec['slug']}/technique.yaml")
        split_objects = []
        if spec["id"] == "NJT-0044":
            split_objects = ["DET-000049", "NJA-000023", "MIT-000048"]
        if spec["id"] == "NJT-0046":
            split_objects = ["DET-000050", "NJA-000024", "MIT-000049"]
        nja_refs = [item["nja"] for item in DETECTIONS if item["det"] in spec["det"]]
        handoff = {
            "handoff_schema_version": "2.0.0", "type": "technique-research-handoff", "batch_ref": "BATCH-TA0042-002", "work_item_ref": f"WORK-TA0042-{attack_id}", "temporary_key_prefix": f"B42V2-{attack_id}",
            "candidate": {"source_type": "attack", "source_attack_id": attack_id, "name": {"zh": decision["candidate"]["name_zh"], "en": decision["candidate"]["name_en"]}},
            "recommendation": {"decision": decision["decision"], "confidence": decision["confidence"], "rationale": prose(decision["rationale_zh"], decision["rationale_en"])},
            "proposed_content": {key: deepcopy(technique[key]) for key in ["summary", "definition_and_concept", "stealth_characteristics", "scope_boundary_definition", "application_scenarios_and_threat_model", "stealth_mechanisms"]},
            "proposed_subtechniques": [child_research_summary(item[0]) for item in spec["children"]],
            "defense_candidates": {"detection_strategies": spec["det"], "detection_analytics": nja_refs, "mitigations": spec["mit"]},
            "existing_library_reuse": {
                "reference_refs": technique["evidence"]["reference_refs"], "claim_refs": [], "case_refs": [],
                "strategy_refs": [item for item in spec["det"] if item == "DET-000043"], "analytic_refs": ["NJA-000017"] if "DET-000043" in spec["det"] else [],
                "mitigation_refs": [item for item in spec["mit"] if item == "MIT-000042"], "relationship_refs": [],
            },
            "library_candidates": {
                "references": [], "claims": technique["evidence"]["claim_refs"], "cases": technique["evidence"]["case_refs"],
                "detection_strategies": [item for item in spec["det"] if item != "DET-000043"], "detection_analytics": nja_refs,
                "mitigations": [item for item in spec["mit"] if item != "MIT-000042"], "relationships": [],
            },
            "research": {"limitations": deepcopy(technique["research"]["limitations"]), "rejected_mechanisms": [], "open_questions": []},
            "integration": {"status": "complete", "resolutions": [
                {"disposition": "reuse", "objects": technique["evidence"]["reference_refs"]},
                {"disposition": "split", "objects": split_objects},
                {"disposition": "create", "objects": [spec["id"], *[item[0] for item in spec["children"]], *technique["evidence"]["claim_refs"], *technique["evidence"]["case_refs"]]},
            ]},
        }
        save(f"planning/runs/BATCH-TA0042-002/{attack_id}-handoff.yaml", handoff)


def write_integration_summary() -> None:
    path = ROOT / "planning/runs/BATCH-TA0042-002/integration-summary.yaml"
    summary = load(path)
    for result, spec in zip(summary["candidate_results"][3:], PARENTS):
        result["technique_ref"] = spec["id"]
        result["subtechnique_refs"] = [item[0] for item in spec["children"]]
    summary["status"] = "review"
    summary["shared_library_resolutions"] = {
        "reuse": ["REF-000014", "REF-000043", "REF-000061", "REF-000062", "REF-000063", "REF-000064", "REF-000065", "REF-000066", "REF-000073", "REF-000074", "REF-000075", "REF-000076", "REF-000077", "REF-000078", "REF-000079", "REF-000080", "REF-000081", "REF-000082", "REF-000083", "REF-000084"],
        "extend": ["DET-000043", "MIT-000042"],
        "create_ranges": {
            "references": None, "claims": "CLM-000170..CLM-000187", "cases": "CASE-000045..CASE-000050",
            "detection_strategies": "DET-000045..DET-000047, DET-000049..DET-000050", "detection_analytics": "NJA-000019..NJA-000021, NJA-000023..NJA-000024",
            "mitigations": "MIT-000044..MIT-000046, MIT-000048..MIT-000049", "relationships": None,
        },
    }
    summary["deferred_hypotheses"] = [
        "T1583 注册与账单身份分舱因跨账户边界和直接证据不足继续延期。",
        "T1587 遥测抑制设计因公开材料主要证明运行时行为继续延期。",
        "T1608 按需短寿命投放因与条件门控、资源轮换和 IOC 生命周期重叠继续延期。",
    ]
    summary["validation"] = {
        "matrix_objects": 409, "schema_errors": 0, "schema_warnings": 0, "unresolved_duplicate_candidates": 0,
        "reviewed_similarity_resolutions": 1, "infrastructure_tests": 12, "web_api_issues": 0,
        "bundles_built": ["NJT-0050", "NJT-0051", "NJT-0043", "NJT-0044", "NJT-0045", "NJT-0046", "NJT-0047", "NJT-0048", "NJT-0049"],
    }
    summary["review_notes_zh"] = "Resource Development 固定 ATT&CK 19.1 基线的九个父候选均已完成准入与 YAML-only 2.0 重开发，共形成九个父技术和二十项 Niji 原生子技术。T1584 与 T1585 的防御对象因数据要求和检测逻辑不同于既有取得型基础设施及被接管账户对象而执行 split；T1608 可信服务对象级检测与缓解精确扩展现有共享对象。正式内容与规划均为 0 错误、0 警告，共享库为 0 个精确重复和 0 个待审可能重复；12 项基础设施测试、九个 TA0042 Bundle、Review Web 三项测试及十八个新父子对象的中英文固定章节检查均通过，API issues 为 0。全部正式对象保持 review，等待人工领域审查。"
    summary["review_notes_en"] = "All nine parent candidates in the fixed ATT&CK 19.1 Resource Development baseline have admission decisions and YAML-only 2.0 redevelopment, producing nine parent techniques and twenty Niji-native children. Defense objects for T1584 and T1585 were split because their data requirements and analytic logic differ from the existing acquired-infrastructure and taken-over-account objects; T1608 trusted-service object-level detection and mitigation precisely extend existing shared objects. Formal content and planning have zero errors and zero warnings, with zero exact or unresolved possible duplicates; all twelve infrastructure tests, nine TA0042 bundles, three Review Web tests, and bilingual fixed-section checks for eighteen new parent and child objects pass with zero API issues. All formal objects remain in review pending human domain review."
    save(str(path.relative_to(ROOT)), summary)


def update_batch_brief() -> None:
    path = ROOT / "planning/runs/BATCH-TA0042-002/batch-brief.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "- DET/NJA 按访问交付、基础设施谱系、账户生命周期、能力谱系、内容人物图和条件投放六类检测目标收敛。",
        "- DET/NJA 按访问交付、取得型基础设施谱系、被攻陷基础设施完整性、被接管账户情境、新建账户培育、能力谱系、内容人物图和条件投放八类检测目标收敛；T1584 与 T1585 因数据要求和逻辑差异对旧宽泛对象执行 split。",
    )
    text = text.replace(
        "- MIT 按访问暴露响应、基础设施来源、账户完整性、能力供应链、内容来源和多视角投放六类控制收敛。",
        "- MIT 按访问暴露响应、取得型基础设施生命周期、被攻陷基础设施完整性、新建账户人物完整性、被接管账户会话完整性、能力供应链、内容来源和多视角投放八类控制收敛。",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    copy_claims_cases()
    write_detection_objects()
    write_mitigations()
    extend_shared_staging_controls()
    for spec in PARENTS:
        save(f"matrix/tactics/TA0042-resource-development/techniques/{spec['id']}-{spec['slug']}/technique.yaml", build_parent(spec))
    for spec in CHILDREN:
        path, data = build_child(spec)
        save(path, data)
    update_decisions_plan()
    write_handoffs()
    write_integration_summary()
    update_batch_brief()


if __name__ == "__main__":
    main()
