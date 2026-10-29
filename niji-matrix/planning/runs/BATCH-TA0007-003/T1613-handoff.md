# T1613 Container and Resource Discovery / 容器与资源发现：只读研究交接

工作项 `WORK-TA0007-T1613`；批次 `BATCH-TA0007-003`；临时键前缀 `D07-03-T1613-*`。本文只提交主审待收敛的研究结果；未分配 NJT/NJS/REF/CLM/CASE/DET/NJA/MIT 正式 ID，未修改正式矩阵、共享库、规划清单或 ID 预留。本文中的 `formal` 只表示建议进入父级正式内容，不能视为已获正式对象身份。

## 1. 先行准入与零子项结论

**建议 `retain`，父级准入置信度 high；建议父级 `NM-FD` 机理置信度 low；正式 Niji 子项 0，taxonomy 建议 `deferred`。** 固定 ATT&CK Enterprise 19.1 工作簿 `/home/shrugging/project/theory_research/data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx` 的 `techniques` 表第 130 行记录 `T1613`、`Container and Resource Discovery`、战术 `Discovery`、平台 `Containers`、`is sub-technique=0`；全表没有 `T1613.*` 行，因此固定版 ATT&CK 子项数为 `0`、ID 为 `[]`。`original_attack_subtechniques_imported: false`。零 ATT&CK 子项仅是普通广度触发条件，不免除开放式 Niji taxonomy 搜索。

**准入理由（zh）：** T1613 的直接行为是取得容器环境中的集群、节点、命名空间、工作负载、镜像、部署及运行状态信息，并把这些实体和关系组成后继选择所需的资源图。固定工作簿记录 TeamTNT 使用 `docker ps`、`docker inspect` 和 Kubernetes Pod 搜索，Hildegard 搜索 kubelet 及其管理的运行中容器，Peirates 可按命名空间枚举 Pod；Unit 42 的 Hildegard 调查还直接记录从节点与容器发现转向后继容器执行和横向移动。这些材料足以证明父级行为及 Discovery 目的。保留 ATT&CK 父语义可以稳定信息对象；不需要把它改写成执行、部署或云 IaaS 发现。

**Admission rationale (en):** T1613 directly acquires cluster, node, namespace, workload, image, deployment, and runtime-state information in a container environment and joins those entities into a resource graph for later decisions. The fixed workbook records TeamTNT using `docker ps`, `docker inspect`, and Kubernetes pod searches, Hildegard searching for kubelets and their running containers, and Peirates enumerating pods in a namespace. Unit 42's Hildegard investigation further observes discovery of nodes and containers before later container execution and lateral movement. This evidence supports the parent behavior and its Discovery purpose. Retaining the ATT&CK parent preserves the information object without rewriting it as execution, deployment, or IaaS discovery.

**零 NJS 理由（zh）：** 已审查有效身份下正常读表象、中央 API 与节点局部观察面切换、查询范围收敛、既存/缓存视图转读、时间与来源分布等变量。来源能证明行为、接口能力和审计字段，却没有同一事件中的攻击者选择—痕迹变化—防守效果对照，也没有实测漏报或独立缓解差。Hildegard 的节点路径证明节点局部发现存在，但其 `masscan` 和匿名 kubelet 访问本身可能比合法控制器更显眼；Peirates 证明工具能力，不证明现场规避意图；分页、watch、selector 和命名空间范围都是正常客户端能力。因此证据不足时保持 `0 NJS`，不按 API、资源类别、平台或工具强制造子项。

**Why zero NJS (en):** The review examined ordinary read appearance under valid identities, switching between central and node-local observation planes, constrained query scope, retrieval from existing or cached views, and distribution over time or sources. The sources establish behavior, interface capability, and audit fields, but do not provide a same-incident comparison linking adversary choice to trace change and defender effect, a measured miss, or a distinct mitigation. Hildegard proves node-local discovery occurred, yet its `masscan` and anonymous kubelet access may be more conspicuous than legitimate controller activity. Peirates establishes tool capability rather than an observed evasion decision, while pagination, watch, selectors, and namespace scope are normal client behavior. The supported result is therefore zero formal NJS.

## 2. 结论级证据与来源层级

| 临时证据键 | 来源与库状态 | 直接支持的结论 | 不支持或必须校准的结论 |
|---|---|---|---|
| `D07-03-T1613-REF-ATTACK` | [MITRE ATT&CK T1613 固定版页面](https://attack.mitre.org/versions/v19/techniques/T1613)；上述 19.1 `techniques` 工作簿第 130 行；建议 `create` 专用 REF | 父行为、Discovery 映射、Containers 平台、零 ATT&CK 子项；固定版 procedure examples 为 TeamTNT、Hildegard、Peirates | 父页不能证明 Niji 子项、匿迹意图、审计完整性或检测效果；当前 live 页面已有 19.1 之后的新 procedure examples，本批不得吸收 |
| `D07-03-T1613-REF-DET0490` | 固定 19.1 `detectionstrategies` 第 243 行、`analytics` 第 1353 行及 `defensive mappings` 第 1457–1458 行；[ATT&CK DET0490](https://attack.mitre.org/detectionstrategies/DET0490/)；建议 `create` | AN1352 要求识别容器、Pod、节点等枚举，并把 Kubernetes/Docker 调用、Dashboard 活动和网络上下文相关联；映射列出 Kubernetes API Server 与 Docker daemon 两类通道 | 只给高层策略，不给可直接复制的窗口、阈值、完整 Docker 审计实现或实测性能 |
| `D07-03-T1613-REF-HILDEGARD` | [Unit 42: Hildegard](https://unit42.paloaltonetworks.com/hildegard-malware-teamtnt/)；建议 `create` | 2021 年活动中，攻击者从已入侵容器使用 `masscan` 搜索内部 kubelet，并通过 kubelet API 查找具体节点上的运行中容器，随后向这些容器推进执行与挖矿 | 不证明攻击者为绕过 kube-apiserver audit 而选择 kubelet；不提供检测命中率，也不证明所有 kubelet 架构都匿名或无日志 |
| `D07-03-T1613-REF-PEIRATES` | [InGuardians Peirates](https://github.com/inguardians/peirates) 及其 `GetPodsInfo`/namespace 代码；建议 `create` | 工具可在 Kubernetes 身份上下文中列 Pod，并把发现结果用于后继操作；证明 namespace 与身份范围在实现中存在 | 工具能力不是实际入侵案例；不能据此断言攻击者选择小范围查询以降低告警 |
| `REF-000211` | 现有 [Kubernetes Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)；`reuse` | kube-apiserver 可按 user、source IP、verb、resource/subresource、namespace、request URI、stage 和 response status 留痕；级别可从 `None` 到 `RequestResponse` | audit 未配置时无事件；`Metadata` 不含 request/response body；它不覆盖所有直连 kubelet、runtime 或本地 Docker socket 行为 |
| `REF-000212` | 现有 Kubernetes Authorization and Request Attributes；`reuse` | 授权按 user/group、verb、resource/subresource、namespace、API group 决定，可支持最小读权限与基线 | 授权成功不代表请求合法；RBAC 规则本身不证明实际调用或攻击意图 |
| `REF-000375` | 现有 Kubernetes Service Accounts；`reuse` | Pod 可通过 ServiceAccount 获得 namespaced 工作负载身份，默认账户、token 自动挂载与最小权限均可配置 | 证明身份机制，不证明 T1613 案例使用了被盗服务账户或实现了身份表象伪装 |
| `D07-03-T1613-REF-K8S-API` | [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/)；建议 `create` | `list/get/watch`、cluster/namespace scope、collection、`limit/continue`、field/label selector 等实际请求语义，可用于字段解析和候选轴审查 | 分页、watch 和 selector 是正常可靠性/效率能力，不能自动升级为匿迹技术 |
| `D07-03-T1613-REF-DOCKER-API` | [Docker Engine API](https://docs.docker.com/reference/api/engine/version/v1.40/)；建议 `create` | `docker ps` 映射 `GET /containers/json`，image list 与 inspect 具有可识别的 API 路径和过滤参数 | 文档定义接口，不保证部署默认保存每个只读请求；不能把 Docker lifecycle events 当作完整 API access log |
| `REF-000385` | 现有 Protect the Docker Daemon Socket；`reuse` | Docker 默认本地 socket、SSH/mTLS 和 authorization plugin 支持管理端点暴露控制 | 主要支持缓解，不能证明攻击案例或默认请求日志字段 |
| `REF-000214` | 现有 Docker System Events；`reuse`，仅作边界/盲区证据 | create/start 与 exec_create/exec_start/exec_die 可分别观察，且命令历史有限；帮助 T1609/T1610 事件链划界 | 没有列出 `docker ps`、inspect 或 image list 的只读请求事件；不得用它声称 T1613 已被 Docker events 完整覆盖 |
| `REF-000118` / `REF-000119` | 现有 T1609/T1610 ATT&CK 固定版来源；`reuse`，仅作相邻边界 | 既有容器管理执行与新容器部署是独立直接对象 | 不支持把发现请求本身解释为执行或部署 |

建议 `D07-03-T1613-CASE-HILDEGARD` 记录一个新 Case：主体为 TeamTNT/Hildegard，时间为 Unit 42 可证的 2021 年活动，中心事实为已入侵容器发起内部 kubelet 扫描、通过 kubelet API发现节点上的运行中容器、再向发现的容器推进执行。该 Case 可在主审分配 T1613 父级身份后同时关联新父级与 `NJT-0066`，但不得把“绕过中央审计”写成已观察事实。现有 `CASE-000073` 是 2022 年 Sysdig 所述的另一 TeamTNT kubelet 事件，事件身份不同，不合并。

建议原子 Claim：`D07-03-T1613-CLM-PARENT` 只陈述父级资源图发现；`D07-03-T1613-CLM-HILDEGARD` 只陈述 Hildegard 的 kubelet/容器发现与后继；`D07-03-T1613-CLM-AUDIT` 陈述 kube-apiserver audit 的字段和级别条件；`D07-03-T1613-CLM-READ-APPEARANCE` 陈述同类读接口可由用户、应用与控制面调用、恶意性需上下文判断，置信度 low；`D07-03-T1613-CLM-ZERO-NJS` 陈述当前轴均未通过正式子项门禁。

## 3. 父行为、事务终点与相邻边界

父行为的直接对象是**容器环境资源图**：cluster/daemon、node、namespace、workload/controller、Pod/container、image reference/digest、部署关系、运行状态和必要的所有者/调度关系。事务在攻击者取得可用于选择下一步的资源信息时结束；随后的 exec、创建容器、读取秘密、修改 RBAC、下载内容或横向移动是独立行为。CLI、API、SDK、Dashboard、kubelet 和 Docker socket 是入口，不是父级或 NJS 身份。

| 相邻对象 | 归属判据 | 与 T1613 的硬边界 |
|---|---|---|
| `NJT-0139` / T1580 Cloud Infrastructure Discovery | 查询云账户/项目中的 VM、VPC、安全组、卷、数据库、桶等 IaaS 实体和关系 | 托管 Kubernetes 的 node 可能同时是云 VM；如果直接问题是 cluster 内 Pod/namespace/workload/调度关系，归 T1613；如果直接问题是云 VM/网络/数据库/桶关系，归 NJT-0139。不得因同一云厂商重复分类 |
| `NJT-0066` / T1609 Container Administration Command | 管理请求在**既有容器**中产生新的命令或进程结果 | T1613 的 `list/get/inspect` 只取得资源信息；`pods/exec`、kubelet run command、Docker exec 的请求—runtime 事务才进入 NJT-0066。Hildegard 的“先发现容器、后执行”可形成相邻链，但不能合成一个行为 |
| `NJT-0067` / T1610 Deploy Container | 创建、调度或启动**新容器/workload**并产生攻击者执行 | 查询 deployment/Pod/image 不等于创建；POST/create、admission、runtime create/start 才进入 NJT-0067。发现结果可指导部署目标，但不继承部署子项 |
| T1526 Cloud Service Discovery | 判断云服务能力是否启用或可访问 | Kubernetes/Docker 作为服务是否存在与其中有哪些资源是不同问题；响应同时含能力和实体时按直接求取问题及后继用途裁定 |
| T1619 Cloud Storage Object Discovery | 列举已知存储容器中的对象键、前缀和对象元数据 | 容器镜像、Pod、Deployment 与运行容器不是对象存储键；镜像 registry 内 tag/manifest 的研究若直接寻找镜像资产可落 T1613，但 bucket/object key 仍归 T1619 |
| 正常反例 | controller、scheduler、CSPM、GitOps、Dashboard、SRE、备份/安全扫描与事件响应会大量读取资源 | 单条 `list/get/docker ps/inspect`、合法 ServiceAccount 或批准 user-agent 均不能独自判恶；必须比较身份职责、来源、资源/namespace 范围、时序和后继结果 |

边界上的双标记只在两个直接行为都被独立证实时使用。例如，同一会话先 `list pods` 再 `pods/exec` 可分别标记 T1613 与 NJT-0066；不能仅因发现请求返回 Pod 名就推断后继执行已经发生。类似地，查询 Deployment 后出现 create 必须有独立写事件和 runtime 结果，不能把读请求计入 NJT-0067。

## 4. Niji 原生轴审查：formal / defer / reject

已完成两轮开放搜索。第一轮从查询身份、范围、读取位置、时间/来源分布与返回语义检查；第二轮从中央 API、Dashboard、kubelet、Docker daemon/socket、缓存/日志视图及后继行为反向验证观察差。结果如下。

| 轴与临时键 | 攻击者可控变量 → 痕迹变化 → 防守观察差 | 证据、反例与结论 |
|---|---|---|
| `D07-03-T1613-AX-01` 有效身份下的正常读表象 | 使用已获 user/ServiceAccount/session 调用 `list/get/watch/inspect` → 请求保留真实主体、方法与资源，但外形与 controller、SRE、CSPM 或 Dashboard 相同 → 单事件难判断控制者目的，需身份职责和后继关联 | Kubernetes audit 与 ATT&CK AN1352 支持观察模型，未有固定版实案直接证明被盗工作负载身份用于 T1613 或测得漏报。**`formal: parent-core only`**，作为父级低置信 `NM-FD`，不拆 NJS |
| `D07-03-T1613-AX-02` 中央与节点局部观察面切换 | 选择 kube-apiserver、kubelet 或 Docker daemon/socket 取得资源 → 中央 API audit、节点网络/服务日志和本地主机进程痕迹不同 → 只看 kube-apiserver 的防守方可能漏掉节点局部读取 | Hildegard 直接证明 kubelet discovery，官方 audit 证明 kube-apiserver 观察边界；但没有同案说明攻击者为降低观察而选路径，也无 kubelet/Docker 审计对照。**`defer`**，当前最强子项假设 |
| `D07-03-T1613-AX-03` 查询范围收敛 | 选择单 namespace、已知名称、label/field selector 或少量资源类型 → 资源覆盖与事件扇出减少，请求参数仍可能可见 → 只按跨 namespace/资源种类计数的检测可能降分 | Peirates 能按 namespace 枚举，TeamTNT 固定版映射含特定 container 名，Kubernetes/Docker 官方文档证明 selector/filter；都未证明规避目的或独立缓解。**`defer`**，保留在父级 NJA 的评分维度，不正式化 |
| `D07-03-T1613-AX-04` 既存或被动视图转读 | 从 Dashboard cache、controller cache、Docker 日志或已保存输出取得资源图 → 本次可能没有新的权威 list 请求，转而留下页面、文件、日志或本地进程读取 → API-only 分析可能看不到当前取图 | ATT&CK 父页只笼统说明 Docker logs 可泄露环境；无固定版同案、具体缓存访问或统一审计面。该轴还可能跨入 T1083、日志枚举或 TA0009 内容读取。**`defer`**，必须先按读取对象和审计面 split 后再审 |
| `D07-03-T1613-AX-05` watch、分页、低速或多源分布 | 改变请求持续时间、页大小、间隔或来源 → 单窗口计数和单主体覆盖变化 → 短窗阈值可能弱化 | `watch` 与 `limit/continue` 是正常同步和规模控制能力；无恶意同案或互补分工证据。**`reject` 作为当前 NJS**，可作为 NJA 调优和长期关联要求 |
| `D07-03-T1613-AX-06` API、工具、产品、资源类别拆分 | 在 Kubernetes/Docker、CLI/SDK、Pod/node/image/deployment 间换实现 → 字段与日志通道不同，但直接信息对象不变 → 需要解析适配而非稳定匿迹分类 | 违反按产品、API、平台、工具或资源类造 NJS 的门禁。**`reject`**；仅用于数据源分支与边界测试 |

**收敛结果：** `proposed_niji_child_count: 0`；`coverage: deferred`；无 formal NJS。`AX-01` 进入父级机理，不构成兄弟项。`AX-02/03/04` 仅为 hypothesis/defer；`AX-05/06` reject。没有任何 ATT&CK 子项被继承或翻译。

## 5. 父级双语核心字段与机理提案

**Name / 名称：** 容器与资源发现 / Container and Resource Discovery。

**Summary / 摘要：** 攻击者读取容器环境中的集群、节点、命名空间、工作负载、镜像、部署与运行状态关系，以选择后继目标；这些读取可能混在合法平台盘点中，但仍保留身份、范围、入口与后继痕迹。 / The adversary reads cluster, node, namespace, workload, image, deployment, and runtime-state relationships in a container environment to select later targets. These reads can blend with legitimate platform inventory while still leaving identity, scope, entry-point, and successor traces.

**definition_and_concept** — zh：容器与资源发现是在已经可达的容器主机、daemon 或编排集群中取得资源实体、状态及关系的行为。其直接成果是“哪些集群/节点/命名空间/工作负载/镜像/运行容器存在、归谁管理、处于何种状态”的资源图，用于决定后续横向移动、执行、凭据访问或资源劫持目标。Dashboard、CLI、API、SDK、kubelet 和 socket 都只是取得同一信息对象的入口；接口或资源名称本身不构成 Niji 子项。 / en: Container and Resource Discovery acquires resource entities, state, and relationships from an accessible container host, daemon, or orchestration cluster. Its direct output is a graph answering which clusters, nodes, namespaces, workloads, images, and running containers exist, who owns them, and what state they are in, so later lateral movement, execution, credential access, or resource hijacking can be selected. A dashboard, CLI, API, SDK, kubelet, or socket is an entry to the same information object; interface and resource names do not define Niji children.

**stealth_characteristics** — zh：容器平台必须持续执行资源读取，controller、scheduler、GitOps、CSPM 与运维人员会产生大量与恶意枚举同形的 `list/get/watch/inspect`。请求本身常可见，但审计事件未直接编码控制者目的；Metadata 级别还不含返回对象，Docker 本地 socket 读取也不能由 lifecycle events 自动还原。攻击者若借用获准身份和常见客户端，单条读事件的恶意可区分性会降低；异常来源、scope 扩张、非常见资源组合、节点局部入口、网络扫描及后继 exec/create 仍是残余信号。Hildegard 的 masscan 与匿名 kubelet 路径说明某些发现会非常显眼，因此不能把父级所有实现概括成低噪声。 / en: Container platforms continuously read resources, and controllers, schedulers, GitOps, CSPM, and operators generate large volumes of `list`, `get`, `watch`, and `inspect` activity shaped like adversarial enumeration. Requests are often visible, but audit events do not directly encode the controller's purpose; Metadata-level audit omits returned objects, and Docker lifecycle events do not reconstruct local socket reads. Use of an entitled identity and familiar client can reduce the malicious distinguishability of an individual read, while unusual origin, scope expansion, uncommon resource combinations, node-local entry, network scanning, and later exec or create remain residual signals. Hildegard's masscan and anonymous kubelet path may be conspicuous, so the parent must not be characterized as uniformly quiet.

**scope_boundary_definition** — zh：纳入为求取容器环境资源实体、状态、所有者与关系而进行的读取。云账户中的 VM、VPC、数据库与桶资源图归 NJT-0139；容器服务能力是否存在归 T1526；桶内对象键归 T1619。对既有容器发起 exec 并产生进程归 NJT-0066，对新 workload/container 发起 create/start 归 NJT-0067。秘密正文读取、RBAC 修改、镜像拉取、命令执行和数据收集均需独立证据。controller、scheduler、CSPM、GitOps、Dashboard、SRE、备份、安全扫描和事件响应是强正常反例，不能仅凭成功 read 或工具名判恶。 / en: Include reads aimed at container-resource entities, state, ownership, and relationships. NJT-0139 owns VM, VPC, database, and bucket graphs in cloud accounts; T1526 owns service availability, and T1619 owns keys inside storage containers. Exec that produces a process in an existing container belongs to NJT-0066, while create or start of a new workload or container belongs to NJT-0067. Secret-content reads, RBAC changes, image pulls, command execution, and collection require separate evidence. Controllers, schedulers, CSPM, GitOps, dashboards, SRE, backup, security scanning, and incident response are strong benign counterexamples, so a successful read or tool name alone cannot establish maliciousness.

**application_scenarios** — zh：攻击者取得容器内 foothold、管理端点可达性、Docker socket、kubelet 入口、Dashboard 会话或 Kubernetes 身份后，可先定位节点、Pod、Deployment、DaemonSet、镜像和状态，再选择可进入的既有容器、可部署位置或含高价值身份的工作负载。Hildegard 从一个容器扫描内部 kubelet、发现其管理的运行中容器，再向这些容器推进执行，证明父级可直接服务于后继横向移动；该案例不代表所有资源读取都产生同样后继。 / en: After obtaining a container foothold, reachable management endpoint, Docker socket, kubelet entry, dashboard session, or Kubernetes identity, an adversary may locate nodes, pods, deployments, daemonsets, images, and state before selecting an existing container to enter, a deployment location, or a workload with valuable identity. Hildegard scanned internal kubelets from one container, found the running containers they managed, and then advanced execution toward them, directly showing how the parent can support later movement. That case does not make the successor universal.

**attacker_model** — zh：攻击者至少需要一个可读入口：有权执行 `list/get/watch` 的用户或 ServiceAccount、可达 Dashboard/API、Docker socket/daemon、kubelet 或已经泄露的资源输出。可见图受 RBAC、namespace、cluster/daemon、node、本地缓存时效和网络可达性约束，不预设 cluster-admin 或宿主 root。节点局部路径需能到达目标 node 或 socket；范围收敛查询需先有名称、namespace、label 或其他线索。 / en: The attacker needs at least one readable entry: a user or ServiceAccount allowed to perform `list`, `get`, or `watch`; a reachable dashboard or API; a Docker socket or daemon; a kubelet; or previously exposed resource output. RBAC, namespace, cluster or daemon, node, cache freshness, and network reachability bound the visible graph; cluster-admin and host root are not assumed. A node-local path requires reachability to the target node or socket, while a constrained query requires a prior name, namespace, label, or other clue.

**defender_model** — zh：防守方可能有 kube-apiserver audit、Dashboard/API gateway 日志、身份/token 元数据、RBAC 与 ServiceAccount 基线、kubelet/节点服务访问日志、Docker API 代理日志、端点进程、网络流量和后继 exec/create/runtime 事件。可见性取决于 audit policy、stage/level、响应对象保留、节点覆盖、Docker 请求日志是否另行部署及短命容器的保留。防守方应能把合法 controller/调度器的预期身份、来源、user-agent、资源、namespace 与 cadence 同异常查询比较；缺日志只能证明观察不足，不能证明攻击者成功规避。 / en: Defenders may have kube-apiserver audit, dashboard or API-gateway logs, identity and token metadata, RBAC and ServiceAccount baselines, kubelet or node-service access logs, Docker API proxy logs, endpoint processes, network flows, and later exec, create, or runtime events. Visibility depends on audit policy, stage and level, response-object retention, node coverage, separately deployed Docker request logging, and retention for short-lived containers. Defenders should compare expected controller and scheduler identity, origin, user agent, resource, namespace, and cadence with unusual queries. Missing telemetry establishes an observation gap, not successful evasion.

**stealth_mechanism proposal：** `NM-FD` primary，`low`。短摘要 zh「容器资源读取借用获准身份和平台盘点的可见特征」；en “Container-resource reads borrow visible features of entitled platform inventory”。分析 zh：攻击者若用已有 user、ServiceAccount 或管理会话发起与 controller/SRE 相同的 `list/get/watch/inspect`，日志保留真实身份、资源和结果状态，却不直接显示请求由攻击者控制；仅按 API 名或 read 成功判断的检测难以区分，需把主体职责、来源、scope 扩张和后继行为连成资源读取谱系。ATT&CK AN1352 与 Kubernetes audit/authorization 文档支持这种观察模型，但固定版实际案例没有直接证明被盗合法身份的伪装选择，也没有测量漏报，所以置信度为 low。Hildegard 的匿名 kubelet/masscan 不用来抬高该机理。 / en: When an adversary uses an existing user, ServiceAccount, or management session for the same `list`, `get`, `watch`, or `inspect` operations used by controllers and SREs, logs retain a real identity, resource, and result status without showing that the request is adversary-controlled. Detection based only on API names or successful reads cannot separate intent and must join principal duty, origin, scope expansion, and successors into a resource-read lineage. ATT&CK AN1352 and Kubernetes audit and authorization documentation support this observation model, but the fixed-version incidents do not directly establish deliberate impersonation through a stolen entitled identity or measure misses. Confidence therefore remains low, and Hildegard's anonymous kubelet scan does not raise it.

**subtechnique_taxonomy narrative** — zh：当前没有同时满足攻击者可控、稳定兄弟边界、痕迹变化、防守观察差、实际恶意证据和独立防御价值的子项。最优先的后续问题是“同一资源图从中央 API 还是节点局部入口取得”，其次是查询范围收敛与既存视图转读；它们必须取得同案路径选择与实际日志对照后才能 formal。分页、watch、时间稀释、产品和资源类别只保留为分析调优或 reject。 / en: No child currently satisfies attacker control, stable sibling boundary, trace change, defender-observation difference, observed malicious evidence, and distinct defense value together. The leading future question is whether the same resource graph is acquired from the central API or a node-local entry, followed by constrained query scope and retrieval from an existing view. Each requires same-incident path choice and actual log comparison before formalization. Pagination, watch, time dilution, products, and resource classes remain analytic tuning dimensions or rejected partitions.

**research.limitations** — zh：固定版 ATT&CK procedure mappings 中，Peirates 是工具能力，TeamTNT 的 `docker ps/inspect` 与 Pod 搜索来自 ATT&CK 汇总，当前未取得两篇原始报告的完整同案日志；只有 Unit 42 Hildegard 提供较完整的节点—容器—后继链。Kubernetes 文档证明 audit 与 API 语义，不证明某目标集群启用了相应 policy/level；Docker API 文档证明路径，不证明 daemon 默认保存读请求。当前 live ATT&CK 页面已增加 19.1 之后的 procedure examples，本批明确排除。未来若获得同案 kube-apiserver/kubelet/Docker 日志、被盗身份来源、实际 response scope 与检测结果，应重评 `AX-02/03/04` 和机理置信度。 / en: In the fixed ATT&CK procedure mappings, Peirates is tool capability, while TeamTNT's `docker ps`, `docker inspect`, and pod searches are ATT&CK summaries for which this review did not obtain complete same-incident logs from both original reports. Only Unit 42's Hildegard report provides a relatively complete node-to-container-to-successor chain. Kubernetes documentation establishes audit and API semantics rather than proving that a target cluster enabled a policy and level. Docker API documentation establishes routes rather than default retention of read requests. The live ATT&CK page now includes procedure examples added after 19.1, which this batch excludes. Same-incident kube-apiserver, kubelet, and Docker logs, stolen-identity provenance, actual response scope, and detection outcomes could change the `AX-02/03/04` and mechanism conclusions.

## 6. 暂缓子项的双语核心内容（研究稿，不分配 NJS）

`D07-03-T1613-SUB-NODE-LOCAL` **节点局部观察面资源发现 / Node-Local Observation-Plane Resource Discovery**，状态 `hypothesis; defer`；`lineage.attck_subtechnique_inherited: false`。这是 `AX-02` 的研究稿，不在 `proposed_subtechniques` 中。

**summary** — zh：攻击者从 kubelet、container runtime 或本地 daemon/socket 取得节点上的 workload 与容器图，使发现痕迹落在节点观察面，而非仅落在中央编排 API。 / en: The adversary obtains a node's workload and container graph from a kubelet, container runtime, or local daemon or socket, placing discovery traces in the node observation plane instead of only the central orchestration API.

**definition_and_concept** — zh：候选变量是同一类资源信息的权威读取位置：从节点局部管理面取得本节点 Pod/container/image/state，而不是通过 kube-apiserver 的 cluster/namespace collection 取得。只有请求确实命中节点局部入口并返回资源信息时才成立；kubelet、Docker 和 runtime 是实现，不能各自拆成兄弟项。 / en: The candidate variable is the authoritative reading location for the same resource information: acquiring node-local pods, containers, images, or state from a node management plane rather than obtaining a cluster or namespace collection through kube-apiserver. It applies only when a request actually reaches a node-local entry and returns resource information. Kubelet, Docker, and container runtimes are implementations rather than sibling children.

**stealth_characteristics** — zh：路径切换可使本次发现不产生 kube-apiserver audit 中的相应 `list/get`，转而留下节点网络、服务访问、本地 socket 或调用进程痕迹；只部署中央 audit 的防守方会缺失请求。节点端点扫描、匿名访问、非常见源和本地 CLI 仍可非常显眼，路径也可能被 API gateway、host audit 或网络监控完整观察，因此不能假定天然隐蔽。 / en: Switching paths can remove the corresponding `list` or `get` from kube-apiserver audit and instead leave node-network, service-access, local-socket, or invoking-process traces. A defender with only central audit lacks the request. Node-endpoint scanning, anonymous access, unusual origins, and local CLI processes can still be conspicuous, and an API gateway, host audit, or network monitor may observe the path completely, so the route is not inherently stealthy.

**scope_boundary_definition** — zh：纳入节点局部入口返回 T1613 资源图；通过 kubelet run command 或 Docker exec 产生进程归 NJT-0066，通过 daemon 创建/启动新容器归 NJT-0067，单纯发现 node IP/端口还可能属于网络服务发现。必须把“找到 kubelet”与“用 kubelet 列出其容器”分成前后证据。合法 node agent、CNI/CSI、监控、runtime 运维和故障排查是强反例。 / en: Include node-local entries that return a T1613 resource graph. Kubelet run-command or Docker exec that produces a process belongs to NJT-0066, daemon create or start of a new container belongs to NJT-0067, and merely finding a node IP or port may be Network Service Discovery. Evidence must separate finding a kubelet from using it to list its containers. Legitimate node agents, CNI or CSI components, monitoring, runtime operations, and troubleshooting are strong counterexamples.

**application_scenarios** — zh：已有容器 foothold 的攻击者可扫描内部 kubelet 或访问挂载的 Docker socket，先取得本节点或邻接节点上的运行容器，再选择 exec 或部署目标。Hildegard 直接支持 kubelet/容器发现和后继执行顺序，但没有提供中央与节点日志的成对比较。 / en: An adversary with a container foothold can scan internal kubelets or access a mounted Docker socket, obtain running containers on the local or adjacent node, and then select an exec or deployment target. Hildegard directly supports the kubelet and container discovery followed by execution, but does not provide paired central and node log comparison.

**attacker_model** — zh：需要能到达 kubelet/daemon/socket 并满足其认证授权条件，或已在具有本地 socket 权限的容器/主机上下文中；可见范围通常局限于节点或 daemon，不保证全 cluster 图。 / en: The attacker must reach a kubelet, daemon, or socket and satisfy or bypass its authentication and authorization, or already execute in a container or host context with local socket authority. Visibility is usually bounded to a node or daemon and does not guarantee a cluster-wide graph.

**defender_model** — zh：防守方需同时保留 kube-apiserver audit、节点网络流、kubelet/daemon/API proxy access、socket 调用主体、host process 和 runtime 事件，并以 node、source、principal、container 与时间连接。只有中央 audit 时，节点局部请求是盲区；只有 host process 时，直接 SDK/socket 调用又可能缺命令行语义。 / en: The defender needs kube-apiserver audit, node network flows, kubelet or daemon or API-proxy access, socket-calling subject, host process, and runtime events joined by node, source, principal, container, and time. Central audit alone leaves node-local requests blind, while host process data alone can miss semantics from direct SDK or socket calls.

**mechanism / defer reason** — 候选 `NM-BT`，`hypothesis`。行为设计为节点局部读取，痕迹从中央 audit 转移到节点/主机面，缺节点遥测时会落出有效观察；Unit 42 与 Kubernetes audit 架构分别支持行为和观察边界。当前仍不 formal，因为没有同案成对日志证明痕迹差、没有攻击者规避选择证据、没有检测效果或独立 mitigation 对照，而且扫描噪声可能抵消该效果。 / Candidate `NM-BT`, `hypothesis`. Node-local reading shifts traces from central audit to node and host telemetry, which can fall outside effective observation when node coverage is absent; Unit 42 and Kubernetes audit architecture separately support the behavior and boundary. It remains deferred because no same-incident paired logs establish the trace difference, no source establishes an evasion choice, no detection effect or distinct mitigation is measured, and scan noise may offset the effect.

## 7. 可实施 DET / NJA / MIT 提案

### 7.1 Detection Strategy

**`D07-03-T1613-DET-RESOURCE-GRAPH`（建议 `create`）— 容器资源图读取上下文关联 / Container Resource-Graph Read Context Correlation。**

目标 zh：重构 Kubernetes、Dashboard、kubelet 与 Docker 入口上的资源枚举，把请求主体、来源、资源/namespace scope、成功结果和后继动作同批准 controller/CSPM/GitOps/SRE 基线比较；先确认发现，再把 exec/create 作为独立后继证据。 / Objective en: Reconstruct resource enumeration across Kubernetes, dashboard, kubelet, and Docker entries; compare principal, origin, resource and namespace scope, successful result, and later actions with approved controller, CSPM, GitOps, and SRE baselines; establish discovery first and treat exec or create only as independent successor evidence.

建议两个 NJA 分担实际不同的数据平面，不能把 Kubernetes 与 Docker 仅因同属 Containers 平台塞进换名逻辑。Strategy 域为 `enterprise`，未来 `detects_refs` 只指向新 T1613 父级；若节点局部子项将来 formal，再经同目标和分析适用性审查扩展。

### 7.2 NJA-A：Kubernetes 与 kubelet 资源读取图

**`D07-03-T1613-NJA-K8S`（建议 `create`）— Kubernetes 资源读取身份—范围—后继分析 / Kubernetes Resource-Read Identity–Scope–Successor Analytic。**

**Logic zh：** 从 kube-apiserver audit 归一化 `list/get/watch`，保存 principal/token context、source IP、user-agent、verb、API group、resource/subresource、namespace/name、request URI 中的 selector/limit/continue/watch 参数、stage、authorization annotation 和 response status；在 RequestResponse 合规可用时只派生 returned kind/count/hash，不默认集中保存可能含秘密的完整对象。为每个 principal/session/source 生成 resource-read graph，先在 30 分钟内比较资源种类、namespace/node 范围、名称/selector 聚焦和首次来源，再与至少 14 日的 controller、scheduler、CSPM、GitOps、Dashboard 与 SRE 基线比较。成功读之后两小时内的 `pods/exec`、kubelet run、workload create 或敏感对象 read 仅作为独立 successor 加权，不改变前一读事件的技术归属。直接 kubelet access 有实际可用日志时归入同一 graph 并标记 `observation_plane=node`；没有节点通道时明确报盲区，不从中央 audit 缺失推断节点读取。

**Logic en:** Normalize `list`, `get`, and `watch` from kube-apiserver audit and retain principal and token context, source IP, user agent, verb, API group, resource or subresource, namespace or name, selector, limit, continue, and watch parameters from the request URI, stage, authorization annotations, and response status. When RequestResponse is available and policy permits, derive only returned kind, count, or hash rather than centrally storing full objects that may contain secrets. Build a resource-read graph per principal, session, and source; compare resource classes, namespace or node scope, name or selector focus, and first-seen origin over an initial 30-minute session, then compare at least 14 days of controller, scheduler, CSPM, GitOps, dashboard, and SRE baseline. `pods/exec`, kubelet run, workload create, or sensitive-object read within two hours after a successful read raises successor context while retaining separate technique attribution. Add direct kubelet access only when a real log channel exists and mark `observation_plane=node`; when it does not, report a blind spot rather than infer node reads from absence in central audit.

**Data requirements：**

| `source_type` | 实际通道 | 必需字段 |
|---|---|---|
| `kubernetes-api-audit` | kube-apiserver audit file/webhook | `timestamp,audit_id,stage,user,groups,extra_or_token_context,source_ips,user_agent,verb,object_ref.api_group,object_ref.resource,object_ref.subresource,object_ref.namespace,object_ref.name,request_uri,response_status.code,authorization_annotations,audit_level` |
| `kubernetes-resource-response-summary` | RequestResponse 派生摘要；可用时才启用 | `audit_id,returned_kind,returned_item_count_or_hash,response_bytes,continuation_present` |
| `kubelet-or-node-api-access` | 经部署验证的 kubelet access/API gateway/node service log；无标准通道时为缺口 | `timestamp,node_id,principal_or_peer,source_ip,http_method_or_rpc,request_path_or_operation,response_status,response_bytes,request_id` |
| `container-platform-identity-baseline` | RBAC/RoleBinding/ClusterRoleBinding、ServiceAccount/token inventory、IdP | `principal_id,token_issuer_or_audience,source_scope,allowed_verbs,allowed_resources,allowed_namespaces,role_binding,owner,expiry` |
| `approved-resource-reader-register` | controller/CSPM/GitOps/SRE/Dashboard 作业台账 | `principal_id,client_or_user_agent,source,expected_resources,expected_namespaces_or_nodes,expected_cadence,change_ticket,validity_window,owner` |
| `container-successor-events` | kube audit、kubelet/runtime、admission；只作关联 | `timestamp,principal_or_session,target_namespace,target_pod_or_workload,event_type,subresource_or_verb,runtime_outcome` |

**Observables：** 新主体/来源/user-agent 扩大到未批准 namespace 或 cluster-scoped node；工作负载 ServiceAccount 从非预期 Pod/source 读取多类资源；匿名或非常见来源访问 kubelet 并成功取得容器列表；短时资源图读取后出现同主体或同源的 exec/create。单条 list/get 只给低级线索。

**Correlation：** 初始 discovery session 为 30 分钟，长 `watch` 按 request/audit ID 持续到连接结束；successor 窗口从最后成功读后两小时开始部署验证；主体职责基线至少 14 日并按发布/备份周期扩展。维度为 `cluster,node,observation_plane,principal,token_session,source_ip_or_workload,user_agent,verb_or_operation,resource,subresource,namespace,object_name,selector,request_id,audit_id,successor,time`。这些窗口是工程起点，不是来源给出的有效阈值。

**False positives：** controller/scheduler/reconciler、GitOps/CSPM、Dashboard、SRE 排障、扩缩容、备份、安全扫描、事件响应和授权红队。**Blind spots：** audit 未配置或规则为 `None`，Metadata 无返回集，托管平台隐藏 policy，kubelet/node 未收 access log，ServiceAccount 被盗后仍来自正常 workload，缓存视图读取及低速长期拼接。**Tuning：** 按有到期时间的主体—来源—资源—namespace—cadence 台账降噪，不按 `kubectl`、常见 user-agent、system 身份或单个 ServiceAccount 永久放行；对 controller 身份仍保留来源变化、scope 扩张和异常后继。

### 7.3 NJA-B：Docker daemon 与本地 CLI/API 资源读取

**`D07-03-T1613-NJA-DOCKER`（建议 `create`，部署前验证通道）— Docker 资源读取调用者—API—后继分析 / Docker Resource-Read Caller–API–Successor Analytic。**

**Logic zh：** 在有反向代理、authorization plugin、daemon request instrumentation 或受管 Desktop/Engine 审计时，规范化 `GET /containers/json`、container inspect、`GET /images/json`、image inspect 与 daemon info 等只读路径，保存 authenticated client/peer、socket/transport、API version、filters、target、status 和 response bytes/count。对本地 Unix socket 再连接 host/container process telemetry 中的 `docker ps`、`docker inspect`、`docker images` 及其 parent、subject container/host、command line/hash；直接 SDK/socket 调用可能没有 CLI 进程，必须把它列为盲区。按 daemon+caller/session+source 在 30 分钟构建资源读图，与批准运维/监控作业比较；两小时内的 Docker exec_create/start 或 container create/start 仅作为独立 successor。

**Logic en:** Where a reverse proxy, authorization plugin, daemon request instrument, or managed Desktop or Engine audit exists, normalize read routes including `GET /containers/json`, container inspect, `GET /images/json`, image inspect, and daemon info. Retain authenticated client or peer, socket or transport, API version, filters, target, status, and response bytes or count. For a local Unix socket, join host or container process telemetry for `docker ps`, `docker inspect`, and `docker images`, including parent, subject container or host, and command line or hash. Direct SDK or socket calls may have no CLI process and must remain an explicit blind spot. Build a 30-minute resource-read graph by daemon, caller or session, and source, compare it with approved operations and monitoring jobs, and treat Docker exec or container create or start in the following two hours as independent successors.

**Data requirements：** `docker-engine-request` 的实际通道必须部署验证，字段为 `timestamp,daemon_id,authenticated_client_or_peer,source_ip_or_socket_subject,transport,http_method,api_version,path,filters,target_id_or_name,response_status,response_bytes_or_count,request_id`；`host-or-container-process` 字段为 `timestamp,host_id,subject_container_id,user_or_uid,parent_process,executable,command_line_or_hash,socket_inode_or_destination,process_start_key`；`docker-approval-baseline` 字段为 `caller,source,daemon,allowed_routes_or_commands,allowed_targets,job_window,owner,expiry`；successor fields 为 `exec_id_or_container_id,event_type,timestamp,caller_or_session,runtime_outcome`。

**False positives：** Docker 运维、监控、备份、镜像清理、CI runner、Desktop UI、安全与资产工具。**Blind spots：** Docker System Events 不提供完整只读请求审计，本地 socket 直连 SDK 缺 CLI 进程，代理只见 TLS 终端、命令行被截断、daemon 日志轮转和合法监控身份被盗。**Tuning：** 用调用主体、socket 来源、daemon、API route、filters、目标与作业时段建立到期基线；不能只按 `docker` 可执行文件或 `GET` 方法判恶。若环境没有 request 或 process 通道，Docker 分支应标为 unavailable，不能声称 DET 覆盖。

### 7.4 Mitigation

**`D07-03-T1613-MIT-READ-GOVERNANCE`（建议 `create`）— 容器资源读取权限与观察面治理 / Container Resource-Read Authority and Observation-Plane Governance。**

**Description zh：** 将资源读取身份、可见 cluster/namespace/node/daemon 范围、管理端点暴露和审计覆盖作为一个控制事务。Kubernetes 中按职责拆分 `list/get/watch` 与 exec/create，优先 namespaced RoleBinding，移除 wildcard 和无期限 cluster-wide read；ServiceAccount 使用短期、audience-bound token 并限制自动挂载。Docker/kubelet 管理端点不匿名暴露，保护本地 socket，远程访问使用 SSH/mTLS、网络限制与可用的 authorization layer。所有批准 controller/CSPM/GitOps/SRE 读取登记主体、来源、资源、scope、cadence 与到期，并从中央和节点两面验证日志到达。

**Description en:** Treat resource-read identity, visible cluster, namespace, node, or daemon scope, management-endpoint exposure, and audit coverage as one control transaction. In Kubernetes, separate `list`, `get`, and `watch` from exec and create by duty, prefer namespaced RoleBindings, and remove wildcards and indefinite cluster-wide read. Use short-lived, audience-bound ServiceAccount tokens and limit automatic mounting. Do not expose Docker or kubelet management endpoints anonymously; protect local sockets and use SSH or mTLS, network restrictions, and an available authorization layer for remote access. Register principal, origin, resources, scope, cadence, and expiry for every approved controller, CSPM, GitOps, and SRE reader, and test log arrival from both central and node observation planes.

**Measures：**

1. `least-resource-read-authority` / 资源读取最小权限：按 resource、verb、namespace 和职责审查 Kubernetes RBAC；把 Dashboard 与平台盘点的 read 身份同 exec/create 身份拆开。Docker socket 权限按宿主高权限面处理，不能把只读假设建立在 CLI 命令名上。 / Review Kubernetes RBAC by resource, verb, namespace, and duty; separate dashboard and inventory readers from exec and create identities. Treat Docker socket access as a high-authority host surface rather than assuming read-only use from a CLI command name.
2. `management-endpoint-exposure-control` / 管理端点暴露控制：禁用匿名 kubelet/daemon，限制 API server、Dashboard、kubelet 和 Docker remote API 的来源网络，使用短期/JIT 会话、SSH/mTLS 与授权插件。 / Disable anonymous kubelet and daemon access; restrict source networks for API server, dashboard, kubelet, and Docker remote API; use short-lived or JIT sessions, SSH or mTLS, and authorization plugins.
3. `central-and-node-read-audit` / 中央与节点读取审计：配置 kube-apiserver audit 覆盖关键 `list/get/watch`，保留 audit ID、主体、来源、URI、资源、namespace、stage 和结果；在节点/daemon 部署可验证的 access/process telemetry，定期以受控读请求测试路由和保留。 / Configure kube-apiserver audit for important `list`, `get`, and `watch` activity and retain audit ID, principal, origin, URI, resource, namespace, stage, and result. Deploy verified access or process telemetry on nodes and daemons and regularly test routing and retention with controlled reads.
4. `approved-reader-baseline-and-response` / 批准读取基线与处置：维护 controller/CSPM/GitOps/SRE 的主体—来源—scope—cadence—责任人台账；异常时冻结 token/session、保存中央与节点日志、确认实际可见资源范围，再分别调查后继 exec/create、轮换身份并修复端点暴露。 / Maintain principal, origin, scope, cadence, and owner records for controllers, CSPM, GitOps, and SRE. On anomaly, freeze the token or session, preserve central and node logs, establish actual visible resource scope, then investigate exec or create successors separately, rotate identity, and close exposed endpoints.

**未来父级 Application：** use zh：对 T1613 绑定读取身份与最小 namespace/resource/node/daemon 范围，保护 API、Dashboard、kubelet 与 Docker socket，并把批准读取台账同中央/节点审计比较。expected effect zh：减少攻击者可取得的资源图范围，移除匿名或不必要入口，使借用合法读接口的异常 scope 与来源更易区分。limitations zh：controller、scheduler、CSPM 与 GitOps 常需持续广域读取；被盗的批准身份仍可保持正常模式，Metadata audit 不还原完整返回集，Docker 本地 socket 也缺统一默认读审计，严格收敛可能破坏运维。 / use en: Bind T1613 readers to minimum namespace, resource, node, and daemon scope, protect API, dashboard, kubelet, and Docker socket entries, and compare approved-reader records with central and node audit. expected effect en: Reduce the resource graph available to an adversary, remove anonymous or unnecessary entries, and make abnormal scope and origin under legitimate read interfaces easier to distinguish. limitations en: Controllers, schedulers, CSPM, and GitOps often need continuous broad reads; a stolen approved identity can preserve normal patterns, Metadata audit does not reconstruct the full returned set, Docker local sockets lack uniform default read auditing, and aggressive restriction can disrupt operations.

**证据与实现限制：** `REF-000211/212/375/385` 支持 audit、授权、ServiceAccount 与 endpoint 控制；`D07-03-T1613-REF-DET0490/K8S-API/DOCKER-API/HILDEGARD` 支持检测对象、请求语义和案例。30 分钟、两小时与 14 日均为初始工程参数，必须用本地发布/调度周期回放校准。为避免秘密二次暴露，response body 默认不集中保存，只在政策允许时派生对象 kind、数量或受控 hash。

## 8. 共享库 reuse / create / defer 决议

| 对象 | 决议 | 理由与限制 |
|---|---|---|
| `REF-000211`, `REF-000212`, `REF-000375`, `REF-000385` | `reuse` | 分别支持 Kubernetes audit、授权、ServiceAccount 和 Docker endpoint 控制；不扩写为攻击案例或检测效果 |
| `REF-000214`, `REF-000118`, `REF-000119` | `reuse`，boundary only | 用于区分只读发现、既有容器 exec 和新容器 create/start；不作为 T1613 只读请求已被 Docker events 观察的证据 |
| `REF-000625` ATT&CK 19.1 STIX baseline | `extend` 或仅由主审选择性 `reuse` | 宽基线 REF 的 canonical URL 已存在但当前 locator 未含 T1613；主审可扩展 locator/notes，不能复制同一 STIX URL。为清晰引用单技术，可另 `create` 不同 canonical URL 的 `D07-03-T1613-REF-ATTACK` |
| `D07-03-T1613-REF-ATTACK`, `REF-DET0490`, `REF-HILDEGARD`, `REF-PEIRATES`, `REF-K8S-API`, `REF-DOCKER-API` | `create`，先做 canonical URL 最终查重 | 当前共享库精确 URL 检索无命中；Peirates 只标工具能力，Unit 42 才形成 Case 证据；ATT&CK live 新增项不得进入固定 19.1 结论 |
| `D07-03-T1613-CLM-PARENT/HILDEGARD/AUDIT/READ-APPEARANCE/ZERO-NJS` | `create` | 五项命题的主体、证据层级与因果强度不同，不合并成一条“父页证明全部”主张 |
| `D07-03-T1613-CASE-HILDEGARD` | `create` | 与 `CASE-000073` 的时间、来源和中心事实不同；新 Case 只保留 Unit 42 实际观察，不写“规避中央审计” |
| `DET-000150` / `NJA-000158` / `MIT-000139`（NJT-0139） | `split`，不 extend 为 T1613 | 其目标和通道是 IaaS CloudTrail 跨服务资源读取；T1613 需要 kube audit、节点/kubelet、Docker request/process 与 RBAC/ServiceAccount 基线，数据和措施实质不同 |
| `DET-000081` / `NJA-000060` / `MIT-000081`（T1609） | `reuse` 作后继边界，**不 extend coverage/application** | 对象是 exec 请求到 runtime 结果；T1613 是资源读取。可在新 NJA 中关联其事件类型，但不能把 exec 策略冒充 discovery 检测 |
| `DET-000082` / `NJA-000061` / `MIT-000082`（T1610） | `reuse` 作后继边界，**不 extend coverage/application** | 对象是 create/admission/image/first-action；发现 deployment/image 仍是 read，不满足其 create/start 事务 |
| `D07-03-T1613-DET-RESOURCE-GRAPH`, `NJA-K8S`, `NJA-DOCKER`, `MIT-READ-GOVERNANCE` | `create` | 检测目标、数据平面、关联逻辑和控制措施均与现有容器执行/部署及 IaaS 读取对象不同；NJA-DOCKER 正式化前必须验证实际 request/process channel |
| `D07-03-T1613-SUB-NODE-LOCAL`、AX-03/04 对应 Claim/REL/MIT Application | `defer` | 缺同案痕迹对照、攻击者规避选择、实测防守效果和正式 target_ref；不得预留 NJS 或提前写 MIT application |
| Hildegard discovery → `NJT-0066` 的关系 | `defer` 至父级分配后再 `create` | Unit 42 支持 discovery 后进入既有容器执行，但关系源端尚无正式 NJT；不得用临时键写共享 REL |

## 9. 交接门禁自检

- `recommendation.decision: retain`；`confidence: high`；`original_attack_subtechniques_imported: false`。
- 固定 ATT&CK 19.1 子项 `0 / []`；已完成多轴开放搜索与第二轮观察面检查；正式 NJS `0`，`coverage: deferred`。
- 已给出 6 个轴并明确 `formal-parent-core / defer / reject`；没有按 Kubernetes、Docker、API、资源类型或工具造 NJS。
- 父级双语字段覆盖定义、匿迹特性、边界、场景、攻击者模型、防守方模型、机理、taxonomy 和限制；暂缓子项也提供了双语核心字段与 defer 原因。
- DET 定义检测目标；两个 NJA 分别列出真实数据通道、字段、逻辑、窗口、维度、误报、盲区和调优；MIT 给出可实施 Measure 及父级 use/effect/limitations。
- 发现与后继 exec/create 在逻辑、时间窗和边界中分开；`NJT-0139`、`NJT-0066`、`NJT-0067` 均有明确对象边界。
- 已按 canonical URL、ATT&CK ID、事件身份和语义目标查重并给出 `reuse/create/extend/split/defer`；未分配正式 ID，未修改正式矩阵或共享库。
- 证据限制保留：Peirates 是能力材料；Hildegard 不证明规避意图；Kubernetes/Docker 文档不证明目标部署实际留存；ATT&CK live 超出 19.1 的新 procedure examples 未纳入。

