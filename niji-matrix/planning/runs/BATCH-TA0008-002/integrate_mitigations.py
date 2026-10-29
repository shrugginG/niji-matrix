#!/usr/bin/env python3
"""Serialize four distinct controls and target-specific applications."""
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[3]
def P(zh,en):return {"paragraphs":[{"zh":zh,"en":en}]}
def M(key,zh,en,dzh,den,kind):
    return {"key":key,"name":{"zh":zh,"en":en},"description":P(dzh,den),"control_type":kind}
def A(target,uz,ue,ez,ee,lz,le):
    return {"target_ref":target,"use":P(uz,ue),"expected_effect":P(ez,ee),"limitations":P(lz,le)}
DATA=[
{
"id":"MIT-000152","slug":"shared-object-authority-and-consumer-integrity",
"name":{"zh":"共享对象写权与消费完整性治理","en":"Shared-Object Authority and Consumer Integrity Governance"},
"summary":{"zh":"限制共享对象的未批准改写，并在另一主机消费前验证内容与导航目标。","en":"Constrain unauthorized shared-object mutations and verify content and navigation targets before another host consumes them."},
"description":P(
"该控制同时保护共享对象的写入前态和异机消费点。对关键文档、安装包及导航目录保存旧新版本、授权发布者、内容摘要和目标绑定，使安全团队能把原路径下的恶意内容变化与另一主机的首次结果相连。保留业务协作能力，但不把熟悉的文件名、目录图标、签名容器或受信位置视作本次改写的授权。",
"This control protects both a shared object's prior state and its cross-host consumption point. Preserve old and new versions, authorized publishers, digests, and target bindings for critical documents, installers, and navigation directories so security teams can join malicious change under an original path to another host's first outcome. Keep legitimate collaboration available without treating a familiar filename, directory icon, signed container, or trusted location as authorization for this mutation."),
"measures":[
M("bounded-shared-write-authority","限定共享内容写权","Bound Shared-Content Write Authority",
"把高价值共享区的编辑者、发布窗口与目标对象限定到具名角色和变更单；分离文档日常编辑与可执行内容发布权限，并保留不可由同一编辑者删除的旧版本和摘要。",
"Limit editors, release windows, and target objects in high-value shares to named roles and change records. Separate routine document editing from executable-content publishing, and retain prior versions and digests that the same editor cannot delete.","preventive"),
M("active-content-and-binding-check","消费前检查活动内容与导航绑定","Check Active Content and Navigation Binding Before Consumption",
"对原路径内容变化检查宏、远程模板、脚本入口和二进制签名或摘要差异；对目录入口核对可见名称、图标、实际目标命令和隐藏原目录。目标主机对未批准活动内容实施 Office、脚本或应用控制。",
"Inspect changes under original paths for macros, remote templates, script entry points, and binary signing or digest differences. Compare a directory entry's visible name and icon with its actual target command and any hidden original. Enforce Office, script, or application control on unapproved active content at consuming hosts.","preventive"),
M("consumer-scope-recovery","按版本恢复异机消费范围","Recover Cross-Host Consumer Scope by Version",
"发现污染时冻结对应对象版本与导航入口，隔离恶意内容并查询哪些内部设备实际读取、打开和产生后继进程；通过批准版本恢复共享内容后再解除限制。",
"On taint discovery, freeze the object version and navigation entry, isolate malicious content, and identify internal devices that actually read, opened, and launched successors from it. Restore an approved version before lifting controls.","containment")],
"applications":[
A("NJT-0148",
"把共享对象变更审批、旧新版本留存和异机消费日志连成发布事务，要求调查明确写者、对象、目标设备及首个攻击者结果。",
"Treat share mutation approval, retained versions, and cross-host consumption logs as one release transaction, requiring investigation to identify writer, object, destination device, and first attacker outcome.",
"恶意内容即使保留原路径也会与授权版本产生差异，已消费目标可以按同一版本枚举并处置。",
"Malicious content retaining an original path still differs from an approved version, and affected consumers can be enumerated and remediated by version.",
"高频协作和内部受信位置可能缺精确版本、预览与真实打开的区别；无法解析活动内容时要保留不确定性并用目标进程补证。",
"High-volume collaboration and internal trusted locations may lack exact versions or distinguish preview from real open. Retain uncertainty when active content cannot be parsed and corroborate with destination processes."),
A("NJS-0148-001",
"针对既有对象原位污染，锁定旧新摘要、嵌入宏或模板引用与授权编辑者，并在另一设备打开前检查其活动内容。",
"For in-place taint of an established object, bind old and new digests, embedded macro or template references, and approved editor, then inspect active content before another device opens it.",
"原文件名和路径不再足以让被替换文档或安装包自动继承信任；同一版本的消费者能被准确回查。",
"Original name and path no longer confer automatic trust on a replaced document or installer, and consumers of one version can be traced accurately.",
"恶意逻辑可位于合法签名容器或运行时远程模板中；内容扫描需要联网响应和解析能力，业务宏例外须绑定版本和期限。",
"Malicious logic may sit inside a legitimately signed container or a runtime remote template. Content scanning needs response access and parsers, while business macro exceptions must bind a version and expiry."),
A("NJS-0148-002",
"针对导航替身，比较目录项可见名称和图标与真实文件类型、快捷方式目标、隐藏原目录及受害主机点击后的命令链，阻止非管理员在高价值共享目录创建同名替身。",
"For navigation substitution, compare visible name and icon with actual entry type, shortcut target, hidden original directory, and the consumer's post-click command chain. Block non-administrators from creating same-name substitutes in high-value shares.",
"攻击者不能仅靠目录外观和后续正常 Explorer 视图掩盖额外命令，异常绑定可在多台用户触发前被阻断。",
"The attacker cannot rely only on directory appearance and a later normal Explorer view to conceal the extra command; anomalous bindings can be blocked before many users trigger them.",
"合法 DFS、快捷方式和目录迁移也会改变导航绑定；缺少目标端进程谱系时只能确认替身存在，不能证明其被打开并执行。",
"Legitimate DFS, shortcuts, and directory migrations also change navigation bindings. Without destination process lineage, only substitute presence can be confirmed, not open and execution.")],
"evidence_refs":["REF-000590","REF-000591","REF-000592","REF-000593","REF-000594","REF-000595","REF-000190"]},
{
"id":"MIT-000153","slug":"internal-remote-service-exploit-surface-control",
"name":{"zh":"内网远程服务漏洞触发面控制","en":"Internal Remote-Service Exploit Surface Control"},
"summary":{"zh":"缩小可触达的内网脆弱服务，及时修补并保留请求到目标结果的响应证据。","en":"Reduce reachability of vulnerable internal services, patch promptly, and preserve request-to-target-outcome evidence."},
"description":P(
"该控制针对内网服务漏洞这一横向因果入口，而非通用远程登录。资产所有者先盘点服务版本和业务源，再实施补丁、弃用脆弱协议与分区访问；安全团队对仍暴露的关键服务保留利用请求、异常状态和目标结果，使失败尝试与已确认异机控制可以分开处置。",
"This control targets the internal service vulnerability as the lateral causal entry rather than remote login in general. Asset owners inventory service versions and business sources before patching, retiring vulnerable protocols, and segmenting access. Security teams retain exploit requests, abnormal states, and target outcomes for remaining critical services so failed attempts and confirmed cross-host control receive different responses."),
"measures":[
M("patch-and-retire-vulnerable-service","修补或退役脆弱服务","Patch or Retire Vulnerable Services",
"把资产、服务版本、补丁与暴露源按时间绑定；优先修补高价值主机的已知远程执行漏洞，无法修补时禁用对应旧协议或服务功能。",
"Bind assets, service versions, patches, and reachable sources over time. Prioritize known remote-code-execution fixes on high-value hosts and disable obsolete protocols or service functions when patching is impossible.","preventive"),
M("least-reachable-east-west-service","最小化东西向服务可达性","Minimize East-West Service Reachability",
"用分区和主机防火墙只允许需要该服务的具名源连接目标，不让普通工作站任意触达服务器管理或遗留 SMB/RDP 面；对例外设置 owner 与到期时间。",
"Use segmentation and host firewalls to allow named business sources only, preventing ordinary workstations from reaching server management or legacy SMB/RDP surfaces indiscriminately. Give each exception an owner and expiry.","exposure-reduction"),
M("exploit-to-outcome-evidence","保留利用到结果的多层证据","Preserve Exploit-to-Outcome Evidence",
"保留协议异常、服务崩溃或缓解事件、目标进程及后继连接，并把受影响版本与事件时补丁状态附在告警中。",
"Retain protocol anomalies, service crashes or mitigation events, destination processes, and successor connections, attaching the affected version and event-time patch state to alerts.","detective-support")],
"applications":[
A("NJT-0149",
"对 T1210 的内部目标按服务和业务源建立允许图，修补或关闭已知脆弱版本；若告警出现入站利用迹象与目标异常结果，限制源到其他同类目标的可达性并核查已受控主机。",
"For T1210 internal targets, build an allowed service-by-source graph and patch or close known vulnerable versions. When exploit indications meet an abnormal target outcome, restrict the source's reach to similar targets and inspect potentially controlled hosts.",
"攻击者可尝试的目标数量和脆弱功能减少；未被阻断的利用也更容易形成可核查的请求—状态—结果链。",
"The number of reachable targets and vulnerable functions declines, while unblocked exploitation yields a more reviewable request-to-state-to-outcome chain.",
"未知漏洞、旧系统停机窗口、加密协议和无服务内部日志会限制效果；补丁台账与一次 SMB 会话都不能单独证明某台目标未被利用或已经失陷。",
"Unknown vulnerabilities, legacy-system maintenance windows, encrypted protocols, and missing service logs limit the effect. Patch inventory or one SMB session alone cannot prove a destination safe or compromised.")],
"evidence_refs":["REF-000591","REF-000600","REF-000602","REF-000603","REF-000605","REF-000243"]},
{
"id":"MIT-000154","slug":"internal-lure-inspection-and-recipient-verification",
"name":{"zh":"内部诱导消息检查与收件者独立核验","en":"Internal Lure Inspection and Independent Recipient Verification"},
"summary":{"zh":"对组织内消息执行内容检查和高风险动作独立核验，阻止受陷账户把信任继续传给下一主体。","en":"Inspect intra-organization messages and independently verify high-risk recipient actions so a compromised account cannot carry trust to another principal."},
"description":P(
"该控制处理“真实内部发件身份仍可作恶”的问题。内部邮件和协作消息应接受与外部诱导相称的链接、附件和身份风险检查，并在敏感凭据、远程协助或付款请求处设置独立确认路径；事件响应同时保留发件会话、收件范围和点击或附件结果。邮箱账户和规则完整性由 MIT-000036 补充，消息本身及收件动作由本对象控制。",
"This control addresses malicious use of a genuine internal sender. Intra-organization mail and collaboration messages receive link, attachment, and identity-risk inspection commensurate with external lures, while sensitive credential, remote-assistance, or payment requests require independent confirmation. Response retains sender sessions, recipient scope, and click or attachment outcomes. MIT-000036 complements mailbox account and rule integrity, while this object controls the message and recipient action."),
"measures":[
M("inspect-internal-message-content","检查内部链接与附件","Inspect Internal Links and Attachments",
"对组织内流转的消息仍运行 URL、附件和异常发件会话检查，保留 NetworkMessageId、发件与收件身份、内容摘要及投递状态，不能因同域身份自动免检。",
"Run URL, attachment, and anomalous-sender-session checks on internal messages, retaining NetworkMessageId, sender and recipient identities, content digest, and delivery state without automatically trusting same-domain mail.","preventive"),
M("independent-high-risk-action-verification","高风险动作独立核验","Independently Verify High-Risk Actions",
"当内部消息要求重新认证、启用宏、安装远控或处理敏感流程时，收件者通过既有可信渠道联系真实发件人或业务 owner，核验当前请求与操作目标。",
"When an internal message requests reauthentication, macro enablement, remote-control installation, or a sensitive workflow, recipients confirm the current request and target through an existing trusted channel with the real sender or business owner.","cost-increasing"),
M("trace-and-contain-recipient-fanout","追踪并处置收件扩散","Trace and Contain Recipient Fan-Out",
"发现受陷发件账户时撤销其会话、冻结继续投递，按消息标识查找所有内部收件者及后续动作，并对已出现第二账户异常的主体优先处置。",
"When a sender compromise is found, revoke sessions, stop further delivery, identify all internal recipients and subsequent actions by message ID, and prioritize principals with signs of second-account compromise.","containment")],
"applications":[
A("NJT-0150",
"对内部定向钓鱼把已证受陷发送者、消息内容、受害收件者动作与第二账户结果绑定。高风险请求通过独立渠道复核；发现连锁失陷时按同一发件会话和消息批次处置全部目标。",
"For Internal Spearphishing, join a confirmed compromised sender to message content, recipient action, and second-account outcome. Verify high-risk requests through an independent channel and, on chained compromise, respond to every target in the same sender session and message batch.",
"内部发件身份不再自动绕过内容与操作核验，第二账户失陷前的点击或附件打开可触发有范围的阻断与告警。",
"An internal sending identity no longer bypasses content and action checks; clicks or attachment opens can trigger scoped blocking and alerts before a second account is lost.",
"获批安全演练、真实协作和帮助台流程会产生相似消息；未知协作平台、无链接点击遥测或第二账户调查未完成时，不能以投递数替代横向成功判断。",
"Approved simulations, genuine collaboration, and help-desk workflows create similar messages. Unlogged collaboration platforms, absent click telemetry, or unfinished second-account investigation prevent delivery count from substituting for lateral success.")],
"evidence_refs":["REF-000607","REF-000608","REF-000609","REF-000610","REF-000611","REF-000612"]},
{
"id":"MIT-000155","slug":"remote-session-ownership-and-control-governance",
"name":{"zh":"远程会话所有权与控制端治理","en":"Remote Session Ownership and Controller Governance"},
"summary":{"zh":"限制已认证连接的额外控制者，并记录 SSH 通道或 RDS 会话控制端变化。","en":"Restrict extra controllers on authenticated connections and record SSH channel or RDS session controller changes."},
"description":P(
"该控制固定远程传输和交互会话的原所有者、合法复用主体、授权窗口与目标范围。对 SSH，保护 ControlPath 套接字和运行中客户端，必要时关闭持久复用并验证通道级遥测；对 RDS，限制 tscon 与 shadow 控制权限、要求可核查同意并及时结束不再需要的会话。安全审计需要从附着动作继续看到目标结果，而不把无新登录事件误当成安全状态。",
"This control fixes the original owner, allowed sharing principals, authorization window, and target scope of remote transports and interactive sessions. For SSH, protect ControlPath sockets and running clients, disable persistent sharing where unnecessary, and validate channel-level telemetry. For RDS, restrict tscon and shadow-control rights, require verifiable consent, and end sessions no longer needed. Audit must continue from an attachment action to destination outcome instead of treating no new logon event as a safe state."),
"measures":[
M("protect-ssh-controller-boundary","保护 SSH 控制套接字与客户端","Protect SSH Control Sockets and Clients",
"把控制套接字置于仅原所有者可访问的目录，限制跨用户 ptrace 与调试；跳板上按角色缩短 ControlPersist，并在不需多路复用的服务关闭该功能。",
"Keep control sockets in directories accessible only to their original owner, restrict cross-user ptrace and debugging, shorten ControlPersist by jump-host role, and disable multiplexing where service duties do not need it.","preventive"),
M("bound-rds-session-transfer","限定 RDS 会话转移与影子控制","Bound RDS Session Transfer and Shadow Control",
"最小化可运行 tscon 或修改 shadow 策略的身份，要求帮助台会话接管有目标、工单、时限及原用户可核查的同意；对高权限断开会话实施短期终止策略。",
"Minimize identities able to run tscon or change shadow policy. Require target, ticket, expiry, and verifiable original-user consent for support takeover, and end disconnected high-privilege sessions promptly.","preventive"),
M("retain-controller-transition-evidence","保留控制者转换证据","Retain Controller-Transition Evidence",
"在可部署环境保留 SSH 连接/通道标识和本地 socket 访问，Windows 保留 4778/4779、进程命令行、shadow 操作及策略旧新值，并连接目标资源结果。",
"Where deployable, retain SSH connection and channel IDs with local socket access; on Windows retain 4778 and 4779, process command lines, shadow operations, and old and new policy values, joining them to target resource outcomes.","detective-support")],
"applications":[
A("NJT-0151",
"为高价值远程会话登记原所有者、可附着主体和失效时间，并将任何新控制者与目标动作核对；不允许一个成功登录记录长期代表所有后来操作。",
"Register original owner, allowed attaching principals, and expiry for high-value remote sessions, and compare every later controller with target actions rather than letting one successful logon stand for all future operations.",
"旧会话在被他人复用时产生可审计的身份差异，未批准附着的机会和存活时间下降。",
"Reuse of an old session by another person yields an auditable identity difference, while opportunities and lifetime for unauthorized attachment decline.",
"授权帮助台与自动化也会复用会话；缺少通道级或影子控制遥测时只能降低信心、不能宣称没有接管。",
"Authorized support and automation also reuse sessions. Without channel-level or shadow-control telemetry, confidence falls and absence of takeover cannot be asserted."),
A("NJS-0151-001",
"对同一认证 SSH 传输上的增附通道限制 ControlPath 访问者与跨用户调试，并按连接 ID、通道 ID 与本地发起进程记录批准复用关系。",
"For added channels on one authenticated SSH transport, constrain ControlPath access and cross-user debugging, recording approved sharing by connection ID, channel ID, and local initiating process.",
"攻击者难以借用原管理员连接悄然增加新 shell/exec 通道；不符原所有者的本地发起者仍可被定位。",
"An adversary finds it harder to add a shell or exec channel through the original administrator's connection without detection, and a local initiator outside the owner's lineage can be located.",
"标准 sshd 不保证可查询通道 ID，root 或已控跳板传感器可绕过本机记录；需要在具体部署上验证日志能力。",
"Stock sshd does not guarantee queryable channel IDs, and root or a compromised jump-host sensor may defeat local logging; verify capabilities in each deployment."),
A("NJS-0151-002",
"对已有 RDS 交互会话的独占迁移或 shadow 共控，按原 LogonID 保留旧新客户端、tscon 或 mstsc 控制请求、策略和原用户同意，并对高权限会话单独审批。",
"For exclusive transfer or shadow co-control of an existing RDS session, retain old and new clients, tscon or mstsc control requests, policy, and original-user consent under one LogonID, requiring separate approval for privileged sessions.",
"接管不能仅凭原账户已登录而失去归因，未经批准的控制端和会话结果可被关联并阻断。",
"Takeover no longer loses attribution merely because the original account was logged on; an unapproved controller can be joined to session outcomes and blocked.",
"网络断线重连与合法支持接管可同形，部分平台不产生所有 4778/4779 或 shadow 事件；受阻 tscon 也不能当作成功迁移。",
"Network reconnects and legitimate support handoffs can look similar; some platforms do not emit all 4778, 4779, or shadow events, and a blocked tscon cannot be counted as successful transfer.")],
"evidence_refs":["REF-000614","REF-000615","REF-000616","REF-000617","REF-000618","REF-000619","REF-000620","REF-000621","REF-000622","REF-000623","REF-000624","REF-000370"]},
]
assert len(DATA)==4
for d in DATA:
    obj={"schema_version":"2.0.0","type":"mitigation",**{k:v for k,v in d.items() if k!="slug"},
         "domains":["enterprise"],
         "lifecycle":{"status":"draft","version":"0.1.0","created":"2026-09-22","modified":"2026-09-22",
                      "contributors":["Niji Matrix Research"],"reviewers":[]}}
    slug=d["slug"]
    path=ROOT/"mitigations"/f"{d['id']}-{slug}.yaml"
    if path.exists():raise RuntimeError(path)
    path.write_text(yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
print("serialized",len(DATA),"reviewed mitigations")
