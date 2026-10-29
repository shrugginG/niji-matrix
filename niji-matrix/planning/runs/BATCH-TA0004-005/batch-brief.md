# BATCH-TA0004-005 研究与收敛约束

## 研究前冻结的前五项

以下顺序来自 matrix.yaml 锁定的 MITRE ATT&CK Enterprise 19.1 官方 Enterprise ATT&CK matrix 展示顺序。跨战术对象只能作为共享对象候选，不能替代 TA0004 的独立 retain、adapt 或 exclude 决议。

| 顺序 | ATT&CK ID | 英文父技术名称 | 现有决策 | 现有 Niji 对象 |
|---|---|---|---|---|
| 1 | T1548 | Abuse Elevation Control Mechanism | TA0004 adapt，DEC-TA0004-T1548 | NJT-0098；NJS-0098-001、NJS-0098-002 |
| 2 | T1134 | Access Token Manipulation | TA0004 adapt，DEC-TA0004-T1134 | NJT-0099；NJS-0099-001、NJS-0099-002、NJS-0099-003 |
| 3 | T1098 | Account Manipulation | TA0003 retain，DEC-TA0003-T1098；TA0004 retain，DEC-TA0004-T1098 | NJT-0083；NJS-0083-001、NJS-0083-002、NJS-0083-003 |
| 4 | T1547 | Boot or Logon Autostart Execution | TA0003 retain，DEC-TA0003-T1547；TA0004 retain，DEC-TA0004-T1547 | NJT-0084；NJS-0084-001、NJS-0084-002、NJS-0084-003 |
| 5 | T1037 | Boot or Logon Initialization Scripts | TA0003 retain，DEC-TA0003-T1037；TA0004 尚无决议 | NJT-0085；NJS-0085-001、NJS-0085-002 |

这五项是总体任务范围，不是五个正式 NJT 的产量承诺。当前批次只研究第 5 项 T1037，独立判断其 TA0004 相关性、权限结果门以及 NJT-0085 的跨战术复用、扩展或排除。完成本批只能声明本次前五候选完成，不能据此关闭 TA0004。

## 固定基线与批次控制

- 战术：TA0004 Privilege Escalation。
- ATT&CK domain：enterprise-attack。
- ATT&CK version：19.1；不迁移版本。
- TA0004 冻结父候选共十三项：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。第六至第十三项仍未开发。
- BATCH-TA0004-001 至 004 已通过证据、taxonomy、字段、防御、机器校验、Bundle 和双语 Web QA。
- 当前批仅 T1037；它有五项固定 ATT&CK 子技术，必须逐项或逐簇覆盖，并至少检查两个实质不同的候选匿迹轴或解释收敛。正式数量不按五项设配额。

## T1037 父级问题与跨战术边界

T1037 的直接对象是由启动或登录生命周期解释执行的初始化脚本正文、命令序列或脚本 hook，不是只指向不变目标的通用 autostart descriptor。TA0003 结果是脚本在后续生命周期恢复代码；TA0004 只有在攻击者能以较低权限影响脚本内容或其集中分发源，而脚本由更高权限 interpreter/consumer 执行并产生新获准操作时才成立。同一用户上下文的登录脚本持久化不能自动计为提权。

优先检查 NJT-0085 的同一脚本内容对象跨战术复用。既有 NJS-0085-001 固定“既有脚本中局部内联植入”，NJS-0085-002 固定“集中脚本一次修改向多目标 fan-out”；两者必须在 TA0004 下分别验证 line-level provenance、distribution scope 与 interpreter authority 对观察和防御的影响。权限差是父级结果门，不得按 root/SYSTEM、平台、语言、脚本名、GPO/共享目录或 ATT&CK 子技术机械拆分。

边界保持：只改变外部启动映射而脚本正文不变归 NJT-0084；service/daemon definition 归 T1543；scheduler state 归 T1053；非启动/登录事件订阅归 T1546；解释器代理、脚本混淆、下载和权限修改可并列记录但不取代本对象。

## 固定 ATT&CK 子技术覆盖先验

| 顺序 | ATT&CK 子技术 | 英文名称 | 代表的实现或行为维度 | 初始覆盖状态 |
|---|---|---|---|---|
| 1 | T1037.001 | Logon Script (Windows) | 本地或目录配置的 Windows 登录脚本内容 | pending |
| 2 | T1037.002 | Login Hook | macOS 登录 hook 脚本或命令 | pending |
| 3 | T1037.003 | Network Logon Script | 目录/GPO/共享源向账户或主机分发登录脚本 | pending |
| 4 | T1037.004 | RC Scripts | Unix/Linux/网络设备启动 RC 脚本正文 | pending |
| 5 | T1037.005 | Startup Items | macOS StartupItems 中生命周期脚本内容 | pending |

开放搜索至少覆盖：existing-script inline implantation、centralized-source fan-out、whole-script replacement/new script、interpreter authority transition、script-signing or policy bypass、pre-sensor execution、conditional host/user branches、platform/language/medium。每项标记 formal、hypothesis、parent-core、adjacent、deferred 或 rejected，并说明为何最终数量不增不减。

## 证据、共享库与门禁

先查 references、claims、cases、detections、analytics、mitigations 和 relationships。ATT&CK T1037 父页只锚定父行为、TA0004 映射与五项广度；脚本执行权限、集中分发、line-level diff、interpreter context、首个新获准结果和防御差异需窄证据。优先复用并必要时扩展 TA0003 的 REF/CLM/CASE、DET-000066、NJA-000045 和 MIT-000065，只有 stable key 或控制 owner 实质不同才 create/split。

正式变更保持 schema 2.0.0、中英逐段配对和候选特定 threat model/limitations。每项 mechanism 形成行为设计→痕迹变化→观察影响→匿迹效果。完成后运行 make quality、重建 NJT-0085 Bundle、检查 pipeline 与 reserved ID、运行 Review Web npm test，并实际渲染父、两个 NJS、DET/NJA/MIT 的 zh/en 页面、必要链接和 raw YAML。

## 执行安排

- 本任务未请求 sub-agent；主 Agent 串行完成。
- 暂存路径：planning/runs/BATCH-TA0004-005/。
- taxonomy、证据和七库决议完成前不写 canonical YAML。
- 完成本批后仅更新“前五候选 5/5”；TA0004 其余八个父候选、Niji-native gap、跨技术收敛与人工审查仍未完成，战术保持 active。
