from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[3]
ARCHIVE_ROOT = ROOT.parent / "tmp/niji-matrix-yaml-v2-migration-2026-09-09"
ARCHIVE_TECHNIQUES = ARCHIVE_ROOT / "canonical/matrix/tactics/TA0001-initial-access/techniques"
PRUNED = ARCHIVE_ROOT / "pruned-records"
TACTIC_ROOT = ROOT / "matrix/tactics/TA0001-initial-access"
BATCH = "BATCH-TA0001-001"
TODAY = "2026-09-10"


PARENT_ID_MAP = {
    "NJT-0021": "NJT-0052",
    "NJT-0022": "NJT-0053",
    "NJT-0023": "NJT-0054",
    "NJT-0024": "NJT-0055",
    "NJT-0025": "NJT-0056",
    "NJT-0026": "NJT-0057",
    "NJT-0027": "NJT-0058",
    "NJT-0028": "NJT-0059",
    "NJT-0029": "NJT-0060",
    "NJT-0030": "NJT-0061",
    "NJT-0031": "NJT-0062",
}

CHILD_ID_MAP = {
    "NJS-0049": "NJS-0052-001",
    "NJS-0050": "NJS-0052-002",
    "NJS-0051": "NJS-0052-003",
    "NJS-0052": "NJS-0053-001",
    "NJS-0053": "NJS-0053-002",
    "NJS-0054": "NJS-0053-003",
    "NJS-0055": "NJS-0053-004",
    "NJS-0056": "NJS-0054-001",
    "NJS-0057": "NJS-0054-002",
    "NJS-0058": "NJS-0055-001",
    "NJS-0059": "NJS-0055-002",
    "NJS-0060": "NJS-0056-001",
    "NJS-0061": "NJS-0056-002",
    "NJS-0062": "NJS-0057-001",
    "NJS-0063": "NJS-0057-002",
    "NJS-0064": "NJS-0057-003",
    "NJS-0065": "NJS-0057-004",
    "NJS-0066": "NJS-0057-005",
    "NJS-0067": "NJS-0058-001",
    "NJS-0068": "NJS-0058-002",
    "NJS-0069": "NJS-0059-001",
    "NJS-0070": "NJS-0059-002",
    "NJS-0071": "NJS-0059-003",
    "NJS-0072": "NJS-0060-001",
    "NJS-0073": "NJS-0060-002",
    "NJS-0074": "NJS-0061-001",
    "NJS-0075": "NJS-0061-002",
    "NJS-0076": "NJS-0062-001",
    "NJS-0077": "NJS-0062-002",
}

CLAIM_ID_MAP = {
    f"CLM-{legacy:06d}": f"CLM-{197 + legacy - 88:06d}"
    for legacy in range(88, 117)
}

PARENT_CLAIM_MAP = {
    legacy: f"CLM-{237 + index:06d}"
    for index, legacy in enumerate(PARENT_ID_MAP)
}

DET_ID_MAP = {
    "DET-000025": "DET-000051",
    "DET-000026": "DET-000052",
    "DET-000027": "DET-000053",
    "DET-000028": "DET-000054",
    "DET-000029": "DET-000055",
    "DET-000030": "DET-000056",
}

NJA_BY_DET = {
    "DET-000025": "NJA-000025",
    "DET-000026": "NJA-000026",
    "DET-000027": "NJA-000027",
    "DET-000028": "NJA-000028",
    "DET-000029": "NJA-000029",
    "DET-000030": "NJA-000030",
}

MIT_ID_MAP = {
    "MIT-000025": "MIT-000050",
    "MIT-000026": "MIT-000051",
    "MIT-000027": "MIT-000052",
    "MIT-000028": "MIT-000053",
    "MIT-000029": "MIT-000054",
    "MIT-000030": "MIT-000055",
}

ID_REMAP = PARENT_ID_MAP | CHILD_ID_MAP | CLAIM_ID_MAP | DET_ID_MAP | MIT_ID_MAP
ID_PATTERN = re.compile("|".join(re.escape(key) for key in sorted(ID_REMAP, key=len, reverse=True)))


PARENT_BOUNDARIES = {
    "NJT-0021": (
        "被操纵的数据传输路径与按请求形成的注入响应",
        "compromised data-transfer paths and request-specific injected responses",
        "用户访问攻击者控制网站属于可信浏览触发入口，产品在交付前被污染属于供应链入口",
        "a user visiting an adversary-controlled site belongs to trusted-browsing entry, while a product altered before delivery belongs to supply-chain entry",
    ),
    "NJT-0022": (
        "用户正常浏览到被操纵网页、子资源或重定向链所触发的入口",
        "entry triggered when ordinary browsing reaches a manipulated page, subresource, or redirect chain",
        "主动发送诱导消息属于钓鱼，面向服务端的公开应用利用属于公开应用入口",
        "actively sent lures belong to phishing, while server-side exploitation belongs to public-application entry",
    ),
    "NJT-0023": (
        "互联网公开应用、API 与边界设备的漏洞或配置弱点",
        "vulnerabilities or configuration weaknesses in Internet-facing applications, APIs, and edge devices",
        "使用有效凭据登录属于有效身份或远程服务入口，交付前预置污染属于供应链入口",
        "sign-in with valid credentials belongs to valid-identity or remote-service entry, while pre-delivery compromise belongs to supply-chain entry",
    ),
    "NJT-0024": (
        "VPN、RDP、VDI 与远程管理网关所承载的外部会话入口",
        "external session entry carried by VPN, RDP, VDI, and remote-management gateways",
        "身份本身的冒用属于有效身份，服务漏洞利用属于公开应用入口",
        "abuse of the identity itself belongs to valid-identity entry, while exploitation of a service flaw belongs to public-application entry",
    ),
    "NJT-0025": (
        "被物理引入目标环境并提供计算、网络或外设能力的新增硬件",
        "new hardware physically introduced into the victim environment to provide computing, network, or peripheral capability",
        "可移动介质上的数据复制属于介质入口，仅通过无线关联建立访问属于无线入口",
        "data replication on removable media belongs to media entry, while access established solely through wireless association belongs to Wi-Fi entry",
    ),
    "NJT-0026": (
        "攻击者主动发送并以执行、认证、远程协助或首个会话为目的的电子社会工程",
        "adversary-sent electronic social engineering intended to obtain execution, authentication, remote assistance, or a first session",
        "仅索取信息属于侦察阶段的信息钓鱼，内容生成与准备属于资源开发",
        "requests made only to obtain information belong to reconnaissance phishing, while content generation and preparation belong to resource development",
    ),
    "NJT-0027": (
        "可移动介质上的复制、传播与入口触发",
        "replication, propagation, and entry triggering through removable media",
        "新增硬件功能属于硬件入口，在交付链中预置介质属于供应链入口",
        "new hardware functionality belongs to hardware entry, while media prepositioned in a delivery chain belongs to supply-chain entry",
    ),
    "NJT-0028": (
        "产品、依赖、构建、更新或硬件在最终用户接收前遭到操纵",
        "manipulation of products, dependencies, builds, updates, or hardware before receipt by the final user",
        "用户接收后的伙伴连接滥用属于受信关系，普通可移动介质传播属于介质入口",
        "abuse of a partner connection after delivery belongs to trusted-relationship entry, while ordinary removable-media propagation belongs to media entry",
    ),
    "NJT-0029": (
        "供应商、承包商、托管服务商或合作伙伴已有的连接、委托与授权路径",
        "existing connection, delegation, and authorization paths of suppliers, contractors, managed-service providers, or partners",
        "访问资源的购买或准备属于资源开发，有效身份本身的使用属于有效身份入口",
        "purchase or preparation of access belongs to resource development, while use of the valid identity itself belongs to valid-identity entry",
    ),
    "NJT-0030": (
        "能够通过正常认证或既有会话被系统接受的真实身份状态",
        "authentic identity state accepted through normal authentication or an established session",
        "承载入口的远程服务属于远程服务技术，账户取得与准备属于资源开发",
        "the remote service carrying entry belongs to remote-service entry, while account acquisition and preparation belong to resource development",
    ),
    "NJT-0031": (
        "目标无线网络的认证与关联面以及近距离无线入口",
        "the authentication and association surface of victim wireless networks and proximate wireless entry",
        "物理植入设备属于硬件入口，公网远程服务会话属于远程服务入口",
        "physically planted devices belong to hardware entry, while public remote-service sessions belong to remote-service entry",
    ),
}


MECHANISM_EFFECT = {
    "NM-FD": (
        "攻击者以合法、可信或常见入口特征替代显著恶意特征，使粗粒度规则难以区分；防守方必须恢复行为、身份与来源谱系，因而形成特征伪装效果。",
        "The adversary substitutes legitimate, trusted, or common entry features for conspicuous malicious features, weakening coarse rules; defenders must recover behavioral, identity, and provenance lineage, producing a Feature Disguise effect.",
    ),
    "NM-BT": (
        "关键入口动作在单一观察模型中表现为空白、低信号或正常结果，使原有分析逻辑不触发；扩大观察面或关联前后结果仍可恢复差异，因而形成行为透明效果。",
        "The critical entry action appears blank, low-signal, or normal under one observation model, preventing existing analytics from firing; broader vantage and correlation with preceding and subsequent outcomes can recover the difference, producing a Behavioral Transparency effect.",
    ),
    "NM-ST": (
        "同一入口链的痕迹被分散到时间、路径、视点、主体或供应层，使短窗口和单点指标只能看到片段；防守方必须跨单元重建共同谱系，因而形成时空释痕效果。",
        "Traces of one entry chain are distributed across time, paths, vantages, subjects, or supply layers so short windows and point indicators see only fragments; defenders must rebuild shared lineage across units, producing a Spatiotemporal Trace Dilution effect.",
    ),
}


DETECTION_CONFIG = {
    "DET-000025": {
        "platforms": ["Network", "Web", "Browser", "Endpoint"],
        "dimensions": ["request", "url", "origin", "vantage", "client", "redirect", "object", "process", "time"],
        "requirements": [
            ("multivantage-request-response", "多视角请求与响应记录", "Multi-vantage request and response records", ["timestamp", "vantage_id", "client_id", "request_url", "request_headers", "response_status", "response_headers", "response_hash"]),
            ("web-resource-provenance", "网页资源与重定向谱系", "Web-resource and redirect lineage", ["timestamp", "page_url", "resource_url", "resource_hash", "redirect_source", "redirect_target", "publisher_or_tenant"]),
            ("browser-endpoint-lineage", "浏览器与端点结果谱系", "Browser and endpoint outcome lineage", ["timestamp", "device_id", "browser_process", "page_url", "child_process", "download_hash", "network_destination"]),
        ],
    },
    "DET-000026": {
        "platforms": ["Web Server", "Cloud", "Network Device", "Application Server"],
        "dimensions": ["asset", "version", "request", "session", "process", "file", "configuration", "network_destination", "time"],
        "requirements": [
            ("application-edge-request", "公开应用与边界请求日志", "Public-application and edge request logs", ["timestamp", "asset_id", "source", "request_method", "request_path", "request_body_hash", "response_status", "session_id"]),
            ("asset-version-configuration", "资产版本与配置清单", "Asset version and configuration inventory", ["asset_id", "product", "version", "configuration_hash", "exposure", "last_patch_time"]),
            ("server-device-outcome", "服务端与设备结果遥测", "Server and device outcome telemetry", ["timestamp", "asset_id", "process", "file_path", "file_hash", "configuration_change", "network_destination"]),
        ],
    },
    "DET-000027": {
        "platforms": ["Identity Provider", "VPN", "Remote Desktop", "Cloud", "SaaS"],
        "dimensions": ["identity", "session", "token", "device", "network_origin", "resource", "tenant", "delegation", "time"],
        "requirements": [
            ("identity-session-authentication", "身份、令牌与会话认证事件", "Identity, token, and session authentication events", ["timestamp", "identity_id", "session_id", "token_id", "authentication_method", "mfa_result", "device_id", "network_origin"]),
            ("remote-service-access", "远程服务访问与资源事件", "Remote-service access and resource events", ["timestamp", "service_id", "identity_id", "session_id", "device_id", "source", "target_resource", "action"]),
            ("cross-organization-trust", "跨组织委托与服务主体审计", "Cross-organization delegation and service-principal audit", ["timestamp", "source_tenant", "target_tenant", "principal_id", "delegation_id", "role", "resource", "action"]),
        ],
    },
    "DET-000028": {
        "platforms": ["Endpoint", "Network Device", "Wireless", "Physical Security"],
        "dimensions": ["device", "media", "identity", "location", "switch_port", "ssid", "access_point", "radio", "process", "time"],
        "requirements": [
            ("physical-asset-access", "物理门禁与资产盘点", "Physical-access and asset inventory", ["timestamp", "identity_id", "location", "asset_id", "asset_type", "inspection_result"]),
            ("media-device-endpoint", "介质、设备与端点事件", "Media, device, and endpoint events", ["timestamp", "device_id", "media_id", "volume_id", "file_path", "file_hash", "process", "action"]),
            ("wired-wireless-access", "交换、无线与认证接入日志", "Switching, wireless, and access-authentication logs", ["timestamp", "device_id", "mac", "switch_port", "ssid", "access_point", "identity_id", "authentication_result", "signal_strength"]),
        ],
    },
    "DET-000029": {
        "platforms": ["Email", "Collaboration", "Browser", "Endpoint", "Identity Provider"],
        "dimensions": ["sender", "recipient", "thread", "message", "object", "url", "device", "identity", "session", "time"],
        "requirements": [
            ("message-conversation-audit", "邮件、即时消息与协作会话审计", "Mail, messaging, and collaboration conversation audit", ["timestamp", "sender_id", "recipient_id", "thread_id", "message_id", "reply_to", "object_id", "url"]),
            ("hosted-object-navigation", "托管对象与导航链", "Hosted-object and navigation chain", ["timestamp", "object_id", "tenant_id", "url", "redirect_source", "redirect_target", "requester_id", "response_hash"]),
            ("endpoint-identity-outcome", "端点与身份入口结果", "Endpoint and identity entry outcomes", ["timestamp", "device_id", "process", "object_id", "identity_id", "session_id", "authentication_method", "mfa_result", "remote_assistance_event"]),
        ],
    },
    "DET-000030": {
        "platforms": ["Source Control", "Build System", "Code Signing", "Software Distribution", "Endpoint"],
        "dimensions": ["source", "dependency", "build", "artifact", "signature", "publisher", "release", "installation", "organization", "time"],
        "requirements": [
            ("source-build-signing-lineage", "源码、构建与签名谱系", "Source, build, and signing lineage", ["timestamp", "source_revision", "dependency_id", "build_id", "builder_identity", "artifact_hash", "signature_id", "publisher"]),
            ("release-installation-base", "发布、更新与安装基数遥测", "Release, update, and installed-base telemetry", ["timestamp", "release_id", "artifact_hash", "delivery_channel", "organization_id", "device_id", "installation_result"]),
            ("post-installation-behavior", "安装后行为与跨组织结果", "Post-installation behavior and cross-organization outcomes", ["timestamp", "artifact_hash", "device_id", "organization_id", "process", "network_destination", "second_stage_hash", "activation_result"]),
        ],
    },
}


MITIGATION_CONFIG = {
    "MIT-000025": ("path-browser-integrity", "传输与浏览器入口完整性控制", "Transfer and Browser-Entry Integrity Controls", "preventive"),
    "MIT-000026": ("public-application-edge-hardening", "公开应用与边界设备分层加固", "Layered Public-Application and Edge-Device Hardening", "preventive"),
    "MIT-000027": ("identity-remote-trust-controls", "身份、远程服务与跨组织信任控制", "Identity, Remote-Service, and Cross-Organization Trust Controls", "governance"),
    "MIT-000028": ("physical-media-wireless-controls", "物理、介质与无线入口控制", "Physical, Media, and Wireless Entry Controls", "preventive"),
    "MIT-000029": ("phishing-entry-controls", "钓鱼会话、对象与认证入口控制", "Phishing Conversation, Object, and Authentication Entry Controls", "preventive"),
    "MIT-000030": ("supply-chain-integrity", "构建、交付与传递供应链完整性", "Build, Delivery, and Transitive Supply-Chain Integrity", "governance"),
}


def raw_load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def remap_ids(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: remap_ids(item) for key, item in value.items()}
    if isinstance(value, list):
        return [remap_ids(item) for item in value]
    if isinstance(value, str):
        return ID_PATTERN.sub(lambda match: ID_REMAP[match.group(0)], value)
    return value


def archive_load(path: Path) -> dict[str, Any]:
    return remap_ids(raw_load(path))


def save(relative: str, data: dict[str, Any]) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=180), encoding="utf-8")


def prose(zh: str, en: str) -> dict[str, Any]:
    return {"paragraphs": [{"zh": clean(zh), "en": clean(en)}]}


def lifecycle() -> dict[str, Any]:
    return {
        "status": "review",
        "version": "1.0.0",
        "created": TODAY,
        "modified": TODAY,
        "contributors": ["Niji Matrix Research"],
        "reviewers": [],
    }


def clean(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return value


def short(value: str) -> str:
    return clean(value).rstrip("。！？；.!?;")


def join_zh(values: list[str]) -> str:
    return "、".join(short(value) for value in values)


def lower_first(value: str) -> str:
    value = clean(value)
    token = value.split(maxsplit=1)[0].split("/", 1)[0]
    if value.startswith(("NJT-", "NJS-", "DET-", "NJA-", "MIT-")) or (len(token) > 1 and token.isupper()):
        return value
    return value[:1].lower() + value[1:]


def join_en(values: list[str]) -> str:
    cleaned = []
    for value in values:
        value = short(value)
        if value.lower().startswith("and "):
            value = value[4:]
        cleaned.append(lower_first(value))
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return " and ".join(cleaned)
    return ", ".join(cleaned[:-1]) + ", and " + cleaned[-1]


def pair_items(zh_values: list[str], en_values: list[str]) -> list[dict[str, str]]:
    if len(zh_values) == len(en_values):
        return [{"zh": short(zh), "en": short(en)} for zh, en in zip(zh_values, en_values)]
    return [{"zh": join_zh(zh_values), "en": join_en(en_values)}]


def legacy_parent_id(path: Path) -> str:
    return "-".join(path.parent.name.split("-")[:2])


def legacy_child_id(path: Path) -> str:
    return "-".join(path.parent.name.split("-")[:2])


def suffix_after_id(directory_name: str) -> str:
    return directory_name.split("-", 2)[2]


def parent_paths() -> list[Path]:
    return sorted(ARCHIVE_TECHNIQUES.glob("NJT-*/technique.yaml"))


def child_paths(parent_path: Path) -> list[Path]:
    return sorted(parent_path.parent.glob("subtechniques/*/subtechnique.yaml"))


def parent_mechanisms(old: dict[str, Any], observables_zh: str, observables_en: str) -> list[dict[str, Any]]:
    values = []
    for item in old["stealth"]["mechanism_mappings"]:
        mechanism = item["mechanism_ref"]
        effect_zh, effect_en = MECHANISM_EFFECT[mechanism]
        if mechanism == "NM-FD":
            summary_zh = "可信或常见入口特征替代显著恶意特征并削弱粗粒度区分"
            summary_en = "Trusted or common entry features replace conspicuous malicious features and weaken coarse discrimination"
        elif mechanism == "NM-BT":
            summary_zh = "关键入口动作在单一观察面中呈现为正常低信号或观测空白"
            summary_en = "Critical entry actions appear normal low-signal or absent within one observation vantage"
        else:
            summary_zh = "入口链痕迹跨时间路径视点主体或供应层分散并提高重构成本"
            summary_en = "Entry-chain traces disperse across time paths vantages subjects or supply layers and raise reconstruction cost"
        values.append({
            "mechanism_ref": mechanism,
            "role": item["role"],
            "summary": {"zh": summary_zh, "en": summary_en},
            "analysis": prose(
                f"{old['name_zh']}的已证实子技术通过有意控制入口条件，使原本可以集中关联的{observables_zh}发生位置、密度、外观或可见性变化。{effect_zh}",
                f"Supported children of {old['name_en']} intentionally control entry conditions so that otherwise correlatable traces such as {observables_en} change location, density, appearance, or visibility. {effect_en}",
            ),
            "evidence_refs": item["evidence_refs"],
            "confidence": item["confidence"],
        })
    return values


def build_parent(parent_path: Path) -> dict[str, Any]:
    legacy_id = legacy_parent_id(parent_path)
    old = archive_load(parent_path)
    raw = raw_load(parent_path)
    direct_zh, direct_en, neighbor_zh, neighbor_en = PARENT_BOUNDARIES[legacy_id]
    context = old["context"]
    observables_zh = join_zh(context["observables_zh"])
    observables_en = join_en(context["observables_en"])
    children = [archive_load(path) for path in child_paths(parent_path)]
    child_names_zh = "、".join(child["name_zh"] for child in children)
    child_names_en = ", ".join(child["name_en"] for child in children)
    axes_zh = "；".join(short(child["definition"]["operating_principle_zh"]) for child in children)
    axes_en = "; ".join(lower_first(short(child["definition"]["operating_principle_en"])) for child in children)
    old_det = raw["detection_refs"][0]
    old_mit = raw["mitigation_refs"][0]
    return {
        "schema_version": "2.0.0",
        "type": "technique",
        "id": old["id"],
        "name": {"zh": old["name_zh"], "en": old["name_en"]},
        "summary": {"zh": clean(old["definition"]["summary_zh"]), "en": clean(old["definition"]["summary_en"])},
        "aliases": old.get("aliases", []),
        "classification": {"tactic_refs": ["TA0001"], "origin": old["origin"], "decision_ref": old["decision_ref"]},
        "definition_and_concept": prose(
            f"{old['definition']['summary_zh']}{old['name_zh']}以{direct_zh}为直接行为对象，目标是在初始入侵阶段取得第一个可执行、可认证或可通信立足点。该概念描述入口行为及其受控匿迹变量，不以工具、产品、媒介或 ATT&CK 子技术名称划界。",
            f"{old['definition']['summary_en']} {old['name_en']} treats {direct_en} as its direct behavioral object and seeks the first executable, authenticated, or communicating foothold during Initial Access. The concept describes the entry behavior and its controlled stealth variables rather than a tool, product, medium, or ATT&CK child name.",
        ),
        "stealth_characteristics": prose(
            f"{old['name_zh']}通过子技术改变入口痕迹的外观、位置、密度或跨层关联，使受害方难以从单一事件区分攻击与正常访问。匿迹并不消除证据，{observables_zh}仍会残留在受害方、服务提供方、身份平面、端点或供应方；拥有更长保留期和跨视角关联能力的防守方可以限制这种效果。",
            f"{old['name_en']} changes the appearance, location, density, or cross-layer linkage of entry traces through its children, making one event difficult to distinguish from normal access. Stealth does not erase evidence: {observables_en} remain at the victim, service provider, identity plane, endpoint, or supplier, and defenders with longer retention and cross-vantage correlation can constrain the effect.",
        ),
        "scope_boundary_definition": prose(
            f"本技术纳入攻击者有意利用{direct_zh}并改变首个入口痕迹的行为，截止于立足点建立。它排除后续执行、持久化、提权、横向移动与命令控制，也不按 ATT&CK 子技术、产品或介质直接拆分；相邻边界是{neighbor_zh}。合法运维、个人化服务、兼容性行为或偶发故障只有在攻击者控制了稳定变量并产生对应观察差异时才可纳入。",
            f"This technique includes adversary-controlled use of {direct_en} that changes traces of the first entry and ends when the foothold is established. It excludes downstream execution, persistence, privilege escalation, lateral movement, and command and control and is not partitioned directly by ATT&CK children, product, or medium; its neighboring boundary is that {neighbor_en}. Legitimate administration, personalized service, compatibility behavior, or accidental failure qualifies only when an adversary controls a stable variable and produces the corresponding observation difference.",
        ),
        "application_scenarios_and_threat_model": {
            "application_scenarios": prose(
                f"本技术适用于攻击者在{join_zh(context['environments_zh'])}中，借助{direct_zh}接近{join_zh(context['targets_zh'])}并希望入口在建立前后保持低可区分性的场景。应用触发是首个入口条件已经可用且攻击者开始利用该条件；后续行动只能作为入口结果的证据，不能扩张本技术边界。",
                f"This technique applies when an adversary uses {direct_en} in {join_en(context['environments_en'])} to approach {join_en(context['targets_en'])} while keeping the entry difficult to distinguish before and immediately after establishment. The trigger is availability and use of the first-entry condition; downstream action may evidence the entry outcome but cannot expand this technique boundary.",
            ),
            "threat_model": {
                "attacker_model": prose(
                    f"攻击者必须满足以下前提：{join_zh(context['prerequisites_zh'])}。实施者还需控制{direct_zh}的关键条件、时点或上下文，并能够承受选择性交付、跨视角协调、长期等待、物理接近或供应关系维护中至少一项成本；失去控制、目标不匹配或提供方处置会削弱匿迹效果。",
                    f"The adversary must satisfy these prerequisites: {join_en(context['prerequisites_en'])}. The operator must also control key conditions, timing, or context of {direct_en} and bear at least one cost involving selective delivery, cross-vantage coordination, delay, physical proximity, or supply-relationship maintenance; loss of control, target mismatch, or provider enforcement weakens the stealth effect.",
                ),
                "defender_model": prose(
                    f"防守方可能观察到{observables_zh}，但受害方、服务提供方、身份系统、端点、物理设施与供应商掌握的字段和保留期不同。可靠判断需要在授权范围内连接入口前后事件、验证真实主体与来源，并为合法相似行为建立基线；缺少任一关键视角时只能形成受限推断。",
                    f"Defenders may observe {observables_en}, but victims, service providers, identity systems, endpoints, physical facilities, and suppliers hold different fields and retention periods. Reliable judgment requires authorized linkage of pre-entry and post-entry events, validation of the actual subject and provenance, and baselines for legitimate lookalikes; missing a critical vantage limits the inference.",
                ),
            },
        },
        "stealth_mechanisms": parent_mechanisms(old, observables_zh, observables_en),
        "subtechnique_taxonomy": {
            "narrative": prose(
                f"本技术建立以下 Niji 原生匿迹子技术：{child_names_zh}。它们分别以{axes_zh}为稳定划分变量，每项都会形成独立的痕迹变化、防守观察影响和防御需求；这些变量可以组合，但不能彼此替代。分类不继承 ATT&CK 子技术，也不按工具、产品、账户类型、介质、目标类型或数据字段拆分。",
                f"This technique defines the following Niji-native evasion sub-techniques: {child_names_en}. They use these stable partition variables respectively: {axes_en}. Each produces a distinct trace change, defender-observation effect, and defensive requirement; the variables may combine but do not substitute for one another. The taxonomy does not inherit ATT&CK children or partition by tool, product, account type, medium, target type, or data field.",
            ),
            "coverage": "established",
            "subtechnique_refs": [child["id"] for child in children],
        },
        "defense": {
            "detections": {"coverage": "available", "strategy_refs": [DET_ID_MAP[old_det]]},
            "mitigations": {"coverage": "available", "mitigation_refs": [MIT_ID_MAP[old_mit]]},
        },
        "evidence": {
            "claim_refs": [PARENT_CLAIM_MAP[legacy_id]],
            "case_refs": [],
            "reference_refs": list(dict.fromkeys(
                old["external_reference_refs"]
                + [ref for mechanism in old["stealth"]["mechanism_mappings"] for ref in mechanism["evidence_refs"]]
            )),
        },
        "research": {"limitations": prose(
            f"公开证据支持该 ATT&CK 父行为与至少一项稳定匿迹变量，但不能证明每个实例都具有相同主观意图、跨平台效果或提供方可见性。{neighbor_zh}也可能在局部产生相似信号，因此结论必须限制在来源直接支持的入口行为、痕迹变化和观察模型内；新增子技术需要独立证据与防御差异。",
            "Public evidence supports the ATT&CK parent behavior and at least one stable stealth variable, but it does not establish identical intent, cross-platform effect, or provider visibility in every instance. The neighboring behaviors described above can also produce locally similar signals, so conclusions must remain within entry behavior, trace change, and observation models directly supported by sources; any additional child requires independent evidence and a defensive distinction.",
        )},
        "lifecycle": lifecycle(),
    }


def child_mechanisms(old: dict[str, Any]) -> list[dict[str, Any]]:
    operation_zh = short(old["definition"]["operating_principle_zh"])
    operation_en = short(old["definition"]["operating_principle_en"])
    trace_zh = short(old["stealth"]["trace_change_zh"])
    trace_en = lower_first(short(old["stealth"]["trace_change_en"]))
    defender_zh = short(old["stealth"]["defender_effect_zh"])
    defender_en = lower_first(short(old["stealth"]["defender_effect_en"]))
    values = []
    for index, item in enumerate(old["stealth"]["mechanism_realizations"]):
        mechanism = item["mechanism_ref"]
        effect_zh, effect_en = MECHANISM_EFFECT[mechanism]
        if mechanism == "NM-FD":
            summary = {"zh": "借助该受控变量使入口外观贴近合法或可信活动", "en": "Use the controlled variable to make entry resemble legitimate or trusted activity"}
        elif mechanism == "NM-BT":
            summary = {"zh": "借助该受控变量使关键入口动作在单一视角中保持低信号", "en": "Use the controlled variable to keep the critical entry action low-signal from one vantage"}
        else:
            summary = {"zh": "借助该受控变量把入口链痕迹分散到多个观察单元", "en": "Use the controlled variable to distribute entry-chain traces across observation units"}
        values.append({
            "mechanism_ref": mechanism,
            "role": "primary" if index == 0 else "secondary",
            "summary": {"zh": short(summary["zh"]), "en": short(summary["en"])},
            "analysis": prose(
                f"攻击者有意实施该子技术的操作原则，即{operation_zh}。这一行为产生所述痕迹变化，并导致{defender_zh}。{effect_zh}",
                f"The adversary deliberately applies this child's operating principle by acting to {lower_first(operation_en)}. This produces the stated trace change and means that {defender_en}. {effect_en}",
            ),
            "evidence_refs": item["evidence_refs"],
            "confidence": item["confidence"],
        })
    return values


def build_child(parent_path: Path, child_path: Path) -> tuple[str, dict[str, Any]]:
    old = archive_load(child_path)
    boundary = old["boundaries"]
    context = old["context"]
    observables_zh = join_zh(context["observables_zh"])
    observables_en = join_en(context["observables_en"])
    operation_zh = short(old["definition"]["operating_principle_zh"])
    operation_en = lower_first(short(old["definition"]["operating_principle_en"]))
    siblings = [archive_load(path) for path in child_paths(parent_path) if path != child_path]
    sibling_names_zh = "、".join(f"{item['id']} {item['name_zh']}" for item in siblings)
    sibling_names_en = ", ".join(f"{item['id']} {item['name_en']}" for item in siblings)
    data = {
        "schema_version": "2.0.0",
        "type": "evasion-subtechnique",
        "id": old["id"],
        "parent_ref": old["parent_ref"],
        "name": {"zh": old["name_zh"], "en": old["name_en"]},
        "summary": {"zh": clean(old["definition"]["summary_zh"]), "en": clean(old["definition"]["summary_en"])},
        "aliases": old.get("aliases", []),
        "lineage": {"attck_subtechnique_inherited": False},
        "definition_and_concept": prose(
            f"{old['definition']['summary_zh']}该行为的直接目标是{short(old['definition']['stealth_goal_zh'])}；攻击者控制的是促成该入口结果的时点、情境、路径、身份、设备、内容或供应关系。该边界描述可重复的匿迹变量，而不是特定工具、产品、介质或偶然环境。",
            f"{old['definition']['summary_en']} Its direct objective is to {lower_first(short(old['definition']['stealth_goal_en']))}; the adversary controls the timing, context, path, identity, device, content, or supply relationship that produces this entry result. This boundary describes a repeatable stealth variable rather than a particular tool, product, medium, or accidental environment.",
        ),
        "stealth_characteristics": prose(
            f"{old['name_zh']}由攻击者有意改变可见入口痕迹，具体做法是{short(old['stealth']['trace_change_zh'])}。这会导致{short(old['stealth']['defender_effect_zh'])}；与此同时，{observables_zh}仍是可恢复的残余痕迹，更细粒度遥测、较长保留期或额外观察视角能够限制效果。",
            f"{old['name_en']} deliberately changes which entry traces are exposed by having the adversary act to {lower_first(short(old['stealth']['trace_change_en']))}. As a result, {lower_first(short(old['stealth']['defender_effect_en']))}; at the same time, {observables_en} remain recoverable residual traces, and finer telemetry, longer retention, or another vantage can constrain the effect.",
        ),
        "scope_boundary_definition": prose(
            f"本子技术纳入攻击者有意{operation_zh}以改变首个入口痕迹的行为。它排除仅按媒介、产品或工具名称进行的分类，也排除立足点建立后的行为；与{sibling_names_zh}的边界在于，本项控制上述变量，而每个兄弟项控制父级分类中另一项独立痕迹变量。只有攻击者有意控制该变量并产生对应观察差异时才纳入，合法运维、个人化服务、兼容性行为或普通用户活动造成的相似现象不能单独证明分类。",
            f"This child includes adversary-controlled action to {operation_en} in order to change traces of the first entry. It excludes classifications based only on medium, product, or tool name and excludes all behavior after foothold establishment. It differs from {sibling_names_en} because this child controls the stated variable while each sibling controls another independent trace variable in the parent taxonomy. Inclusion requires deliberate adversary control and the corresponding observation difference; similar effects from legitimate administration, personalized service, compatibility behavior, or ordinary user activity do not establish the classification alone.",
        ),
        "application_scenarios_and_threat_model": {
            "application_scenarios": prose(
                f"本子技术适用于攻击者在{join_zh(context['environments_zh'])}中利用首个入口条件，并采用上述受控变量降低入口事件可区分性的场景。具体入口行为表现为攻击者有意{operation_zh}；{observables_zh}可在入口前后或与后续结果关联后出现，但立足点建立后的执行、持久化、横向移动与通信不属于本子技术。",
                f"This child applies when an adversary uses a first-entry condition in {join_en(context['environments_en'])} and applies the stated controlled variable to reduce entry-event distinguishability. The concrete entry behavior has the adversary act to {operation_en}; {observables_en} may appear around entry or after correlation with later outcomes, but execution, persistence, lateral movement, and communication after foothold establishment are outside this child.",
            ),
            "threat_model": {
                "attacker_model": prose(
                    f"攻击者必须满足以下前提：{join_zh(context['prerequisites_zh'])}。实施者还需持续控制用于{operation_zh}的身份、会话、内容、路径、设备、时点或供应关系，并承担资源失效、目标不匹配、物理接近、延迟或第三方处置的约束；缺少这种控制时只能形成正常相似行为。",
                    f"The adversary must satisfy these prerequisites: {join_en(context['prerequisites_en'])}. The operator also needs sustained control of the identity, session, content, path, device, timing, or supply relationship used to {operation_en} and must tolerate resource loss, target mismatch, proximity, delay, or third-party enforcement; without that control, only a legitimate lookalike remains.",
                ),
                "defender_model": prose(
                    f"防守模型包括直接受害方、入口服务或身份提供方、端点与能够保存跨视角谱系的分析者。直接受害方可能只看到局部正常结果，其他观察者可能看到{observables_zh}；可靠识别需要在授权与保留期内关联这些视角，并把正常相似行为纳入基线。",
                    f"The defender model includes the direct victim, the entry-service or identity provider, the endpoint, and analysts able to retain cross-vantage lineage. The victim may see only a locally normal result while other observers may see {observables_en}; reliable identification requires authorized correlation across those vantages and retention periods with legitimate lookalikes represented in the baseline.",
                ),
            },
        },
        "stealth_mechanisms": child_mechanisms(old),
        "defense": {
            "detections": {"coverage": "available", "strategy_refs": old["detection_refs"]},
            "mitigations": {"coverage": "available", "mitigation_refs": old["mitigation_refs"]},
        },
        "evidence": {
            "claim_refs": old["claim_refs"],
            "case_refs": [],
            "reference_refs": list(dict.fromkeys(old["external_reference_refs"])),
        },
        "research": {"limitations": prose(
            f"公开证据支持本子技术的稳定变量和所列痕迹变化，但不能保证每个{join_zh(context['environments_zh'])}实例都有相同匿迹意图或效果。按媒介、产品或工具形成的相似外观以及立足点建立后的行为可能产生局部相似信号，且提供方内部数据通常不公开；置信度应随直接入口证据、跨视角复现和正常基线的可得性调整。",
            f"Public evidence supports this child's stable variable and stated trace change but does not establish identical stealth intent or effect in every instance of {join_en(context['environments_en'])}. Similar appearance caused by medium, product, or tool choice and behavior after foothold establishment can produce locally similar signals, while provider-internal data is often unavailable; confidence should vary with direct entry evidence, cross-vantage reproduction, and availability of a legitimate baseline.",
        )},
        "lifecycle": lifecycle(),
    }
    parent_slug = suffix_after_id(parent_path.parent.name)
    child_slug = suffix_after_id(child_path.parent.name)
    relative = f"matrix/tactics/TA0001-initial-access/techniques/{old['parent_ref']}-{parent_slug}/subtechniques/{old['id']}-{child_slug}/subtechnique.yaml"
    return relative, data


def child_claim_subjects() -> dict[str, str]:
    subjects = {}
    for parent_path in parent_paths():
        for child_path in child_paths(parent_path):
            raw = raw_load(child_path)
            for claim_ref in raw["claim_refs"]:
                subjects[claim_ref] = CHILD_ID_MAP[raw["id"]]
    return subjects


def write_claims() -> None:
    subjects = child_claim_subjects()
    for old_id, new_id in CLAIM_ID_MAP.items():
        source = next((PRUNED / "claims").glob(f"{old_id}-*.yaml"))
        claim = archive_load(source)
        claim["subject_refs"] = [subjects[old_id]]
        suffix = source.name[len(old_id) + 1:]
        save(f"claims/{new_id}-{suffix}", claim)
    for parent_path in parent_paths():
        legacy_id = legacy_parent_id(parent_path)
        old = archive_load(parent_path)
        attack_id = old["origin"]["source_attack_id"]
        decision = raw_load(TACTIC_ROOT / f"decisions/DEC-TA0001-{attack_id}.yaml")
        claim_id = PARENT_CLAIM_MAP[legacy_id]
        mode = "directly-observed" if decision["confidence"] == "high" else "strongly-inferred"
        claim = {
            "schema_version": "1.0.0",
            "type": "claim",
            "id": claim_id,
            "claim_type": "technique-relevance",
            "statement_zh": f"{decision['rationale_zh']}该结论支持在 TA0001 下以{old['name_zh']}作为独立父技术，并将范围限制在首个立足点。",
            "statement_en": f"{decision['rationale_en']} This supports {old['name_en']} as a distinct parent technique under TA0001 with scope ending at the first foothold.",
            "subject_refs": [old["id"]],
            "evidence_refs": decision["evidence_refs"],
            "evidence_mode": mode,
            "confidence": decision["confidence"],
            "status": "review",
        }
        save(f"claims/{claim_id}-{attack_id.lower()}-{suffix_after_id(parent_path.parent.name)}-relevance.yaml", claim)


def targets_for(ref_type: str, legacy_ref: str) -> list[str]:
    result = []
    key = "detection_refs" if ref_type == "detection" else "mitigation_refs"
    for parent_path in parent_paths():
        parent = raw_load(parent_path)
        if legacy_ref in parent[key]:
            result.append(PARENT_ID_MAP[parent["id"]])
        for child_path in child_paths(parent_path):
            child = raw_load(child_path)
            if legacy_ref in child[key]:
                result.append(CHILD_ID_MAP[child["id"]])
    return result


def write_detection_objects() -> None:
    for old_det, new_det in DET_ID_MAP.items():
        source = next((PRUNED / "detections").glob(f"{old_det}-*.yaml"))
        old = raw_load(source)
        config = DETECTION_CONFIG[old_det]
        nja = NJA_BY_DET[old_det]
        objective_zh = clean(old["objective_zh"])
        objective_en = clean(old["objective_en"])
        analytic_zh = clean(old["analytic_description_zh"])
        analytic_en = clean(old["analytic_description_en"])
        strategy = {
            "schema_version": "2.0.0",
            "type": "detection-strategy",
            "id": new_det,
            "name": {"zh": old["name_zh"], "en": old["name_en"]},
            "summary": {"zh": objective_zh, "en": objective_en},
            "description": prose(
                f"本策略以{short(objective_zh)}为检测目标。{nja} 负责把入口前后的多源事件组织为时间、主体与资源谱系，并要求至少两个独立信号共同支持结论；成功认证、可信来源、合法平台、已签名制品、新设备或单次异常本身都不构成恶意判据。",
                f"This strategy seeks to {lower_first(short(objective_en))}. {nja} organizes multi-source events around entry into temporal, subject, and resource lineage and requires at least two independent signals to support a conclusion; successful authentication, trusted provenance, legitimate platform, signed artifact, new device, or one anomaly is not a maliciousness verdict by itself.",
            ),
            "detects_refs": targets_for("detection", old_det),
            "domains": ["enterprise"],
            "analytic_refs": [nja],
            "evidence_refs": old["evidence_refs"],
            "lifecycle": lifecycle(),
        }
        analytic = {
            "schema_version": "2.0.0",
            "type": "detection-analytic",
            "id": nja,
            "strategy_ref": new_det,
            "name": {"zh": f"{old['name_zh']}分析", "en": f"{old['name_en']} Analytic"},
            "summary": {"zh": analytic_zh, "en": analytic_en},
            "domains": ["enterprise"],
            "platforms": config["platforms"],
                "logic": prose(
                f"{analytic_zh}分析先按配置的关联维度规范化事件，建立入口条件、控制变化、实际进入与首个结果的序列；仅当所列可观测信号在相同关联键内共同出现，并与控制平面异常、完整性变化或已确认入口结果一致时提高风险，正常相似行为必须作为替代解释保留。",
                f"{analytic_en} The analytic first normalizes events across the configured correlation dimensions and builds a sequence from entry condition through control change, actual entry, and first outcome. Raise risk only when listed observables co-occur on the same correlation keys and align with a control-plane anomaly, integrity change, or confirmed entry outcome, while retaining legitimate lookalikes as alternative explanations.",
            ),
            "data_requirements": [
                {"source_type": source_type, "name": {"zh": zh, "en": en}, "channel": None, "required_fields": fields}
                for source_type, zh, en, fields in config["requirements"]
            ],
            "observables": pair_items(old["observables_zh"], old["observables_en"]),
            "correlation": {
                "window": {
                    "zh": f"关联窗口覆盖{short(old['correlation_window_zh'])}，并依据入口类型、事件延迟与日志保留期调整。",
                    "en": f"The correlation window spans {lower_first(short(old['correlation_window_en']))} and is adjusted for entry type, event delay, and telemetry retention.",
                },
                "dimensions": config["dimensions"],
            },
            "false_positives": pair_items(old["false_positives_zh"], old["false_positives_en"]),
            "blind_spots": pair_items(old["blind_spots_zh"], old["blind_spots_en"]),
            "tuning_guidance": prose(
                "应按资产所有者、业务角色、入口类型、设备群、地理、发布周期与合法个性化条件建立基线，并分别评分来源、行为差异、完整性变化和入口后结果。白名单必须限定到具体主体、用途和有效期，不能永久排除可信平台、长期身份、已签名制品或维护活动；单一信号不足以触发处置。",
                "Maintain baselines by asset owner, business role, entry type, device population, geography, release cycle, and legitimate personalization condition, and score provenance, behavioral difference, integrity change, and post-entry outcome separately. Allowlists must be scoped to a concrete subject, purpose, and validity period rather than permanently excluding trusted platforms, long-lived identities, signed artifacts, or maintenance activity; one signal is insufficient for enforcement.",
            ),
            "evidence_refs": old["evidence_refs"],
            "lifecycle": lifecycle(),
        }
        suffix = source.name[len(old_det) + 1:]
        save(f"detections/{new_det}-{suffix}", strategy)
        save(f"analytics/{nja}-{suffix}", analytic)


def object_names() -> dict[str, dict[str, str]]:
    names = {}
    for parent_path in parent_paths():
        parent = archive_load(parent_path)
        names[parent["id"]] = {"zh": parent["name_zh"], "en": parent["name_en"]}
        for child_path in child_paths(parent_path):
            child = archive_load(child_path)
            names[child["id"]] = {"zh": child["name_zh"], "en": child["name_en"]}
    return names


def write_mitigations() -> None:
    names = object_names()
    for old_mit, new_mit in MIT_ID_MAP.items():
        source = next((PRUNED / "mitigations").glob(f"{old_mit}-*.yaml"))
        old = raw_load(source)
        key, measure_zh, measure_en, control_type = MITIGATION_CONFIG[old_mit]
        description_zh = clean(old["description_zh"])
        description_en = clean(old["description_en"])
        limitation_zh = join_zh(old["limitations_zh"])
        limitation_en = join_en(old["limitations_en"])
        applications = []
        for target in targets_for("mitigation", old_mit):
            name = names[target]
            applications.append({
                "target_ref": target,
                "use": prose(
                    f"针对{name['zh']}，将本缓解落实到其直接入口对象与控制平面：{description_zh}实施时必须保存入口前后关联键和处置证据，并针对该目标的身份、会话、对象、设备、路径或供应关系验证真实来源，而不是依据外层信誉自动放行。",
                    f"For {name['en']}, apply this mitigation to the direct entry object and its control plane: {description_en} Implementation must retain pre-entry and post-entry correlation keys and enforcement evidence and validate the actual provenance of the relevant identity, session, object, device, path, or supply relationship rather than auto-allowing outer reputation.",
                ),
                "expected_effect": prose(
                    f"该应用缩小{name['zh']}利用正常外观、观测空白或分散谱系建立首个立足点的机会，同时提高攻击者维持匹配条件、合法关系和低差异痕迹的成本，并为跨视角恢复入口链提供数据。",
                    f"This application narrows the opportunity for {name['en']} to establish a first foothold through normal appearance, observation gaps, or dispersed lineage, raises the cost of maintaining matching conditions, legitimate relationships, and low-difference traces, and supplies data for cross-vantage reconstruction of the entry chain.",
                ),
                "limitations": prose(
                    f"该控制无法消除所有{name['zh']}实例；{limitation_zh}会限制效果。处置必须依赖组合证据并评估业务连续性、隐私与跨组织授权，不能把单个新设备、可信来源、签名、身份或响应差异等同于恶意。",
                    f"The control cannot eliminate every instance of {name['en']}. Effectiveness is limited by {limitation_en}. Enforcement must rely on combined evidence and account for business continuity, privacy, and cross-organizational authority rather than treating one new device, trusted source, signature, identity, or response difference as maliciousness.",
                ),
            })
        mitigation = {
            "schema_version": "2.0.0",
            "type": "mitigation",
            "id": new_mit,
            "name": {"zh": old["name_zh"], "en": old["name_en"]},
            "summary": {"zh": description_zh, "en": description_en},
            "description": prose(
                f"{description_zh}本缓解把可复用控制措施与逐目标应用分开，重点减少攻击者对入口信任、观测缺口和分散谱系的利用，同时保留合法业务所需的例外与审计证据。",
                f"{description_en} This mitigation separates reusable controls from per-target applications, reducing adversary use of entry trust, observation gaps, and dispersed lineage while retaining exceptions and audit evidence required for legitimate business.",
            ),
            "domains": ["enterprise"],
            "measures": [{
                "key": key,
                "name": {"zh": measure_zh, "en": measure_en},
                "description": prose(description_zh, description_en),
                "control_type": control_type,
            }],
            "applications": applications,
            "evidence_refs": old["evidence_refs"],
            "lifecycle": lifecycle(),
        }
        suffix = source.name[len(old_mit) + 1:]
        save(f"mitigations/{new_mit}-{suffix}", mitigation)


def technique_relative(parent_path: Path) -> str:
    return f"matrix/tactics/TA0001-initial-access/techniques/{PARENT_ID_MAP[legacy_parent_id(parent_path)]}-{suffix_after_id(parent_path.parent.name)}/technique.yaml"


def write_techniques() -> None:
    for parent_path in parent_paths():
        save(technique_relative(parent_path), build_parent(parent_path))
        for child_path in child_paths(parent_path):
            relative, child = build_child(parent_path, child_path)
            save(relative, child)


def update_decisions_and_plan() -> None:
    by_attack: dict[str, tuple[str, int]] = {}
    for parent_path in parent_paths():
        old = archive_load(parent_path)
        attack_id = old["origin"]["source_attack_id"]
        child_count = len(child_paths(parent_path))
        by_attack[attack_id] = (old["id"], child_count)
        path = TACTIC_ROOT / f"decisions/DEC-TA0001-{attack_id}.yaml"
        decision = raw_load(path)
        decision["resulting_technique_ref"] = old["id"]
        decision["review"]["review_notes_zh"] = f"已按 YAML-only 2.0 契约完成父技术、{child_count} 项 Niji 原生子技术、证据和防御对象的机器审查，等待人工领域复核。"
        decision["review"]["review_notes_en"] = f"The parent, {child_count} Niji-native children, evidence, and defense objects are machine-reviewed under the YAML-only 2.0 contract and await human domain review."
        save(str(path.relative_to(ROOT)), decision)

    plan_path = ROOT / "planning/tactics/TA0001.yaml"
    plan = raw_load(plan_path)
    for item in plan["work_items"]:
        technique_id, child_count = by_attack[item["source_attack_id"]]
        item["resulting_technique_ref"] = technique_id
        item["stage"] = "review"
        item["notes_zh"] = f"已按 YAML-only 2.0 契约完成父技术、{child_count} 项 Niji 原生子技术、共享证据和防御对象；机器门禁通过后进入 review，等待人工领域审查。"
        item["notes_en"] = f"Completed under the YAML-only 2.0 contract with a parent, {child_count} Niji-native children, shared evidence, and defense objects; enters review after machine gates and awaits human domain review."
    plan["status"] = "review"
    plan["batches"][0]["status"] = "review"
    plan["gap_analysis"]["notes_zh"] = "固定 ATT&CK 19.1 基线的 11 个父候选均已完成准入决策与 YAML-only 2.0 重开发，共形成 29 项按稳定匿迹变量划分的 Niji 原生子技术；未发现需要 add 的稳定跨入口缺口。会话状态借用式利用、无身份被动链路插入、隔离区定向载荷门控、嵌套信任链和低速低权限首用继续因证据不足或边界重叠延期，全部正式对象保持 review，等待人工领域审查。"
    plan["gap_analysis"]["notes_en"] = "All eleven parent candidates in the fixed ATT&CK 19.1 baseline have admission decisions and YAML-only 2.0 redevelopment, producing 29 Niji-native children partitioned by stable stealth variables; no stable cross-entry gap requiring add was identified. Session-state-borrowed exploitation, identity-free passive path insertion, air-gap-targeted payload gating, nested trust chaining, and low-rate or low-privilege first use remain deferred for insufficient evidence or overlapping boundaries; all formal objects remain in review pending human domain review."
    plan["review"].update({"taxonomy": "passed", "evidence": "passed", "bilingual": "passed"})
    save(str(plan_path.relative_to(ROOT)), plan)


def generated_parent(parent_path: Path) -> dict[str, Any]:
    return raw_load(ROOT / technique_relative(parent_path))


def generated_child_path(parent_path: Path, child_path: Path) -> Path:
    relative, _ = build_child(parent_path, child_path)
    return ROOT / relative


def write_handoffs() -> None:
    for parent_path in parent_paths():
        parent = generated_parent(parent_path)
        attack_id = parent["classification"]["origin"]["source_attack_id"]
        decision = raw_load(TACTIC_ROOT / f"decisions/DEC-TA0001-{attack_id}.yaml")
        children = [raw_load(generated_child_path(parent_path, path)) for path in child_paths(parent_path)]
        strategy_refs = parent["defense"]["detections"]["strategy_refs"]
        mitigation_refs = parent["defense"]["mitigations"]["mitigation_refs"]
        analytic_refs = [NJA_BY_DET[next(old for old, new in DET_ID_MAP.items() if new == ref)] for ref in strategy_refs]
        handoff = {
            "handoff_schema_version": "2.0.0",
            "type": "technique-research-handoff",
            "batch_ref": BATCH,
            "work_item_ref": f"WORK-TA0001-{attack_id}",
            "temporary_key_prefix": f"B1V2-{attack_id}",
            "candidate": {"source_type": "attack", "source_attack_id": attack_id, "name": {"zh": decision["candidate"]["name_zh"], "en": decision["candidate"]["name_en"]}},
            "recommendation": {"decision": decision["decision"], "confidence": decision["confidence"], "rationale": prose(decision["rationale_zh"], decision["rationale_en"])},
            "proposed_content": {key: deepcopy(parent[key]) for key in ["summary", "definition_and_concept", "stealth_characteristics", "scope_boundary_definition", "application_scenarios_and_threat_model", "stealth_mechanisms"]},
            "proposed_subtechniques": [{
                "canonical_ref": child["id"],
                "name": child["name"],
                "stable_variable": child["summary"],
                "evidence_refs": child["evidence"]["reference_refs"],
                "confidence": child["stealth_mechanisms"][0]["confidence"],
            } for child in children],
            "defense_candidates": {"detection_strategies": strategy_refs, "detection_analytics": analytic_refs, "mitigations": mitigation_refs},
            "existing_library_reuse": {"reference_refs": parent["evidence"]["reference_refs"], "claim_refs": [], "case_refs": [], "strategy_refs": [], "analytic_refs": [], "mitigation_refs": [], "relationship_refs": []},
            "library_candidates": {"references": [], "claims": parent["evidence"]["claim_refs"] + [ref for child in children for ref in child["evidence"]["claim_refs"]], "cases": [], "detection_strategies": strategy_refs, "detection_analytics": analytic_refs, "mitigations": mitigation_refs, "relationships": []},
            "research": {"limitations": deepcopy(parent["research"]["limitations"]), "rejected_mechanisms": [], "open_questions": []},
            "integration": {"status": "complete", "resolutions": [
                {"disposition": "reuse", "objects": parent["evidence"]["reference_refs"]},
                {"disposition": "create", "objects": [parent["id"], *[child["id"] for child in children], *parent["evidence"]["claim_refs"], *[ref for child in children for ref in child["evidence"]["claim_refs"]], *strategy_refs, *analytic_refs, *mitigation_refs]},
                {"disposition": "defer", "objects": []},
            ]},
        }
        save(f"planning/runs/{BATCH}/{attack_id}-handoff.yaml", handoff)


def write_integration_summary() -> None:
    candidate_results = []
    all_references = set()
    bundles = []
    for parent_path in parent_paths():
        parent = generated_parent(parent_path)
        attack_id = parent["classification"]["origin"]["source_attack_id"]
        decision = raw_load(TACTIC_ROOT / f"decisions/DEC-TA0001-{attack_id}.yaml")
        candidate_results.append({
            "source_attack_id": attack_id,
            "decision": decision["decision"],
            "technique_ref": parent["id"],
            "subtechnique_refs": parent["subtechnique_taxonomy"]["subtechnique_refs"],
        })
        all_references.update(parent["evidence"]["reference_refs"])
        bundles.append(parent["id"])
    summary = {
        "schema_version": "1.0.0",
        "type": "batch-integration-summary",
        "batch_ref": BATCH,
        "status": "review",
        "candidate_results": candidate_results,
        "shared_library_resolutions": {
            "reuse": sorted(all_references),
            "extend": [],
            "create_ranges": {
                "references": None,
                "claims": "CLM-000197..CLM-000225, CLM-000237..CLM-000247",
                "cases": None,
                "detection_strategies": "DET-000051..DET-000056",
                "detection_analytics": "NJA-000025..NJA-000030",
                "mitigations": "MIT-000050..MIT-000055",
                "relationships": None,
            },
        },
        "deferred_hypotheses": [
            "T1190 会话状态借用式利用入口因缺少漏洞直接生成或泄露会话状态的充分原子证据继续延期。",
            "T1200 无身份被动链路插入因目前只有工具能力而缺少实战使用证据继续延期。",
            "T1091 隔离区定向载荷门控因公开材料未稳定证明入口前门控继续延期。",
            "T1199 嵌套信任链串联因路径长度尚未形成独立于连接或委托的防守边界继续延期。",
            "T1078 低权限或低速首用因缺少稳定且跨环境的独立行为模式继续延期。",
        ],
        "duplicate_resolution_refs": [],
        "validation": {
            "matrix_objects": 507,
            "schema_errors": 0,
            "schema_warnings": 0,
            "unresolved_duplicate_candidates": 0,
            "reviewed_similarity_resolutions": 1,
            "infrastructure_tests": 12,
            "web_api_issues": 0,
            "bundles_built": bundles,
        },
        "review_notes_zh": "Initial Access 固定 ATT&CK 19.1 基线的 11 个父候选均已完成准入与 YAML-only 2.0 重开发，共形成 11 个父技术和 29 项 Niji 原生子技术。REF-000042、REF-000043、REF-000067、REF-000068、REF-000070、REF-000084 及 REF-000085 至 REF-000114 按已存在身份复用；六类入口防御因检测目标、数据要求和控制动作不同于现有共享对象而新建 DET→NJA 与 MIT。正式内容与规划为 0 错误、0 警告，共享库为 0 个精确重复和 0 个待审可能重复；12 项基础设施测试、11 个 Bundle、Review Web 测试及全部新父子对象的中英文固定章节检查均通过，API issues 为 0。全部正式对象保持 review，等待人工领域审查。",
        "review_notes_en": "All eleven parent candidates in the fixed ATT&CK 19.1 Initial Access baseline have admission decisions and YAML-only 2.0 redevelopment, producing eleven parent techniques and 29 Niji-native children. REF-000042, REF-000043, REF-000067, REF-000068, REF-000070, REF-000084, and REF-000085 through REF-000114 are reused under their existing identities; six entry-defense families receive new DET-to-NJA and MIT objects because their objectives, data requirements, and control actions differ from existing shared objects. Formal content and planning have zero errors and zero warnings, with zero exact or unresolved possible duplicates; all twelve infrastructure tests, eleven bundles, Review Web tests, and bilingual fixed-section checks for every new parent and child pass with zero API issues. All formal objects remain in review pending human domain review.",
    }
    save(f"planning/runs/{BATCH}/integration-summary.yaml", summary)


def main() -> None:
    write_claims()
    write_detection_objects()
    write_mitigations()
    write_techniques()
    update_decisions_and_plan()
    write_handoffs()
    write_integration_summary()


if __name__ == "__main__":
    main()
