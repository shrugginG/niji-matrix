# T1667 Email Bombing / 邮件轰炸：TA0040 研究交接

工作项 `WORK-TA0040-T1667`；批次 `BATCH-TA0040-004`；临时键前缀 `TA0040-T1667-`。固定基线为 ATT&CK Enterprise 19.1。本交接只提交研究结果，不分配正式 ID，不修改正式矩阵、准入决策、共享库、战术计划或集成摘要。

## 1. 准入建议

**建议 `adapt`，父行为置信度 high，匿迹适配置信度 high。** T1667 与 Impact 直接相关，但正式范围必须从“发送很多邮件”改写为可验证的邮件注意力或邮件可用性损失：大量消息实际进入目标邮箱或邮件处理路径，并导致合法消息难以发现、处理或投递，邮箱接收限制/配额被触发，或业务响应出现可归因延迟。高消息量 alone 只能形成 `bomb_candidate`，不能完成技术。

**Recommendation: `adapt`, with high confidence in both the parent behavior and its stealth relevance.** T1667 directly belongs to Impact, but formal scope must be rewritten from “sending many messages” to verifiable loss of mail attention or mail availability: large message volume enters a target mailbox or mail-processing path and makes legitimate messages difficult to discover, process, or deliver, triggers mailbox receiving or quota constraints, or causes attributable business-response delay. High message volume alone creates only a `bomb_candidate` and does not complete the technique.

开放搜索支持两个 Niji 原生子项：

1. **合法发送者扇出式收件箱洪泛 / Legitimate-Sender Fan-Out Inbox Flooding**：攻击者把目标地址自动登记到大量第三方订阅/表单，让众多通过正常认证和信誉检查的发送者分别投递少量邮件，恶意因果只在单一收件人的 fan-in 处显现。
2. **关键消息埋没同步 / Consequential-Message Burial Synchronization**：攻击者围绕账户、交易、安全或业务事件安排轰炸窗口，使相应合法通知进入高密度邮件流并超出正常发现/处置时限。

ATT&CK T1667 没有子项；以上 taxonomy 完全依据稳定变量、痕迹变化和防守观察差异，不存在导入关系。

## 2. 邻接技术边界

| 相邻行为 | T1667 边界 |
|---|---|
| `NJT-0199` / T1499 端点拒绝服务 | T1667 的直接对象是收件人注意力、邮箱接收能力和合法邮件处理/投递。若 crafted message、zip bomb、附件解析或一般消息负载耗尽邮件服务器/客户端 CPU、内存、线程、存储或使应用崩溃，直接对象是 endpoint/application resources，应归 NJT-0199；若同一事件同时造成邮箱埋没和服务器资源失效，可分别记录。 |
| `NJT-0198` / T1498 网络拒绝服务 | SMTP 边界、链路或网络容量被包/连接洪泛饱和而邮件事务没有形成时归 NJT-0198。T1667 要求消息进入邮件处理或邮箱语义；网络带宽高不等于邮件轰炸完成。 |
| 钓鱼与初始访问 | 钓鱼邮件的直接目的在于诱导点击、附件执行、凭据提交或对话响应；无合法邮件埋没/投递影响时，即使大量投递也不是 T1667。Storm-1811 后续 Teams/电话冒充与 Quick Assist 属钓鱼/初始访问，前置 inbox overwhelm 可另记 T1667。 |
| 邮件 C2 | 邮件被用作 command、dead drop、任务或回传信道时直接对象是控制通信；少量或周期邮件不因使用邮件成为 bombing。只有相同信道另有可验证的 legitimate-message burial/service impact 时才共同记录。 |
| `NJT-0175` / T1621 MFA 请求轰炸 | T1621 由权威 IdP 产生真实 MFA challenge，直接目标是让用户批准或完成认证。即使 challenge 通知通过 email 到达，身份事务仍归 T1621。只有通知量进一步造成普通合法邮件埋没或邮箱接收损失时，才能用独立证据同时记录 T1667。 |
| 正常批量邮件 | 批准营销、员工通知、票务/告警风暴、邮件迁移、邮件列表错误、reply-all accident 和订阅导入可能产生相似量；缺少攻击者控制、target concentration 和实际影响时是反例。 |

## 3. Niji 原生轴开放搜索与收敛

固定 ATT&CK 子项数为 `0`，`original_attack_subtechniques_imported: false`。

| 候选轴 | 行为设计 → 痕迹变化 → 防守观察差异 | 决议 |
|---|---|---|
| 合法发送者扇出式收件箱洪泛 | bot 将一个地址登记到大量 newsletter/form → SPF/DKIM/DMARC 可通过、发送域/IP/模板高度分散、单源量接近正常 → source-centric block/reputation 只看见正常第三方，recipient-centric fan-in 才显示共同目标和影响 | **formal**。HHS 和 2016 .gov registration bombing 直接支持；专用字段和 mitigation 明确。 |
| 关键消息埋没同步 | bombing window 与 sign-in、contact change、financial transaction、order 或安全事件相邻 → 高价值合法通知本身不变，却与数百/数千低价值消息共享时间线 → mail-only volume 看不出被埋对象，需要 business/security event—notification—mailbox response 关联 | **formal**，confidence medium。HHS 明确说明攻击者希望受害者漏看这些消息；正式确认要求实际 notification 与响应延迟，不能从时间巧合升级。 |
| 低速长期积累 | 每分钟少量邮件长期维持 backlog，避开短窗阈值 → 单窗量低但未处理队列累积 | **defer**。Krebs/HHS 记录轰炸后仍持续来信，但没有足够结论级证据证明低速阶段是独立主动规避变量而非订阅后果。 |
| 别名/plus-address 变体扩张 | 攻击者利用地址规范化差异让多个表面地址落到同一 mailbox，绕过 exact-recipient 限额 | **defer**。存在实践报道，但缺少稳定跨提供方语义、攻击案例和专用防御证据。 |
| 大附件、zip bomb、reply-all 或 mass-mail 类型 | 改变 message payload、发送方式或事故来源 | **parent-core / adjacent**。若主要结果是服务计算/存储耗尽则归 T1499；类型本身不形成 NJS。 |
| spoof、compromised sender、botnet、newsletter、marketing platform | 改变发送来源 | **implementation**。只有跨合法第三方 fan-out 产生认证/信誉观察差异时进入 child 1；来源类别本身不划分。 |

## 4. 父技术完整双语字段草稿

### name / summary

- zh：**邮件轰炸**。攻击者向目标邮箱或邮件服务制造足以埋没合法消息或损害投递/处理的大量邮件，并利用合法发送者扇出或关键事件同步削弱 source-centric 过滤和用户发现。
- en: **Email Bombing**. Adversaries cause enough mail to enter a target mailbox or mail service to bury legitimate messages or impair delivery and handling, while legitimate-sender fan-out or synchronization with consequential events weakens source-centric filtering and user discovery.

### definition_and_concept

zh：邮件轰炸是攻击者控制消息生成或第三方订阅触发，使大量邮件集中进入一个或一组目标邮箱或其邮件处理路径，并实际造成合法邮件难以发现、阅读、处置或投递，或者使邮箱接收能力和业务工作流中断的 Impact 行为。直接对象是邮件注意力与邮箱/邮件流可用性；发送工具、SMTP 软件、附件类型、邮件客户端和云厂商只是实现。

en: Email Bombing is an Impact behavior in which an adversary controls message generation or third-party subscription triggers so that large volumes of mail converge on one or more target mailboxes or their processing path and actually make legitimate mail difficult to discover, read, act upon, or deliver, or interrupt mailbox receiving capacity and business workflow. The direct object is mail attention and mailbox or mail-flow availability. Sending tool, SMTP software, attachment type, mail client, and cloud provider are implementations.

zh：Niji 关注高量如何改变合法消息在守方和用户视野中的相对位置，而不是把 message count 本身当成匿迹。攻击者可把发送动作委托给大量真实 newsletter/transactional senders，使单个 message 通过认证并保持正常来源外观；也可把 bombing 与一个需要被受害者发现的合法通知同步，让该通知的内容、签名和投递都正常，却在高密度 mailbox timeline 中失去显著性。必须证明 burial、处理延迟、接收限制或投递失败，不能从高量直接推断影响。

en: Niji focuses on how volume changes the relative position of legitimate messages in defender and user views rather than treating message count itself as stealth. An adversary can delegate delivery to many genuine newsletter or transactional senders so each message authenticates and retains ordinary source appearance. The actor can also synchronize bombing with a legitimate notification the victim needs to discover, leaving its content, signature, and delivery intact while removing its salience in a dense mailbox timeline. Burial, handling delay, receiving limits, or delivery failure must be proven rather than inferred from volume.

### stealth_characteristics

zh：邮件轰炸总体数量通常显眼；匿迹特性存在于 source-local 与 recipient-global 观察差。Registration bomb 中，数百或数千邮件由不同合法组织发送，SPF/DKIM/DMARC 可能正常、每个 sender 只占很小比例，按源信誉、单域速率或 spoof 检查的过滤器因而看不到共同攻击者。所有 messages 的共同关系是 target recipient、相近 signup/start time、首次联系、主题/模板簇和异常 fan-in。

en: Overall email-bomb volume is usually conspicuous. Its stealth characteristic lies in the difference between source-local and recipient-global observation. In a registration bomb, hundreds or thousands of messages come from different legitimate organizations, SPF, DKIM, or DMARC may pass, and each sender contributes little, so source reputation, per-domain rate, or spoofing checks do not reveal one adversary. The shared relationship lies in target recipient, nearby signup or start time, first contact, subject or template clusters, and anomalous fan-in.

zh：当 bombing 与关键通知同步时，合法 message 不被删除、篡改或隐藏规则移动；它仍可在 trace 和 inbox 中存在，却因相邻消息密度、client notification overload 和人工处理 backlog 而未被及时访问或处置。残余包括 `NetworkMessageId`、sender/domain/IP、authentication result、`EmailClusterId`、delivery action/location、received/isRead/folder 状态、MailItemsAccessed、mailbox receive-limit/queue/NDR、业务 notification ID 和 acknowledgment。用户离线、夜间、休假、合法告警风暴及 inbox rule 仍是强反例。

en: When bombing is synchronized with a consequential notification, the legitimate message is not deleted, altered, or moved by a hiding rule. It remains present in trace and mailbox but is not accessed or acted on in time because of adjacent-message density, client-notification overload, and human-processing backlog. Residual evidence includes `NetworkMessageId`, sender, domain, IP, authentication result, `EmailClusterId`, delivery action and location, received, isRead, and folder state, MailItemsAccessed, mailbox receiving limits, queue, NDR, business notification ID, and acknowledgment. User absence, nighttime, leave, legitimate alert storms, and inbox rules remain strong counterexamples.

### scope_boundary_definition

zh：纳入要求三层至少闭合两层且结果层必有：攻击者控制的发送/订阅触发或可支持的 campaign attribution；大量消息实际被 target mailbox/mail path 接收；合法消息发现/处置超时、关键通知漏看、接收限制/配额、合法邮件 defer/reject 或业务工作流中断。只有前两层而无结果时标为 candidate，只有 message count 或 spam verdict 不确认技术。

en: Inclusion requires closure of at least two of three layers, always including the outcome layer: adversary-controlled sending or subscription triggers or supported campaign attribution; large message volume actually received by the target mailbox or mail path; and overdue discovery or handling of legitimate mail, a missed consequential notification, receiving or quota constraint, legitimate-message deferral or rejection, or disrupted business workflow. The first two layers without outcome remain a candidate. Message count or spam verdict alone does not confirm the technique.

zh：若 SMTP 网络链路或边界容量在消息事务形成前被淹没，归 T1498/NJT-0198；若附件解压、解析、CPU、线程、storage 或邮件应用崩溃是直接原因，归 T1499/NJT-0199。单封或批量 lure 的直接目的为点击/执行/凭据取得时归 Phishing；mail protocol 只承载 command/task/result 时归 C2；真实 MFA challenge 重复压力归 T1621/NJT-0175。相同事件可以共同映射，但 T1667 必须单独证明普通合法邮件或 mailbox workflow 的可用性损失。

en: SMTP network-link or boundary-capacity flooding before message transactions form belongs to T1498 or NJT-0198. Attachment decompression, parsing, CPU, worker, storage, or mail-application crash as the direct cause belongs to T1499 or NJT-0199. One or many lures intended to obtain clicks, execution, or credentials belong to Phishing. Mail protocol carrying only command, task, or result belongs to C2. Repetition pressure from genuine MFA challenges belongs to T1621 or NJT-0175. One incident can map to several techniques, but T1667 independently requires availability loss for ordinary legitimate mail or mailbox workflow.

### application_scenarios_and_threat_model

**application_scenarios**

zh：攻击者可用 bot 同时把一个员工地址提交给数千个无需 confirmed opt-in 的 newsletter/form，导致来自全球合法组织的确认和订阅邮件在数分钟至数小时内涌入；HHS 和 2016 .gov 事件证明这一路径可使 inbox 数日不可用。Storm-1811/相似集群还会先用数千 spam 消息让少数员工邮箱和注意力超载，再通过 Teams/电话冒充 help desk；后续社会工程独立归类。

en: An adversary can use a bot to submit one employee address simultaneously to thousands of newsletter or form endpoints without confirmed opt-in, causing confirmation and subscription mail from legitimate organizations worldwide to arrive within minutes or hours. HHS and the 2016 .gov incident establish that this path can make an inbox unusable for days. Storm-1811 and similar clusters first overload a few employees’ mailboxes and attention with thousands of spam messages and then impersonate help desk personnel over Teams or phone; the successor social engineering is classified separately.

zh：在关键消息埋没场景中，攻击者先或同时完成 account sign-in、联系信息更改、金融交易、online order 或其他会生成合法通知的动作，再启动/安排 bombardment，使 notification 在高密度时间线上超出用户或 workflow 的正常响应时限。只有实际 notification ID、delivery 和 response/outcome 可以关联时才确认这一 child；一般 urgency 或 vishing 不代替 burial 证据。

en: In a consequential-message-burial scenario, an adversary performs or accompanies an account sign-in, contact-information change, financial transaction, online order, or another action that generates a legitimate notification and starts or schedules bombardment so the notification exceeds the user’s or workflow’s normal response time in the dense timeline. This child is confirmed only when actual notification ID, delivery, and response or outcome can be joined. General urgency or vishing does not substitute for burial evidence.

**attacker_model**

zh：攻击者至少需要目标 email address 和可生成大量消息的机制。合法发送者扇出要求自动发现/维护缺少 live-user validation 的 signup forms，并承受 CAPTCHA、confirmed opt-in、provider rate limits、form abuse response 和发送方下架；关键消息同步还要求知道或控制会生成通知的账户/交易事件及其大致发送时点。攻击者不能保证所有邮件绕过 gateway、进入 Inbox、触发 quota 或让用户漏看；过高量也会迅速触发 recipient-centric 告警。

en: The adversary needs at least the target email address and a mechanism that generates large message volume. Legitimate-sender fan-out requires automated discovery or maintenance of signup forms lacking live-user validation and must contend with CAPTCHA, confirmed opt-in, provider rate limits, form-abuse response, and sender takedown. Consequential-message synchronization additionally requires knowledge or control of an account or transaction event that generates a notification and its approximate sending time. The actor cannot guarantee that all messages bypass the gateway, reach Inbox, trigger quota, or make the user miss a message. Excessive volume also quickly activates recipient-centric detection.

**defender_model**

zh：防守方可取得 MTA/message trace、Defender `EmailEvents`、raw authentication headers、mailbox message metadata/Graph state、MailItemsAccessed、mail-flow queue/receiving-limit/NDR、user report、business/security notification and acknowledgment，以及 approved bulk-mail context。应按 recipient、rolling time、unique authenticated sender/domain/IP、template cluster、first-contact、delivery location、folder/read/access state 和 workflow SLA 关联。只采集 blocked spam 会遗漏 delivered legitimate-source bomb；只看 message count 又无法证明 attention impact。

en: Defenders can obtain MTA or message trace, Defender `EmailEvents`, raw authentication headers, mailbox message metadata or Graph state, MailItemsAccessed, mail-flow queues, receiving limits and NDRs, user reports, business or security notifications and acknowledgments, and approved bulk-mail context. Correlation should use recipient, rolling time, unique authenticated sender, domain, IP, template cluster, first contact, delivery location, folder, read or access state, and workflow SLA. Collecting only blocked spam misses delivered legitimate-source bombs, while message count alone cannot prove attention impact.

### stealth_mechanisms

**`NM-ST` primary — 高密度邮件在时间和来源上稀释合法消息显著性 / Dense mail across time and sources dilutes legitimate-message salience**

zh：攻击者把轰炸拆成大量独立邮件并集中到目标 recipient，合法 security/transaction/business message 成为同一时间窗中的少数事件。任何单 sender、domain、IP 或短内容簇只占局部，用户和 source-centric detector 难以从全量中恢复高价值消息；recipient fan-in、message timeline 与 workflow outcome 能重新建立整体。HHS 直接说明 mail bombs 用于埋没 sign-in、contact、financial 和 order 通知，Krebs 记录多源流量使邮箱无法用于真实邮件。证据 `TA0040-T1667-REF-HHS`、`TA0040-T1667-REF-KREBS`; confidence high。

en: The adversary divides bombing into many individual messages converging on a target recipient, leaving a legitimate security, transaction, or business message as a small minority in the same time window. Any single sender, domain, IP, or short content cluster contributes only a local part, making the high-value message difficult to recover from the whole for a user or source-centric detector. Recipient fan-in, message timeline, and workflow outcome restore the aggregate. HHS directly states that mail bombs bury sign-in, contact, financial, and order notifications, while Krebs records multi-source traffic making mailboxes unusable for real mail. Evidence is `TA0040-T1667-REF-HHS` and `TA0040-T1667-REF-KREBS`; confidence high.

**`NM-FD` secondary — 真实第三方邮件认证与正常模板掩盖共同恶意触发 / Genuine third-party authentication and ordinary templates disguise a common malicious trigger**

zh：registration bomb 让各第三方 sender 按正常业务系统生成 confirmation/newsletter，message 可通过 SPF/DKIM/DMARC 并拥有正常 From、template 和 sending infrastructure；被替换的是订阅请求的 owner/consent，而不是每封邮件的发送真实性。按 sender reputation 或 spoof detection 的守方会把它们视为互不相关的良性 bulk mail。异常 first-contact 扇出、共同 recipient、接近的 received time 和 signup-abuse reports 可破坏伪装。证据 `TA0040-T1667-REF-HHS`、`TA0040-T1667-REF-RAPID7`; confidence high。

en: A registration bomb causes each third-party sender to generate confirmation or newsletter mail through its normal business system. Messages can pass SPF, DKIM, or DMARC and carry ordinary From identities, templates, and sending infrastructure; ownership or consent for the signup request changes rather than authenticity of each delivery. A defender relying on sender reputation or spoof detection sees unrelated benign bulk mail. Anomalous first-contact fan-out, a shared recipient, nearby receive time, and signup-abuse reports break the disguise. Evidence is `TA0040-T1667-REF-HHS` and `TA0040-T1667-REF-RAPID7`; confidence high.

### subtechnique_taxonomy

zh：合法发送者扇出式收件箱洪泛按 delivery agency 和 source topology 划分：攻击者利用大量独立第三方发送者，让攻击关系只在 recipient fan-in 处闭合。关键消息埋没同步按 bombing window 与一个可识别的 consequential notification/外部事件之间的时间与业务关系划分：检测必须从邮件平面跨到 identity、finance、order、ticket 或 security workflow。前者即使没有特定被埋消息也可造成 inbox 不可用，后者可由直接 spam source 实现而不要求多源扇出；二者可共现但防御不可互换。

en: Legitimate-Sender Fan-Out Inbox Flooding is divided by delivery agency and source topology: the adversary uses many independent third-party senders so the attack relationship closes only at recipient fan-in. Consequential-Message Burial Synchronization is divided by the temporal and business relationship between a bombing window and an identifiable consequential notification or external event, requiring detection to cross from mail into identity, finance, order, ticket, or security workflow. The first can make an inbox unusable without one particular buried message, while the second can use a direct spam source without multi-source fan-out. They can co-occur but their defenses are not interchangeable.

zh：direct mass mail、attachment、zip、reply-all、client、server、sender type、message language 和目标部门不构成 NJS。低速长期积累与 alias expansion 因证据不足 defer。ATT&CK 无子项，分类不按邮件类型或产品补配额。

en: Direct mass mail, attachment, zip, reply-all, client, server, sender type, message language, and target department do not define NJS. Low-rate long-term accumulation and alias expansion remain deferred for insufficient evidence. ATT&CK has no children, and the taxonomy does not create quota-filling partitions by mail type or product.

### defense / evidence / limitations

- detection: create `TA0040-T1667-DET-MAIL-FANIN-IMPACT` with three analytics in section 7.
- mitigation: create `TA0040-T1667-MIT-RECIPIENT-CENTRIC-CONTINUITY` with parent and child applications.
- claim keys: `TA0040-T1667-CLM-PARENT`, `TA0040-T1667-CLM-FANOUT`, `TA0040-T1667-CLM-BURIAL`, `TA0040-T1667-CLM-BOUNDARY`, `TA0040-T1667-CLM-DEFENSE`.
- case keys: `TA0040-T1667-CASE-GOV-REGISTRATION-BOMB`, `TA0040-T1667-CASE-STORM1811-HELPDESK`.

zh：HHS 提供父行为、registration bomb、legitimate-source difficulty、具体被埋通知类别和 mitigation 的政府结论；Rapid7/Sophos 提供实际 MDR 事件链；Krebs 记录 2016 .gov 事件与 mailbox unusability。公开来源没有提供逐封 raw trace、用户完整阅读历史和业务 SLA，因此正式案例不能声称每个合法消息都被漏看。Graph `isRead`、MailItemsAccessed 和 workflow acknowledgment 都有可见性/隐私限制；用户未读不自动等于 bombing 造成。

en: HHS supplies government conclusions for the parent behavior, registration bombs, difficulty of blocking legitimate sources, categories of buried notifications, and mitigation. Rapid7 and Sophos provide direct MDR incident chains, while Krebs records the 2016 .gov event and mailbox unusability. Public sources do not publish per-message raw traces, complete user reading history, or business SLAs, so cases cannot claim every legitimate message was missed. Graph `isRead`, MailItemsAccessed, and workflow acknowledgment each have visibility and privacy limits; unread status does not automatically mean bombing caused it.

## 5. 子技术完整双语字段草稿

### 5.1 合法发送者扇出式收件箱洪泛 / Legitimate-Sender Fan-Out Inbox Flooding

**summary**

- zh：攻击者让大量真实第三方发送系统分别向同一目标投递正常外观邮件，使 source-local 过滤难以识别，而 recipient fan-in 埋没合法通信。
- en: The adversary causes many genuine third-party sending systems to deliver ordinary-looking mail independently to one target, defeating source-local filtering while recipient fan-in buries legitimate communication.

**definition_and_concept**

zh：合法发送者扇出式收件箱洪泛是攻击者自动把目标地址提交给大量 newsletter、registration、contact 或 transactional forms，使彼此独立的第三方发送系统生成邮件并在目标邮箱汇聚。稳定变量是攻击者把 delivery agency 分散给正常发送者；每封邮件可以真实、通过认证且符合发送者模板，但 signup intent/consent 是恶意伪造的。

en: Legitimate-Sender Fan-Out Inbox Flooding occurs when an adversary automatically submits a target address to many newsletter, registration, contact, or transactional forms, causing independent third-party sending systems to generate mail that converges on the target mailbox. The stable variable is dispersing delivery agency across normal senders. Each message can be genuine, authenticated, and consistent with sender templates while signup intent or consent is maliciously fabricated.

zh：子项不由 newsletter 产品、SPF/DKIM pass、域名数量或使用 bot 本身定义；必须证明跨来源汇聚与目标 mailbox/legitimate-mail impact。一个被攻陷 bulk sender 对目标直接发大量邮件留父级核心，除非还存在真实多发送者扇出。合法 sender 不自动成为攻击者基础设施或受陷组织。

en: The child is not defined by newsletter product, SPF or DKIM pass, domain count, or bot use alone. It requires proof of cross-source convergence and target mailbox or legitimate-mail impact. One compromised bulk sender directly sending high volume remains parent core unless genuine multi-sender fan-out also exists. A legitimate sender does not automatically become adversary infrastructure or a compromised organization.

**stealth_characteristics**

zh：**合法发送者扇出式收件箱洪泛**把同一攻击分拆到大量 From/MAIL FROM domain、sending IP、ASN、template 和 mail flow。每个 sender 的单收件人量可能低、认证结果正常、IP reputation 良好；DMARC/anti-spoofing 因此不能识别共同恶意 consent。攻击只在 recipient address、相近时间、first-contact 激增、unique authenticated sender fan-in 和 signup template clusters 上形成完整图像。

en: **Legitimate-Sender Fan-Out Inbox Flooding** splits one attack across many From and MAIL FROM domains, sending IPs, ASNs, templates, and mail flows. Each sender’s volume to the recipient can be low, authentication can pass, and IP reputation can be good, so DMARC or anti-spoofing cannot identify shared malicious consent. The complete attack appears only in recipient address, nearby time, first-contact growth, unique authenticated-sender fan-in, and signup-template clusters.

zh：残余还包括 form/provider abuse time、confirmation/welcome semantics、message trace、`EmailClusterId`、bulk complaint level、delivery location、user report 和 unsubscribe/cleanup workload。confirmed opt-in 与 CAPTCHA 会阻止未授权订阅，但 confirmation email 本身仍可能成为洪泛；发送者不共享 request ID、数据跨组织不可得和隐私限制是主要盲区。

en: Residual evidence also includes form or provider abuse time, confirmation or welcome semantics, message trace, `EmailClusterId`, bulk complaint level, delivery location, user report, and unsubscribe or cleanup workload. Confirmed opt-in and CAPTCHA prevent unauthorized subscription, although confirmation mail itself can still be flooded. Senders do not share one request ID, cross-organization data may be unavailable, and privacy constraints create principal blind spots.

**scope_boundary_definition**

zh：纳入多个独立 legitimate senders 对同一 recipient 的异常 fan-in，且目标合法邮件可发现性、mailbox receiving 或处理工作流实际受损。只有域认证 pass、多 first contacts 或 newsletter subjects 不足；需要 recipient-level volume/impact。伪造大量 sender 字符串但实际来自一个基础设施属于 direct mass mail parent-core，认证失败 spoof campaign 也不自动进入本 child。

en: Include anomalous fan-in from multiple independent legitimate senders to one recipient when discoverability of legitimate mail, mailbox receiving, or handling workflow is actually impaired. Authentication pass, many first contacts, or newsletter subjects alone are insufficient and need recipient-level volume and impact. Many forged sender strings from one infrastructure remain direct mass-mail parent core, and an authentication-failing spoof campaign does not automatically enter this child.

zh：合法营销峰值、员工新订阅、role mailbox、conference registration、邮件迁移、供应商通知和 reply-all accident 是反例。若大量第三方消息全被 quarantine/junk 且普通邮件、配额和用户工作流未受影响，只能标记 attempted fan-out。

en: Legitimate marketing peaks, employee subscriptions, role mailboxes, conference registration, mail migration, vendor notifications, and reply-all accidents are counterexamples. If all third-party messages are quarantined or junked and ordinary mail, quota, and user workflow remain unaffected, classify only attempted fan-out.

**application_scenarios_and_threat_model**

zh：2016 年攻击者把超过一百个 .gov 地址加入大量 mailing lists；一些地址被注册到近一万个 customer lists，邮件从大量不同来源到达，使 mailbox 无法用于真实邮件。Rapid7 2024 案例观察到 newsletter confirmation 来自全球合法组织并成功穿过已有 email protection 进入 inbox，随后攻击者以 IT 支持身份联系被压垮的用户。后续 remote access 不属于本 child 的结果。

en: In 2016, attackers added more than one hundred .gov addresses to many mailing lists; some addresses were signed up for nearly ten thousand customer lists, and mail from many different sources made mailboxes unusable for real mail. Rapid7’s 2024 incidents observed newsletter confirmations from legitimate organizations worldwide bypassing existing email protection and reaching inboxes before actors contacted overwhelmed users while posing as IT support. The later remote access is not an outcome of this child.

zh：攻击者需要目标地址、自动化表单发现/提交和足够多缺少 consent validation 的发送服务。发送方 CAPTCHA、confirmed opt-in、per-IP/device/account/form limits、abuse sharing 和 recipient provider 的 fan-in quarantine 会提高成本。防守方须保留 recipient-centric delivery history，并把 authentication pass 视为 sender authenticity 而非 signup authorization；若只能看到单个 sender，无法证明 fan-out。

en: The adversary needs the target address, automated form discovery or submission, and enough sending services without consent validation. Sender-side CAPTCHA, confirmed opt-in, per-IP, device, account, or form limits, abuse sharing, and recipient-provider fan-in quarantine raise cost. Defenders must retain recipient-centric delivery history and treat authentication pass as sender authenticity rather than signup authorization. Seeing one sender alone cannot establish fan-out.

**mechanisms / defense / limitations**

- `NM-ST` primary: 多个低贡献发送者在目标邮箱汇聚 / Low-contribution senders converge at the target mailbox; evidence HHS/Krebs; high.
- `NM-FD` secondary: 真实 sender authentication 与正常模板掩盖恶意 signup intent / Genuine sender authentication and ordinary templates disguise malicious signup intent; evidence HHS/Rapid7; high.
- detection: `TA0040-T1667-NJA-RECIPIENT-FANIN-BURIAL`。
- mitigation: new MIT dedicated child application。

zh：HHS、Krebs 和 Rapid7 直接支持来源分散、legitimate messages 和 mailbox impact；公开资料不提供统一 sender independence 判据。共享 ESP/CDN 可能让多个域共用 IP，反之一个组织可能使用多个域，因此正式检测应把 domain、DKIM/From、connector、template cluster 和 owner 组合，不能用 unique IP 数替代。

en: HHS, Krebs, and Rapid7 directly support source dispersion, legitimate messages, and mailbox impact, but public evidence does not define one universal sender-independence test. Shared ESPs or CDNs can place many domains on one IP, while one organization may use several domains, so formal detection should combine domain, DKIM or From identity, connector, template cluster, and owner rather than substituting unique IP count.

### 5.2 关键消息埋没同步 / Consequential-Message Burial Synchronization

**summary**

- zh：攻击者把邮件轰炸窗口与一个安全、账户、交易或业务事件同步，使相应合法通知虽正常投递却超出用户或流程的正常发现和处置时限。
- en: The adversary synchronizes an email-bombing window with a security, account, transaction, or business event so the corresponding legitimate notification is delivered normally but exceeds normal user or workflow discovery and handling time.

**definition_and_concept**

zh：关键消息埋没同步是攻击者围绕自己知道、触发或利用的 consequential event 安排大量邮件，并使该事件的合法 notification 在同一 mailbox timeline 中失去显著性或处理优先级。稳定变量是 bombing 与一个可识别 business/security notification 的时间和因果关系，而不是 message subject、finance vertical 或收件客户端。

en: Consequential-Message Burial Synchronization occurs when an adversary arranges large mail volume around a consequential event the actor knows, triggers, or exploits, causing the event’s legitimate notification to lose salience or processing priority in the same mailbox timeline. The stable variable is the temporal and causal relationship between bombing and an identifiable business or security notification, not message subject, financial vertical, or mail client.

zh：子项要求通知本身确实生成并交付，以及用户/流程响应相对同类基线或明确 SLA 实际延迟、遗漏或未能阻止后继结果。轰炸与事件时间相近但没有 notification mapping，或 notification 按时被其他通道处置，只能保持 hypothesis；高量和未读标志不能单独证明 attacker synchronization。

en: The child requires proof that the notification was generated and delivered and that user or workflow response was actually delayed, missed, or failed to stop a later outcome relative to the same notification class baseline or an explicit SLA. Nearby bombing and event time without notification mapping, or timely handling through another channel, remains a hypothesis. Volume and unread state alone do not prove adversary synchronization.

**stealth_characteristics**

zh：**关键消息埋没同步**不需要删除、篡改或移动目标通知。安全 alert、sign-in notice、contact change、financial transaction detail 或 order confirmation 可保持正确 sender/authentication/contents，却被相邻低价值 messages 稀释，导致用户 notification center、Focused/Other 分类、移动同步和人工 triage 超载。Mail gateway 看见正常投递，业务系统看见正常 notification send，任何单面都无法解释缺失响应。

en: **Consequential-Message Burial Synchronization** does not require deleting, altering, or moving the target notification. A security alert, sign-in notice, contact change, financial transaction detail, or order confirmation can retain correct sender, authentication, and content while adjacent low-value messages dilute it, overloading user notification centers, Focused or Other classification, mobile synchronization, and human triage. The mail gateway sees successful delivery and the business system sees successful notification send; neither plane alone explains the missing response.

zh：可恢复痕迹包括 event/transaction ID、notification job ID、message ID、send/received/delivery time、folder/isRead/lastModified 或 MailItemsAccessed、expected acknowledgment、实际处理结果，以及 bombing window 的 recipient fan-in。不同系统缺少共同 ID 时只可按 recipient、时间、notification class 和 expected sender 概率关联，须显式保留 uncertainty。

en: Recoverable traces include event or transaction ID, notification job ID, message ID, send, receive, and delivery time, folder, isRead, lastModified, or MailItemsAccessed, expected acknowledgment, actual handling result, and recipient fan-in during the bombing window. When systems lack one common identifier, only probabilistic correlation by recipient, time, notification class, and expected sender is possible and uncertainty must remain explicit.

**scope_boundary_definition**

zh：纳入 bombing window 与具体 consequential event/notification 的闭合关系及超时或损失结果。一般 spam flood 使 inbox unusable 由 parent/child 1 表达；只有攻击者利用特定通知埋没这一变量时进入本 child。邮箱 rule 删除/移动通知属于另一 hiding/data-manipulation 行为，不能用 T1667 替代。

en: Include a closed relationship between a bombing window and a concrete consequential event or notification plus overdue or loss outcome. A general spam flood making an inbox unusable is covered by the parent or child 1. This child applies only when the adversary exploits burial of a particular notification. A mailbox rule deleting or moving the notification is another hiding or data-manipulation behavior and is not replaced by T1667.

zh：用户夜间/休假、通知 fatigue、业务系统未发送、sender delay、mail rule、quarantine、客户端离线和 alternate-channel acknowledgment 是反例或替代解释。Phishing/vishing 在轰炸后利用 urgency 但没有被埋 message 时不属于本 child。

en: User nighttime or leave, notification fatigue, business-system failure to send, sender delay, mail rules, quarantine, offline clients, and alternate-channel acknowledgment are counterexamples or alternative explanations. Phishing or vishing exploiting urgency after bombing without a buried message does not belong to this child.

**application_scenarios_and_threat_model**

zh：HHS 明确指出攻击者用 mail bomb 使受害者错过 account sign-in attempts、contact-information updates、financial transactions 和 online-order confirmations。一个受约束场景是攻击者控制账户完成交易后，在预期通知前后发动 registration bomb；notification 正常到达，但用户在定义的响应 SLA 内没有访问/处置，交易继续。该场景的正式 case 只能在实际 incident evidence 存在时创建，本 handoff 不凭通用 HHS 结论填造受害者案例。

en: HHS explicitly states that actors use mail bombs so victims miss account sign-in attempts, contact-information updates, financial transactions, and online-order confirmations. A bounded scenario is an actor controlling an account, completing a transaction, and launching a registration bomb around the expected notification. The notification arrives normally, but the user does not access or handle it within the defined response SLA and the transaction continues. A formal case for this scenario requires actual incident evidence; this handoff does not fabricate a victim case from general HHS guidance.

zh：攻击者需要知道 notification recipient 和大致时点，并能触发或预测 underlying event；随机轰炸无法稳定同步。out-of-band alerts、mobile push/app inbox、trusted-sender priority、transaction hold、independent confirmation 和 recipient-centric bombing response 会削弱效果。防守方需要业务/身份/安全系统把 notification ID 或安全摘要传播到 mail trace，并按 notification class 建立正常 deliver-to-access/acknowledge 基线；没有这些字段时只能生成 burial risk。

en: The adversary needs the notification recipient and approximate timing and must trigger or predict the underlying event; random bombing cannot reliably synchronize. Out-of-band alerts, mobile push or app inbox, trusted-sender priority, transaction holds, independent confirmation, and recipient-centric bombing response reduce the effect. Defenders need business, identity, or security systems to propagate a notification ID or safe digest into mail trace and maintain normal deliver-to-access or acknowledgment baselines by notification class. Without these fields, only burial risk can be produced.

**mechanism / defense / limitations**

- mechanism: `NM-ST` primary; summary zh：轰炸窗口稀释关键通知并拉长响应；en: The bombing window dilutes a consequential notification and lengthens response; evidence HHS; confidence medium.
- detection: `TA0040-T1667-NJA-CONSEQUENTIAL-MESSAGE-BURIAL`。
- mitigation: new MIT with alternate-path/priority application。

zh：HHS 结论直接支持被埋消息类别和攻击目的，却没有发布一笔带完整 notification/message/read/business-outcome 链的原始案例。因此 child 存在性为 medium，具体事件必须按数据闭合；没有共同 ID、read evidence 或 SLA 时不得从时间邻近宣称 burial confirmed。

en: HHS directly supports the categories of buried messages and adversary purpose but does not publish one incident with a complete notification, message, read, and business-outcome chain. Child existence is therefore medium confidence, and each event requires data closure. Without common identifier, read evidence, or SLA, temporal proximity cannot establish confirmed burial.

## 6. 来源与证据账本

### 复用现有 Reference

- `REF-000609`，**reuse + extend locator/notes**：同一 Microsoft Defender XDR `EmailEvents` source；为 T1667 使用 `NetworkMessageId`, sender domains/IP, recipient, `EmailClusterId`, delivery action/location, authentication, BCL, size, first contact 等字段。
- `REF-000567`，**reuse unchanged**：MailItemsAccessed 的 Sync/Bind 语义和 offline reread blind spot；支持 message-access evidence 的限制，不能把无 audit 当成未读。

### 新 Reference 候选

| 临时键 | 来源 | 支持结论 |
|---|---|---|
| `TA0040-T1667-REF-ATTACK` | MITRE ATT&CK Enterprise 19.1 T1667, `https://attack.mitre.org/versions/v19/techniques/T1667/` | 父行为、Impact、无 ATT&CK 子项、Storm-1811、基础 mitigation/detection 线索。 |
| `TA0040-T1667-REF-HHS` | HHS HC3, Defense and Mitigations from E-mail Bombing, `https://www.hhs.gov/sites/default/files/email-bombing-sector-alert-tlpclear.pdf` | legitimate transaction/security burial、registration bomb、numerous legitimate sources、mailbox unusability、confirmed opt-in/CAPTCHA。 |
| `TA0040-T1667-REF-KREBS` | KrebsOnSecurity, Massive Email Bombs Target .Gov Addresses, `https://krebsonsecurity.com/2016/08/massive-email-bombs-target-gov-addresses/` | 100+ .gov targets、near-10,000 lists、multi-source blocking difficulty、mailbox unusability and cleanup burden；secondary incident reporting。 |
| `TA0040-T1667-REF-RAPID7` | Rapid7, Ongoing Social Engineering Campaign Linked to Black Basta Ransomware Operators, `https://www.rapid7.com/blog/post/2024/05/10/ongoing-social-engineering-campaign-linked-to-black-basta-ransomware-operators/` | direct MDR cases: legitimate newsletter confirmation from many organizations overwhelmed protection/inbox, followed by vishing。 |
| `TA0040-T1667-REF-SOPHOS` | Sophos MDR, Email bombing and Teams vishing, `https://www.sophos.com/en-us/blog/sophos-mdr-tracks-two-ransomware-campaigns-using-email-bombing-microsoft-teams-vishing` | 15+ incidents, up to 3,000 messages in under an hour, one case 3,000 in 45 minutes, targeted few users and urgency。 |
| `TA0040-T1667-REF-MS-GRAPH-MESSAGE` | Microsoft Graph message resource, `https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0` | `internetMessageId`, `receivedDateTime`, `isRead`, `lastModifiedDateTime`, `parentFolderId`, importance/inference classification and delta/change notifications。 |
| `TA0040-T1667-REF-MS-RECEIVE-LIMITS` | Microsoft, Mailboxes exceeding receiving limits report, `https://learn.microsoft.com/en-us/exchange/monitoring/mail-flow-reports/mailboxes-exceeding-receiving-limits-report` | hot/SRP/warm limits, warm risk at 1,000 messages per rolling hour, blocking effect。 |
| `TA0040-T1667-REF-MS-MESSAGE-TRACE` | Microsoft Graph `exchangeMessageTrace`, `https://learn.microsoft.com/graph/api/resources/exchangemessagetrace` | fromIP, messageId, receivedDateTime, recipient, sender, size, status, subject and delivery lifecycle。 |
| `TA0040-T1667-REF-MS-NDR` | Microsoft Exchange Online NDR/SMTP errors, `https://learn.microsoft.com/en-us/Exchange/mail-flow-best-practices/non-delivery-reports-in-exchange-online/non-delivery-reports-in-exchange-online` | recipient thread limit, queue expiration, enhanced status and delivery failure evidence。 |

### Claim 候选

- `TA0040-T1667-CLM-PARENT`：大量邮件只有在造成合法邮件埋没、处理/投递困难或 mailbox/business interruption 时完成 T1667；ATT&CK/HHS。
- `TA0040-T1667-CLM-FANOUT`：registration bomb 可利用大量 legitimate senders，单源真实性与共同 malicious consent 分离；HHS/Krebs/Rapid7。
- `TA0040-T1667-CLM-BURIAL`：攻击者可用 bombing 埋没 sign-in/contact/financial/order/security notifications；HHS，medium。
- `TA0040-T1667-CLM-BOUNDARY`：resource exhaustion、network flood、phishing/C2/MFA bombing 与 mail-attention outcome 按直接对象区分；相邻 NJT/ATT&CK。
- `TA0040-T1667-CLM-DEFENSE`：recipient fan-in、message access/workflow acknowledgment、mail queue/receiving limits 是三条互补 outcome gate；Microsoft schemas + HHS。

### Case 候选

- `TA0040-T1667-CASE-GOV-REGISTRATION-BOMB`：2016-08，超过 100 个 .gov 地址被大量 lists 集中订阅；部分地址接近一万个 customer lists，邮件来自众多不同来源并使邮箱数日无法处理真实邮件。subject refs parent + legitimate-sender child；来源 HHS/Krebs，confidence medium。
- `TA0040-T1667-CASE-STORM1811-HELPDESK`：2024，Rapid7/Sophos 多个 MDR customer incidents；legitimate newsletter confirmations/大量 spam 进入少数用户 inbox，一例 45 分钟超过 3,000 封，随后外部 Teams/电话冒充 help desk。case 对 parent/fan-out 与 precursor boundary 有效；不自动支持 consequential-message child。

关键消息埋没 child 当前 `case_refs: []`；HHS 支持一般结论，不能制造具体受害者案例。

## 7. 可实施 Detection Strategy 与 Analytics

### `TA0040-T1667-DET-MAIL-FANIN-IMPACT` — 收件人邮件扇入至合法通信影响谱系 / Recipient Mail Fan-In to Legitimate-Communication Impact Lineage

**objective:** recipient-first 检测并分级输出 `bomb_candidate`、`mailbox_attention_impacted`、`mail_delivery_impacted` 和 `consequential_message_buried`。不从高量直接确认；至少一个 Analytic 必须闭合 legitimate-message/workflow/service outcome。覆盖 parent 和两个 children，domains `[enterprise]`。

#### `TA0040-T1667-NJA-RECIPIENT-FANIN-BURIAL`

**name:** 多发送者扇入—收件箱积压—合法消息访问差分 / Multi-Sender Fan-In–Inbox Backlog–Legitimate-Message Access Differential。

**platforms:** `[Office Suite, SaaS]`。

**logic:** 以 `RecipientEmailAddress` 为主键，在 rolling 15 分钟和 60 分钟窗口统计 delivered+junked messages、unique From/MAIL FROM domains、sending IP/ASN、DKIM domains、`EmailClusterId`、first-contact、authentication-pass share、delivery location 和 total bytes，并与同 recipient/role/weekday-hour 的前 30 天基线比较。工程初值为 `>=250 messages/15m` 或 `>=1000 messages/rolling hour`，同时满足 recipient 99.9 percentile；这些阈值用于候选，不是恶意结论。fan-out child 进一步要求至少 20 个独立 sender-owner/domain groups、正常/通过认证占较高比例或 signup/confirmation cluster evidence。然后检查 bombardment 前后正常 trusted/business messages 的 folder/isRead/MailItemsAccessed/acknowledgment 和 user report；只有合法消息的 access/handling 超出 class SLA 或 mailbox backlog 实际阻断工作时输出 impact。

**data requirements:**

- `mail-delivery-events`: channel `Microsoft Defender XDR EmailEvents or equivalent`; fields `Timestamp`, `NetworkMessageId`, `InternetMessageId`, `SenderMailFromAddress`, `SenderFromAddress`, `SenderMailFromDomain`, `SenderFromDomain`, `SenderIPv4`, `SenderIPv6`, `RecipientEmailAddress`, `Subject`, `EmailClusterId`, `EmailDirection`, `DeliveryAction`, `DeliveryLocation`, `AuthenticationDetails`, `BulkComplaintLevel`, `EmailSize`, `IsFirstContact`, `Connectors`。
- `mailbox-message-state`: channel `Microsoft Graph message/delta or provider equivalent`; fields `mailbox_id`, `message_id`, `internet_message_id`, `received_date_time`, `is_read`, `last_modified_date_time`, `parent_folder_id`, `importance`, `inference_classification`。
- `mail-access-audit`: channel `MailItemsAccessed or equivalent`; fields `event_time`, `mailbox_id`, `internet_message_id_or_folder`, `operation`, `session_id`, `client_ip`, `access_type`, `result`。
- `mailbox-role-and-impact`: fields `mailbox_id`, `owner`, `role`, `critical_sender_or_class`, `expected_handling_sla`, `user_report_time`, `backlog_count`, `business_outcome`。

**observables:** recipient fan-in from many new authenticated senders; signup/confirmation clusters across unrelated owners; legitimate trusted message delivered during burst but not accessed/handled beyond SLA; user reports mailbox unusable and backlog growth.

**correlation:** 15-minute burst, rolling 60-minute receiving-limit view, 30-day baseline; continue message-access/acknowledgment observation to configured SLA or 24 hours. Dimensions `recipient`, `sender_owner/domain`, `dkim_domain`, `sender_ip/asn`, `email_cluster`, `message_id`, `folder`, `notification_class`, `time`。

**false positives:** approved campaigns, HR/company announcements, incident alert storms, ticket or monitoring bursts, conference registration, new employee onboarding, mailbox migration/import, mailing-list loop, reply-all accident.

**blind_spots:** messages blocked before retained trace, personal/external mailboxes, Graph/isRead collection not permitted, offline client reads, MailItemsAccessed license/Sync semantics, aliases not normalized, shared role mailbox with many legitimate senders, sender-owner mapping absent.

**tuning:** normalize aliases only where provider rules are known; baseline role mailboxes separately; derive sender owner from authenticated domains/connectors/template clusters, not unique IP alone. Require an impact outcome for severity. Protect privacy by storing message identifiers and categories rather than bodies unless incident policy authorizes content review.

#### `TA0040-T1667-NJA-CONSEQUENTIAL-MESSAGE-BURIAL`

**name:** 关键事件—通知消息—轰炸窗口—响应结果关联 / Consequential Event–Notification Message–Bombing Window–Response Outcome Correlation。

**platforms:** `[Office Suite, SaaS]`。

**logic:** 从 identity/security/finance/order/ticket system 取得 consequential event 和 notification job；优先用 `notification_id`/safe digest 映射 `NetworkMessageId`/InternetMessageId，缺少共同 ID 时按 exact recipient、expected sender、notification class 和 narrow time 做低置信关联。比较 bombing 从通知前 10 分钟到后 30 分钟的 message density，验证 notification delivered location，再检查 user/message access、workflow acknowledgment、transaction hold/cancel 和最终 outcome。只有 notification 已交付、bomb window 存在且响应超过明确 SLA 或同类消息前 30 日 p95 的两倍（上限 24 小时），并有未处置后果/用户报告时输出 confirmed burial。其他情况输出 burial risk。

**data requirements:**

- `consequential-event`: fields `event_time`, `event_id`, `event_type`, `subject_or_account_id`, `recipient_email`, `criticality`, `action`, `risk`, `outcome`。
- `notification-job`: fields `notification_id`, `event_id`, `recipient_email`, `notification_class`, `expected_sender`, `generated_time`, `send_time`, `message_id_or_safe_digest`, `required_ack`, `ack_sla`。
- `mail-delivery-and-access`: fields from prior analytic plus `delivery_time`, `latest_delivery_location`, `is_read`, `access_time`, `folder_id`。
- `workflow-response`: fields `event_id`, `notification_id`, `ack_time`, `actor`, `channel`, `hold_or_cancel_time`, `case_id`, `final_outcome`。

**observables:** notification generated from sign-in/contact/financial/order/security event and delivered inside a bomb window; corresponding message remains unaccessed beyond normal class SLA; account/transaction action continues without expected hold/cancel; user later reports missing alert amid flood.

**correlation:** bomb window `event/notification -10m` to `+30m`; response window configured SLA or `2 × 30-day p95`, capped at 24h. Dimensions `event_id`, `notification_id`, `recipient`, `message_id`, `notification_class`, `expected_sender`, `bomb_window_id`, `case_id`, `time`。

**false positives:** user leave/nighttime, acknowledged alternate-channel push/SMS, legitimate notification storm after a major incident, failed notification generation, provider delivery delay, mailbox rule/quarantine, user intentionally ignores low-priority alert.

**blind_spots:** notification system does not emit message ID, provider hides read/access, privacy prevents mailbox state, alternate personal channel invisible, multiple users share mailbox, adversary changes notification destination before bombing.

**tuning:** define notification classes and SLA with business owner; alternate-channel acknowledgment cancels burial confirmation. Do not use subject keyword alone or assume every unread security email is impact. Require exact ID for high confidence; probabilistic joins remain medium/low and cannot drive irreversible response alone.

#### `TA0040-T1667-NJA-MAIL-TRANSPORT-MAILBOX-AVAILABILITY`

**name:** 邮件传输队列—邮箱接收限制—合法投递结果关联 / Mail Transport Queue–Mailbox Receiving Limit–Legitimate Delivery Outcome Correlation。

**platforms:** `[Office Suite, Mail Server]`。

**logic:** 按 recipient/mailbox/server 计算 accepted、delivered、pending、failed、quarantined、filtered-as-spam、deferred 和 NDR；连接 MTA queue age/length、recipient thread limit、receive limit/quota、mailbox delivery latency 和 client sync. Candidate volume 必须与合法 sender/message class 的 delivery delay、`432 4.3.2 recipient thread limit exceeded`、hot-limit block、queue expiry 或 mailbox workflow unavailable 相连，才输出 `mail_delivery_impacted`。若 CPU/storage/parser 是直接瓶颈，路由到 NJT-0199；若 SMTP network capacity 是瓶颈，路由 NJT-0198。

**data requirements:**

- `message-trace`: channel `Exchange message trace or equivalent`; fields `trace_id`, `message_id`, `received_date_time`, `sender_address`, `recipient_address`, `from_ip`, `size`, `status`, `subject`, `event_time`, `delivery_latency`。
- `mta-queue`: channel `Exchange Queue Viewer, Postfix/Sendmail logs, or provider queue`; fields `event_time`, `server_id`, `queue_id`, `message_id`, `sender`, `recipient`, `date_received`, `status`, `defer_reason`, `expiration_time`, `last_error`, `size`。
- `mailbox-receiving-state`: fields `event_time`, `mailbox_id`, `rolling_receive_count`, `warm_limit`, `hot_limit`, `sender_recipient_limit`, `quota_used`, `quota_limit`, `thread_limit`, `sync_latency`。
- `smtp-delivery-result`: fields `event_time`, `message_id`, `recipient`, `smtp_status`, `enhanced_status_code`, `dsn_type`, `attempt_count`, `final_result`。
- `mail-service-health`: fields `event_time`, `service_id`, `accept_latency`, `delivery_latency`, `active_queue_length`, `defer_count`, `reject_count`, `health_status`。

**observables:** mailbox reaches provider receiving-limit risk/block state; legitimate mail remains pending/deferred or rejected during bombardment; recipient thread-limit NDRs rise; queue age/length and delivery latency increase for the targeted mailbox; service returns after quarantine/volume controls.

**correlation:** operational window 5 minutes for queue/limit changes, 15 minutes for recipient burst, 60 minutes for rolling receive limits, 24 hours for queue expiry/recovery. Dimensions `mailbox_id`, `recipient`, `message_id`, `queue_id`, `server_id`, `sender_class`, `smtp_status`, `limit_type`, `time`。

**false positives:** migration/import, backup restore, journaling duplication, approved campaigns, monitoring/ticket storm, connector failure, network/firewall change, recipient misconfiguration, mailbox quota neglect.

**blind_spots:** SaaS provider does not expose queues or numeric limits, delayed message trace (5–30 minutes), messages dropped before trace, client sync telemetry absent, shared infrastructure aggregates targets, NDR suppressed.

**tuning:** use provider warm/hot limit as availability context, not a maliciousness threshold. Start early warning near 1,000 messages/rolling hour where applicable and lower for critical individual mailboxes, but confirm with delivery/handling impact. Separate one-recipient impact from server-wide resource exhaustion.

## 8. Mitigation 设计

### `TA0040-T1667-MIT-RECIPIENT-CENTRIC-CONTINUITY` — 收件人中心的邮件准入与关键通信连续性 / Recipient-Centric Mail Admission and Critical-Communication Continuity

**measures**

1. `confirmed-consent-and-bot-resistant-signup`：对 newsletter/contact/registration forms 使用 confirmed opt-in、CAPTCHA/等价 bot challenge、per-source/device/account/address rate、abuse telemetry 和 rapid unsubscribe；confirmation resend 也须限速。`preventive`。
2. `recipient-fanin-admission`：recipient provider 按 rolling recipient volume、unique authenticated sender/owner、first-contact、template cluster、BCL 和 mailbox role 做 adaptive throttle/quarantine；新 bulk senders 先入临时 review，不永久 block 整个 ESP/domain。`preventive`。
3. `critical-message-priority-and-alternate-path`：为 security/account/finance/order/incident notifications 传播 notification ID/safe digest、trusted connector/class 和 owner，使用 app portal/push/SMS/phone 等独立路径并要求 high-risk event acknowledgment/hold；mail delivery 不是唯一确认。`detective-support`。
4. `mailbox-receiving-and-queue-resilience`：监测 warm/hot/SRP/quota/thread limits，保护 critical/role mailbox，提供受控 overflow/quarantine、优先合法 sender class、队列扩展和已演练的 emergency alias；不得把负载转移成无审计丢弃。`containment`。
5. `evidence-preserving-bulk-cleanup-and-user-response`：保留 message trace/cluster/authentication/notification IDs 后按 campaign cluster 批量隔离或清理，检查 account/financial/order/security events；培训用户通过已知渠道联系 IT，不响应轰炸后主动联系的陌生“支持”。`containment`。

**parent application**

zh：邮件提供方、组织和高风险表单 owner 共同实施 sender-side consent admission、recipient-centric fan-in control、关键通知独立路径和 queue/limit resilience；检测到 candidate 时先保护 trusted business/security mail flow，再清理 bomb clusters 并检查伴随账户/交易事件。预期效果是缩小可汇聚消息量、降低合法邮件被埋/拒收的概率并缩短恢复。限制是组织无法强制所有外部网站启用 opt-in，攻击者可用大量真实来源或被盗平台，严格 recipient throttling 会误伤合法 incident/marketing traffic，out-of-band channel 也可能失陷。

en: Mail providers, organizations, and high-risk form owners jointly apply sender-side consent admission, recipient-centric fan-in control, independent paths for critical notifications, and queue or limit resilience. On a candidate, protect trusted business and security mail flow before cleaning bomb clusters and reviewing accompanying account or transaction events. The expected effect is lower converging volume, reduced burial or rejection of legitimate mail, and shorter recovery. An organization cannot force every external site to deploy opt-in, actors can use many genuine sources or compromised platforms, strict recipient throttling can harm legitimate incident or marketing traffic, and alternate channels can also be compromised.

**fan-out child application**

zh：发送方对 signup form 强制 confirmed opt-in、bot challenge 和 per-address/source limits，并共享 abuse fingerprints；收件方按 recipient fan-in 和 sender-owner diversity 临时隔离新 first-contact bulk clusters，同时为 known critical senders 保留受监控优先通道。预期效果是让单次 bot submit 不再自动生成持续 legitimate mail，并使分散来源在目标汇聚前被识别。限制是 confirmation messages 仍会被滥用、shared ESP owner mapping 不完整、allowlisted sender 被盗和跨组织协调延迟。

en: Senders enforce confirmed opt-in, bot challenges, and per-address or source limits on signup forms and share abuse fingerprints. Recipients temporarily isolate new first-contact bulk clusters based on recipient fan-in and sender-owner diversity while retaining a monitored priority path for known critical senders. The expected effect is to prevent one bot submission from automatically generating durable genuine mail and identify dispersed sources before full convergence. Confirmation messages can still be abused, shared-ESP owner mapping is incomplete, allowlisted senders can be compromised, and cross-organization coordination is slow.

**consequential-message child application**

zh：identity、finance、order 和 security systems 为高风险通知使用 mail 之外的独立 channel、明确 acknowledgment/hold SLA 和 notification-to-message ID；bombing 时在安全 portal/客户端中提升并固定这些通知，未确认前暂停可逆交易。预期效果是即使 inbox 被淹，关键事件仍有可发现和可中断路径。限制是 channel compromise、用户 device 不可达、误 hold 影响业务、通知内容隐私和第三方系统不支持共同 ID。

en: Identity, finance, order, and security systems use an independent nonmail channel, explicit acknowledgment or hold SLA, and notification-to-message identifier for high-risk notifications. During bombing, surface and pin these notices in a security portal or client and pause reversible transactions until confirmed. The expected effect is a discoverable and interruptible path for consequential events even when the inbox is flooded. Limitations include alternate-channel compromise, unreachable user devices, business harm from false holds, notification privacy, and third-party systems without common identifiers.

## 9. 共享库查重与复用决议

已运行 `library_lookup.py` 搜索 `email bombing recipient message volume legitimate mail burial`、`mailbox fan in multiple authenticated senders subscription bombing`、`security transaction alert buried in inbox flood`、`mail delivery queue recipient limit availability impact`、`mailbox message access read state high volume`、`recipient centric mail flow resilience critical message continuity`，并用 `rg` 对 T1667、HHS/Rapid7/Sophos/Krebs URL、EmailEvents、Graph message、receiving-limit 和 mail-flow 关键词做精确检查。

| 对象 | 决议 | 原因 |
|---|---|---|
| `REF-000609` | **reuse + extend locator/notes** | Exact Microsoft EmailEvents URL；扩充 T1667 使用字段，不复制 REF。 |
| `REF-000567` | **reuse** | MailItemsAccessed identity/limitations unchanged。 |
| T1667 fixed ATT&CK/HHS/Rapid7/Sophos/Krebs/Graph/limits refs | **create** | 无 exact shared object。 |
| T1667 Claims/Cases | **create** | 无现有 parent/child proposition or event identity。关键消息 child case 仍 defer/none。 |
| `NJA-000124` mail display/authentication differential | **no reuse** | 目标是 spoofed provenance 与社会工程结果；T1667 fan-out 常通过 authentication，逻辑/确认门相反。可复用 `REF-000609`，不复用 Analytic。 |
| `DET-000231` / NJT-0199 external-input endpoint capacity | **adjacent / split** | 端点内部资源/健康因果，不含 mailbox attention、message access 或 notification SLA。 |
| NJT-0198 network DoS DET/MIT | **adjacent / no reuse** | 聚合 network capacity 与 mail-message semantics 不同。 |
| `DET-000202` / NJT-0175 MFA request generation | **adjacent / no reuse** | Identity challenge transaction、approval/token outcome；不是 general mail fan-in/burial。 |
| `MIT-000054` phishing entry controls | **no extend** | Controls lure authenticity/entry, not mail availability or recipient fan-in。 |
| `MIT-000198` metered-service transaction admission | **split / no extend** | Contains bot challenge for SMS/OTP billed transactions, but purpose/measures are victim-billed provider work and cost, not third-party newsletter consent or mailbox continuity。 |
| `MIT-000037` trusted form ownership | **no extend** | Validates sensitive form owner/data destination, not public signup consent and bombing prevention。 |
| New DET/NJA/MIT | **create** | Objective, fields, outcome gates and cross-system notification logic are unique。 |

正式分配前主 Agent 应复核同批 T1657 的 transaction-alert controls 是否可共享“independent confirmation”措施。只有 MIT control concept 与 measures 完全相同才合并；T1667 的 recipient fan-in、mail queue、confirmed opt-in 和 campaign cleanup 不应因都提到 financial notification 而并入 financial-theft MIT。

## 10. 集成门禁与研究限制

1. 准入 `adapt`；`original_attack_subtechniques_imported: false`；正式 lifecycle 保持 `review`。
2. 两个 formal NJS：合法发送者扇出式收件箱洪泛、关键消息埋没同步。低速积累和 alias expansion 保持 `defer`，不预留 ID。
3. 每个 detection outcome 明确分级；message volume、unique senders、authentication pass、unread flag 或 mailbox receiving-limit risk 单独都不确认 T1667。
4. parent/child 均明确 T1499、T1498、Phishing、mail C2 和 T1621 边界；共现时每项需要自己的结果证据。
5. 新 DET 含三项双向 NJA：recipient fan-in/attention、consequential notification、transport/receiving availability。MIT 分别建立 parent 和两个 child applications。
6. `250/15m`, `1000/hour`, `20 sender groups`, `-10/+30m`, `2 × p95`, `24h` 均为由 HHS/Sophos/Exchange limit 与工程需求给出的起始值，不是来源证明的通用恶意阈值；正式文本须标注按 mailbox role/provider/SLA 调优。
7. 不采集 message body 作为默认必需字段；优先 ID、cluster、sender/authentication、folder/read/access 和 workflow outcome，按隐私与最小化原则授权内容检查。
8. HHS 一般结论不能填造关键消息埋没 victim case；没有 notification/message/outcome 闭环时保持 risk/hypothesis。
9. 正式写入后完成 exact/fuzzy duplicate review、ID sync、`make quality`、Bundle、完整双语 Web/API；无人工 reviewer 不得 `published`。

**最终交接状态：** `adapt`；formal Niji child `2`；defer axes `2`；reuse `REF-000567`, reuse+extend `REF-000609`; create DET `1`, NJA `3`, MIT `1`, parent/fan-out cases `2`; consequential-message child case `0` pending incident-level evidence。
