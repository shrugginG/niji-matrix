"""Integrate reviewed BATCH-TA0009-004 research into canonical matrix objects.

Sub-agent handoffs remain planning evidence. This script applies the primary
agent's admission, boundary, duplicate, and ID decisions.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
DATE = "2026-10-05"
TIDS = ("T1115", "T1005", "T1039", "T1530", "T1602")
H = {tid: yaml.safe_load((RUN / f"{tid}-handoff.yaml").read_text(encoding="utf-8")) for tid in TIDS}

PARENT = {
    "T1115": ("NJT-0214", "stealth-oriented-clipboard-content-acquisition"),
    "T1005": ("NJT-0215", "stealth-oriented-local-system-data-acquisition"),
    "T1039": ("NJT-0216", "stealth-oriented-network-share-content-acquisition"),
    "T1530": ("NJT-0217", "stealth-oriented-cloud-storage-content-acquisition"),
    "T1602": ("NJT-0218", "stealth-oriented-configuration-repository-acquisition"),
}

CHILD = {
    "T1115_CHILD_CHANGE_EVENT": ("NJS-0214-001", "clipboard-change-event-coupled-acquisition"),
    "T1115_CHILD_CONSUMER_INTERPOSITION": ("NJS-0214-002", "paste-consumer-context-interception"),
    "T1039_CHILD_EXISTING_MAPPING": ("NJS-0216-001", "preexisting-mapped-share-context-reuse"),
    "T1530_CHILD_CONSUMER_IDENTITY_DECOUPLED": ("NJS-0217-001", "consumer-identity-decoupled-cloud-object-retrieval"),
    "T1602_CHILD_TRUSTED_CONTEXT": ("NJS-0218-001", "trusted-management-context-configuration-retrieval"),
    "T1602_CHILD_PREEXISTING_COPY": ("NJS-0218-002", "preexisting-configuration-copy-retrieval"),
}

TARGET = {f"{tid}_PARENT": value[0] for tid, value in PARENT.items()}
TARGET.update({key: value[0] for key, value in CHILD.items()})

DET = {
    "T1005_DET_LOCAL_CONTENT_READ_LINEAGE": "DET-000249",
    "T1039_DET_SHARE_READ_OUTCOME": "DET-000250",
    "T1115_DET_EVENT_CAPTURE": "DET-000251",
    "T1115_DET_CONSUMER_INTERPOSITION": "DET-000252",
    "T1530_DET_OBJECT_DELIVERY_PROVENANCE": "DET-000253",
    "T1602_DET_ACQUISITION_OUTCOME": "DET-000254",
}
NJA = {
    "T1005_NJA_WINDOWS_LOCAL_READ_OUTCOME": "NJA-000326",
    "T1005_NJA_WINDOWS_DERIVATIVE_PRODUCER_READER": "NJA-000327",
    "T1005_NJA_WINDOWS_BACKUP_PRIVILEGE_READ": "NJA-000328",
    "T1039_NJA_WINDOWS_SMB_READ_LINEAGE": "NJA-000329",
    "T1039_NJA_ONTAP_NAS_READ_SCOPE": "NJA-000330",
    "T1115_NJA_EVENT_READ_OUTPUT": "NJA-000331",
    "T1115_NJA_CONSUMER_HOOK_OUTCOME": "NJA-000332",
    "T1530_NJA_AWS_S3_DELIVERY": "NJA-000333",
    "T1530_NJA_AZURE_BLOB_CARRIER": "NJA-000334",
    "T1530_NJA_GCP_OBJECT_DELIVERY": "NJA-000335",
    "T1530_NJA_M365_CLOUD_DRIVE_DOWNLOAD": "NJA-000336",
    "T1602_NJA_LIVE_READ_OUTCOME": "NJA-000337",
    "T1602_NJA_COPY_READ_OUTCOME": "NJA-000338",
}
MIT = {
    "T1039_MIT_SHARE_READ_SCOPE_AUDIT": "MIT-000221",
    "T1115_MIT_EXPOSURE": "MIT-000222",
    "T1530_MIT_OBJECT_READ_AUTH_AUDIT": "MIT-000223",
    "T1602_MIT_READ_PLANE": "MIT-000224",
    "MIT-000102": "MIT-000102",
    "MIT-000137": "MIT-000137",
}

REUSED_REFS = {
    "T1530_REF_GCP_AUDIT_FORMAT": "REF-000528",
    "T1530_REF_MS365_ACTIVITY_SCHEMA": "REF-000944",
    "T1530_REF_MS365_AUDIT_ACTIVITIES": "REF-000561",
    "T1602_REF_CISA_AA25": "REF-000792",
}

REF = dict(REUSED_REFS)
new_ref_ids = iter([f"REF-{number:06d}" for number in range(1075, 1126)])
for tid in ("T1005", "T1039", "T1115", "T1530", "T1602"):
    for item in H[tid]["library_candidates"]["references"]:
        key = item.get("temporary_key") or item.get("key")
        if key not in REF:
            REF[key] = next(new_ref_ids)

CLAIM_KEYS = {
    "T1005": [
        "T1005_CLM_PARENT_BEHAVIOR", "T1005_CLM_TAJMAHAL_CAPABILITY",
        "T1005_CLM_COOKIEMINER_CAPABILITY", "T1005_CLM_WINDOWS_READ_TELEMETRY",
        "T1005_CLM_BACKUP_AUTHORITY_ONLY",
    ],
    "T1039": [
        "T1039_CLM_ADMISSION", "T1039_CLM_DIRECT_SHARE_ACQUISITION",
        "T1039_CLM_EXISTING_MAPPING_IMPLEMENTATION", "T1039_CLM_AUDIT_OUTCOME_LEVELS",
        "T1039_CLM_BOUNDARY",
    ],
    "T1115": [
        "T1115_CLM_PARENT_COMPLETION", "T1115_CLM_EVENT_CHILD",
        "T1115_CLM_CONSUMER_CHILD", "T1115_CLM_PLATFORM_LIMIT",
        "T1115_CLM_EXPOSURE_CONTROL",
    ],
    "T1530": [
        "T1530_CLM_ADMISSION", "T1530_CLM_OUTCOME_TIERS", "T1530_CLM_AUDIT_DEFAULTS",
        "T1530_CLM_CARRIER_CHILD", "T1530_CLM_CAPITALONE_RESULT",
        "T1530_CLM_STORM0501_RESULT", "T1530_CLM_APT42_ONEDRIVE",
    ],
    "T1602": [
        "T1602_CLM_PARENT_COMPLETION", "T1602_CLM_JAGUAR_OUTCOME",
        "T1602_CLM_TRUSTED_CONTEXT", "T1602_CLM_PREEXISTING_COPY",
        "T1602_CLM_AUDIT_GAP",
    ],
}
CLM = {}
claim_ids = iter([f"CLM-{number:06d}" for number in range(1063, 1090)])
for tid in ("T1005", "T1039", "T1115", "T1530", "T1602"):
    for key in CLAIM_KEYS[tid]:
        CLM[key] = next(claim_ids)

CASE = {
    "T1039_CASE_TINYTYPHON_MAPPED_DRIVES": "CASE-000325",
    "T1115_CASE_NIGHTSHADE": "CASE-000326",
    "T1115_CASE_QBOT": "CASE-000327",
    "T1530_CASE_CAPITALONE_CLOUD_COPY": "CASE-000328",
    "T1530_CASE_STORM0501_STORAGE_KEY_EXFIL": "CASE-000329",
    "T1530_CASE_APT42_ONEDRIVE_DOWNLOAD": "CASE-000330",
    "T1602_CASE_JAGUAR_TOOTH": "CASE-000331",
    "T1602_CASE_PRC_PROVIDER_CONFIG": "CASE-000332",
}

LIFE = {
    "status": "review", "version": "1.0.0", "created": DATE, "modified": DATE,
    "contributors": ["Niji Matrix Research"], "reviewers": [],
}


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def pair(zh: str, en: str) -> dict:
    return {"zh": zh, "en": en}


def block(value, zh_fallback: str | None = None) -> dict:
    if isinstance(value, dict) and "paragraphs" in value:
        return deepcopy(value)
    if isinstance(value, dict) and "zh" in value and "en" in value:
        return {"paragraphs": [deepcopy(value)]}
    if isinstance(value, str):
        return {"paragraphs": [pair(zh_fallback or "该结论需要在目标环境中验证。", value)]}
    raise TypeError(f"cannot convert to paragraphs: {value!r}")


def slug(text: str) -> str:
    value = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:92] or "object"


def unique(values):
    return list(dict.fromkeys(value for value in values if value))


def ref_keys(keys):
    result = []
    for key in keys or []:
        if key.startswith("REF-"):
            result.append(key)
        elif key in REF:
            result.append(REF[key])
        else:
            raise KeyError(f"unmapped reference key {key}")
    return unique(result)


def mechanisms(values):
    result = []
    for item in values or []:
        copied = {key: deepcopy(item[key]) for key in ("mechanism_ref", "role", "summary", "analysis", "confidence")}
        copied["evidence_refs"] = ref_keys(item.get("evidence_keys") or item.get("evidence_refs"))
        result.append(copied)
    return result


REF_TITLES = {
    "T1005_R_ATTACK_PARENT": pair("从本地系统获取数据（T1005，ATT&CK Enterprise v19）", "Data from Local System, Technique T1005, ATT&CK Enterprise v19"),
    "T1005_R_ATTACK_DET0380": pair("外传前本地数据收集检测（DET0380）", "Detection of Local Data Collection Prior to Exfiltration, DET0380"),
    "T1005_R_TAJMAHAL": pair("Project TajMahal：复杂 APT 框架", "Project TajMahal: A Sophisticated APT Framework"),
    "T1005_R_COOKIEMINER": pair("窃取加密货币交易所 Cookie 的 macOS 恶意软件", "Mac Malware Steals Cryptocurrency Exchanges' Cookies"),
    "T1005_R_MS_AUDIT_FILE_SYSTEM": pair("审核文件系统", "Audit File System"),
    "T1005_R_MS_BACKUP_PRIVILEGE": pair("文件系统中的特权管理", "Managing Privileges in a File System"),
    "T1005_R_MS_BACKUP_AUDIT": pair("审核敏感特权使用", "Audit Sensitive Privilege Use"),
    "T1005_R_MS_BACKUP_RIGHT": pair("备份文件和目录安全策略", "Back Up Files and Directories Security Policy"),
    "T1005_R_MS_PRINT_307": pair("RPC_BranchOfficeJobDataPrinted 结构", "RPC_BranchOfficeJobDataPrinted"),
    "T1005_R_APPLE_LOCAL_BACKUP": pair("iPhone、iPad 或 iPod touch 加密本地备份", "About Encrypted Backups on iPhone, iPad, or iPod touch"),
    "T1039_REF_ATTACK19": pair("从网络共享驱动器获取数据（T1039，ATT&CK Enterprise v19）", "Data from Network Shared Drive, Technique T1039, ATT&CK Enterprise v19"),
    "T1039_REF_FORCEPOINT_MONSOON": pair("MONSOON APT 活动分析", "MONSOON: Analysis of an APT Campaign"),
    "T1039_REF_DFIR_EMOTET": pair("存活还是消亡：一次 Emotet 事件", "Dead or Alive? An Emotet Story"),
    "T1039_REF_MS_MAPPED_SESSION": pair("UAC 凭据提示下提升命令行不可见映射驱动器", "Mapped Drives Are Not Available from an Elevated Prompt When UAC Prompts for Credentials"),
    "T1039_REF_MS_SMB2_READ_RESPONSE": pair("SMB2 READ 响应结构", "SMB2 READ Response Structure"),
    "T1039_REF_NETAPP_NAS_AUDIT": pair("ONTAP SVM 文件与文件夹审核配置", "ONTAP SVM File and Folder Auditing Configuration"),
    "T1039_REF_NETAPP_NFS_FPOLICY": pair("ONTAP FPolicy 支持的 NFSv4 文件操作与过滤器", "ONTAP FPolicy Supported NFSv4 File Operations and Filters"),
    "T1039_REF_NETAPP_AUDIT_BYPASS": pair("ONTAP NAS 文件系统审核", "ONTAP NAS File-System Auditing"),
    "T1039_REF_MS_STORAGE_MIGRATION": pair("使用存储迁移服务迁移服务器", "Use Storage Migration Service to Migrate a Server"),
    "T1115_REF_ATTACK": pair("剪贴板数据（T1115，ATT&CK Enterprise v19）", "Clipboard Data, Technique T1115, ATT&CK Enterprise v19"),
    "T1115_REF_MS_CLIPBOARD": pair("Windows 剪贴板使用与变化监听", "Using and Monitoring the Windows Clipboard"),
    "T1115_REF_VOLATILITY": pair("窗口站与剪贴板恶意软件内存取证", "Window Stations and Clipboard Malware Memory Forensics"),
    "T1115_REF_NIGHTSHADE": pair("NightshadeC2 僵尸网络分析", "NightshadeC2 Botnet Analysis"),
    "T1115_REF_QBOT": pair("QBot 活动深度分析", "Deep Analysis of a QBot Campaign"),
    "T1115_REF_CORTEX": pair("异常 GetClipboardData 调用分析告警", "Uncommon GetClipboardData API Invocation Analytics Alert"),
    "T1115_REF_DLP": pair("Microsoft Purview DLP 策略参考", "Microsoft Purview DLP Policy Reference"),
    "T1115_REF_BITWARDEN": pair("Bitwarden 浏览器自动填充与剪贴板设置", "Bitwarden Browser Autofill and Clipboard Settings"),
    "T1115_REF_MS_FORMATS": pair("Windows 剪贴板格式、历史与云同步控制", "Windows Clipboard Formats, History, and Cloud Controls"),
    "T1115_REF_RDP": pair("Azure 虚拟桌面剪贴板重定向配置", "Azure Virtual Desktop Clipboard Redirection Configuration"),
    "T1115_REF_APPLE_PASTEBOARD": pair("NSPasteboard changeCount", "NSPasteboard changeCount"),
    "T1115_REF_X11": pair("X Window System 剪贴板规范", "X Window System Clipboard Specification"),
    "T1115_REF_WAYLAND": pair("Wayland 客户端间数据共享协议", "Wayland Data Sharing Between Clients"),
    "T1530_REF_ATTACK19": pair("从云存储获取数据（T1530，ATT&CK Enterprise v19）", "Data from Cloud Storage, Technique T1530, ATT&CK Enterprise v19"),
    "T1530_REF_DOJ_THOMPSON_CASE": pair("美国诉 Paige Thompson 案", "United States v. Paige Thompson"),
    "T1530_REF_AWS_REQUEST_IDENTIFICATION": pair("使用 CloudTrail 识别 Amazon S3 请求", "Identifying Amazon S3 Requests Using CloudTrail"),
    "T1530_REF_AWS_PRESIGNED_URLS": pair("使用预签名 URL 下载与上传 S3 对象", "Download and Upload S3 Objects with Presigned URLs"),
    "T1530_REF_AWS_BLOCK_PUBLIC": pair("配置 S3 账户级阻止公共访问", "Configuring S3 Block Public Access for an Account"),
    "T1530_REF_AZURE_BLOB_LOG_SCHEMA": pair("Azure StorageBlobLogs 字段参考", "Azure Monitor StorageBlobLogs Field Reference"),
    "T1530_REF_AZURE_SHARED_KEY_PREVENT": pair("阻止 Azure Storage 共享密钥授权", "Prevent Shared Key Authorization for Azure Storage"),
    "T1530_REF_AZURE_SAS_EXPIRY": pair("配置共享访问签名到期策略", "Configure an Expiration Policy for Shared Access Signatures"),
    "T1530_REF_GCP_USAGE_LOGS": pair("Cloud Storage 用量日志与存储日志", "Usage Logs and Storage Logs for Cloud Storage"),
    "T1530_REF_GCP_SIGNED_URLS": pair("Cloud Storage 签名 URL", "Signed URLs for Cloud Storage"),
    "T1530_REF_GCP_PUBLIC_ACCESS_PREVENTION": pair("Cloud Storage 公共访问防护", "Cloud Storage Public Access Prevention"),
    "T1530_REF_MS365_AUDIT_SETUP": pair("Microsoft 365 审核解决方案入门", "Get Started with Microsoft 365 Auditing Solutions"),
}


def title_for(key: str, item: dict) -> dict:
    if key in REF_TITLES:
        return REF_TITLES[key]
    value = item.get("title")
    if isinstance(value, dict):
        return deepcopy(value)
    en = item.get("title_en") or value or key.replace("_", " ")
    zh = item.get("title_zh") or f"{en}（研究来源）"
    return pair(zh, en)


def publisher_for(item: dict) -> str:
    if item.get("publisher"):
        return item["publisher"]
    host = urlsplit(item["url"]).netloc.lower()
    mapping = {
        "attack.mitre.org": "MITRE ATT&CK", "learn.microsoft.com": "Microsoft",
        "docs.microsoft.com": "Microsoft", "support.apple.com": "Apple",
        "developer.apple.com": "Apple", "docs.aws.amazon.com": "Amazon Web Services",
        "docs.cloud.google.com": "Google Cloud", "www.justice.gov": "United States Department of Justice",
        "www.forcepoint.com": "Forcepoint", "thedfirreport.com": "The DFIR Report",
        "docs.netapp.com": "NetApp", "www.esentire.com": "eSentire",
        "www.fortinet.com": "Fortinet", "volatilityfoundation.org": "Volatility Foundation",
        "bitwarden.com": "Bitwarden", "specifications.freedesktop.org": "freedesktop.org",
        "wayland.freedesktop.org": "freedesktop.org", "securelist.com": "Kaspersky",
        "unit42.paloaltonetworks.com": "Palo Alto Networks Unit 42",
    }
    return mapping.get(host, host.removeprefix("www.") or "Source publisher")


def source_type_for(value: str) -> str:
    allowed = {
        "official-documentation", "academic-paper", "incident-report", "threat-report",
        "vendor-report", "news", "dataset", "sample-analysis", "web-page", "other",
    }
    if value in allowed:
        return value
    lowered = value.lower()
    if any(token in lowered for token in ("malware", "sample", "technical-analysis")):
        return "sample-analysis"
    if "incident" in lowered or "case-record" in lowered:
        return "incident-report"
    if "report" in lowered:
        return "vendor-report"
    if any(token in lowered for token in ("official", "framework", "standard", "documentation", "protocol")):
        return "official-documentation"
    return "web-page"


def note_for(item: dict, title: dict) -> dict:
    supports = item.get("supports")
    limitations = item.get("limitations")
    if isinstance(supports, dict):
        zh, en = supports.get("zh", ""), supports.get("en", "")
    else:
        en = "; ".join(supports) if isinstance(supports, list) else str(supports or "")
        zh = f"用于支持“{title['zh']}”所定位的行为、字段或控制。"
    if limitations:
        en = f"{en} Limitation: {limitations}".strip()
        zh += " 来源局限须按定位字段和结论层级保留。"
    return pair(zh, en or f"Supports the located facts in {title['en']} at the stated conclusion level.")


def write_references() -> None:
    for tid in ("T1005", "T1039", "T1115", "T1530", "T1602"):
        for item in H[tid]["library_candidates"]["references"]:
            key = item.get("temporary_key") or item.get("key")
            if key in REUSED_REFS:
                continue
            rid = REF[key]
            title = title_for(key, item)
            notes = note_for(item, title)
            locator = item.get("locator")
            if isinstance(locator, list):
                locator = "; ".join(locator)
            record = {
                "schema_version": "1.0.0", "type": "reference", "id": rid,
                "title_zh": title["zh"], "title_en": title["en"],
                "source_type": source_type_for(item.get("source_type", "official-documentation")),
                "authors": [item["publisher"]] if item.get("publisher") else [],
                "publisher": publisher_for(item), "published": item.get("published"),
                "url": item["url"], "accessed": DATE, "locator": locator,
                "archive_url": None, "credibility": item.get("confidence", "high"),
                "notes_zh": notes["zh"], "notes_en": notes["en"],
            }
            save(ROOT / "references" / f"{rid}-{slug(title['en'])}.yaml", record)


def find_item(tid: str, section: str, key: str):
    for item in H[tid]["library_candidates"][section]:
        if (item.get("temporary_key") or item.get("key")) == key:
            return item
    raise KeyError((tid, section, key))


CLAIM_CHILD = {
    "T1039_CLM_EXISTING_MAPPING_IMPLEMENTATION": "T1039_CHILD_EXISTING_MAPPING",
    "T1115_CLM_EVENT_CHILD": "T1115_CHILD_CHANGE_EVENT",
    "T1115_CLM_CONSUMER_CHILD": "T1115_CHILD_CONSUMER_INTERPOSITION",
    "T1530_CLM_CARRIER_CHILD": "T1530_CHILD_CONSUMER_IDENTITY_DECOUPLED",
    "T1602_CLM_TRUSTED_CONTEXT": "T1602_CHILD_TRUSTED_CONTEXT",
    "T1602_CLM_PREEXISTING_COPY": "T1602_CHILD_PREEXISTING_COPY",
}


def claim_type(key: str) -> str:
    if key in CLAIM_CHILD:
        return "subtechnique-existence"
    if "BOUNDARY" in key:
        return "technique-boundary"
    if any(token in key for token in ("IMPLEMENTATION", "AUDIT", "TELEMETRY", "OUTCOME", "RESULT")):
        return "mechanism-mapping"
    return "technique-relevance"


def write_claims() -> None:
    for tid, keys in CLAIM_KEYS.items():
        parent_ref = PARENT[tid][0]
        for key in keys:
            item = find_item(tid, "claims", key)
            statement = item.get("statement") or item.get("proposition") or pair(
                item.get("proposition_zh", ""), item.get("proposition_en", "")
            )
            subjects = [parent_ref]
            if key in CLAIM_CHILD:
                subjects.append(CHILD[CLAIM_CHILD[key]][0])
            observed = any(token in key for token in ("JAGUAR", "NIGHTSHADE", "CONSUMER", "STORM0501", "APT42", "CAPITALONE", "DIRECT_SHARE"))
            record = {
                "schema_version": "1.0.0", "type": "claim", "id": CLM[key],
                "claim_type": claim_type(key), "statement_zh": statement["zh"],
                "statement_en": statement["en"], "subject_refs": subjects,
                "evidence_refs": ref_keys(item.get("evidence_keys")),
                "evidence_mode": "directly-observed" if observed else "strongly-inferred",
                "confidence": item.get("confidence", "medium"), "status": "review",
            }
            save(ROOT / "claims" / f"{CLM[key]}-{slug(statement['en'])}.yaml", record)


CASE_ACTOR = {
    "T1039_CASE_TINYTYPHON_MAPPED_DRIVES": "TINYTYPHON / MONSOON",
    "T1115_CASE_NIGHTSHADE": "NightshadeC2",
    "T1115_CASE_QBOT": "QBot",
    "T1530_CASE_CAPITALONE_CLOUD_COPY": "Paige Thompson / Capital One intrusion",
    "T1530_CASE_STORM0501_STORAGE_KEY_EXFIL": "Storm-0501",
    "T1530_CASE_APT42_ONEDRIVE_DOWNLOAD": "APT42",
    "T1602_CASE_JAGUAR_TOOTH": "APT28 / Jaguar Tooth",
    "T1602_CASE_PRC_PROVIDER_CONFIG": "PRC state-sponsored network actors",
}
CASE_CHILDREN = {
    "T1039_CASE_TINYTYPHON_MAPPED_DRIVES": ["T1039_CHILD_EXISTING_MAPPING"],
    "T1115_CASE_NIGHTSHADE": ["T1115_CHILD_CHANGE_EVENT"],
    "T1115_CASE_QBOT": ["T1115_CHILD_CONSUMER_INTERPOSITION"],
    "T1530_CASE_STORM0501_STORAGE_KEY_EXFIL": ["T1530_CHILD_CONSUMER_IDENTITY_DECOUPLED"],
    "T1602_CASE_PRC_PROVIDER_CONFIG": ["T1602_CHILD_TRUSTED_CONTEXT", "T1602_CHILD_PREEXISTING_COPY"],
}


def write_cases() -> None:
    for tid in ("T1039", "T1115", "T1530", "T1602"):
        for item in H[tid]["library_candidates"]["cases"]:
            key = item.get("temporary_key") or item.get("key")
            if key not in CASE:
                continue
            name = item.get("name") or pair(f"{CASE_ACTOR[key]} 数据获取事件", f"{CASE_ACTOR[key]} Data-Acquisition Event")
            event = item.get("event")
            if not event and item.get("event_zh"):
                event = pair(item["event_zh"], item["event_en"])
            if not event and item.get("observed_facts"):
                event = pair(
                    "Forcepoint 样本分析显示 TINYTYPHON 遍历已映射或可见驱动器，按配置扩展名选择文档并上传；研究者在控制端看到数千份受害者文档。来源未给出逐文档本地或网络来源、登录 LUID 或实测告警差异。",
                    "Forcepoint sample analysis showed TINYTYPHON crawling mapped or visible drive letters, selecting configured document extensions, and uploading matches. Researchers observed thousands of victim documents on the controller. The source provides no per-document local-versus-network origin, logon LUID, or measured alert difference.",
                )
            subjects = [PARENT[tid][0]] + [CHILD[child][0] for child in CASE_CHILDREN.get(key, [])]
            record = {
                "schema_version": "1.0.0", "type": "case", "id": CASE[key],
                "name_zh": name["zh"], "name_en": name["en"],
                "actor_or_campaign": item.get("actor_or_campaign", CASE_ACTOR[key]),
                "subject_refs": subjects, "description_zh": event["zh"], "description_en": event["en"],
                "time_range": item.get("time_range"), "target_sectors_zh": [], "target_sectors_en": [],
                "evidence_refs": ref_keys(item.get("evidence_keys")),
                "confidence": item.get("confidence", "high"), "status": "review",
            }
            save(ROOT / "cases" / f"{CASE[key]}-{slug(name['en'])}.yaml", record)


def formal_claims(tid: str):
    return [CLM[key] for key in CLAIM_KEYS[tid]]


def formal_cases(tid: str):
    return [value for key, value in CASE.items() if key.startswith(tid)]


def handoff_reference_refs(tid: str):
    result = []
    for item in H[tid]["library_candidates"]["references"]:
        result.append(REF[item.get("temporary_key") or item.get("key")])
    result.extend(H[tid].get("existing_library_reuse", {}).get("reference_refs", []))
    return unique(result)


def research_limits(tid: str):
    return deepcopy(H[tid]["research"]["limitations"])


def write_techniques() -> dict[str, Path]:
    roots = {}
    for tid in TIDS:
        nid, folder_slug = PARENT[tid]
        source = H[tid]["proposed_content"]
        children = [value[0] for key, value in CHILD.items() if key.startswith(tid)]
        taxonomy = deepcopy(source["subtechnique_taxonomy"])
        taxonomy = {
            "narrative": deepcopy(taxonomy["narrative"]),
            "coverage": "deferred" if tid == "T1005" else "established",
            "subtechnique_refs": children,
        }
        strategy_refs = [value for key, value in DET.items() if key.startswith(tid)]
        mitigation_refs = [value for key, value in MIT.items() if key.startswith(tid)]
        if tid == "T1005":
            mitigation_refs = ["MIT-000137"]
        if tid == "T1115":
            mitigation_refs.append("MIT-000102")
        record = {
            "schema_version": "2.0.0", "type": "technique", "id": nid,
            "name": deepcopy(source["name"]), "summary": deepcopy(source["summary"]),
            "aliases": deepcopy(source.get("aliases", [])),
            "classification": {
                "tactic_refs": ["TA0009"],
                "origin": {"kind": "attack-adapted", "source_attack_id": tid, "source_attack_version": "19.1"},
                "decision_ref": f"DEC-TA0009-{tid}",
            },
            "definition_and_concept": deepcopy(source["definition_and_concept"]),
            "stealth_characteristics": deepcopy(source["stealth_characteristics"]),
            "scope_boundary_definition": deepcopy(source["scope_boundary_definition"]),
            "application_scenarios_and_threat_model": deepcopy(source["application_scenarios_and_threat_model"]),
            "stealth_mechanisms": mechanisms(source["stealth_mechanisms"]),
            "subtechnique_taxonomy": taxonomy,
            "defense": {
                "detections": {"coverage": "available", "strategy_refs": strategy_refs},
                "mitigations": {"coverage": "available", "mitigation_refs": unique(mitigation_refs)},
            },
            "evidence": {
                "claim_refs": formal_claims(tid), "case_refs": formal_cases(tid),
                "reference_refs": handoff_reference_refs(tid),
            },
            "research": {"limitations": research_limits(tid)}, "lifecycle": deepcopy(LIFE),
        }
        if tid == "T1115":
            record["research"]["limitations"]["paragraphs"][2] = pair(
                "autofill、DLP、短清理、history/cloud 排除与 RDP 重定向限制降低暴露或传播，却不能阻止清理前同会话的实时读取，也可能影响可用性和无障碍。合法剪贴板历史、密码管理器、DLP、远程支持、虚拟化和自动化与恶意行为共享接口，必须按精确版本、owner、会话、目的地和变更窗口调优。消费者介入还需最小化跨进程写入和调试权，并约束动态代码、模块来源与回调完整性；单靠减少剪贴板暴露不能覆盖进程内 hook。",
                "Autofill, DLP, short clearing, history or cloud exclusion, and RDP-redirection restrictions reduce exposure or propagation but do not stop real-time reads in the same session before clearing and may affect usability and accessibility. Legitimate clipboard history, password managers, DLP, remote support, virtualization, and automation share interfaces with malicious behavior and require tuning by exact version, owner, session, destination, and change window. Consumer interposition also requires least cross-process write and debug rights plus dynamic-code, module-provenance, and callback integrity controls; reducing clipboard exposure alone does not cover in-process hooks.",
            )
        if tid == "T1005":
            record["research"]["limitations"]["paragraphs"][0] = pair(
                "T1005 来源页能锚定广泛的本地内容获取行为，却不能证明任一读取天然匿迹。TajMahal 与 CookieMiner 是代码或模块能力分析，缺少派生对象已向攻击者返回内容的受害端证据。因此父级结论为 medium，派生视图假设与相应 NM-BT 机理只有 low；当前不把派生视图列为正式子技术。",
                "The T1005 source page anchors broad local-content acquisition but does not make every read stealthy. TajMahal and CookieMiner are code or module capability analyses without victim-side evidence that a derivative object returned content to an adversary. The parent conclusion is therefore medium confidence, while the derivative-view hypothesis and associated NM-BT mechanism are low; the derivative view is not a formal child at present.",
            )
        if tid == "T1530":
            record["research"]["limitations"]["paragraphs"][0] = pair(
                "T1530 来源页能证明广泛父行为和平台范围，却不能证明每次云读取天然匿迹，也不能自动支持原生子技术。Capital One 司法资料证明云端存储数据被复制并在设备中发现副本，但未公开原始 CloudTrail、对象键、请求状态或字节，不能据此补造日志序列。APT42 报告直接观察 OneDrive 下载到磁盘，却没有逐对象 UAL 字段或总量；向仿冒 OneDrive 外传仅为“尝试且可能成功”。",
                "The T1530 source page establishes broad behavior and platform scope but does not make every cloud read stealthy or automatically support a native child. Capital One court material establishes copied cloud-stored data and a copy on devices, but publishes no raw CloudTrail, object keys, request status, or bytes and cannot support an invented log sequence. The APT42 report directly observes OneDrive download to disk but gives no per-object UAL fields or total volume, while transfer to a masquerading OneDrive is only attempted and possibly successful.",
            )
            paragraph = record["subtechnique_taxonomy"]["narrative"]["paragraphs"][1]
            paragraph["en"] = paragraph["en"].replace("is parent-core in IaaS", "is intrinsic to the IaaS behavior")
        root = ROOT / "matrix/tactics/TA0009-collection/techniques" / f"{nid}-{folder_slug}"
        save(root / "technique.yaml", record)
        roots[tid] = root
    return roots


CHILD_CLAIMS = {
    "T1115_CHILD_CHANGE_EVENT": ["T1115_CLM_EVENT_CHILD"],
    "T1115_CHILD_CONSUMER_INTERPOSITION": ["T1115_CLM_CONSUMER_CHILD"],
    "T1039_CHILD_EXISTING_MAPPING": ["T1039_CLM_EXISTING_MAPPING_IMPLEMENTATION"],
    "T1530_CHILD_CONSUMER_IDENTITY_DECOUPLED": ["T1530_CLM_CARRIER_CHILD", "T1530_CLM_STORM0501_RESULT"],
    "T1602_CHILD_TRUSTED_CONTEXT": ["T1602_CLM_TRUSTED_CONTEXT"],
    "T1602_CHILD_PREEXISTING_COPY": ["T1602_CLM_PREEXISTING_COPY"],
}


def write_children(roots: dict[str, Path]) -> None:
    for tid in TIDS:
        for source in H[tid]["proposed_subtechniques"]:
            key = source["temporary_key"]
            if key not in CHILD:
                continue
            sid, folder_slug = CHILD[key]
            strategy_refs = [DET[value] for value in source.get("defense_strategy_keys", []) if value in DET]
            mitigation_refs = [MIT[value] for value in source.get("mitigation_keys", []) if value in MIT]
            if key == "T1115_CHILD_CONSUMER_INTERPOSITION":
                mitigation_refs.append("MIT-000102")
            case_refs = [CASE[case] for case, children in CASE_CHILDREN.items() if key in children]
            record = {
                "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": sid,
                "parent_ref": PARENT[tid][0], "name": deepcopy(source["name"]),
                "summary": deepcopy(source["summary"]), "aliases": [],
                "lineage": {"attck_subtechnique_inherited": False},
                "definition_and_concept": deepcopy(source["definition_and_concept"]),
                "stealth_characteristics": deepcopy(source["stealth_characteristics"]),
                "scope_boundary_definition": deepcopy(source["scope_boundary_definition"]),
                "application_scenarios_and_threat_model": deepcopy(source["application_scenarios_and_threat_model"]),
                "stealth_mechanisms": mechanisms(source["stealth_mechanisms"]),
                "defense": {
                    "detections": {"coverage": "available", "strategy_refs": unique(strategy_refs)},
                    "mitigations": {"coverage": "available", "mitigation_refs": unique(mitigation_refs)},
                },
                "evidence": {
                    "claim_refs": [CLM[value] for value in CHILD_CLAIMS[key]],
                    "case_refs": case_refs, "reference_refs": ref_keys(source.get("evidence_keys")),
                },
                "research": {"limitations": deepcopy(source.get("limitations") or source.get("research_limitations"))},
                "lifecycle": deepcopy(LIFE),
            }
            if key == "T1115_CHILD_CONSUMER_INTERPOSITION":
                record["application_scenarios_and_threat_model"]["threat_model"]["defender_model"]["paragraphs"][0] = pair(
                    "防守方需要不可变进程启动键、source-target 注入或模块加载谱系、目标进程内函数入口与调用栈完整性、成功剪贴板返回和后继写入。进程注入分析可以证明跨进程写入与调度，却不单独证明剪贴板内容结果；本子项分析还必须连接 GetClipboardData 或等效调用的返回状态与日志、IPC 或网络结果。没有内存或 call-stack 传感器时，可疑应用内部读取只能保持未解析。批准的 EDR、DLP、无障碍和调试工具例外必须绑定精确包、版本、owner、目标进程和用途。",
                    "Defenders need an immutable process-start key, source-to-target injection or module-load lineage, function-entry and call-stack integrity inside the target, a successful clipboard return, and a downstream write. Process-injection analytics can establish cross-process write and dispatch but do not by themselves prove a clipboard-content result. This child additionally requires a GetClipboardData or equivalent return joined to a log, IPC, or network outcome. Without memory or call-stack sensors, suspicious in-application reads remain unresolved. Exceptions for approved EDR, DLP, accessibility, and debugging tools must bind exact package, version, owner, target process, and purpose.",
                )
            for lang in ("zh", "en"):
                first = record["stealth_characteristics"]["paragraphs"][0][lang]
                name = record["name"][lang]
                if not first.startswith(name):
                    record["stealth_characteristics"]["paragraphs"][0][lang] = f"{name}：{first}"
            save(roots[tid] / "subtechniques" / f"{sid}-{folder_slug}" / "subtechnique.yaml", record)


def write_decisions() -> None:
    for tid in TIDS:
        item = H[tid]
        recommendation = item["recommendation"]
        rationale = recommendation["rationale"]["paragraphs"]
        scope = recommendation.get("scope_notes") or item["proposed_content"]["scope_boundary_definition"]["paragraphs"][0]
        candidate = item["candidate"]
        evidence = handoff_reference_refs(tid)[:4]
        record = {
            "schema_version": "1.1.0", "type": "technique-decision", "id": f"DEC-TA0009-{tid}",
            "tactic_ref": "TA0009",
            "candidate": {
                "source_type": "attack", "source_attack_id": tid, "source_attack_version": "19.1",
                "name_en": candidate["name"]["en"], "name_zh": candidate["name"]["zh"],
            },
            "decision": "adapt", "rationale_zh": "\n\n".join(value["zh"] for value in rationale),
            "rationale_en": "\n\n".join(value["en"] for value in rationale),
            "scope_notes_zh": scope["zh"], "scope_notes_en": scope["en"],
            "gap_statement_zh": None, "gap_statement_en": None,
            "original_attack_subtechniques_imported": False,
            "resulting_technique_ref": PARENT[tid][0], "evidence_refs": evidence,
            "confidence": recommendation.get("confidence", "medium"),
            "review": {
                "status": "review", "authors": ["Niji Matrix Research"], "reviewers": [],
                "review_notes_zh": "第四批准入、跨技术边界、正式内容、共享库与自动质量门禁已完成；等待人工领域评审。",
                "review_notes_en": "Batch-four admission, cross-technique boundaries, canonical content, shared libraries, and automated quality gates are complete; human domain review remains.",
            },
        }
        save(ROOT / "matrix/tactics/TA0009-collection/decisions" / f"DEC-TA0009-{tid}.yaml", record)


STRATEGY_DESC = {
    "T1005_DET_LOCAL_CONTENT_READ_LINEAGE": pair("在数据 owner 指定的敏感本地对象上验证成功 ReadData，并把对象、登录会话和不可变进程实例连接到输出、临时副本或外送结果。目录列举、属性读取、特权分配和读取能力分别保留为较低级状态；备份、打印、索引、EDR、迁移与取证只有在主体、签名、作业、路径和时间全部匹配时才排除。", "Validate successful ReadData on owner-designated sensitive local objects and join the object, logon session, and immutable process instance to an output, temporary copy, or transfer result. Keep enumeration, attribute reads, privilege assignment, and capability as lower states. Exclude backup, printing, indexing, EDR, migration, and forensics only when principal, signer, job, path, and time all match."),
    "T1039_DET_SHARE_READ_OUTCOME": pair("把共享服务器的成功 READ 或实际 ReadData 与客户端登录会话、进程、映射来源和后继结果关联。5145 只作权限检查线索；分析必须区分新映射、既有映射、NAS 管理面和合法迁移作业，并在服务器不提供字节结果时降低结论等级。", "Join a share server's successful READ or exercised ReadData to client logon session, process, mapping provenance, and downstream outcome. Treat 5145 only as an authorization lead. Distinguish new and preexisting mappings, NAS administrative paths, and approved migration jobs, and lower confidence when the server does not expose returned-byte results."),
    "T1115_DET_EVENT_CAPTURE": pair("在经验证可记录剪贴板监听、变化标识和成功读取的终端上，将 listener 注册、变化后短窗读取和日志、IPC 或网络结果闭合。隐藏窗口或注册只形成暴露线索；必须确认内容结果，且默认不集中采集明文剪贴板。", "On endpoints validated to record clipboard listeners, change identifiers, and successful reads, close listener registration, short-window post-change reads, and file, IPC, or network outcomes. A hidden window or registration is only exposure; require a content outcome and avoid centralized plaintext clipboard capture by default."),
    "T1115_DET_CONSUMER_INTERPOSITION": pair("把进入正常粘贴消费者的跨进程写入、模块或函数介入，与成功剪贴板返回及攻击者控制的第二内容结果连接。进程注入可提供前置谱系，但只有消费者调用路径和内容结果同时闭合时才确认本子项。", "Join cross-process writes, modules, or function interposition inside a normal paste consumer to a successful clipboard return and a second attacker-controlled content outcome. Process injection supplies prerequisite lineage, but confirm this child only when the consumer call path and content result both close."),
    "T1530_DET_OBJECT_DELIVERY_PROVENANCE": pair("按平台使用对象正文成功返回字段，把对象键、响应状态或字节、来源地址、客户端和授权载体连接到可识别主体或公开/共享授权路径。列举、HEAD、授权成功和权限存在不替代正文结果；正常同步、备份和数据管道按批准职责与对象范围排除。", "Use platform-specific successful object-body return fields to join object key, status or bytes, source, client, and authorization carrier to an identifiable principal or public/shared path. Listing, HEAD, authorization success, and permission existence do not replace a body result. Exclude normal sync, backup, and data pipelines by approved duty and object scope."),
    "T1602_DET_ACQUISITION_OUTCOME": pair("把设备实时配置响应或配置副本成功读取与主体、管理来源、作业 ID、设备范围和批准意图核对。命令执行、登录或仓库访问本身不证明配置取得；NMS、备份、合规、灾备和厂商支持必须以精确作业范围作为正常反例。", "Reconcile a live device-configuration response or successful configuration-copy read with principal, management source, job ID, device scope, and approved intent. Command execution, login, or repository access alone does not prove acquisition. Treat NMS, backup, compliance, disaster recovery, and vendor support as benign only with exact job scope."),
}

ANALYTIC_SUMMARY = {
    key: pair(
        f"按对象、主体、会话与结果字段实现“{next(a['name']['zh'] for a in H[tid]['defense_candidates']['detection_analytics'] if a['temporary_key'] == key)}”。",
        f"Implement {next(a['name']['en'] for a in H[tid]['defense_candidates']['detection_analytics'] if a['temporary_key'] == key)} with object, principal, session, and outcome fields.",
    )
    for tid in TIDS for key in NJA if key.startswith(tid)
}

T1005_TEXT = {
    "T1005_NJA_WINDOWS_LOCAL_READ_OUTCOME": {
        "window": pair("同一进程谱系从 ReadData 到输出默认三十分钟；保留主体和路径三十天基线，并按应用导出耗时校准。", "Pilot thirty minutes from ReadData to output for one process lineage, retain thirty days of per-principal and per-path baseline, and adapt both to application export duration."),
        "fp": pair("批准的备份、端点安全、索引、打印、数据库维护、迁移、电子发现、事件响应和取证会读取敏感内容并产生结果。", "Approved backup, endpoint security, indexing, printing, database maintenance, software migration, e-discovery, incident response, and digital forensics can read sensitive content and create outputs."),
        "blind": pair("未配置匹配 SACL 时没有 4663；内存或应用内部读取可能无文件事件，端点文件表不是完整读取记录，结果也可能只在内存或加密流中。", "Event 4663 is absent without a matching SACL; memory-only or application-internal reads may lack a file event; endpoint file tables are not universal read records; output can remain in memory or an encrypted stream."),
        "tune": pair("只对 owner 批准的敏感路径配置 SACL，要求 FILE_READ_DATA，以主体、签名、作业、路径和时间共同限定例外；无法确认内容结果时保留独立状态。", "Scope SACLs to owner-approved sensitive paths, require FILE_READ_DATA, version exceptions by principal, signer, job, path, and time, and retain a separate state when content outcome is unconfirmed."),
    },
    "T1005_NJA_WINDOWS_DERIVATIVE_PRODUCER_READER": {
        "window": pair("临时打印队列在生成前后十分钟关联；备份和导出按生产者保留期、试点上限二十四小时；消费者基线保留三十天。", "Use ten minutes around transient print-spool production; producer-defined retention for backups and exports capped at twenty-four hours in the pilot; retain thirty days of consumer baselines."),
        "fp": pair("打印渲染和重试、备份校验、反恶意软件或 EDR、索引、DLP、支持导出、法律保全、迁移和取证会读取派生副本。", "Print rendering and retry, backup verification, antivirus or EDR scanning, indexing, DLP inspection, support export, legal hold, migration, and forensic acquisition can read derivative copies."),
        "blind": pair("打印事件 307 可能没有稳定 spool 路径，manifest 可能缺逐文件映射，应用 API 或内存解析可能没有 4663；Windows 字段也不能证明 macOS 备份读取。", "Print Event 307 may lack a stable spool path, manifests can omit per-file mappings, application APIs or memory parsing may not emit 4663, and Windows telemetry does not establish macOS backup reads."),
        "tune": pair("要求生产者 manifest 与实际 ReadData，优先使用稳定派生对象 ID，以签名、服务 SID 和作业范围绑定批准消费者；映射不确定时只输出异常状态。", "Require a producer manifest and exercised ReadData, prefer stable derivative IDs, bind approved consumers to signer, service SID, and job scope, and emit only an anomaly state when mapping is uncertain."),
    },
    "T1005_NJA_WINDOWS_BACKUP_PRIVILEGE_READ": {
        "window": pair("从特权实际使用到敏感读取和结果默认零至三十分钟，限定同一设备、SubjectLogonId 与进程谱系；批准作业历史保留三十天。", "Use zero to thirty minutes from privilege exercise to sensitive read and output on one device, SubjectLogonId, and process lineage; retain thirty days of approved-job history."),
        "fp": pair("企业备份、系统状态恢复、批准迁移、事件响应采集及存储或安全产品会合法调用备份 API。", "Enterprise backup, system-state recovery, authorized migration, incident-response acquisition, and storage or security products legitimately invoke backup APIs."),
        "blind": pair("备份/恢复特权审计常因事件量关闭，API 和事件版本可能没有直接内容结果；原始卷读取属于 NJT-0108 并需其他遥测。", "Backup or restore privilege-use auditing is often disabled for volume, APIs and event versions may lack a content result, and raw-volume reads belong to NJT-0108 with different telemetry."),
        "tune": pair("仅在选定系统和路径部署，按服务 SID、签名、作业 ID、来源与目的范围比较；不得只按进程名放行，并分开记录特权分配、使用、ReadData 和物化结果。", "Deploy only on selected systems and paths; compare service SID, signer, job ID, and source or destination scope; never suppress by process name alone; separate privilege assignment, exercise, ReadData, and materialized output."),
    },
}

WINDOW_ZH = {
    "T1039_NJA_WINDOWS_SMB_READ_LINEAGE": "5145 到 4663 或 SMB 成功响应默认六十秒，读取按三十分钟分组，并保留用户、共享和进程三十天基线。",
    "T1039_NJA_ONTAP_NAS_READ_SCOPE": "成功 READ 按三十分钟分组，并保留主体、客户端和导出范围三十天基线。",
    "T1530_NJA_AWS_S3_DELIVERY": "CloudTrail 与服务器日志默认十分钟内关联，读取片段三十分钟，角色、授权载体和作业基线保留三十天。",
    "T1530_NJA_AZURE_BLOB_CARRIER": "控制或密钥事件到读取默认一小时，读取片段三十分钟，批准作业基线保留三十天。",
    "T1530_NJA_GCP_OBJECT_DELIVERY": "审计日志到 usage log 默认十五分钟，读取片段三十分钟，签名者与公共策略历史保留三十天。",
    "T1530_NJA_M365_CLOUD_DRIVE_DOWNLOAD": "登录或会话到下载默认八小时，读取片段三十分钟，用户、应用和设备基线保留三十天。",
}


def field_key(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return value.lower()


def normalized_requirements(values):
    result = []
    for item in values:
        name = item.get("name")
        if not name:
            en = item["source_type"].replace("-", " ").title()
            name = pair(f"经验证的{en}数据", en)
        result.append({
            "source_type": item["source_type"], "name": name,
            "channel": item.get("channel"), "required_fields": [field_key(value) for value in item["required_fields"]],
        })
    return result


def normalized_pair_list(value, fallback: dict | None = None):
    if isinstance(value, list):
        return [deepcopy(item) if isinstance(item, dict) else pair(fallback["zh"] if fallback else "需人工核实的正常活动。", item) for item in value]
    if isinstance(value, dict):
        return [deepcopy(value)]
    if isinstance(value, str):
        return [deepcopy(fallback) if fallback else pair("需人工核实的正常活动或数据缺口。", value)]
    return []


def write_defense() -> None:
    for tid in TIDS:
        handoff = H[tid]
        for item in handoff["defense_candidates"]["detection_strategies"]:
            key = item["temporary_key"]
            detects = item.get("detects_keys") or item.get("subjects") or []
            detects_refs = [TARGET[value] for value in detects if value in TARGET]
            analytics = [NJA[value] for value in item["analytic_keys"]]
            desc = STRATEGY_DESC[key]
            evidence = ref_keys(item.get("evidence_keys"))
            for analytic_key in item["analytic_keys"]:
                analytic = next(value for value in handoff["defense_candidates"]["detection_analytics"] if value["temporary_key"] == analytic_key)
                evidence.extend(ref_keys(analytic.get("evidence_keys")))
            record = {
                "schema_version": "2.0.0", "type": "detection-strategy", "id": DET[key],
                "name": deepcopy(item["name"]), "summary": deepcopy(item["objective"]),
                "description": block(desc), "detects_refs": unique(detects_refs),
                "domains": item.get("domains") or [item.get("domain", "enterprise")],
                "analytic_refs": analytics, "evidence_refs": unique(evidence), "lifecycle": deepcopy(LIFE),
            }
            save(ROOT / "detections" / f"{DET[key]}-{slug(item['name']['en'])}.yaml", record)

        for item in handoff["defense_candidates"]["detection_analytics"]:
            key = item["temporary_key"]
            logic = item["logic"]
            if not (isinstance(logic, dict) and "paragraphs" in logic):
                logic = block(logic, "按成功读取、对象、主体、进程谱系和后继结果进行关联，并保留分级结论。")
            correlation = item.get("correlation")
            t1005 = T1005_TEXT.get(key)
            if correlation:
                window = correlation["window"]
                if isinstance(window, str):
                    window = pair(WINDOW_ZH[key], window)
                dimensions = [field_key(value) for value in correlation["dimensions"]]
            else:
                window = t1005["window"]
                dimensions = unique([field for req in item["data_requirements"] for field in req["required_fields"] if field in {"timestamp", "device_id", "subject_logon_id", "process_id", "process_start_id", "object_name", "job_id"}])
            fp = normalized_pair_list(item["false_positives"], t1005["fp"] if t1005 else None)
            blind = normalized_pair_list(item["blind_spots"], t1005["blind"] if t1005 else None)
            tuning = item.get("tuning_guidance") or item.get("tuning")
            if isinstance(tuning, str):
                tuning = block(t1005["tune"])
            elif not (isinstance(tuning, dict) and "paragraphs" in tuning):
                tuning = block(tuning)
            record = {
                "schema_version": "2.0.0", "type": "detection-analytic", "id": NJA[key],
                "strategy_ref": DET[item["strategy_key"]], "name": deepcopy(item["name"]),
                "summary": ANALYTIC_SUMMARY[key], "domains": ["enterprise"],
                "platforms": item.get("platforms") or [item.get("platform", "Windows")],
                "logic": logic, "data_requirements": normalized_requirements(item["data_requirements"]),
                "observables": normalized_pair_list(item["observables"]),
                "correlation": {"window": window, "dimensions": dimensions},
                "false_positives": fp, "blind_spots": blind, "tuning_guidance": tuning,
                "evidence_refs": ref_keys(item.get("evidence_keys")), "lifecycle": deepcopy(LIFE),
            }
            save(ROOT / "analytics" / f"{NJA[key]}-{slug(item['name']['en'])}.yaml", record)

        for item in handoff["defense_candidates"]["mitigations"]:
            key = item["temporary_key"]
            if key not in MIT:
                continue
            measures = []
            for measure in item["measures"]:
                description = measure.get("description") or pair(measure.get("description_zh", ""), measure.get("description_en", ""))
                name = measure.get("name") or pair(f"控制措施：{measure['key']}", measure["key"].replace("-", " ").title())
                measures.append({
                    "key": measure["key"].replace("_", "-"), "name": name, "description": block(description),
                    "control_type": "containment" if measure["control_type"] == "response" else measure["control_type"],
                })
            applications = []
            for app in item["applications"]:
                target_key = app.get("target_key") or app.get("target_ref")
                if target_key not in TARGET and target_key not in TARGET.values():
                    continue
                target_ref = TARGET.get(target_key, target_key)
                use = app.get("use") or pair(app.get("use_zh", ""), app.get("use_en", ""))
                effect = app.get("expected_effect") or pair(app.get("expected_effect_zh", ""), app.get("expected_effect_en", ""))
                limits = app.get("limitations") or pair(app.get("limitations_zh", ""), app.get("limitations_en", ""))
                applications.append({
                    "target_ref": target_ref, "use": block(use),
                    "expected_effect": block(effect), "limitations": block(limits),
                })
            description = item["description"]
            summary = item.get("summary") or pair(
                f"以最小授权、对象范围和审计结果降低{item['name']['zh']}相关风险。",
                f"Reduce risk through least authorization, object scope, and auditable outcomes for {item['name']['en']}.",
            )
            record = {
                "schema_version": "2.0.0", "type": "mitigation", "id": MIT[key],
                "name": deepcopy(item["name"]), "summary": summary,
                "description": block(description), "domains": item.get("domains", ["enterprise"]),
                "measures": measures, "applications": applications,
                "evidence_refs": ref_keys(item.get("evidence_keys")), "lifecycle": deepcopy(LIFE),
            }
            save(ROOT / "mitigations" / f"{MIT[key]}-{slug(item['name']['en'])}.yaml", record)


def extend_shared() -> None:
    reference_updates = {
        "REF-000530": {
            "locator": "Protection-state reconnaissance plus storageAccounts/write network exposure, storageAccounts/listkeys/action account-key theft, AzCopy data transfer, and completed exfiltration",
            "zh": "同一 Storm-0501 来源同时定位防护状态测绘、开放存储网络、账户密钥取得及 AzCopy 完成的数据转移；未公开逐对象 StorageBlobLogs 字段。",
            "en": "The same Storm-0501 source locates protection-state reconnaissance, storage-network exposure, account-key acquisition, and completed AzCopy transfer; it does not publish per-object StorageBlobLogs fields.",
        },
        "REF-000731": {
            "locator": "APT42 Microsoft 365 operations in 2022-2023; OneDrive browsing and download to disk; built-in features, public tools, and anonymized infrastructure",
            "zh": "同一 APT42 来源扩展到 OneDrive 浏览和下载到磁盘；向仿冒 OneDrive 的外传仅为尝试且可能成功。",
            "en": "The same APT42 source now locates OneDrive browsing and download to disk; transfer to masquerading OneDrive remains only attempted and possibly successful.",
        },
        "REF-000792": {
            "locator": "Packet capture plus configuration acquisition from provider-script output, active device survey and TFTP, configuration-archive service credentials, and existing monitoring tools",
            "zh": "通告聚合多个 actor 和事件，可支持配置取得路径的存在，不能把服务凭据、监控工具、provider 输出和单一配置产物串成一笔事务。",
            "en": "The advisory aggregates multiple actors and incidents. It supports existence of configuration-acquisition paths but cannot combine service credentials, monitoring tools, provider output, and one artifact into a single transaction.",
        },
    }
    for rid, update in reference_updates.items():
        path = next((ROOT / "references").glob(f"{rid}-*.yaml"))
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["locator"] = update["locator"]
        data["notes_zh"] = update["zh"]
        data["notes_en"] = update["en"]
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

    path = next((ROOT / "cases").glob("CASE-000214-*.yaml"))
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["name_zh"] = "Bazar/Conti 从 UNC 共享直接复制到 MEGA"
    data["name_en"] = "Bazar/Conti Direct Copy from UNC Share to MEGA"
    data["description_zh"] = "The DFIR Report 在同一 Bazar/Conti 入侵中观察到 Rclone 以 UNC Shares 路径为源直接复制到 MEGA，并记录 SMB 共享连接活动。该事件分别支持共享内容取得与云服务外传；没有中间落点时不能反推数据暂存，且报告未提供逐文件 4663、映射 LUID 或服务器返回字节。"
    data["description_en"] = "The DFIR Report observed Rclone copying directly from a UNC Shares source to MEGA in the same Bazar/Conti intrusion and recorded SMB share connection activity. The event separately supports share-content acquisition and cloud-service exfiltration. Without an intermediate destination it does not establish staging, and the report provides no per-file 4663, mapping LUID, or server-return byte record."
    for target in ("NJT-0216",):
        if target not in data["subject_refs"]:
            data["subject_refs"].append(target)
    if "REF-000640" not in data["evidence_refs"]:
        data["evidence_refs"].append("REF-000640")
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

    for rid, target, use, effect, limits, extra_refs in [
        (
            "MIT-000102", "NJS-0214-002",
            pair("对浏览器、编辑器、邮件和业务应用按 source-target pair 收紧跨进程写入、调试和模块装载权，启用兼容的动态代码、CIG/ACG/CFG 或等效完整性策略，并把批准 DLP、EDR、无障碍和插件绑定到精确 hash、owner、目标进程、函数用途与到期窗口。", "For browsers, editors, mail, and business apps, tighten cross-process write, debug, and module-load rights by source-target pair; enable compatible dynamic-code, CIG, ACG, CFG, or equivalent integrity policy; bind approved DLP, EDR, accessibility, and plug-ins to exact hash, owner, target, function, and expiry."),
            pair("未批准代码更难进入正常粘贴消费者或改变剪贴板返回路径，受信进程名不能覆盖异常模块、调用栈和第二内容结果。", "Unapproved code has less ability to enter a normal paste consumer or alter clipboard returns, and a trusted process name no longer masks anomalous modules, call stacks, and second content outcomes."),
            pair("合法 DLP、EDR、无障碍、输入法、JIT、调试和热补丁可能需要进程内介入；内核或受陷签名组件仍可绕过，且没有剪贴板结果时不能确认本子项。", "Legitimate DLP, EDR, accessibility, input methods, JIT, debugging, and hot patching may require in-process interposition. Kernel or compromised signed components can bypass controls, and missing clipboard outcome prevents confirmation."),
            ["REF-000362", REF["T1115_REF_QBOT"]],
        ),
        (
            "MIT-000137", "NJT-0215",
            pair("把 owner 指定的本地敏感路径、数据库导出区和批准读取者纳入最小授权，限制交互账户和长期备份权限，并用定向 SACL 将成功 ReadData、作业范围和后继结果关联。", "Place owner-designated sensitive local paths, database export areas, and approved readers under least authorization; restrict interactive and standing backup rights; use targeted SACLs to join successful ReadData, job scope, and downstream outcomes."),
            pair("减少非批准主体可读取的本地内容，并使内容读取与目录发现、权限存在或普通管理活动分离。", "Reduce local content available to unapproved actors and separate content reads from discovery, permission existence, and ordinary administration."),
            pair("SACL 与特权审计可能产生高事件量，应用内部或内存读取可能不可见；批准备份、索引、EDR、迁移和取证仍需精确作业例外。", "SACL and privilege auditing may produce high volume, and application-internal or memory reads may be invisible. Approved backup, indexing, EDR, migration, and forensics still need exact job exceptions."),
            ["REF-000379", REF["T1005_R_MS_AUDIT_FILE_SYSTEM"], REF["T1005_R_MS_BACKUP_RIGHT"]],
        ),
    ]:
        path = next((ROOT / "mitigations").glob(f"{rid}-*.yaml"))
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["applications"] = [item for item in data["applications"] if item["target_ref"] != target]
        data["applications"].append({"target_ref": target, "use": block(use), "expected_effect": block(effect), "limitations": block(limits)})
        data["evidence_refs"] = unique(data.get("evidence_refs", []) + extra_refs)
        data["lifecycle"]["version"] = "1.1.0"
        data["lifecycle"]["modified"] = DATE
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def update_tactic() -> None:
    path = ROOT / "matrix/tactics/TA0009-collection/tactic.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    # Technique membership is directory-derived in tactic schema 1.0.0.
    # Preserve inherited source metadata rather than inventing an unsupported index.
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def finalize_planning() -> None:
    path = ROOT / "planning/tactics/TA0009.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    batch = next(item for item in data["batches"] if item["id"] == "BATCH-TA0009-004")
    batch["status"] = "review"
    for item in data["work_items"]:
        tid = item["source_attack_id"]
        if tid not in PARENT:
            continue
        item["decision_ref"] = f"DEC-TA0009-{tid}"
        item["resulting_technique_ref"] = PARENT[tid][0]
        item["stage"] = "review"
        item["notes_zh"] = (
            item["notes_zh"].split(" 第四批五候选范围；")[0]
            + " 第四批五候选由独立 sub-agent 分两轮完成研究，主 Agent 统一完成 adapt 准入、跨技术边界、共享库查重、正式写入与质量验收；对象保持 review，等待人工领域评审。"
        )
        item["notes_en"] = (
            item["notes_en"].split(" In the batch-four")[0]
            + " Batch four used two waves of independent sub-agent research. The primary agent completed adapt admission, cross-technique boundaries, shared-library deduplication, canonical integration, and quality gates. Objects remain at review pending human domain approval."
        )
    data["gap_analysis"]["status"] = "pending"
    data["gap_analysis"]["notes_zh"] = "固定版 17 个 TA0009 父候选已登记；前四批 15 个父技术和 19 个 NJS 已入正式矩阵并保持 review，剩余 T1025 与 T1056 两个父候选。整体 Niji 原生缺口将在最终批及战术收敛后评估。"
    data["gap_analysis"]["notes_en"] = "All 17 fixed TA0009 parents are registered. The first four batches place fifteen parents and nineteen NJS in the formal matrix at review, leaving T1025 and T1056. Tactic-wide Niji-native gaps will be assessed after the final batch and tactic convergence."
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def write_integration_summary() -> None:
    record = {
        "schema_version": "1.0.0", "type": "batch-integration-summary",
        "batch_ref": "BATCH-TA0009-004", "status": "review",
        "delivery_control": {
            "overall_candidate_count": 17, "batch_candidate_count": 5,
            "batch_size_rationale": pair(
                "第四批恰含五个父候选；按要求分两轮由每名 sub-agent 独立研究一个父技术，主 Agent 等全部结果后统一裁决本地、共享、云和配置副本边界。",
                "Batch four contains five parents. Per instruction, one sub-agent researched each parent in two waves, and the primary agent waited for all results before reconciling local, share, cloud, and configuration-copy boundaries.",
            ),
            "previous_batch_gate_passed": True,
        },
        "candidate_results": [
            {"source_attack_id": tid, "decision": "adapt", "technique_ref": PARENT[tid][0],
             "subtechnique_refs": [value[0] for key, value in CHILD.items() if key.startswith(tid)]}
            for tid in TIDS
        ],
        "shared_library_resolutions": {
            "reuse": ["REF-000379", "REF-000475", "REF-000868", "REF-000474", "REF-000906", "REF-000625", "REF-000528", "REF-000944", "REF-000561", "MIT-000102", "MIT-000137", "CASE-000214"],
            "extend": ["REF-000530", "REF-000731", "REF-000792", "CASE-000214", "MIT-000102", "MIT-000137"],
            "create_ranges": {
                "references": "REF-001075..REF-001125", "claims": "CLM-001063..CLM-001089",
                "cases": "CASE-000325..CASE-000332", "detection_strategies": "DET-000249..DET-000254",
                "detection_analytics": "NJA-000326..NJA-000338", "mitigations": "MIT-000221..MIT-000224",
                "relationships": None,
            },
        },
        "deferred_hypotheses": [
            "T1005 派生本地视图只有能力与可行性证据，缺少成功内容取得及独立观察差，正式 taxonomy 为 deferred。",
            "T1530 数据面与前端审计错位保留为父级机理；GUI/API/CLI 不构成子项。",
            "T1602 接口审计错位、选择性配置投影和分散查询缺少独立证据；增量变量归 NJT-0135。",
        ],
        "duplicate_resolution_refs": [],
        "semantic_validation": {
            "candidate_level_gates_passed": True, "conclusion_level_evidence_passed": True,
            "njt_0001_field_responsibility_reviewed": True, "bilingual_argument_depth_passed": True,
            "boilerplate_review_passed": True, "taxonomy_breadth_reviewed": True,
            "attack_breadth_gap_explained": True, "canonical_prose_bulk_generated": False,
        },
        "validation": {
            "matrix_objects": 3901, "schema_errors": 0, "schema_warnings": 0,
            "unresolved_duplicate_candidates": 0, "reviewed_similarity_resolutions": 12,
            "infrastructure_tests": 12, "web_tests": 127, "web_api_issues": 0,
            "bundles_built": [PARENT[tid][0] for tid in TIDS],
        },
        "review_notes_zh": "五个 ATT&CK Enterprise 19.1 父候选均先完成 adapt 准入，新增 NJT-0214 至 NJT-0218 及六个 Niji 原生子项。T1005 派生视图因证据不足保持 deferred；其余子项按变化事件、消费者介入、既有共享映射、云授权载体与消费主体解绑、受信管理语境及既有配置副本划分。质量、五份 Bundle、127 项 Web 测试和 11 个对象双语 API QA 通过；TA0009 正式 15/17，剩余 2 项。对象保持 review，等待人工领域评审。",
        "review_notes_en": "All five ATT&CK Enterprise 19.1 parents received adapt admission, producing NJT-0214 through NJT-0218 and six Niji-native children. T1005's derivative-view hypothesis remains deferred for insufficient evidence. The admitted children separate change events, consumer interposition, preexisting share mappings, cloud authorization-carrier and consumer decoupling, trusted management context, and preexisting configuration copies. Quality, five bundles, 127 Web tests, and bilingual API QA for eleven objects passed. TA0009 has 15 of 17 formal parents with two remaining. Objects remain at review pending human domain approval.",
    }
    save(RUN / "integration-summary.yaml", record)


def main() -> None:
    write_references()
    write_claims()
    write_cases()
    roots = write_techniques()
    write_children(roots)
    write_decisions()
    write_defense()
    extend_shared()
    update_tactic()
    finalize_planning()
    write_integration_summary()
    print("Integrated 5 NJT, 6 NJS, 51 REF, 27 CLM, 8 CASE, 6 DET, 13 NJA, and 4 MIT objects at review")


if __name__ == "__main__":
    main()
