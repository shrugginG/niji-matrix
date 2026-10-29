# BATCH-TA0004-011 — T1055 Process Injection

## 固定基线、剩余范围与现状

唯一基线是 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1，不迁移版本。TA0004 十三个父候选顺序保持：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。前十项已经逐批通过；当前总体剩余范围为第 11–13 项。

| 批次 | 顺序 | ATT&CK 父候选 | 现有决策 | 现有 Niji 对象 | 当前状态 |
| --- | ---: | --- | --- | --- | --- |
| BATCH-TA0004-011 | 11 | T1055 Process Injection | TA0004 尚无独立决策 | 无以 T1055 为 origin 的正式 NJT | active；本批仅此一项 |
| BATCH-TA0004-012 | 12 | T1053 Scheduled Task/Job | DEC-TA0002-T1053 retain（Execution） | NJT-0075 与四个既有 NJS；TA0004 决策待定 | planned |
| BATCH-TA0004-013 | 13 | T1078 Valid Accounts | DEC-TA0001-T1078 retain（Initial Access） | NJT-0061 与两个既有 NJS；TA0004 决策待定 | planned |

T1055 在固定基线有十二项 ATT&CK 子技术，达到十项以上门槛，必须作为单候选批次。它未通过证据、逐项覆盖、第二轮 taxonomy、字段深度、防御对象、机器校验、Bundle 与双语 Web QA 前，不开始 T1053 正式 YAML 写入。预检确认当前 reserved ID 为零；相邻对象中的 T1055 提及只表达边界或共映射，不构成既有 T1055 正式对象。

## 固定 ATT&CK 19.1 子技术清单与实现维度

官方父页展示顺序冻结如下；这些名称仅作研究广度先验，不直接导入、翻译或改名为 Niji 子技术：

1. T1055.001 Dynamic-link Library Injection — 以目标进程加载/映射 DLL 并执行；
2. T1055.002 Portable Executable Injection — 把 PE image/sections 写入另一进程并执行；
3. T1055.003 Thread Execution Hijacking — 暂停并改写既有线程执行上下文；
4. T1055.004 Asynchronous Procedure Call — 将执行入口排入目标线程 APC；
5. T1055.005 Thread Local Storage — 利用 TLS callback/初始化路径转移执行；
6. T1055.008 Ptrace System Calls — 通过 ptrace 读取/改写进程状态并驱动执行；
7. T1055.009 Proc Memory — 通过 `/proc/[pid]/mem` 与 mappings 改写目标地址空间；
8. T1055.011 Extra Window Memory Injection — 借窗口对象额外内存和 callback 路径写入/触发；
9. T1055.012 Process Hollowing — 创建/暂停合法进程并替换其原始映像或入口；
10. T1055.013 Process Doppelgänging — 借事务化文件/section 与进程创建制造可见映像差异；
11. T1055.014 VDSO Hijacking — 改写 Linux 目标进程 vDSO 执行路径；
12. T1055.015 ListPlanting — 借 ListView callback/sort 等消息路径在目标进程触发执行。

必须对十二项逐项或逐簇记录 parent-core、niji-variable-candidate、adjacent-technique、evidence-deferred 或 not-stealth-distinct，并完成第二轮 taxonomy 搜索。最终若只有 0–1 个正式 Niji 子项，主 Agent 必须逐轴给出 breadth-gap explanation。

## 研究问题与准入门

- 父级直接对象是否应固定为 source process/control → target live process → cross-process state mutation or execution dispatch → malicious instructions executing in target context；仅 API 调用、写内存、句柄、远程线程对象或目标进程网络活动是否只能是中间证据；
- TA0004 成立是否必须进一步证明 target context 相对 source pre-state 的正权限差和首个新增授权结果，同时保留“用于 defense evasion 但没有提权”的非 TA0004 情况；
- 可控且持久的匿迹变量是否来自 payload representation/backing、execution-dispatch carrier、target lifecycle/image identity、writer/runner/provenance separation、入口时间与线程状态，而非 DLL/PE/Windows/Linux/API 名称；
- hollowing/doppelgänging 的 image identity mismatch、APC/TLS/thread hijack 的 execution-dispatch state、ptrace/proc memory 的写入介质，以及 window/ListPlanting 的 trusted UI message broker 是否形成独立、可证且有差异化防御的 Niji 轴，或收敛为更少的跨平台变量；
- 与 NJT-0077 当前进程 module instantiation、NJT-0072 IPC brokerage、NJT-0099 token carrier、NJT-0102 exploit transition、NJT-0101 boundary crossing、T1106 API resolution、T1574 loader selection 和后续 defense impairment 的 ownership 边界；
- 公开案例能否把攻击者选择、source→target、write/map、dispatch/start、target-context behavior 与 TA0004 authority result 连成结论链；证据只证明注入/规避而不证明权限差时，必须校准或仅支撑通用父行为。

每个正式 mechanism 必须写出行为设计 → 目标地址空间/线程/映像或来源痕迹变化 → 防守观察、关联、区分或归因影响 → 匿迹效果，并以结论级 evidence_refs 和校准置信度支撑。所有不足的候选轴保持 hypothesis/deferred/rejected，不以十二项 ATT&CK 子技术数量倒推 Niji 子项数量。

## 防御与验收约束

先查询 References、Claims、Cases、Detection Strategies、Detection Analytics、Mitigations、Relationships 七库，并对每库记录 reuse、extend、create、split 或 defer。DET 与 NJA 必须双向引用；MIT 每个 application 必须针对父或具体 Niji 子项给出独立 use、expected_effect、limitations。

非排除候选完成后，逐字段对照 NJT-0001，运行 `make quality`、构建 technique bundle、运行 `python3 scripts/pipeline_status.py`、确认 reserved ID 为零、在 `tool/niji-matrix-review` 运行 `npm test`，并用 live Review Web 检查父技术、全部子技术和防御对象的中英文页面及跨对象引用。所有 lifecycle 保持 `review`。
