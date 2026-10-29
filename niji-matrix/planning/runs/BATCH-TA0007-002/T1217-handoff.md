# T1217 Browser Information Discovery / 浏览器信息发现：只读研究交接

批次：`BATCH-TA0007-002`；工作项：`WORK-TA0007-T1217`；临时键：`D07-02-T1217-*`；研究日：2026-09-22。此文件只提出研究结论，不分配正式 ID，不改正式矩阵或共享库。

## 1. 准入建议先行

**建议：`adapt`；置信度 `medium`；原 ATT&CK 子技术不导入。**

**中文理由。** T1217 在已入侵环境中读取浏览器保留的书签、访问历史及设置，以恢复用户曾接触的站点、内部入口和工作习惯，具有独立的 Discovery 信息对象。CISA 联合通告明确报告攻击者枚举书签，Volexity 对 ICONICSTEALER 的分析明确给出历史标题和 URL 的提取；这足以保留父行为。Niji 需要将范围改写为“保留的浏览上下文发现”：账户标识清单交给 NJT-0131，当前窗口和焦点交给 NJT-0132，密码、Cookie 和会话令牌提取交给 Credential Access，批量资料获取、暂存与外传交给 Collection 或 Exfiltration。父级的匿迹判断限于攻击者复用既有浏览记录时，本次发现不必产生相应的新网页导航，而会转成端点读访问与后继结果；这一观察面差异是由恶意读取和浏览器存储架构合并推得的中等置信结论，不是案例已证明的规避意图或检测成功率。

**English rationale.** T1217 has a distinct Discovery object after compromise: browser-retained bookmarks, visit history, and settings can reveal previously used sites, internal entry points, and work habits. A joint CISA advisory reports adversarial bookmark enumeration, and Volexity documents ICONICSTEALER extracting history titles and URLs. That supports a parent technique. Niji should adapt its scope to discovery of retained browsing context: identity-list acquisition belongs to NJT-0131, current window and focus to NJT-0132, passwords, cookies, and session tokens to Credential Access, and bulk acquisition, staging, or transfer to Collection or Exfiltration. The parent stealth proposition is narrow: rereading stored browsing context need not create fresh navigation to the same sites and instead leaves endpoint reads and possible follow-on outcomes. That observation shift is a medium-confidence inference joining malicious-read evidence with browser storage architecture, not proven evasion intent or measured detection efficacy.

**固定基线确认。** `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx` 的 `techniques` 工作表第 85 行是 `T1217`，`name=Browser Information Discovery`，`domain=enterprise-attack`，`tactics=Discovery`，`is sub-technique=0`，平台 Linux/Windows/macOS，URL 为 `https://attack.mitre.org/techniques/T1217`。检查 `sub-technique of=T1217` 的行数为 **0**；本候选无 ATT&CK 子项覆盖表触发，但仍完成开放式 Niji 轴搜索。固定版父描述包括书签、账户、历史以及本地文件或数据库；账户字样不能自行证明 NJT-0131 意义上的多账户身份枚举。ATT&CK 页面用于父锚点，不作 Niji 子项、机理或检测字段的单独证据。[E01]

## 2. 结论级一手证据与限制

以下键均为本交接的临时键。`观察`表示来源直接陈述的案例或产品事实，`推断`表示需要联合来源与防守模型才能成立，绝不把“工具能力”升格为已发生的行动。

| 临时键、来源与 URL | 可支持的结论层级 | 不能支持的升级 |
|---|---|---|
| **D07-02-T1217-E01** MITRE ATT&CK Enterprise T1217，`https://attack.mitre.org/techniques/T1217/` | 固定父行为、Discovery 映射、无 ATT&CK 子项、示例与 ATT&CK 检测线索。 | 不能单独证明某个 Niji 原生轴、规避意图、Windows 审计字段或缓解效果。 |
| **D07-02-T1217-E02** CISA/Treasury/FBI/USCYBERCOM 联合通告 AA20-239A，`https://content.govdelivery.com/accounts/USDHSCISA/bulletins/29bf7dc` | **观察/联合通告判断：** BeagleBoyz 枚举浏览器书签，用于了解主机、用户及内部网络资源。这是书签发现的恶意活动证据。 | 通告明确把技术分析写成多个事件的汇总；未给出单一事件的书签文件访问序列、同步副本、查询时序或规避审计意图，不能凭此建离散 CASE。 |
| **D07-02-T1217-E03** Volexity 对 3CX/ICONICSTEALER 样本分析，`https://www.volexity.com/blog/2023/03/30/3cx-supply-chain-compromise-leads-to-iconic-incident/` | **样本分析：** DLL 内嵌 SQLite3，从 Brave、Chrome、Edge、Firefox 取浏览历史标题与 URL，输出上限 500 条并交由上游组件 POST；支持本地历史读取与可能的后继传输。 | “前 500 条”没有证明按最近访问时间筛选；作者仅推测可能据此选择后续载荷，不能当成已观察的时间线门控或匿迹动机。 |
| **D07-02-T1217-E04** Mandiant 3CX 应急调查，`https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise` | **调查/样本定义：** ICONICSTEALER 收集应用配置和浏览历史，可交叉确认父行为与配置对象。 | 没有同一终端的读文件事件、浏览器同步记录或检测率；与 E03 属同一事件，不能算两个独立攻击案例。 |
| **D07-02-T1217-E05** Google Chrome Enterprise 漫游配置文档，`https://support.google.com/chrome/a/answer/7349337?hl=en` | **产品架构：** 漫游配置可含书签、自动填充、密码、部分历史、偏好与扩展；本地 `profile.pb` 可位于 `%APPDATA%` 或另设位置；该模式与 Chrome 云同步互斥。 | 不能证明攻击者读取 `profile.pb`，也不能把漫游文件、云同步与本机配置合称一种已观察的恶意路径。 |
| **D07-02-T1217-E06** Google Chrome Sync 数据说明，`https://support.google.com/chrome/a/answer/13616205?hl=en`；Microsoft Edge 企业同步文档，`https://learn.microsoft.com/en-us/deployedge/microsoft-edge-enterprise-sync` | **产品架构：** 在相应设置下，书签/收藏夹、历史等可跨设备同步；保留内容和策略依部署而异。 | 不能证明攻击者从云端或另一台设备取了同步副本；Google 文档对 Enterprise 用户历史处理另有范围限定，不能概括为所有租户都同步历史。 |
| **D07-02-T1217-E07** Chrome History API 文档，`https://developer.chrome.com/docs/extensions/reference/api/history` | **产品能力：** 具有 `lastVisitTime`、`visitTime` 等时间字段和 `history` 权限要求；历史可以按时间查询。 | 能按时间查不等于攻击者确实按时间筛选，更不等于有独立规避效果。 |
| **D07-02-T1217-E08** Microsoft Windows Security 4663 与 Audit File System，`https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4663`、`https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-file-system` | **日志合同：** 目标文件有匹配 SACL 且启用审计时，4663 可提供对象路径、进程路径/PID、SID、访问权限；`ReadData` 代表文件数据读取。 | 默认不保证发出读取事件；4663 不记录所读 URL/书签内容，也不能凭单次事件判定恶意。 |
| **D07-02-T1217-E09** Microsoft Sysmon 文档，`https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon` | **日志边界：** Event 1 可用于进程谱系，Event 3 为网络连接，Event 11 为文件创建；Event 10 是跨进程访问，非普通浏览器历史文件读取。 | 不能把 Event 11 或 Defender `DeviceFileEvents` 泛称为可靠“文件读”日志；需单独验证 EDR 是否真的提供读事件。 |
| **D07-02-T1217-E10** Microsoft App Control 文档，`https://learn.microsoft.com/en-us/windows/security/application-security/application-control/introduction-to-virtualization-based-security-and-appcontrol`；Edge `SavingBrowserHistoryDisabled`，`https://learn.microsoft.com/en-us/deployedge/microsoft-edge-browser-policies/savingbrowserhistorydisabled` | **控制能力：** 应用控制可限制未获准代码运行；Edge 策略可阻止新历史保存，并同时禁用标签页同步。 | 控制不能追回既存副本，也不能阻止已获准进程中的恶意代码；关历史的功能代价必须由业务评估。 |

**原子结论候选。** `D07-02-T1217-CLM-PARENT`：入侵后读取浏览器保留的 URL、标题、书签或配置属于独立 Discovery 信息对象，E01/E02/E03/E04 支持，`high`。`D07-02-T1217-CLM-SURFACE`：复用历史无需同站点新导航，导致网页访问遥测与本次端点读取分离，E03/E05/E08/E09 联合支持，**推断、medium**。`D07-02-T1217-CLM-BOUNDARY`：密码/Cookie 提取与纯浏览上下文发现需按直接目的拆开，E01/E03/E05 支持范围界定，但混合载荷必须允许多技术标注。案例候选 `D07-02-T1217-CASE-3CX` 只记 Volexity/Mandiant 共同覆盖的 3CX/ICONICSTEALER 行为；CISA BeagleBoyz 是多个事件的综合分析，只用于 Claim，不据此新建离散 Case。

## 3. 原生匿迹轴搜索与收敛

搜索入口分别为恶意活动报告（E02–E04）、浏览器厂商存储/同步合同（E05–E07）、端点审计合同（E08–E09），没有用平台、产品、浏览器字段或 ATT&CK 子项构造 NJS。轴之间的直接对象仍是“已保留的浏览上下文”，而非密码、身份清单或网页正文。

| 候选轴与独立检索 | 攻击者可控变量 → 痕迹 → 防守效果 | 处理与证据门槛 |
|---|---|---|
| **既存本地记录读取**：E03 恶意样本；E05 本机/漫游结构；E08/E09 审计。 | 选择读取既有浏览历史/书签而非重新访问站点 → 可能没有本次对应的新网页请求，产生文件读、进程和可能外传痕迹 → 只看网页导航的检测漏掉发现环节。 | **正式化于父级，零 NJS。** 这是 T1217 最典型的取得方式，若单列子项会把父行为自身复制一遍。E03 证实恶意读取；“避开网页导航日志”是架构推断，未证实主观匿迹。 |
| **同步或漫游副本复用**：E05/E06 独立架构来源；另查 E02–E04 的恶意案例，均未证明从同步副本取数。 | 选择在另一设备或同步位置消费已存在副本 → 本次原设备没有相应读取，可能留下云同步、另一端点文件或账户访问痕迹 → 若防守只监视原设备，观察域可能错位。 | **暂缓 `defer`。** 产品能力清楚，但无结论级恶意证据、权限路径与实测防御差异。不能照搬 NJT-0131 的“既存身份视图复用”；浏览器副本若主要是身份清单仍归该项。 |
| **历史时间窗/先后顺序选择**：E07 证明时间字段；E03 的 500 条限制；再查 CISA E02 与 Mandiant E04。 | 可选择只取近期记录、特定时段或访问顺序 → 数据量及潜在暂存/外传量变化 → 数据量规则可能较弱，后续选择可能更贴近用户活动。 | **假设 `hypothesis`，不正式化。** E03 未说明 500 条的排序、时间谓词或规避理由；E07 只是 API 能力。需样本代码或同案指令证实时间谓词，以及与全量读取不同的检测/缓解模型。 |
| **分批/低频重读**：以 E03 的单次上限为启发，检索恶意报告 E02–E04 和端点事件合同 E08/E09。 | 控制每次读取量与间隔 → 小批多次的读和出站事件 → 短窗口阈值可能漏看，长窗口可恢复同一进程谱系。 | **假设 `hypothesis`，不正式化。** E03 只给上限，不证明跨时段重复、低频策略或告警规避；需要同一主体多次读的时间线及与正常同步区分。 |
| **进程内或扩展 API 取历史**：E07 权限与 API；E09 进程事件边界；搜过 E02–E04，未证明这些案例经扩展 API 完成发现。 | 攻击者若控制已获准浏览器/扩展的执行路径 → 独立陌生进程的文件读取可能消失，转为扩展权限或同进程活动 → 端点文件规则可能失效。 | **暂缓 `defer`。** 缺少本候选内实际恶意调用证据及可取得的扩展审计字段。扩展安装/驻留另属持久化或执行边界，不能把工具形式直接当 NJS。 |

**分类结论：`subtechnique_taxonomy.coverage=none-justified`，正式子项 0。** 这不是“ATT&CK 没有子项所以 Niji 也没有”的推断；五条原生轴已分别以恶意案例、架构和防守合同检视。本地读取是父级核心，其他轴欠缺恶意实例、稳定变量或差异化防御。未来若获得恶意同步副本消费、时间谓词或跨时段读序列，应重新审查；目前不能凭合理设想给 NJS 身份。

## 4. 与已有对象和相邻行为的判定边界

| 邻项 | T1217 的可判定界线 |
|---|---|
| `NJT-0131` 账户发现与 `NJS-0131-001` 既存身份视图复用 | 直接问题若是“有哪些用户/账户标识”，尤其地址簿或账户名单，则归 NJT-0131；浏览器历史里偶然出现登录名不自动改变 T1217 主体。T1217 问的是“用户曾去过哪些站点、入口或工具”。同步副本概念相似，但身份副本子项不能无证据扩成浏览历史子项。 |
| `NJT-0132` 应用窗口发现与 `NJS-0132-001` 窗口上下文门控 | 当前打开、前台、标题/焦点状态归 NJT-0132；浏览器长期保留的历史与书签归 T1217。历史中曾访问某银行站点不证明当前窗口条件门控，不能引用 Grandoreiro 案例为 T1217 子项。 |
| Credential Access：浏览器密码、Cookie、令牌；TA0009 Collection；Exfiltration | 把密码、Cookie 或令牌作为直接目标时，归凭据/会话窃取；读取 URL/书签以识别入口仍属 Discovery。整库复制、打包、传送是可并行标注的 Collection/Exfiltration 结果，不让传输行为替代发现分类。ICONICSTEALER 的历史提取与 POST 可分别标注。 |
| `T1083` 文件与目录发现、`T1518` 软件发现、其他站点情报 | 仅找浏览器安装路径/文件名是文件或软件发现；读保留的浏览上下文才是 T1217。对网页正文/云内容的读取按其直接对象另判。 |
| 正常行为 | 用户浏览、恢复配置、IT 支持、取证、备份、索引和批准的同步会读取相同材料。仅凭路径命中、SQLite 库或无新网络请求不判定恶意；需进程来源、授权用途、读取组合与后继活动。 |

## 5. 可供主 Agent 改写的父级双语核心字段

**临时父键 `D07-02-T1217-PARENT`；名称：浏览器信息发现 / Browser Information Discovery。** 以下为研究正文建议，不是已分配的 NJT YAML。

**summary** — 中文：攻击者读取已保留的浏览上下文以识别曾访问的站点与环境入口；这可使本次发现与新的网页导航脱钩。 English: An adversary reads retained browsing context to identify visited sites and environment entry points, potentially separating this discovery from new web navigation.

**definition_and_concept** — 中文：浏览器信息发现是在获得受害环境访问后，读取浏览器先前保存的书签、历史标题与 URL、偏好或扩展配置，从中确认用户曾使用的外部服务、内部仪表板或其他环境入口。其直接目的在于形成后续目标地图，而不是访问那些站点本身。浏览器只是这些记录的载体，分类以“恢复既有浏览上下文”为准，不按 Chrome、Edge、Firefox 或某个文件格式区分。 English: Browser Information Discovery occurs after access to a victim environment when an adversary reads browser-retained bookmarks, history titles and URLs, preferences, or extension configuration to identify services, internal dashboards, and other entry points the user has used. The direct purpose is to build a map for later targeting, not to visit those sites now. The browser carries the records; the defining act is recovering existing browsing context rather than using a particular browser or file format.

**stealth_characteristics** — 中文：读取已保存记录可以把“知道哪些站点”与“本次访问哪些站点”分开。若防守方仅以代理或浏览器导航日志重建发现活动，本次端点读取可能没有相应的新站点请求，尤其当记录来自较早会话时；攻击者仍会留下进程执行、对象访问、临时文件或网络结果，且没有读访问审计时不能把缺失事件当成未发生读取。此差异并不表明攻击者专为躲避审计而选用历史，现有案例也没有测出规避成功率。 English: Reading stored records can separate knowledge of a site from a visit to it during the current operation. A defender reconstructing discovery only from proxy or navigation logs may see no new request corresponding to the endpoint read, particularly when the record came from an older session. Process execution, object access, temporary files, or network outcomes can remain visible, and missing read events without read auditing do not prove that no read occurred. The difference does not establish that the adversary chose history to evade logging, and the cases do not measure evasion success.

**scope_boundary_definition** — 中文：纳入恶意主体有意取用已保留的站点、访问脉络和浏览器配置，以识别环境入口或用户工作方式。仅枚举账户名单、读取当前窗口状态、取密码/Cookie/令牌，或获取网页正文与批量打包外传，按各自直接对象或后继行为另记；混合载荷可多技术标注。用户恢复、合法同步、企业迁移、帮助台与取证可能产生相似读取，需要结合主体、获准用途、读出的信息类别和后继动作。 English: Include intentional adversarial consumption of retained sites, visit context, and browser configuration to identify environment entry points or user work patterns. Account-list enumeration, current window state, passwords, cookies, tokens, page content, and bulk packaging or transfer belong to their respective direct objects or follow-on acts; a mixed payload may receive multiple technique labels. User recovery, approved synchronization, enterprise migration, support, and forensics can produce similar reads, requiring actor, authorized purpose, information category, and follow-on context to distinguish them.

**application_scenarios** — 中文：在受控交互工作站或可访问的用户配置目录上，攻击者可在选择下一目标前查看历史或书签；这些记录可能暴露管理入口、金融站点或常用服务。3CX 样本显示恶意代码提取多个浏览器的标题和 URL 并交给上游组件；CISA 通告显示书签可用于认识内部资源。记录的时效与覆盖取决于用户浏览习惯、保留策略和配置位置。 English: On a controlled workstation or accessible user-profile directory, an adversary may inspect history or bookmarks before selecting later targets; the records may reveal administrative entry points, financial sites, or commonly used services. The 3CX sample extracted titles and URLs from several browsers for an upstream component, while the CISA advisory describes bookmark enumeration for knowledge of internal resources. Freshness and coverage depend on user habits, retention policy, and profile location.

**attacker_model** — 中文：攻击者至少需要已访问主机上的用户权限、可读配置副本，或能代表用户读取浏览器记录的执行路径。若数据在本机文件或 SQLite 数据库，读权限及文件占用状态会限制方法；若是漫游或云同步副本，还要另外证明该副本存在、同步范围与可用会话。现有证据不支持默认假定攻击者持有浏览器云账户、利用历史时间谓词，或能避开所有终端监控。 English: The adversary needs at least user-level access to an affected host, a readable profile copy, or an execution path able to read browser records for the user. Local files or SQLite databases impose read-permission and file-state constraints; a roaming or cloud-synchronized copy additionally requires proof of its existence, synchronization scope, and usable session. Current evidence does not justify assuming control of a browser cloud account, use of a history-time predicate, or evasion of all endpoint monitoring.

**defender_model** — 中文：防守方可能拥有代理/网页访问、进程、文件对象访问和出站网络记录，但这些来源观察的是不同时间与位置。浏览器导航日志只证明真正发生的请求；要看见本次配置读取，受管 Windows 终端须为目标路径配置并验证 4663 或验证等效 EDR 读事件，再用主机、SID、PID/进程创建时间与后继暂存/网络结果关联。仅有 Sysmon 文件创建事件不能补足读取盲区，且合法浏览器与备份作业会带来高噪声。 English: A defender may have proxy or navigation records, process events, file-object access, and outbound-network logs, but these cover different times and locations. Navigation logs establish requests that actually occurred. To observe a present profile read on managed Windows, the defender must configure and verify 4663 on relevant paths or validate an equivalent EDR read event, then join host, SID, PID and process start to staging or network outcomes. Sysmon file-creation events alone cannot fill the read gap, and ordinary browsers and backups create heavy noise.

**stealth_mechanism candidate** — `NM-BT`，`primary`，`medium`（E03/E05/E08/E09，明确标记架构推断）。摘要：中文“复用已存浏览记录使本次发现离开新网页导航观察面”；English “Reuse stored browsing records to move present discovery outside fresh web-navigation telemetry”。分析：恶意进程读取已保存的历史或书签，便能获知站点而无需在这一步再次访问它；网页代理侧因此不必出现与本次发现对应的新请求，单靠当前导航量的检测会低估所知入口。端点读、进程、暂存与外传仍可见。Volexity 证明恶意本地历史提取，浏览器/Windows 文档说明存储与可审计面，尚无案例证明规避动机或量化效果。 English: A malicious process can learn sites by reading existing history or bookmarks without revisiting them during this step. A web proxy therefore need not receive a fresh request corresponding to the present discovery, so current-navigation-only detection can underestimate the entry points learned. Endpoint reads, processes, staging, and transfer may remain visible. Volexity demonstrates malicious local history extraction and vendor documentation explains storage and audit surfaces; no case establishes evasion motive or quantified impact.

**subtechnique_taxonomy** — 中文：本轮不建立正式子技术。已检索的本地、同步、时间、分批和应用内路径分别是父级核心或尚无足够恶意与防守差异证据的假设，浏览器产品和历史字段不形成兄弟边界。 English: No formal child is proposed in this pass. The searched local, synchronized, temporal, batched, and in-application paths are either parent-core or hypotheses lacking enough adversarial and defensive-difference evidence; browser products and history fields do not define sibling boundaries. `coverage=none-justified`，`subtechnique_refs=[]`。

**研究限制** — 中文：公开资料证明书签/历史被恶意取用，但没有同案的文件读、同步事件与代理记录联结，也没有攻击者主动规避导航审计的陈述。4663 必须预先配置对象 SACL，且路径、权限与浏览器配置方式会变；对没有端点读遥测的环境，只能较弱地从暂存或外传推断发现。若取得恶意同步副本访问、明确时间筛选代码及同案检测数据，再重校子分类。 English: Public sources establish adversarial bookmark and history use but do not join file reads, sync events, and proxy records for the same incident, nor document a deliberate choice to evade navigation auditing. Event 4663 requires a preconfigured object SACL, and paths, permissions, and browser profile handling vary. Where endpoint-read telemetry is absent, discovery can only be inferred more weakly from staging or transfer. Malicious synchronized-copy access, explicit time-selection code, and same-incident detection data would justify revisiting the child taxonomy.

**子级双语核心字段状态。** `proposed_subtechniques=[]`；没有可安全书写为正式 NJS 的名称、summary、定义、匿迹特性、威胁模型、机理或独立防御引用。上述五轴是研究条目而非未编号的正式子项；给它们填完整子级字段会把证据不足伪装成准入已通过。 / `proposed_subtechniques=[]`; no child has sufficient support for a formal bilingual name, summary, definition, stealth profile, threat model, mechanism, or distinct defense reference. The five axes above remain research entries rather than unnumbered formal children.

## 6. 可实施防御候选：DET → NJA 与 MIT

**`D07-02-T1217-DET-LOCAL`：浏览器保留信息异常读取关联 / Correlation of Abnormal Retained-Browser-Information Reads。** 覆盖父级、域 `enterprise`。目标是在受管端点识别非惯常主体读取浏览配置/历史后出现的可归属结果，而不是仅凭书签路径报警。它与 `DET-000140` 都处理端点既存资料，但后者的目标是身份副本与目录查询盲区；若把两者合并，目标对象、正常客户端、路径基线及分析调优会变宽，建议新建或拆分，勿直接 extend。

**`D07-02-T1217-NJA-READ`：浏览器配置读取与后继结果谱系 / Browser-Profile Read and Follow-On Lineage。** 平台先限 Windows，试点可执行逻辑如下。先按用户和已部署浏览器盘点实际配置路径与批准客户端，给高价值终端的目标文件设置 `ReadData` SACL 并验证 Security 4663 发出；基于 `Computer + SubjectUserSid + ProcessID + TimeCreated` 与 Sysmon Event 1 的主机、PID、进程创建时间联结，恢复进程 GUID、父进程、签名和用户。聚合同一谱系短窗内对历史/书签/偏好等对象的读，比较用户和设备的批准浏览器、同步、备份、取证任务基线。若同一谱系后续创建临时输出、压缩包或连向异常目的地，则提高优先级；没有这些后继结果的异常读取仍可作为低优先级 Discovery 线索，不能为了提高精度要求一定外传。不要把“没有新导航”作为必需条件或恶意证据，它只是解释网页日志为何不覆盖此行为。

数据合同：`windows-security-object-access`，通道 `Security 4663 + matching SACL`，必需字段 `TimeCreated, Computer, SubjectUserSid, ProcessID, ProcessName, ObjectName, AccessMask`；`endpoint-process-lineage`，通道 `Sysmon Event 1` 或验证过的等效 EDR，字段 `UtcTime, Computer, ProcessGuid, ProcessId, ParentProcessGuid, Image, User`；可选结果通道 `Sysmon Event 11`（输出文件创建）与 `Sysmon Event 3`（已启用的网络连接），字段分别需时间、主机、进程 GUID、目标路径或目的地址/端口。可选 EDR 若声称文件读，须先核实具体 `ActionType`；`DeviceFileEvents` 文档本身不保证泛化读访问。观测量是未经批准谱系的配置读、多个浏览资料对象的连续读取、同谱系短时暂存/网络结果。试点关联窗建议读至结果 **30 分钟**、正常任务基线 **7 天**；这是待本地验证的分析参数，不是来源实测阈值。主键为主机、SID、进程创建时间/Guid、对象路径与时间；跨子进程要有父子谱系，不能只用相同用户名和时间邻近。

误报：浏览器自身数据库维护、个人资料恢复、索引/备份、企业迁移、响应取证、浏览器更新和获准扩展可能大量读；调优按业务 owner、签名与实际进程谱系和时间窗设例外，避免永久放行签名为浏览器的进程。盲区：未配置 SACL、应用内接口/内存读取、数据先前被复制、恶意代码注入批准进程、E03 的 SQLite 库本身无可用读日志、不同浏览器路径和日志留存不足。优先在少数高价值端点验证字段、事件量及隐私影响，再扩展；不要从一次 4663 声称取到了具体 URL。E03/E08/E09 为逻辑与字段证据，阈值和误报处置为待试点推断。

**`D07-02-T1217-MIT-EXPOSURE`：浏览记录暴露面与读取问责 / Browser-Record Exposure and Read Accountability。** 可实施 Measure A（`exposure-reduction`）：按业务需要选择浏览器配置与历史保留/同步策略，减少高敏工作站不必要的跨设备历史副本；Edge 的 `SavingBrowserHistoryDisabled` 可阻止新历史保存，但会影响标签同步，不能全组织盲开。Measure B（`detective-support`）：盘点实际配置目录，在高价值终端试点 4663/SACL 或经验证的 EDR 文件读遥测，保留进程和结果谱系。Measure C（`preventive`）：按环境适用性启用应用控制以限制陌生可执行代码与脚本，但不把它描述为禁止合法浏览器读自身配置的文件 ACL。

**针对父级的唯一 Application。** `use`：对浏览器保留信息发现，缩小未来可保留/同步的工作浏览记录，记录批准的同步和恢复主体，并把异常端点读与后继输出归于同一进程谱系。`expected_effect`：未来可暴露的历史范围减少；未批准读取更容易与正常浏览器维护区分，攻击者可能需要转用受监测的其他路径或接受较少上下文。`limitations`：现存历史、已同步副本与已外传数据不会自动消失；关闭历史可能损害业务功能与取证；4663 有部署和事件量成本，获准/注入进程仍可能读。English: Reduce future retention and synchronization where justified, inventory approved readers, and join unusual endpoint reads with outcomes in the same process lineage. This reduces future exposure and improves attribution but does not retract existing copies, may impair useful history and tab features, requires scoped auditing, and cannot prevent reads by allowed or injected processes. E05/E06/E08/E10 支持控制能力；目标级效果是审慎推断，待试点确认。

**逐目标说明。** 由于正式子项为零，DET/NJA/MIT 只提议直接覆盖父级 `D07-02-T1217-PARENT`；不得为五个被暂缓轴预填适用目标。若主 Agent 后续让某轴入库，须重新审查其独立 Analytic 与 MIT Application，而非沿用本父级结果。

## 7. 共享库决议建议与交接门槛

| 候选 | 建议 | 原因 |
|---|---|---|
| E01–E10 `REF` | `create`，先按 URL/标题查重；E03/E04 两条来源、一个 3CX 案例。 | 只读 `rg` 检索 `T1217/ICONICSTEALER/BeagleBoyz/Roaming User Profiles` 未在当前共享库找到同名对象；主 Agent 仍须以 catalog 做正式判重。 |
| `D07-02-T1217-CLM-PARENT/SURFACE/BOUNDARY` | `create`，其中 SURFACE 明记推断及 `medium`。 | NJT-0131 的“既存身份视图”Claim 对象是账户清单，不能把它 extend 成站点历史。 |
| `D07-02-T1217-CASE-3CX` | `create` 或同一活动的已有 CASE 经核查后 `reuse/extend`；BeagleBoyz CASE `defer`。 | 3CX 的 Volexity 和 Mandiant 是同一事件不同一手视角。CISA 明示为多事件综合分析，不具备一个离散 CASE 的事件时间线与目标。 |
| `DET-000140` / `NJA-000145` | 对 T1217 `split/create`，不要直接 `extend`。 | 现有对象针对地址簿/身份副本，虽共享 4663+谱系方法，信息目标、合法基线、关联逻辑和调优不同；新 DET/NJA 可复用方法而不复用身份。 |
| `MIT-000129` | 对 T1217 `split/create`，不直接 `extend`。 | ABP/GAL/OAB 缩限不能降低浏览器历史暴露；可借鉴端点审计 Measure，但控制概念与父级 Application 必须重写。 |
| `DET-000141` / `MIT-000130` | `defer` 任何 T1217 复用。 | 这组对象针对当前窗口和窗口条件门控，不检测或缓解保留浏览记录读取。 |
| 同步副本、时间谓词、分批与扩展 API 的子项/防御对象 | `defer`。 | 尚缺结论级恶意实例与独立防守价值，主 Agent 不应预留 NJS 或关联库 ID。 |

**交接质量结论。** 已逐项对照 NJT-0001 所要求的定义、匿迹特性、边界、应用场景、攻防模型、机理、证据限制与防御合同；本交接刻意把实际恶意行为、厂商架构和分析推断分层。父级可进入主审的 `adapt` 评估，子分类本轮建议 `none-justified`；正式内容仍需主 Agent 的共享库查重、人工语义审查、编号、机器校验与双语 Web QA。没有研究证据可支持同步副本取用、历史时间线选择或定量规避效果的正式声称。
