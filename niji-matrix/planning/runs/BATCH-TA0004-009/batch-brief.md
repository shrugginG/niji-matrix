# BATCH-TA0004-009 研究与收敛约束

## 固定候选与总体进度

唯一基线是 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1，不迁移版本。TA0004 十三个父候选顺序保持：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。前八项已经逐批通过；当前总体剩余范围为第 9–13 项。

| 批次 | 顺序 | ATT&CK 父技术 | 现有决策与 Niji 对象 | 状态 |
|---|---:|---|---|---|
| BATCH-TA0004-009 | 9 | T1546 Event Triggered Execution | TA0003 DEC-TA0003-T1546；NJT-0090 及两个既有 NJS | active |
| BATCH-TA0004-010 | 10 | T1068 Exploitation for Privilege Escalation | 待独立准入 | planned |
| BATCH-TA0004-011 | 11 | T1055 Process Injection | 待独立准入 | planned |
| BATCH-TA0004-012 | 12 | T1053 Scheduled Task/Job | TA0002 DEC-TA0002-T1053；NJT-0075 | planned |
| BATCH-TA0004-013 | 13 | T1078 Valid Accounts | TA0001 DEC-TA0001-T1078；NJT-0061 | planned |

T1546 在固定基线中有十八项 ATT&CK 子技术，按十项以上规则作为单候选批次。它未通过证据、十八项覆盖与第二轮 taxonomy、TA0004 权限结果、字段、防御对象、机器校验、Bundle 与双语 Web QA 前，不开始 T1068 正式 YAML 写入。候选必须重新独立得到 retain、adapt 或 exclude；既有 TA0003 决策和 NJT-0090 是优先复用对象，不是自动准入。当前 reserved ID 为零。

## 当前候选 T1546

T1546 的固定英文名为 Event Triggered Execution。研究必须从 Enterprise ATT&CK 19.1 的十八项子技术逐项记录 ID、名称与行为维度，并决议为 parent-core、niji-variable-candidate、adjacent-technique、evidence-deferred 或 not-stealth-distinct；不得导入、翻译或改名这些 ATT&CK 子技术。随后从分类内部、跨分类和分类外执行第二轮匿迹变量搜索。

现有 NJT-0090 已为 TA0003 建模 event registration/predicate → trusted broker/consumer → action outcome，并拥有两个 Niji-native 子项。当前批次优先验证该直接对象和 taxonomy 是否可以完整承载 TA0004：不仅要确认恶意动作被触发，还要证明较低权限 writer/caller 经 registration、consumer 或 Broker 获得更高 effective authority，并完成首个原 pre-state 无权执行的 operation。若只是同权限执行或持久触发，没有正权限差，则不能声明 Privilege Escalation。

## 权限结果与相邻边界假设

TA0004 分支的最低链为 lower-authority writer/caller pre-state → exact trigger registration or state → predicate satisfied → consumer/broker identity and effective policy → positive authority difference → first newly authorized action/result。单独存在 WMI subscription、profile、shim、IFEO、COM registration、installer、udev rule、trap 或事件触发进程，只能证明注册、消费或执行；consumer 为 root/SYSTEM 的标签也不能替代 writer pre-state、consumer adopted state 和实际授权结果。

与 TA0003 的 durable recurrence 共用直接对象时应 retain/extend 同一 NJT，而不是复制。T1547/T1037/T1543/T1053 分别拥有启动/登录点、初始化脚本、系统服务定义和 scheduler；T1574 等拥有加载顺序或组件劫持；T1068 拥有漏洞利用事实。当前批必须用 writer→state→consumer→action 的最窄直接对象处理重叠，并说明并列或排除条件。

## Taxonomy breadth 搜索

十八项 ATT&CK 实现不能决定 Niji 子技术数量。除逐项覆盖外，第二轮至少检查：

- trigger predicate 的选择性、环境值与仅在目标条件成立时的激活；
- registration writer 与 trusted broker/consumer 之间的来源转换；
- registration/state 的命名、位置、格式、分片、层级、precedence 与 inheritance；
- action inline、indirect payload、合法 host binary、script/profile、DLL/module 或 package consumer 的差异；
- trigger 创建、修改、使用、禁用、删除、恢复与残留 consumer/result 的时间关系；
- one-shot、recurrent、boot/login/event/request/session/package/device 等 trigger cadence；
- local、remote、domain/tenant、fleet fan-out 与跨 host/identity 的触发范围；
- writer authority、consumer authority、impersonation/delegation 和 first privileged result；
- 与 autostart、scheduled task、service、load-order hijacking、execution-flow hijack 及 vulnerability exploitation 的 ownership；
- 平台、产品、ATT&CK 子技术名、registry path、file name、event source、工具、介质、目标和日志字段分区。

formal 轴必须同时满足攻击者可控稳定键、持久 sibling 边界、痕迹属性改变、观察/关联/归因效果变化、明确场景、结论级证据及独立检测/缓解差异。既有两个 Niji 子项也必须重新通过门禁；可以合并、保留、降为 parent-core/hypothesis/deferred 或拒绝，不能因对象已存在而保留数量。

## 证据、共享库与门禁

先查询 references、claims、cases、detections、analytics、mitigations、relationships，并检查 TA0003 的 DEC/NJT/NJS/DET/NJA/MIT 及其 cases。ATT&CK 父页只锚定父行为、战术映射和官方子项；十八项覆盖、匿迹轴、权限差、检测与缓解结论必须使用层级匹配的技术文档、研究或事件证据。七库逐项决议 reuse、extend、create、split 或 defer；DET/NJA 保持双向引用，MIT applications 对父及每个保留子项提供目标特定 use、expected_effect、limitations。

正式内容继续采用 YAML-only `schema_version: 2.0.0` 和逐段中英配对。每项 mechanism 必须形成行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果；完成后逐字段对照 NJT-0001，运行 `make quality`、构建 Bundle、pipeline/reserved-ID 检查、Review Web `npm test`，并实际渲染父技术、全部子技术及 DET/NJA/MIT 中英文页面与跨对象引用。所有生命周期保持 review；本批完成只推进到 9/13，不声明 TA0004 关闭。
