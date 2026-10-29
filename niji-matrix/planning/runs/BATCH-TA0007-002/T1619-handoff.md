# T1619 Cloud Storage Object Discovery / 云存储对象发现：第二轮只读研究交接

工作项 `WORK-TA0007-T1619`；批次 `BATCH-TA0007-002`；临时键 `D07-02-T1619-*`。本文只提出主 Agent 待审的准入、内容和共享库决议；没有分配正式 ID，也没有修改正式矩阵或共享库。固定基线是 `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx`，其中 `techniques` 表第 99 行为 T1619、Cloud Storage Object Discovery、Discovery、IaaS、`is sub-technique=0`。全表无 `T1619.*` 行：固定版 ATT&CK 子项数 `0`、ID `[]`，`original_attack_subtechniques_imported: false`。零子项仍须开放搜索 Niji 原生轴；本交接已作该搜索。

## 1. 先行准入结论

**建议 `retain` 父项，父行为置信度 high；可归于 Niji 的父级匿迹因果置信度 medium；当前正式 NJS 建议 0，taxonomy 为 `deferred`。** 这不表示“对象列举不留痕”，也不把日常分页或公开接口当成规避意图。父项采用固定 ATT&CK 的行为语义，直接产物是已知桶/容器内部的对象键、名称、前缀、基本元数据或清单关系；对象内容读取属于后续阶段。若主审认为必须有真实攻击者同案来证明每个 Niji 机理，则把机理置信度降为 `hypothesis` 并暂缓正式化，不能用厂商 API 文档填补攻击意图。

**准入理由（zh）：** 已取得存储访问权的攻击者可在不先下载对象正文的情况下，列出容器内的键和前缀，用名称和清单关系选择下一步对象。AWS、Azure、GCP 的原始接口文档分别证明这一信息对象；ATT&CK 19.1 将其置于 Discovery。匿迹相关性来自这类只读请求可沿用获准身份和正常备份、索引、治理所用的调用形态，使单条事件的恶意意图难判，同时各云的详细读审计有实际启用和范围条件。Unit 42 的 Bling Libra 应急案例证明攻击者使用存储浏览工具及对象访问，但受害环境没有对象级日志，不能据此声称实际看见了 ListObjects；其另行受控实验只证明工具触发了哪些调用。因此父行为可保留，特定规避子项不能靠这一案例确立。[ATT&CK T1619](https://attack.mitre.org/techniques/T1619/)；[Unit 42 原始应急及实验](https://unit42.paloaltonetworks.com/shinyhunters-ransomware-extortion/)。

**Admission rationale (en):** An adversary with storage access can enumerate keys and prefixes inside a known container and use the resulting names and inventory relationships to select later objects without first downloading their bodies. The AWS, Azure, and GCP API specifications establish that direct information object, and the fixed ATT&CK 19.1 row maps it to Discovery. Its stealth relevance is conditional: a read request using an entitled identity can resemble backup, indexing, or governance activity, while detailed read audit depends on provider and deployment settings. Unit 42 observed Bling Libra using storage browsing tools and accessing objects, but the victim lacked object-level logs, so the report does not establish an observed ListObjects event in that incident. Unit 42's separate controlled experiment establishes tool-generated calls, not the attacker's exact listing trace. Retain the parent, while withholding a formal evasion child until an attacker-controlled variable and its trace effect have conclusion-level support.

## 2. 一手结论级证据表

| 临时来源键 | 一手来源及直接结论 | 不能推出的结论 |
|---|---|---|
| `D07-02-T1619-REF-01` | [固定版工作簿](../../../../data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx) 第 99 行与 [MITRE T1619](https://attack.mitre.org/techniques/T1619/)：容器内对象发现、Discovery/IaaS、固定版 0 子项。网页可能晚于 19.1，版本事实由工作簿裁定。 | 不支持 Niji 子项、规避意图、具体审计字段或检测有效率。ATT&CK 当前 DC0017 把桶和对象混列，不能替代本批父边界。 |
| `D07-02-T1619-REF-02` | [AWS ListObjectsV2 API](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html)：已知 bucket 内按 `prefix`、`delimiter`、分页条件返回对象键/元数据；单次最多 1000 键，继续页需 token；`ListBuckets` 返回桶清单，语义不同。 | 请求日志本身不等于完整返回对象清单；分页或小范围查询是正常功能，不证明匿迹。 |
| `D07-02-T1619-REF-03` | [AWS S3 CloudTrail 事件表](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html)：2026-09-22 复核实时 HTML 与 Markdown，普通 S3 的 `AWS::S3::Object` 行列 `ListObjects`，**未列 `ListObjectsV2`**；V2 出现在 S3 Express、Access Point、Outposts 行。数据事件默认关闭，Event history 不含数据事件；advanced selector 可按事件名、只读及资源 ARN 过滤。 | 主审所述 V2 在普通对象行与实时页面行归属不一致。不能由 Get/Put locator 推出 V2，也不能从该表遗漏推出 V2 绝无记录；普通桶 V2 要以目标 trail/event data store 的受控请求和选择器验证。 |
| `D07-02-T1619-REF-10` | [AWS CloudTrail record contents](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html)：`eventTime`、`userIdentity`、`eventSource`、`eventName`、`awsRegion`、`sourceIPAddress` 为基本事件字段；`requestParameters` 可能省略，只读 API 的 `responseElements` 为 `null`，`resources`、`userAgent`、`errorCode` 等按事件可用性核对。 | 请求日志不能恢复完整返回对象键集；prefix、分页 token、KeyCount 或返回 key 不可设为每条事件必需字段。 |
| `D07-02-T1619-REF-04` | [AWS S3 server access logging](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html) 与 [日志格式](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html)：可记录桶请求及 requester、时间、operation、request URI、状态；AWS [事件调查示例](https://aws.amazon.com/blogs/security/incident-response-guide-for-aws-cloudtrail-investigations-part-1/) 展示 `REST.GET.BUCKET` 和 `GET /?list-type=2` 的列举痕迹。server access log 按 best effort 投递，可能迟到、缺失或重复。 | AWS 调查博客使用示例地址和占位账户，不作为真实攻击 CASE；server log 不提供可靠完整计数，也不等同 CloudTrail V2 事件。 |
| `D07-02-T1619-REF-05` | [Azure List Blobs REST](https://learn.microsoft.com/en-us/rest/api/storageservices/list-blobs)：在一个已知 container 中列 blob，可用 prefix/delimiter/marker；需要对象读取权限或带 `l` 的 SAS。 [Azure 已记录操作表](https://learn.microsoft.com/en-us/rest/api/storageservices/storage-analytics-logged-operations-and-status-messages) 明列 `ListBlobs`。 | `ListContainers` 是容器清单，不能当 T1619；同名 SAS/账户密钥不足以识别背后的个人。 |
| `D07-02-T1619-REF-06` | [Azure Blob 监控场景](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-storage-monitoring-scenarios)、[StorageRead 类别](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/supported-logs/microsoft-storage-storageaccounts-blobservices-logs)、[StorageBlobLogs 字段](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/storagebloblogs)、[诊断设置](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings)：数据面日志须为 blob service 配置诊断导出；可用 `OperationName`, `Uri`, `TimeGenerated`, `AuthenticationType`, `RequesterObjectId`, `AuthenticationHash`, `CallerIpAddress`, `UserAgentHeader`, `StatusCode`。 | Azure Activity Log 不是 Blob `ListBlobs` 的替代输入；共享密钥/SAS 没有 OAuth 个人身份，URI/对象键字段也不能被当成完整列举响应。 |
| `D07-02-T1619-REF-07` | [GCP Objects:list](https://docs.cloud.google.com/storage/docs/json_api/v1/objects/list)：已知 bucket 的 `objects.list` 可按 prefix/delimiter/offset/分页列键，权限为 `storage.objects.list`。 [Cloud Storage 审计映射](https://docs.cloud.google.com/storage/docs/audit-logging)：列对象属于 Data Access `DATA_READ`，须显式启用；公开对象访问不由 Cloud Audit Logs 追踪。 | Admin Activity 不覆盖对象列举；不能假定每种 JSON/XML/gRPC 调用在目标环境都有相同 `methodName` 或完整返回对象；需逐方法、项目和 sink 验证。 |
| `D07-02-T1619-REF-08` | [Unit 42 Bling Libra 原始调查及受控工具实验](https://unit42.paloaltonetworks.com/shinyhunters-ransomware-extortion/)：失窃 AWS 凭证后的实际桶发现、S3 Browser/WinSCP 使用及对象访问；受控开启数据事件的桶中，S3 Browser 浏览桶目录产生 `ListObjects`，预览产生 `GetObject`。受害环境未启用 S3 data/server access logging。 | 受害环境中**没有**可观察的 ListObjects 事件或完整下载清单；实验的 GUI 工具自动调用不能归因给真实攻击者的逐项意图，也不能证明规避成功。CASE 仅可严格记录已证的攻击者桶访问；本研究不建议创建 T1619 专属 CASE。 |
| `D07-02-T1619-REF-09` | [AWS S3 Inventory](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory.html) 和 [GCP inventory reports](https://docs.cloud.google.com/storage/docs/insights/inventory-reports)：预存报告包含对象键/元数据；AWS 生成报告不使用 List API，GCP 生成时不为源桶逐对象元数据读取生成审计日志。 | **读取报告文件或查询数据集仍有自己的访问痕迹**；报告可能过期、不完整。未找到同案攻击者为降低源桶列举痕迹而转读清单的证据，故只能作 deferred 轴。 |

证据层级：`REF-01` 锚定父行为；`REF-02/05/07` 锚定三云列举能力；`REF-03/04/06/07/10` 锚定有条件的日志面与字段；`REF-08` 区分实际入侵与受控实验；`REF-09` 仅支持替代视图的架构可能。GCP 官方审计映射将 Listing buckets 归 Data Access `ADMIN_READ`，Listing objects 归 `DATA_READ`，支持 T1580/T1619 的行为与日志边界。拟议 `D07-02-T1619-CLM-01` 为对象键发现，`CLM-02` 为审计条件，`CLM-03` 为请求事件不证明完整返回集，`CLM-04` 为实验/实战边界，`CLM-05` 为清单转读架构但攻击用途未证。

## 3. 原生变量搜索、痕迹差与 taxonomy 决议

搜索分两次：先从直接列举的范围、节奏、身份和查询来源寻找攻击者可控变量；再从已生成对象清单反向寻找“本次发现是否触发源容器 List”的变量。固定版 ATT&CK 0 子项不是停止理由。当前**正式子项数 0**；`subtechnique_taxonomy.coverage: deferred`。无需要逐 ATT&CK 子项覆盖的表，但下表覆盖所有已审查的原生轴。

| 轴/临时键 | 可控设计 → 痕迹变化 → 防守观察差异 | 决议及证据限制 |
|---|---|---|
| `D07-02-T1619-AX-01` 既有授权身份下的只读清单 | 沿用可列对象的身份访问已知容器 → 记录为正常接口的读请求，保留时间、身份/凭证类型、来源和容器；无对象正文读取或修改事件 → 仅看写入/下载的检测看不到发现阶段，单条 List 难定恶意。 | **父级核心，NM-FD 候选 medium**。API/审计与 Unit 42 的受害身份滥用支持“有相似表象”，但没有测得检出率；不把“使用凭证”单独做子项。无日志时的缺口要归于部署条件，不称为攻击者必然消除了痕迹。 |
| `D07-02-T1619-AX-02` 限定范围的分段列举 | 已知命名规则后用 prefix/delimiter/offset 只问局部 → 单请求范围和可见次数可能变小，但请求参数、身份、容器和跨时序仍可关联；只按全桶扫或单窗次数告警会漏局部探查。 | **defer**。三云 API 证明选择能力，不证明攻击者有意压低阈值或实际检测差；备份、索引、UI 导航也大量使用 prefix 和分页。只有同案请求序列、目标前缀选择与规则对照出现，才考虑独立子项。 |
| `D07-02-T1619-AX-03` 预存对象清单转读 | 读取已有 inventory/report 而非在源桶实时 List → 源桶此刻缺少 List 序列，转为报告文件 GetObject/Blob 读取或数据集查询；只盯源桶 List 的策略失明。 | **最有价值的 deferred 子项 `D07-02-T1619-SUB-01`，候选 NM-BT**。AWS/GCP 原厂资料确认源侧痕迹转移，尚无一手恶意同案和报告读取审计核验；其前提是报告已存在且身份可读，时效/范围会限制。不能把 inventory 产品名拆为 NJS。 |
| `D07-02-T1619-AX-04` 跨身份/时间稀释 | 将一份对象图拆给多个身份或作业时段 → 局部计数减少，仍有凭证、IP、时间与容器线索，跨身份关联可能恢复。 | **defer**。架构可想象，但没有结论级恶意样本、关联窗口或阈值实测；不能从多个正常作业推断攻击协调。 |
| `D07-02-T1619-AX-05` 浏览器、CLI、SDK、API 版本、对象字段或云厂商 | 改变工具/协议/字段 → 可能改变 UA 和请求名，但没有稳定的匿迹变量或独立防御目标。 | **拒绝建 NJS**。T1538 的 GUI 仅是路径；ListObjects/V2、ListBlobs、GCS `objects.list` 是同一对象清单行为的实现；metadata 类型不是兄弟项。 |

**机理裁定：** 父级仅建议 `NM-FD` 主导，简述“授权对象清单的正常读取表象 / Ordinary read appearance of an authorized object inventory”，无句末标点。因果是借用获准身份读取对象清单 → 读审计中的身份和接口形态与合法作业相似但仍留请求 → 单事件分类难辨控制者和目的 → 借助后继访问及作业谱系才能恢复判断；证据 `REF-02/06/07/08`，`medium`，需主审审查“攻击者有意利用相似表象”的推断强度。`NM-BT` 只留给 `AX-03` 假设，或特定未启用读审计的**防守观察模型**，不能对所有云一概宣称无痕。`NM-ST` 对分段/节奏缺样本而 defer；`NM-DO` 无证据；GUI 本身不是 `NM-FD` 证据。

## 4. 相邻父技术与后继边界

T1580 的直接结果是桶/容器是否存在、访问配置及其与其他 IaaS 资源的关系；一旦针对**已知容器内部**列对象键或前缀，归 T1619。T1526 关心存储服务能力是否启用或可访问；T1538 的 GUI 只描述界面/路径，不因浏览器页面替换 API 就建立另一个发现结果。T1083 是主机本地文件目录；远端对象服务即使呈现文件夹 UI，判定仍以存储对象清单为准。`GetObject`、`GetBlob` 或 GCS 对象数据读取进入 TA0009 Collection 的 T1530 等后续语境；预览若下载正文，就不能只记成 T1619。列举可以为后续下载选目标，但 List 日志不能证明下载、更不能证明外传。S3 `ListBuckets` 与 Azure `ListContainers` 属容器级；`HeadBucket` 的存在/访问测试也不回答桶内有哪些键。一个交互可触发多类事件，应按直接信息结果分别归属，不按 GUI/CLI、产品或 API 名切父子。

## 5. 父级双语核心字段（供主审正式编写）

**name/summary：** 云存储对象发现 / Cloud Storage Object Discovery。攻击者列举已知云存储容器内的对象键和清单属性，以便选择后继目标；在有效身份和普通只读作业外观下，其意图可能难以单凭请求判断。 / An adversary enumerates object keys and inventory attributes inside a known cloud storage container to select later targets; under an entitled identity and ordinary read workload appearance, the purpose may be hard to judge from an isolated request.

**definition_and_concept — zh：** 云存储对象发现是对一个已定位的云对象存储容器取得其中对象名称、键、前缀或可列举元数据的行为。攻击者由此得到可筛选后续对象访问的清单，而不需要先读取每个对象正文；列举结果不是服务是否存在、桶是否存在，也不是对象内容已经被收集的证明。对象可以通过实时列举接口呈现，也可能在既存清单中被间接获知，后者是否形成独立匿迹子项须另证。本概念按直接信息结果而非 API、工具或云厂商界定。

**definition_and_concept — en:** Cloud Storage Object Discovery obtains names, keys, prefixes, or listable metadata for objects inside an already identified cloud object-storage container. The adversary gains an inventory from which later access can be selected without first reading every object body. The result establishes neither service or bucket existence alone nor completion of content collection. A live listing interface can expose the inventory, and a preexisting report may expose it indirectly; the latter needs separate evidence before it becomes an evasion child. The concept follows the direct information result rather than an API, tool, or provider.

**stealth_characteristics — zh：** 云存储对象发现常借用备份、索引和数据治理也需要的只读接口。若攻击者控制的是有权列举的身份，审计中仍会留下身份、时间、来源、容器和请求名，却未必出现写入或对象正文读取；只看破坏性动作或下载量的防守方可能较晚识别其目标选择。详细列举日志依赖 S3 数据事件/访问日志、Azure Blob 诊断设置或 GCP Data Access 的实际启用与覆盖；一旦有完整请求和批准作业基线，跨容器、陌生来源与后继 Get/下载可缩小伪装空间。只读性质和缺日志本身都不能证明攻击者设计了规避。

**stealth_characteristics — en:** Cloud Storage Object Discovery can use the same read interfaces as backup, indexing, and data-governance jobs. When an adversary controls an identity entitled to list, audit may still retain identity, time, source, container, and operation, while producing no write or object-body read at this stage. A defender watching only destructive actions or download volume can recognize target selection late. Detailed listing visibility depends on the actual S3 data-event or access-log selection, Azure Blob diagnostic routing, or GCP Data Access configuration. Complete request logs and approved-job baselines can expose unfamiliar origins, cross-container exploration, and later Get or download activity. A read-only request or missing logging alone does not establish an evasion design.

**scope_boundary_definition — zh：** 纳入针对已知容器内部的对象键、前缀和清单属性获取，即使同一次 GUI 操作还触发桶属性调用，也只把对象列举部分归此父级。账户桶清单、容器存在性和服务启用属于相邻发现对象；实际读对象正文属于后续 Collection，复制/外传须另按动作证明。正常备份、搜索索引、生命周期治理、迁移和取证同样会列举大量键，必须以身份授权、批准作业、范围和后继动作区分，不能把 prefix、分页或工具指纹单独当恶意标志。

**scope_boundary_definition — en:** Include acquisition of keys, prefixes, and inventory attributes inside a known container, even when the same GUI interaction also causes bucket-property calls; only the object-listing portion belongs here. Account-level bucket inventories, container-existence checks, and service enablement answer neighboring questions. Reading object bodies belongs to later Collection, and copying or exfiltration needs separate action evidence. Approved backup, indexing, lifecycle governance, migration, and forensics can enumerate many keys. Identity authorization, approved-job context, scope, and successor activity are therefore necessary to distinguish them; a prefix, page token, or tool signature is not an evil indicator by itself.

**application_scenarios — zh：** 攻击者在已经获得存储入口和容器标识后，可先查看键名与前缀以定位备份、导出文件或业务数据，再决定是否请求具体对象。目标环境的对象命名习惯、权限范围和清单规模决定能看见多少；若可读已有库存报告，则可能先从报告获得部分键，但报告的时效和覆盖未必足以代替实时查询。/ **en:** After obtaining a storage entry point and a container identifier, an adversary can inspect keys and prefixes for backups, exports, or business data before requesting any selected objects. Naming conventions, authorization scope, and inventory size limit what is visible. If a preexisting inventory report is readable, it may supply some keys first, although freshness and coverage can make it an incomplete substitute for a live query.

**attacker_model — zh：** 攻击者至少需知道一个目标容器及可列其中对象的有效权限，或先取得含该容器清单的报告访问权；可控制请求身份、来源、查询范围和节奏的程度取决于已获凭证及接口。仅有订阅可读权、能打开控制台或能看到桶名，不能自动推出对象列举权。/ **en:** The adversary needs a known target container and valid authority to list its objects, or access to a report containing that inventory. The ability to choose identity, origin, scope, and cadence depends on the obtained credentials and interface. Subscription read access, a visible console, or knowledge of a bucket name does not automatically confer object-list permission.

**defender_model — zh：** 防守方若已经收集并保留目标读日志，可关联身份、时间、来源、容器、操作和可得的请求范围，与批准作业及后继对象读取比较。CloudTrail 对只读 API 的 `responseElements` 为 `null`，请求参数也可能省略；普通桶 V2 的事件名及选择器必须在目标环境验证。Azure SAS/账户密钥限制个人归因，GCP 的 `DATA_READ` 要显式启用且受项目、方法和公开访问条件限制。缺事件可能来自选择器、路由、投递、保留或跨账户视角。/ **en:** With relevant read logs collected and retained, defenders can join identity, time, origin, container, operation, and available request scope to approved jobs and later object reads. CloudTrail sets `responseElements` to `null` for read-only APIs and may omit request parameters; the event name and selectors for ordinary-bucket V2 need a target test. Azure SAS or account-key use limits personal attribution, while GCP `DATA_READ` must be enabled and is scoped by project, method, and public-access conditions. Missing records can reflect selector, routing, delivery, retention, or account-visibility gaps.

**subtechnique_taxonomy narrative — zh：** 本轮没有把范围、分页、身份分散或预存报告读取提升为正式 Niji 子项。它们分别缺少恶意控制意图、实测痕迹对照、稳定兄弟边界或独立防御验证；下一轮优先取证“从既存对象清单转读”是否在真实攻击中替代源桶实时 List，并对报告文件/数据集访问补齐审计。/ **en:** This round does not promote scoped queries, pagination, identity spread, or preexisting-report reads to formal Niji children. They lack adversarial intent evidence, a measured trace comparison, stable sibling boundaries, or a distinct validated defense. The next review should prioritize whether a real adversary used an existing inventory instead of a live source-bucket List and verify audit on the report file or dataset.

**research.limitations — zh：** 固定版父行和接口证明行为，不证明攻击者选择参数或成功规避。Unit 42 真实受害环境缺对象级日志，其受控实验不能补成真实 List 事件。2026-09-22 实时 AWS 资源类型表的普通对象行未列 V2，与主审所见存在行归属分歧；需用目标普通桶受控 V2 请求及 CloudTrail selector 消除该歧义。Azure/GCP 还须确认日志类别、项目、方法、保留及匿名/共享凭证情况；取得同案原始列举与库存报告读取证据后再审子项。/ **en:** The fixed parent row and provider APIs establish the behavior, not chosen adversarial parameters or evasion success. Unit 42's victim lacked object-level logging, and its tool test cannot substitute for a victim List event. The live AWS resource table checked on 2026-09-22 omits V2 from the ordinary-object row, differing from the reviewer’s reading; a controlled ordinary-bucket V2 request and selector review must resolve it. Azure and GCP need checks of log category, project, method, retention, and anonymous or shared credentials. Same-case listing and inventory-report access evidence would be needed before promoting a child.

## 6. Deferred 子项双语核心内容（仅研究稿，非 NJS）

`D07-02-T1619-SUB-01` **既存对象清单转读 / Retrieval from a Preexisting Object Inventory**；`hypothesis; defer`；若将来获准，`lineage.attck_subtechnique_inherited: false`。它以**信息读取位置**而非 Inventory 产品名称为变量。

**summary — zh：** 攻击者从已有对象库存取得容器内部键名，使当次目标选择不触发源容器实时列举。/ **en:** An adversary obtains keys inside a container from an existing object inventory, so present target selection does not trigger a live list against the source container.

**definition_and_concept — zh：** 此候选要求源容器对象清单已经生成、被攻击者实际读取并用于确定目标；单是平台提供清单功能或合法治理作业生成报告并不足够。AWS/GCP 的 inventory 是实现线索，清单格式不是分类边界。/ **en:** The candidate requires an already generated source-container inventory that the adversary actually reads and uses for target selection. Merely offering inventory functionality or generating an authorized governance report does not qualify. AWS and GCP inventory services are implementation leads, not taxonomy boundaries or format-based siblings.

**stealth_characteristics — zh：** 既存对象清单转读把当次发现从源容器 List 请求移至报告文件 Get/读取或数据集查询，使只监听源容器列举的防守方失去这次目标选择的直接信号。报告访问仍应有自身痕迹；报告可能过期、仅含部分前缀，无法代表完整当前对象集。/ **en:** Retrieval from a Preexisting Object Inventory shifts present discovery from a source-container List request to a report-file read or dataset query. A defender watching only live source-container listings loses that direct signal. Report access can leave its own trace, and reports may be stale or limited to selected prefixes rather than the current full namespace.

**scope / scenario / models — zh：** 仅在攻击者有权读取含目标容器的既存报告且需要规避当次源桶列举时成立；报告正文的读取是为了发现键名，其日志需按所在存储或数据集另查。备份、成本核算和合规查询是强反例。防守方若同时关联报告访问与后续对象 Get，仍可恢复路径，但本研究没有真实同案。/ **en:** This applies only when an adversary can read an existing report containing the target container and uses it to avoid a current live listing. Reading the report body serves key discovery and must be audited through the report's storage or dataset channel. Backup, cost analysis, and compliance queries are strong counterexamples. A defender joining report access to later object Gets can recover the path, but no real same-case adversarial example was found here.

**mechanism / limit：** `NM-BT` 仅 `hypothesis`，`REF-09` 支持架构痕迹转移；缺恶意选择、报告实际读取和跨通道检测对照，不能进入正式子项。/ `NM-BT` remains a hypothesis: `REF-09` supports architectural trace relocation, while adversarial choice, actual report access, and cross-channel detection evidence are missing.

## 7. 可实施 DET/NJA/MIT 提案及逐目标限制

**`D07-02-T1619-DET-01`，建议 `create`：** 目标为在已知容器内部对象清单获取中识别与批准作业不符的身份、来源、范围和后继对象访问；覆盖获准父 T1619，域 `enterprise`。策略组织各云分析，不能把 T1580 的桶存在性或 NJT-0135 的 GetObject 收集轮次直接改标题充数。各 NJA 的阈值是待部署校准的工程设计，不是厂商或案例验证的检测率。

**`D07-02-T1619-NJA-01`，AWS 列举请求关联，建议 `create` 但设部署验证门：** CloudTrail S3 data events 只在相应 `resources.type`、目标桶 ARN、read 事件和 `eventName` selector 覆盖时可用；普通桶先用官方表明确列的 `ListObjects`，S3 Express/Access Point/Outposts 可列 V2，普通桶 V2 在受控请求核实实际记录后纳入。CloudTrail 必需字段为 `eventTime,eventSource,eventName,userIdentity,awsRegion,sourceIPAddress` 及从实际 `resources` 或 `requestParameters` 取的目标桶；`recipientAccountId,userAgent,readOnly,errorCode,requestParameters` 按实测可用性作为增强字段。`responseElements` 对只读调用为 `null`，不要求返回 key、KeyCount、prefix 或 token。备选为已启用的 S3 server access log `REST.GET.BUCKET` 与 `list-type=2` 请求 URI，但其投递 best effort。按 bucket+主体/凭证+来源聚合初始 24 小时的 List 和后继 GetObject，另以 7–30 天批准作业建立基线，均属待校窗口；首次来源、非批准范围及后继内容读取加权，不把单次 List 或分页判恶。误报含备份、浏览工具自动列举、索引、迁移和取证；盲区含未启用 data events、选择器漏桶、普通桶 V2 歧义、跨账户日志、server log 缺失、合法身份滥用与返回对象集不可见。

**`D07-02-T1619-NJA-02`，Azure Blob 列举，建议 `create`：** 输入为在 blob service 诊断设置中启用 `StorageRead` 并路由至 `StorageBlobLogs` 的 `OperationName == "ListBlobs"`；必需 `TimeGenerated,AccountName,OperationName,Uri,AuthenticationType,CallerIpAddress,StatusCode`，可得时关联 `RequesterObjectId,RequesterAppId,AuthenticationHash,UserAgentHeader`。以账户+容器 URI+OAuth 主体或 SAS signature hash+来源分组，按获批作业周期建立 24 小时行为窗口与较长基线，观察从 `ListContainers` 到 `ListBlobs` 再到 `GetBlob` 的序列，但只将中段归 T1619。SAS hash 仅帮助同令牌关联，不能替代人的归因。误报为 Storage Explorer、迁移、搜索索引和备份；盲区为未配诊断导出、错误表模式、SAS/Shared Key 的个人身份缺口、日志保留不足及合法身份滥用。窗口和偏离阈值需本地验证。

**`D07-02-T1619-NJA-03`，GCP 对象列举，建议 `create` 且逐部署验证方法：** 仅对已显式开启 Cloud Storage Data Access `DATA_READ` 的项目/桶查询 `storage.googleapis.com` 对象列举记录，核验实际 `protoPayload.methodName`（JSON `objects.list` 或部署中观察到的 gRPC 名称）、`resourceName`/bucket、`authenticationInfo.principalEmail`、`requestMetadata.callerIp`、时间、状态及可得请求过滤条件。按 project+bucket+principal+来源与批准作业关联，连接后继对象读取而不混为同一技术。误报为备份、分析、治理及控制台浏览；盲区为 Data Access 默认关闭、公开对象访问不追踪、字段遮蔽、跨项目 sink 缺失和请求不含完整返回清单。不能仅写 `storage.objects.list` 权限名作为日志方法名。

**`D07-02-T1619-MIT-01`，建议 `create` 或与已有控制 `split`：** Measure 1 是按业务主体和容器/可用前缀收紧对象列举权，审查 AWS `s3:ListBucket`、Azure Blob 数据读取或 SAS 的 `l`、GCP `storage.objects.list`，并保留确需全容器列举的批准作业；各云作用域能力须按具体授权模型实施，不承诺统一“只允许列键而绝不可读内容”。Measure 2 是对高价值容器部署并定期验证列举读日志、选择器、sink、保留和测试事件，同时记录批准的备份、索引、迁移身份及窗口。对获准父 T1619，`use` 为缩小失陷身份可见的对象命名空间并留下可关联的列举请求；`expected_effect` 为降低未经授权清单范围，增加发现阶段与后继 Get 的可见性；`limitations` 为业务作业可能仍需广泛列举、被盗的合法身份仍可读、CloudTrail/诊断/Data Access 未覆盖的历史行为不可追溯，且日志本身不证明返回了哪些键。对 deferred `SUB-01` 只给**条件性**应用：限制库存报告文件/数据集的读取权并审计报告访问；预期恢复替代入口可见性；限制为已被复制的离线报告、报告延迟及缺失跨通道日志。该应用在子项获准前不得写入正式 MIT。

## 8. 共享库 reuse / extend / create / split / defer

| 对象或临时键 | 建议 | 语义与去重理由 |
|---|---|---|
| `D07-02-T1619-REF-01` ATT&CK 官方页 | `create` 或同 URL `reuse` | 主审按 URL 查重；网页版本与固定工作簿区分。 |
| `REF-000513` | **`extend` locator 后 `reuse`** | URL 与 `REF-03` 相同，不另建 REF；定位扩至 `ListObjects`、明确列 V2 的资源行、默认关闭和 selector 规则，并把普通桶 V2 的行归属分歧留给目标验证。原 Get/Put locator 不够。 |
| `D07-02-T1619-REF-10` CloudTrail record contents | `create` 或 URL 相同则 `reuse` | 独立 AWS 官方 URL 只支持字段可用性、参数省略和只读 `responseElements: null`，不证明普通桶 V2 的资源表覆盖。 |
| `D07-02-T1619-REF-02/04/05/06/07/08/09` | `create` 或规范 URL `reuse` | AWS API/访问日志、Azure API/日志、GCP API/日志、Unit 42 调查和库存报告须逐 URL 查库；同一网页可支持不同精确段落，不按候选重复建源。 |
| `D07-02-T1619-CLM-01..05` | 原子 `create`，同命题再 `extend` | 父行为、审计前提、返回集限制、实验/实战边界、库存转读架构分别成立；库存恶意应用只可 `defer` 或 `hypothesis`。 |
| `D07-02-T1619-CASE-01` | `defer` | Unit 42 真实案例未留对象列举日志；AWS 调查博客为说明性示例；不制造 T1619 实战 CASE。若主审复用 Unit 42 已有 CASE，只能扩充“存储工具/对象访问”已证事实，不加 ListObjects 标签。 |
| `DET-000148` / `NJA-000156` | `split`，不 `extend` | 既有目标是 NJT-0135 的重复 GetObject 收集轮次，需要对象键和跨轮读取；本目标是 List 请求与授权作业/后继动作，数据、阶段和窗口不同。 |
| `MIT-000137` | 控制思想可 `reuse`，应用应 `split` 或审查后 `extend` | 其对象读取授权与审计治理面向 Collection 的 GetObject/重复源读取；T1619 的列举许可、请求日志和报告替代入口不同。若主审确认控制目的与措施完全同一，可新增逐目标 application；不可复制文字仅替换目标名。 |
| `D07-02-T1619-DET-01/NJA-01..03/MIT-01` | 倾向 `create`，待主审语义查重 | 策略统一检测目标；各 NJA 按实有日志和身份模型实现，不按产品拆 NJS。普通桶 V2 通道在目标环境验证前不作为必需输入。 |
| `D07-02-T1619-SUB-01`、`AX-02/04` 的 Claim、REL | `defer` | 缺同案攻击选择、稳定边界和独立防御效果；主审不因架构可行而预留正式 ID。 |

质量自检：父级双语草案分别回答定义、直接对象、痕迹和残余观察、范围与正常反例、攻防模型、机理证据、限制；deferred 子项首段匿迹特性以准确双语名称开头。与 NJT-0001 比较的是字段责任和因果深度，不复制其机理或子项数。正式化前需主审完成普通桶 V2 受控日志核验、三云实际采集/保留核验、共享库 URL/语义查重及五候选交叉边界审查。
