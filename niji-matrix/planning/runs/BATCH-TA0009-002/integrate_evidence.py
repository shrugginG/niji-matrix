"""Serialize reviewed admission, atomic claims, and narrowly scoped cases."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
H = {t: yaml.safe_load((RUN / f"{t}-handoff.yaml").read_text(encoding="utf-8"))
     for t in ("T1557", "T1213", "T1114", "T1185", "T1123")}

REF = {
    "REF-000488": "REF-000488", "REF-000379": "REF-000379", "REF-000509": "REF-000509",
    "REF-000366": "REF-000366", "REF-000491": "REF-000491", "REF-000515": "REF-000515",
    "T1557C_REF_KAZAKH_PAPER": "REF-000556", "T1557C_REF_MOZILLA_KAZAKH": "REF-000557",
    "T1213_R_ATTACK_PARENT": "REF-000558", "T1213_R_ATTACK_DET": "REF-000559",
    "T1213_R_MANDIANT_SEARCH": "REF-000560", "T1213_R_M365_AUDIT": "REF-000561",
    "T1213_R_M365_FIELDS": "REF-000562", "T1213_R_M365_GETSTARTED": "REF-000563",
    "T1213_R_ATLASSIAN_AUDIT": "REF-000564", "T1213_R_MS_SAM": "REF-000565",
    "T1114_REF_ATTACK": "REF-000566", "T1114_REF_MS_MAIL_AUDIT": "REF-000567",
    "T1114_REF_MS_CACHE": "REF-000568", "T1114_REF_MANDIANT_APT1": "REF-000569",
    "T1114_REF_MS_BEC": "REF-000570", "T1114_REF_MS_FORWARD_REPORT": "REF-000571",
    "T1114_REF_MS_RULE_AUDIT": "REF-000572", "T1114_REF_MS_FORWARD_CONTROL": "REF-000573",
    "T1114_REF_MS_4663": "REF-000379", "T1114_REF_VOLEXITY": "REF-000509",
    "T1185_REF_ATTACK": "REF-000574", "T1185_REF_COBALT": "REF-000575",
    "T1185_REF_KASPERSKY": "REF-000576", "T1185_REF_TALOS": "REF-000577",
    "T1185_REF_ELASTIC": "REF-000578", "T1185_REF_CHROME_DEBUGGER": "REF-000579",
    "T1185_REF_MS_POLICY": "REF-000580", "T1185_REF_MS_EXTINV": "REF-000581",
    "T1123_REF_ATTACK": "REF-000582", "T1123_REF_ESET_PDF": "REF-000583",
    "T1123_REF_T9000": "REF-000584", "T1123_REF_MITRE_DET": "REF-000585",
    "T1123_REF_MS_PRIVACY": "REF-000586", "T1123_REF_MS_CSP": "REF-000587",
    "T1123_REF_APPLE_MIC": "REF-000588",
}


def refs(keys):
    return list(dict.fromkeys(REF[k] for k in keys))


def save(folder, filename, data):
    p = ROOT / folder / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def source_claim(tactic, key):
    for x in H[tactic]["library_candidates"]["claims"]:
        if x.get("key") == key or x.get("temporary_key") == key:
            if "statement" in x: return x["statement"], x["evidence_keys"]
            if "proposition" in x: return x["proposition"], x["evidence_keys"]
            return {"zh": x["proposition_zh"], "en": x["proposition_en"]}, x["evidence_keys"]
    raise KeyError((tactic, key))


# ID, tactic, research key, filename, claim type, subjects, evidence mode,
# calibrated confidence. Every proposition is copied from an independently
# researched handoff and checked against its exact source scope by the primary.
CLAIMS = [
    ("CLM-000728", "T1557", "T1557C_CLM_SCOPE", "collection-content-path-boundary", "technique-relevance", ["NJT-0142"], "strongly-inferred", "medium"),
    ("CLM-000729", "T1557", "T1557C_CLM_SELECTIVE", "selective-sni-path-interception", "subtechnique-existence", ["NJT-0142", "NJS-0142-001"], "directly-observed", "high"),
    ("CLM-000730", "T1557", "T1557C_CLM_TRUSTED_TERMINATION", "trusted-root-readable-termination", "subtechnique-existence", ["NJT-0142", "NJS-0142-002"], "strongly-inferred", "medium"),
    ("CLM-000731", "T1557", "T1557C_CLM_PRESERVED_RESPONSE", "measured-content-preservation-limit", "mechanism-mapping", ["NJT-0142", "NJS-0142-002"], "directly-observed", "high"),
    ("CLM-000732", "T1213", "T1213_CLM_PARENT_SCOPE", "information-repository-acquisition-boundary", "technique-relevance", ["NJT-0143"], "strongly-inferred", "medium"),
    ("CLM-000733", "T1213", "T1213_CLM_SEARCH_READ", "unc6661-search-download-cooccurrence", "case-attribution", ["NJT-0143"], "directly-observed", "medium"),
    ("CLM-000734", "T1213", "T1213_CLM_TELEMETRY", "repository-audit-configuration-conditions", "detection", ["NJT-0143", "NJS-0143-001"], "strongly-inferred", "medium"),
    ("CLM-000735", "T1213", "T1213_CLM_LOW_VOLUME_INFERENCE", "conditional-selective-read-signal", "subtechnique-existence", ["NJT-0143", "NJS-0143-001"], "hypothesized", "low"),
    ("CLM-000736", "T1114", "T1114_CLM_PARENT", "email-content-acquisition-observation", "technique-relevance", ["NJT-0144"], "strongly-inferred", "high"),
    ("CLM-000737", "T1114", "T1114_CLM_REPLICA", "offline-mail-replica-read-differential", "subtechnique-existence", ["NJT-0144", "NJS-0144-001"], "strongly-inferred", "medium"),
    ("CLM-000738", "T1114", "T1114_CLM_ARRIVAL", "arrival-conditional-mail-copy", "subtechnique-existence", ["NJT-0144", "NJS-0144-002"], "strongly-inferred", "high"),
    ("CLM-000740", "T1185", "T1185_CLM_PARENT", "active-browser-context-content-access", "technique-relevance", ["NJT-0145"], "strongly-inferred", "medium"),
    ("CLM-000741", "T1185", "T1185_CLM_COVIEW", "co-viewed-page-content-interposition", "subtechnique-existence", ["NJT-0145", "NJS-0145-001"], "strongly-inferred", "medium"),
    ("CLM-000742", "T1185", "T1185_CLM_RELAY", "browser-context-proxy-capability", "subtechnique-existence", ["NJT-0145", "NJS-0145-002"], "hypothesized", "low"),
    ("CLM-000743", "T1123", "T1123_CLM_PARENT", "audio-capture-behavior", "technique-relevance", ["NJT-0146"], "directly-observed", "high"),
    ("CLM-000744", "T1123", "T1123_CLM_PROCESS", "attor-meeting-process-recording", "subtechnique-existence", ["NJT-0146", "NJS-0146-001"], "strongly-inferred", "medium"),
    ("CLM-000745", "T1123", "T1123_CLM_CALL", "t9000-call-interface-recording", "case-attribution", ["NJT-0146"], "directly-observed", "medium"),
]

for cid, tactic, key, slug, kind, subjects, mode, confidence in CLAIMS:
    statement, evidence = source_claim(tactic, key)
    save("claims", f"{cid}-{slug}.yaml", {
        "schema_version": "1.0.0", "type": "claim", "id": cid,
        "claim_type": kind, "statement_zh": statement["zh"], "statement_en": statement["en"],
        "subject_refs": subjects, "evidence_refs": refs(evidence),
        "evidence_mode": mode, "confidence": confidence, "status": "draft",
    })

save("claims", "CLM-000739-mail-audit-condition.yaml", {
    "schema_version": "1.0.0", "type": "claim", "id": "CLM-000739", "claim_type": "detection",
    "statement_zh": "邮件服务器的逐封访问、自动转发结果和规则变更分别依赖适用许可、审计配置与消息追踪；缺少任一记录不能单独证明没有离线读取或规则副本。",
    "statement_en": "Per-message server access, auto-forward outcomes, and rule changes depend on applicable licensing, audit configuration, and message trace. Absence of any one record does not alone establish that no offline read or rule-generated copy occurred.",
    "subject_refs": ["NJT-0144", "NJS-0144-001", "NJS-0144-002"],
    "evidence_refs": ["REF-000567", "REF-000571", "REF-000572"],
    "evidence_mode": "strongly-inferred", "confidence": "high", "status": "draft",
})


def case(cid, slug, name_zh, name_en, actor, body_zh, body_en, subjects, evidence,
         time_range=None, confidence="medium"):
    save("cases", f"{cid}-{slug}.yaml", {
        "schema_version": "1.0.0", "type": "case", "id": cid,
        "name_zh": name_zh, "name_en": name_en, "actor_or_campaign": actor,
        "subject_refs": subjects, "description_zh": body_zh, "description_en": body_en,
        "time_range": time_range, "target_sectors_zh": [], "target_sectors_en": [],
        "evidence_refs": evidence, "confidence": confidence, "status": "draft",
    })


case("CASE-000191", "qaznet-selective-https-interception", "Qaznet 选择性 HTTPS 中间介入", "Qaznet Selective HTTPS Interception", "Qaznet Trust Network",
     "IMC 研究者在 2019 年测到部分哈萨克斯坦路径和通信站点 SNI 触发 Qaznet 替代证书，自控源站见到中间节点上游握手；测试响应未见改变。案例只支持选择性介入和可解密条件，不证明任何具体用户正文已被保存。",
     "IMC researchers measured Qaznet substitute certificates for selected Kazakhstan paths and communications-site SNIs in 2019 and observed the intermediary's upstream handshake at a controlled origin; test responses showed no change. The case supports selective interposition and decryptability conditions, not retention of any particular user's body.",
     ["NJT-0142", "NJS-0142-001", "NJS-0142-002"], ["REF-000556", "REF-000557"], "2019", "high")
case("CASE-000192", "unc6661-search-and-sharepoint-download", "UNC6661 搜索与 SharePoint 下载共现", "UNC6661 Search and SharePoint Download Co-Occurrence", "UNC6661",
     "GTIG 记录 UNC6661 在云应用中使用敏感词搜索，并在同一行动中观察到 SharePoint 下载。公开资料没有建立某个搜索词与某个下载文件的同对象链，亦未量化匿迹效果，因此本案例只支持父级内容获取背景。",
     "GTIG recorded UNC6661 searching cloud apps for sensitive terms and observed SharePoint downloads in the same activity. The public account does not join a term to a downloaded file or measure stealth, so this case supports parent-level acquisition context only.",
     ["NJT-0143"], ["REF-000560"], "2026", "medium")
case("CASE-000193", "apt1-getmail-pst-extraction", "APT1 GETMAIL 从 PST 抽取邮件", "APT1 GETMAIL Extraction from PST", "APT1",
     "Mandiant 报告 GETMAIL 从既有 PST 归档按日期抽取邮件和附件，观察到攻击者连续四周每周取上周邮件。该行为证明离线邮件副本读取；不证明 OST 也被攻击或服务器端审计实际漏报。",
     "Mandiant reported GETMAIL extracting messages and attachments by date from an existing PST archive and observed an intruder returning weekly for four weeks for the prior week's mail. This establishes offline replica reading, not an observed OST attack or measured server-audit miss.",
     ["NJT-0144", "NJS-0144-001"], ["REF-000569"], None, "high")
case("CASE-000194", "microsoft-bec-keyword-forwarding", "Microsoft 观察的关键词条件转发", "Microsoft-Observed Keyword-Conditional Forwarding", "BEC activity observed by Microsoft",
     "Microsoft 在多个受损邮箱发现针对 invoice、payment 等词的转发规则，把匹配邮件送往攻击者控制地址，也观察到删除规则。公开报告未给出逐封匹配消息的完整路由日志，故案例只证明规则与持续分流行为，不证明每封消息实际到达。",
     "Microsoft found forwarding rules for words such as invoice and payment across compromised mailboxes, routing matching mail to attacker addresses, and also observed deletion rules. The report does not publish complete per-message routing logs, so the case supports the rule and continuing diversion behavior, not arrival of every message.",
     ["NJT-0144", "NJS-0144-002"], ["REF-000570"], None, "high")
case("CASE-000195", "qakbot-browser-network-hook", "QakBot 浏览器网络 Hook 与定向注入", "QakBot Browser Network Hook and Targeted Injection", "QakBot",
     "Kaspersky 在 QakBot 样本中分析到注入浏览器进程的网络 API Hook，目标金融页面被访问时插入 JavaScript。该事实支持活动页面内的控制与内容可接触性，不能从 Hook 存在推断每个受害者页面内容已被保存。",
     "Kaspersky analyzed QakBot's browser-process network API hooks and JavaScript injection on visits to targeted financial pages. This supports control and a content-access opportunity inside an active page, not proof that content from every victim page was saved.",
     ["NJT-0145", "NJS-0145-001"], ["REF-000576"], None, "medium")
case("CASE-000196", "kremlin-extension-page-source-capability", "KREMLIN 扩展页面源码取得能力", "KREMLIN Extension Page-Source Acquisition Capability", "KREMLIN browser extension",
     "Elastic 对恶意扩展样本的分析显示其包含页面源码和匹配请求上传命令，并在研究者实验页面验证了行为。此案例支持样本能力和实验结果，未给出具体真实受害者页面被取走的完整事件链。",
     "Elastic's malicious-extension analysis found commands to upload page source and matched requests and reproduced the behavior on a researcher test page. This supports sample capability and lab results, not a complete chain for a specific real victim page.",
     ["NJT-0145", "NJS-0145-001"], ["REF-000578"], None, "medium")
case("CASE-000197", "attor-teleconference-process-audio", "Attor 会议进程归因录音", "Attor Teleconference-Process-Attributed Recording", "Attor",
     "ESET 逆向发现 Attor 录音插件仅在列名电话会议应用进程中激活，调用麦克风并把加密音频写入共享上传目录。作者提出这种进程选择可能降低用户怀疑；报告没有量化告警变化。",
     "ESET reverse engineered Attor's recorder activating only in named teleconference-app processes, using the microphone, and writing encrypted audio to a shared upload directory. The authors suggest that process choice may reduce suspicion; the report does not quantify alert changes.",
     ["NJT-0146", "NJS-0146-001"], ["REF-000583"], None, "high")
case("CASE-000198", "t9000-skype-call-recording", "T9000 经 Skype 接口录制通话", "T9000 Skype-Interface Call Recording", "T9000",
     "Unit 42 分析 T9000 经已登录 Skype 的接口在用户许可后录制通话，临时文件位于应用数据目录并在会后压缩加密。该路径支持父级音频捕获和接口防御分析，不构成第二个 Niji 子项或无提示权限绕过证据。",
     "Unit 42 analyzed T9000 recording calls through a signed-in Skype interface after user approval, with temporary files under application data and later compression and encryption. This supports parent audio capture and an interface defense analytic, not a second Niji child or a promptless permission bypass.",
     ["NJT-0146"], ["REF-000584"], None, "high")


for tid, nid, source_name_zh, source_name_en, source_refs in [
    ("T1557", "NJT-0142", "攻击者居中", "Adversary-in-the-Middle", ["REF-000488", "REF-000556", "REF-000557"]),
    ("T1213", "NJT-0143", "从信息库获取数据", "Data from Information Repositories", ["REF-000558", "REF-000560", "REF-000561"]),
    ("T1114", "NJT-0144", "邮件收集", "Email Collection", ["REF-000566", "REF-000567", "REF-000569", "REF-000570"]),
    ("T1185", "NJT-0145", "浏览器会话劫持", "Browser Session Hijacking", ["REF-000574", "REF-000576", "REF-000578", "REF-000575"]),
    ("T1123", "NJT-0146", "音频捕获", "Audio Capture", ["REF-000582", "REF-000583", "REF-000584"]),
]:
    recommendation = H[tid]["recommendation"]
    rationale = recommendation["rationale"]["paragraphs"]
    scope = recommendation.get("scope_notes") or {
        "zh": "只纳入取得协作、代码或业务信息库实际内容且其查询与读取安排改变防守观察的行为。单纯搜索或权限存在不证明内容取得；T1530 云对象存储、T1602 配置存储库、T1114 邮件、NJT-0086 既有集成身份与 NJT-0135 状态化自动收集各保有直接对象。六个 ATT&CK 产品/内容子项不导入 NJS。",
        "en": "Include acquisition of actual collaboration, code, or business-repository content where query and read arrangements change defender observation. Search or permission alone does not prove acquisition. T1530 cloud object storage, T1602 configuration stores, T1114 email, NJT-0086 integration identity, and NJT-0135 stateful automation retain their direct objects. The six ATT&CK product or content children are not imported as NJS."
    }
    save("matrix/tactics/TA0009-collection/decisions", f"DEC-TA0009-{tid}.yaml", {
        "schema_version": "1.1.0", "type": "technique-decision", "id": f"DEC-TA0009-{tid}", "tactic_ref": "TA0009",
        "candidate": {"source_type": "attack", "source_attack_id": tid, "source_attack_version": "19.1",
                      "name_en": source_name_en, "name_zh": source_name_zh},
        "decision": "adapt", "rationale_zh": "\n\n".join(p["zh"] for p in rationale),
        "rationale_en": "\n\n".join(p["en"] for p in rationale),
        "scope_notes_zh": scope["zh"], "scope_notes_en": scope["en"],
        "gap_statement_zh": None, "gap_statement_en": None,
        "original_attack_subtechniques_imported": False, "resulting_technique_ref": nid,
        "evidence_refs": source_refs, "confidence": recommendation.get("confidence", "medium"),
        "review": {"status": "draft", "authors": ["Niji Matrix Research"], "reviewers": [],
                   "review_notes_zh": "第二批准入与跨技术边界已收敛，待正式内容及质量门禁。",
                   "review_notes_en": "Batch-two admission and cross-technique boundaries are converged; canonical content and quality gates remain."},
    })

print("Serialized 18 claims, 8 scoped cases, and 5 admission decisions")
