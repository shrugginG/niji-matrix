"""Mechanically assemble five reviewed bilingual parent/child research drafts."""

from copy import deepcopy
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
H = {t: yaml.safe_load((RUN / f"{t}-handoff.yaml").read_text(encoding="utf-8"))
     for t in ("T1557", "T1213", "T1114", "T1185", "T1123")}
BASE = ROOT / "matrix/tactics/TA0009-collection/techniques"
LIFE = {"status": "draft", "version": "1.0.0", "created": "2026-09-22", "modified": "2026-09-22",
        "contributors": ["Niji Matrix Research"], "reviewers": []}

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


def block(zh, en):
    return {"paragraphs": [{"zh": zh, "en": en}]}


def refs(keys):
    return list(dict.fromkeys(REF[k] for k in keys))


def mechanism_items(source, confidence_override=None):
    out = []
    for item in source:
        value = {k: deepcopy(item[k]) for k in ("mechanism_ref", "role", "summary", "analysis", "confidence")}
        value["evidence_refs"] = refs(item.get("evidence_keys", []))
        if confidence_override:
            value["confidence"] = confidence_override
        out.append(value)
    return out


def defense(strategies, mitigations):
    return {"detections": {"coverage": "available", "strategy_refs": strategies},
            "mitigations": {"coverage": "available", "mitigation_refs": mitigations}}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


TAXONOMY = {
    "T1557": block("本技术以中间节点对内容流的可控范围和外观为两条独立轴：选择性内容流介入只改变哪些域和网络路径被劫入，受信终止与原样内容转发则改变客户端所信任的终止者与真实源站的关系。前者需比较受影响和未受影响的会话，后者需比对证书链、上游握手与响应。两者可共现，但 ARP、DHCP、无线和名称解析仅是实现面，四个 ATT&CK 子项不成为 Niji 子项。",
        "Two independent variables organize this technique: Selective Content-Flow Interception changes which domains and network paths enter the intermediary, while Trusted Termination with Content-Preserving Relay changes the relationship between the client's trusted terminator and the true origin. The first requires affected-versus-unaffected session comparison; the second compares certificate chains, upstream handshakes, and responses. They can coexist, but ARP, DHCP, wireless, and name resolution are implementation surfaces rather than imported ATT&CK children."),
    "T1213": {"paragraphs": [
        {"zh": "本技术目前仅建立查询驱动的选择性库内读取一项低置信度子技术，其变量是用库内语义或谓词选择缩小后继内容读取集合，而非仓库产品、数据类型、SQL 方言或是否由脚本执行。防守方需尝试连接查询意图与成功读取，且在无法取得同对象键时把结论保留为条件性推断。",
         "en": "This technique currently establishes one low-confidence child, Query-Led Selective Repository Reading. Its variable is repository-native semantic or predicate selection that narrows subsequent content reads, not product, data type, SQL dialect, or script execution. Defenders must try to join query intent to successful reads and keep the conclusion conditional when no same-object key is available."},
        {"zh": "六个 ATT&CK 子项主要按产品和内容模型划分。既有集成身份归 NJT-0086，状态化增量获取归 NJT-0135；原位浏览、多主体稀释和接口选择没有独立结论级支持。因此六对一的广度差距反映不同分类问题及证据限制，不是要以产品名称补足的空缺。",
         "en": "The six ATT&CK children mostly partition product and content models. Existing integration identity remains with NJT-0086 and stateful incremental acquisition with NJT-0135; in-place viewing, cross-principal dilution, and interface choice lack independent conclusion-level support. The six-to-one breadth gap therefore reflects different classification questions and evidence limits, not a gap to fill with product names."}
    ]},
    "T1114": block("正式子项按邮件副本如何偏离单一邮箱审计视角划分。既存邮件副本二次读取使当前内容读取发生在预先同步或归档的副本上，关键是服务器逐封访问与端点读取的时间错位；到达条件驱动的邮件副本分流让投递事件和规则谓词产生新副本，关键是规则版本与实际消息路由闭环。两者可组合，但不按本地/远程或转发功能名称照搬三个 ATT&CK 子项；一般自动化调度另由 T1119 处理。",
        "The children divide how mail copies depart from one mailbox-audit view. Rereading a Preexisting Mail Replica moves a current content read to a previously synchronized or archived copy, with a time gap between server item access and endpoint read. Arrival-Conditioned Mail Replication uses delivery and a rule predicate to create new copies, requiring a join from rule version to actual message route. They can coexist but do not import ATT&CK local, remote, or forwarding labels; general automation belongs to T1119."),
    "T1185": block("本技术按攻击者与用户活动是否共用同一页面过程划分：同页活动内容中介在用户正在访问的页面内条件式读取请求或页面内容，浏览器上下文代理借用则让远端操作者借受害浏览器状态发起额外请求。前者保留页面脚本、扩展与内容差异，后者保留控制通道和服务端额外访问序列。浏览器品牌、扩展或 DLL、表单字段和目标网站类别都不是稳定子项边界；代理借用仍以工具能力证据作低置信度分类。",
        "The children divide whether adversary action shares the user's current page activity. Co-Viewed Page Content Interposition conditionally reads requests or page content during that activity; Browser-Context Proxy Borrowing drives additional requests from a remote operator through the victim browser's state. The first leaves page script, extension, and content-difference traces, while the second leaves a control channel and extra service-side requests. Browser brand, extension versus DLL, form fields, and target site type are not stable boundaries; proxy borrowing remains a low-confidence classification based chiefly on tool capability."),
    "T1123": block("本技术只按一项已证匿迹变量建立子项：恶意录音被归因给本来就承担音频职责的会议进程，需用模块、设备会话和进程身份恢复真实调用者。T9000 通过应用接口录制通话需要另一套防守分析，但两条路径共同借用正常通信应用身份，接口类型差异不足以再建一项 NJS。短时启停与内存缓冲缺少独立企业端点证据，保留为研究限制。",
        "This technique establishes one supported stealth variable: malicious recording appears under a meeting process with a normal audio role, requiring module, device-session, and process identity to recover the true caller. T9000's call-app interface path needs a different defense analytic, yet both paths borrow normal communication-app identity and interface type alone does not justify another child. Short activation and memory buffering lack independent enterprise-endpoint evidence and remain research limits."),
}

LIMITATIONS = {
    "T1557": {"paragraphs": [
        {"zh": "运营商级 HTTPS 测量证实部分域与路径上的证书替换、上游连接及受信根下的可解密条件，却未进入中间节点证明真实用户正文被保存。案例和检测结果必须分别标识路径介入、内容可读终止和已证实的内容取得，不能把凭据事件或工具能力升级为一般内容证据。该案例也不能直接外推到企业 DNS、DHCP 或无线部署。",
         "en": "Carrier-scale HTTPS measurements establish substitute certificates, upstream connections, and decryptability conditions for selected domains and paths, but did not enter the intermediary to prove retention of real-user bodies. Cases and detections must distinguish path intervention, readable termination, and proven content acquisition rather than promoting credential events or tool capability to general-content evidence. The carrier case does not automatically generalize to enterprise DNS, DHCP, or wireless deployments."},
        {"zh": "两种变量来自同一现场系统，不能据此断言所有协议都独立支持它们。ECH、端到端应用加密、证书轮换和缺少源站协作会削弱证书差分与明文判定；正常企业 TLS 检查、授权代理和网络迁移也是强反例。窗口及关联字段应按实际部署可见性校准。",
         "en": "Both variables are observed in one field system, not proof that every protocol supports them independently. ECH, application-layer end-to-end encryption, certificate rotation, and absent origin cooperation weaken certificate differential and plaintext conclusions. Authorized enterprise TLS inspection, proxies, and network migration are strong comparators. Correlation windows and fields require deployment-specific calibration."}
    ]},
    "T1213": {"paragraphs": [
        {"zh": "公开事件证明信息库敏感词搜索与 SharePoint 下载在同一行动中出现，未证明某次搜索导致同一文件被下载，也未量化选择性读取的告警影响。因此父级内容获取和单项低置信度子技术的结论层级不同；缺少同对象键时，只能把短窗信号下降视为条件性推断，不能把该案例标作子项已证事件。",
         "en": "Public reporting places sensitive-term repository searches and SharePoint downloads in the same activity but does not prove one search caused a download of the same file or quantify an alert effect. Parent-level acquisition and the sole low-confidence child thus carry different conclusion levels. Without a same-object key, reduced short-window signal remains conditional inference and this case must not be labeled a proven child event."},
        {"zh": "信息库审计依赖平台、许可与设置。SharePoint 搜索事件可能由系统账户生成，文件访问存在重复抑制；Confluence Full 审计可能记录搜索词与附件下载却不记录页面正文读取。实现检测时必须先验证租户实际字段、保留期和对象键，避免把一种平台的可见性推广到所有库。",
         "en": "Repository audit depends on platform, license, and settings. SharePoint search events may be produced by system accounts and file access can be deduplicated; Confluence Full audit may record terms and attachment downloads without page-body reads. Detection must first verify tenant fields, retention, and object keys instead of generalizing one platform's visibility to every repository."}
    ]},
    "T1114": block("GETMAIL 的 PST 事件证明离线邮件抽取，却不能证明 OST 缓存也在该入侵中被利用或特定告警被规避。Microsoft 的 BEC 报告证明条件转发规则存在，但没有公开逐封消息的完整匹配与送达链；邮件审计和自动转发报告还受许可、启用及留存条件限制。正常迁移、备份、eDiscovery、委派、合规日记与用户离线阅读均可能形成相似形状，缺少授权、设备与结果目的地证据时应降低置信度。",
        "The GETMAIL PST incident establishes offline extraction, not use of an OST cache in that intrusion or evasion of a particular alert. Microsoft's BEC report establishes conditional forwarding rules but does not publish a complete per-message match-and-delivery chain. Mail audit and auto-forward reports also depend on licensing, enablement, and retention. Authorized migration, backup, eDiscovery, delegation, compliance journaling, and ordinary offline reading can look similar; confidence falls without authorization, device, and destination evidence."),
    "T1185": block("浏览器代理借用的一手资料来自工具作者，说明 IE/WinINet 能力但不是受害者现场取证；QakBot 和 KREMLIN 样本证明控制与可读内容路径，不能把每个可触发功能当作真实用户数据已取得。浏览器版本、扩展 API、目标站点、会话隔离与隐私权限会改变可见字段；Talos 对 Qbot 样本看到的登出重定向也提醒，页面改动不自动意味着内容收集。",
        "The first-party browser-pivot source is a tool author's account of IE/WinINet capability rather than victim incident response. QakBot and KREMLIN samples support control and content-readable paths but do not turn each available feature into observed user-data acquisition. Browser version, extension APIs, target site, session isolation, and privacy permission change telemetry. Talos's observed logout redirects in Qbot samples also show that a page change does not automatically establish collection."),
    "T1123": {"paragraphs": [
        {"zh": "ESET 与 Unit 42 样本分析直接报告录音，平台文档只说明权限、指示或控制能力。Attor 对进程条件和磁盘产物的证据较强，降低用户怀疑是作者的可能性判断；T9000 是旧 Skype 接口的真实实现，不代表现行会议客户端或无提示权限绕过。设备和接口字段需经本地产品试点验证，Windows 用户界面的七日历史不自动构成企业日志流。",
         "en": "ESET and Unit 42 sample analyses directly report recording, whereas platform documentation establishes only permission, indicator, or control capabilities. Attor strongly documents process gating and disk output, while reduced suspicion is the authors' possible explanation. T9000 is a real older Skype implementation, not evidence for current meeting clients or silent permission bypass. Device and interface fields need local product-pilot validation; Windows' seven-day UI history is not automatically an enterprise log stream."},
        {"zh": "合法会议录音、转写、客服质检和无障碍使用是必要反例。缺少模块身份、接口请求者、音频会话与录音结果关联时，只能上报较弱的调查线索，不能从麦克风活动、授权提示或音频扩展名直接断言恶意采集。",
         "en": "Authorized meeting recording, transcription, contact-center quality assurance, and accessibility are necessary comparators. Without joins among module identity, interface requester, audio session, and recording result, only weaker investigation leads are justified; microphone activity, a grant prompt, or an audio extension alone cannot prove malicious capture."}
    ]},
}

PARENTS = [
    ("T1557", "NJT-0142", "content-path-adversary-in-the-middle", {"zh": "通信内容路径中间介入", "en": "Content-Path Adversary-in-the-Middle"}, ["NJS-0142-001", "NJS-0142-002"], ["DET-000155"], ["MIT-000131", "MIT-000144"], ["CLM-000728", "CLM-000729", "CLM-000730", "CLM-000731"], ["CASE-000191"], ["REF-000488", "REF-000556", "REF-000557", "REF-000491", "REF-000515"]),
    ("T1213", "NJT-0143", "stealth-constrained-repository-collection", {"zh": "匿迹约束的信息库内容获取", "en": "Stealth-Constrained Information Repository Collection"}, ["NJS-0143-001"], ["DET-000156"], ["MIT-000145"], ["CLM-000732", "CLM-000733", "CLM-000734", "CLM-000735"], ["CASE-000192"], ["REF-000558", "REF-000559", "REF-000560", "REF-000561", "REF-000562", "REF-000563", "REF-000564", "REF-000565"]),
    ("T1114", "NJT-0144", "stealth-oriented-email-content-collection", {"zh": "匿迹型邮件内容收集", "en": "Stealth-Oriented Email Content Collection"}, ["NJS-0144-001", "NJS-0144-002"], ["DET-000157", "DET-000158"], ["MIT-000146"], ["CLM-000736", "CLM-000737", "CLM-000738", "CLM-000739"], ["CASE-000193", "CASE-000194", "CASE-000183"], ["REF-000566", "REF-000567", "REF-000568", "REF-000569", "REF-000570", "REF-000571", "REF-000572", "REF-000573", "REF-000379", "REF-000509"]),
    ("T1185", "NJT-0145", "browser-session-content-interposition", {"zh": "浏览器会话内内容介入", "en": "Browser-Session Content Interposition"}, ["NJS-0145-001", "NJS-0145-002"], ["DET-000159", "DET-000160"], ["MIT-000147"], ["CLM-000740", "CLM-000741", "CLM-000742"], ["CASE-000195", "CASE-000196"], ["REF-000574", "REF-000575", "REF-000576", "REF-000577", "REF-000578", "REF-000579", "REF-000580", "REF-000581", "REF-000366"]),
    ("T1123", "NJT-0146", "stealth-oriented-audio-capture", {"zh": "匿迹型音频捕获", "en": "Stealth-Oriented Audio Capture"}, ["NJS-0146-001"], ["DET-000161", "DET-000162"], ["MIT-000148", "MIT-000149"], ["CLM-000743", "CLM-000744", "CLM-000745"], ["CASE-000197", "CASE-000198"], ["REF-000582", "REF-000583", "REF-000584", "REF-000585", "REF-000586", "REF-000587", "REF-000588"]),
]

PARENT_DIR = {}
for tid, nid, slug, name, child_ids, strategies, mits, claims, cases, evidence_refs in PARENTS:
    source = H[tid]["proposed_content"]
    mechanisms = mechanism_items(source["stealth_mechanisms"])
    record = {
        "schema_version": "2.0.0", "type": "technique", "id": nid, "name": name,
        "summary": deepcopy(source["summary"]), "aliases": [],
        "classification": {"tactic_refs": ["TA0009"],
                           "origin": {"kind": "attack-adapted", "source_attack_id": tid, "source_attack_version": "19.1"},
                           "decision_ref": f"DEC-TA0009-{tid}"},
        "definition_and_concept": deepcopy(source["definition_and_concept"]),
        "stealth_characteristics": deepcopy(source["stealth_characteristics"]),
        "scope_boundary_definition": deepcopy(source["scope_boundary_definition"]),
        "application_scenarios_and_threat_model": deepcopy(source["application_scenarios_and_threat_model"]),
        "stealth_mechanisms": mechanisms,
        "subtechnique_taxonomy": {"narrative": TAXONOMY[tid], "coverage": "established", "subtechnique_refs": child_ids},
        "defense": defense(strategies, mits),
        "evidence": {"claim_refs": claims, "case_refs": cases, "reference_refs": evidence_refs},
        "research": {"limitations": LIMITATIONS[tid]}, "lifecycle": deepcopy(LIFE),
    }
    for mechanism in mechanisms:
        assert set(mechanism["evidence_refs"]).issubset(record["evidence"]["reference_refs"]), tid
    folder = BASE / f"{nid}-{slug}"
    save(folder / "technique.yaml", record)
    PARENT_DIR[tid] = folder

CHILDREN = [
    ("T1557", "T1557C_CHILD_SELECTIVE", "NJS-0142-001", "selective-content-flow-interception", ["DET-000155"], ["MIT-000131"], ["CLM-000729"], ["CASE-000191"], ["REF-000488", "REF-000556"]),
    ("T1557", "T1557C_CHILD_TRUSTED_TERMINATION", "NJS-0142-002", "trusted-termination-content-preserving-relay", ["DET-000155"], ["MIT-000144"], ["CLM-000730", "CLM-000731"], ["CASE-000191"], ["REF-000488", "REF-000556", "REF-000557"]),
    ("T1213", "T1213_CHILD_QUERY_SELECTIVE", "NJS-0143-001", "query-led-selective-repository-reading", ["DET-000156"], ["MIT-000145"], ["CLM-000734", "CLM-000735"], [], ["REF-000558", "REF-000559", "REF-000560", "REF-000561", "REF-000562", "REF-000563", "REF-000564"]),
    ("T1114", "T1114_CHILD_PREEXISTING_REPLICA_READ", "NJS-0144-001", "preexisting-mail-replica-reread", ["DET-000157"], ["MIT-000146"], ["CLM-000737", "CLM-000739"], ["CASE-000193"], ["REF-000566", "REF-000567", "REF-000568", "REF-000569", "REF-000379"]),
    ("T1114", "T1114_CHILD_ARRIVAL_CONDITIONED_REPLICATION", "NJS-0144-002", "arrival-conditioned-mail-replication", ["DET-000158"], ["MIT-000146"], ["CLM-000738", "CLM-000739"], ["CASE-000194"], ["REF-000566", "REF-000570", "REF-000571", "REF-000572", "REF-000573"]),
    ("T1185", "T1185_CHILD_COVIEW", "NJS-0145-001", "co-viewed-page-content-interposition", ["DET-000159"], ["MIT-000147"], ["CLM-000741"], ["CASE-000195", "CASE-000196"], ["REF-000574", "REF-000576", "REF-000577", "REF-000578", "REF-000579", "REF-000581", "REF-000366"]),
    ("T1185", "T1185_CHILD_RELAY", "NJS-0145-002", "browser-context-proxy-borrowing", ["DET-000160"], ["MIT-000147"], ["CLM-000742"], [], ["REF-000574", "REF-000575", "REF-000366"]),
    ("T1123", "T1123_CHILD_PROCESS", "NJS-0146-001", "teleconference-process-attributed-recording", ["DET-000161"], ["MIT-000148"], ["CLM-000744"], ["CASE-000197"], ["REF-000582", "REF-000583", "REF-000585", "REF-000586", "REF-000587", "REF-000588"]),
]

PARENT_ID = {t: n for t, n, *_ in PARENTS}
for tid, key, cid, slug, strategies, mits, claims, cases, evidence_refs in CHILDREN:
    source = next(x for x in H[tid]["proposed_subtechniques"] if x["temporary_key"] == key)
    content = source.get("proposed_content", source)
    child_name = source["name"]
    summary = source.get("summary") or content["summary"]
    mechanisms = mechanism_items(content["stealth_mechanisms"], "low" if cid == "NJS-0145-002" else None)
    content = deepcopy(content)
    if cid == "NJS-0142-002":
        content["stealth_characteristics"]["paragraphs"][0] = {
            "zh": "受信终止与原样内容转发让中间节点以复制的 Subject 和 SAN、看似未改变的页面维持正常外观，使 URL、内容及服务成功日志单独看都符合预期；真正差异转移到公钥、签发链、根证书来源、TLS 指纹和真实服务所见上游客户端。现场测量观察到名称字段被复制而密钥与扩展不同，且中间节点先向真实服务器握手；测试响应未见头部或正文变化，这不证明所有真实用户交易都未改动。",
            "en": "Trusted Termination with Content-Preserving Relay lets an intermediary copy certificate Subject and SAN and return an apparently unchanged page, so URL, content, and service success logs can each look expected. The real difference moves to public key, issuing chain, trust-root provenance, TLS fingerprint, and the upstream client seen by the origin. Field measurements found copied names with changed keys and extensions and an intermediary handshake to the real server; test headers and bodies showed no change, which does not prove every real-user transaction was unmodified."}
    if cid == "NJS-0144-001":
        content["stealth_characteristics"]["paragraphs"][0] = {
            "zh": "既存邮件副本二次读取要求同时看到服务器缺少本次逐封访问、端点却出现异常副本读取或复制，才形成可解释的观察差。Microsoft 说明同步后的离线访问不会产生新的邮箱审计；Mandiant 的 GETMAIL 事件证明攻击者能从 PST 抽取限定日期邮件。但该事件未证明攻击者专为避开审计而选择副本，合法迁移工具也可能读取整个 PST。",
            "en": "Rereading a Preexisting Mail Replica creates an observation difference only when a current per-message server read is absent while anomalous endpoint replica reads or copies are present. Microsoft explains that offline access after sync creates no new mailbox audit event, and Mandiant's GETMAIL case establishes date-limited extraction from PST. The case does not prove the copy was chosen to evade audit, and an authorized migration tool may also read the whole PST."}
    if cid == "NJS-0144-002":
        content["stealth_characteristics"]["paragraphs"][0] = {
            "zh": "到达条件驱动的邮件副本分流使一次配置在较长时间内产生多个匹配副本，内容取得不再与攻击者登录或主动读信逐次对应。Microsoft 的 BEC 案例证明按财务关键词转发到受控地址并设置删除规则；删除是相邻痕迹抑制行为，不是本子项成立条件。每次成功分流仍可在自动转发报告或邮件流记录留下目的地，效果取决于防守能否联查规则和消息结果。",
            "en": "Arrival-Conditioned Mail Replication lets one configuration create many matching copies over time, so content acquisition no longer maps one-to-one to attacker sign-ins or active reads. Microsoft's BEC case documents finance-keyword forwarding to controlled addresses with deletion rules; deletion is adjacent trace suppression, not a condition of this child. Each successful copy can still leave a destination in forwarding reports or message trace, and the effect depends on joining rule and message outcomes."}
    limits = source.get("limitations") or source.get("research_limitations")
    record = {
        "schema_version": "2.0.0", "type": "evasion-subtechnique", "id": cid,
        "parent_ref": PARENT_ID[tid], "name": child_name, "summary": summary, "aliases": [],
        "lineage": {"attck_subtechnique_inherited": False},
        "definition_and_concept": content["definition_and_concept"],
        "stealth_characteristics": content["stealth_characteristics"],
        "scope_boundary_definition": content["scope_boundary_definition"],
        "application_scenarios_and_threat_model": content["application_scenarios_and_threat_model"],
        "stealth_mechanisms": mechanisms, "defense": defense(strategies, mits),
        "evidence": {"claim_refs": claims, "case_refs": cases, "reference_refs": evidence_refs},
        "research": {"limitations": limits}, "lifecycle": deepcopy(LIFE),
    }
    assert record["stealth_characteristics"]["paragraphs"][0]["zh"].startswith(child_name["zh"]), cid
    assert record["stealth_characteristics"]["paragraphs"][0]["en"].startswith(child_name["en"]), cid
    for mechanism in mechanisms:
        assert set(mechanism["evidence_refs"]).issubset(evidence_refs), cid
    save(PARENT_DIR[tid] / "subtechniques" / f"{cid}-{slug}" / "subtechnique.yaml", record)

print("Serialized 5 parent and 8 Niji-native child packages in draft")
