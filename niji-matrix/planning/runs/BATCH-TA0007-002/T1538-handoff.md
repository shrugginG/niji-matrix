# T1538 Cloud Service Dashboard / 云服务控制台：只读研究交接

- 批次 `BATCH-TA0007-002`；工作项 `WORK-TA0007-T1538`；所有新对象暂存键前缀 `D07-02-T1538-*`。
- 固定基线：`/home/shrugging/project/theory_research/data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx`，`techniques` 工作表。第 97 行为 Enterprise/Discovery 父项 T1538、名称 Cloud Service Dashboard、技术版本 1.5、`is sub-technique=0`；逐行核查 `sub-technique of=T1538` 得 **0 个 ATT&CK 子项**。Niji 不继承 ATT&CK 子项：`original_attack_subtechniques_imported: false`。在线 ATT&CK 页只辅助解释，不能替换冻结基线。
- 本文是准入研究，不是正式 Technique/DET/NJA/MIT。建议正式 NJT **0**、NJS **0**；未分配正式 ID，未修改矩阵或共享库。

## 1. 准入建议：exclude（中高置信度）

**中文理由。** 冻结的 T1538 行确立了攻击者凭窃取的凭据阅读云服务 GUI 控制台，取得服务、资源、功能等环境信息的 ATT&CK 行为；因此本建议并不否认 T1538 或控制台调查价值。Niji 的直接信息对象门槛却未通过：资源/配置属于 T1580，服务能力和安全/日志服务属于 T1526，容器内对象键属于 T1619；仪表板主要规定交互入口和呈现方式。Google Security Command Center（SCC）的资产与发现可由控制台查看，也有资源搜索与发现 API；AWS Systems Manager Inventory 有控制台卡片与 `GetInventory` API。现有一手来源没有证明攻击者能稳定控制一种**仅属于 GUI 的**信息选择变量，使同一目标调查相比 API 路径产生可重复的匿迹痕迹差和专属防御。登录和读请求还可能留下控制面审计。以 GUI、新浏览器页或“未手工调用 API”直接正式化，会把身份使用或相邻发现重复成另一父项。故建议把 GUI 作为相邻发现的 `access_path`/来源上下文记录，不单独建立 Niji 父项或子项。

**English rationale.** The frozen T1538 row establishes an ATT&CK behavior: an adversary uses stolen credentials to read cloud service dashboards for information about services, resources, and features. The exclusion recommendation does not deny that behavior or the value of investigating console activity. For Niji admission, however, resource and configuration inventories belong to T1580, enabled services and security or logging capabilities to T1526, and object keys inside storage containers to T1619. The dashboard primarily specifies an interaction and presentation path. Google Security Command Center exposes assets and findings in the console as well as resource search and findings APIs; AWS Systems Manager Inventory has console cards and a `GetInventory` API. The reviewed primary sources do not establish a stable **GUI-specific** attacker-controlled information-selection variable that reproducibly changes traces and calls for a defense distinct from the API path to the same target. Sign-ins and read requests can also leave control-plane records. Treating a GUI, browser page, or absence of manually issued API calls as sufficient would duplicate identity use or adjacent discovery. Record GUI as access-path and provenance context for those objects; do not create a separate Niji parent or child now.

**准入事实与推断分层。** 父行为与零 ATT&CK 子项是固定版事实。控制台和 API 能查询相近信息、控制台登录及部分实际服务请求可审计，受官方文档直接支持。由这些事实推到“目前不够 Niji 独立性”是本批分类判断，置信度中高；它不宣称所有产品的 GUI 与 API 完全等价，也不宣称每次浏览页面都有后端 API 事件。若以后得到结论级对照证据，主审可重新审查 `adapt`，但当前不得用仅有的架构可能性顶替机制证据。

## 2. 结论级一手证据与限制

| 暂存源键或现有 REF | 一手来源与 URL | 可支持的具体结论 | 不能升级成的结论 |
|---|---|---|---|
| `D07-02-T1538-REF-ATTACK` | 上述本地固定工作簿第 97 行；[MITRE T1538](https://attack.mitre.org/techniques/T1538/) | T1538 的父行为、Discovery 归属、GUI 和凭据语境、零子项。父页写的是“不必**手工**发起 API 请求”。 | 不证明浏览器服务请求不存在、没有 CloudTrail/Audit 事件、GUI 比 API 更隐蔽，或任何 Niji 子项成立。在线页面可能变化。 |
| `D07-02-T1538-REF-SCC-CONSOLE` | [Google SCC 控制台使用说明](https://docs.cloud.google.com/security-command-center/docs/how-to-use-security-command-center)、[SCC 资产与资源说明](https://docs.cloud.google.com/security-command-center/docs/assets-resources-overview) | 控制台呈现风险概览、资产、发现及相关配置；资产页由 Cloud Asset Inventory 提供元数据；可按组织/项目等范围查看。 | 显示的每个像素、聚合风险分数或导航行为均有租户可见逐页日志；也不证明攻击者用此界面规避了监控。 |
| `D07-02-T1538-REF-SCC-API` | [Google SCC `ListFindings` 指南](https://docs.cloud.google.com/security-command-center/docs/how-to-api-list-findings)、[Cloud Asset Inventory `searchAllResources` API](https://docs.cloud.google.com/asset-inventory/docs/reference/rest/v1/TopLevel/searchAllResources) | 安全发现与资源搜索并非 GUI 独占；访问仍受 IAM 范围和权限控制。 | 不保证 API 与任意控制台页面逐字段、逐版本完全相同；不能推断日志覆盖相同。 |
| `D07-02-T1538-REF-SSM-UI-API` | [AWS Systems Manager Inventory](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-inventory.html)、[Inventory 聚合与 `GetInventory`](https://docs.aws.amazon.com/systems-manager/latest/userguide/inventory-aggregate.html) | Inventory 卡片显示托管节点元数据，聚合数量也可通过 API 取得；证明 CISA 案例中的信息对象并不天然由 GUI 独占。 | 不证明 CISA 案例实际用了 GUI 或 `GetInventory`，也不证明两路径请求序列完全相同。 |
| `D07-02-T1538-REF-CISA` | [FBI/CISA AA23-320A，表 12，第 8 页](https://www.cisa.gov/sites/default/files/2023-11/aa23-320a_scattered_spider_0.pdf) | Scattered Spider 使用 AWS Systems Manager Inventory 识别横向移动目标；是父行为相关的真实活动证据。 | 公告未披露具体 GUI 页面、请求序列、控制台/API 比较、匿迹意图、漏报率。故不新建“GUI 匿迹”CASE。 |
| `D07-02-T1538-REF-AWS-LOGIN` | [AWS CloudTrail 控制台登录事件](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-aws-console-sign-in-events.html) | `ConsoleLogin` 示例包含身份、时间、源 IP、`userAgent`、成功状态及 MFA 信息；控制台登录不是当然无痕。 | 不能用缺少一条新 `ConsoleLogin` 推定没有既存会话浏览；不同身份/联合登录路径和区域须按部署核验。 |
| `D07-02-T1538-REF-AWS-EVENT` | [CloudTrail 事件字段](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html)、[管理读取事件](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html) | `AwsApiCall`、`AwsConsoleAction`、`AwsConsoleSignIn` 是不同事件类型；读管理事件可记录 `Describe*` 等调用。`sessionCredentialFromConsole=true` 出现时可提示控制台会话来源；该字段可选，`userAgent` 是线索。 | `sessionCredentialFromConsole` 不出现不等于 CLI；`AwsConsoleAction` 不等于逐页导航日志；`userAgent` 不能独立证明 GUI；审计项必须按启用状态和服务实测。 |
| `REF-000206`（现有） | [AWS Systems Manager CloudTrail 说明](https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-cloudtrail-logs.html) | 官方明确：Systems Manager 控制台及代码发出的 API 调用可形成 CloudTrail 事件；管理事件历史与数据事件覆盖不同，持久保留需配置 trail/Lake。 | 不能由此推断所有页面渲染都产生一个 API 事件，或任意组织已保留所需日志。 |
| `D07-02-T1538-REF-GCP-AUDIT` | [Google Cloud Audit Logs](https://docs.cloud.google.com/logging/docs/audit)、[Data Access 配置](https://docs.cloud.google.com/logging/docs/audit/configure-data-access) | 资源配置/元数据读取等用户驱动 API 调用可写 Data Access 日志；除 BigQuery 外通常默认关闭，需按权限类型启用。 | 默认关闭是**配置盲区**，不是 GUI 固有的匿迹属性；不能断言任意 SCC 页面事件都等于一条 Data Access 记录。 |
| `REF-000307`、`REF-000376`（现有） | [Microsoft Entra 登录详情](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-in-log-activity-details)、[交互式登录](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-interactive-sign-ins) | 交互登录可提供身份、来源、设备/浏览器及资源上下文，用于控制台身份链关联。 | 登录成功不能证明之后具体浏览的页面或获得的信息。 |
| `D07-02-T1538-REF-ADJACENT` | [MITRE T1580](https://attack.mitre.org/techniques/T1580/)、[T1526](https://attack.mitre.org/techniques/T1526/)、[T1619](https://attack.mitre.org/techniques/T1619/)；直接归属仍以本批冻结工作簿和 brief 为准 | 三个相邻信息对象分别是资源实体、服务能力、容器内对象。 | 在线页的后续修订不能改写 19.1 的候选库存，也不自动决定 Niji 准入。 |

**原子研究结论。** `D07-02-T1538-CLM-01`：T1538 确有控制台环境读取行为，证据为固定行与 MITRE，置信度 high。`D07-02-T1538-CLM-02`：SCC 与 SSM 示例显示控制台呈现的信息至少部分可经 API 得到，证据为两家厂商的控制台与 API 文档，置信度 high，范围限于这些示例。`D07-02-T1538-CLM-03`：AWS 控制台登录及实际 Systems Manager 服务请求有可配置的审计路径，GCP 元数据读取日志依配置而定，证据为官方日志文档，置信度 high；这不等于任何浏览器页面都被完整记录。`D07-02-T1538-CLM-04`：现有证据未满足独立 Niji 匿迹变量及专属防御门槛，是中高置信度的**准入判断**，不应伪装成厂商或 CISA 的实测结论。

## 3. 零子项广度先验与独立匿迹轴搜索

固定 ATT&CK 子项数 **0**、ID `[]`、所代表的子项维度 `[]`；没有要逐项覆盖的 ATT&CK 子项，也没有 6+ 第二轮强制触发。仍独立检查了身份、请求来源、查询强度、预聚合视图、范围选择、页面遥测六类潜在轴。**正式化：无；假设：两个；暂缓或归邻：其余；拟议 Niji 子项数 0。** 下表的“痕迹差”区分直接证实、可能性与反证；不能把前提或传感器缺失算作攻击者可控的子项变量。

| 轴与独立检索线索 | 可控变量 → 痕迹 → 防守效果 | 决议与门槛结果 |
|---|---|---|
| **GUI 入口相对手工 CLI/API**：检索 MITRE T1538、AWS CloudTrail 事件/SSM 日志、Google SCC 控制台/API | 攻击者可选择用浏览器；可留下 `ConsoleLogin`、会话来源、实际服务读取调用或产品级页面记录。不同入口能改变来源线索，但未证明同等信息任务下减少或模糊可观察请求；若有 `sessionCredentialFromConsole` 反而可能增强归因。 | `parent-core` 访问路径；不是独有信息对象。**否决“GUI=无 API/审计痕迹”**。按 GUI/CLI/API 复制 NJS 不合格。 |
| **沿用已认证会话、免新登录**：检索 AWS 登录事件、Entra 交互登录和既有 `NJS-0061-002` | 攻击者若控制现存会话或 Cookie，可减少新的认证/MFA事件；资源读取仍可能留痕。 | `adjacent-technique`：稳定身份/会话变量已属 NJT-0061 的既存会话复用，不是 T1538 所独有；API 路径同样可用。 |
| **低频、窄范围阅读相对批量枚举**：检索 CloudTrail 读管理事件、GCP Data Access 和 MITRE DET0291 | 攻击者可减少每次查询范围、次数或拉长间隔；已启用的服务读日志可能更稀疏，短窗口阈值易漏，但登录和读请求仍在。 | `hypothesis`，由通用计数/窗口逻辑推断；缺控制台对 API 同等任务的请求数量、时间和检测率对照，也缺 T1538 独立于 T1580/T1526/T1619 的信息对象与防御。可在相邻候选研究低速读取，不正式化此处。 |
| **读取预聚合或缓存视图**：检索 SCC 风险/发现页与 `ListFindings`、SSM Inventory 卡片与 `GetInventory` | 攻击者可选既成视图而不自行枚举底层资源；理论上查询数或关联路径可能变化。视图本身可能由后台服务请求、缓存或租户事件实现，不能在文档层定量比较。 | `hypothesis`、`evidence-deferred`。SCC/SSM API 的存在削弱 GUI 独占论；如将来证明特定服务中的汇总风险信息对象独立，应作为跨入口 Niji 缺口另审，而非按仪表板产品分 NJS。 |
| **组织/项目/区域过滤与范围切换**：检索 SCC scope 说明、Cloud Asset `searchAllResources` 与 SSM 跨区域清单 | 攻击者可选择较小作用域，可能减少被观察到的目标数；但 API 同样支持 scope/filter，较小范围也可能只是权限与业务任务结果。 | `not-stealth-distinct`；过滤字段不是子项。若主动选择低监控区域或改变治理层级，需按相邻区域/层级匿迹行为另证。 |
| **只浏览页面以避开后端审计**：检索 CloudTrail `AwsConsoleAction`/`AwsApiCall`、GCP Data Access、Microsoft 页面审计活动 | 页面本地呈现、服务器处理、云服务 API 与租户可见日志是不同层。若浏览器缓存显示已有内容，可能没有新的特定后端读取；若页面请求服务则可能有。缺什么事件取决于服务与日志开关。 | `defer`，尚无针对 T1538 的实测页面到请求到日志映射，且日志开关不由当前攻击者必然控制。不能把“看不到页面事件”写成独立 NM-BT/NM-ST。 |
| **正常管理员外观/熟悉来源**：检索 Entra 登录、既有 `NJS-0061-001/-003` | 选用受害者身份、设备、位置或低反馈账户可让认证片段接近日常；服务读取依然需要对象和时序调查。 | `adjacent-technique`：既有 NJT-0061 的登录情境合形、低反馈身份选择；正常管理员浏览、SOC 调查、帮助台与云盘点是强反例。 |

**机理映射。** 本候选没有达到正式 Technique 所要求的至少一项独立 `stealth_mechanism`。`NM-BT` 的“页面/服务日志分离”在缺少日志时是监测覆盖问题，未证明由 T1538 受控行为设计所致；`NM-FD` 的合法管理员外观属于有效身份与情境，不由 dashboard 创造；`NM-ST` 的稀疏/预聚合阅读目前是跨入口、跨信息对象假设。因而不为填充字段而建立机制或 NJS。针对零子项的双语分类结论：**中文**“当前没有一种仅因使用控制台而成立、能够稳定改变痕迹并要求独立防御的原生划分；任何将来成立的读取强度或预聚合变量须先证明与信息对象的归属和相邻父项的区别。” **English** “No native partition currently shows that using a dashboard alone reliably changes traces and calls for a distinct defense; any future read-intensity or pre-aggregated-view variable must first establish its direct information object and boundary against adjacent parents.”

## 4. 相邻候选及已有 NJT 的边界

| 直接对象/条件 | 归属建议 | 控制台在证据中的作用 |
|---|---|---|
| 实例、快照、网络、存储桶、数据库、配置关系；SSM Inventory 识别托管节点目标 | T1580 候选；主审作最终准入 | GUI 可作为来源路径；CISA 只证明使用 Inventory，未证明 GUI 或独立匿迹。 |
| 已启用或可用的 CI/CD、身份、安全、日志、计算等服务能力及其防护状态 | T1526 候选；主审作最终准入 | GUI 上的“服务目录/安全服务卡片”不改变信息对象。SCC 风险发现若超出服务有无，应作为新信息对象缺口另审。 |
| 已知桶/容器内的对象名称、前缀和元数据 | T1619 候选；主审作最终准入 | 浏览器文件列表只是访问路径；真实下载/收集另判。 |
| 凭据/既存会话、登录位置与设备合形、低反馈身份 | 已有 `NJT-0061`、`NJS-0061-001/-002/-003` | 控制台浏览可成为后继结果，不重建身份匿迹子项。`REF-000307/376` 可支持身份遥测边界。 |
| 已访问端点的浏览器历史、书签、配置 | T1217 候选 | 浏览器内查看云控制台的**云端**状态不等于读取端点浏览器保留信息。 |
| 账户清单；当前窗口/标题 | 已有 `NJT-0131` / `NJT-0132` | 控制台可能显示账户或窗口，需按直接查询对象分别判断；“打开了控制台窗口”不是云信息已被读取的证据。 |

## 5. 父级双语核心字段：仅供排除决策与相邻对象引用

以下文字**不**构成正式 NJT，也不应因字段齐全而自动转为 YAML。子级核心字段不适用：建议子项数零，无子项名、定义、机理或父级编号。

**名称与 summary。** 云服务控制台 / Cloud Service Dashboard。中文：攻击者利用已认证会话经云服务图形界面阅读环境信息；本候选的 GUI 路径未被证明具有独立于信息对象的匿迹因果。English: An adversary uses an authenticated session to read environment information through a cloud service GUI; the GUI path has not been shown to create stealth causality independent of the information object.

**definition_and_concept。** 中文：T1538 描述攻击者用被盗凭据进入云服务 GUI，并阅读当前运行环境的资产、服务、配置或安全发现视图，以选择后续目标。它规定交互界面和呈现方式，而直接取得的具体环境事实取决于被打开的视图；“无需手工调用 API”只说明人的操作方式，不是底层请求或日志性质。English: T1538 describes an adversary entering a cloud-service GUI with stolen credentials and reading asset, service, configuration, or security-finding views to choose later targets. It specifies an interaction and presentation path, while the information obtained depends on the view. “No manually issued API requests” describes the operator's workflow, not the underlying requests or their logging.

**stealth_characteristics。** 中文：在已获准的账号与正常管理界面中阅读，认证和页面访问可能外观类似合法运维；少量、窄范围读取也可能不触发批量枚举阈值。但这些可能性分别取决于身份情境、读取强度、服务实现与日志配置，均未被证实为 T1538 独有机理。控制台登录、实际服务请求、可用的页面遥测及后继动作仍是残余线索；如果日志未启用，应标为观察盲区而不是“GUI 无痕”。English: Reading through an authorized account and an ordinary management interface can resemble legitimate operations, and limited reads might stay below bulk-enumeration thresholds. Those possibilities depend on identity context, query volume, service implementation, and logging configuration; none is established here as a T1538-specific mechanism. Console sign-ins, actual service requests, available page telemetry, and follow-on actions remain observable. Disabled logging is a visibility gap, not proof that GUI use leaves no trace.

**scope_boundary_definition。** 中文：本次研究只把以云控制台为入口的环境读取视作 T1538 父候选事实，不把入口本身当作独立信息对象。若读到资源实体、启用服务或存储对象键，分别转入 T1580、T1526 或 T1619 的准入和检测设计；身份取得、会话复用与账号情境归 NJT-0061 等既有对象。合法管理员、SOC 和帮助台可作相同浏览；应结合所有者、任务、授权范围与后继结果判断，而不能按浏览器或页面名定性。English: This review treats cloud-console entry as the T1538 parent behavior but not as an independent information object. Reads of resource entities, enabled services, or storage object keys route to the T1580, T1526, or T1619 admission and detection designs. Credential acquisition, session reuse, and account context remain with NJT-0061 and related objects. Administrators, SOC analysts, and help desks can browse the same pages; owner, task, entitlement scope, and follow-on behavior must inform interpretation rather than browser or page names alone.

**application_scenarios。** 中文：在已取得云账号或会话的 Discovery 阶段，攻击者可能打开资产、服务、Inventory 或安全态势页，以选定可访问的资源和下一步目标。CISA 公告说明 Inventory 被用于识别横向移动目标，但没有公布界面选择。English: During Discovery after obtaining a cloud account or session, an adversary may inspect asset, service, Inventory, or security-posture views to choose reachable resources and next targets. The CISA advisory establishes use of Inventory for lateral-movement targeting but does not disclose the interface selected.

**attacker_model。** 中文：攻击者需要被服务接受的账号、联合身份或既存会话，以及目标视图所需的 IAM/租户权限；还受界面、范围、订阅级别和会话时效限制。是否主动选择低频浏览或预聚合视图须有操作证据，不能从“使用浏览器”反推。English: The adversary requires an accepted account, federated identity, or established session and permissions for the target view. Interface availability, scope, service tier, and session lifetime constrain access. Deliberate low-rate browsing or selection of an aggregated view requires operational evidence; it cannot be inferred merely from use of a browser.

**defender_model。** 中文：防守方可依据已保留的身份登录、会话和云服务读事件关联主体、源、时间、目标及后续操作；AWS 控制台来源字段只能在出现且语义经核验时使用，GCP Data Access 覆盖需先确认启用。页面导航、浏览器缓存、后台请求与租户审计不应混为一谈。缺登录或页面事件不等于未访问，缺读事件也须先排查日志设置和服务覆盖。English: The defender may correlate retained identity sign-ins, sessions, and cloud-service read events by actor, source, time, target, and subsequent action. AWS console-origin fields should be used only when present and validated; GCP Data Access coverage must be checked before reliance on it. Page navigation, browser cache, backend requests, and tenant-visible audit are separate layers. Missing sign-in or page events do not establish non-access, and missing read events require a check of logging and service coverage.

**research.limitations。** 中文：当前证据没有同一身份、权限、对象和信息目标下的 GUI/API 配对实验，也没有逐页请求—日志映射或检测效能数据。厂商文档证明机制能力，CISA 公告证明 Inventory 使用，两者不能拼接成已观察的 GUI 匿迹案例。若以后证实仅 GUI 可达的独有信息对象、攻击者稳定控制的选择变量、可重复的痕迹差和不同的可实施防御，应重开准入。English: The present record lacks paired GUI/API measurements under the same identity, permissions, target, and information goal, a page-to-request-to-log mapping, and detection-effectiveness data. Vendor documents establish platform capability and the CISA advisory establishes Inventory use; together they do not establish an observed GUI-stealth case. Reopen admission if future evidence identifies a GUI-only information object, a stable attacker-controlled selection variable, reproducible trace differences, and a distinct implementable defense.

## 6. 防御暂存设计：路由至获准的信息对象，不为 T1538 建正式对象

### `D07-02-T1538-DET-01`：身份会话—环境读取—后继使用关联

**目标 / Objective.** 中文：发现异常身份会话中的资源、服务或对象信息读取，并把所获信息与随后的目标选择关联；将 GUI 作为来源标记，按直接对象路由给 T1580/T1526/T1619 中获准的目标。English: Identify resource, service, or object-information reads in anomalous identity sessions and connect them to later target selection; preserve GUI as a provenance attribute and route by direct object to whichever of T1580/T1526/T1619 is admitted. 此 DET 暂存方案不以 T1538 为 `detects_ref`；若仅有网页登录而无对象读取，应输出“身份风险”，不能宣称完成 Discovery 检测。

### `D07-02-T1538-NJA-01`：分层证据的控制台来源读行为关联

| 数据通道与前提 | 必需字段或信号 | 能证明的层级 |
|---|---|---|
| AWS CloudTrail `ConsoleLogin`；相关身份提供者登录 | `eventTime`, `userIdentity.principalId/arn`, `recipientAccountId`, `sourceIPAddress`, `userAgent`, `responseElements.ConsoleLogin` 或登录结果，MFA/设备线索（若有） | 身份/入口，不证明任何资源已读。联合登录须用对应 IdP/Identity Center 实际日志补足。 |
| AWS CloudTrail **已保留的**管理读事件；SSM 等具体服务请求 | `eventTime`, `userIdentity`, `eventSource`, `eventName`, `readOnly`, `sourceIPAddress`, `userAgent`, `requestParameters`, `resources`, `recipientAccountId`；`sessionCredentialFromConsole` **只在存在时**使用 | 实际服务请求和目标范围；浏览器来源只是辅助，不能从缺少该字段判定非 GUI。 |
| AWS S3 或其他对象数据事件；必须显式确认对目标资源已启用 | 主体、桶/容器、对象或前缀、操作、时间、来源；按具体服务日志模式验证 | 对象级读取；不能用管理事件默认覆盖代替对象级数据事件。 |
| GCP 身份日志与**已启用**的 Cloud Audit Data Access | `timestamp`, `authenticationInfo.principalEmail`（若可用）, `serviceName`, `methodName`, `resourceName`, `requestMetadata.callerIp`（若可用）, 状态；另保留审计配置快照 | 实际被记录的资源配置/元数据或数据读取；Data Access 未启用时只能判“未知”。 |
| 厂商或组织自有经验证的门户页面遥测，可选 | 会话/主体、页面 ID、时间、租户、页面结果、页面到信息对象映射版本 | 可加强“看过哪页”；没有该通道不能凭 CloudTrail/Cloud Audit 自动补出逐页历史。 |

**逻辑与关联。** 先以身份、租户/账号、可用会话 ID 或临时凭据、源 IP/设备建立登录上下文，再在试运行的 30 分钟窗口内连接实际 `List/Get/Describe/Search` 读事件，按返回对象或已知操作语义分别归资源、服务能力、存储对象；窗口为调优起点而非来源证实的阈值。记录是否属于正常角色/工单、既有权限、首次或罕见作用域及随后的快照、角色、对象读取、下载或远程访问。仅 `ConsoleLogin` 为低级“入口线索”；登录加对象读为“发现嫌疑”；再有异常来源、越常规范围和后继使用才提高调查优先级。没有对象读取日志时输出“覆盖不足/待核验”，不把“缺失”当成“无请求”。同一用户多个并发会话、NAT 和角色切换需以可信会话/凭据键优先，无法唯一关联时降置信度。

**误报与调优。** 云管理员、SOC、帮助台、CSPM、IaC 漂移检查、资产盘点、成本治理和故障调查都可能高频或跨服务读取。按账号所有者、批准任务、时间、作用域、角色及同类同岗基线调优，并保留对获准主体超范围或异常设备的检测；不能仅按浏览器 `userAgent`、已知办公 IP 或读操作性质永久放行。研究中无已验证的误报率或最佳窗口。

**盲区。** 既存会话未产生新登录；CloudTrail trail/Lake 筛选、区域或保留策略和数据事件未启用；GCP Data Access 默认缺口；门户页面遥测缺失、缓存或服务端聚合；API 代理造成来源字段不稳定；身份跨租户和角色切换；返回数据内容未被审计日志完整保存。任何 `page_view` 字段必须由部署中的真实门户通道证明存在，不能从 MITRE DET0291 的跨产品示例直接搬入 NJA。该实现按信息对象可复用，但没有“GUI 专属检测目标”。

### `D07-02-T1538-MIT-01`：云环境可见范围与审计连续性治理

**Measure A（preventive / exposure-reduction）：** 按业务任务收敛资源/服务/对象的读取权限，缩短高权限会话并定期复核；对控制台与 API 均执行相同对象层授权，不以只关闭某个页面作为防御。**Measure B（detective-support）：** 保留身份登录及管理读事件，为高价值服务和对象启用所需 Data Access/数据事件，测试页面动作到服务请求到日志的映射，并记录每租户、项目、区域的覆盖与保留期限。**Measure C（containment）：** 对异常会话撤销有效凭据/令牌、隔离受影响身份并核查后继对象访问；合法 SOC/帮助台调查需保留审批与工单映射。三项措施均有运维成本和正常阅读需求，不保证阻断已获授权的全部浏览。

| 逐目标应用（待主审准入，不写正式 `target_ref`） | use / 使用 | expected effect / 预期效果 | limitation / 限制 |
|---|---|---|---|
| T1580 资源实体 | 限制跨账号/项目资产 `List/Describe/Search` 权限；按主体与资源作用域保留管理读审计。 | 减少可见资源面，使异常跨范围资源清单更易关联。 | 管理员和盘点服务仍需读；API 与 GUI 均受影响；无日志时只能降置信。 |
| T1526 服务能力 | 限制服务目录、配置与安全/日志服务状态读取给职责所需主体；保留具体服务查询。 | 缩小防御能力暴露，并让服务状态侦察可与身份/后继行为连接。 | 服务可用性有时可从其他资源或行为推断；不能靠隐藏控制台卡片阻止。 |
| T1619 存储对象键 | 单独限制桶内列举及前缀范围，为敏感容器启用对象级数据事件并管理成本。 | 减少对象名暴露、补足容器内读取证据。 | 数据事件覆盖需逐桶确认；备份与索引正常列举可能很多；不防已授权少量读取。 |
| `NJT-0061` 身份/会话 | 复用既有身份治理，包括抗钓鱼 MFA、设备/会话评估和及时撤销；结合工单检查读取。 | 降低被盗身份及既存会话用于任意发现路径的机会，并提升身份归因。 | 不能单独区分资源/服务/对象的直接信息目标；现存会话和联合身份需专门核验。 |

## 7. 共享库决议建议

| 对象 | 决议 | 精确边界 |
|---|---|---|
| `REF-000206`、`REF-000307`、`REF-000376` | `reuse` | SSM 云审计和 Entra 登录来源已在库；只复用其实际支持的服务请求或身份字段。 |
| `NJT-0061` 相关身份 Claim/DET/MIT，尤其 `CLM-000222/-223` 与 `MIT-000052` | `reuse` 或由主审按既有目标 `extend` | 登录情境合形、会话复用与身份控制已有规范语义；控制台只是一个后继访问场景。不能把身份 Claim 改写成 GUI 无审计 Claim。 |
| T1538 固定父页、CISA AA23-320A、SCC 控制台/API、SSM Inventory/API、AWS ConsoleLogin/事件字段、GCP Audit 文档 | `defer` 建库；若主审需保存排除决策证据，先按 URL 查重再 `create` 单一 REF | 排除决策可直接引用资料；当前没有获准 NJT/DET 对象需要把每篇资料转为共享对象。`REF-000206` 已覆盖 SSM 日志，不重复建立。 |
| `D07-02-T1538-CLM-01..04` | `defer` 正式 CLM；准入理由中保留原子结论 | 01 为 ATT&CK 父事实，02/03 为有限平台事实，04 为研究判定；不能合并成“GUI 隐蔽”的共享 Claim。 |
| CISA Scattered Spider / Inventory 事件 | `defer` CASE | 资料未确证 GUI 路径、具体请求和匿迹变量。若未来建 CASE，只能写 Inventory 目标识别，不写 GUI 或审计缺失。 |
| `D07-02-T1538-DET-01` / `D07-02-T1538-NJA-01` | `defer` 为 T1538 独立对象；对获准的 T1580/T1526/T1619 可 `extend`/`split` | 身份—读取关联可作为共同检测目的，但按资源/服务/对象的实际操作、数据事件、调优不同决定 Analytic 拆分；不得仅换标题复用。 |
| `D07-02-T1538-MIT-01` | `defer` 为 T1538；对获准目标可核查既有最小权限/审计 MIT 后 `extend`，动作不同则 `split` | 控制概念跨 GUI/API；每个目标的授权面、日志类型、预期效果和限制必须分别写 Application。 |
| REL | `defer` | 目前只有规划边界，不足以制造正式跨技术关系。 |

## 8. 证据限制与重审条件

本次网络检索按官方 ATT&CK/CISA 案例、Google SCC 控制台与 API、AWS SSM GUI/API 与 CloudTrail、GCP Audit/Entra 登录四组独立展开；检索只能证明所列结论。没有受害租户实测、会话级浏览器 HAR、页面请求与审计事件配对、API 对照、检测统计，也未取得 Scattered Spider 使用 GUI 的直接案例证据。因此不把权限差、缓存、日志未开启或管理者合法外观说成 T1538 独立匿迹效果。

若主审考虑 `adapt`，须先提交：① GUI 独有或在相同授权下 API 不能取得的**明确定义的信息对象**；② 可由攻击者稳定选择的行为变量，而非产品、页面、字段或日志配置标签；③ 同身份/权限/对象下 GUI 与 API 的请求、登录、页面、服务审计和后继结果配对证据，证明可重复的痕迹及观察差；④ 与 T1580/T1526/T1619、NJT-0061 不重复的检测数据/逻辑及缓解动作；⑤ 正常管理员/SOC/帮助台反例和盲区。满足这些条件前，`exclude` 与零子项是可复核的保守结论。
