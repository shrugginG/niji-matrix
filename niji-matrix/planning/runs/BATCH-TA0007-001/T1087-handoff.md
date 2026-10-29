# T1087 Account Discovery / 账户发现：只读研究交接

研究单元：`WORK-TA0007-T1087`；批次：`BATCH-TA0007-001`；临时键前缀：`D07-01-T1087-`。研究日期：2026-09-22。本文只是规划材料，不分配 NJT、NJS 或共享库正式 ID，不修改正式矩阵。下文“拟议”均待主 Agent 跨候选查重、领域审查与验证。英文段落与中文段落保持同一结论强度。

## 1. 准入建议（先于分类与 ID）

**建议 `adapt`，置信度 `medium`；`original_attack_subtechniques_imported: false`。** 保留 T1087 的直接信息对象——既有账户标识、用户名、邮箱地址或账户清单——以及 Discovery 目的；Niji 正式范围缩为攻击者有意选择读取路径、查询组织方式或时序，使账户发现相对于通常的枚举在可见性、关联或归因上发生可论证的变化。单纯运行 `net user`、列出 IAM 用户，或因业务缓存自然存在而读取地址簿，只能证明账户发现；必须再论证受控变量和防守观察差异。固定基线的四个 ATT&CK 子项是广度先验，不作为 Niji 子项名称或配额。[E01][E02]

**Recommendation `adapt`, confidence `medium`; `original_attack_subtechniques_imported: false`.** Keep T1087's direct object—the identifiers or lists of existing accounts, usernames, and email addresses—and its Discovery purpose. Narrow the formal Niji scope to intentionally chosen retrieval paths, query organization, or timing that demonstrably change visibility, correlation, or attribution compared with ordinary enumeration. Running `net user`, listing IAM users, or reading an address book that happens to be cached proves account discovery alone; a controlled variable and defender-observation difference must also be shown. The four ATT&CK children are breadth context, not Niji child names or a quota.[E01][E02]

父级可成立的最窄机理候选是 **NM-BT（行为透明），`medium`，条件性**：攻击者从已经在端点保存的身份视图取名单时，目录服务器本次不会收到一条对应的批量查询；若防守侧只观察目录/云 API，取名单这一动作落在其覆盖之外。端点文件读取、进程、邮箱下载、后续传输仍可能可见，因此不得写成“无痕”。此处的“刻意选择离线视图以匿迹”是对已观察取址行为和产品架构的推断，并无直接意图供述。[E04][E05][E06][E12] NM-ST（低频或分散查询）目前只可作 `hypothesis/defer`；NM-FD（借用常规客户端）也待异常会话与正常客户端对比证据；NM-DO 无内容变形证据，拒绝。

## 2. 固定基线与相邻边界

本地权威基线为 `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx` 的 `techniques` 工作表，T1087 位于第 16 行，四个子项位于第 17–20 行，`domain=enterprise-attack`、`tactics=Discovery`；与 `niji-matrix/matrix.yaml` 的 19.1 配置一致。在线 ATT&CK 页面用于补充定义与资料入口，不能代替本地版本冻结。[E01][E02]

| 固定基线子项 | 19.1 划分维度 | 本研究的覆盖决议 | 理由 |
|---|---|---|---|
| T1087.001 Local Account | 主机/ESXi 本地账户存储和命令 | `parent-core`；本机既存清单的读取也可为离线视图轴提供对照 | 本地存储是信息位置，`net user`、`/etc/passwd` 本身不证明匿迹；“当前用户是谁”另看 T1033。[E01][E02] |
| T1087.002 Domain Account | AD/LDAP、SAMR、域命令 | `niji-variable-candidate`（在线查询时序/范围）；未独立正式化 | 目录查询留下可观测查询痕迹，分散查询可能改变时间聚合；现有案例不证明刻意避阈值。[E01][E08][E09] |
| T1087.003 Email Account | GAL、邮箱/地址簿 | `niji-variable-candidate`（既存身份视图复用） | 已记录攻击者取用 Outlook 地址簿；缓存地址簿具本地副本，可与即时目录查询形成不同观察面；不能把所有邮件发现等同于离线读取。[E04][E05][E06] |
| T1087.004 Cloud Account | 云/IAM/IdP/SaaS 用户或角色 API | `parent-core`，在线 API 时序轴为 `evidence-deferred` | API 名称、云平台不是匿迹变量。云读操作在启用相应审计时仍可见；不同服务的日志字段和覆盖不能机械合并。[E01][E10][E11] |

广度触发为 **3–5 项：至少检验两个不同匿迹轴**。已检验下节三个轴；建议 **1 个待主审的正式 Niji 子项、2 个 defer 轴**。四比一的数量差异来自原四项按账户所在平台/介质划分，真正有资料支撑且防守面不同的控制变量目前仅“即取在线查询与已存身份视图复用”的选择；其他轴尚缺意图和独立性证据。第二轮 taxonomy 不是 3–5 项的强制门禁，当前已做跨四项的逆向核查。`subtechnique_taxonomy.coverage` 应在主审确认离线视图轴后用 `established`；若主审认为其意图证据不足，则用 `deferred`，不得为了配额凑出第二项。

| 邻项 | 判定线 | 双重活动的处理 |
|---|---|---|
| T1069 Permission Groups Discovery | 问题是“哪些组/权限存在、谁属于何组”；即使命令同时返回用户名，成员关系/授权拓扑由 T1069 主持。T1087 主持“哪些账户标识存在”。[E03] | 一个 `Get-ADGroupMember` 结果若同时用于名单与成员关系，可标注两个行为结论，不能把组查询自动当成本候选独立匿迹子项。 |
| T1033 System Owner/User Discovery | 问题是特定系统当前、主要或近期使用者/所有者；`whoami`、`$USER` 单一身份通常归 T1033。账户总体清单归 T1087。[E03] | `dscl . list /Users` 等可产生多账户清单，按实际信息目标判定；命令名不能单独决定归属。 |
| T1136 Create Account | 新增账户或建立后续凭据入口改变身份状态；本候选只读取既有身份。[E03] | 攻击者先创建、后查询确认时，将写入和读取拆成两个事件；不要复用“创建—首次使用”的检测目标当作“枚举”检测。 |
| T1078 Valid Accounts | 用已有有效凭据认证、进入或维持访问；它可为 T1087 查询提供权限，但不等于发现。[E03] | 同一会话先登录再读账户清单时，分别建模身份使用与发现；查询内容、读访问的稀有度才是本候选核心。 |

外部公开人员资料收集（T1589）、邮箱内容收集、凭据提取、权限提升及单纯登录失败的账号有效性探测也不自动落入此父级；需要看目标空间、直接输出与行为阶段。合法目录同步、帮助台批量查询、邮件客户端正常同步和安全审计是重要反例。

## 3. 结论级证据表

“直接”表示来源明言行为、产品性质或日志字段；“推断”表示由两个已证事实组合成防守观察结论。访问日期均为 2026-09-22。仅 E01 的子项数量与版本取自固定工作簿；线上页面可能随后更新。

| 键 | 一手资料及可核查 URL | 直接支持 | 可支持的结论 / 不可越级的结论 |
|---|---|---|---|
| E01 | 本地 MITRE Enterprise 19.1 工作簿：`data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx`，`techniques!A16:Q20` | T1087 定义、TA0007、四个子项、账户列表/邮箱/内置命令和文件搜索。 | 父行为与广度；不单独证明 Niji 匿迹轴、攻击意图或检测效果。 |
| E02 | MITRE ATT&CK, [T1087 Account Discovery](https://attack.mitre.org/techniques/T1087/) | 有效账户、用户名、邮箱清单及后续目标选择；平台示例与检测线索。 | 父行为补充；在线页面不得改写本地 19.1 数量。 |
| E03 | MITRE ATT&CK, [T1069](https://attack.mitre.org/techniques/T1069/), [T1033](https://attack.mitre.org/techniques/T1033/), [T1136](https://attack.mitre.org/techniques/T1136/), [T1078](https://attack.mitre.org/techniques/T1078/) | 各邻项分别关注组/权限、特定系统用户、新建账户、有效账户使用。 | 边界标准；一次事件的多个输出需按直接目的审查。 |
| E04 | Broadcom/Symantec, [Dragonfly: Western Energy Companies Under Sabotage Threat](https://www.security.com/threat-intelligence/dragonfly-energy-companies-sabotage) 与 [原研究 PDF](https://docs.broadcom.com/doc/dragonfly_threat_against_western_energy_suppliers) | Oldrea 从受害机 Outlook 地址簿取数据，写临时加密文件后发送；论文还列端点、网络痕迹。 | 实际攻击者使用既存地址簿和残余痕迹。资料未证明读取的是 OAB 文件，也未证明目的在躲避目录审计。 |
| E05 | Microsoft, [Offline address books in Exchange Online](https://learn.microsoft.com/en-us/exchange/address-books/offline-address-books/offline-address-books), [Cached Exchange Mode](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/configuration/cached-exchange-mode) | OAB 可下载并保存在端点；Outlook 缓存模式可离线用身份地址列表，常规客户端会同步更新。 | 本地既存身份视图的技术可行性；不能把 Oldrea 的 Outlook 访问直接断言为 OAB 文件读取。 |
| E06 | Microsoft, [Outlook recipient resolution with OAB](https://learn.microsoft.com/en-us/microsoft-365-apps/outlook/configuration/force-outlook-to-resolve-proxy-addresses) | 缓存模式默认用 OAB 解析收件人，相关身份/邮箱字段可索引。 | 用本机 OAB 与在线 GAL 的观察面差异是架构性推断；数据范围取决于配置。 |
| E07 | ESET Research, [Gamaredon group grows its game](https://www.welivesecurity.com/2020/06/11/gamaredon-group-grows-its-game/) | 观察到恶意 Outlook VBA 使用受害者地址簿联系人或组织联系人。 | 支持地址簿被攻击者利用；主要案例是发送/传播，不能据此说它为匿迹而离线枚举。 |
| E08 | Canadian Centre for Cyber Security, [Threat detection for SharePoint vulnerabilities](https://www.cyber.gc.ca/en/news-events/threat-detection-sharepoint-vulnerabilities) | 一起调查中，攻击者两周内向 DC 发出 19 次 LDAP 查询，收集用户、服务账户、组、管理员和邮箱资料。 | 证明跨时间的实际账户相关查询；不证明攻击者以低频避阈值，且资料混有 T1069 输出。 |
| E09 | Microsoft, [Defender for Identity classic security alerts](https://learn.microsoft.com/en-us/defender-for-identity/alerts-mdi-classic), [monitored activities](https://learn.microsoft.com/en-us/defender-for-identity/monitored-activities), [Event 1644 diagnostic guidance](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/event1644reader-analyze-ldap-query-performance) | 身份传感器可看 LDAP/SAMR；枚举告警参考异常方法、猜测数量和历史基线。1644 主要记录昂贵/低效/慢查询，受诊断配置与阈值限制。 | 设计目录侧检测和盲区；不能把 1644 当成所有成功 LDAP 搜索的完整记录。 |
| E10 | Microsoft, [Microsoft Graph activity logs](https://learn.microsoft.com/en-us/graph/microsoft-graph-activity-logs-overview), [List users API](https://learn.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0) | 若启用 Graph 活动日志，记录 RequestUri、UserId、AppId、IPAddress、状态、响应字节等；Graph 可列用户。 | 可实施云 API 关联字段；日志未启用或其他 SaaS 不具同一覆盖时需标盲区。 |
| E11 | AWS, [Logging IAM and STS API calls](https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html), [CloudTrail read management event selection](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html), [record fields](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html), [ListUsers](https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListUsers.html) | IAM `ListUsers` 是账户清单 API；CloudTrail 可记调用者、eventName、sourceIPAddress；只记写类管理事件会丢读类查询，读操作响应内容通常不在日志内。 | 云侧检测和日志配置的必要条件；不能从一条 ListUsers 事件推断实际返回的用户名数。 |
| E12 | Microsoft, [Windows event 4663](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4663), [4688 command-line audit](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing) | 4663 可显示受 SACL 管控对象的实际访问；4688 命令行须另启策略。 | 端点取名单分析的可实施遥测；默认不保证 OAB 每次读取都有 4663。 |
| E13 | Microsoft, [Exchange Online address book policies](https://learn.microsoft.com/en-us/exchange/address-books/address-book-policies/address-book-policies), [assign an ABP](https://learn.microsoft.com/en-us/exchange/address-books/address-book-policies/assign-an-address-book-policy-to-mail-users) | ABP 限定用户可见 GAL/OAB 视图；未分配时可见全组织 GAL；ABP 是目录视图虚拟隔离。 | 缓解“暴露面”而非强制安全隔离；不会删除已同步的历史副本。 |
| E14 | Microsoft, [Graph user delta](https://learn.microsoft.com/en-us/graph/api/user-delta?view=graph-rest-1.0) | 合法客户端可用增量接口跟踪账户变化，避免每次完整读取；需相应授权。 | 证明增量/低量形态也是正常业务，削弱“低量即恶意”的判定，不能把该 API 本身命名为 Niji 子项。 |
| E15 | Microsoft Security, [2026 identity/cloud intrusion report](https://www.microsoft.com/en-us/security/blog/2026/09/09/passkey-themed-social-engineering-leads-identity-cloud-compromise/) | 一起入侵中，攻陷云身份后使用 Graph 枚举租户用户，另枚举组/角色并访问数据。 | 实际在线云账户发现案例与 T1069/T1078 边界；未给出刻意分散请求、借客户端拟态或避审计证据。 |

**证据等级与案例使用。** E04 可提议 CASE `D07-01-T1087-CASE-01`（Oldrea/Dragonfly），事实仅到“从 Outlook 地址簿获取联系人并留下暂存/发送痕迹”；E08 可提议 CASE `D07-01-T1087-CASE-02`，事实仅到“两周内 19 次混合 LDAP 查询”；E15 可提议 CASE `D07-01-T1087-CASE-03`，事实仅到“攻陷身份后用 Graph 列用户及分别查询组角色”。三者均不得写成已证实“匿迹策略成功”。E04 对具体 OAB 文件没有结论级支撑，故离线视图子项只以产品能力 + 实际地址簿利用组成 `medium` 推断；若正式对象需要确证 OAB 读取，须再找端点取证来源或降为 `deferred`。

## 4. Niji 原生分类：变量、痕迹、防守差异

| 轴与结果 | 攻击者可控变量 / 前提 | 行为 → 痕迹变化 → 防守影响 | 兄弟边界与防御价值 |
|---|---|---|---|
| **A. 既存身份视图复用 / Reuse of a Preexisting Identity View**；**建议 1 个有条件正式子项**，临时键 `D07-01-T1087-SUB-01`，`medium` | 已取得可读取身份材料的端点/邮箱会话，攻击者选择用现成地址簿、已同步 OAB 或本地账户清单，而非在该次操作中向身份权威发起新批量查询。不能把“平台是邮箱”当变量。 | 读取现成身份视图 → 权威侧少了一次本该与即时枚举对应的查询，端点文件/应用访问、暂存与传输仍可见 → 只盯权威查询的检测可能漏掉取名单。E04 证明地址簿被取用，E05–E06 证明可本地使用；“攻击者刻意避权威审计”仍是推断。[E04][E05][E06][E12] | 与 B 的区别是**查询发生的位置/时点**，不是查询速率；防守需端点身份材料读取与客户端谱系，而非仅拉长目录窗口。限制：OAB 可能未同步、范围陈旧/受 ABP 限定；合法 Outlook 常读这些材料；Oldrea 例并未证实 OAB 文件访问。 |
| **B. 跨时段小量查询 / Temporally Dispersed Small Queries**；`defer`，`hypothesis` | 攻击者拆分账户清单请求、延长间隔或分散来源。 | 局部窗口请求数下降 → 单窗口告警可能不触发、长时同一主体聚合才还原范围；每次 LDAP/API 仍有可见事件。[E08][E09][E11] | 候选 NM-ST。E08 观察到两周 19 次，但未说明为避检测而刻意安排，且混合用户/组/邮箱目标；不能正式声称稳定匿迹子项。可以先做长窗 Analytic 验证。 |
| **C. 既有业务客户端/权限借道 / Existing Workflow and Principal Context**；`defer`，`hypothesis` | 已掌握有效会话或应用授权，并以常见客户端/正常业务路径读取账户清单。 | 命令进程可能消失而应用/API 日志仍存在；日志中“正常”AppId/会话可能增加归因难度，但异常扇出、访问时间和授权范围仍可比较。[E10][E11][E15] | 与 A 不同，它仍向权威发在线请求；与 T1078 不同，核心仍是取名单。E15 证明攻陷身份 + Graph 枚举，却未证明客户端拟态或检测混淆，故不能给 NM-FD 正式化。 |

**拒绝的伪轴：** 本地/域/邮件/云是账户位置；`net user`/`ldapsearch`/Graph 是工具或协议；用户/管理员/服务账户是目标类别；加密传输是常规协议性质。它们可改变检测适配器，却未自行满足“稳定受控变量 → 迹象变化 → 防守观察差异”。NM-DO 需要信息内容或语义被刻意改变，当前没有对应证据。公开人员资料和登录表单的用户名差异推断需由 T1589/身份工作流对象主审，不能借 T1087 名义导入。

## 5. 父级双语核心字段建议（读者正文草案，不是正式 YAML）

**Name / Summary.** 账户发现 / Account Discovery。中文：攻击者获取受害环境中既有账户标识；当其有意改变获取路径或查询节奏，使读取动作偏离防守方的观察与关联范围时，构成此处的匿迹型账户发现。English: An adversary retrieves identifiers of existing accounts in the victim environment; the Niji scope covers a deliberate change of retrieval path or query organization that moves this reading activity outside effective defensive observation or correlation.

**Definition and concept.** 中文：账户发现读取系统、目录、邮箱或云身份空间中的既有账户名、地址及其清单，直接目的是确认哪些身份存在，以便后续筛选目标。行为由“取得既有身份集合”界定，不由产品、命令或账号种类界定。Niji 在此关注发现行为如何安排观察面；获取凭据、创建身份和使用身份是相邻而不同的事件。English: Account Discovery reads existing usernames, addresses, or account lists from systems, directories, mail environments, or cloud identity spaces to establish which identities exist for later selection. The behavior is defined by acquisition of an existing identity set rather than a product, command, or account category. Niji examines the observation path of that acquisition; credential acquisition, account creation, and account use are separate neighboring events.

**Stealth characteristics.** 中文：同一批账户名可以由权威目录的即时搜索取得，也可以从端点已保留的身份视图恢复。后者会改变“本次取名单”在目录侧的痕迹，而端点读取、进程活动、缓存更新和后继传输可能仍在。低频或常用应用会话本身不足以认定匿迹；只有来源、时间或客户端选择实际改变了防守方的可见性和关联能力，才在本范围内。English: The same identities can be obtained through an immediate authoritative directory query or recovered from a view already held on an endpoint. The latter changes the directory-side trace of the current retrieval, while endpoint reads, process activity, cache updates, and later transfer may remain visible. Low volume or a familiar client session alone does not establish stealth; source, timing, or client choice must actually change defender visibility or correlation.

**Scope boundary.** 中文：纳入既有账户清单的有意取得，以及有证据支持的观察面转换。排除仅识别当前登录用户的 T1033、以组成员关系为直接目标的 T1069、增加账户的 T1136、利用有效身份访问的 T1078，也排除无匿迹变量的普通运维查询。单条查询可同时暴露用户名与组关系，分类应按提问目标和实际结果分别记录，不按命令名互斥。English: Include deliberate acquisition of existing account sets when evidence supports a change of observation surface. Exclude T1033's identification of a current user, T1069's direct pursuit of group membership, T1136's account creation, T1078's use of valid identity, and ordinary administrative queries without a stealth variable. A single query may reveal both usernames and group relationships; classify the actual questions and outputs separately instead of enforcing exclusivity by command name.

**Application scenario.** 中文：在取得低权限主机、邮箱或云会话后，攻击者可能先识别可用身份，再决定钓鱼、口令尝试或下一步权限调查。已同步的地址簿提供无需本次权威枚举即可检视的候选名单；在线目录/API 查询则可能用于新鲜或更完整的信息，但其请求在对应审计面留下记录。[E01][E04][E05][E15] English: After gaining a low-privilege host, mailbox, or cloud session, an adversary may identify available identities before phishing, password attempts, or further privilege investigation. A synchronized address book can offer candidates without a fresh authoritative enumeration for that retrieval; online directory and API queries may provide fresher or broader data but leave requests in the corresponding audit surface.[E01][E04][E05][E15]

**Attacker model.** 中文：攻击者至少需要能读取某个身份空间或其副本；若选择既存视图，还需端点/邮箱访问及可读取的缓存，并接受资料陈旧或可见范围受限。若选择云 API，必须有对应会话与读取权限。当前资料不支持默认假定管理员权限、跨源协同或大规模自动化。English: The adversary needs access to an identity space or a copy of it. Reusing a preexisting view additionally requires endpoint or mailbox access and a readable cache, while accepting stale or scoped data. Cloud API retrieval requires a session and relevant read permission. The present evidence does not justify assuming administrator privilege, coordinated sources, or large-scale automation by default.

**Defender model.** 中文：防守方可能拥有目录传感器、Graph 活动日志、CloudTrail 读类管理事件、端点进程与文件访问遥测，并能按主体、会话和时间关联。若只保留目录侧查询，则无法直接看到已在端点的资料被再次读取；若未配置 4663 的 SACL、未启用 Graph 活动日志或只记 CloudTrail 写类管理事件，相应视图会缺失。保留、正常同步基线和跨端点身份映射决定结论强度。English: The defender may have directory sensors, Graph activity logs, CloudTrail read management events, endpoint process and file-access telemetry, and correlation by principal, session, and time. Directory-only retention cannot directly see a local reread of previously held identity data. Without a file SACL for 4663, enabled Graph activity logging, or read management-event capture in CloudTrail, those views are missing. Retention, normal synchronization baselines, and cross-endpoint identity mapping determine conclusion strength.[E09][E10][E11][E12]

**Mechanism proposal.** `NM-BT`, primary, `medium` conditional. Summary zh：复用端点既存身份视图绕开本次权威枚举痕迹；en: Reuse an endpoint-held identity view outside the current authoritative query trail。分析：选择已下载/可用的地址视图 → 本次取名单不需要等量目录搜索 → 只看权威请求的防守方看不到此读取 → 端点文件/应用活动和后续外传仍可揭示。E04–E06 支持行为和架构，E12 支持剩余端点痕迹；主审如要求直接证明攻击者刻意离线避审计，应降为 hypothesis/defer。`NM-ST` 和 `NM-FD` 暂不写入正式机制表。

**Limitations.** 中文：公开案例证明账户发现和地址簿利用，产品资料证明存在端点缓存，但两类来源合起来只能支持“可能避开本次目录查询”的架构性推断，不能证明具体入侵曾故意这样规避检测。合法 Outlook 同步、帮助台、目录同步和云管理会造成相似读取；1644、4688、4663、Graph 与 CloudTrail 的启用条件不同，缺少任何一层都可能改变结论。English: Public cases establish account discovery and address-book use, while product documentation establishes endpoint caching; together they support an architectural inference that a current directory query may be avoided, not proof that a particular intrusion intentionally evaded detection this way. Legitimate Outlook synchronization, help-desk work, directory sync, and cloud administration create similar reads. Event 1644, 4688, 4663, Graph, and CloudTrail have different enablement requirements, so missing any layer changes what can be concluded.

## 6. 条件性子项 `D07-01-T1087-SUB-01` 的双语核心字段

**Name / Summary.** 既存身份视图复用 / Reuse of a Preexisting Identity View。中文：从攻击者已能读取的身份副本恢复账户标识，将当前取名单动作从权威目录查询面转移到端点或应用访问面。English: Recover account identifiers from an identity copy already accessible to the adversary, moving the present retrieval from authoritative directory queries to endpoint or application access.

**Definition and concept.** 中文：本子项描述攻击者在获得端点或邮箱访问后，利用现成地址簿或其他已同步的身份清单识别多个既有账户，而不是为同一批名字立即向权威身份服务发起新枚举。稳定变量是取名单所依赖的数据视图是否已经在可读位置，不是 Outlook、OAB 或邮件账户这一产品与目标类别。English: This child describes identifying multiple existing accounts through an already available address book or other synchronized identity list after endpoint or mailbox access, without immediately issuing a new authoritative enumeration for those same names. Its stable variable is whether the identity view already resides at an accessible location, not Outlook, an OAB, or an email-account category.

**Stealth characteristics.** 既存身份视图复用使本次账户读取不一定出现在目录查询流中；若防守分析只统计 LDAP、SAMR 或云列表 API，就可能低估攻击者取得的身份范围。文件读取、客户端异常、临时加密文件和外传仍是可观察残余；定期同步也可能在历史时段留下下载记录。Reuse of a Preexisting Identity View may leave the current retrieval outside directory-query streams, so analysis limited to LDAP, SAMR, or cloud listing APIs can underestimate the identities obtained. File reads, client anomalies, temporary encrypted files, and transfer remain observable, while periodic synchronization may have left earlier download records.[E04][E05][E12]

**Scope boundary.** 中文：纳入“攻击者选择读取既有身份副本以得到多账户标识”，且能说明其相对于即时查询改变了哪一侧的痕迹。若攻击者刚触发完整 OAB 下载，则该下载本身是可见的在线访问，不能把它写成纯离线；若只提取当前用户名归 T1033，若读取组关系则相应事实归 T1069。正常 Outlook 浏览和经授权的目录导出是反例。English: Include an adversary's choice to read an existing identity copy for multiple account identifiers when its trace difference from an immediate query can be stated. A newly triggered full OAB download is itself visible online access and must not be called purely offline. Reading only the current username belongs to T1033; group relationships belong to T1069. Ordinary Outlook browsing and authorized directory export are counterexamples.

**Application scenario.** 中文：在已控制使用缓存模式的工作站或可访问邮箱地址簿的会话后，攻击者从该用户本可见的名单筛选后续接触对象；其覆盖仅限该用户已同步和允许查看的身份，资料可能滞后。English: After obtaining a cached-mode workstation or a session able to access a mailbox address book, an adversary selects later contacts from identities visible to that user. Coverage is limited to what the user could see and had synchronized, and the data can be stale.[E04][E05][E13]

**Attacker / defender model.** 中文：攻击者需要读取既存视图的访问权，不预设目录管理权；若能运行任意进程或恶意邮件客户端，还可能留下异常进程和材料暂存。防守方若有端点文件访问、进程链、邮件客户端与网络传输记录，可在缺少即时目录搜索时恢复这段行为；若仅保留目录日志则盲。English: The adversary needs read access to the existing view, without presumed directory administration. Arbitrary process execution or a malicious mail client may leave unusual process and staging traces. Endpoint file access, process lineage, mail-client activity, and transfer records can recover the behavior even when no immediate directory search appears; directory-only monitoring is blind to the local read.[E04][E12]

**Mechanism / limitations.** `NM-BT`, primary, `medium` conditional. 中文：选择端点既存身份视图 → 本次查询不进入权威服务 → 权威侧检测无法单独判断是否取名单；端点、下载与传输仍可见。Oldrea 证明地址簿利用，但不能推断它必定读取 OAB 文件或刻意规避日志。English: Selecting an endpoint-held identity view means the current lookup need not reach the authoritative service, so authority-side detection alone cannot establish whether the list was read; endpoint, download, and transfer traces may remain. Oldrea demonstrates address-book use, not necessarily OAB-file access or deliberate log evasion.[E04][E05][E06][E12]

## 7. 可实施防御候选与限制

以下只有临时键。所有关联窗口是**工程起点/推断**，不是来源验证的最佳阈值；主审须以环境基线校准。DET 为检测目标，NJA 为实现；正式引用时须双向连接。MIT 的每个应用需由主 Agent 在正式目标确定后单独落地。

### `D07-01-T1087-DET-01`：跨观察面的账户清单读取 / Account-list Retrieval Across Observation Surfaces

目标：识别在线目录/API 批量或异常账户读取，以及没有相应即时在线查询、却在端点集中消费既有身份副本的行为；分别输出在线与本地证据，避免凭缺失日志反证无查询。域 `enterprise`；拟议覆盖父级和条件性子项。可组织下列两个 NJA；如共享库身份需要不同目标，也可拆 DET。

**`D07-01-T1087-NJA-01`：在线身份目录读取关联 / Online identity-directory read correlation。**

- 数据要求：AD 身份查询遥测（确有产品事件时：`timestamp, principal, source_host, protocol, query_target, query_filter_or_operation, result_status`）；Graph activity（`TimeGenerated, UserId, AppId, IPAddress, RequestUri, RequestMethod, ResponseStatusCode, SessionId, ResponseSizeBytes`）；CloudTrail 读类管理事件（`eventTime, eventSource, eventName, userIdentity, sourceIPAddress, recipientAccountId, readOnly, errorCode`）；授权同步作业登记（`principal, application, host, approved_scope, approved_window`）。按环境选择有覆盖的适配器，不要求同时有 AD、Graph、AWS。Graph 字段与 CloudTrail 字段见 E10–E11；不要把 1644 当全量普通 LDAP 明细。[E09][E10][E11]
- 逻辑：把真正返回或请求账户对象的操作规范化为 `identity-list-read`，按主体/会话/客户端/租户和查询目标聚合；在 30 分钟窗口检查稀有读取、首次出现客户端、跨多身份对象的连续访问，在 7–30 日窗口检查同一主体或可证明相同会话谱系的分散读取。比较该主体获授权目录同步的对象范围与时间，而非只用高次数阈值。账户数只能从确实记录返回对象的来源计算；CloudTrail 读事件不能据此估算返回名单。与登录成功、组成员查询和账户创建分别关联作为上下文，不把它们作为此检测的必要条件。
- 可观测输出：陌生主体/应用读取用户目录；异常时段的身份 API 查询；一段时间内多个小量目录读取汇合。误报：目录同步、HR 导入、帮助台、威胁狩猎、租户迁移。盲区：Graph 活动日志未启用；CloudTrail 只记写类管理事件；LDAP 只有 1644 阈值事件；加密/代理后的主体归属缺失；超留存期低频活动。调优：按主体职能、目录大小、同步频率和权限范围建基线；授权同步可降低权重，但对新设备、新 AppId、超批准范围和高价值身份保留告警。[E08][E09][E10][E11][E14]

**`D07-01-T1087-NJA-02`：端点既存身份视图的异常读取 / Anomalous reading of an endpoint-held identity view。**

- 数据要求：对试点端点 OAB/地址簿目录启用对象访问审计并配置有效 SACL 后的 4663（`timestamp, host, user, process_id, process_name, object_name, access_mask`）；4688/EDR 进程（`timestamp, host, process_id, parent_process_id, image, command_line, signer`）；若可得，邮件客户端 OAB 同步或下载记录（`timestamp, user, device, address_book_id, download_type`）和后续网络传输（`timestamp, host, process_id, destination, bytes_out`）。OAB 文件路径按本机 Outlook 配置发现，不硬编码全局目录。[E05][E12]
- 逻辑：识别非批准邮件客户端或异常进程链对可读地址视图的短时多次访问，结合身份名单临时文件、异常传输或已知恶意进程上下文提高风险。比较最近一次正常同步及该用户的平常客户端；没有同窗目录查询只是“本次未观察到”，不能作为恶意性的独立证据。初始关联窗：端点访问至暂存/传输 30 分钟；同步基线 7 日；均须环境校准。
- 可观测输出：非常用进程读取身份副本并暂存/发送；客户端启动后异常遍历通讯录。误报：首次 Outlook 启动、全量 OAB 重建、索引/备份/EDR 扫描、经授权的邮箱迁移。盲区：未配 SACL、进程内读取不可区分、应用内地址簿 API 无文件事件、内容端到端加密、旧缓存已从端点转移。调优：以批准进程签名和用户平常访问范围加权，不能把 Outlook 进程名本身全局白名单化；敏感端点先试点 SACL 以控制事件量。[E04][E05][E12]

### 缓解候选

**`D07-01-T1087-MIT-01`：账户可见范围与读权限治理 / Account Visibility and Read-Permission Governance。** `exposure-reduction` + `preventive`。措施一：定期审查 AD/云目录和 Graph 应用的用户清单读取授权、服务主体与批准同步范围，收回非必要广域读权限；措施二：在需隔离联系人视图的 Exchange 场景按租户业务边界配置 ABP/GAL/OAB，检查用户确有分配并测试不同会话所见名单；措施三：在适用成员机上约束匿名 SAM 枚举。父级应用：减少低权限身份能看到的总名单及后续目标池，但无法阻止仍被授权的主体、泄露的旧缓存或其他可见渠道。子项应用：缩小今后同步到端点的地址列表范围，但已下载的副本必须按端点数据治理另行处置；ABP 只是视图分段，不应宣称为完整安全隔离。[E10][E13]

**`D07-01-T1087-MIT-02`：端点身份副本访问与留存治理 / Endpoint Identity-Copy Access and Retention Governance。** `exposure-reduction` + `detective-support`。措施一：盘点可缓存 OAB 的设备与账户，限制非必要共享端点对缓存的访问，按产品支持的方式管理受管设备的缓存生命周期；措施二：在高风险端点为 OAB/身份视图建立可承受事件量的对象访问审计或 EDR 文件访问覆盖，并与客户端/进程/传输日志关联。父级应用：把权威查询之外的身份材料消费纳入观察；子项应用：减少攻击者复用既存视图的机会并增加端点痕迹。限制：合法 Outlook 必须读其 OAB；访问审计有性能与噪声成本；无法追回外传过的副本，也不能保证所有应用内读取可见。[E05][E12] 此 MIT 与 MIT-01 的控制动作不同，宜 `split`。

## 8. 全局共享库复用 / 新建 / 延迟决议建议

已用 `library_lookup.py` 查询 `T1087`、`Account Discovery`、`LDAP`、`address book`、`account enumeration`、`identity directory`，并读取相关正式对象。相似名不等于语义复用；下列结论供主 Agent 作精确查重。

| 类型 | 建议 | 身份理由与临时键 |
|---|---|---|
| REF | `reuse` `REF-000094`（T1078 边界）、`REF-000165`（T1136 边界）；`REF-000303` 仅在引用联合 AD 防御一般原则时复用，不把其 Skeleton Key 内容当账户枚举证据。 | `REF-000034` OWASP 登录/恢复响应差异适用于身份工作流推断，与本次内部清单读取不同；只作边界参考。E01 的 T1087 固定父来源、E04–E15 的结论级一手资料需逐 URL 查重后以 `D07-01-T1087-REF-*` 提议新建。 |
| CLM | `create` 两项原子结论：`D07-01-T1087-CLM-01` 既存地址簿可提供账户标识且可能避开本次权威查询（明确“推断”、E04–E06）；`D07-01-T1087-CLM-02` 云读类日志缺失会使列表 API 检测失效（E10–E11）。 | 不扩充现有“账户创建—首次使用”或“身份工作流响应差异”主张。低频匿迹意图 `defer`，不能用 E08 越级证明。 |
| CASE | `create` 候选 E04 Oldrea、E08 Canadian Centre 调查、E15 Microsoft 云入侵；都需在主审检查已有同一事件案例后决定 `reuse/create`。 | 案例只写来源直接记录的动作，不把推断子项或匿迹成功归于攻击者。 |
| DET/NJA | `create` `D07-01-T1087-DET-01`、`NJA-01`、`NJA-02`；若正式 review 认为两个观察面目标不同，可 `split` DET。 | `DET-000033`/`NJA-000007` 研究登录/注册/恢复响应差异；`DET-000069` 等研究账户状态变化；两者均不满足本设计的数据和逻辑身份，不能直接扩充覆盖引用。 |
| MIT | `create` MIT-01、MIT-02，或与经主审确认同措施的全局控制作 `extend`。 | `MIT-000032` 是外部公开身份暴露治理，非受害环境内部目录/OAB 读权限；`MIT-000068` 是创建账户治理；不能按名称相似复用。 |
| REL | `defer` 独立关系对象。 | T1069/T1033/T1136/T1078 的边界在范围段已足够；若主 Agent 需要可查询的“先登录→取名单”关系，须先确认关系类型、事件证据和跨技术指向。 |

## 9. 主审前未决事项与质量对照

1. **子项入库闸门：** 查找有端点取证证明某一攻击者确实读取 OAB/本地既存身份视图且权威查询未发生或明显减少的案例；目前 E04 是地址簿利用，E05–E06 是产品架构，不能写成同一事件的 OAB 取证。没有这类证据时可将 SUB-01 保持 `hypothesis` 并把正式 `subtechnique_taxonomy.coverage` 设为 `deferred`。
2. **时序轴：** E08 的两周 19 次查询是行为观察，缺乏对刻意避阈值的意图及与正常同步对照。若未来来源呈现分拆逻辑、时间安排及告警差异，再复审 NM-ST；目前不得正式化。
3. **客户端拟态轴：** E15 证实攻陷身份与 Graph 枚举，却未证实伪装正常客户端；需原始 AppId/UserAgent、会话谱系及正常同职能基线后再审 NM-FD。
4. **跨技术审查：** 组成员与用户名可能来自同一 API；应让 T1069 主审组/权限结论。只见单一当前用户需交 T1033；账户新建交 T1136；有效账户登录交 T1078。对外公开身份信息由 T1589/相邻对象审查。
5. **NJT-0001 字段责任核对：** 上文分别给出定义/目的、可控痕迹、纳入与反例、场景、攻击与防守模型、因果机理、证据限制；子项另说明独立变量、前提、残余痕迹与专用防守。双语核心内容是独立写作的完整自然段；正式化时仍须按 `technique-field-specification.md` 和 `defense-object-specification.md` 校验 2.0.0 YAML、机理证据覆盖、DET↔NJA、MIT application、双语等价与 Web 展示。当前无正式字段、无分配 ID、无运行正式质量门禁。

