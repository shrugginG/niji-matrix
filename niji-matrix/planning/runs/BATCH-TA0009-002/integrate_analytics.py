"""Serialize candidate-specific Collection Strategies and implementable Analytics."""

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
H = {t: yaml.safe_load((RUN / f"{t}-handoff.yaml").read_text(encoding="utf-8"))
     for t in ("T1557", "T1213", "T1114", "T1185", "T1123")}
LIFE = {"status": "draft", "version": "1.0.0", "created": "2026-09-22", "modified": "2026-09-22",
        "contributors": ["Niji Matrix Research"], "reviewers": []}
REF = {
    "REF-000366": "REF-000366", "REF-000379": "REF-000379", "REF-000488": "REF-000488",
    "T1557C_REF_KAZAKH_PAPER": "REF-000556", "T1557C_REF_MOZILLA_KAZAKH": "REF-000557",
    "T1213_R_ATTACK_PARENT": "REF-000558", "T1213_R_ATTACK_DET": "REF-000559",
    "T1213_R_MANDIANT_SEARCH": "REF-000560", "T1213_R_M365_AUDIT": "REF-000561",
    "T1213_R_M365_FIELDS": "REF-000562", "T1213_R_M365_GETSTARTED": "REF-000563",
    "T1213_R_ATLASSIAN_AUDIT": "REF-000564", "T1213_R_MS_SAM": "REF-000565",
    "T1114_REF_ATTACK": "REF-000566", "T1114_REF_MS_MAIL_AUDIT": "REF-000567",
    "T1114_REF_MS_CACHE": "REF-000568", "T1114_REF_MANDIANT_APT1": "REF-000569",
    "T1114_REF_MS_BEC": "REF-000570", "T1114_REF_MS_FORWARD_REPORT": "REF-000571",
    "T1114_REF_MS_RULE_AUDIT": "REF-000572", "T1114_REF_MS_FORWARD_CONTROL": "REF-000573",
    "T1114_REF_MS_4663": "REF-000379",
    "T1185_REF_ATTACK": "REF-000574", "T1185_REF_COBALT": "REF-000575",
    "T1185_REF_KASPERSKY": "REF-000576", "T1185_REF_TALOS": "REF-000577",
    "T1185_REF_ELASTIC": "REF-000578", "T1185_REF_CHROME_DEBUGGER": "REF-000579",
    "T1185_REF_MS_POLICY": "REF-000580", "T1185_REF_MS_EXTINV": "REF-000581",
    "T1123_REF_ATTACK": "REF-000582", "T1123_REF_ESET_PDF": "REF-000583",
    "T1123_REF_T9000": "REF-000584", "T1123_REF_MITRE_DET": "REF-000585",
    "T1123_REF_MS_PRIVACY": "REF-000586", "T1123_REF_MS_CSP": "REF-000587",
    "T1123_REF_APPLE_MIC": "REF-000588",
}


def pair(zh, en): return {"zh": zh, "en": en}
def para(zh, en): return {"paragraphs": [pair(zh, en)]}
def refs(keys): return list(dict.fromkeys(REF[k] for k in keys))


def save(folder, filename, item):
    p = ROOT / folder / filename
    p.write_text(yaml.safe_dump(item, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def research_analytic(tactic, key):
    for x in H[tactic]["defense_candidates"]["detection_analytics"]:
        if x.get("key") == key or x.get("temporary_key") == key:
            return x
    raise KeyError((tactic, key))


SOURCE_NAME = {
    "endpoint-tls-probe": pair("端点 TLS 探测", "Endpoint TLS probe"),
    "network-path-map": pair("网络出口与路由路径映射", "Network egress and path map"),
    "approved-proxy-certificate-inventory": pair("批准代理与证书清单", "Approved proxy and certificate inventory"),
    "endpoint-certificate-observation": pair("端点实际证书观察", "Endpoint accepted-certificate observation"),
    "endpoint-trust-store-inventory": pair("端点信任根清单", "Endpoint trust-root inventory"),
    "independent-origin-probe": pair("独立出口源站证书探测", "Independent-origin certificate probe"),
    "origin-tls-access": pair("源站 TLS 访问记录", "Origin TLS access record"),
    "m365-sharepoint-search-audit": pair("Microsoft 365 SharePoint 搜索审计", "Microsoft 365 SharePoint search audit"),
    "m365-sharepoint-file-audit": pair("Microsoft 365 SharePoint 文件审计", "Microsoft 365 SharePoint file audit"),
    "object-sensitivity-and-duty": pair("对象敏感度与职责映射", "Object sensitivity and duty map"),
    "confluence-datacenter-search-audit": pair("Confluence Data Center 搜索审计", "Confluence Data Center search audit"),
    "confluence-datacenter-attachment-audit": pair("Confluence Data Center 附件审计", "Confluence Data Center attachment audit"),
    "repository-authorization-context": pair("信息库授权与业务上下文", "Repository authorization and business context"),
    "endpoint-file-access": pair("端点邮件副本文件读取", "Endpoint mail-replica file access"),
    "endpoint-process-lineage": pair("端点进程与复制谱系", "Endpoint process and copy lineage"),
    "exchange-mailbox-audit": pair("Exchange 邮箱访问审计", "Exchange mailbox access audit"),
    "exchange-unified-audit": pair("Exchange 规则变更审计", "Exchange rule-change audit"),
    "exchange-mail-flow": pair("Exchange 自动转发与邮件流", "Exchange auto-forward and mail flow"),
    "governance-baseline": pair("批准转发与迁移清单", "Approved forwarding and migration register"),
    "browser-extension-inventory": pair("浏览器扩展与权限清单", "Browser extension and permission inventory"),
    "endpoint-process-and-network": pair("浏览器进程及外联事件", "Browser process and egress events"),
    "application-request-log": pair("应用资源请求日志", "Application resource request log"),
    "sysmon-process-access": pair("Sysmon 浏览器进程访问", "Sysmon browser process access"),
    "endpoint-network-connection": pair("端点网络连接", "Endpoint network connection"),
    "endpoint-audio-session": pair("端点音频设备会话", "Endpoint audio-device session"),
    "module-and-process-lineage": pair("模块加载与进程谱系", "Module load and process lineage"),
    "file-creation": pair("录音产物文件创建", "Recorded-audio file creation"),
    "call-app-interface-audit": pair("通话应用第三方接口审计", "Call-app third-party interface audit"),
    "call-app-session": pair("通话应用会话事件", "Call-app session event"),
    "endpoint-file-creation": pair("端点音频文件创建", "Endpoint audio-file creation"),
}


def requirements(items):
    out = []
    for x in items:
        source_type = x["source_type"].replace("_", "-")
        assert source_type in SOURCE_NAME, source_type
        normalized = [re.sub(r"(?<!^)(?=[A-Z])", "_", field).lower() for field in x["required_fields"]]
        out.append({"source_type": source_type, "name": SOURCE_NAME[source_type],
                    "channel": x.get("channel"), "required_fields": normalized})
    return out


# ID, tactic, handoff analytic key, filename, bilingual name and summary,
# platform, correlation window, fallback correlation dimensions, concrete
# bilingual observables, T1213-specific false-positive/blind-spot/tuning text.
ANALYTICS = [
    ("NJA-000164", "T1557", "T1557C_NJA_SELECTED_FLOW", "sni-path-certificate-differential", pair("域与路径交集证书差分", "Domain-and-Path Certificate Differential"), pair("识别同一域仅在特定出口路径收到未经批准的替代证书。", "Identify a domain receiving an unapproved substitute certificate only on selected egress paths."), [], pair("在同一十分钟探测周期比较，并保留二十四小时路径及批准例外历史。", "Compare within one ten-minute probe cycle and retain twenty-four hours of path and approved-exception history."), None, [pair("同域同时间的证书公钥仅在特定出口改变", "The same domain has a changed certificate public key only on selected egress"), pair("受影响与未受影响端点共享相同 SNI 但不同路径", "Affected and unaffected endpoints share SNI but take different paths")], None),
    ("NJA-000165", "T1557", "T1557C_NJA_SPLIT_TLS", "trusted-root-origin-handshake-join", pair("客户端信任链与源站上游握手关联", "Client Trust Chain and Origin Upstream-Handshake Join"), pair("将客户端接受的替代链与独立源站证书及中间节点上游握手连接。", "Join the client's accepted substitute chain to independent-origin certificates and an intermediary's upstream handshake."), [], pair("以请求前后二分钟连接两段 TLS，并复核前后二十四小时的根证书变更。", "Join both TLS legs within two minutes of a request and review trust-root changes across the surrounding twenty-four hours."), None, [pair("客户端接受的受信根与独立源站链不一致", "The client accepts a trusted root divergent from the independent origin chain"), pair("源站看到与客户端请求时间闭合的另一上游握手", "The origin sees another upstream handshake aligned with the client request")], None),
    ("NJA-000166", "T1213", "T1213_NJA_SHAREPOINT_SEARCH_READ", "sharepoint-query-sensitive-read", pair("SharePoint 查询与敏感文件读取关联", "SharePoint Query and Sensitive-File Read Correlation"), pair("在已验证审计覆盖的租户中连接查询上下文与高敏对象访问，保留无法同对象关联的状态。", "In a tenant with verified audit coverage, join query context to sensitive object access and preserve an unresolved state when object linkage is absent."), ["Office Suite"], pair("查询到访问初始取六十分钟，另保留三十天身份与站点基线；窗口按业务流程调整。", "Start with sixty minutes from query to access and retain a thirty-day principal-and-site baseline, adjusting to the workflow."), ["user_id", "site_id", "object_id", "query_time", "access_time"], [pair("敏感词查询后同身份访问少量高敏文件", "A principal accesses a small high-sensitivity set after a sensitive-term query"), pair("搜索对象与访问对象无法对应时保留未解析链", "An unresolved chain is retained when search and accessed object cannot be joined")], ["合法 eDiscovery、事件响应、分类服务与员工研究也会产生相同的搜索和读取。", "Legal eDiscovery, incident response, classification services, and employee research can create the same search-read shape.", "搜索词可能不可得，重复文件访问可能被抑制，许可和保留期还会影响可见性。", "Terms may be unavailable, repeat file access can be suppressed, and license or retention changes visibility.", "按职责、站点、对象敏感度和批准案件建立基线，不用全局小文件数阈值；只有同对象键闭合时升级确认。", "Baseline duty, site, object sensitivity, and approved case rather than a global small-count threshold; confirm only with a same-object join."]),
    ("NJA-000167", "T1213", "T1213_NJA_CONFLUENCE_SEARCH_ATTACHMENT", "confluence-search-attachment-lineage", pair("Confluence 搜索与附件下载关联", "Confluence Search and Attachment Download Correlation"), pair("在 Full 审计下连接搜索词、附件 ID 与授权角色，并把页面正文读取留作盲区。", "Under Full audit, join terms, attachment ID, and authorized role while retaining page-body reads as a blind spot."), ["Confluence Data Center"], pair("查询到附件下载初始取六十分钟，另保留三十天用户与空间基线。", "Start with sixty minutes from query to attachment download and retain a thirty-day actor-and-space baseline."), ["actor", "space_id", "attachment_id", "query_time", "download_time"], [pair("同一角色搜索后取得高敏空间附件", "The same actor retrieves a high-sensitivity space attachment after searching"), pair("未授权角色的少量高价值下载偏离职责", "A few high-value downloads by an unauthorized role depart from duty")], ["文档维护、支持、法务审查与获批机密调查也会搜索并下载附件。", "Documentation maintainers, support, legal review, and approved sensitive investigations also search and download attachments.", "Base/Advanced 审计不一定提供这组事件，页面浏览可能没有同等记录。", "Base or Advanced audit may not provide the required pair and page views may lack equivalent records.", "先核验 Full 审计与附件键，再按空间和职责建立例外；只凭搜索词不能判定内容已取得。", "Verify Full audit and attachment keys first, then baseline by space and duty; terms alone do not establish acquired content."]),
    ("NJA-000168", "T1114", "T1114_NJA_REPLICA_READ", "mail-replica-endpoint-reread", pair("既存邮件副本端点读取与历史同步关联", "Preexisting Mail Replica Endpoint Read and Prior Sync Correlation"), pair("关联端点非预期副本读取、历史同步范围与本次服务器逐封审计缺口。", "Join unexpected endpoint replica reads, prior sync scope, and the current gap in server per-item audit."), ["Windows", "Office Suite"], pair("围绕端点读取取二十四小时，同时回溯副本的先前同步范围。", "Use twenty-four hours around the endpoint read and look back to the replica's earlier sync scope."), None, [pair("未批准进程在本次服务器逐封 Bind 缺席时读取既存 PST 或缓存副本", "An unapproved process reads an existing PST or cache while no current server per-item Bind appears"), pair("同进程复制或提取邮件内容并形成后继产物", "The same process copies or extracts mail content into a successor artifact")], None),
    ("NJA-000169", "T1114", "T1114_NJA_RULE_TO_MESSAGE", "mail-rule-matched-delivery-copy", pair("邮件规则版本与匹配副本投递关联", "Mail Rule Version and Matched-Copy Delivery Correlation"), pair("证明条件规则对实际到达消息生成了非批准副本，而非只发现规则存在。", "Prove that a conditional rule generated unapproved copies of arriving messages rather than only finding the rule."), ["Office Suite"], pair("覆盖规则有效期并以三十天为初始回看期，保留每次消息投递的顺序。", "Cover the rule's effective interval with an initial thirty-day lookback and preserve each message's delivery order."), None, [pair("新增规则谓词匹配到达邮件并出现异常接收目的地", "A new rule predicate matches arriving mail and an anomalous destination appears"), pair("规则配置人、消息 ID 和副本结果构成闭合链", "Rule writer, message ID, and copy outcome form a closed chain")], None),
    ("NJA-000170", "T1185", "T1185_NJA_COVIEW", "browser-control-to-page-read", pair("浏览器控制点到同页内容读取关联", "Browser Control Point to Co-Viewed Page Read Correlation"), pair("将扩展或注入控制变化与用户页面活动及额外内容读取连接。", "Join extension or injection control changes to the user's page activity and additional content reads."), ["Windows"], pair("围绕浏览器控制变化与敏感页面访问取三十分钟窗口。", "Use a thirty-minute window around browser-control change and sensitive-page access."), None, [pair("未批准扩展取得敏感域权限后发生页面源码或请求读取", "An unapproved extension reads page source or requests after gaining sensitive-domain permission"), pair("浏览器外联或应用请求与用户同页操作时间重叠", "Browser egress or app requests overlap the user's page activity")], None),
    ("NJA-000171", "T1185", "T1185_NJA_RELAY", "browser-relay-extra-resource-reads", pair("浏览器代理控制与额外资源读取关联", "Browser Relay Control and Extra Resource Read Correlation"), pair("连接浏览器进程控制、代理链路与用户未发起的服务端额外请求。", "Join browser-process control, proxy link, and extra service-side requests the user did not initiate."), ["Windows"], pair("以代理链路出现前后二十分钟为初始关联窗口。", "Use an initial twenty-minute window around the appearance of the relay link."), None, [pair("浏览器进程被写入后产生独立代理连接", "A browser process starts an independent relay connection after write access"), pair("同一会话从该设备访问用户未打开的额外资源", "The same session reads additional resources the user did not open")], None),
    ("NJA-000172", "T1123", "T1123_NJA_PROCESS", "meeting-process-module-audio-session", pair("会议进程模块与麦克风会话关联", "Meeting-Process Module and Microphone-Session Correlation"), pair("将会议进程内新模块、麦克风会话和音频产物闭合，识别借用正常进程身份的录音。", "Close the chain from a new meeting-process module to microphone session and audio artifact, exposing recording under a normal process identity."), ["Windows"], pair("从音频激活前十五分钟到结束后三十分钟关联。", "Correlate from fifteen minutes before audio activation through thirty minutes after it ends."), None, [pair("会议进程出现未批准模块并启动麦克风会话", "A meeting process gains an unapproved module and starts a microphone session"), pair("该会话后同进程形成非批准音频产物", "The same process produces an unapproved audio artifact after the session")], None),
    ("NJA-000173", "T1123", "T1123_NJA_CALL_API", "call-interface-grant-audio-artifact", pair("通话接口授权与录音产物关联", "Call-Interface Grant and Audio Artifact Correlation"), pair("在实际导出接口审计的应用中连接第三方授权、通话时段及录音结果。", "For apps that actually export interface audit, join third-party grants, call intervals, and recording outcomes."), ["Windows"], pair("从通话开始前十五分钟到结束后三十分钟关联。", "Correlate from fifteen minutes before call start through thirty minutes after call end."), None, [pair("未批准第三方组件在通话附近取得媒体接口授权", "An unapproved third-party component gains media-interface access near a call"), pair("同会话随后出现音频文件或导出任务", "An audio file or export task follows in the same call session")], None),
]

STRATEGIES = [
    ("DET-000155", "T1557", "content-path-trust-differential", pair("内容路径与受信终止差分", "Content-Path and Trusted-Termination Differential"), pair("比较端点所见证书、路径与独立源站，分级识别内容流介入及可读终止。", "Compare endpoint certificates and paths to an independent origin, grading content-flow intervention and readable termination."), para("NJA-000164 在受控探测中比较同域不同出口是否出现选择性证书替换；NJA-000165 再把客户端信任根与源站上游握手连接。策略明确分开路径异常、可解密终止和真实内容取得，不把证书差异单独当作已窃内容；企业检查代理须先按批准清单排除。", "NJA-000164 compares a domain across egress paths for selective certificate replacement under controlled probes. NJA-000165 joins the client's trust root to an origin upstream handshake. The strategy separates path anomaly, decryptable termination, and actual content acquisition; a certificate difference alone is not stolen content, and approved enterprise inspection is excluded first."), ["NJT-0142", "NJS-0142-001", "NJS-0142-002"], ["NJA-000164", "NJA-000165"]),
    ("DET-000156", "T1213", "repository-query-to-sensitive-read", pair("库内查询—敏感内容读取谱系", "Repository Query-to-Sensitive-Read Lineage"), pair("把库内搜索或谓词与实际敏感对象读取连接，并保留无法闭合的查询为调查线索。", "Join repository searches or predicates to actual sensitive-object reads, leaving unclosed queries as leads."), para("NJA-000166 在 Microsoft 365 中检查查询与文件访问的身份、站点、对象和时间关系；NJA-000167 在 Confluence Full 审计中检查搜索词与附件下载。两项分析只在审计字段确实可用且成功读取有对象键时给出闭合链。合法 eDiscovery、分类和内容维护可出现同型行为，短窗小量访问只提高复核优先级。", "NJA-000166 tests identity, site, object, and timing links between query and file access in Microsoft 365. NJA-000167 tests terms and attachment downloads in Confluence Full audit. A closed chain requires actual audit fields and an object key for successful reads. Authorized eDiscovery, classification, and content maintenance can look similar; a small short-window count only changes review priority."), ["NJT-0143", "NJS-0143-001"], ["NJA-000166", "NJA-000167"]),
    ("DET-000157", "T1114", "mail-sync-to-endpoint-replica-read", pair("邮件同步范围到端点副本读取谱系", "Mail Sync Scope to Endpoint Replica Read Lineage"), pair("用端点副本读取与既有同步范围还原缺少本次服务器逐封访问的邮件取得。", "Use endpoint replica reads and prior sync scope to reconstruct mail acquisition without a current server per-item event."), para("NJA-000168 需要已启用的文件读取审计、稳定进程谱系和 MailItemsAccessed 同步上下文。它比较本次端点非预期读取与较早同步范围，并区分正常迁移或 eDiscovery；没有端点读取结果时，服务器缺少 Bind 只能是观察缺口，不能判定恶意副本阅读。", "NJA-000168 requires enabled file-read audit, stable process lineage, and MailItemsAccessed sync context. It compares an unexpected current endpoint read with earlier sync scope and excludes migration or eDiscovery. Without an endpoint read outcome, an absent server Bind is an observation gap, not a malicious replica-read verdict."), ["NJT-0144", "NJS-0144-001"], ["NJA-000168"]),
    ("DET-000158", "T1114", "mail-rule-to-matched-copy", pair("邮件条件配置到投递副本谱系", "Mail Predicate Configuration to Delivery Copy Lineage"), pair("证明条件规则对到达邮件产生了非批准副本，并定位实际接收目的地。", "Prove that a conditional rule made unapproved copies of arriving mail and identify the recipient."), para("NJA-000169 将规则版本、匹配谓词、消息 ID、转发报告或邮件流结果逐一关联。规则创建、规则启用、单封消息命中和目的地实际收取分别保留为不同结论层级；合规日记、迁移和受管转发应按具体规则与期限排除。", "NJA-000169 joins rule version, match predicate, message ID, and forwarding report or message-trace outcome. Rule creation, activation, a matching message, and actual destination receipt remain distinct conclusion levels. Compliance journaling, migration, and managed forwarding are excluded by specific rule and time-bounded authorization."), ["NJT-0144", "NJS-0144-002"], ["NJA-000169"]),
    ("DET-000159", "T1185", "browser-control-co-viewed-content", pair("浏览器控制点与同页内容读取关联", "Browser Control to Co-Viewed Content Read Correlation"), pair("将浏览器扩展或 Hook 控制变化接到用户当前页面的额外内容读取。", "Join extension or hook changes to extra content reads on the user's current page."), para("NJA-000170 连接扩展权限、浏览器进程变化、应用资源请求和额外外联。策略的直接结果是控制点与内容可读链，纯 Cookie 取得、输入按键截取或页面外观改变没有实际读取证据时留给相邻对象。批准扩展、无障碍插件与浏览器调试必须按身份和业务目的校准。", "NJA-000170 joins extension permission, browser-process changes, app resource requests, and extra egress. The direct result is a control point linked to content access. Cookie theft, keystroke capture, or page appearance change without a read belongs to adjacent objects. Approved extensions, accessibility plug-ins, and browser debugging require identity and business-purpose calibration."), ["NJT-0145", "NJS-0145-001"], ["NJA-000170"]),
    ("DET-000160", "T1185", "browser-relay-extra-resource-lineage", pair("浏览器代理控制与额外站点读取关联", "Browser Relay Control to Extra Site Read Lineage"), pair("把浏览器进程代理植入与用户未发起的同会话资源读取连接。", "Join browser-process proxy implantation to same-session resource reads not initiated by the user."), para("NJA-000171 要求浏览器写入或注入、独立控制链路及站点额外请求三者闭合；缺少应用资源结果时只能报代理暴露，不能报内容取得。旧 IE/WinINet 的作者演示提供技术能力，实际现代浏览器部署必须另做验证。合法远程支持和自动化测试应逐任务授权。", "NJA-000171 requires browser write or injection, a distinct control link, and extra site requests. Without a resource result it reports relay exposure, not acquired content. The author's old IE/WinINet demonstration establishes capability; modern browser deployments need separate verification. Legitimate remote support and automation tests require task-specific authorization."), ["NJT-0145", "NJS-0145-002"], ["NJA-000171"]),
    ("DET-000161", "T1123", "meeting-process-module-microphone-lineage", pair("会议进程麦克风会话与模块谱系", "Meeting-Process Microphone Session and Module Lineage"), pair("将正常会议进程中的异常模块、音频设备会话和录音产物连接。", "Join anomalous modules, audio-device sessions, and recording output inside an ordinary meeting process."), para("NJA-000172 只在端点产品实际提供音频会话与模块事件时执行进程归因差分，随后要求同进程录音产物或对应输出。签名会议客户端并不免检；若只有麦克风指示、没有模块与结果，只能报待查。合法会议录音、转写与客服质检按具体插件和时段区分。", "NJA-000172 performs process-attribution differential only when endpoint products actually export audio-session and module events, then requires same-process audio output. A signed meeting client is not exempt. With only a microphone indicator and no module or result, report an investigation lead. Authorized meetings, transcription, and contact-center recording are distinguished by specific plug-in and interval."), ["NJT-0146", "NJS-0146-001"], ["NJA-000172"]),
    ("DET-000162", "T1123", "call-interface-grant-recording-outcome", pair("通话接口授权与音频产物关联", "Call-Interface Grant to Audio-Outcome Correlation"), pair("在实际导出接口审计的应用中，把第三方授权、通话和非批准录音产物连接。", "Where an app exports interface audit, join third-party grant, call, and unapproved audio output."), para("NJA-000173 为 T1123 父级处理 T9000 所示接口路径。它只在产品提供 requester、grant 和会话事件时关联后继音频产物；旧 Skype API 名称不迁移为现代通用字段。接口不同不构成第二个 Niji 子项，授权提示或正常音频文件也不能单独证明恶意录制。", "NJA-000173 covers the T9000-style interface path at the T1123 parent. It joins later audio output only where a product supplies requester, grant, and call-session events; old Skype API names are not universal modern fields. Interface type does not create a second Niji child, and a grant prompt or ordinary audio file alone does not prove malicious recording."), ["NJT-0146"], ["NJA-000173"]),
]


def get_obs(source, explicit):
    return explicit


for aid, tactic, key, slug, name, summary, platforms, window, fallback_dimensions, observables, t1213_local in ANALYTICS:
    src = research_analytic(tactic, key)
    corr = src.get("correlation", {})
    dimensions = corr.get("dimensions") or fallback_dimensions
    if t1213_local:
        fp = [pair(t1213_local[0], t1213_local[1])]
        blind = [pair(t1213_local[2], t1213_local[3])]
        tuning = para(t1213_local[4], t1213_local[5])
    else:
        fp_source = src["false_positives"]
        blind_source = src["blind_spots"]
        fp = fp_source if isinstance(fp_source, list) else [fp_source]
        blind = blind_source if isinstance(blind_source, list) else [blind_source]
        guide = src.get("tuning") or src.get("tuning_guidance")
        tuning = guide if "paragraphs" in guide else para(guide["zh"], guide["en"])
    item = {
        "schema_version": "2.0.0", "type": "detection-analytic", "id": aid,
        "strategy_ref": {"NJA-000164":"DET-000155", "NJA-000165":"DET-000155",
                         "NJA-000166":"DET-000156", "NJA-000167":"DET-000156",
                         "NJA-000168":"DET-000157", "NJA-000169":"DET-000158",
                         "NJA-000170":"DET-000159", "NJA-000171":"DET-000160",
                         "NJA-000172":"DET-000161", "NJA-000173":"DET-000162"}[aid],
        "name": name, "summary": summary, "domains": ["enterprise"], "platforms": platforms,
        "logic": para(src["logic"]["zh"], src["logic"]["en"]),
        "data_requirements": requirements(src["data_requirements"]),
        "observables": get_obs(src, observables),
        "correlation": {"window": window, "dimensions": dimensions},
        "false_positives": fp, "blind_spots": blind,
        "tuning_guidance": tuning, "evidence_refs": refs(src["evidence_keys"]),
        "lifecycle": LIFE.copy(),
    }
    save("analytics", f"{aid}-{slug}.yaml", item)

for sid, tactic, slug, name, summary, description, subjects, analytic_ids in STRATEGIES:
    all_refs = []
    for aid in analytic_ids:
        path = next((ROOT / "analytics").glob(f"{aid}-*.yaml"))
        all_refs.extend(yaml.safe_load(path.read_text(encoding="utf-8"))["evidence_refs"])
    all_refs = list(dict.fromkeys(all_refs + {
        "T1557":["REF-000488"], "T1213":["REF-000558", "REF-000559"],
        "T1114":["REF-000566"], "T1185":["REF-000574"], "T1123":["REF-000582"]
    }[tactic]))
    save("detections", f"{sid}-{slug}.yaml", {
        "schema_version": "2.0.0", "type": "detection-strategy", "id": sid,
        "name": name, "summary": summary, "description": description,
        "detects_refs": subjects, "domains": ["enterprise"], "analytic_refs": analytic_ids,
        "evidence_refs": all_refs, "lifecycle": LIFE.copy(),
    })

print("Serialized 10 candidate-specific Analytics and 8 bidirectional Strategies in draft")
