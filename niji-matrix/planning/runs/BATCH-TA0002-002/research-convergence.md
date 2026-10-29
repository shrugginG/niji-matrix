# BATCH-TA0002-002 准入与分类收敛记录

本记录在正式 ID 分配前固定准入、父级范围、Niji 原生子技术分类和共享对象决议。全部候选都以 ATT&CK Enterprise 19.1 父技术为锚，`original_attack_subtechniques_imported` 一律为 `false`。

## 准入结论

| 候选 | 决策 | 置信度 | 收敛理由 |
|---|---|---|---|
| T1106 | adapt | medium | 原生 API 的一般使用不是匿迹；只保留攻击者有意绕开高层受监控接口或动态解析调用关系，从而改变传感器可见性和静态归因的执行实现。 |
| T1677 | retain | medium | 对流水线定义、间接构建输入或外部贡献触发面的投毒，会使攻击逻辑由受信 runner 和正常构建图执行，直接产生可论证的来源与因果断点。 |
| T1053 | retain | medium | 调度器保存未来执行条件并以受信调度主体启动程序，能够稳定分离创建与执行时刻，或把激活贴合正常维护节奏。 |
| T1648 | adapt | medium | 无服务器功能本身不是匿迹；只保留攻击者有意利用短驻实例、事件触发和控制面—运行时日志分离来降低主机级可见性的执行。 |
| T1129 | adapt | medium | 普通模块加载不是匿迹；只保留在既有进程中承载恶意功能或以内存驻留方式降低独立进程、静态制品和加载来源可见性的实现。 |
| T1072 | retain | medium | 企业软件部署和配置管理套件以受信管理身份向大量受管终端执行，能够借用维护工作流并跨目标或时段分散执行痕迹。 |
| T1569 | retain | medium | 服务管理器或守护进程可作为受信执行代理，且短驻服务的创建—启动—删除可压缩到轮询和短查询之间。 |
| T1127 | retain | high | ATT&CK 明确把受信、常带签名的开发实用程序代理执行及绕过应用控制作为父行为核心，匿迹因果直接成立。 |
| T1204 | adapt | medium | 用户动作本身不是匿迹；只保留攻击者有意让触发动作贴合正常工作流或跨多个交互表面分离诱导与执行因果的实现。 |
| T1047 | retain | medium | WMI/CIM 通过统一管理基础设施在本地或远程执行，能够让 provider 宿主承载结果并借用正常管理身份与命名空间。 |

## Niji 原生子技术分类

| 候选 | 临时键 | 子技术名称 | 稳定匿迹变量与兄弟边界 |
|---|---|---|---|
| T1106 | EX2-T1106-SUB-01 | 直接系统调用遥测层绕行 / Direct-System-Call Telemetry-Layer Bypass | 变量是绕过高层封装和用户态挂钩的调用路径；不等同于动态隐藏 API 身份。 |
| T1106 | EX2-T1106-SUB-02 | 动态解析原生调用 / Dynamically Resolved Native Invocation | 变量是运行时才解析调用目标并避免稳定静态导入关系；不要求绕过用户态挂钩。 |
| T1677 | EX2-T1677-SUB-01 | 受信流水线定义注入 / Trusted Pipeline-Definition Injection | 变量是直接改变版本化流水线图，使恶意步骤表现为已登记 job。 |
| T1677 | EX2-T1677-SUB-02 | 间接构建输入激活 / Indirect Build-Input Activation | 变量是保持主流水线定义不变，把攻击逻辑放入其引用的测试、构建或检查输入。 |
| T1677 | EX2-T1677-SUB-03 | 外部贡献情境门控执行 / External-Contribution Context-Gated Execution | 变量是由 fork、拉取请求或攻击者可控元数据满足特定触发条件后在有权限 runner 中执行。 |
| T1053 | EX2-T1053-SUB-01 | 基线合形计划激活 / Baseline-Conforming Scheduled Activation | 变量是让计划、身份、频率和窗口贴合已有维护或业务周期。 |
| T1053 | EX2-T1053-SUB-02 | 长周期延期计划执行 / Long-Horizon Deferred Scheduled Execution | 变量是把任务创建与实际运行分隔到不同保留窗口或启动周期。 |
| T1648 | EX2-T1648-SUB-01 | 短驻函数实例执行 / Ephemeral Function-Instance Execution | 变量是把代码限制在按需创建、执行后回收且无持续主机身份的运行实例。 |
| T1648 | EX2-T1648-SUB-02 | 良性事件流耦合执行 / Benign Event-Stream-Coupled Execution | 变量是把恶意函数或自动化绑定到高频正常业务事件，使单次调用混入预期事件流。 |
| T1129 | EX2-T1129-SUB-01 | 既有进程内模块承载 / Existing-Process In-Module Payload Hosting | 变量是让恶意功能作为显式加载模块在已有进程内运行，不产生独立载荷进程。 |
| T1129 | EX2-T1129-SUB-02 | 内存驻留模块实例化 / Memory-Resident Module Instantiation | 变量是从内存实例化并调用模块，减少可长期检查的落盘模块与路径关系。 |
| T1072 | EX2-T1072-SUB-01 | 批准部署窗口伪装 / Approved Deployment-Window Camouflage | 变量是使用预期维护身份、包命名与批准窗口下发攻击任务。 |
| T1072 | EX2-T1072-SUB-02 | 分批分布式终端执行 / Staged Distributed Endpoint Execution | 变量是把同一执行拆成小批次、不同目标与延迟波次，降低集中异常。 |
| T1569 | EX2-T1569-SUB-01 | 既有服务情境借用 / Existing-Service Context Borrowing | 变量是通过已存在服务或守护进程的受支持控制路径承载一次执行，不改变加载搜索关系。 |
| T1569 | EX2-T1569-SUB-02 | 短驻服务生命周期压缩 / Ephemeral Service-Lifecycle Compression | 变量是快速创建、启动并删除临时服务，使状态型盘点难以捕获完整生命周期。 |
| T1127 | EX2-T1127-SUB-01 | 受信实用程序输入代理执行 / Trusted-Utility Input-Proxy Execution | 变量是让受信开发实用程序解析攻击者项目、配置或调试输入并产生执行。 |
| T1127 | EX2-T1127-SUB-02 | 无独立制品实用程序内执行 / Artifactless In-Utility Execution | 变量是让恶意逻辑在实用程序进程或其内存中运行，不留下独立可执行制品。 |
| T1204 | EX2-T1204-SUB-01 | 工作流合形用户触发 / Workflow-Conforming User Trigger | 变量是把所需动作嵌入用户正在进行且语义合理的业务或支持工作流。 |
| T1204 | EX2-T1204-SUB-02 | 多步交互因果分离 / Multi-Step Interaction Causality Separation | 变量是把呈现、转录、打开或确认和最终执行分散到多个应用或时间点。 |
| T1047 | EX2-T1047-SUB-01 | Provider 宿主执行来源遮蔽 / Provider-Hosted Execution-Provenance Masking | 变量是让 WMI provider 宿主派生或承载结果，使直接请求者不出现在本地父子谱系。 |
| T1047 | EX2-T1047-SUB-02 | 日常管理情境合形 / Routine-Administration Context Conformity | 变量是让 WMI 方法、目标、身份和时间贴合既有管理基线，而非仅使用远程 WMI。 |

## 机理与防御收敛

- T1106 采用 `NM-BT` 与 `NM-DO`；新建原生调用路径检测 Strategy/Analytic，扩展 MIT-000058。
- T1677 采用 `NM-BT`、`NM-FD` 与 `NM-ST`；新建流水线图完整性检测 Strategy/Analytic 和 CI/CD 信任边界缓解。
- T1053 采用 `NM-ST` 与 `NM-FD`；与 T1569、T1047 共建调度器—服务—管理 provider 执行检测和治理缓解。
- T1648 采用 `NM-BT`、`NM-ST` 与 `NM-FD`；扩展 DET-000058、MIT-000057，并新建无服务器因果 Analytic。
- T1129 采用 `NM-BT` 与 `NM-DO`；扩展 DET-000059 与 MIT-000058，不改变现有 Analytic 的核心逻辑。
- T1072 采用 `NM-FD` 与 `NM-ST`；扩展 DET-000058、NJA-000032 与 MIT-000057。
- T1569 采用 `NM-BT` 与 `NM-ST`；使用本批次新建的调度器—服务 Analytic 与治理缓解。
- T1127 采用 `NM-FD` 与 `NM-BT`；扩展 DET-000059 与 MIT-000058。
- T1204 采用 `NM-FD` 与 `NM-ST`；扩展 DET-000060、MIT-000059，并新建真实用户动作因果 Analytic。
- T1047 采用 `NM-BT` 与 `NM-FD`；使用本批次新建的 WMI 请求—provider 结果 Analytic 与治理缓解。

共享库决议为：十项固定版本 ATT&CK Reference 和三十一项原子 Claim `create`；DET-000058、DET-000059、DET-000060、NJA-000032、MIT-000057、MIT-000058、MIT-000059 `extend`；三项 Detection Strategy、六项 Detection Analytic、两项 Mitigation `create`；Case 与 Relationship `defer`。动态 API 解析、内存模块、外部贡献触发和多步用户交互的证据强度不超过固定 ATT&CK 页面所支持范围，正式置信度最高为 `medium`；T1127 的受信代理与应用控制绕过由父技术直接陈述，可设为 `high`。
