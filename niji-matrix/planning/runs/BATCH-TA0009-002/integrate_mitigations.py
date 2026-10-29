"""Serialize target-specific Collection mitigations and extend one shared control."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
H = {t: yaml.safe_load((RUN / f"{t}-handoff.yaml").read_text(encoding="utf-8"))
     for t in ("T1557", "T1213", "T1114", "T1185", "T1123")}
LIFE = {"status": "draft", "version": "1.0.0", "created": "2026-09-22", "modified": "2026-09-22",
        "contributors": ["Niji Matrix Research"], "reviewers": []}


def pair(zh, en): return {"zh": zh, "en": en}
def para(zh, en): return {"paragraphs": [pair(zh, en)]}


def save(path, item):
    path.write_text(yaml.safe_dump(item, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def mitigation(mid, slug, name, summary, description, measures, applications, refs):
    save(ROOT / "mitigations" / f"{mid}-{slug}.yaml", {
        "schema_version": "2.0.0", "type": "mitigation", "id": mid,
        "name": name, "summary": summary, "description": description,
        "domains": ["enterprise"], "measures": measures, "applications": applications,
        "evidence_refs": refs, "lifecycle": LIFE.copy(),
    })


def measure(key, name, action, control_type):
    return {"key": key, "name": name, "description": action, "control_type": control_type}


def application(target, use, effect, limits):
    return {"target_ref": target, "use": use, "expected_effect": effect, "limitations": limits}


def researched(tactic, key):
    return next(x for x in H[tactic]["defense_candidates"]["mitigations"]
                if x.get("temporary_key") == key or x.get("key") == key)


def app_from_pairs(target, item):
    return application(target, para(item["use"]["zh"], item["use"]["en"]),
                       para(item["expected_effect"]["zh"], item["expected_effect"]["en"]),
                       para(item["limitations"]["zh"], item["limitations"]["en"]))


# MIT-000131 already enforces access-layer path authority for authentication.
# Its two measures are unchanged; add precise content-flow applications instead
# of duplicating those controls under a new ID.
path = next((ROOT / "mitigations").glob("MIT-000131-*.yaml"))
shared = yaml.safe_load(path.read_text(encoding="utf-8"))
shared["summary"] = pair(
    "限制非授权网络权威发布并保留终端实际指向，降低认证或内容通信被改道的机会。",
    "Restrict unauthorized network-authority announcements and retain endpoint-accepted directions to reduce redirection of authentication or content communications.")
shared["description"] = para(
    "在接入层限制谁能发布地址、名称与网关权威，并保留终端实际采用的配置。现有 DHCP snooping、动态 ARP 检查、DHCPv6 Guard、RA Guard 和名称解析治理分别覆盖适用协议；同一控制既能减少凭据路径替换，也能减少一般内容流被引到非授权中间节点。它不能阻止攻击者控制已批准代理或受信根后的 TLS 终止。",
    "Constrain who can announce address, name, and gateway authority at the access layer and retain the configuration endpoints actually accept. Existing DHCP snooping, Dynamic ARP Inspection, DHCPv6 Guard, RA Guard, and name-resolution governance cover their applicable protocols. The same control reduces both credential-path substitution and diversion of ordinary content flows, but it cannot stop TLS termination by a compromised approved proxy or trusted root.")
authority = researched("T1557", "T1557C_MIT_NETWORK_AUTHORITY_EXTENSION")
targets = {"T1557C_PARENT": "NJT-0142", "T1557C_CHILD_SELECTIVE": "NJS-0142-001"}
shared["applications"] = [a for a in shared["applications"] if a["target_ref"] not in targets.values()]
shared["applications"].extend(app_from_pairs(targets[x["target_key"]], x) for x in authority["applications"])
shared["evidence_refs"] = list(dict.fromkeys(shared["evidence_refs"] + ["REF-000556", "REF-000488"]))
shared["lifecycle"]["version"] = "0.2.0"
shared["lifecycle"]["modified"] = "2026-09-22"
save(path, shared)

tls = researched("T1557", "T1557C_MIT_TLS_TRUST")
tls_names = [pair("受信根与检查代理来源管理", "Trust-Root and Inspection-Proxy Provenance"),
             pair("敏感源站独立证书对照", "Independent Certificate Comparison for Sensitive Origins")]
tls_measures = [measure(x["key"], tls_names[i], para(x["description"]["zh"], x["description"]["en"]), x["control_type"])
                for i, x in enumerate(tls["measures"])]
tls_apps = [app_from_pairs(target, item) for target, item in
            zip(["NJT-0142", "NJS-0142-002"], tls["applications"])]
mitigation("MIT-000144", "content-tls-trust-boundary-governance", tls["name"],
           pair("约束内容通信的受信根和检查代理，暴露未经批准的 TLS 终止。",
                "Constrain trusted roots and inspection proxies for content communications and expose unapproved TLS termination."),
           para("对受管端点的根证书、浏览器信任库和批准检查代理维持所有者、来源、范围与撤销历史，再从独立出口比较敏感域源站证书和终端实见链。该控制使攻击者难以让替代证书被默默接受；对合法企业检查与 CDN 差异必须按具体服务核验。",
                "Maintain owner, provenance, scope, and revocation history for endpoint roots, browser stores, and approved inspection proxies, then compare independent-origin certificates with chains actually accepted for sensitive domains. This makes silent acceptance of substitutes harder while requiring service-specific review of authorized enterprise inspection and CDN differences."),
           tls_measures, tls_apps, ["REF-000556", "REF-000557"])

repo = researched("T1213", "T1213_MIT_REPOSITORY_READ_SCOPE")
repo_names = [pair("敏感库按职责授权", "Duty-Based Sensitive Repository Grants"),
              pair("查询与成功读取审计", "Query and Successful-Read Audit")]
repo_measures = [measure(x["key"], repo_names[i], para(x["description_zh"], x["description_en"]), x["control_type"])
                 for i, x in enumerate(repo["measures"])]
repo_apps = [application(target, para(x["use_zh"], x["use_en"]),
                         para(x["expected_effect_zh"], x["expected_effect_en"]),
                         para(x["limitations_zh"], x["limitations_en"]))
             for target, x in zip(["NJT-0143", "NJS-0143-001"], repo["applications"])]
mitigation("MIT-000145", "sensitive-repository-read-scope-governance", repo["name"],
           pair("缩小非职责信息库读取范围并保留低量高敏对象访问的上下文。",
                "Narrow out-of-duty repository reads and retain context for small high-sensitivity access sets."),
           para("以业务 owner 和对象敏感度约束站点、空间和库的读取权，同时验证搜索、对象读取与下载审计确已开启并能用稳定对象键关联。这个控制既减少可被关键词筛中的无关敏感内容，也让合法调查、维护和员工研究有可核对的批准范围；产品不能提供页面读取事件时，应承认盲区。",
                "Constrain site, space, and repository reads by business owner and object sensitivity while verifying that search, object-read, and download audit is enabled and joinable through stable object keys. This reduces unrelated sensitive content reachable by keyword selection and gives legitimate investigations, maintenance, and employee research an auditable approval scope. Where a product lacks page-read events, the gap remains explicit."),
           repo_measures, repo_apps, ["REF-000565", "REF-000561", "REF-000563", "REF-000564"])

mail = researched("T1114", "T1114_MIT_CONTENT_PATH_CONTROL")
mail_measures = [
    measure("managed-mail-replica", pair("受管邮件副本范围", "Managed Mail Replica Scope"),
            para(mail["measures"][0]["use"]["zh"], mail["measures"][0]["use"]["en"]), "preventive"),
    measure("automatic-routing-governance", pair("自动邮件分流治理", "Automatic Mail Routing Governance"),
            para(mail["measures"][1]["use"]["zh"], mail["measures"][1]["use"]["en"]), "preventive"),
]
mail_apps = [
    application("NJT-0144",
                para("对高敏邮箱同时限定可保留的端点副本和允许的自动转发目的地，保留服务器与端点的读取、规则和消息结果记录。",
                     "For sensitive mailboxes, constrain retained endpoint replicas and allowed auto-forward destinations while keeping server and endpoint read, rule, and message-outcome records."),
                para("攻击者可继承的历史邮件集合和能自动生成的新副本范围缩小，跨平面调查有可连接的证据。",
                     "The historical mail an actor can inherit and new copies a rule can generate both shrink, with joinable evidence for cross-plane investigation."),
                para("离线办公、合规日记与迁移需例外；已控制的受管端点或获批收件人仍可能被滥用。",
                     "Offline work, journaling, and migration need exceptions; a compromised managed endpoint or approved recipient may still be abused.")),
    application("NJS-0144-001",
                para("将高敏邮箱的离线同步期限和设备限定到有业务需要的范围，盘点既存 PST/缓存并审计非预期进程读取。",
                     "Limit offline sync duration and devices for sensitive mailboxes to business need, inventory existing PST or caches, and audit unexpected process reads."),
                para("可离线二次读取的历史邮件范围下降，端点副本接触更容易归因到设备和进程。",
                     "The historical mail available for offline rereading shrinks, and replica access becomes easier to attribute to device and process."),
                para("既有副本不会因策略更新立刻消失，合法迁移或 eDiscovery 也会读取相同文件。",
                     "Existing copies do not disappear immediately after policy changes, and authorized migration or eDiscovery reads the same files.")),
    application("NJS-0144-002",
                para("对新增的条件自动转发要求具体邮箱、谓词、目的地、批准人和有效期，并把规则变更同实际自动转发报告核对。",
                     "Require mailbox, predicate, destination, approver, and expiry for new conditional auto-forwarding, then compare rule changes with actual forwarding reports."),
                para("非批准外部分流被阻断或留下策略拒绝结果，内部异常目的地也更容易偏离批准清单。",
                     "Unapproved external diversion is blocked or leaves policy-denial evidence, while anomalous internal recipients depart from the approved register."),
                para("被盗获批账户和受控内部收件人仍可取得邮件；外部转发禁令不能替代匹配消息的结果核验。",
                     "A stolen approved account or controlled internal recipient can still receive mail; external-forward blocking does not replace matched-message outcome checks.")),
]
mitigation("MIT-000146", "mail-replica-and-routing-minimization", mail["name"],
           pair("约束既存邮件副本与条件自动转发两种可被滥用的内容取得路径。",
                "Constrain preexisting mail replicas and conditional auto-forwarding as distinct paths to mailbox content."),
           para("高敏邮箱的缓存范围、允许设备和端点副本需要和业务离线需求匹配；自动转发规则需按邮箱、匹配谓词、目的地和期限审批。服务器逐封访问、规则变更、转发结果与端点副本读取分别留存，避免把某一平面无事件误作无收集。措施不能直接撤回已被复制的邮件。",
                "Cache scope, allowed devices, and endpoint replicas for sensitive mailboxes should match real offline needs; auto-forward rules need approval by mailbox, predicate, destination, and duration. Retain server per-item access, rule changes, forwarding outcomes, and endpoint replica reads separately so silence on one plane is not mistaken for absence of collection. The measures cannot retract mail already copied."),
           mail_measures, mail_apps, ["REF-000567", "REF-000568", "REF-000570", "REF-000571", "REF-000572", "REF-000573", "REF-000379"])

browser = researched("T1185", "T1185_MIT_BROWSER_CONTROL")
browser_names = [pair("敏感站点扩展权限治理", "Sensitive-Site Extension Permission Governance"),
                 pair("浏览器进程写入权限限制", "Browser-Process Write Permission Reduction"),
                 pair("高价值会话寿命控制", "High-Value Session Lifetime Control")]
browser_measures = [measure(x["key"].replace("_", "-"), browser_names[i],
                            para(x["description"]["zh"], x["description"]["en"]), x["control_type"])
                    for i, x in enumerate(browser["measures"])]
browser_apps = [app_from_pairs(target, x) for target, x in
                zip(["NJT-0145", "NJS-0145-001", "NJS-0145-002"], browser["applications"])]
mitigation("MIT-000147", "browser-control-and-session-reduction", browser["name"],
           pair("限制对浏览器执行上下文的控制，并缩短已认证内容可被借用的窗口。",
                "Constrain control over browser execution contexts and shorten the window in which authenticated content can be borrowed."),
           para("对敏感站点治理扩展来源、主机和调试权限，限制普通账户写入浏览器进程，并对高价值应用采用合理会话到期和设备复核。措施分别提高同页中介与代理借用的成本；既有受信扩展失陷和正常远程支持必须依具体身份、版本与任务审查，不能只按浏览器名称允许。",
                "Govern extension origin, host, and debugger permissions for sensitive sites, reduce ordinary-account write access to browsers, and apply reasonable expiry and device checks to high-value sessions. These controls raise the cost of both co-viewed interposition and proxy borrowing. Compromise of an approved extension and legitimate remote support require identity, version, and task-specific review rather than a browser-name allow rule."),
           browser_measures, browser_apps,
           ["REF-000574", "REF-000575", "REF-000579", "REF-000580", "REF-000581", "REF-000366"])

audio_process = researched("T1123", "T1123_MIT_PROCESS")
audio_names = [pair("受管会议进程与麦克风授权", "Managed Meeting Process and Microphone Grants"),
               pair("音频活动与模块复核", "Audio Activity and Module Review")]
audio_measures = [measure(x["key"].replace("_", "-"), audio_names[i], para(x["zh"], x["en"]), x["control_type"])
                  for i, x in enumerate(audio_process["measures"])]
audio_apps = [app_from_pairs(target, x) for target, x in
              zip(["NJT-0146", "NJS-0146-001"], audio_process["applications"])]
mitigation("MIT-000148", "meeting-process-microphone-integrity", audio_process["name"],
           pair("限制未批准录音模块进入会议进程，并把麦克风活动与真实模块及结果关联。",
                "Constrain unapproved recorder modules in meeting processes and join microphone activity to real module and output."),
           para("会议客户端、插件和麦克风权限应经受管渠道批准，并留存能实际取得的音频设备会话与模块谱系。对正常会议进程中的新模块、非会议时段录音和异常产物按业务批准单核查；进程签名或授权提示只证明表层身份，不替代录音目的判断。",
                "Approve meeting clients, plug-ins, and microphone permissions through managed channels and retain audio-device sessions and module lineage where actually available. Compare new modules, out-of-meeting recording, and unusual outputs in normal meeting processes with business approvals. Process signing or a permission prompt proves surface identity, not recording purpose."),
           audio_measures, audio_apps, ["REF-000583", "REF-000586", "REF-000587", "REF-000588"])

call = researched("T1123", "T1123_MIT_CALL_API")
call_names = [pair("批准通话媒体集成", "Approved Call-Media Integrations"),
              pair("接口授权与录音结果复核", "Interface Grant and Recording Outcome Review")]
call_measures = [measure(x["key"].replace("_", "-"), call_names[i], para(x["zh"], x["en"]), x["control_type"])
                 for i, x in enumerate(call["measures"])]
call_app = app_from_pairs("NJT-0146", call["applications"][0])
mitigation("MIT-000149", "call-app-interface-grant-governance", call["name"],
           pair("审批第三方通话媒体接口并把授权与录音结果连接。",
                "Approve third-party call-media interfaces and join grants to recording outcomes."),
           para("对提供媒体接口的受管通话应用，按请求组件、用户、会话和有效期限制第三方授权，并保留可查询的授予及撤销记录。通话时段、音频文件和导出任务应与授权链比较；没有接口审计的产品须退回到端点应用控制，不能把旧 Skype 接口名称当作现行通用措施。",
                "For managed call apps with media interfaces, constrain third-party grants by requester, user, session, and duration, retaining searchable grant and revocation records. Compare call periods, audio files, and export jobs with the grant chain. Products without interface audit require endpoint application control, and old Skype API names are not universal current controls."),
           call_measures, [call_app], ["REF-000584"])

print("Extended MIT-000131 and serialized six target-specific Collection mitigations in draft")
