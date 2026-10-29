# BATCH-TA0004-004 研究与收敛约束

## 研究前冻结的前五项

以下顺序来自 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1 官方 Enterprise ATT&CK matrix 展示顺序。既有跨战术对象只作为共享对象候选，不能替代 TA0004 下独立的 `retain`、`adapt` 或 `exclude` 决议。

| 顺序 | ATT&CK ID | 英文父技术名称 | 现有决策 | 现有 Niji 对象 |
|---|---|---|---|---|
| 1 | T1548 | Abuse Elevation Control Mechanism | TA0004 `adapt`，DEC-TA0004-T1548 | NJT-0098；NJS-0098-001、NJS-0098-002 |
| 2 | T1134 | Access Token Manipulation | TA0004 `adapt`，DEC-TA0004-T1134 | NJT-0099；NJS-0099-001、NJS-0099-002、NJS-0099-003 |
| 3 | T1098 | Account Manipulation | TA0003 `retain`，DEC-TA0003-T1098；TA0004 `retain`，DEC-TA0004-T1098 | NJT-0083；NJS-0083-001、NJS-0083-002、NJS-0083-003 |
| 4 | T1547 | Boot or Logon Autostart Execution | TA0003 `retain`，DEC-TA0003-T1547；TA0004 尚无决议 | NJT-0084；NJS-0084-001、NJS-0084-002、NJS-0084-003 |
| 5 | T1037 | Boot or Logon Initialization Scripts | TA0003 `retain`，DEC-TA0003-T1037；TA0004 尚无决议 | NJT-0085；NJS-0085-001、NJS-0085-002 |

这五项是总体任务范围，不是五项正式 NJT 的产量承诺。当前批次只研究 T1547，并独立判断 TA0004 相关性、直接对象、权限变化门槛以及 NJT-0084 跨战术复用或排除。T1037 只在本批全部门禁通过后进入下一批。

## 固定基线与批次控制

- 战术：TA0004 Privilege Escalation。
- ATT&CK domain：`enterprise-attack`。
- ATT&CK version：`19.1`；本任务不迁移版本。
- TA0004 冻结父候选共十三项：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。第六至第十三项仅冻结顺序，不进入本次前五开发。
- BATCH-TA0004-001 至 003 的证据、taxonomy、字段深度、防御、机器校验、Bundle 和双语 Web QA 已通过。
- T1547 在固定基线中有十四项 ATT&CK 子技术，强制单候选交付、逐项覆盖表和第二轮开放 taxonomy 搜索；本批未通过全部门禁前不写 T1037 的正式 YAML。

## T1547 父级问题与跨战术边界

T1547 的直接对象是由启动或登录生命周期消费的持久激活映射。其 TA0003 结果是当前会话结束后恢复执行；TA0004 只有在映射由比写入者或先前执行上下文更高权限的生命周期消费者执行，并产生可证明的有效权限增量时才成立。用户级 Run 项在同一用户权限下恢复载荷通常只承担 Persistence，不能因为发生于登录阶段就推断提权。

优先检查 NJT-0084 的同一映射对象能否跨战术扩展复用：如果 descriptor、target、scope、writer 和 lifecycle consumer 相同，应在父/子内容以及 DET/NJA/MIT 中增加 `writer/pre-state authority → lifecycle consumer/effective execution authority → privileged outcome` 结果门，而不是复制 NJT 或按高权限位置另建 Niji 子项。初始化脚本正文属于 T1037/NJT-0085；服务定义属于 T1543；启动/登录之外的事件订阅属于 T1546；调度状态属于 T1053；加载路径重定向属于 T1574；这些边界不因 TA0004 改变。

## 固定 ATT&CK 子技术覆盖先验

| 顺序 | ATT&CK 子技术 | 英文名称 | 代表的实现或行为维度 | 初始覆盖状态 |
|---|---|---|---|---|
| 1 | T1547.001 | Registry Run Keys / Startup Folder | 注册表或启动目录中的登录激活映射 | pending |
| 2 | T1547.002 | Authentication Package | 认证子系统加载的注册包 | pending |
| 3 | T1547.003 | Time Providers | 时间服务加载的 provider 注册 | pending |
| 4 | T1547.004 | Winlogon Helper DLL | Winlogon 生命周期 helper 注册 | pending |
| 5 | T1547.005 | Security Support Provider | LSA/SSPI 安全支持 provider 注册 | pending |
| 6 | T1547.006 | Kernel Modules and Extensions | 启动期内核模块或扩展加载状态 | pending |
| 7 | T1547.007 | Re-opened Applications | 前序会话到下次登录的恢复队列 | pending |
| 8 | T1547.008 | LSASS Driver | LSASS 受保护进程加载 driver 注册 | pending |
| 9 | T1547.009 | Shortcut Modification | 既有快捷方式描述符及目标变化 | pending |
| 10 | T1547.010 | Port Monitors | 打印子系统加载的 port monitor 注册 | pending |
| 11 | T1547.012 | Print Processors | 打印子系统加载的 processor 注册 | pending |
| 12 | T1547.013 | XDG Autostart Entries | Linux 桌面会话 autostart 描述符 | pending |
| 13 | T1547.014 | Active Setup | 每用户登录时消费的 Active Setup 状态 | pending |
| 14 | T1547.015 | Login Items | macOS 登录项及后台项目 | pending |

ATT&CK 子项只作为研究广度先验，不按平台、组件、介质、位置或子技术名导入。既有 TA0003 的三个正式轴——更新主题描述符伪装、既有描述符目标替换、会话恢复队列注入——必须在 TA0004 下重新验证是否有独立的提权观察和防御差异。还要开放搜索 writer/consumer privilege separation、system-scope versus user-scope、early-boot sensor gap、broker provenance、scope transition 与 trusted-component loading；每项最终标记为 `formal`、`hypothesis`、`parent-core`、`adjacent`、`deferred` 或 `rejected`。最终数量不按十四项设配额。

## 证据、共享库与门禁

先查 references、claims、cases、detections、analytics、mitigations 和 relationships。ATT&CK 父页只锚定 T1547 父行为、TA0004 映射与十四项广度。TA0004 retain 需要窄证据支持生命周期 consumer 的权限语义、写入/执行上下文差异和实际高权限结果；匿迹机理仍须形成“行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果”链。优先复用 TA0003 的 REF、CLM、CASE、DET-000065、NJA-000044 和 MIT-000064；只在新结论无法表达时 create 或 split。

正式内容保持 schema 2.0.0、中英逐段配对、候选特定 threat model 与 limitations。完成后运行 `make quality`、重建 NJT-0084 Bundle、检查 pipeline 和 reserved ID、运行 Review Web `npm test`，并实际渲染所有受影响父/子/DET/NJA/MIT 的 zh/en 页面、交叉链接与 raw YAML。

## 执行安排

- 本任务未请求 sub-agent；主 Agent 串行完成。
- 暂存路径：`planning/runs/BATCH-TA0004-004/`。
- coverage、第二轮 taxonomy、证据与七库决议收敛前不写 canonical YAML。
- 核心判断是同一持久激活映射何时仅恢复访问，何时通过生命周期消费者形成可证明的 authority delta；高权限位置、平台或 ATT&CK 子项本身都不是独立 Niji 子技术的充分条件。
