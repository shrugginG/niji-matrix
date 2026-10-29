# BATCH-TA0004-003 研究与收敛约束

## 研究前冻结的前五项

以下顺序来自 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1 官方 Enterprise ATT&CK matrix 工作表。跨战术对象只能作为共享对象候选，不能替代 TA0004 下独立的 retain、adapt 或 exclude 决策。

| 顺序 | ATT&CK ID | 英文父技术名称 | 现有决策 | 现有 Niji 对象 |
|---|---|---|---|---|
| 1 | T1548 | Abuse Elevation Control Mechanism | TA0004 adapt，DEC-TA0004-T1548 | NJT-0098；NJS-0098-001、NJS-0098-002 |
| 2 | T1134 | Access Token Manipulation | TA0004 adapt，DEC-TA0004-T1134 | NJT-0099；NJS-0099-001、NJS-0099-002、NJS-0099-003 |
| 3 | T1098 | Account Manipulation | TA0003 retain，DEC-TA0003-T1098；TA0004 尚无决议 | NJT-0083；NJS-0083-001、NJS-0083-002、NJS-0083-003 |
| 4 | T1547 | Boot or Logon Autostart Execution | TA0003 retain，DEC-TA0003-T1547 | NJT-0084；NJS-0084-001、NJS-0084-002、NJS-0084-003 |
| 5 | T1037 | Boot or Logon Initialization Scripts | TA0003 retain，DEC-TA0003-T1037 | NJT-0085；NJS-0085-001、NJS-0085-002 |

这五项是总体任务范围，不是五项正式 NJT 的产量承诺。当前批次只研究 T1098；必须独立判断其在 TA0004 下的相关性、直接对象与证据，并决定复用、扩展或拒绝既有 NJT-0083。T1547 和 T1037 在后续批次处理。

## 固定基线与批次控制

- 战术：TA0004 Privilege Escalation。
- ATT&CK domain：enterprise-attack。
- ATT&CK version：19.1；本程序不迁移版本。
- TA0004 冻结父候选顺序共十三项：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。第六至第十三项只冻结顺序，不进入本次前五开发。
- 当前交付候选：仅 T1098。BATCH-TA0004-001 与 002 的证据、taxonomy、字段、防御、机器校验、Bundle 和双语 Web QA 均已通过。
- 本批次全部门禁通过前，不得启动 BATCH-TA0004-004 的正式 YAML 写入。

T1098 含七项固定基线 ATT&CK 子技术，强制显式覆盖表和第二轮 taxonomy 搜索。其认证器、授权图、设备信任、云/目录/主机实现以及“持久状态”与“提权结果”的双重语义需要独立 ownership 和防御评估，因此作为单候选批次。

## T1098 父级边界与既有对象问题

T1098 的直接行为是修改既有账户的凭据、权限组或其他访问状态，以保存或提升访问。TA0004 成立必须证明该状态变化使攻击者取得比变更前更高的有效权限；仅保持现有访问而没有 authority delta 只承担 Persistence 语义。NJT-0083 的直接对象已经是既有身份的持久认证或授权状态，因此优先检查同一对象跨战术复用，而不是建立名称不同的重复 NJT。

与相邻对象的边界：T1136 负责新建身份；T1078 负责未修改状态的有效账户使用；T1556 负责全局认证过程；T1134/NJT-0099 负责令牌运行时上下文；T1548/NJT-0098 负责提权控制事务；角色/组/SID-History 等持久授权边按直接对象归 NJT-0083，即使其后进入 token。TA0004 结果必须在 detection 与 prose 中保留 pre-state、mutation、effective-authority delta 和首次高权限使用。

## 固定子技术覆盖先验

| 顺序 | ATT&CK 子技术 | 英文名称 | 代表的实现或行为维度 | 初始覆盖状态 |
|---|---|---|---|---|
| 1 | T1098.001 | Additional Cloud Credentials | 既有云身份新增密码、密钥或证书认证器 | pending |
| 2 | T1098.002 | Additional Email Delegate Permissions | 邮箱/邮件委托授权边 | pending |
| 3 | T1098.003 | Additional Cloud Roles | 云身份/应用新增角色或权限 | pending |
| 4 | T1098.004 | SSH Authorized Keys | 既有主机账户新增并行 SSH 公钥路径 | pending |
| 5 | T1098.005 | Device Registration | 既有身份绑定设备身份/设备信任 | pending |
| 6 | T1098.006 | Additional Container Cluster Roles | 容器编排主体新增角色/绑定 | pending |
| 7 | T1098.007 | Additional Local or Domain Groups | 本地或目录身份新增组成员边 | pending |

既有 TA0003 taxonomy 只作为研究输入：认证路径扩增、间接授权图扩增、身份绑定设备信任是三个已有正式轴；credential lifetime cycling 与 account-specific security-policy exception 为 deferred。TA0004 必须重新检查每个轴是否改变防守方对 privilege delta 的观察、关联、区分或归因，并执行 ATT&CK 分类之外的第二轮搜索。最终数量不按七项设配额；若没有新的 TA0004-specific stable stealth variable，应复用既有三个 NJS 并在父/子、DET/NJA/MIT 中补足战术结果边界，而不是复制子技术。

## 证据、共享库与质量门禁

先查 references、claims、cases、detections、analytics、mitigations 和 relationships。ATT&CK T1098 页面只锚定父行为、TA0004 映射和固定广度；凭据/SSH key、委托/角色/组、设备注册、authority delta、首次高权限使用和防御差异必须由窄证据支持。优先复用并在需要时扩展 TA0003 已有 REF/CLM/CASE/DET/NJA/MIT；只有 TA0004 新结论无法由既有对象表达时才 create 或 split。

正式变更必须保持 schema 2.0.0、中英文逐段配对和候选特定 threat model/limitations。每项 mechanism 写出行为设计→痕迹变化→观察影响→匿迹效果。完成后运行 `make quality`、重建 NJT-0083 Bundle、`pipeline_status.py`、reserved-ID 检查、Review Web `npm test`，并对所有受影响的父/子/DET/NJA/MIT 页面执行中英实际渲染、必要链接和原始 YAML QA。

## 执行安排

- 本任务未请求 sub-agent；主 Agent 串行完成。
- 暂存路径：`planning/runs/BATCH-TA0004-003/`。
- 在 coverage、第二轮 taxonomy、证据和 shared-library resolution 收敛前，不写 canonical YAML。
- 关键问题是同一身份状态对象如何分别承担 Persistence 的跨会话存续与 TA0004 的 authority delta，而不复制 taxonomy 或使用通用威胁模型。
