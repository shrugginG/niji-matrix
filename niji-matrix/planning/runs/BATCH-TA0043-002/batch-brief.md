# BATCH-TA0043-002 研究与收敛约束

## 范围

本批次处理 ATT&CK Enterprise 19.1 中 TA0043 目标侦查的五个父技术候选：T1592、T1589、T1590、T1591、T1598。每项必须形成准入决策；只有 retain、adapt 或 add 才形成正式 Niji 技术。

## 父技术边界

| 候选 | 直接信息目标 | 与兄弟候选的主要边界 |
|---|---|---|
| T1592 | 主机、设备、平台和端点属性 | 不以人员身份、网络拓扑或组织运作为主要信息对象 |
| T1589 | 人员、账户及数字身份属性 | 组织岗位属于 T1591；网络与端点属性分别属于 T1590/T1592 |
| T1590 | 网络命名、地址、拓扑、信任与边界属性 | 单主机平台属性属于 T1592；一般主动探测行为还需与 NJT-0001 区分 |
| T1591 | 组织结构、业务关系、角色和运营规律 | 个人身份记录属于 T1589；网络结构属于 T1590 |
| T1598 | 通过电子社会工程直接诱导目标披露信息 | 以执行代码或取得访问为目标的钓鱼不属于本技术 |

## 子技术规则

- 不读取或导入 ATT&CK 原子技术作为 Niji 子技术分类。
- 子技术必须由匿迹实现变量区分，而不是由信息类别、数据字段或工具名称区分。
- “查询公开资料”本身不自动构成匿迹；必须说明行为如何降低受害方观测、跨事件关联、可区分性或归因能力。
- 相同来源或控制逻辑应复用全局 REF、CASE、DET、MIT 或 CLM；同名但因果与适用范围不同的对象不得强行合并。
- 主动请求目标基础设施时，必须说明与 NJT-0001 主动扫描的主要目的和边界；必要时使用 relationship，而不是复制分类。

## English convergence notes

Partition the five parent candidates by their immediate information object: host, identity, network, organization, or direct social elicitation. Derive children from stealth implementation variables rather than information categories. Passive or public collection is not inherently an evasion sub-technique unless it demonstrably changes victim-side observability, correlation cost, distinguishability, or attribution. Reuse canonical global-library objects and keep Active Scanning boundaries explicit.
