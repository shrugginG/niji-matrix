# T1491 Defacement / 篡改展示内容：TA0040 研究交接

工作项 `WORK-TA0040-T1491`；批次 `BATCH-TA0040-002`；临时键前缀 `TA0040-T1491-`。本交接固定使用 ATT&CK Enterprise 19.1，只提交研究结论，不分配正式 ID，不修改正式矩阵、决策或共享库。

## 1. 准入结论

**建议 `adapt`，置信度 high。** T1491 的父行为与 Impact 目的成立：攻击者恶意替换组织控制的视觉内容、界面或发布结果，以传递消息、恐吓、误导或宣示入侵，从而直接损害展示完整性。Niji 应把直接对象固定为“组织身份或系统界面下实际呈现给人的内容”，并只在实施方式改变痕迹位置或防守观察关系时记录匿迹机理。普通网页攻陷、Web shell、不可见脚本注入和恶意文件上传本身不构成本技术；必须证明未经授权的展示结果。

The T1491 parent behavior and its Impact purpose are established: an adversary maliciously replaces visual content, an interface, or a publication result controlled by an organization to deliver a message, intimidate, mislead, or claim an intrusion, directly damaging display integrity. Niji should anchor the direct object in content actually presented to a person under the organization’s identity or system interface and record stealth only when implementation changes trace location or defender observation. An ordinary website compromise, web shell, invisible script injection, or malicious upload is insufficient without an unauthorized display outcome.

当前支持一个正式 Niji 原生子项：**展示源绑定替换 / Display-Source Binding Substitution**。其变量不是内外网位置或 DNS 产品，而是组织展示标识仍然不变、标识到内容源的绑定被替换，同时受监测的规范源保持干净。ICANN 对 2005 年 Hushmail 事件的原始报告给出完整因果链：注册记录被接管，`www.hushmail.com` 的 DNS 记录被指向攻击者服务器，访问者看到篡改页面，而 Hush 服务器没有被未授权访问、托管数据没有被破坏。

## 2. ATT&CK 子项 planning-only 覆盖决议

固定版子项数为 `2`，ID 为 `T1491.001`、`T1491.002`；`original_attack_subtechniques_imported: false`。

| ATT&CK 子项 | 所代表维度 | 覆盖决议 | 理由 |
|---|---|---|---|
| `T1491.001` Internal Defacement | 内部网站、登录消息、桌面壁纸等内部展示面 | `not-stealth-distinct`，行为纳入父级 | “内部”只描述受众和部署位置。直接修改内部门户、壁纸或 banner 未自动产生独立痕迹变化或防守观察差异；若通过源绑定替换实现，可按 Niji 原生变量另行归类。 |
| `T1491.002` External Defacement | 外部网站等公开展示面 | `not-stealth-distinct`，行为纳入父级；Hushmail 证据支持原生变量 | “外部”仍是位置维度。DNS 劫持案例没有被改名为外部篡改子项，而是用于证明“展示源绑定替换”这一跨位置变量。 |

两个 ATT&CK 子项覆盖了应用位置，却没有回答攻击者怎样改变痕迹或防守观察；因此不能直接转化为 NJS。一个正式 Niji 子项与两个 ATT&CK 子项之间的数量差异是合理的。

## 3. Niji 原生轴搜索与收敛

| 候选轴 | 行为设计 → 痕迹变化 → 防守观察差异 | 决议 |
|---|---|---|
| 展示源绑定替换 | 攻击者保留组织域名或界面标识，但把其解析或源绑定改到攻击者内容源 → 规范源文件/CMS 可保持不变，变化进入注册、DNS、路由或发布控制面 → 只监测源站完整性的防守方看见干净源，用户却看见被篡改结果 | **formal**；证据和专用防御差异均成立。 |
| 按受众条件呈现 | 依据 User-Agent、Referer、地域、会话或时间只向部分访问者返回篡改内容 → 单点监测可能取得正常版本 → 需多画像差分 | **defer**。Google 确认黑客使用 cloaking 隐藏被黑内容，但现有来源主要涉及搜索垃圾、恶意重定向或投放，没有结论级证据证明其直接结果是 T1491 的可见完整性影响。 |
| 小区域覆盖或低差分注入 | 只覆盖页面一小块、引用外部图片或 CSS overlay → 文件差分较小但用户仍见篡改内容 | **defer**。技术上可行，但现有一手材料不足以证明稳定攻击变量、独立防御边界及真实匿迹效果。 |
| 集中策略或管理代理委托发布 | 修改 GPO、MDM、CMS 工作流或集中 banner 配置，让受信代理在多个终端呈现消息 → 端点写入主体与原决策者分离 | **defer**。缺少直接攻击案例和不可互换防御证据；不得从合法产品能力推造 NJS。 |
| 文件、数据库、CMS、对象存储或桌面壁纸介质 | 更换存储位置或产品，但直接覆写展示内容 | **parent-core**。介质和产品不是稳定匿迹变量。 |

## 4. 父技术完整双语字段草稿

### name / summary

- zh：**篡改展示内容**。攻击者恶意替换组织控制的视觉内容或界面结果，并通过把变化移出受监测的规范发布源而延迟发现与归因。
- en: **Defacement**. Adversaries maliciously replace organization-controlled visual content or interface output and delay detection and attribution by moving the change outside the monitored canonical publication source.

### definition_and_concept

zh：篡改展示内容是攻击者让组织控制的网站、内部入口、登录消息、桌面或其他面向人的界面呈现未经授权的文字、图像或布局，以传递消息、恐吓、误导、施压或宣示入侵，并直接损害展示内容的完整性与受众信任。概念单位是组织身份或系统界面下实际呈现结果的恶意变化；文件、数据库行、CMS 对象、壁纸、DNS 记录和云存储产品只是可能的实现载体。

en: Defacement occurs when an adversary causes a website, internal portal, login message, desktop, or other human-facing interface controlled by an organization to present unauthorized text, imagery, or layout in order to deliver a message, intimidate, mislead, pressure, or claim an intrusion, directly harming display integrity and audience trust. The conceptual unit is a malicious change in what is actually presented under the organization’s identity or system interface; a file, database row, CMS object, wallpaper, DNS record, or cloud-storage product is only an implementation surface.

zh：Niji 关注展示结果与防守方所监测发布源之间的观察差异。直接覆写 HTML、CMS 页面或壁纸界定父行为，却不能自动证明匿迹；当攻击者保留规范源而替换域名到内容源的绑定时，源站文件完整性可以持续显示正常，受众却从攻击者服务器取得篡改页面。攻击者获得网页权限、部署 Web shell 或插入不可见脚本若没有产生展示完整性结果，仍属于相邻的入侵、执行、投放或控制行为。

en: Niji focuses on the observation difference between the displayed result and the publication source monitored by defenders. Directly overwriting HTML, a CMS page, or wallpaper defines the parent behavior but does not automatically establish stealth. When an actor preserves the canonical source while replacing the binding from a domain to its content source, origin file integrity can continue to appear normal while the audience retrieves a defaced page from an adversary server. Website access, web-shell deployment, or invisible script injection without a display-integrity outcome remains adjacent compromise, execution, staging, or control behavior.

### stealth_characteristics

zh：篡改展示内容通常有意对目标受众可见，匿迹价值存在于影响发生前后的守方观察错位，而不是让最终消息对所有人不可见。展示源绑定被替换后，恶意内容、Web 访问和证书痕迹位于替代服务器或解析路径，规范源文件、CMS 记录和部署历史可以没有对应改动；只检查源站或单一探测点的守方因而可能把用户报告误判为缓存、客户端或普通网站故障。

en: Defacement is usually intended to be visible to its target audience; its stealth value lies in defender-observation mismatch before and around the impact rather than hiding the final message from everyone. After a display-source binding is replaced, malicious content, web access, and certificate traces reside at the substitute server or resolution path while canonical origin files, CMS records, and deployment history may have no corresponding change. A defender checking only the origin or one probe can therefore misclassify user reports as cache, client, or ordinary site failure.

zh：残余痕迹包括域名注册或托管区变更、旧新 RRset、TTL、解析器与观察点之间的答案差、DNSSEC 验证状态、替代 IP 和证书、HTTP 重定向与正文/视觉哈希，以及规范源与用户取得内容之间的差分。独立观察点、长期控制面日志和发布源快照能够恢复因果链；正常 DNS 故障切换、CDN 迁移、维护页面、A/B 测试、区域化内容和个人壁纸设置是主要反例。

en: Residual traces include registrar or hosted-zone changes, old and new RRsets, TTLs, answer differences across resolvers and vantages, DNSSEC validation state, substitute IP addresses and certificates, HTTP redirects and body or visual hashes, and differences between the canonical source and content obtained by users. Independent vantages, retained control-plane logs, and publication-source snapshots can restore the causal chain. Legitimate DNS failover, CDN migration, maintenance pages, A/B testing, localization, and user-selected wallpaper are principal counterexamples.

### scope_boundary_definition

zh：纳入组织控制的展示身份或系统界面实际向人呈现未经授权内容的行为，无论内容存放在文件、CMS、对象存储、桌面配置还是替代服务器。判断必须同时确认组织所控制或被冒用的展示身份、未经授权的可见结果，以及攻击行为与该结果的关系。CMS 首页即使存放在数据库中，只要直接对象是展示页面，仍属于本技术。

en: Include behavior that makes an organization-controlled display identity or system interface actually present unauthorized content to a person, whether the content resides in a file, CMS, object store, desktop configuration, or substitute server. Classification requires the display identity controlled or appropriated from the organization, an unauthorized visible result, and a relationship between the adversary action and that result. A CMS home page remains in scope even if stored in a database when the direct object is the displayed page.

zh：T1565 负责改变业务数据值、传输数据或运行时数据以影响业务流程、组织理解或决策；业务记录被篡改后恰好在界面显示，不因此自动变成 T1491。相似域上的克隆站、凭据收集页和首次访问诱饵归钓鱼或初始访问；只承载命令、死信箱或载荷的网页内容归 C2 或投放；未改变面向人内容的 Web shell、漏洞利用和普通站点攻陷不纳入。DNS 改道若只窃取凭据、读取流量或造成不可用，应分别评价钓鱼、通信路径中间介入或拒绝服务；只有组织身份下出现恶意展示结果时才确认本技术。

en: T1565 owns changes to business data values, transmitted data, or runtime data intended to affect a business process, organizational understanding, or decision making; a manipulated business record does not become T1491 merely because an interface later renders it. A cloned site on a lookalike domain, credential-harvesting page, or first-contact lure belongs to phishing or Initial Access; web content that only carries commands, a dead drop, or a payload belongs to C2 or staging; a web shell, exploitation, or ordinary site compromise without changed human-facing content is excluded. DNS diversion used only to steal credentials, read traffic, or cause unavailability should be assessed as phishing, content-path interception, or denial of service. This technique is confirmed only when malicious display occurs under the organization’s identity.

### application_scenarios_and_threat_model

**application_scenarios**

zh：在外部网站场景中，攻击者可以接管注册商或权威 DNS 账户，把组织网站的 A、AAAA、CNAME 或 NS 绑定改到托管篡改页面的服务器，同时保留真实源站内容。内部场景可包括被篡改的入口页面、登录 banner 或桌面消息，但直接本地修改通常属于父级核心；只有观察关系存在独立变化时才进入子项。篡改可出现在其他入侵目标完成后，也可用于施压或公开宣示，伴随的加密、擦除或凭据盗取必须分别建模。

en: In an external-site scenario, an actor can take over a registrar or authoritative-DNS account and change an organization site’s A, AAAA, CNAME, or NS binding to a server hosting a defacement page while leaving the real origin intact. Internal scenarios include altered portal pages, login banners, or desktop messages, although direct local changes remain parent core unless they create an independently supported observation difference. Defacement may follow completion of other intrusion goals or serve coercion and public signaling; accompanying encryption, wiping, or credential theft requires separate modeling.

**attacker_model**

zh：攻击者至少需要修改展示内容源或标识到内容源绑定的权限、识别高价值展示面的知识，以及让恶意结果维持到目标受众看到的时间。源绑定替换还需要控制注册、权威 DNS、解析器或等效发布映射，并提供可访问的替代内容；HTTPS 场景可能要求有效证书或容忍明显证书错误。注册锁、多因素认证、双人批准、DNSSEC 验证、外部变更通知、TTL 缓存和快速回滚都会限制效果。

en: The adversary needs authority to change a display source or the binding from an identifier to that source, knowledge of a high-value display surface, and enough residence time for the target audience to see the result. Source-binding substitution additionally requires control of registration, authoritative DNS, a resolver, or an equivalent publication mapping and an accessible substitute content source; HTTPS may require a valid certificate or tolerance for conspicuous certificate errors. Registry locks, multifactor authentication, dual approval, DNSSEC validation, out-of-band change notification, TTL caching, and rapid rollback constrain the effect.

**defender_model**

zh：防守方可分别取得内容库或 CMS 版本、文件完整性、部署审计、域名注册与权威 DNS 变更、递归解析答案、TLS 证书、多个地域的 HTTP/视觉快照以及用户报告。检测必须把“批准发布状态—实际展示结果”和“域名绑定—实际内容源”两条关系连接起来。只保留源站 FIM、只从一个解析器探测、缺少变更前 RRset 或未覆盖认证后页面时，展示与原因会被拆散；动态内容和合法个性化还会降低单一哈希证据强度。

en: Defenders may separately obtain content-repository or CMS versions, file integrity, deployment audit, domain-registration and authoritative-DNS changes, recursive answers, TLS certificates, HTTP or visual snapshots from several regions, and user reports. Detection must join both approved publication state to actual display output and domain binding to actual content source. Origin FIM alone, one resolver vantage, absent pre-change RRsets, or missing authenticated-page coverage separates the display from its cause; dynamic content and legitimate personalization also weaken a single hash.

### stealth_mechanisms

**`NM-BT` primary — 解析绑定替换使恶意展示落在规范源监测之外 / Resolution-binding replacement moves malicious display outside canonical-source monitoring**

zh：攻击者不必修改受监测源站，而是把组织展示标识指向攻击者服务器。行为设计把关键变化写入注册或解析控制面，用户请求随后在另一内容源结束；源站 FIM、CMS 审计和规范部署哈希因此可以保持正常，防守方若未连接 DNS 变化、跨解析器答案和实际 HTTP 内容就看不到影响原因。ICANN 的 Hushmail 调查直接记录了 DNS 记录改向、攻击者服务器上的篡改页面、真实服务器未被访问与数据未被破坏这一链条。置信度 high；证据键 `TA0040-T1491-REF-ICANN-SAC007`。

en: The actor does not need to modify the monitored origin and instead directs the organization’s display identifier to an adversary server. The design places the critical change in registration or resolution control, after which user requests terminate at a different content source. Origin FIM, CMS audit, and canonical deployment hashes can therefore remain normal, and a defender that does not join DNS changes, cross-resolver answers, and actual HTTP content misses the cause of impact. ICANN’s Hushmail investigation directly records DNS redirection, a defaced page on an adversary server, no unauthorized origin-server access, and no compromise of hosted data. Confidence is high; evidence key `TA0040-T1491-REF-ICANN-SAC007`.

### subtechnique_taxonomy

zh：当前原生分类只保留“展示源绑定替换”。其稳定变量是组织展示标识与规范内容源的绑定被替换，而规范源自身保持不变；该变量把痕迹从文件/CMS 平面移到注册、解析或等效发布控制面，并要求跨观察点重建。内部与外部、网站与桌面、文件与数据库、云产品与操作系统均不是子项边界。按受众条件呈现、低差分覆盖和集中策略委托发布均因结论级证据不足而 defer，不分配 ID。

en: The current native taxonomy retains only Display-Source Binding Substitution. Its stable variable is replacement of the binding between an organization’s display identifier and its canonical content source while the canonical source itself remains unchanged. The variable moves traces from the file or CMS plane into registration, resolution, or an equivalent publication-control plane and requires cross-vantage reconstruction. Internal versus external, website versus desktop, file versus database, cloud product, and operating system do not define children. Audience-conditioned presentation, low-difference overlay, and delegated policy publication remain deferred for lack of conclusion-level evidence and receive no ID.

### defense / evidence / limitations

- detections: `TA0040-T1491-DET-DISPLAY-INTEGRITY-LINEAGE`（create，含两个 Analytic）。
- mitigations: `TA0040-T1491-MIT-PUBLICATION-RESOLUTION-INTEGRITY`（create）。
- claims: `TA0040-T1491-CLM-PARENT`, `TA0040-T1491-CLM-BOUNDARY`, `TA0040-T1491-CLM-SOURCE-BINDING`, `TA0040-T1491-CLM-DEFENSE`。
- case: `TA0040-T1491-CASE-HUSHMAIL-DNS-DEFACEMENT`。
- references: reuse `REF-000524`, `REF-000029`; create the reference candidates in section 7.

zh：ATT&CK 19.1 充分锚定父行为和内外展示场景，ICANN 对 Hushmail 的调查充分证明 DNS 源绑定替换与实际篡改结果。该案例是 2005 年单一外部域名事件，不能直接证明 CDN 边缘映射、内部解析、MDM/GPO 或按受众条件呈现都具有相同链条。DNS 或注册变更本身也不证明篡改；必须保留实际可见内容、规范源状态和授权上下文。动态页面、合法区域化、缓存传播、TLS 错误阻断和缺失控制面日志会限制检测结论。

en: ATT&CK 19.1 adequately anchors the parent behavior and internal or external display scenarios, while ICANN’s Hushmail investigation directly establishes DNS source-binding substitution and an actual defacement result. That evidence is one external-domain incident from 2005 and does not prove that CDN edge mappings, internal resolution, MDM or GPO, or audience-conditioned presentation share the same chain. A DNS or registration change alone also does not establish defacement; actual visible content, canonical-source state, and authorization context are required. Dynamic pages, legitimate localization, cache propagation, TLS errors that block display, and absent control-plane logs limit detection conclusions.

## 5. 正式子项完整双语字段草稿

### 展示源绑定替换 / Display-Source Binding Substitution

**summary**

- zh：攻击者保留组织展示标识，却把该标识绑定到替代内容源，使用户看到篡改结果而规范源完整性监测保持正常。
- en: The adversary preserves an organization’s display identifier but binds it to a substitute content source, causing users to see defacement while canonical-source integrity monitoring remains normal.

**definition_and_concept**

zh：展示源绑定替换是攻击者不直接改写规范展示源，而是改变组织标识到内容提供者的权威或被客户端接受的映射，使同一域名、入口名称或界面标识从攻击者控制的源取得未经授权的可见内容。当前结论级实例是注册与 DNS 记录被改变后，组织域名指向托管篡改页面的服务器。

en: Display-Source Binding Substitution occurs when an adversary avoids directly rewriting the canonical display source and instead changes the authoritative or client-accepted mapping from an organization identifier to its content provider, causing the same domain, portal name, or interface identifier to retrieve unauthorized visible content from an adversary-controlled source. The current conclusion-level instance is alteration of registration and DNS records so that an organization domain points to a server hosting a defacement page.

zh：子项边界由“标识—源绑定被替换且规范源保持干净”定义，不由 DNS 厂商、记录类型或内外网位置定义。只有替代源在组织身份下产生可见完整性影响时才属于本子项；指向凭据收集页、透明代理、C2 资源或不可用终点而没有篡改展示结果，分别属于相邻行为。

en: The child is defined by replacement of the identifier-to-source binding while the canonical source remains clean, not by DNS vendor, record type, or internal versus external location. It applies only when the substitute source creates a visible integrity impact under the organization’s identity. Diversion to credential harvesting, a transparent proxy, C2 material, or an unavailable endpoint without a defacement result belongs to adjacent behavior.

**stealth_characteristics**

zh：**展示源绑定替换**把恶意内容与攻击决策放到规范源站之外：源站文件、CMS 版本和部署流水线没有对应变化，访问组织域名的用户却因解析绑定而到达替代服务器。TTL、递归器缓存、分裂视图和地域传播还可能让部分探测点取得正常页面、另一些取得篡改页面，使一次源站检查或单点可用性监测无法代表受众实际观察。

en: **Display-Source Binding Substitution** places malicious content and the adversary decision outside the canonical origin: origin files, CMS versions, and deployment pipelines have no corresponding change, yet users visiting the organization’s domain reach a substitute server through the resolution binding. TTLs, recursive caches, split views, and geographic propagation can also make some probes retrieve the normal page while others retrieve the defacement, so one origin check or single-vantage availability monitor does not represent audience observation.

zh：控制面身份、旧新记录值、变更 ID、TTL、DNSSEC 状态、不同解析器的答案、替代服务器 IP、TLS 证书和页面正文/视觉哈希仍然可见。独立保留注册和权威 DNS 审计，并从多个解析器和地域重取实际页面，会把干净源站与恶意展示重新连接；若攻击者同时控制日志或替代源只短时存在，链条会变弱。

en: Control-plane identity, old and new record values, change identifiers, TTL, DNSSEC state, answers from different resolvers, substitute server IP, TLS certificate, and page body or visual hashes remain observable. Independently retained registrar and authoritative-DNS audit plus actual page retrieval through several resolvers and regions reconnects the clean origin to the malicious display. The chain weakens if the actor also controls logs or the substitute source exists only briefly.

**scope_boundary_definition**

zh：纳入域名注册、NS 委派、A/AAAA/CNAME 等权威记录、递归器答案或等效发布映射被恶意替换，并使组织展示标识实际呈现攻击者内容的情况。规范源未改动是本子项的重要判定条件；若源站文件或 CMS 对象本身被直接覆写，则保留在父级核心，除非另有独立绑定替换证据。

en: Include malicious replacement of domain registration, NS delegation, authoritative A, AAAA, or CNAME records, resolver answers, or an equivalent publication mapping when the organization’s display identifier actually presents adversary content. An unchanged canonical source is a material classification condition. Direct overwrite of an origin file or CMS object remains parent core unless independent binding-substitution evidence also exists.

zh：同形网站位于相似域名而没有取得组织真实展示标识时属于钓鱼或品牌冒用；DNS 改道到透明代理并读取流量属于 NJT-0142，改变业务数据内容属于 T1565，只有断站属于拒绝服务。合法流量工程、灾备切换、CDN 迁移、蓝绿发布、区域化 DNS 和缓存未过期均可能产生答案差，必须用批准记录和实际内容结果排除。

en: A lookalike site on a similar domain without control of the organization’s real display identifier belongs to phishing or brand abuse. DNS diversion to a transparent proxy that reads traffic belongs to NJT-0142, alteration of business data belongs to T1565, and outage alone belongs to denial of service. Legitimate traffic engineering, disaster-recovery failover, CDN migration, blue-green release, geo-DNS, and unexpired caches can all create answer differences and require approved-change and actual-content context.

**application_scenarios_and_threat_model**

zh：典型场景是攻击者通过社会工程或被盗凭据控制注册商账户，修改组织网站记录并把域名指向托管攻击者消息和图像的服务器。Hushmail 事件中，攻击者先改变注册联系信息和密码，再把网站 DNS 记录指向篡改主页；真实服务器未被未授权访问。相同变量理论上可出现在内部解析或其他展示映射，但在获得独立证据前不把这些实现写成事实案例。

en: A representative scenario is registrar-account control through social engineering or stolen credentials, followed by changing an organization’s website record to point at a server hosting adversary messages and images. In the Hushmail incident, the actor first changed registration contact information and the password, then pointed the website’s DNS record to a defaced home page; the real servers were not accessed without authorization. The same variable could theoretically occur in internal resolution or another display mapping, but those implementations should not be stated as observed cases without independent evidence.

zh：攻击者需要接触注册、权威 DNS 或客户端接受的解析路径，知道目标名称与当前记录，并控制替代内容源。若要避免证书警报，还需要能够取得被接受的证书或利用仍允许明文的入口；同时要考虑 TTL、缓存、DNSSEC、注册锁和快速通知。错误记录、短驻留、替代服务器下线或证书错误会降低实际受众覆盖并增加暴露。

en: The adversary needs access to registration, authoritative DNS, or a resolution path accepted by clients, knowledge of the target name and current records, and control of a substitute content source. Avoiding certificate warnings also requires an accepted certificate or an entry point that still permits plaintext. TTLs, caching, DNSSEC, registry locks, and rapid notification constrain the operation. Wrong records, brief residence, substitute-server removal, or certificate errors reduce audience coverage and increase exposure.

zh：防守方需要独立保存注册和 DNS 变更身份、前后 RRset 与批准单，从权威服务器及多个递归器记录实际答案，并以 Host/SNI 保持不变的方式抓取 HTTP/TLS 内容，再与规范源和批准发布比较。单一公司解析器可能只看到缓存，源站监控只证明源站未改，公共探测也可能错过内部或选择性答案；三者必须分级表达而不能相互替代。

en: Defenders need independently retained registration and DNS change identity, before-and-after RRsets, and approvals; actual answers from authoritative servers and several recursive resolvers; and HTTP or TLS retrieval using the same Host and SNI, compared with the canonical origin and approved release. One corporate resolver may see only cache state, origin monitoring proves only that the origin is unchanged, and public probes may miss internal or selective answers. These evidence levels must be reported separately rather than substituted for one another.

**stealth mechanism**

- `NM-BT`, primary；摘要 zh：源绑定替换绕开规范源完整性观察；en: Source-binding substitution bypasses canonical-source integrity observation。
- 分析与父级同一因果链，但子级限定为标识到源的映射替换；证据 `TA0040-T1491-REF-ICANN-SAC007`，confidence high。

**defense / evidence / limitations**

- detection: `TA0040-T1491-DET-DISPLAY-INTEGRITY-LINEAGE`，直接由 DNS Analytic 覆盖。
- mitigation: `TA0040-T1491-MIT-PUBLICATION-RESOLUTION-INTEGRITY`，须有独立 child application。
- claims: `TA0040-T1491-CLM-SOURCE-BINDING`、`TA0040-T1491-CLM-DEFENSE`。
- case: `TA0040-T1491-CASE-HUSHMAIL-DNS-DEFACEMENT`。

zh：正式结论主要依赖一个外部域名案例和规范文档。案例证明注册/DNS 改向、替代页面、干净源站和品牌影响，却不证明所有 DNS 劫持都以匿迹为目的，也不证明现代 HTTPS、DNSSEC、CDN 或内部解析具有相同结果。没有实际页面快照、用户观察或等价输出证据时，只能确认路径风险，不能确认篡改展示。

en: The formal conclusion relies primarily on one external-domain case and protocol or provider documentation. The case establishes registration and DNS diversion, a substitute page, a clean origin, and brand impact, but does not prove that every DNS hijack has a stealth purpose or that modern HTTPS, DNSSEC, CDN, or internal resolution produces the same result. Without an actual page snapshot, user observation, or equivalent output evidence, only path risk can be established, not defacement.

## 6. 可实施防御候选

### `TA0040-T1491-DET-DISPLAY-INTEGRITY-LINEAGE` — 批准发布状态至实际展示谱系 / Approved Publication State to Observed Display Lineage

**目标：** 比较批准发布状态、标识到源的绑定和实际展示结果，确认未经授权的可见变化并定位变化发生在内容源还是解析/发布控制面。`detects_refs` 在主 Agent 分配后应覆盖父 NJT 与正式 child；domains `[enterprise]`。

#### `TA0040-T1491-NJA-PUBLICATION-OUTPUT-DIFFERENTIAL`

**name:** 批准发布状态—实际展示差分 / Approved Publication State–Observed Display Differential。

**logic:** 对每个高价值展示面登记 `surface_id`、表面类型、owner、规范 `source_id`、批准 `release_id`、允许的地域/语言/认证变体和可稳定比较的 DOM、文本、视觉或 UI 状态。事件触发并至少每五分钟从匹配画像取得实际结果；先规范化时间戳、nonce、个性化槽等批准动态区，再比较语义文本哈希、DOM 结构和视觉哈希。出现未经批准的可见差分时，在前后二十四小时内关联文件、CMS、对象、壁纸/banner 配置和部署控制面变更，输出 `source_modified`、`rendered_only_divergence` 或 `authorized_variant`。只有站点被攻陷、脚本新增或文件变化而没有可见结果时不确认 T1491；源保持批准状态而展示改变时转交 DNS/绑定 Analytic。

**data requirements:**

- `display-surface-inventory`: `surface_id`, `surface_type`, `owner`, `canonical_source_id`, `approved_release_id`, `allowed_variant_profile`, `criticality`。
- `publication-change-audit`: `event_time`, `surface_id`, `source_id`, `actor_id`, `operation`, `object_path_or_id`, `before_hash`, `after_hash`, `release_id`, `approval_id`, `source_ip`, `process_start_key`。
- `display-output-observation`: `event_time`, `surface_id`, `viewer_profile`, `vantage_id`, `result_status`, `content_hash`, `semantic_text_hash`, `dom_or_ui_hash`, `visual_hash`, `evidence_ref`。

**observables:** 未经批准的语义/视觉结果与当前 release 不一致；异常发布身份或本地进程修改后相同内容实际出现；源站批准状态正常而用户观察持续偏离。

**correlation:** 同一比较轮的探测结果限制在五分钟内；发布变更与展示结果初始使用前后 24 小时窗口，并按实际发布周期缩短。维度：`surface_id`, `viewer_profile`, `vantage_id`, `source_id`, `release_id`, `actor_id`, `content_variant`, `time`。

**false positives:** 批准发布/回滚、维护或事件通知页面、A/B 测试、地域/语言/认证个性化、CDN 缓存传播、用户自选桌面背景。

**blind spots:** 需要交互后才出现的内容、未覆盖的认证页面、动态页面无法稳定规范化、没有历史 release 或变更审计、攻击者使用合法发布身份并同步篡改批准记录。

**tuning:** 为每个表面登记允许变体和过期时间；按 DOM 区域、语义和视觉组合比较，避免对整个动态页面用一个哈希。批准发布身份不得永久白名单；仍须核对 approval、release 与实际输出。高风险表面至少保留一个不依赖生产 CDN/解析路径的独立观察点。

#### `TA0040-T1491-NJA-BINDING-TO-OUTPUT-LINEAGE`

**name:** 名称绑定—内容源—展示结果谱系 / Name Binding–Content Source–Display Outcome Lineage。

**logic:** 在 DNS/注册变更事件触发时及固定五分钟轮次，从权威服务器和至少三个独立递归/地域观察点解析高价值名称，保存完整 NS、CNAME、A/AAAA 链、TTL、DNSSEC 验证和回答来源。对每个答案以相同 Host/SNI 抓取 TLS 与 HTTP 结果，记录证书、公钥、重定向、正文/语义/视觉哈希并与规范源比较。将注册或托管区 `actor_id`、前后记录、change ID 和批准单连接到答案传播及页面差分；只有异常绑定或答案差与未经授权的可见内容共同成立，且规范源仍为批准版本时，输出 `display_source_substitution_confirmed`。只有 IP 变化、证书变化或 DNS 错误时保持路径异常，不确认篡改。

**data requirements:**

- `dns-registration-control-plane`: `event_time`, `actor_id`, `event_name`, `zone_or_domain_id`, `record_name`, `record_type`, `action`, `old_rdata`, `new_rdata`, `ttl`, `change_id`, `source_ip`, `approval_id`。
- `multivantage-dns-answer`: `event_time`, `vantage_id`, `resolver_id`, `qname`, `qtype`, `rcode`, `answers`, `ttl`, `dnssec_status`, `authoritative_ns`。
- `tls-http-content-observation`: `event_time`, `vantage_id`, `qname`, `resolved_ip`, `sni`, `certificate_fingerprint`, `issuer`, `http_status`, `redirect_chain`, `content_hash`, `semantic_text_hash`, `visual_hash`。
- `canonical-publication-state`: `surface_id`, `source_endpoint`, `approved_release_id`, `content_hash`, `observed_at`。

**observables:** 未经批准的 NS/RRset/注册信息变化；同一名称跨解析器得到超出批准流量工程的内容源差异；替代答案对应未经授权页面而规范源仍为批准内容。

**correlation:** 同一五分钟轮次比较各观察点；控制面变化从前 15 分钟连接到 `max(2 × 旧 TTL, 1 小时)`，上限 24 小时，并保留 24 小时传播状态。维度：`domain`, `record_name`, `record_type`, `change_id`, `resolver_id`, `vantage_id`, `resolved_ip`, `certificate_fingerprint`, `content_variant`, `time`。

**false positives:** 批准 DNS/CDN 迁移、灾备和健康检查故障切换、蓝绿发布、GeoDNS/Anycast、DDoS sinkhole、递归器过期缓存。

**blind spots:** 未抽样的递归器或窄范围投毒、DoH/DoT 绕过受管解析、注册商不提供审计、攻击者同步修改批准记录、替代源复用批准 CDN 或证书、短于探测间隔的改向。

**tuning:** 登记批准 NS/RRset、ASN/CDN、证书和内容变体及变更窗口；不按 IP 变化单独告警。将用户报告触发临时高频多观察点抓取，使用独立通知域接收注册/DNS 变更告警，并对每次例外绑定 owner、approval 和到期时间。

### `TA0040-T1491-MIT-PUBLICATION-RESOLUTION-INTEGRITY` — 展示发布与解析权威完整性 / Display Publication and Resolution Authority Integrity

**measures:**

1. `segregated-publish-and-dns-authority`：分离内容发布、DNS/注册、证书和恢复权限；对注册商、权威 DNS 与 CMS 强制抗钓鱼 MFA、最小权限、独立恢复渠道，并对 NS、DS 及高价值 A/AAAA/CNAME 变更实施双人批准。控制类型 `preventive`。
2. `domain-lock-and-signed-resolution`：启用适用的 registrar/registry update/transfer/delete locks，正确部署 DNSSEC 并监测验证失败；锁解除和 DS/NS 变化必须走带外复核。控制类型 `preventive`。
3. `versioned-display-state-and-independent-assurance`：保存不可变或版本化的批准内容、UI 配置、RRset 与发布清单，从不共用生产解析/源站的多个观察点核对实际展示，并把变更通知送到独立域。控制类型 `detective-support`。
4. `evidence-preserving-rollback`：篡改时先保存注册/DNS、证书、页面和发布证据，再恢复账户、记录和已知良好内容，撤销受影响会话/密钥并验证各解析器和地域收敛。控制类型 `containment`。

**parent application:** 对网站、内部入口、banner、壁纸及其内容源建立 owner、批准发布、可见结果和恢复版本；分离高权限并以实际输出验证发布。预期效果是缩小未经授权展示更改机会，并使变更可快速定位与恢复。限制是被盗的批准身份或同步被篡改的审批系统仍可产生完整但恶意的发布链；备份可恢复内容，却不能代替修补入侵入口或处理品牌影响。

**child application:** 对组织域使用注册/registry lock、抗钓鱼 MFA、独立恢复联系和双人 DNS 变更；保留前后 RRset，启用适用 DNSSEC，从多个解析器核对答案并抓取实际页面。预期效果是阻止或快速暴露标识到源的替换，避免把干净源站误作无影响证据。限制是 DNSSEC 不能阻止已获权威签名/注册控制的攻击者发布已签名恶意记录，本地解析器或客户端路径劫持也可能在权威区之外发生；缓存传播和严格锁定会增加恢复复杂度。

## 7. 来源与原子证据账本

### 可复用来源

- `REF-000524`，**reuse**：AWS CloudTrail Record Contents。支持 `userIdentity`、`eventName`、`sourceIPAddress`、`requestParameters`、`responseElements` 等控制面字段，不单独证明 Route 53 记录语义或恶意目的。
- `REF-000029`，**reuse only for boundary**：JPCERT/CC 被篡改 VPN 页面加载 Scanbox。它证明站点攻陷可服务侦察/投放，却不自动构成面向人的篡改展示，适合支持“普通网页入侵不是 T1491 直接结果”的边界。

### 新 Reference 候选

| 临时键 | 来源与 URL | 支持结论 |
|---|---|---|
| `TA0040-T1491-REF-ATTACK-T1491` | MITRE ATT&CK Enterprise 19.1 T1491, `https://attack.mitre.org/versions/v19/techniques/T1491/` | 父行为、Impact、两个 planning-only 子项。 |
| `TA0040-T1491-REF-ATTACK-T1565` | MITRE ATT&CK Enterprise 19.1 T1565, `https://attack.mitre.org/versions/v19/techniques/T1565/` | 数据操纵以影响业务流程、理解或决策，支持相邻边界。 |
| `TA0040-T1491-REF-ICANN-SAC007` | ICANN SSAC, SAC 007 Domain Name Hijacking, `https://www.icann.org/en/ssac/registration-services/documents/sac-007-domain-name-hijacking-incidents-threats-risks-and-remediation-12-07-2005-en` | Hushmail DNS 改向、篡改页面、源站未入侵、品牌影响、Registrar-Lock/EPP authInfo/通知。 |
| `TA0040-T1491-REF-MICROSOFT-SIR15` | Microsoft Security Intelligence Report Volume 15, `https://download.microsoft.com/download/5/0/3/50310cce-8af5-4fb4-83e2-03f1da92f33c/microsoft_security_intelligence_report_volume_15_english.pdf` | 被攻陷 DNS 记录造成看似网站被篡改、用户难区分 DNS 与站点问题。 |
| `TA0040-T1491-REF-GOOGLE-HACKED-CLOAKING` | Google Search spam policies, `https://developers.google.com/search/docs/essentials/spam-policies` | 黑客会用 cloaking 让站主更难发现被黑内容；只支持 deferred 轴，不证明 T1491 结果。 |
| `TA0040-T1491-REF-AWS-ROUTE53-CLOUDTRAIL` | AWS, Logging Route 53 API calls with CloudTrail, `https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/logging-using-cloudtrail.html` | `ChangeResourceRecordSets` 及记录名、类型、值、TTL 等请求字段。 |
| `TA0040-T1491-REF-AWS-ROUTE53-QUERYLOG` | AWS, Route 53 resolver query-log format, `https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-query-logs-format.html` | query name/type、rcode、answers/rdata、client、time 等解析数据。 |
| `TA0040-T1491-REF-NCSC-REGISTRAR-SECURITY` | UK NCSC, Good security practice for domain registrars, `https://www.ncsc.gov.uk/collection/security-practice-domain-registrars/make-strong-security-available` | MFA、registrar/registry locks、变更通知和审计日志。 |
| `TA0040-T1491-REF-NIST-SP800-81R3` | NIST SP 800-81r3, `https://doi.org/10.6028/NIST.SP.800-81r3` | 权威 DNS、日志和 DNSSEC 的部署与完整性指导。 |

### Claim 与 Case 候选

- `TA0040-T1491-CLM-PARENT`：攻击者替换组织控制的内部或外部视觉内容会直接损害原展示完整性；由 ATT&CK 19.1 支持。
- `TA0040-T1491-CLM-BOUNDARY`：T1491 的直接对象是组织身份下的人类可见展示结果；改变业务数据以影响流程/理解/决策属于 T1565，网页攻陷而无可见结果不满足本候选。
- `TA0040-T1491-CLM-SOURCE-BINDING`：标识到源的 DNS 绑定可被替换，使攻击者页面在组织域名下显示而规范源服务器未被入侵；由 ICANN Hushmail 调查直接支持。
- `TA0040-T1491-CLM-DEFENSE`：DNS 控制面审计、跨解析器答案、实际 HTTP/TLS 内容与规范源差分可恢复该链；AWS、NCSC、NIST 和 ICANN 分别支持字段与控制，窗口和多观察点数量是可调实施设计而非来源测得阈值。
- `TA0040-T1491-CASE-HUSHMAIL-DNS-DEFACEMENT`：2005-04-24，攻击者通过注册商支持流程接管 Hushmail 注册账户，把 `www.hushmail.com` 指向托管篡改主页的服务器；页面持续少于六小时，正确解析多数用户约十六小时恢复，部分缓存影响持续更久；真实 Hush 服务器未被未授权访问。case 只支持展示源绑定替换，不支持按受众门控或现代 CDN 推断。

## 8. 共享库查重与决议

已运行 `library_lookup.py` 搜索 `defacement visual content website`、`DNS hijacking defacement compromised record displayed content`、`conditional content cloaking user agent referrer hacked site`、`domain registrar lock DNS change monitoring`、`multivantage web content integrity response hash`、`ChangeResourceRecordSets DNS audit content`，并以 `rg` 对 `T1491`、固定 URL 与域名锁/解析关键词做精确检查。

| 对象或近邻 | 决议 | 原因 |
|---|---|---|
| T1491 REF/CLM/CASE | **create** | 共享库中无 T1491 或固定 T1491 URL 精确对象。 |
| `REF-000524` | **reuse** | CloudTrail 通用事件字段身份完全相同；Route 53 服务字段另建 REF。 |
| `REF-000029` | **reuse for boundary** | 支持被改网页可服务侦察这一相邻结果，不支持篡改影响或 child。 |
| `DET-000047` / `NJA-000021` 条件门控投放多视角差异 | **split / no extend** | 目标是能力投放和后继执行，数据包含 staging control plane；T1491 要求批准展示状态、实际人类可见结果和影响边界。条件展示轴本批 defer。 |
| `DET-000032` / `NJA-000006` Web 主机画像与选择性响应 | **split / no extend** | 目标是客户端画像与选择性投递，确认门槛不是未经授权展示完整性。 |
| `DET-000155` 内容路径与受信终止差分 | **adjacent / no reuse** | 目标是路径介入、可读终止和内容取得；T1491 DNS child 要证明替代内容和干净规范源。可共享遥测思想，Analytic 身份不同。 |
| `DET-000165` / `NJA-000177` Web 失败至 DNS 控制序列 | **no reuse** | 检测备用 C2 的持续任务/响应，不检测 DNS 到展示结果。 |
| `DET-000180` / `NJA-000197` DNS 答案至进程控制结果 | **no reuse** | 以 DNS 承载命令和端点执行为目标，缺少发布和可见输出比较。 |
| `MIT-000131` 网络路径权威约束 | **split** | 措施集中于 DHCP/ARP/RA/LLMNR 与接入层名称解析，未覆盖注册商、权威域锁、发布内容版本和篡改恢复。 |
| `MIT-000046` 多视角投放验证 | **no extend** | 控制对象是投放服务的条件规则与租户，不是组织展示和域名权威。 |
| 新 DET/NJA/MIT | **create** | 检测目标、字段、确认门槛和缓解措施均有独立语义。 |

关系对象当前无需单独创建；父子、Technique→DET 和 MIT application 按现有规范表达即可。若主 Agent 的跨候选收敛发现另一候选建立完全相同的注册/DNS 权威控制，可在正式分配前重新评估 MIT 合并，但不得只因都使用 CloudTrail 而合并 Analytic。

## 9. 集成门禁

1. 决策为 `adapt`，`original_attack_subtechniques_imported: false`；正式 lifecycle 保持 `review`。
2. 两个 ATT&CK 子项都必须保留上述 planning-only `not-stealth-distinct` 决议，不得改名为 NJS。
3. 只为“展示源绑定替换”分配一个正式 NJS；三个 defer 轴不预留 ID。
4. 主 Agent 须与 T1565、NJT-0142、钓鱼/初始访问和 C2 做最终边界复核：可见展示、业务数据、可读中间路径和控制内容分别需要自己的结果证据。
5. DET 应含两个双向连接 NJA；父级引用 Strategy，child 由 DNS Analytic 直接覆盖。MIT 必须分别建立 parent 与 child application。
6. Hushmail 案例不得扩张到条件门控、CDN、内部 DNS 或全部现代 HTTPS；Analytics 的五分钟轮次、三个观察点与窗口是实施起点，正式文本应标注需按 TTL、发布周期和环境调优。
7. 完成正式对象后运行共享库精确/模糊查重、ID sync、`make quality`、Bundle 和双语 Web 测试；人工领域评审前不得 `published`。

**最终交接状态：** `adapt`；父技术正式编写；正式 Niji 子项 `1`（展示源绑定替换）；T1491.001/.002 均为 planning-only `not-stealth-distinct`；条件呈现、低差分覆盖、集中委托发布 `defer`；新 DET `1`、NJA `2`、MIT `1`；共享引用 reuse `REF-000524` 与边界用 `REF-000029`，其余按来源账本 create。
