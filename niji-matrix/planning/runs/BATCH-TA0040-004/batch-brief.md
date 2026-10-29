# BATCH-TA0040-004 最终研究与收敛约束

## 基线与范围

- 战术：TA0040 Impact；仅按固定 ATT&CK Enterprise 19.1 清单和当前 TA0040 正式矩阵计数。
- 最终批次处理三个剩余父候选：T1565 Data Manipulation、T1657 Financial Theft、T1667 Email Bombing。
- BATCH-TA0040-003 已通过质量、五个 Bundle 和完整 Web/API 门禁并处于 `review`。本批完成后还需执行 TA0040 全清单、跨技术、gap analysis、共享库、防御覆盖和人工评审状态的战术收敛。
- 三个候选分别由独立 sub-agent 研究；主 Agent 等三份交接全部返回后才做准入、查重、ID 分配和正式写入。

## 父技术边界

| 候选 | 直接行为或状态对象 | 必须检查的相邻边界 |
|---|---|---|
| T1565 | 仍可被系统或人员消费的数据值、消息或运行时结果被恶意改变，损害完整性、流程或决策 | NJT-0156 数据销毁、NJT-0187 展示内容篡改、NJT-0157 加密不可读、T1657 最终资产转移；stored/transmitted/runtime 仅作 ATT&CK 广度参考。 |
| T1657 | 受害方资金、数字资产或等价价值经未授权交易/结算实际转移给攻击者或其受益方 | NJT-0189 资源劫持只转移使用成本/容量；T1565 可操纵交易数据但没有完成价值转移；Credential Access、账户接管和业务邮件欺诈是前置。 |
| T1667 | 大量邮件进入目标邮箱或邮件服务，导致合法邮件难以发现、处理或投递并造成业务中断 | T1499 的端点/应用资源耗尽、T1498 网络容量洪泛、钓鱼/初始访问的诱饵投递、C2 邮件信道、T1621 MFA 请求轰炸；高量邮件 alone 需实际可用性/注意力结果。 |

## 原生 taxonomy 规则

- T1565 固定有 3 个 ATT&CK 子项（stored、transmitted、runtime），只作 planning-only 广度先验；至少比较两个实质不同的匿迹轴，不得按数据状态直接翻译为 NJS。
- T1657、T1667 无 ATT&CK 子项，仍需开放搜索时间、主体、交易/传输代理、观察域、归因、痕迹密度、合法业务外观等变量。
- 正式 NJS 必须具有攻击者可控稳定变量、痕迹变化、防守观察差异、前提、场景、结论级证据及不可互换防御；证据不足的轴保持 hypothesis/defer。零 NJS 或 exclude 可以成立，但须完整解释。

## 并行、共享库与防御边界

- 三名 sub-agent 各研究一个父候选，只写 `planning/runs/BATCH-TA0040-004/<ATTACK-ID>-handoff.md`，使用 `TA0040-<ATTACK-ID>-` 临时键。
- 不得修改正式矩阵、准入决策、共享库、战术计划、brief、ID 预留、集成摘要或 gap analysis。主 Agent 在三份结果全部返回前不分配正式 ID。
- 每份交接包含 retain/adapt/exclude 建议、完整双语父级/子项草稿、ATT&CK 覆盖决议、来源账本、共享库 reuse/extend/create/split/defer 建议和 NJT-0001 字段责任对照。
- DET/NJA 必须提供真实数据源、字段、窗口、关联、误报、盲区、调优；MIT 提供措施及逐目标 use/effect/limitations。ATT&CK 父页只锚定父行为，不能替代 NJS、机理、字段、阈值、控制效果或案例证据。

## 战术关闭附加门禁

- 三项完成后核对 15/15 固定候选均有正式 decision，统计只取 TA0040 正式矩阵。
- 复核原生 gap analysis、跨 TA0040 父级/NJS 重复、共享库精确/相似项、Detection/Mitigation 覆盖、ID 无悬空、全部 Bundle 与完整 Web/API。
- 机器通过后所有正式对象和 TA0040 计划仍保持 `review`；没有人工领域 reviewer 时不得把技术、批次或战术标为 `published`。
