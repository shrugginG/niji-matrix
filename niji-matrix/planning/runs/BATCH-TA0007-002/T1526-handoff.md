# T1526 Cloud Service Discovery / 云服务发现：第二轮只读研究交接

工作项 `WORK-TA0007-T1526`；批次 `BATCH-TA0007-002`；临时键 `D07-02-T1526-*`。本文是独立研究提案，供主 Agent 与其他四项交接统一准入；仅写本 handoff，未分配 NJT/NJS 或共享库正式 ID。本文所说的“服务状态”包括能力是否可用、启用、运行、可访问，以及安全、日志服务的有效覆盖；它不等同于某个资源实体的存在。

## 1. 先行准入建议

**建议 `adapt`，父项准入置信度 medium–high；正式 Niji 子项当前 `0`，`subtechnique_taxonomy.coverage: deferred`。** 固定 `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx` 的 `techniques` 工作表第 98 行确认：`T1526`、`Cloud Service Discovery`、`Discovery`、`enterprise-attack`、父项标记 `is sub-technique=0`。全表无 `sub-technique of=T1526` 或 `T1526.*` 行，故固定版 ATT&CK 子项数 `0`、ID `[]`；`original_attack_subtechniques_imported: false`。父行明确提到服务启用信息及安全/日志服务，但也把 Azure 资源清单写进宽泛示例。本次有意把直接问题收紧为**“此范围具备、启用了哪些服务能力，安全与日志覆盖处于何种状态？”**，让实体资源图归 T1580。ATT&CK 子项为零不免除独立的 Niji 轴搜索。

**中文理由。** 服务能力与覆盖状态能够直接改变攻击者下一步选择。Microsoft 对 Storm-0501 的实案报告记载攻击者理解了 Azure 策略、资源锁与存储不可变性等保护，然后试图移除保护并实施云端破坏；这支持“测绘防护状态有攻击用途”，但不证明其查询路径本身避开了审计。官方资料另显示不同服务读取的可观察性确实不同：AWS GuardDuty 调用进入 CloudTrail，而 Google Service Usage `ListServices` 不产生日志、Azure Activity Log 通常不收读取。把“利用已知读取盲区获取服务能力图”作为 **有条件、待主审校准的 NM-BT 父级机理** 有结构证据；现有实案尚不足以声称攻击者有意选择该盲区，也不足以把某个平台/API 划成 NJS。若主审要求对具体匿迹意图有事件级证据，应暂停正式机制与正式父项写入，保留 `adapt` 准入建议，不以普通合法只读查询填充机制。

**English rationale.** Service capability and protective coverage can directly shape an adversary's next action. Microsoft's observed Storm-0501 campaign shows that the actor mapped Azure policies, locks, and storage immutability protections before trying to remove protections and cause cloud impact; it supports the operational value of coverage discovery but does not show that the discovery queries evaded audit. Provider documentation establishes different observation surfaces: GuardDuty calls enter CloudTrail, Google Service Usage `ListServices` is listed as producing no audit log, and Azure Activity Log generally omits reads. A visibility-gap-aware service read can therefore support a **conditional, reviewer-calibrated NM-BT parent mechanism** at the architectural level. The incident does not prove deliberate selection of those gaps, and no platform or API merits an NJS on that basis. If event-level evidence of stealth intent is required, pause formal mechanism and parent authoring while retaining this `adapt` admission recommendation; ordinary authorized read access cannot fill the mechanism field.

## 2. 一手结论级证据表

下列 `REF-*` 是建议共享库临时键；网页随时间更新，固定版 ATT&CK 行以本地 v19.1 工作簿为准。产品文档证明接口/遥测能力，不自动证明攻击者使用或实测检测效果。

| 键 | 一手来源 | 可支持的准确结论 | 不能推出的结论 |
|---|---|---|---|
| `D07-02-T1526-REF-01` | 本地 Enterprise 19.1 工作簿第 98 行；[MITRE T1526 当前公开页](https://attack.mitre.org/techniques/T1526/) | 父项属于 Discovery；服务启用及安全/日志服务可为直接发现对象；固定版零子项 | 网页现行内容不替代冻结版；父页不证明 Niji 机理、子项或攻击者匿迹意图 |
| `D07-02-T1526-REF-02` | [Microsoft Threat Intelligence，Storm-0501，2025-08-27](https://www.microsoft.com/en-us/security/blog/2025/08/27/storm-0501s-evolving-techniques-lead-to-cloud-based-ransomware/)，“Discovery”及随后防护删除段 | 真实攻击者映射 Azure policies、resource locks、Storage immutability policies，后续尝试移除防护；防护状态有攻击用途 | 未列出取得每项状态的精确 GET 请求、读取审计结果或有意选无日志路径；不能称“无痕侦察” |
| `D07-02-T1526-REF-03` | [Google Service Usage `services.list` REST](https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/services/list)；[列出已启用服务指南](https://docs.cloud.google.com/service-usage/docs/list-services) | `state:ENABLED` 可列项目已启用服务；返回 `Service` 与 `nextPageToken`，权限为 `serviceusage.services.list` | “available” 不等于“enabled”；接口不返回任意安全产品的完整有效覆盖，也不表示项目中有具体工作负载 |
| `D07-02-T1526-REF-04` | [Google Service Usage 审计日志表](https://docs.cloud.google.com/service-usage/docs/audit-logging)，“Methods that don't produce audit logs” | `ServiceUsage.ListServices`、`GetService` 与 `BatchGetServices` 被明确列为**不产生日志**；启用 Data Access 不能据此承诺该方法有逐次审计 | 不代表 GCP 所有服务读取均无日志；也不代表网络、身份或其他独立来源没有残余信号 |
| `D07-02-T1526-REF-05` | [Google Cloud Data Access 审计配置](https://docs.cloud.google.com/logging/docs/audit/configure-data-access) | 除部分 BigQuery 服务外，Data Access 审计默认关闭，需按服务显式启用；是另一种配置性盲区 | 不能把它与 `ListServices` 明列为“不产生日志”混同；开启 Data Access 不会补回从未生成的 `ListServices` 事件 |
| `D07-02-T1526-REF-06` | [AWS GuardDuty `ListDetectors`](https://docs.aws.amazon.com/cli/latest/reference/guardduty/list-detectors.html)；[`GetDetector`](https://docs.aws.amazon.com/cli/latest/reference/guardduty/get-detector.html) | 前者列现有 detector ID，后者返回 `Status`、`Features` 等启用状态；该序列可回答特定区域的防护能力 | `ListDetectors` 的 ID 列表本身不等于启用状态；不能从未列出 detector 推断组织其他区域或账户均无 GuardDuty |
| `D07-02-T1526-REF-07` | [AWS GuardDuty CloudTrail 记录](https://docs.aws.amazon.com/guardduty/latest/ug/logging-using-cloudtrail.html)；[CloudTrail 事件字段](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html)；[事件历史](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events-console.html) | GuardDuty 控制面 API 调用及控制台调用可有 CloudTrail 事件；事件可含 `eventTime`、`userIdentity`、`eventSource`、`eventName`、`awsRegion`、`sourceIPAddress`；Event history 保留近 90 天管理事件 | 控制台 Event history 默认过滤只读事件不等于事件不存在；CloudTrail 记录调用不保证保留服务返回的完整状态内容，长期集中保留需 trail/event data store |
| `D07-02-T1526-REF-08` | [AWS CloudTrail `GetEventSelectors`](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_GetEventSelectors.html)；[日志选择器解释](https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/get-event-selectors.html) | 返回管理/数据事件及 read/write 选择器，可判断某条 trail 的审计覆盖设置；缺失被选择器排除的事件不应被误报为“攻击者无痕” | 不代表 CloudTrail Event history 同步缺失；选择器状态也不证明攻击者查询过它 |
| `D07-02-T1526-REF-09` | [Azure Providers List API](https://learn.microsoft.com/en-us/rest/api/resources/providers/list?view=rest-resources-2021-04-01)；[Azure resource providers](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types) | ARM `providers` 列表返回 namespace 与 `registrationState`；注册是订阅能否使用该资源提供程序的一项能力线索 | `Registered` 不证明该服务已有实例、正在运行或其所有功能启用；若直接问题是具体资源，归 T1580 |
| `D07-02-T1526-REF-10` | [Microsoft Defender for Cloud Pricing Get API](https://learn.microsoft.com/en-us/rest/api/defenderforcloud/pricings/get?view=rest-defenderforcloud-2024-01-01) | `pricingTier` 和扩展/子计划信息可表达指定范围的 Defender 计划状态，较 provider 注册更接近安全覆盖 | 订阅层计划不能证明每个资源得到有效传感器覆盖；需按作用域和实际注册校验 |
| `D07-02-T1526-REF-11` | [Azure Activity Log](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log)；[Entra sign-in 详情](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-in-log-activity-details) | Activity Log 默认保存管理变更且**通常不捕获读操作**；Entra 登录可提供身份、应用、资源、来源等会话线索 | 仅有登录不证明哪个服务状态被读取；不能机械把 ARM GET 当作可在 AzureActivity 里逐次检出的事件 |
| `REF-000422` / `CASE-000144` | [Datadog 已修复 Service Catalog gamma 端点研究](https://securitylabs.datadoghq.com/articles/bypass-cloudtrail-aws-service-catalog-and-other/)；仓库既有对象 | 有效 IAM 调用在特定旧端点曾不进 CloudTrail，AWS 确认并修复；这是审计盲区存在可能性的研究对照 | **不是在野攻击**，也不证明当下 T1526 服务状态读取仍可借该端点绕过；不得拿它作为正式 NJS 或现实攻击案例 |

`D07-02-T1526-CASE-01` 可提议为 Storm-0501 2025 的**防护状态发现案例**：仅写报告确述的映射、后续删除尝试和时间/攻击环境，置信度 medium；不写读取 API、避审计、检测成功率。2024 年 `REF-000382` 是同演员不同报告，不能按演员名当作同一 Reference 或事件案例。

## 3. 直接对象、混合响应主归属与相邻边界

判定单位是**本次查询直接要回答的问题及被用于下一步的结果**，而不是 API、GUI、云平台、响应的单一字段。若攻击者问“Defender/GuardDuty/CloudTrail 是否启用、哪些服务能力可用、实际保护计划覆盖什么范围”，归 T1526。若问“有哪些 VM、快照、网络、桶、数据库及关系”，归 T1580。若问“已知桶内有哪些对象键、前缀和元数据”，归 T1619。T1538 仅记录控制台 GUI 为取得这些信息的路径，不因界面而复制父项。

| 混合结果示例 | 主归属 | 可附加记录的次级信息及限制 |
|---|---|---|
| ARM `providers/list` 返回 namespace、注册状态及 resource type 名 | T1526：能力/注册状态 | Resource type **类型**不是部署的资源实体；不能据此建 T1580 实例清单 |
| `GetDetector` 返回 detector ID、`Status`、`Features` | T1526：保护是否启用和覆盖设置 | detector ID 是定位状态的句柄；若后续继续盘点实例级 coverage，单独按实际直接目标评估 T1580 |
| 同一 inventory 请求列出服务名、具体 VM/桶 ID 和配置 | 若主要逐项定位实体，T1580；若主要判定某防护服务覆盖/启用，T1526 | 双重标签只在确有两项可区分目的和后续使用证据时使用；不能按响应字段自动双归属 |
| 控制台页面展示服务开关与桶内对象键 | 状态归 T1526；对象键归 T1619；GUI 是 T1538 路径上下文 | 页面载体不证明审计缺席，也不产生 GUI NJS |

正常反例包括授权服务目录、租户治理、成本盘点、CSPM、审计覆盖核查、应急响应和服务上线检查。它们可产生与攻击者非常相似的查询；仅靠只读成功、低请求量、陌生 API 或服务名称不能推断匿迹。已存在的 `NJT-0131` 处理身份对象清单；`NJT-0126` 处理云层级迁移造成的**实际**防御覆盖位移；T1526 只读取当前服务/覆盖，不等同于改变层级或关闭日志。后续 `Disable or Modify Cloud Log`、工具关闭和实际数据访问另属其行为对象。

## 4. Niji 原生变量搜索、痕迹差与分类决议

固定版零 ATT&CK 子项是普通广度触发，仍搜索了四条彼此不同的可控变量；所有候选都按“行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果”审查，不按服务、云、API 或字段拆分。

| 临时轴 | 行为与 trace/defender 差异 | 当前决议 |
|---|---|---|
| `D07-02-T1526-AX-01` 利用已知读取审计缺口 | 攻击者如能选择能回答服务状态问题的读取面，而该方法不产生日志或租户未开相应读审计，服务状态可被获知而常规控制面无逐次请求；身份/网络/后续动作仍可能留痕。Google `ListServices` 与 Azure Activity Log 给出结构上可检验的对照，AWS GuardDuty 读则通常有 CloudTrail。 | **父级有条件 NM-BT**；跨环境存在机制差，但目前无同案证明攻击者为匿迹而选择路径，更不能按 GCP/Azure 或 API 建 NJS。主审需校准为 `medium` 的结构推断或继续 defer。 |
| `D07-02-T1526-AX-02` 转读预存服务/防护状态快照 | 读取已存在的治理报告、服务目录导出或缓存视图而不在线逐服务询问，可能减少原服务 API 请求；改在快照/文件读取层留下痕迹。 | `evidence-deferred`。尚无本候选的攻击者实际使用、快照新鲜度、两路径 trace 对照和独立防御价值；并须与 T1580 的预存**资源**图转读严格分开。 |
| `D07-02-T1526-AX-03` 按防护状态条件门控后继行为 | 先识别覆盖，随后仅在无监测范围继续操作，可能减少受监测区的恶意后继动作；状态查询本身仍有或没有服务级痕迹，取决于通道。Storm-0501 证明防护测绘和后续对防护操作，却未证明“只选择无覆盖区”的条件门控。 | `evidence-deferred`；若有同案时间链及跨有/无覆盖区的选择证据，可重审。不能把受害环境原有盲区本身当作攻击者设计。 |
| `D07-02-T1526-AX-04` 身份/时间/界面/产品差异 | 使用既有身份、低速轮询、GUI、CLI 或某服务名可能改变归因、速率或日志字段，但目前没有 T1526 专属的稳定痕迹/防御差别；身份外观与既存 `NJT-0061` 相邻。 | `adjacent-technique` 或 `not-stealth-distinct`；不建 NJS。 |

**分类结论 / Taxonomy conclusion.** 中文：现有一手资料支持服务状态发现和跨云读审计差异，但未证明任何轴同时具有攻击者意图、稳定兄弟边界、结论级事件证据和独立防御价值；正式 NJS 为零，taxonomy 保持 `deferred` 而非宣称已证明 `none-justified`。English: Primary sources support service-state discovery and provider-specific read-audit differences, but no axis yet has attacker intent, a stable sibling boundary, event-level evidence, and distinct defensive value together. Propose zero formal NJS and `deferred` taxonomy, not a claim that a partition is impossible.

## 5. 父级双语核心字段与有条件机理草案

以下段落供主审逐字段重写/审定，非正式 YAML；`schema_version: 2.0.0` 的最终对象还需由主 Agent 配置 classification、evidence、defense 和 lifecycle。

| 字段 | 中文 | English |
|---|---|---|
| `name` / `summary` | **云服务能力与覆盖发现。** 攻击者在取得云身份后探明可用服务、启用状态及安全/日志覆盖，以选择后续目标和操作路径；当读取落在已验证的审计盲区时，状态判断可能早于防守方的逐次观察。 | **Cloud Service Capability and Coverage Discovery.** After gaining cloud access, an adversary determines available services, enabled states, and security or logging coverage to choose later targets and actions; a read through a verified audit gap can yield that knowledge before a defender sees an individual request. |
| `definition_and_concept` | 本技术是对租户、订阅、账户、项目或服务作用域的能力状态进行测绘，直接问题是某项服务能否使用、是否启用，以及日志和保护计划实际覆盖了哪些范围。攻击者可据此决定后续凭据、数据或防护操作；列出的服务名只有在说明能力或覆盖时才是本对象，具体 VM、桶或对象键不因出现在同一响应而被吸收。 | This technique maps capability state at a tenant, subscription, account, project, or service scope. Its direct question is whether a service is usable or enabled and what logging or protection plans cover. The answer can guide later credential, data, or protection actions. A service name belongs here when it describes capability or coverage; VM, bucket, and object-key inventories do not become this object merely because they appear in the same response. |
| `stealth_characteristics` | 服务状态读取常是合法治理和运维也会做的只读操作，单条成功调用的语义难与正常盘点区分，但这不是自动匿迹。可论证的特殊风险是**读取通道覆盖不一致**：某些方法不产生日志或某类读审计未启用，攻击者获知状态而服务级逐次请求没有进入防守视野；在 AWS GuardDuty 等已审计通道仍会留下身份、来源、时间和方法，其他身份或网络痕迹也可能残留。 | Service-state reads are also routine for governance and operations, so one successful read has weak intent value; that fact alone is not stealth. The narrower defensible risk is **uneven read coverage**: where a method generates no audit event or a read category is disabled, an adversary can learn a state without a service-level request entering the defender's normal view. Audited paths such as GuardDuty still leave identity, source, time, and action records, and other identity or network traces may remain. |
| `scope_boundary_definition` | 纳入对服务可用性、启用、运行、保护或日志覆盖的直接探询；排除实体 IaaS 资源清单、桶内对象键、单纯 GUI 导航、身份清单及真正关闭/篡改服务。若查询返回混合信息，以请求要回答的问题和后续使用为主归属。合法管理员、CSPM、成本管理及事件响应可作同样读取，缺少会话异常或后继行为时不得写成恶意或匿迹事实。 | Include direct inquiries into service availability, enablement, operation, protection, or logging coverage. Exclude concrete IaaS entity inventories, keys inside a storage container, GUI navigation alone, identity inventories, and actual service disabling or tampering. For mixed responses, assign primary ownership by the question the request answers and how the answer is used. Administrators, CSPM, cost management, and incident response can make the same reads; without anomalous session or follow-on evidence, intent and stealth remain unproven. |
| `application_scenarios` | 攻击者已取得能读取某云作用域的凭据或会话，在横向扩展、寻找数据入口或准备对防护设施采取行动前，先检查哪些能力已经启用及哪些范围受保护。跨账户、区域、订阅或项目的结果可能不同，因此攻击者需要保留作用域和时间；一处“未启用”不能外推到整个组织。 | After obtaining a session or credentials allowed to read a cloud scope, an adversary may check enabled capabilities and protected areas before expanding, seeking data, or acting against defenses. State can differ by account, region, subscription, or project, so scope and time matter; an absent service in one scope cannot be generalized to the whole organization. |
| `attacker_model` | 攻击者至少控制已认证身份及相应读权限，知道或能发现作用域并可解释服务状态；并不假定管理员写权、完整组织视图或能操纵日志。若主张利用审计缺口，还需证明该身份能到达相应读取面、返回值确实回答服务状态问题，并存在可比较的常规审计路径。 | The adversary controls an authenticated identity with relevant read permission, can locate a scope, and can interpret service state. Administrative write authority, organization-wide visibility, and log manipulation are not assumed. A claim of exploiting an audit gap additionally requires access to that read path, a response that actually answers the service-state question, and a comparable ordinary observation path. |
| `defender_model` | 防守方可有云控制面审计、身份登录、网络出口、配置快照及服务覆盖清单，但是否看见每次读取由提供商、方法和租户设置决定。AWS 管理事件与 GuardDuty 记录能保留请求；GCP Service Usage `ListServices` 缺逐次日志，Azure Activity Log 通常缺 GET；Entra 登录只证明会话而非被读状态。短保留、跨作用域断链和无独立基线会限制归因。 | The defender may have control-plane audit, identity sign-ins, network egress, configuration snapshots, and coverage inventories, but individual read visibility depends on provider, method, and tenant settings. AWS management and GuardDuty records can retain requests; GCP Service Usage `ListServices` has no per-call log, and Azure Activity Log generally omits GET reads. An Entra sign-in establishes a session, not the state read. Short retention, cross-scope gaps, and lack of an independent baseline constrain attribution. |
| `research.limitations` | 当前公开实案证明防护状态曾被攻击者测绘并用于后续攻击，却没有完整请求序列或“有审计路径—无审计路径”实测对照。提供商文档证明可用接口与日志类别，不证明某租户配置、攻击者意图或成功漏检。若发现完整服务查询事件、响应快照或新的同案选择证据，应重新校准 NM-BT 和子项；若只有正常盘点，应降低匿迹结论而非扩大本父项。 | The public incident establishes that the actor mapped protections and used that understanding later, but it lacks a full request sequence or measured comparison between audited and unaudited paths. Provider documentation proves interfaces and log categories, not tenant configuration, attacker intent, or a missed detection. Recalibrate NM-BT and children if complete query events, response snapshots, or same-incident selection evidence appear; ordinary inventories instead warrant a weaker stealth conclusion. |

**有条件 `stealth_mechanisms` 提案：** `NM-BT`，`role: primary`，`confidence: medium`（仅结构推断；若主审要求在野意图，则 `defer`）。摘要中文“服务状态读取落在已证实的逐次审计缺口”；English “Service-state reads through a verified per-request audit gap”，均无句末标点。分析：在可访问且确实返回目标状态的无逐次审计读取面查询 → 服务级请求事件缺席、但身份/网络/后继行为可能仍存 → 只依赖该审计源的防守方无法把状态获知与主体逐次关联 → 侦察发生在该观察模型之外。证据 `REF-03/04/05/07/11` 支持对照，但**不以 Storm-0501 或 `REF-000422` 证明该选择曾在野使用**。拒绝把普通合法读外观直接映射 `NM-FD`，或把慢速查询在没有时间对照时映射 `NM-ST`。

## 6. 暂缓子项双语核心稿：仅供未来重审

`D07-02-T1526-SUB-01` **既存服务状态视图转读 / Retrieval from a Preexisting Service-State View**，状态 `hypothesis; defer`，未分配 NJS；若将来正式化，必须 `lineage.attck_subtechnique_inherited: false`，其 ID 必须在父 NJT 确定后由主 Agent 分配。

| 字段 | 中文 | English |
|---|---|---|
| 定义与概念 | 攻击者从先前生成的服务目录或防护覆盖快照取得启用状态，而不对每个原服务在线逐一查询；其直接对象仍是服务能力或覆盖，资源实体快照应归 T1580。 | The adversary obtains enablement or coverage from a previously generated service directory or protection snapshot instead of querying each original service live. The direct object remains capability or coverage; a snapshot of concrete resource entities belongs to T1580. |
| 匿迹特性 | **既存服务状态视图转读**可能把痕迹从多项服务读取转移到一次快照访问，使只监控原服务 API 的防守方低估侦察；快照对象访问、身份会话及后继动作仍可能可见。尚无证明同等状态问题下请求数/审计差异的同案证据。 | **Retrieval from a Preexisting Service-State View** could move traces from multiple service reads to one snapshot access, causing a defender who watches only service APIs to undercount reconnaissance; snapshot access, identity sessions, and later actions may remain visible. No same-incident evidence yet establishes a trace difference for equivalent state questions. |
| 范围、场景与攻防模型 | 仅在快照包含足够新鲜、可信的服务状态并且攻击者有读取权限时适用；过时数据、正常 CSPM 报告、资产盘点及为直接获得资源实体的报告不在此子项。防守方须同时覆盖快照读取与原服务 API 才能比较，否则只能观察某一个面。 | It requires a sufficiently fresh, trustworthy service-state snapshot and attacker read access. Stale reports, normal CSPM output, asset inventories, and reports sought for concrete resource entities do not establish this child. A defender needs visibility into both snapshot access and original service APIs to compare traces; otherwise only one side is observed. |
| 暂缓原因 | 缺真实攻击者选用快照、两路径等价信息量、不同防守可见性及独立 MIT/DET 效益的一手结论级证据。 | Primary conclusion-level evidence is missing for actor selection of a snapshot, equal information from both paths, distinct defender visibility, and independent DET/MIT value. |

## 7. 可实施防御候选与逐目标限制

### `D07-02-T1526-DET-01` 服务状态读取与后继防护动作关联 / Service-State Read and Follow-on Protection-Action Correlation

**目标：** 找出能被逐次审计的高价值服务状态查询，并把身份、作用域、时间与随后防护变更或敏感服务访问连接；不能把所有云的读取都宣称可见。`detects_refs` 暂只指拟议 T1526 父项；`domains: [enterprise]`。`analytic_refs` 至少包含下列 AWS 可实施 NJA；Azure/GCP 的无逐次审计路径在覆盖表中写为盲区，待有真实 gateway/proxy 遥测再拆独立 NJA。该 DET 与既有 `DET-000135` 的层级迁移前后防护覆盖差分不同，不能因“coverage”一词相同而扩充它。

### `D07-02-T1526-NJA-01` AWS 安全/日志状态读取序列 / AWS Security and Logging State-Read Sequence

- **数据源和字段。** 经证实已采集只读管理事件的 CloudTrail trail/event data store，或 90 天 Event history 用于回溯。必需 `eventTime`, `recipientAccountId`, `awsRegion`, `userIdentity`（principal ARN 或 access key ID）, `eventSource`, `eventName`, `sourceIPAddress`；`userAgent`, `requestID`, `errorCode` 在存在时用于区分工具/失败与重试。另接入经过授权的 IAM 主体职责表、账户/区域清单、变更工单、GuardDuty detector/CloudTrail selector **独立状态快照**。CloudTrail 事件不假定含完整查询返回值。
- **逻辑。** 对 `guardduty.amazonaws.com` 的 `ListDetectors`/`GetDetector`、`cloudtrail.amazonaws.com` 的 `DescribeTrails`/`GetEventSelectors` 建立高价值操作族；在同一主体和账户/区域内按 24 小时窗口连接多项状态读、跨区域遍历及其后 24 小时内的防护变更、策略改写或异常敏感服务访问。对低频单次查询仅产生调查线索，若身份不具服务盘点职责、来源与历史不同或紧随可疑认证，再升优先级。`ListDetectors` 不能单独视为启用状态证据；必须另取 `GetDetector` 或基线快照。
- **关联键/结果。** `recipientAccountId + userIdentity.accessKeyId`（缺失时 principal ARN）及 `awsRegion`、时间；来源 IP 作为辅助键而非可靠唯一主体。输出主体、账户、区域、被查询服务族、查询时间、后续动作与基线偏差。`requestID` 只在相应事件存在时使用，不要求跨 API 相等。
- **误报与调优。** CSPM、安全审计、CloudFormation/治理任务、正常 IR 与服务上线均会读状态。按批准身份、预期账户/区域、变更时段建基线；豁免应有过期时间，不屏蔽这些身份在非管理来源或对防护变更的后继关联。
- **盲区。** 某些服务调用归类或 selector 不同；trail 未记录 read management events、保留期已过、跨账户集中接入缺失、服务返回状态未留在日志中时只能检测“读了什么 API”，不能证实获知了什么。Event history 控制台默认隐藏只读记录是显示过滤问题，不等于原事件不存在。GCP `ListServices` 和 Azure ARM GET 不适用本 NJA。数据假设由 `REF-06/07/08` 支撑，阈值与 24 小时窗口是待环境调优的设计选择，不是文献实测效果。

### 平台覆盖与 `D07-02-T1526-DET-02` 暂缓条件

| 平台/路径 | 逐次请求能否由所列默认日志证实 | 可用的残余与正式化条件 |
|---|---|
| AWS GuardDuty/CloudTrail 读 | GuardDuty 官方文档支持 CloudTrail 调用事件；需验证实际集中采集、selector、账户/区域覆盖 | 身份、来源、方法与时间可用；查询**返回状态**须另有快照或服务状态记录。正式 NJA-01 可在通过部署验证后实施。 |
| Google Service Usage `ListServices` | 官方明确该方法不产生日志；即使打开 Data Access 也不能据此承诺逐次事件 | 可能仅有身份、网络或代理侧访问；若组织确有可保留方法、主体、项目与时间的独立 API gateway/proxy 遥测，单独设计 NJA，先验证字段。否则 DET 对该方法 `deferred`。 |
| Azure ARM provider/Defender pricing GET | Activity Log 通常不捕获读取；Entra 登录不等于具体 GET | 可从 Entra 会话和后续写入建立风险上下文，但不可称为精确 T1526 读取检测。只有独立 gateway/API 访问日志经实测能给出操作、主体、订阅、时间时，才为该路径建立独立 NJA。 |

### `D07-02-T1526-MIT-01` 服务状态可见性与读取权限治理 / Service-State Visibility and Read-Authority Governance

**可复用 Measure 候选：** (1) 按职责/作用域收敛安全和日志服务状态读权限，区分普通资源读与高价值覆盖配置读；(2) 对支持逐次审计的通道启用 read management 采集、跨账户/区域集中保留并测试；(3) 对无逐次审计的读取面建立独立访问代理/网络可见性或记录不可覆盖的明确清单，而不是虚构 CloudTrail/GCP/Azure 原生日志。控制类型分别为 `exposure-reduction`、`detective-support`、`governance`。不能许诺彻底阻止服务发现：合法功能可能要求读权限，服务是否可用也可能从公开端点或其他行为间接推断。

| `applications[].target_ref` 待分配 | `use` | `expected_effect` | `limitations` |
|---|---|---|---|
| 拟议 T1526 父 NJT | 对服务能力/启用/保护状态读取按身份职责、账户/项目/订阅范围细分授权；把可审计读取、独立状态快照及例外清单纳入同一治理流程。 | 缩小被盗低权身份可得到的防护图范围；对于 AWS 等受支持路径提高身份—请求—后继动作的可关联性；明确 GCP/Azure 不可见处。 | 不能消除合法管理员读或通过行为推断能力；GCP `ListServices` 的官方无日志方法不会因“打开 Data Access”突然产生逐次事件；Azure Activity Log 不能替代 GET 访问审计；代理部署有覆盖与成本边界。 |
| 暂缓 `SUB-01` | **不建立正式 Application**；若该子项将来获准，再单独限制快照访问、保留快照读取日志并验证快照新鲜度。 | 仅为未来可能的快照路径治理目标。 | 当前无正式子项或事件级证据，不能借父项的效果说明填充它。 |

现有 `MIT-000124` 处理账户/项目层级迁移前后的控制连续性，受控动作和目标不同；若主审发现其 measures 真能原样覆盖服务状态读取，才考虑 `extend`，当前建议 `split/create`。普通最小权限控制可以复用原则，但必须保留 T1526 逐目标 use、expected effect 与 limitations。

## 8. 共享库逐类建议与证据覆盖

| 对象 | 建议决议 | 原因/临时键 |
|---|---|---|
| 固定版 T1526 父来源 | `create` 单一 Reference，先以 ATT&CK ID/版本/URL 查重；`D07-02-T1526-REF-01` | 当前库未查到 T1526 对应 REF；不可用当前网页替代工作簿版本判断 |
| Storm-0501 2025 报告 | `create` `D07-02-T1526-REF-02`；与 2024 `REF-000382` **split** | 同演员不同日期、事实与结论；2025 报告直接支持防护状态发现 |
| AWS/GCP/Azure 官方接口与审计文档 | 先 URL 查重，缺者 `create` `REF-03` 至 `REF-11`；`REF-000205` 可 `reuse` 事件字段 | `REF-000205` 是 Azure Activity Log **schema**，不单独支持“通常不收 GET”；各云读日志类别不可合并为一条 REF/CLM |
| Service Catalog 修复研究 | `reuse` `REF-000422` 仅作限制/历史反例；`CASE-000144` **不扩充至 T1526** | 既有案例是研究者验证已修复端点，不是在野服务发现；把它当 T1526 案例会改变案例含义 |
| 防护状态实案 | `create` 或与真实同案共享案例核对后 `extend`，`D07-02-T1526-CASE-01` | Storm-0501 2025 与 2024 资料不同；案例只包含报告明确的防护测绘与后继动作，不能补写审计结果 |
| 原子 Claims | `create` `D07-02-T1526-CLM-01`（服务状态直接对象/边界，证据 REF-01/03/09/10）；`CLM-02`（Storm-0501 防护状态发现与后继动作，REF-02）；`CLM-03`（GCP `ListServices` 无逐次审计，REF-03/04）；`CLM-04`（AWS GuardDuty 请求有 CloudTrail，REF-06/07）；`CLM-05`（Azure Activity Log 通常缺读取，REF-09/10/11）；`CLM-06`（有条件 NM-BT，结构推断，REF-03/04/07/11） | 每项因果强度不同，不能合成“云服务读取无日志”的错误总论；`CLM-06` 应标 `strongly-inferred`/medium 或由主审 defer |
| Detection | `create` `D07-02-T1526-DET-01` 与 `NJA-01`；对 GCP/Azure 精确读检测 `defer` | 与 `DET-000135` 的 ancestry 变更检测目标/数据不同；NJA-01 仅 AWS，不能名称替换跨云复用 |
| Mitigation | `create` 或经主审与其他候选的相同措施比较后 `extend`；`D07-02-T1526-MIT-01` | 与 `MIT-000124` 的层级治理应拆分，父项 Application 必须独立；若 T1580/T1619 共用权限治理概念，也须按对象分写 Application |
| Relationships | `defer` | T1526 状态发现可先于后续防护关闭或数据访问，但当前无足够同案时序与正式目标 ID，暂不建通用前驱 REL |

**证据覆盖键：** 父行为 `REF-01/02/03/06/09/10`；边界 `REF-03/06/09/10` 加 T1580/T1619/T1538 主审对照；条件机理 `REF-04/05/07/11`；正式 child existence `[]`；检测 `REF-06/07/08/11`，其中 GCP/Azure 精确读取为 deferred；缓解权限与审计措施 `REF-03/04/05/07/08/11`，效果为受条件约束的推断。没有资料把同一 API 的服务状态字段与资源实体字段自动变成两个技术。

## 9. 门禁、限制与主审待决

已按 NJT-0001 的字段责任核对定义、直接目的、匿迹特性、残余痕迹、范围/正常反例、攻防模型、机制因果、taxonomy、逐目标防御和限制；中英文段落维持同等强度。正式集成前仍需主审决定：`NM-BT` 的结构证据是否足以满足该父项“至少一项已成立机制”门禁；核对 Storm-0501 2025 资料是否已由其他候选提出相同 REF/CASE；逐目标验证 AWS 管理读采集和现有 DET/MIT 语义重复。若前者不通过，保留 `adapt` 研究决议但**不得**为凑齐 2.0.0 字段强写正式 NJT、NJS、DET 或 MIT。当前状态 `pending integration`；无正式 ID，未修改共享库、准入决策或正式矩阵。


## 10. 双语防御核心与暂缓子项补充

**暂缓子项场景与威胁模型。** 中文：攻击者若能读到近期生成的服务状态快照，可在规划后续云操作时少向原服务发出逐项查询；他必须有快照权限，并确认时间和作用域。若防守方只采集原服务 API，可能看不到这次信息获取；若快照访问被记录，则痕迹转移而非消失。English: An adversary who can read a recent service-state snapshot may avoid separate live queries while planning later cloud actions, but needs access and must verify the snapshot's time and scope. A defender observing only original service APIs may miss that acquisition; where snapshot access is logged, the trace moves rather than disappears. This remains a hypothesis and has no formal child mechanism or defense application.

**DET 核心。** 中文：目标是在有逐次审计的范围内，将服务状态读取的主体、作用域与时间和后继防护变更相连；不能把 GCP Service Usage `ListServices` 或 Azure ARM GET 宣称为默认逐次可见。English: Join principal, scope, and time for individually audited service-state reads to later protection changes. Do not claim default per-request visibility for GCP Service Usage `ListServices` or Azure ARM GET. The candidate strategy initially covers T1526 through the AWS analytic and keeps the other paths deferred pending independently validated telemetry.

**NJA 核心。** 中文：AWS 分析读取已验证的 CloudTrail read-management 事件，按账户、区域、主体和可调 24 小时窗口关联 GuardDuty/CloudTrail 状态查询，再查后续防护动作；配置快照用于解释状态，不能假定读取响应就在事件中。CSPM、IR 和上线流程是误报；选择器、保留、跨账户采集和响应字段缺失是盲区。English: The AWS analytic consumes verified CloudTrail read-management events and joins GuardDuty or CloudTrail state queries by account, region, principal, and a tunable 24-hour window, then checks subsequent protection actions. A separate configuration snapshot supplies state; the query response is not assumed to be in the audit event. CSPM, incident response, and onboarding are expected false positives; selectors, retention, cross-account collection, and omitted response values are blind spots.

**MIT 与逐目标限制。** 中文：对获准的 T1526 父项，按职责限制服务/防护状态读取，集中保留可用的读审计，并明列无逐次审计方法；这缩小被盗身份的可见范围、改善可审计路径的关联，却不能补出从未生成的 GCP 事件或让 Azure Activity Log 自动记录 GET。暂缓的快照子项不创建正式 Application。English: For an admitted T1526 parent, scope service and protection-state read rights by role, retain supported read audit centrally, and list methods without per-request audit. This narrows what a stolen identity can see and improves correlation where requests are logged, but cannot create GCP events never generated or make Azure Activity Log record GET by default. The deferred snapshot child receives no formal application.
