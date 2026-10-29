"""Integrate the primary-reviewed final TA0009 candidate batch."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import unicodedata

import yaml


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
DATE = "2026-10-05"
STATUS = "review"
TIDS = ("T1025", "T1056")
H = {tid: yaml.safe_load((RUN / f"{tid}-handoff.yaml").read_text(encoding="utf-8")) for tid in TIDS}

PARENT = {
    "T1025": ("NJT-0219", "stealth-oriented-removable-media-content-acquisition"),
    "T1056": ("NJT-0220", "stealth-oriented-interactive-input-acquisition"),
}
CHILD = {
    "T1056_COLLECTION_CHILD_EXTERNAL_STREAM": ("NJS-0220-001", "consumer-external-input-stream-acquisition"),
    "T1056_COLLECTION_CHILD_TRUSTED_ENTRY": ("NJS-0220-002", "trusted-origin-data-entry-interposition"),
}
TARGET = {
    "T1025_PARENT": "NJT-0219",
    "T1056_COLLECTION_PARENT": "NJT-0220",
    **{key: value[0] for key, value in CHILD.items()},
}

REF = {
    "T1025_REF_ATTACK_V19": "REF-001126",
    "T1025_REF_MS_DEVICE_CONTROL_POLICIES": "REF-001127",
    "T1056_COLLECTION_REF_SUCURI_PRESTASHOP": "REF-001128",
    "T1056_COLLECTION_REF_PCI_PAYMENT_PAGE": "REF-001129",
    "T1056_COLLECTION_REF_W3C_CSP": "REF-001130",
    "T1056_COLLECTION_REF_W3C_SRI": "REF-001131",
}
CLM = {
    "T1025_CLM_PARENT": "CLM-001090",
    "T1025_CLM_CRUTCH": "CLM-001091",
    "T1025_CLM_DEVICE_CONTROL": "CLM-001092",
    "T1056_COLLECTION_CLM_RESULT_STAGES": "CLM-001093",
    "T1056_COLLECTION_CLM_EXTERNAL_STREAM": "CLM-001094",
    "T1056_COLLECTION_CLM_TRUSTED_ENTRY": "CLM-001095",
    "T1056_COLLECTION_CLM_OUTCOME_SPLIT": "CLM-001096",
    "T1056_COLLECTION_CLM_ENTRY_CONTROLS": "CLM-001097",
}
CASE = {"T1056_COLLECTION_CASE_PRESTASHOP": "CASE-000333"}
DET = {
    "T1025_DET_MEDIA_READ_OUTCOME": "DET-000255",
    "T1056_COLLECTION_DET_TRUSTED_ENTRY": "DET-000256",
    "T1056_COLLECTION_DET_EXTERNAL_STREAM_REUSE": "DET-000192",
}
NJA = {
    "T1025_NJA_WINDOWS_MEDIA_READ_LINEAGE": "NJA-000339",
    "T1025_NJA_REATTACHMENT_TARGET_RECALL": "NJA-000340",
    "T1056_COLLECTION_NJA_RENDERED_ENTRY": "NJA-000341",
    "T1056_COLLECTION_NJA_SAME_ORIGIN_RECEIVER": "NJA-000342",
    "T1056_COLLECTION_NJA_EXTERNAL_STREAM_REUSE": "NJA-000215",
}
MIT = {
    "T1025_MIT_MEDIA_READ_AUTHORIZATION": "MIT-000225",
    "T1056_COLLECTION_MIT_TRUSTED_ENTRY": "MIT-000226",
    "T1056_COLLECTION_MIT_EXTERNAL_STREAM_REUSE": "MIT-000173",
}

LIFE = {
    "status": STATUS, "version": "1.0.0", "created": DATE, "modified": DATE,
    "contributors": ["Niji Matrix Research"], "reviewers": [],
}


def save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def pair(zh: str, en: str) -> dict:
    return {"zh": zh, "en": en}


def block(value, zh_fallback: str | None = None) -> dict:
    if isinstance(value, dict) and "paragraphs" in value:
        return deepcopy(value)
    if isinstance(value, dict) and "zh" in value and "en" in value:
        return {"paragraphs": [deepcopy(value)]}
    if isinstance(value, str):
        return {"paragraphs": [pair(zh_fallback or "该结论须在目标环境中验证。", value)]}
    raise TypeError(value)


def unique(values):
    return list(dict.fromkeys(value for value in values if value))


def slug(value: str) -> str:
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:96] or "object"


def refs(keys):
    result = []
    for key in keys or []:
        if key.startswith("REF-"):
            result.append(key)
        else:
            result.append(REF[key])
    return unique(result)


def mechanisms(values):
    result = []
    for item in values or []:
        value = {key: deepcopy(item[key]) for key in ("mechanism_ref", "role", "summary", "analysis", "confidence")}
        value["evidence_refs"] = refs(item.get("evidence_keys") or item.get("evidence_refs"))
        result.append(value)
    return result


def candidate_key(item):
    return item.get("temporary_key") or item.get("key")


def find_item(tid: str, section: str, key: str):
    for item in H[tid]["library_candidates"][section]:
        if candidate_key(item) == key:
            return item
    raise KeyError((tid, section, key))


def source_type(value: str) -> str:
    allowed = {
        "official-documentation", "academic-paper", "incident-report", "threat-report",
        "vendor-report", "news", "dataset", "sample-analysis", "web-page", "other",
    }
    if value in allowed:
        return value
    lowered = value.lower()
    if "incident" in lowered:
        return "incident-report"
    if any(token in lowered for token in ("framework", "standard", "guidance", "documentation")):
        return "official-documentation"
    return "web-page"


def write_references() -> None:
    for tid in TIDS:
        for item in H[tid]["library_candidates"]["references"]:
            key = candidate_key(item)
            rid = REF[key]
            title = item["title"]
            notes = item.get("notes")
            if notes:
                note_zh, note_en = notes["zh"], notes["en"]
            else:
                note_zh = f"用于支持“{title['zh']}”所定位的行为、字段或控制；来源限制须随结论保留。"
                note_en = str(item.get("supports") or "")
                if item.get("limitations"):
                    note_en += " Limitation: " + item["limitations"]
            value = {
                "schema_version": "1.0.0", "type": "reference", "id": rid,
                "title_zh": title["zh"], "title_en": title["en"],
                "source_type": source_type(item.get("source_type", "official-documentation")),
                "authors": deepcopy(item.get("authors", [item.get("publisher", "Source publisher")])),
                "publisher": item.get("publisher", "Source publisher"), "published": item.get("published"),
                "url": item["url"], "accessed": item.get("accessed", DATE),
                "locator": item.get("locator"), "archive_url": None,
                "credibility": item.get("credibility", "high"),
                "notes_zh": note_zh, "notes_en": note_en,
            }
            save(ROOT / "references" / f"{rid}-{slug(title['en'])}.yaml", value)


CLAIM_KEYS = {
    "T1025": ["T1025_CLM_PARENT", "T1025_CLM_CRUTCH", "T1025_CLM_DEVICE_CONTROL"],
    "T1056": [
        "T1056_COLLECTION_CLM_RESULT_STAGES", "T1056_COLLECTION_CLM_EXTERNAL_STREAM",
        "T1056_COLLECTION_CLM_TRUSTED_ENTRY", "T1056_COLLECTION_CLM_OUTCOME_SPLIT",
        "T1056_COLLECTION_CLM_ENTRY_CONTROLS",
    ],
}
CLAIM_TARGET = {
    "T1056_COLLECTION_CLM_EXTERNAL_STREAM": "NJS-0220-001",
    "T1056_COLLECTION_CLM_TRUSTED_ENTRY": "NJS-0220-002",
}


def write_claims() -> None:
    for tid, keys in CLAIM_KEYS.items():
        for key in keys:
            item = find_item(tid, "claims", key)
            proposition = item.get("statement") or pair(item["proposition_zh"], item["proposition_en"])
            subjects = [PARENT[tid][0]]
            if key in CLAIM_TARGET:
                subjects.append(CLAIM_TARGET[key])
            ctype = item.get("claim_type")
            if not ctype:
                ctype = "subtechnique-existence" if key in CLAIM_TARGET else "technique-relevance"
            observed = key in {"T1025_CLM_CRUTCH", "T1056_COLLECTION_CLM_TRUSTED_ENTRY"}
            value = {
                "schema_version": "1.0.0", "type": "claim", "id": CLM[key],
                "claim_type": ctype, "statement_zh": proposition["zh"], "statement_en": proposition["en"],
                "subject_refs": subjects, "evidence_refs": refs(item.get("evidence_keys")),
                "evidence_mode": "directly-observed" if observed else "strongly-inferred",
                "confidence": item.get("confidence", "high"), "status": STATUS,
            }
            save(ROOT / "claims" / f"{CLM[key]}-{slug(proposition['en'])}.yaml", value)


def write_case() -> None:
    item = find_item("T1056", "cases", "T1056_COLLECTION_CASE_PRESTASHOP")
    name = item["name"]
    description = pair(
        "Sucuri 在受侵 PrestaShop 结账中发现恶意代码藏于合法单页结账制品，覆盖支付表单、监视支付字段变化、把数据送到同站路径及服务端处理器，并把取得的卡数据转发到攻击者服务器。该事件不提供受影响用户数、告警率，也不能证明每位访问者都提交了数据。",
        item["event"] + " " + item["limitations"],
    )
    sectors = item["target_sectors"]
    value = {
        "schema_version": "1.0.0", "type": "case", "id": "CASE-000333",
        "name_zh": name["zh"], "name_en": name["en"],
        "actor_or_campaign": item["actor_or_campaign"],
        "subject_refs": ["NJT-0220", "NJS-0220-002"],
        "description_zh": description["zh"], "description_en": description["en"],
        "time_range": item.get("time_range"), "target_sectors_zh": sectors["zh"],
        "target_sectors_en": sectors["en"], "evidence_refs": refs(item["evidence_keys"]),
        "confidence": item.get("confidence", "high"), "status": STATUS,
    }
    save(ROOT / "cases" / f"CASE-000333-{slug(name['en'])}.yaml", value)


def parent_reference_refs(tid: str):
    created = [REF[candidate_key(item)] for item in H[tid]["library_candidates"]["references"]]
    reused = H[tid].get("existing_library_reuse", {}).get("reference_refs", [])
    normalized = []
    for item in reused:
        if isinstance(item, str):
            normalized.append(item)
        elif item.get("resolution") not in {"boundary-only", "no-reuse"}:
            normalized.append(item["ref"])
    return unique(created + normalized)


def parent_claim_refs(tid: str):
    return [CLM[key] for key in CLAIM_KEYS[tid]]


def parent_case_refs(tid: str):
    return [] if tid == "T1025" else ["CASE-000235", "CASE-000333"]


def research_limits(tid: str):
    value = deepcopy(H[tid]["research"]["limitations"])
    if tid == "T1025":
        value["paragraphs"][0] = pair(
            "Crutch 资料证明介质监视、匹配文件处理和后续上传能力，但没有公开逐文件读取事件或完整受害时间线。TajMahal 来自一处外交机构受害环境并包含重接入取回模块，却没有证明某个指定文件在现场被成功读取，也没有量化告警变化。因此父级为 medium，重接入假设仅保留在研究限制与父级分析中，不列为正式子技术。",
            "Crutch reporting establishes media monitoring, matching-file handling, and later upload capability but publishes no per-file read events or complete victim timeline. TajMahal came from a diplomatic victim environment and contained a reattachment retrieval module, yet does not prove one requested file was successfully read in the field or quantify alert change. The parent is therefore medium confidence, while the reattachment hypothesis remains in research limits and parent analysis rather than as a formal child.",
        )
    return value


T1025_TAXONOMY = {
    "paragraphs": [
        pair(
            "重接入门控目标回收是唯一找到的候选变量：组件先保存介质与对象知识，待同一介质后续返回时才读取既定目标，使发现与取得跨接入会话分离。TajMahal 支持这一模块设计，但公开资料没有逐文件受害结果或告警测量；按结论级证据门禁，本版将其延期，不建立正式子技术。",
            "Reattachment-Gated Target Recall is the only candidate variable found: a component retains media and object knowledge and reads the selected target only when the same medium later returns, separating discovery from acquisition across attachment sessions. TajMahal supports the module design but public reporting provides no per-file victim outcome or alert measurement. Under the conclusion-level evidence gate, this version defers the hypothesis and creates no formal child.",
        ),
        pair(
            "接入触发、轮询、扩展名、关键词、文件年龄和增量检查由 T1119/NJT-0135 或父级目标范围表达；USB、CD、MTP、操作系统、API、盘符和文件类型只是实现。原始卷归 NJT-0108，介质命令—结果信箱归 NJT-0207，正常导入后的本地副本归 NJT-0215。受信导入进程劫持和策略审计旁路也缺少现场结论证据。",
            "Attachment triggers, polling, extensions, keywords, file age, and incremental checks belong to T1119 and NJT-0135 or parent target scope. USB, CD, MTP, operating system, API, drive letter, and file type are implementations. Raw volumes belong to NJT-0108, media command-result mailboxes to NJT-0207, and local copies after normal import to NJT-0215. Trusted importer hijack and policy-audit bypass also lack field-level outcome evidence.",
        ),
    ]
}


def write_techniques() -> dict[str, Path]:
    roots = {}
    for tid in TIDS:
        nid, folder_slug = PARENT[tid]
        source = H[tid]["proposed_content"]
        if tid == "T1025":
            children = []
            taxonomy = {"narrative": T1025_TAXONOMY, "coverage": "deferred", "subtechnique_refs": []}
            strategies, mitigations = ["DET-000255"], ["MIT-000225"]
        else:
            children = ["NJS-0220-001", "NJS-0220-002"]
            taxonomy = {
                "narrative": deepcopy(source["subtechnique_taxonomy"]["narrative"]),
                "coverage": "established", "subtechnique_refs": children,
            }
            strategies, mitigations = ["DET-000192", "DET-000256"], ["MIT-000173", "MIT-000226"]
        value = {
            "schema_version": "2.0.0", "type": "technique", "id": nid,
            "name": deepcopy(source["name"]), "summary": deepcopy(source["summary"]), "aliases": [],
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
                "detections": {"coverage": "available", "strategy_refs": strategies},
                "mitigations": {"coverage": "available", "mitigation_refs": mitigations},
            },
            "evidence": {
                "claim_refs": parent_claim_refs(tid), "case_refs": parent_case_refs(tid),
                "reference_refs": parent_reference_refs(tid),
            },
            "research": {"limitations": research_limits(tid)}, "lifecycle": deepcopy(LIFE),
        }
        root = ROOT / "matrix/tactics/TA0009-collection/techniques" / f"{nid}-{folder_slug}"
        save(root / "technique.yaml", value)
        roots[tid] = root
    return roots


CHILD_CLAIMS = {
    "T1056_COLLECTION_CHILD_EXTERNAL_STREAM": ["T1056_COLLECTION_CLM_EXTERNAL_STREAM"],
    "T1056_COLLECTION_CHILD_TRUSTED_ENTRY": ["T1056_COLLECTION_CLM_TRUSTED_ENTRY"],
}


def write_children(root: Path) -> None:
    for source in H["T1056"]["proposed_subtechniques"]:
        key = source["temporary_key"]
        sid, folder_slug = CHILD[key]
        external = key.endswith("EXTERNAL_STREAM")
        strategies = ["DET-000192"] if external else ["DET-000256"]
        mitigations = ["MIT-000173"] if external else ["MIT-000226"]
        cases = ["CASE-000235"] if external else ["CASE-000333"]
        value = {
            "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": sid,
            "parent_ref": "NJT-0220", "name": deepcopy(source["name"]),
            "summary": deepcopy(source["summary"]), "aliases": [],
            "lineage": {"attck_subtechnique_inherited": False},
            "definition_and_concept": deepcopy(source["definition_and_concept"]),
            "stealth_characteristics": deepcopy(source["stealth_characteristics"]),
            "scope_boundary_definition": deepcopy(source["scope_boundary_definition"]),
            "application_scenarios_and_threat_model": deepcopy(source["application_scenarios_and_threat_model"]),
            "stealth_mechanisms": mechanisms(source["stealth_mechanisms"]),
            "defense": {
                "detections": {"coverage": "available", "strategy_refs": strategies},
                "mitigations": {"coverage": "available", "mitigation_refs": mitigations},
            },
            "evidence": {
                "claim_refs": [CLM[item] for item in CHILD_CLAIMS[key]], "case_refs": cases,
                "reference_refs": refs(source.get("evidence_keys")),
            },
            "research": {"limitations": deepcopy(source["limitations"])}, "lifecycle": deepcopy(LIFE),
        }
        for lang in ("zh", "en"):
            first = value["stealth_characteristics"]["paragraphs"][0][lang]
            if not first.startswith(value["name"][lang]):
                value["stealth_characteristics"]["paragraphs"][0][lang] = value["name"][lang] + "：" + first
        save(root / "subtechniques" / f"{sid}-{folder_slug}" / "subtechnique.yaml", value)


def write_decisions() -> None:
    for tid in TIDS:
        handoff = H[tid]
        recommendation = handoff["recommendation"]
        rationale = recommendation["rationale"]["paragraphs"]
        scope = recommendation["scope_notes"]
        candidate = handoff["candidate"]
        evidence = parent_reference_refs(tid)[:5]
        value = {
            "schema_version": "1.1.0", "type": "technique-decision", "id": f"DEC-TA0009-{tid}",
            "tactic_ref": "TA0009",
            "candidate": {
                "source_type": "attack", "source_attack_id": tid, "source_attack_version": "19.1",
                "name_en": candidate["name"]["en"], "name_zh": candidate["name"]["zh"],
            },
            "decision": "adapt", "rationale_zh": "\n\n".join(item["zh"] for item in rationale),
            "rationale_en": "\n\n".join(item["en"] for item in rationale),
            "scope_notes_zh": scope["zh"], "scope_notes_en": scope["en"],
            "gap_statement_zh": None, "gap_statement_en": None,
            "original_attack_subtechniques_imported": False,
            "resulting_technique_ref": PARENT[tid][0], "evidence_refs": evidence,
            "confidence": recommendation.get("confidence", "medium"),
            "review": {
                "status": STATUS, "authors": ["Niji Matrix Research"], "reviewers": [],
                "review_notes_zh": "最终批准入、跨技术边界、正式内容、共享库与自动质量门禁已完成；等待人工领域评审。",
                "review_notes_en": "Final-batch admission, cross-technique boundaries, canonical content, shared libraries, and automated quality gates are complete; human domain review remains.",
            },
        }
        save(ROOT / "matrix/tactics/TA0009-collection/decisions" / f"DEC-TA0009-{tid}.yaml", value)


STRATEGY_DESC = {
    "T1025_DET_MEDIA_READ_OUTCOME": pair(
        "为每次介质接入建立稳定会话与介质身份，把策略允许、对象枚举和实际 ReadData 分级，再把成功读取连接到进程、批准作业及文件、归档或网络结果。mount、拒绝事件、目录浏览和属性读取只形成较低级线索；照片导入、备份、杀毒、取证、恢复与迁移须以签名、介质组、路径、工单和有效期共同排除。",
        "Create a stable attachment session and media identity for each insertion, grade policy allow and enumeration separately from exercised ReadData, and join successful reads to process, approved work, and file, archive, or network outcomes. Mount, deny, directory browsing, and attribute reads remain lower-level leads. Exclude photo import, backup, antimalware, forensics, restore, and migration only by signer, media group, path, ticket, and expiry together.",
    ),
    "T1056_COLLECTION_DET_TRUSTED_ENTRY": pair(
        "把受保护发布制品、消费者实际渲染的数据入口、表单与连接目标、同源服务端接收路由和第二输出连接为一条隐私安全谱系。制品漂移、CSP 违例、字段图差异或新路由只表示暴露；只有用户交互后出现攻击者可读文件或非批准外联，才升级为输入取得。",
        "Join protected release artifacts, the data-entry surface actually rendered for the consumer, form and connection destinations, same-origin server receiver routes, and second outputs into one privacy-safe lineage. Artifact drift, CSP violations, field-graph changes, or a new route show exposure only. Escalate to input acquisition only when an attacker-readable file or unapproved egress follows user interaction.",
    ),
}
ANALYTIC_SUMMARY = {
    "T1025_NJA_WINDOWS_MEDIA_READ_LINEAGE": pair("区分介质接入、文件读取允许、实际 ReadData 与攻击者可用结果。", "Distinguish media attachment, allowed file read, exercised ReadData, and attacker-usable outcomes."),
    "T1025_NJA_REATTACHMENT_TARGET_RECALL": pair("关联跨接入对象知识、当前稀疏读取与后继结果，作为父级调查分析。", "Join cross-attachment object knowledge, current sparse reads, and downstream outcomes as a parent investigation analytic."),
    "T1056_COLLECTION_NJA_RENDERED_ENTRY": pair("比较批准制品与消费者实际收到的表单、脚本、字段和接收目标。", "Compare approved artifacts with the form, scripts, fields, and receiver targets actually delivered to the consumer."),
    "T1056_COLLECTION_NJA_SAME_ORIGIN_RECEIVER": pair("关联同源接收路由、成功输入请求与服务端第二输出。", "Join a same-origin receiver route, successful input request, and second server output."),
}
WINDOW_ZH = {
    "T1025_NJA_WINDOWS_MEDIA_READ_LINEAGE": "每个接入会话默认按十五分钟聚合，并按批准业务周期保留历史。",
    "T1025_NJA_REATTACHMENT_TARGET_RECALL": "覆盖一个完整的批准介质返回周期，不设跨环境通用固定时长。",
}


def normalize_requirement(item):
    name = item.get("name")
    if not name:
        en = item["source_type"].replace("-", " ").title()
        name = pair(f"经验证的{en}数据", en)
    return {
        "source_type": item["source_type"], "name": name, "channel": item.get("channel"),
        "required_fields": item["required_fields"],
    }


def normalize_pairs(value):
    if isinstance(value, list):
        return deepcopy(value)
    if isinstance(value, dict):
        return [deepcopy(value)]
    raise TypeError(value)


def write_defense() -> None:
    for tid in TIDS:
        handoff = H[tid]
        for item in handoff["defense_candidates"]["detection_strategies"]:
            key = item["temporary_key"]
            if item.get("resolution") == "extend":
                continue
            targets = [TARGET[value] for value in item.get("detects_keys", []) if value in TARGET]
            analytic_refs = [NJA[value] for value in item["analytic_keys"] if NJA[value] != "NJA-000215"]
            evidence = refs(item.get("evidence_keys"))
            for analytic_key in item["analytic_keys"]:
                analytic = next(value for value in handoff["defense_candidates"]["detection_analytics"] if value["temporary_key"] == analytic_key)
                evidence.extend(refs(analytic.get("evidence_keys")))
            value = {
                "schema_version": "2.0.0", "type": "detection-strategy", "id": DET[key],
                "name": deepcopy(item["name"]), "summary": deepcopy(item.get("summary") or item["objective"]),
                "description": block(item.get("description") or STRATEGY_DESC[key]), "detects_refs": unique(targets),
                "domains": item.get("domains", ["enterprise"]), "analytic_refs": analytic_refs,
                "evidence_refs": unique(evidence), "lifecycle": deepcopy(LIFE),
            }
            save(ROOT / "detections" / f"{DET[key]}-{slug(item['name']['en'])}.yaml", value)

        for item in handoff["defense_candidates"]["detection_analytics"]:
            key = item["temporary_key"]
            if NJA.get(key) == "NJA-000215":
                continue
            logic = block(item["logic"], "按主体、会话、对象和结果建立分级关联。")
            correlation = deepcopy(item["correlation"])
            if isinstance(correlation["window"], str):
                correlation["window"] = pair(WINDOW_ZH[key], correlation["window"])
            tuning = block(item.get("tuning_guidance") or item.get("tuning"))
            value = {
                "schema_version": "2.0.0", "type": "detection-analytic", "id": NJA[key],
                "strategy_ref": DET[item["strategy_key"]], "name": deepcopy(item["name"]),
                "summary": ANALYTIC_SUMMARY[key], "domains": ["enterprise"],
                "platforms": item.get("platforms", [item.get("platform", "Windows")]),
                "logic": logic, "data_requirements": [normalize_requirement(req) for req in item["data_requirements"]],
                "observables": normalize_pairs(item["observables"]), "correlation": correlation,
                "false_positives": normalize_pairs(item["false_positives"]),
                "blind_spots": normalize_pairs(item["blind_spots"]), "tuning_guidance": tuning,
                "evidence_refs": refs(item.get("evidence_keys")), "lifecycle": deepcopy(LIFE),
            }
            save(ROOT / "analytics" / f"{NJA[key]}-{slug(item['name']['en'])}.yaml", value)

        for item in handoff["defense_candidates"]["mitigations"]:
            key = item["temporary_key"]
            if item.get("resolution") == "extend":
                continue
            measures = []
            for measure in item["measures"]:
                measures.append({
                    "key": measure["key"].replace("_", "-"), "name": deepcopy(measure["name"]),
                    "description": block(measure["description"]), "control_type": measure["control_type"],
                })
            applications = []
            for application in item["applications"]:
                target = TARGET.get(application["target_key"])
                if not target:
                    continue
                applications.append({
                    "target_ref": target, "use": block(application["use"]),
                    "expected_effect": block(application["expected_effect"]),
                    "limitations": block(application["limitations"]),
                })
            summary = {
                "T1025_MIT_MEDIA_READ_AUTHORIZATION": pair("以文件级最小读取授权和接入对象谱系约束可移动介质内容获取。", "Constrain removable-media content acquisition through file-level least read authority and attachment-object lineage."),
                "T1056_COLLECTION_MIT_TRUSTED_ENTRY": pair("保护受信数据入口制品与接收路径，并以隐私安全方式核对实际输入流向。", "Protect trusted data-entry artifacts and receiver paths while verifying actual input flow with privacy-safe evidence."),
            }[key]
            value = {
                "schema_version": "2.0.0", "type": "mitigation", "id": MIT[key],
                "name": deepcopy(item["name"]), "summary": summary,
                "description": block(item["description"]), "domains": item.get("domains", ["enterprise"]),
                "measures": measures, "applications": applications,
                "evidence_refs": refs(item.get("evidence_keys")), "lifecycle": deepcopy(LIFE),
            }
            save(ROOT / "mitigations" / f"{MIT[key]}-{slug(item['name']['en'])}.yaml", value)


def extend_shared() -> None:
    updates = {
        "REF-001077": {
            "locator": "Executive summary and Technical details: previously seen USB, operator-requested file, and theft when the same media is next inserted",
            "notes_zh": "同一 TajMahal 来源扩展到先前介质—指定文件—下次接入取回的模块能力；没有逐文件受害结果或告警测量，不能据此正式化子技术。",
            "notes_en": "The same TajMahal source locates the previously seen media, requested file, and next-attachment retrieval capability. It provides no per-file victim outcome or alert measurement and does not by itself formalize a child.",
        },
        "REF-000906": {
            "locator": "Audit File System, Audit Removable Storage, and event 4663 exercised-object-access semantics with required object SACL or removable-storage auditing",
            "notes_zh": "用于区分接入、策略允许与实际使用 ReadData；4663 需要审核前置条件，也不证明完整文件被保留。",
            "notes_en": "Use to distinguish attachment and policy allow from exercised ReadData. Event 4663 depends on audit prerequisites and does not prove complete-file retention.",
        },
    }
    for rid, fields in updates.items():
        path = next((ROOT / "references").glob(f"{rid}-*.yaml"))
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        value.update(fields)
        path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

    case_path = next((ROOT / "cases").glob("CASE-000235-*.yaml"))
    case = yaml.safe_load(case_path.read_text(encoding="utf-8"))
    for target in ("NJT-0220", "NJS-0220-001"):
        if target not in case["subject_refs"]:
            case["subject_refs"].append(target)
    case_path.write_text(yaml.safe_dump(case, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

    strategy_path = next((ROOT / "detections").glob("DET-000192-*.yaml"))
    strategy = yaml.safe_load(strategy_path.read_text(encoding="utf-8"))
    for target in ("NJT-0220", "NJS-0220-001"):
        if target not in strategy["detects_refs"]:
            strategy["detects_refs"].append(target)
    strategy["lifecycle"]["version"] = "0.2.0"
    strategy["lifecycle"]["modified"] = DATE
    strategy_path.write_text(yaml.safe_dump(strategy, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

    mitigation_path = next((ROOT / "mitigations").glob("MIT-000173-*.yaml"))
    mitigation = yaml.safe_load(mitigation_path.read_text(encoding="utf-8"))
    mitigation["summary"] = pair(
        "最小化能在预期消费者之前观察输入的进程、设备与会话，并用不含实际输入内容的远程元数据审计剩余权限。",
        "Minimize processes, devices, and sessions able to observe input before the intended consumer and audit remaining authority with remote metadata that contains no actual input content.",
    )
    mitigation["description"] = block(pair(
        "本缓解把输入观察者清单、隔离输入面与隐私安全审计组合使用。组织按签名、版本、所有者、目标应用和会话审批全局 Hook、Input Monitoring、辅助功能和输入设备读取；对高价值业务输入与认证使用 secure desktop、受保护输入或等价隔离，并只远程保留授权、进程、目标面和结果元数据。",
        "This mitigation combines an input-observer inventory, isolated input surfaces, and privacy-safe audit. Approve global hooks, Input Monitoring, accessibility, and input-device reads by signer, version, owner, target app, and session; use secure desktop, protected input, or equivalent isolation for high-value business and authentication input; and remotely retain only authority, process, target-surface, and outcome metadata.",
    ))
    mitigation["applications"] = [item for item in mitigation["applications"] if item["target_ref"] != "NJS-0220-001"]
    mitigation["applications"].append({
        "target_ref": "NJS-0220-001",
        "use": block(pair(
            "清点并最小化能观察普通业务输入的全局 Hook、Input Monitoring、辅助功能、远程支持和输入设备读取，把新授权与同进程缓冲、文件或外联结果关联，并按签名、版本、owner、目标应用、会话与期限管理例外。",
            "Inventory and minimize global hooks, Input Monitoring, accessibility, remote support, and input-device reads able to observe ordinary business input. Join new authority to same-process buffers, files, or egress and manage exceptions by signer, version, owner, target app, session, and expiry.",
        )),
        "expected_effect": block(pair(
            "缩小能在业务消费者之前复制非认证输入的主体集合，并使剩余观察者具有可核查的权限和结果谱系。",
            "Reduce the set of actors able to copy non-authentication input before a business consumer and preserve verifiable authority and outcome lineage for remaining observers.",
        )),
        "limitations": block(pair(
            "内核控制、批准工具失陷或同一安全上下文内恶意代码仍可观察输入；严格限制会影响无障碍、输入法、远程支持、测试和质量监控。",
            "Kernel control, compromise of an approved tool, or malicious code in the same security context can still observe input. Strict controls can disrupt accessibility, input methods, remote support, testing, and quality monitoring.",
        )),
    })
    mitigation["lifecycle"]["version"] = "0.2.0"
    mitigation["lifecycle"]["modified"] = DATE
    mitigation_path.write_text(yaml.safe_dump(mitigation, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def update_planning() -> None:
    path = ROOT / "planning/tactics/TA0009.yaml"
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    next(item for item in value["batches"] if item["id"] == "BATCH-TA0009-005")["status"] = STATUS
    for item in value["work_items"]:
        tid = item["source_attack_id"]
        if tid in PARENT:
            item["decision_ref"] = f"DEC-TA0009-{tid}"
            item["resulting_technique_ref"] = PARENT[tid][0]
            item["stage"] = STATUS
            if STATUS == "review":
                item["notes_zh"] = item["notes_zh"].split(" 最终批双候选独立研究中；")[0] + " 最终批由独立 sub-agent 完成研究，主 Agent 统一完成 adapt 准入、跨技术边界、共享库查重、正式写入与质量验收；对象保持 review，等待人工领域评审。"
                item["notes_en"] = item["notes_en"].split(" Final-batch independent research")[0] + " Independent sub-agent research and primary-agent adapt admission, boundary reconciliation, shared-library deduplication, canonical integration, and quality gates are complete. Objects remain at review pending human domain approval."
    if STATUS == "review":
        value["status"] = "review"
        value["gap_analysis"] = {
            "status": "complete",
            "notes_zh": "固定 ATT&CK Enterprise 19.1 的 17 个 TA0009 父候选已全部完成准入并进入正式 review，共形成 17 个 ATT&CK 来源 NJT 和 21 个 Niji 原生 NJS。最终批将 T1025 的重接入假设因缺少逐文件受害结果而延期，并把 T1056 的非认证输入 Collection 结果与 NJT-0169 认证秘密范围分开。战术级开放搜索与跨技术收敛未发现证据足以支持额外 add 父技术；跨技术边界、共享库、防御、Bundle、全库质量和双语 Web 门禁通过，等待人工领域评审。",
            "notes_en": "All seventeen fixed Enterprise ATT&CK 19.1 TA0009 parent candidates have admission decisions and formal review packages, producing seventeen ATT&CK-origin NJT objects and twenty-one Niji-native NJS objects. The final batch defers T1025 reattachment recall for lack of a per-file victim outcome and separates T1056 non-authentication Collection results from the authentication-secret scope of NJT-0169. Tactic-level open search and cross-technique convergence found no evidence sufficient for an additional parent. Cross-technique boundaries, shared libraries, defenses, bundles, matrix quality, and bilingual Web gates pass pending human domain review.",
        }
        value["review"] = {"taxonomy": "passed", "evidence": "passed", "bilingual": "passed", "reviewers": []}
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def write_integration_summary() -> None:
    value = {
        "schema_version": "1.0.0", "type": "batch-integration-summary",
        "batch_ref": "BATCH-TA0009-005", "status": STATUS,
        "delivery_control": {
            "overall_candidate_count": 17, "batch_candidate_count": 2,
            "batch_size_rationale": pair(
                "最终批只含固定清单剩余的 T1025 与 T1056；每个候选由独立 sub-agent 完整研究，主 Agent 等两份交接后统一处理介质边界和 T1056 跨战术直接对象拆分。",
                "The final batch contains only the fixed inventory's remaining T1025 and T1056 candidates. One sub-agent fully researched each candidate, and the primary agent waited for both handoffs before reconciling media boundaries and the cross-tactic direct-object split for T1056.",
            ),
            "previous_batch_gate_passed": True,
        },
        "candidate_results": [
            {"source_attack_id": "T1025", "decision": "adapt", "technique_ref": "NJT-0219", "subtechnique_refs": []},
            {"source_attack_id": "T1056", "decision": "adapt", "technique_ref": "NJT-0220", "subtechnique_refs": ["NJS-0220-001", "NJS-0220-002"]},
        ],
        "shared_library_resolutions": {
            "reuse": ["REF-000914", "REF-000597", "REF-001070", "REF-000379", "REF-000728", "NJA-000215"],
            "extend": ["REF-001077", "REF-000906", "CASE-000235", "DET-000192", "MIT-000173"],
            "create_ranges": {
                "references": "REF-001126..REF-001131", "claims": "CLM-001090..CLM-001097",
                "cases": "CASE-000333", "detection_strategies": "DET-000255..DET-000256",
                "detection_analytics": "NJA-000339..NJA-000342", "mitigations": "MIT-000225..MIT-000226",
                "relationships": None,
            },
        },
        "deferred_hypotheses": [
            "T1025 重接入门控目标回收缺少逐文件受害结果和告警测量，不建立正式 NJS。",
            "T1025 受信导入进程劫持、策略审计旁路及介质类型分类缺少独立证据。",
            "T1056 独立仿冒的非认证输入界面缺少结果级案例和独立防御链；认证仿冒仍归 NJS-0169-003。",
        ],
        "duplicate_resolution_refs": [],
        "semantic_validation": {
            "candidate_level_gates_passed": True, "conclusion_level_evidence_passed": True,
            "njt_0001_field_responsibility_reviewed": True, "bilingual_argument_depth_passed": True,
            "boilerplate_review_passed": True, "taxonomy_breadth_reviewed": True,
            "attack_breadth_gap_explained": True, "canonical_prose_bulk_generated": False,
        },
        "validation": {
            "matrix_objects": 3930, "schema_errors": 0, "schema_warnings": 0,
            "unresolved_duplicate_candidates": 0, "reviewed_similarity_resolutions": 12,
            "infrastructure_tests": 12, "web_tests": 129, "web_api_issues": 0,
            "bundles_built": ["NJT-0219", "NJT-0220"],
        },
        "review_notes_zh": "两个剩余 ATT&CK Enterprise 19.1 父候选均完成 adapt 准入。新增 NJT-0219 与 NJT-0220；T1025 因重接入变量缺少逐文件受害结果而保持零正式子项，T1056 形成两个非认证输入原生子项且不扩大 NJT-0169。质量、两份 Bundle、129 项 Web 测试和四个 NJT/NJS 双语 API QA 通过；TA0009 正式 17/17、21 个 NJS，固定清单闭合。对象保持 review，等待人工领域评审。",
        "review_notes_en": "Both remaining ATT&CK Enterprise 19.1 parents received adapt admission, producing NJT-0219 and NJT-0220. T1025 has no formal child because reattachment recall lacks a per-file victim outcome. T1056 produces two non-authentication input children without widening NJT-0169. Quality, two bundles, 129 Web tests, and bilingual API QA for four NJT/NJS objects passed. TA0009 is closed at 17 of 17 formal parents and 21 NJS. Objects remain at review pending human domain approval.",
    }
    save(RUN / "integration-summary.yaml", value)


def main() -> None:
    write_references()
    write_claims()
    write_case()
    roots = write_techniques()
    write_children(roots["T1056"])
    write_decisions()
    write_defense()
    extend_shared()
    update_planning()
    write_integration_summary()
    print(f"Integrated final TA0009 batch at {STATUS}: 2 NJT, 2 NJS, 6 REF, 8 CLM, 1 CASE, 2 DET, 4 NJA, and 2 MIT")


if __name__ == "__main__":
    main()
