# BATCH-TA0004-006 研究与收敛约束

## 总体范围与当前交付

固定基线为 matrix.yaml 锁定的 MITRE ATT&CK Enterprise 19.1，不迁移版本。TA0004 的十三个父候选顺序保持：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。前五项已经逐批通过证据、taxonomy、字段、防御、质量、Bundle 和双语 Web QA；当前剩余总体范围为第 6–13 项。

剩余八项登记为连续单候选批次：

| 批次 | 顺序 | ATT&CK 父技术 | 现有相关 Niji 对象 | 状态 |
|---|---:|---|---|---|
| BATCH-TA0004-006 | 6 | T1543 Create or Modify System Process | TA0003 DEC-TA0003-T1543；NJT-0089 | active |
| BATCH-TA0004-007 | 7 | T1484 Domain or Tenant Policy Modification | 待独立准入 | planned |
| BATCH-TA0004-008 | 8 | T1611 Escape to Host | 待独立准入 | planned |
| BATCH-TA0004-009 | 9 | T1546 Event Triggered Execution | TA0003 DEC-TA0003-T1546；NJT-0090 | planned |
| BATCH-TA0004-010 | 10 | T1068 Exploitation for Privilege Escalation | 待独立准入 | planned |
| BATCH-TA0004-011 | 11 | T1055 Process Injection | 待独立准入 | planned |
| BATCH-TA0004-012 | 12 | T1053 Scheduled Task/Job | TA0002 DEC-TA0002-T1053；NJT-0075 | planned |
| BATCH-TA0004-013 | 13 | T1078 Valid Accounts | TA0001 DEC-TA0001-T1078；NJT-0061 | planned |

单候选批次防止跨战术复用、漏洞或边界逃逸证据，以及高广度 taxonomy 相互压缩。当前 T1543 未通过全部候选门禁前，后续批次不得进入 canonical YAML 写入。八个候选是程序范围，不代表必须产生八个新 NJT。

## 当前候选 T1543

T1543 的 ATT&CK 英文父技术名为 Create or Modify System Process。固定 19.1 有五项子技术：T1543.001 Launch Agent、T1543.002 Systemd Service、T1543.003 Windows Service、T1543.004 Launch Daemon、T1543.005 Container Service。它们只作为实现广度先验，不得翻译为 Niji 子技术。

TA0003 已将该候选 adapt 为 NJT-0089 Durable System-Service Definition，并建立 NJS-0089-001 Established-Service Identity Substitution 与 NJS-0089-002 Enumeration-Restricted Service Registration。当前批次必须独立判断 T1543 在 TA0004 下 retain、adapt 或 exclude；优先检查同一 service definition stable key 是否应跨战术扩展复用，而不是复制技术。

## 权限结果与边界假设

TA0004 只有在攻击者控制的服务/守护进程定义可由低于结果的 writer 或 pre-state 影响，服务管理器随后以更高有效权限创建进程、容器或其他执行主体，并由该定义导致首个新获准操作时成立。新建高权限服务、SYSTEM/root service process、容器 service 或管理员修改本身都不能替代 writer→definition→manager→execution context→authority delta→outcome 证据。

直接对象是持久 service definition，包括身份、目标、参数、账户、权限与生命周期语义。无持久状态的即时服务管理器执行归 T1569；只改目标二进制内容归 NJT-0087；模块/依赖解析劫持归 T1574；计划时间触发归 T1053；容器逃逸到宿主归 T1611。平台、service manager、unit/Registry/plist、服务名、账户名和目标类型不得机械成为 Niji 子项。

## Taxonomy breadth 要求

五项 ATT&CK 子技术触发至少两个实质不同的候选匿迹轴检查。必须逐项或逐簇决议：

- established-service identity replacement；
- new service disguised by generic or vendor-like naming；
- service definition target/argument substitution；
- service-account or execution-context transition；
- delayed/restart-only activation；
- distributed desired-state or orchestrator fan-out；
- transient service creation/deletion；
- platform、manager、unit medium。

每个轴必须标记 formal、hypothesis、parent-core、adjacent、deferred 或 rejected，并解释 trace、观察、前提、证据与防御差异。最终正式 Niji 数量可以为零或任意有证数量，但必须说明为什么不多也不少。

## 证据与共享库

先查询 references、claims、cases、detections、analytics、mitigations 和 relationships。ATT&CK T1543 父页只能锚定父行为、TA0004 映射与子项广度；服务身份连续、definition mutation、manager execution、token/context、首个新获准结果、检测字段和缓解效果需结论级窄证据。

优先审查 TA0003 的 NJT-0089、现有 NJS、Reference/Claim/Case、Detection Strategy/Analytic 与 Mitigation，并将每个对象决议为 reuse、extend、create、split 或 defer。若案例只证明持久服务而没有权限 delta，不得作为 TA0004 成功证据。

## 门禁

正式内容继续使用 YAML-only schema_version 2.0.0 和逐段中英配对。每项 mechanism 必须形成行为设计→痕迹变化→防守观察影响→匿迹效果。完成后逐字段与 NJT-0001 比较，运行 make quality，构建 technique bundle，检查 pipeline 和 reserved ID，运行 Review Web npm test，并实际渲染父技术、全部子技术、DET/NJA/MIT 的中英文页面、交叉引用和 raw YAML。

所有 lifecycle 保持 review。完成本批只推进到 6/13，不得开始 T1484 正式写入或声明 TA0004 关闭。
