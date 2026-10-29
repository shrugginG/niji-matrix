"""Serialize reviewed, candidate-specific source records for TA0009 batch two."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
HANDOFFS = {t: yaml.safe_load((RUN / f"{t}-handoff.yaml").read_text(encoding="utf-8"))
            for t in ("T1557", "T1213", "T1114", "T1185", "T1123")}

# ID, candidate, handoff source key, filename, Chinese/English title, type,
# publisher, source-specific Chinese and English use limits. URLs come unchanged
# from the reviewed handoffs. ATT&CK child URLs remain planning-only.
SOURCES = [
    ("REF-000556", "T1557", "T1557C_REF_KAZAKH_PAPER", "kazakhstan-https-interception-measurement", "哈萨克斯坦大规模 HTTPS 中间介入测量", "Investigating Large Scale HTTPS Interception in Kazakhstan", "academic-paper", "ACM IMC", "现场测得 SNI 与路径选择、替代证书和测试响应；未看到真实用户内容留存。", "Measures SNI/path selection, substitute certificates, and test responses; no real-user content retention was observed."),
    ("REF-000557", "T1557", "T1557C_REF_MOZILLA_KAZAKH", "mozilla-qaznet-root-response", "Mozilla 对 Qaznet 根证书的安全响应", "Protecting our Users in Kazakhstan", "vendor-report", "Mozilla Security", "说明自定义受信根使 HTTPS 可被解密及浏览器阻断该根；不证明具体消息被复制。", "Explains decryptability through the custom trusted root and browser blocking of that root; does not prove a particular message was copied."),

    ("REF-000558", "T1213", "T1213_R_ATTACK_PARENT", "mitre-t1213-information-repositories", "从信息库获取数据，技术 T1213", "Data from Information Repositories, Technique T1213", "official-documentation", "MITRE ATT&CK", "固定父行为和 Collection 映射；六个原子项仅作研究广度背景。", "Anchors fixed parent behavior and Collection mapping; six ATT&CK children are research-breadth context only."),
    ("REF-000559", "T1213", "T1213_R_ATTACK_DET", "mitre-repository-collection-detection", "ATT&CK 信息库收集检测策略", "Abuse of Information Repositories for Data Collection", "official-documentation", "MITRE ATT&CK", "提供批量或程序化访问检测对照，不证明低量选择性读取实际漏报。", "Supplies bulk or programmatic access detection contrast, not a measured miss for selective low-volume reads."),
    ("REF-000560", "T1213", "T1213_R_MANDIANT_SEARCH", "gtig-unc6661-repository-search", "GTIG 对 UNC6661 云应用敏感词搜索的调查", "Tracking the Expansion of ShinyHunters-Branded SaaS Data Theft", "incident-report", "Google Threat Intelligence Group", "记录敏感词搜索和同一行动中的 SharePoint 下载；未建立单个搜索词到文件的因果链。", "Records sensitive-term searches and SharePoint downloads in the same activity, without a query-to-file causal chain."),
    ("REF-000561", "T1213", "T1213_R_M365_AUDIT", "microsoft-purview-audit-activities", "Microsoft Purview 审计活动清单", "Audit Log Activities", "official-documentation", "Microsoft Learn", "用于核对搜索、访问和下载事件名；实际可用性取决于启用、许可和工作负载。", "Checks search, access, and download operation names; availability depends on enablement, license, and workload."),
    ("REF-000562", "T1213", "T1213_R_M365_FIELDS", "microsoft-purview-audit-fields", "Microsoft Purview 审计详细属性", "Detailed Properties in the Audit Log", "official-documentation", "Microsoft Learn", "支撑用户、对象和事件关联字段；不保证每个服务均导出同一字段。", "Supports user, object, and event correlation fields, not identical export across services."),
    ("REF-000563", "T1213", "T1213_R_M365_GETSTARTED", "microsoft-purview-audit-prerequisites", "Microsoft Purview 审计启用前提", "Get Started with Auditing Solutions in Microsoft Purview", "official-documentation", "Microsoft Learn", "支撑审计启用与保留前提，不能把缺失事件当作无访问。", "Supports audit enablement and retention prerequisites; absent events do not establish absence of access."),
    ("REF-000564", "T1213", "T1213_R_ATLASSIAN_AUDIT", "atlassian-confluence-audit-events", "Confluence 审计事件及级别", "Audit Log Events in Confluence", "official-documentation", "Atlassian", "支撑特定 Confluence 部署的搜索与附件事件；页面正文读取可能没有同等日志。", "Supports search and attachment events for specified Confluence deployments; page-body reads may lack equivalent logs."),
    ("REF-000565", "T1213", "T1213_R_MS_SAM", "sharepoint-advanced-management", "SharePoint Advanced Management 治理能力", "SharePoint Advanced Management", "official-documentation", "Microsoft Learn", "支撑站点权限、审计与内容治理措施；功能及许可适用范围须逐租户核验。", "Supports site permission, audit, and content governance measures subject to tenant feature and license checks."),

    ("REF-000566", "T1114", "T1114_REF_ATTACK", "mitre-t1114-email-collection", "邮件收集，技术 T1114", "Email Collection, Technique T1114", "official-documentation", "MITRE ATT&CK", "锚定固定版邮件收集父行为与战术映射；本地、远程、转发三个 ATT&CK 子项不导入 NJS。", "Anchors fixed email-collection behavior and tactic mapping; local, remote, and forwarding ATT&CK children are not imported."),
    ("REF-000567", "T1114", "T1114_REF_MS_MAIL_AUDIT", "microsoft-mailitemsaccessed-investigation", "Microsoft MailItemsAccessed 调查说明", "Use MailItemsAccessed to Investigate Compromised Accounts", "official-documentation", "Microsoft Learn", "区分 Sync 与 Bind 的审计语义及可见范围；离线二次读取不产生新的服务器逐封 Bind。", "Distinguishes Sync and Bind audit semantics; offline rereads do not create a new server-side per-item Bind."),
    ("REF-000568", "T1114", "T1114_REF_MS_CACHE", "microsoft-outlook-cached-exchange-mode", "Outlook 缓存 Exchange 模式", "Cached Exchange Mode", "official-documentation", "Microsoft Learn", "说明客户端既存邮件副本及同步行为；不证明恶意访问。", "Documents preexisting client mail replicas and synchronization; does not establish malicious access."),
    ("REF-000569", "T1114", "T1114_REF_MANDIANT_APT1", "mandiant-apt1-getmail-pst", "Mandiant APT1 报告中的 GETMAIL 邮件抽取", "APT1: Exposing One of China's Cyber Espionage Units", "incident-report", "Mandiant", "证明攻击者从 PST 按日期提取邮件和附件；不能升级为 OST 攻击实测或告警下降。", "Establishes date-selected extraction of mail and attachments from PST, not an observed OST attack or reduced alerts."),
    ("REF-000570", "T1114", "T1114_REF_MS_BEC", "microsoft-bec-conditional-mail-rules", "Microsoft 对条件邮件转发 BEC 的调查", "Behind the Scenes of Business Email Compromise", "incident-report", "Microsoft Security", "记录财务关键词条件转发与删除规则；未公开逐封消息闭环日志。", "Records finance-keyword conditional forwarding and deletion rules; no complete per-message chain is published."),
    ("REF-000571", "T1114", "T1114_REF_MS_FORWARD_REPORT", "microsoft-auto-forwarded-mail-report", "Exchange 自动转发消息报告", "Auto-Forwarded Messages Report", "official-documentation", "Microsoft Learn", "支撑自动转发结果的可见字段；报告覆盖取决于服务和配置。", "Supports visibility into auto-forward results; coverage depends on service and configuration."),
    ("REF-000572", "T1114", "T1114_REF_MS_RULE_AUDIT", "microsoft-mailbox-rule-audit", "Microsoft 邮箱规则审计", "Identify Mailbox Rules Using Audit Logs", "official-documentation", "Microsoft Learn", "支撑规则创建、变更及审查字段；规则存在不等于消息已复制。", "Supports rule creation/change and review fields; rule existence does not prove message copying."),
    ("REF-000573", "T1114", "T1114_REF_MS_FORWARD_CONTROL", "microsoft-external-forwarding-policy", "Microsoft 外部邮件自动转发控制", "Control Automatic External Email Forwarding", "official-documentation", "Microsoft Learn", "支撑限制非批准外部自动转发的控制；正常业务例外仍需审计。", "Supports restriction of unapproved external auto-forwarding, with audited business exceptions."),

    ("REF-000574", "T1185", "T1185_REF_ATTACK", "mitre-t1185-browser-session-hijacking", "浏览器会话劫持，技术 T1185", "Browser Session Hijacking, Technique T1185", "official-documentation", "MITRE ATT&CK", "锚定固定版父行为与 Collection 映射；不证明任一子项的现场成效。", "Anchors fixed parent behavior and Collection mapping, not observed outcomes for a particular child."),
    ("REF-000575", "T1185", "T1185_REF_COBALT", "cobalt-browser-pivot-original", "Cobalt Strike 原作者浏览器 Pivot 说明", "Browser Pivoting (Get Past Two-Factor Auth)", "vendor-report", "Cobalt Strike", "说明 IE/WinINet 上下文代理借用会话状态的能力；不是具体受害者现场案例。", "Describes IE/WinINet context proxying with inherited session state; not a specific victim incident."),
    ("REF-000576", "T1185", "T1185_REF_KASPERSKY", "kaspersky-qakbot-browser-hook", "Kaspersky 对 QakBot 浏览器 Hook 的技术分析", "Technical Analysis of the QakBot Banking Trojan", "sample-analysis", "Kaspersky", "观察浏览器网络 API Hook 和目标金融页面脚本注入；未逐次量化取得的业务内容。", "Observes browser network API hooks and targeted financial-page injection; does not quantify content acquired in each use."),
    ("REF-000577", "T1185", "T1185_REF_TALOS", "talos-qbot-webinject-limit", "Cisco Talos 对 Qbot Webinject 样本的分析", "Research Spotlight: The Resurgence of Qbot", "sample-analysis", "Cisco Talos", "特定样本中只见登出重定向，提供内容获取结论的反例边界。", "Observed logout redirection in examined samples, a boundary against assuming content acquisition from every webinject."),
    ("REF-000578", "T1185", "T1185_REF_ELASTIC", "elastic-kremlin-browser-extension", "Elastic 对 KREMLIN 恶意浏览器扩展的分析", "The Extension You Never Installed: KREMLIN", "sample-analysis", "Elastic Security Labs", "样本代码含页面源码和请求内容上传，实验靶页验证功能；不证明每位真实受害者的取数结果。", "Sample code uploads page source and request content and was tested on a lab page; real-victim outcomes are not established."),
    ("REF-000579", "T1185", "T1185_REF_CHROME_DEBUGGER", "chrome-extension-debugger-api", "Chrome 扩展 debugger API", "Chrome Extensions Debugger API", "official-documentation", "Google Chrome Developers", "支撑浏览器调试接口能力与权限要求，不能证明恶意扩展的现场使用。", "Documents browser debugger capabilities and permission requirements, not malicious field use."),
    ("REF-000580", "T1185", "T1185_REF_MS_POLICY", "microsoft-edge-extension-policy", "Microsoft Edge 扩展管理策略参考", "Microsoft Edge Extension Management Reference", "official-documentation", "Microsoft Learn", "支撑允许列表、强制安装和权限治理措施；需按企业部署核对。", "Supports extension allowlisting, force-install, and permission governance subject to enterprise deployment."),
    ("REF-000581", "T1185", "T1185_REF_MS_EXTINV", "microsoft-browser-extension-inventory", "Microsoft Defender 浏览器扩展清单", "Browser Extensions in Defender Vulnerability Management", "official-documentation", "Microsoft Learn", "支撑扩展身份、权限和安装清单；不能单靠清单证明页面内容被读取。", "Supports extension identity, permission, and installation inventory; inventory alone does not prove page reading."),

    ("REF-000582", "T1123", "T1123_REF_ATTACK", "mitre-t1123-audio-capture", "音频捕获，技术 T1123", "Audio Capture, Technique T1123", "official-documentation", "MITRE ATT&CK", "锚定固定版父行为、Collection 映射和零 ATT&CK 子项；不独立证明匿迹变量。", "Anchors fixed parent behavior, Collection mapping, and zero ATT&CK children; not independent evidence of a stealth variable."),
    ("REF-000583", "T1123", "T1123_REF_ESET_PDF", "eset-attor-audio-recorder", "ESET Attor 音频录制插件白皮书", "AT Commands, Tor-Based Communications: Meet Attor", "sample-analysis", "ESET Research", "第 20 页逆向出会议进程条件、麦克风录音和加密产物；降低怀疑是作者的可能性判断。", "Page 20 reverse engineers meeting-process gating, microphone recording, and encrypted output; reduced suspicion is an author hypothesis."),
    ("REF-000584", "T1123", "T1123_REF_T9000", "unit42-t9000-skype-audio", "Unit 42 对 T9000 Skype 通话录音的分析", "T9000: Advanced Modular Backdoor Uses Complex Anti-Analysis Techniques", "sample-analysis", "Palo Alto Networks Unit 42", "支持旧 Skype 接口附着、用户授权及通话录音；不支持现代客户端普遍性或无提示绕过。", "Supports older Skype API attachment, user approval, and call recording; not generality to modern clients or promptless bypass."),
    ("REF-000585", "T1123", "T1123_REF_MITRE_DET", "mitre-audio-capture-detection", "ATT&CK 音频捕获检测策略", "Behavioral Detection Strategy for Audio Capture", "official-documentation", "MITRE ATT&CK", "提供设备 API 与录音产物的分析线索；具体字段仍需平台文档核验。", "Provides device-API and audio-output analytic clues; exact fields still require platform documentation."),
    ("REF-000586", "T1123", "T1123_REF_MS_PRIVACY", "windows-microphone-privacy-observation", "Windows 麦克风隐私观察", "Windows Privacy Controls", "official-documentation", "Microsoft Learn", "说明应用麦克风访问的用户可见历史与指示，非系统化进程级审计保证。", "Describes user-visible microphone access history and indicators, not guaranteed systematic process-level audit."),
    ("REF-000587", "T1123", "T1123_REF_MS_CSP", "windows-app-privacy-policy", "Windows 应用麦克风隐私策略", "Privacy Policy CSP", "official-documentation", "Microsoft Learn", "支撑受管应用麦克风权限策略；不能由策略状态推断音频已录制。", "Supports managed app microphone permission policy; policy state does not establish recorded audio."),
    ("REF-000588", "T1123", "T1123_REF_APPLE_MIC", "apple-microphone-access-indicator", "Apple 麦克风访问与录音指示", "Control Access to the Microphone on Mac", "official-documentation", "Apple Support", "说明应用授权与录音指示；不能外推为所有端点都有可查询历史日志。", "Describes app authorization and recording indicator; not all endpoints expose queryable history logs."),
]

def lookup_source(tactic, key):
    for item in HANDOFFS[tactic]["library_candidates"]["references"]:
        if item.get("key") == key or item.get("temporary_key") == key:
            return item
    raise KeyError((tactic, key))

for rid, tactic, key, slug, title_zh, title_en, source_type, publisher, note_zh, note_en in SOURCES:
    item = lookup_source(tactic, key)
    path = ROOT / "references" / f"{rid}-{slug}.yaml"
    record = {
        "schema_version": "1.0.0", "type": "reference", "id": rid,
        "title_zh": title_zh, "title_en": title_en, "source_type": source_type,
        "authors": [publisher], "publisher": publisher, "published": None,
        "url": item["url"], "accessed": "2026-09-22",
        "locator": item.get("locator") or note_en, "archive_url": None,
        "credibility": "high", "notes_zh": note_zh, "notes_en": note_en,
    }
    path.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

print(f"Serialized {len(SOURCES)} reviewed source records")
