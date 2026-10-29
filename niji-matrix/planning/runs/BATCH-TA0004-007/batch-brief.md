# BATCH-TA0004-007 研究与收敛约束

## 固定候选与总体进度

唯一基线是 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1，不迁移版本。TA0004 十三个父候选顺序保持：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。前六项已逐批通过；当前总体剩余范围为第 7–13 项。

| 批次 | 顺序 | ATT&CK 父技术 | 现有决策与 Niji 对象 | 状态 |
|---|---:|---|---|---|
| BATCH-TA0004-007 | 7 | T1484 Domain or Tenant Policy Modification | 初始预检未发现 T1484 origin 的正式 DEC/NJT；待七库精确复核 | active |
| BATCH-TA0004-008 | 8 | T1611 Escape to Host | 待独立准入 | planned |
| BATCH-TA0004-009 | 9 | T1546 Event Triggered Execution | TA0003 DEC-TA0003-T1546；NJT-0090 | planned |
| BATCH-TA0004-010 | 10 | T1068 Exploitation for Privilege Escalation | 待独立准入 | planned |
| BATCH-TA0004-011 | 11 | T1055 Process Injection | 待独立准入 | planned |
| BATCH-TA0004-012 | 12 | T1053 Scheduled Task/Job | TA0002 DEC-TA0002-T1053；NJT-0075 | planned |
| BATCH-TA0004-013 | 13 | T1078 Valid Accounts | TA0001 DEC-TA0001-T1078；NJT-0061 | planned |

T1484 单候选批次未通过证据、taxonomy、字段、防御对象、机器校验、Bundle 与双语 Web QA 前，不开始 T1611 正式 YAML 写入。候选必须独立得到 retain、adapt 或 exclude；不预设会建立 NJT 或 NJS。

## 当前候选 T1484

T1484 的固定英文名为 Domain or Tenant Policy Modification。Enterprise 19.1 有两项子技术：T1484.001 Group Policy Modification、T1484.002 Trust Modification。它们分别表示集中组策略与域/租户信任关系实现，只作为研究广度先验，不得翻译、导入或改名为 Niji 子技术。

本批初始预检未发现以 T1484 为 origin 的正式 decision 或 NJT。研究必须先判断直接对象究竟是 policy version、trust relation/edge、scope assignment 还是其共同的授权语义，并与 Account Manipulation、Permission Groups Discovery/Modification、Valid Accounts、Access Token Manipulation、Event Triggered Execution 和 Defense Impairment 等相邻 owner 划清边界。

## 权限结果假设

TA0004 只有在攻击者控制的 policy/trust mutation 使某个主体或会话相对 pre-state 获得更大的有效授权集合，并完成首个此前被拒绝而修改后获准的操作时成立。域管理员、全局管理员、策略对象存在、GPO applied、trust established、组成员变化或高权限 token 字符串都不能替代 mutation → policy/trust version → evaluation/propagation → principal/session → positive authority delta → first newly authorized outcome。

域或租户范围扩大可能同时产生横向移动、Persistence 或 Defense Evasion；本批只把权限增量作为 TA0004 结果门。若攻击者修改前已经能完成同一结果，或策略只削弱防御/改变配置而未授予攻击主体新增权限，应保留相邻战术结论或排除 TA0004 结果。

## Taxonomy breadth 搜索

两项 ATT&CK 子技术数量较少，仍须开放搜索。至少检查以下候选匿迹轴，并逐项标记 formal、hypothesis、parent-core、adjacent、deferred 或 rejected：

- existing-policy or trust-object in-place semantic mutation；
- narrow target/scope or conditional applicability；
- staged propagation, replication or delayed token/session realization；
- direct versus transitive trust/authorization path；
- legitimate administrative workflow or approved-change provenance borrowing；
- deny/allow conflict, precedence or inheritance manipulation；
- central one-to-many fan-out；
- rollback, transient mutation or mutation-after-use；
- provider、cloud/on-prem platform、GPO/trust medium、policy field、group/role/target partitions。

每个 formal 轴必须有攻击者可控稳定键、清晰 sibling 边界、独立痕迹变化、观察/关联/归因影响、明确前提、结论级证据和有意义的检测/缓解差异。零子技术允许；平台、产品、介质、日志字段、目标类型与 ATT&CK 子技术名不得机械拆分。

## 证据、共享库与门禁

先查询 references、claims、cases、detections、analytics、mitigations、relationships。ATT&CK T1484 父页只锚定父行为、TA0004 映射与两个实现维度；策略/信任 stable key、传播、授权评估、实际权限 delta、首个结果、机理和防御必须由结论层级匹配的窄证据支持。七库对象逐一决议 reuse、extend、create、split 或 defer；DET/NJA 保持双向引用，MIT 每个 application 必须具有目标特定 use、expected_effect 与 limitations。

正式内容继续采用 YAML-only `schema_version: 2.0.0` 和逐段中英配对。每项 mechanism 必须形成行为设计→痕迹变化→防守观察影响→匿迹效果。完成后逐字段与 NJT-0001 比较，运行 `make quality`、构建 Bundle、检查 pipeline/reserved ID、运行 Review Web `npm test`，并实际渲染父技术、全部子技术及 DET/NJA/MIT 的中英文页面与跨对象引用。所有 lifecycle 保持 review；本批完成只推进到 7/13，不声明 TA0004 关闭。
