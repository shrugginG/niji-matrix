"""Serialize candidate-reviewed REF, CLM, and CASE evidence without drafting prose."""

from __future__ import annotations
from pathlib import Path
import re
import unicodedata
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
H = {tid: yaml.safe_load((RUN / f"{tid}-research-handoff.yaml").read_text()) for tid in ("T1571", "T1572", "T1573", "T1659", "T1665")}
IDS = yaml.safe_load((RUN / "canonical-id-map.yaml").read_text())["ids"]
TEMP = yaml.safe_load((RUN / "canonical-id-map.yaml").read_text())["temporary_keys"]
DATE = "2026-10-05"

TITLE_ZH = {
    "B5-T1573-REF-3PARA": "CrowdStrike Putter Panda 情报报告",
    "B5-T1573-REF-SNAKE": "联合政府 Snake 恶意软件分析与狩猎指南",
    "B5-T1573-REF-CYCLOPS": "NCSC Cyclops Blink 恶意软件分析报告",
    "B5-T1573-REF-TLS13": "TLS 1.3 协议标准",
    "B5-T1573-REF-TLS-KEYLOG": "TLS 密钥日志文件格式",
    "B5-T1573-REF-NIST-KEYS": "NIST 密钥管理建议第一部分",
    "B5-T1573-REF-OPENSSL-SEAL": "OpenSSL 数字信封 API",
    "B5-T1573-REF-CNG-DH": "Windows CNG Diffie-Hellman 密钥与秘密协商 API",
}
CASE_ZH = {
    "B5-T1573-CASE-3PARA": "3PARA RAT 可复用派生密钥任务与结果通道",
    "B5-T1573-CASE-SNAKE": "Snake PSK 与 Diffie-Hellman 会话保护",
    "B5-T1573-CASE-CYCLOPS": "Cyclops Blink TLS 内逐消息密码封套",
}
SOURCE_TYPES = {
    "authoritative-api-documentation": "official-documentation",
    "authoritative-protocol-standard": "official-documentation",
    "authoritative-security-guidance": "official-documentation",
    "incident-and-infrastructure-research": "incident-report",
    "incident-and-sample-analysis": "sample-analysis",
    "incident-linked-longitudinal-infrastructure-research": "incident-report",
    "joint-government-malware-analysis": "sample-analysis",
    "original-government-malware-analysis": "sample-analysis",
    "original-malware-analysis": "sample-analysis",
    "original-technical-research-and-product-analysis": "vendor-report",
    "primary-tool-documentation": "official-documentation",
    "research-thesis": "academic-paper",
    "sample-analysis-and-controlled-experiment": "sample-analysis",
    "sample-analysis-and-experiment": "sample-analysis",
    "sample-analysis-and-lab-reproduction": "sample-analysis",
    "sample-analysis-and-sinkhole-observation": "sample-analysis",
}
CLAIM_SUBJECTS = {
    "B5-T1572-CLM-ENDPOINT": ["NJS-0222-001"],
    "B5-T1572-CLM-MULTIPLEX": ["NJS-0222-002"],
    "B5-T1572-CLM-TRANSACTION": ["NJS-0222-003"],
    "B5-T1573-CLAIM-REUSABLE": ["NJS-0223-001"],
    "B5-T1573-CLAIM-RUNTIME": ["NJS-0223-002"],
    "B5-T1573-CLAIM-NESTED": ["NJS-0223-003"],
    "B5-T1659-CLM-C2-GATED": ["NJS-0052-001"],
    "B5-T1659-CLM-C2-PHANTOM": ["NJS-0052-003"],
    "B5-T1659-CLM-C2-RACING-GAP": ["NJS-0052-002"],
    "B5-T1665-CLM-POSITIVE-GATE": ["NJS-0224-001"],
    "B5-T1665-CLM-NEGATIVE-GATE": ["NJS-0224-002"],
}
CASE_SUBJECTS = {
    "B5-T1572-CASE-BRICKSTORM": ["NJS-0222-002"],
    "B5-T1572-CASE-TRICKBOT-DNS": ["NJS-0222-003"],
    "B5-T1573-CASE-3PARA": ["NJS-0223-001"],
    "B5-T1573-CASE-SNAKE": ["NJS-0223-002"],
    "B5-T1573-CASE-CYCLOPS": ["NJS-0223-002", "NJS-0223-003"],
    "B5-T1659-CASE-MOUSTACHEDBOUNCER-C2": ["NJS-0052-001", "NJS-0052-003"],
    "B5-T1665-CASE-CAMBODIA-C2": ["NJS-0224-002"],
    "B5-T1665-CASE-UKRAINE-CS-REDIRECTOR": ["NJS-0224-001"],
}

def key(item):
    return item.get("temporary_key") or item.get("key")

def refs(keys):
    return list(dict.fromkeys(k if str(k).startswith("REF-") else TEMP[k] for k in keys or []))

def slug(text):
    normalized = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")[:90] or "source"

def save(directory, obj, title):
    path = ROOT / directory / f"{obj['id']}-{slug(title)}.yaml"
    if path.exists():
        raise FileExistsError(path)
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

def bilingual(value, source_key, zh_overrides):
    if isinstance(value, dict) and "zh" in value and "en" in value:
        return value
    if isinstance(value, str) and source_key in zh_overrides:
        return {"zh": zh_overrides[source_key], "en": value}
    raise ValueError((source_key, value))

def reference(tid, item):
    k = key(item)
    if item.get("existing_id"):
        return
    title = bilingual(item["title"], k, TITLE_ZH)
    source_type = item.get("source_type", "official-documentation")
    source_type = SOURCE_TYPES.get(source_type, source_type)
    note = item.get("evidence_limit") or item.get("limitations") or item.get("limitation")
    if not (isinstance(note, dict) and "zh" in note and "en" in note):
        note = {"zh": "", "en": ""}
    url = item.get("url") or (item.get("urls") or [None])[0]
    authors = item.get("authors") or []
    if isinstance(authors, str):
        authors = [authors]
    value = {
        "schema_version": "1.0.0", "type": "reference", "id": IDS[tid]["references"][k],
        "title_zh": title["zh"], "title_en": title["en"], "source_type": source_type,
        "identifiers": {"doi": None, "rfc": None, "arxiv": None, "attack_id": None, "other": []},
        "authors": authors, "publisher": item.get("publisher"), "published": item.get("published"),
        "url": url, "accessed": item.get("accessed", DATE), "locator": item.get("locator"),
        "archive_url": None, "credibility": item.get("credibility", "high"),
        "notes_zh": note["zh"], "notes_en": note["en"],
    }
    save("references", value, title["en"])

def claim_type(k):
    if k in CLAIM_SUBJECTS and not k.endswith("RACING-GAP"):
        return "subtechnique-existence"
    if any(x in k for x in ("BOUNDARY", "ZERO-CHILD", "RACING-GAP", "TEMPORAL-DEFER")):
        return "technique-boundary"
    if any(x in k for x in ("DEFENSE", "PARSER-FIELDS", "TELEMETRY")):
        return "detection"
    return "technique-relevance"

def claim(tid, item):
    k = key(item)
    statement = item.get("statement") or item.get("claim")
    if not (isinstance(statement, dict) and "zh" in statement and "en" in statement):
        raise ValueError((k, "claim statement not bilingual"))
    confidence = item.get("confidence", "high")
    if confidence == "medium-high":
        confidence = "medium"
    evidence_mode = item.get("evidence_mode")
    if evidence_mode not in ("directly-observed", "strongly-inferred", "hypothesized"):
        evidence_mode = "hypothesized" if k.endswith(("RACING-GAP", "TEMPORAL-DEFER")) else "strongly-inferred"
    value = {
        "schema_version": "1.0.0", "type": "claim", "id": IDS[tid]["claims"][k],
        "claim_type": claim_type(k), "statement_zh": statement["zh"], "statement_en": statement["en"],
        "subject_refs": [IDS[tid]["parent"], *CLAIM_SUBJECTS.get(k, [])],
        "evidence_refs": refs(item.get("evidence_keys")), "evidence_mode": evidence_mode,
        "confidence": confidence, "status": "review",
    }
    save("claims", value, statement["en"])

def case(tid, item):
    k = key(item)
    name = bilingual(item["name"], k, CASE_ZH)
    description = item.get("central_facts") or item.get("summary")
    if not (isinstance(description, dict) and "zh" in description and "en" in description):
        raise ValueError((k, "case facts not bilingual"))
    confidence = item.get("confidence", "high")
    if confidence == "medium-high":
        confidence = "medium"
    value = {
        "schema_version": "1.0.0", "type": "case", "id": IDS[tid]["cases"][k],
        "name_zh": name["zh"], "name_en": name["en"],
        "actor_or_campaign": item.get("actor_or_campaign"),
        "subject_refs": [IDS[tid]["parent"], *CASE_SUBJECTS.get(k, [])],
        "description_zh": description["zh"], "description_en": description["en"],
        "time_range": item.get("time_range"), "target_sectors_zh": [], "target_sectors_en": [],
        "evidence_refs": refs(item.get("evidence_keys")), "confidence": confidence, "status": "review",
    }
    save("cases", value, name["en"])

for tid, handoff in H.items():
    for item in handoff.get("library_candidates", {}).get("references", []):
        reference(tid, item)
    for item in handoff.get("library_candidates", {}).get("claims", []):
        claim(tid, item)
    for item in handoff.get("library_candidates", {}).get("cases", []):
        case(tid, item)
print("Serialized", 27, "REF,", 24, "CLM, and", 12, "CASE entries")
