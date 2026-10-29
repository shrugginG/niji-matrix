# BATCH-TA0004-008 研究与收敛约束

## 固定候选与总体进度

唯一基线是 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1，不迁移版本。TA0004 十三个父候选顺序保持：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。前七项已经逐批通过；当前总体剩余范围为第 8–13 项。

| 批次 | 顺序 | ATT&CK 父技术 | 现有决策与 Niji 对象 | 状态 |
|---|---:|---|---|---|
| BATCH-TA0004-008 | 8 | T1611 Escape to Host | 初始预检未发现 T1611 origin 的正式 DEC/NJT；只有 NJT-0089 将容器越界明确交给 T1611 | active |
| BATCH-TA0004-009 | 9 | T1546 Event Triggered Execution | TA0003 DEC-TA0003-T1546；NJT-0090 | planned |
| BATCH-TA0004-010 | 10 | T1068 Exploitation for Privilege Escalation | 待独立准入 | planned |
| BATCH-TA0004-011 | 11 | T1055 Process Injection | 待独立准入 | planned |
| BATCH-TA0004-012 | 12 | T1053 Scheduled Task/Job | TA0002 DEC-TA0002-T1053；NJT-0075 | planned |
| BATCH-TA0004-013 | 13 | T1078 Valid Accounts | TA0001 DEC-TA0001-T1078；NJT-0061 | planned |

T1611 单候选批次未通过证据、taxonomy、字段、防御对象、机器校验、Bundle 与双语 Web QA 前，不开始 T1546 正式 YAML 写入。候选必须独立得到 retain、adapt 或 exclude；不预设会建立 NJT 或 NJS。当前 reserved ID 为零。

## 当前候选 T1611

T1611 的固定英文名为 Escape to Host。固定基线预计没有 ATT&CK 子技术，研究开始后须以 Enterprise 19.1 来源复核；零子技术只表示没有内部实现清单，仍须执行开放式匿迹变量搜索，不能直接得出零个 Niji 子技术或按 container runtime、orchestrator、kernel、platform、escape vulnerability、socket、mount、namespace 与 host target 拆分。

本批初始预检未发现以 T1611 为 origin 的正式 decision 或 NJT。NJT-0089 已明确：容器服务定义本身归持久系统服务定义，只有越过容器边界取得宿主能力才属于 T1611。研究必须把 escape 的直接对象固定为 container isolation boundary crossing 及其 host-side authority result，并与 T1068 的漏洞利用事实、NJT-0098 的既有提权控制路径、T1543/T1569 的 host service creation/execution、Valid Accounts、Exposed Docker/Kubernetes control sockets、容器配置缺陷和单纯容器内 root 划清边界。

## 宿主权限结果假设

TA0004 只有在攻击者控制的 container-scoped 起点原本不能完成某项 host 操作，经明确 escape primitive 或 broker path 产生 host-side security context/capability，并完成首个此前拒绝、之后获准的 host resource 操作时成立。容器内 UID 0、privileged container 标签、host PID 可见、mount 存在、runtime process、shell 位于 host filesystem 或 CVE 命中都不能替代 container pre-state → boundary primitive → host context → positive authority delta → first host-only authorized outcome。

若攻击者在逃逸前已经能通过合法管理 API 完成同一 host 操作，或只在容器 namespace 内获得更高权限，则不能确认 T1611/TA0004 结果。漏洞 CVE 可作为前提或相邻 T1068 行为；本批必须分别记录 exploit evidence、boundary crossing、host-side identity/capability 与资源结果，不能用“发生漏洞利用”自动推导“已逃逸且提权”。

## Taxonomy breadth 搜索

即使固定 ATT&CK 子技术为零，仍至少检查以下候选匿迹轴，并逐项标记 formal、hypothesis、parent-core、adjacent、deferred 或 rejected：

- direct kernel/namespace boundary crossing versus delegated runtime or host-control-socket mediation；
- host-visible action attributed to container runtime, kubelet, daemon, system service or another trusted broker；
- preservation or borrowing of container/workload identity after host-side execution；
- host filesystem, device, credential, namespace, cgroup, capability or control-plane path as different escape primitives；
- transient host action followed by return to, cleanup from or termination of the container；
- escape across one boundary versus chained guest/container/sandbox/host boundaries；
- workload replacement, restart, reschedule or distributed-node selection separating initial exploit from host result；
- shared-kernel event attribution ambiguity and container telemetry loss at the boundary；
- runtime、orchestrator、cloud provider、operating system、CVE、image、mount/socket/device、host target 和日志字段分区。

formal 轴必须具有攻击者可控稳定键、持久 sibling 边界、独立痕迹变化、观察/关联/归因影响、明确前提、结论级证据和检测/缓解差异。零子技术允许；若证据只支持某个漏洞或工具实例，应保留 parent-core/adjacent/hypothesis，而不得把实现命名为 Niji 子项。

## 证据、共享库与门禁

先查询 references、claims、cases、detections、analytics、mitigations、relationships。ATT&CK T1611 父页只锚定父行为、TA0004 映射和官方案例索引；boundary primitive、实际 host context/capability、首个 host-only outcome、匿迹轴与防御必须由窄技术文档、研究论文或结论级事件证据支持。七库逐一决议 reuse、extend、create、split 或 defer；DET/NJA 双向引用，MIT application 对父/每个正式子项分别写 use、expected_effect 与 limitations。

正式内容继续采用 YAML-only `schema_version: 2.0.0` 和逐段中英配对。每项 mechanism 必须形成行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果；完成后逐字段对照 NJT-0001，运行 `make quality`、构建 Bundle、pipeline/reserved-ID 检查、Review Web `npm test`，并实际渲染父技术、全部子技术及 DET/NJA/MIT 中英文页面与跨对象引用。所有生命周期保持 review；本批完成只推进到 8/13，不声明 TA0004 关闭。
