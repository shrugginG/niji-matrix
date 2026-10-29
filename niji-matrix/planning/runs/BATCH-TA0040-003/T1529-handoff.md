# T1529 System Shutdown/Reboot / 系统关机或重启：TA0040 研究交接

工作项 `WORK-TA0040-T1529`；批次 `BATCH-TA0040-003`；临时键前缀 `TA0040-T1529-`。固定基线为 ATT&CK Enterprise 19.1。本文件只提交研究、双语草稿和共享库决议，不分配正式 ID，不修改正式矩阵、决策、共享库或计划。

## 1. 准入建议

**建议 `adapt`，父行为置信度 high，匿迹适配置信度 medium-high。** ATT&CK 19.1 明确把主机、VM 或网络设备的关机/重启以及由此造成的合法访问中断归入 Impact。Niji 应将直接对象固定为“完整系统生命周期真实进入 shutdown、power-off 或 reboot，并造成系统级访问中断”，同时要求至少一条受支持的观察变化因果链。关机命令或 API 调用未成功、只注销一个用户、只停止单个业务服务，以及重启仅用于装载另一技术而没有独立可用性影响时，不完成本技术。

**Recommendation: `adapt`, with high confidence in the parent behavior and medium-high confidence in the stealth adaptation.** ATT&CK 19.1 explicitly places shutdown or reboot of a host, VM, or network device and the resulting interruption of legitimate access under Impact. Niji should fix the direct object as an actual whole-system lifecycle transition into shutdown, power-off, or reboot that produces system-level access interruption and require at least one supported causal chain changing defender observation. An unsuccessful command or API request, logoff of one user, stopping one business service, or a reboot used only to load another technique without an independent availability effect does not complete this technique.

开放搜索支持两个 Niji 原生子项：

1. **延迟委托式生命周期转换 / Deferred-Delegated Lifecycle Transition**：攻击者先登记未来关机/重启，调度器随后以自身身份执行，使原始写入者与影响事件在时间、进程和审计对象上分离。
2. **目标外控制面生命周期转换 / Out-of-Target Control-Plane Lifecycle Transition**：攻击者从 hypervisor、vCenter、云或等效管理面改变目标 VM/设备电源状态，目标内部没有对应本地请求进程，关键因果留在外层控制面。

ATT&CK T1529 无子项；以上分类来自稳定匿迹变量、痕迹变化和防御差异，不存在导入关系。

## 2. 邻接边界收敛

| 相邻对象 | T1529 边界 |
|---|---|
| `NJT-0185` 业务服务停用 | NJT-0185 的直接对象是一个或多个业务服务通过服务管理路径进入 stopped/disabled，而主机仍可运行。T1529 要求主机、VM 或设备整体进入关机/重启生命周期。停止服务为关机做准备可以共同记录，但不能用单服务停止替代系统结果。 |
| `NJT-0096` 电源状态连续性控制 | NJT-0096 抑制睡眠、关机或重启，以让易失性立足点继续存在；T1529 主动造成关机或重启，以中断合法访问。一个是阻止生命周期边界，另一个是触发生命周期边界。 |
| `NJT-0172` 受限启动防御覆盖缺失 | NJT-0172 要求 boot intent 被消费、实际进入 restricted boot、防御组件缺席且攻击者利用窗口。若重启只用于进入 Safe Mode 并继续活动，直接匿迹对象是 NJT-0172；只有系统级访问中断本身是攻击者预期的 Impact 时才同时记录 T1529。 |
| T1499 / 端点拒绝服务 | 资源耗尽、漏洞或异常导致 OS/应用无响应或崩溃，且没有攻击者控制的系统生命周期请求时归 T1499。显式调用关机/重启控制，或以 `OptionShutdownSystem` 等机制有意把系统送入关机状态，仍可归 T1529。 |
| 普通补丁、维护和恢复 | 批准更新、驱动安装、灾备、HA、故障恢复、用户关机和基础设施维护是强反例；须核对 actor、approval、reason、target、窗口和业务结果。 |
| 仅作前置/消费条件的重启 | 重启只用于加载 bootkit、应用配置、Safe Mode、擦除结果或其他技术，而没有证据表明访问中断是独立目标或实质放大破坏时，T1529 保持 precursor context，不单独确认 Impact。若重启实际消费被破坏的启动/磁盘状态并使合法访问中断，可与对应技术共同记录。 |

## 3. Niji 原生轴覆盖

固定 ATT&CK 子项数为 `0`，`original_attack_subtechniques_imported: false`。零子项不免除开放搜索。

| 原生轴 | 可控变量与因果链 | 决议 |
|---|---|---|
| 延迟委托式生命周期转换 | 登记一次性任务/定时器 → task definition、writer 与未来触发时间先出现 → 调度器稍后以 SYSTEM/服务身份启动 shutdown，原进程可能已退出 → 只看临近关机窗口的分析无法恢复原始决定，需要跨窗口 task-to-boot 关联 | **formal**。Microsoft 对 Petya/NotPetya 的样本分析直接记录 10–60 分钟随机延迟、一次性 Task Scheduler 任务和 `shutdown.exe /r /f`；匿迹动机未被来源直接陈述，机理置信度 medium。 |
| 目标外控制面生命周期转换 | hypervisor/vCenter/云管理面或等效外层控制改变 VM/设备电源状态 → 目标 guest 无本地请求进程，guest telemetry 只见 heartbeat 消失或不干净启动 → 需把外层 actor/session/power event 与 guest availability 相连 | **formal**。CISA 的 Play ESXi 变体报告和 VMware/Broadcom 事件模型支持行为、残余字段与独立防御边界；机理置信度 high。 |
| 正常理由/维护语义伪装 | API 或命令填入 planned reason/comment，让关机记录更接近维护 → 理论上削弱状态事件区分力 | **defer**。Windows 明确允许 caller 指定 reason，但缺少结论级攻击案例证明对手实际使用虚假维护理由形成独立匿迹设计。 |
| 跨主机错峰或维护窗口对齐 | 分批/低速触发关机，使单窗异常量下降或混入批准窗口 | **defer**。存在技术可行性，缺少直接攻击证据和稳定阈值；不得从一般勒索批量操作推造子项。 |
| 强制崩溃、断电、优雅关机、重启、关机、平台或命令 | 改变转换类型或实现，但未必改变因果归属和防守观察 | **parent-core / adjacent**。有明确外层控制或委托变量时进入相应 child；否则不按结果类型、平台或工具分 NJS。 |

## 4. 父技术完整双语字段草稿

### name / summary

- zh：**系统关机或重启**。攻击者使主机、虚拟机或网络设备进入关机、断电或重启生命周期并中断合法访问，同时借正常生命周期终态、延迟委托或外层控制面分离原始发起者与影响结果。
- en: **System Shutdown/Reboot**. Adversaries move a host, virtual machine, or network device into shutdown, power-off, or reboot and interrupt legitimate access while separating the original initiator from the impact through ordinary lifecycle terminal states, delayed delegation, or an external control plane.

### definition_and_concept

zh：系统关机或重启是攻击者使完整主机、VM 或网络设备实际进入 shutdown、power-off 或 reboot 生命周期，使合法用户、业务和响应人员暂时或持续不能访问该系统的 Impact 行为。直接对象是系统生命周期与系统级可用性结果；`shutdown.exe`、`systemctl`、Windows API、network CLI、ESXi shell 和云 API 都只是实现。请求被拒绝、被取消或没有造成状态转换时，只能记录企图或暴露。

en: System Shutdown/Reboot is an Impact behavior in which an adversary causes a whole host, VM, or network device to enter a shutdown, power-off, or reboot lifecycle, preventing legitimate users, workloads, and responders from accessing that system temporarily or persistently. The direct object is the system lifecycle and system-level availability outcome. `shutdown.exe`, `systemctl`, Windows APIs, network CLI, ESXi shell, and cloud APIs are implementations. A rejected, cancelled, or ineffective request is only an attempt or exposure.

zh：Niji 的匿迹问题是原始控制意图如何与防守方首先看到的生命周期终态脱节。正常维护同样会产生 User32 1074、Kernel-General 关机/启动、调度器启动的 `shutdown.exe` 或 VM powered-off 状态；状态本身不编码恶意目的。攻击者可以利用正常控制路径让结果呈现维护终态、把执行委托给未来调度器，或从目标传感器之外的管理面直接改变电源状态。工具、平台、关机与重启的字面差别不是概念边界。

en: Niji’s stealth question is how the original controlling intent becomes detached from the lifecycle terminal state first seen by defenders. Legitimate maintenance produces the same User32 1074, Kernel-General shutdown or startup, scheduler-launched `shutdown.exe`, or VM powered-off state; the state itself does not encode malicious purpose. An adversary can use an accepted control path to produce a maintenance-like terminal state, delegate execution to a future scheduler, or change power state from a management plane outside target sensors. Tool, platform, and the literal distinction between shutdown and reboot do not define the concept.

### stealth_characteristics

zh：系统关机或重启通常会造成明显可用性变化，匿迹价值不在于隐藏系统离线，而在于削弱对发起者、授权上下文和前置行为的解释。优雅转换会关闭进程、刷新缓存并生成正常生命周期事件；只看 uptime、当前 power state 或“planned/unplanned”理由的防守方可能把恶意操作归因于补丁、管理员维护或自动恢复。理由字段由 caller 提供且管理员身份也可能被盗，不能作为授权证明。

en: System Shutdown/Reboot usually creates an obvious availability change. Its stealth value is not hiding that a system is offline but weakening interpretation of the initiator, authorization context, and preceding behavior. An orderly transition closes processes, flushes state, and produces ordinary lifecycle events. A defender observing only uptime, current power state, or a planned or unplanned reason can misattribute malicious activity to patching, administrator maintenance, or automatic recovery. Caller-supplied reason fields and administrator identity are not proof of authorization.

zh：延迟任务会把 task registration 与关机结果分到不同时间和进程身份，外层管理操作会让 guest 只有 heartbeat 终止、网络消失或不干净启动而没有本地请求者。残余痕迹包括原始控制进程、账户与会话、WMI correlation ID、Task Scheduler 定义和 next-run、shutdown reason/type/comment、boot ID、外部健康探针、vCenter/ESXi event key、chainId、userName、host、VM，以及 shell/API 会话。集中且不同权的长期保留会缩小匿迹效果。

en: A deferred task separates registration from the shutdown outcome across time and process identity, while an outer management action can leave a guest with only a heartbeat stop, network disappearance, or dirty boot and no local requester. Residual traces include the original controller process, account and session, WMI correlation identifiers, Task Scheduler definition and next run, shutdown reason, type, comment, boot identity, external health probes, vCenter or ESXi event key, chainId, userName, host, VM, and shell or API session. Centralized long-term retention under a different authority reduces the stealth effect.

### scope_boundary_definition

zh：纳入攻击者控制的系统级关机、断电、重置或重启请求，以及显式让系统进入关机生命周期的 fatal transition；要求目标是完整主机、VM 或网络设备，状态转换实际发生，且合法访问或响应能力受到实质中断。批量 VM power-off 仍按每个 VM 的系统生命周期和共同控制事务分析。命令、API 返回成功但系统未转换时不完成技术。

en: Include adversary-controlled system-level shutdown, power-off, reset, or reboot requests and fatal transitions explicitly intended to enter a shutdown lifecycle. The target must be a whole host, VM, or network device, the transition must occur, and legitimate access or response capability must be materially interrupted. A fleet VM power-off is analyzed as each VM lifecycle plus the shared control transaction. A successful command or API return without an actual transition does not complete the technique.

zh：单个业务服务停止归 NJT-0185；为保持易失入口而阻止关机/重启归 NJT-0096；进入受限启动且主要结果是防御缺席归 NJT-0172；资源耗尽或漏洞导致无受控生命周期请求的崩溃归 T1499。补丁、驱动/软件安装、灾备、HA、故障恢复、操作员排障、用户关机和授权云编排是正常反例。擦除、加密、恢复抑制或固件变化必须独立证明；重启只消费这些变化时不把伴随结果互作证据。

en: Stopping one business service belongs to NJT-0185; preventing shutdown or reboot to preserve a volatile foothold belongs to NJT-0096; restricted boot whose principal result is missing defense belongs to NJT-0172; and resource exhaustion or exploitation causing a crash without a controlled lifecycle request belongs to T1499. Patching, driver or software installation, disaster recovery, HA, fault recovery, operator troubleshooting, user shutdown, and authorized cloud orchestration are normal counterexamples. Wiping, encryption, recovery inhibition, or firmware change requires independent proof. When reboot merely consumes those changes, accompanying outcomes cannot serve as evidence for one another.

### application_scenarios_and_threat_model

**application_scenarios**

zh：破坏型恶意软件可在修改磁盘或数据后安排未来重启，使受害者在重启时进入不可用状态；NotPetya/Petya 样本使用一次性计划任务，在感染后 10–60 分钟以 `shutdown.exe /r /f` 重启。勒索软件也可在 ESXi host 上枚举并关闭全部运行 VM，以中断业务并释放虚拟磁盘供后继加密；该 VM 停电与虚拟磁盘加密须分别确认。直接本地或远程关机同样可以单独用于中断用户访问或阻碍响应。

en: Destructive malware can schedule a future reboot after modifying disk or data so the victim enters an unavailable state on restart. NotPetya or Petya samples used a one-time scheduled task to run `shutdown.exe /r /f` ten to sixty minutes after infection. Ransomware can also enumerate and power off every running VM from an ESXi host, interrupting business and releasing virtual disks for later encryption; VM power loss and virtual-disk encryption require separate confirmation. A direct local or remote shutdown can likewise be used on its own to interrupt user access or impede response.

**attacker_model**

zh：攻击者需要对目标系统拥有本地或远程 shutdown/reboot 权限，或控制承载目标 VM/设备的外层管理面。延迟委托还要求创建/修改具相应 runtime identity 的调度对象并预测时钟和任务运行条件；外层转换要求识别正确 VM、host 和业务依赖。HA 自动恢复、关机取消、应用阻止、错误目标、管理网分段、JIT/MFA、最小 power-operation RBAC、不同权审批和带外告警会限制效果。大规模关机会迅速暴露行动并可能阻断攻击者自己的 C2。

en: The adversary needs local or remote shutdown or reboot authority on the target or control of the outer management plane hosting the target VM or device. Deferred delegation also requires creating or changing a scheduled object with a suitable runtime identity and predicting clock and task conditions. An outer-plane transition requires correct mapping of VM, host, and business dependency. HA restart, shutdown cancellation, blocking applications, wrong targets, segmented management networks, JIT and MFA, least power-operation RBAC, differently authorized approval, and out-of-band alerts constrain the effect. Fleet shutdown rapidly exposes the operation and can sever the adversary’s own C2.

**defender_model**

zh：防守方维护主机/VM/设备 inventory、业务 owner、正常维护与重启节奏，并关联端点进程和 4688/Sysmon、User32 1074、Kernel-General 12/13、Kernel-Power 41、EventLog 6008、WMI operation trace、Task Scheduler definition/runtime、外部健康/heartbeat、vCenter/ESXi event 与会话、批准单和恢复结果。只有本地 agent 时，关机恰好终止观察；只有 hypervisor state 时又缺少来宾原因。因此需要不同权集中保留和 target ID 映射。

en: Defenders maintain host, VM, and device inventory, business owners, and normal maintenance and reboot cadence, and correlate endpoint process and 4688 or Sysmon telemetry, User32 1074, Kernel-General 12 or 13, Kernel-Power 41, EventLog 6008, WMI operation traces, Task Scheduler definitions and runtime, external health or heartbeat, vCenter or ESXi events and sessions, approvals, and recovery outcomes. A local-only agent stops observing precisely when shutdown occurs, while hypervisor state alone lacks the guest cause. Differently authorized centralized retention and target-ID mapping are therefore required.

### stealth_mechanisms

**`NM-FD` primary — 正常生命周期终态掩盖恶意系统中断 / Ordinary lifecycle terminal states disguise malicious system interruption**

zh：攻击者使用系统接受的关机/重启路径，使 OS 或管理面按正常状态机停止进程并报告 familiar terminal state。痕迹从异常故障转为补丁和维护也会生成的 requester、reason、shutdown、boot 序列；只消费状态和理由的守方难以判定恶意，形成特征伪装。调用者、权限前态、审批、业务健康和后继破坏仍能揭示矛盾。证据键 `REF-000870`、`TA0040-T1529-REF-MS-REBOOT-EVENTS`、`TA0040-T1529-REF-MS-EXITWINDOWSEX`；confidence medium。

en: The adversary uses a shutdown or reboot path accepted by the system, causing the OS or management plane to stop processes through its normal state machine and report a familiar terminal state. Traces shift from abnormal failure to a requester, reason, shutdown, and boot sequence also produced by patching and maintenance. A state-and-reason-only defender has difficulty classifying maliciousness, producing Feature Disguise. Caller, authority pre-state, approval, business health, and successor destruction expose contradictions. Evidence keys are `REF-000870`, `TA0040-T1529-REF-MS-REBOOT-EVENTS`, and `TA0040-T1529-REF-MS-EXITWINDOWSEX`; confidence medium.

**`NM-ST` secondary — 延迟委托分散注册与关机结果 / Deferred delegation disperses registration and shutdown outcome**

zh：攻击者先登记未来任务，调度器在数十分钟或更久后启动关机；writer、task definition、scheduler child 和 boot result 被分散在不同时间窗口。临近关机才开始的调查只看到 SYSTEM/Task Scheduler 和生命周期结果，原始恶意进程可能已经退出；按稳定 task ID、definition digest、scheduled time 和 boot 连接可恢复。证据 `REF-000601`；confidence medium。

en: The adversary registers a future task and the scheduler launches shutdown tens of minutes or longer afterward, dispersing the writer, task definition, scheduler child, and boot result across observation windows. An investigation beginning near shutdown sees only SYSTEM or Task Scheduler and the lifecycle outcome, and the original malicious process may have exited. Stable task ID, definition digest, scheduled time, and boot correlation recover the chain. Evidence is `REF-000601`; confidence medium.

**`NM-BT` secondary — 外层电源控制越出目标传感器观察域 / Outer-plane power control falls outside target-sensor scope**

zh：攻击者在 ESXi/vCenter/云或等效管理层对 VM 发出 power-off/reset，关键请求和主体留在外层事件与 shell/API session，guest endpoint 没有本地 shutdown caller，甚至来不及完成干净关机。以 guest agent 为边界的守方只看到 heartbeat 消失或后续 dirty boot；把管理事件、VM ID、host、session 和 guest availability 联接可恢复原因。证据 `TA0040-T1529-REF-CISA-PLAY`、`TA0040-T1529-REF-VSPHERE-EVENT`；confidence high。

en: The adversary issues VM power-off or reset from ESXi, vCenter, cloud, or an equivalent management layer. The critical request and principal remain in outer-plane events and shell or API sessions; the guest endpoint has no local shutdown caller and may not complete a clean shutdown. A defender bounded by the guest agent sees only heartbeat loss or a later dirty boot. Joining management event, VM ID, host, session, and guest availability restores causality. Evidence is `TA0040-T1529-REF-CISA-PLAY` and `TA0040-T1529-REF-VSPHERE-EVENT`; confidence high.

### subtechnique_taxonomy

zh：延迟委托式生命周期转换按“原决策写入者与实际生命周期执行在时间/进程上的分离”划界；目标外控制面生命周期转换按“电源控制发生在目标 OS/设备传感器之外”划界。前者需要 task definition—trigger—shutdown—boot 的跨窗口关联，后者需要 management event—target VM/device—guest availability 的跨平面关联，数据与缓解施加点不可互换。两者可以共现，例如外层编排器安排未来 VM power-off，届时可同时映射。

en: Deferred-Delegated Lifecycle Transition is bounded by separation of the original decision writer from lifecycle execution across time and process. Out-of-Target Control-Plane Lifecycle Transition is bounded by power control occurring outside target OS or device sensors. The first requires cross-window task-definition to trigger to shutdown to boot correlation, while the second requires cross-plane management-event to target VM or device to guest-availability correlation. Their data and mitigation points are not interchangeable. They can co-occur when an outer orchestrator schedules a future VM power-off, in which case both may map.

zh：即时本地 shutdown/API、故意 fatal shutdown 和普通远程系统调用由父级表达。关机/重启、优雅/强制、OS/VM/网络设备、命令/API 和目标数量不是子项；虚假 reason 与错峰批量操作保持 deferred。ATT&CK 无子项，本分类完全来自 Niji 稳定变量。

en: Immediate local shutdown or API use, deliberate fatal shutdown, and ordinary remote system calls remain parent behavior. Shutdown versus reboot, graceful versus forced, OS versus VM versus network device, command versus API, and target count do not define children. False reason codes and staggered fleet operations remain deferred. ATT&CK has no children, and this taxonomy is entirely derived from Niji stable variables.

### defense / evidence / limitations

- detection: create `TA0040-T1529-DET-LIFECYCLE-AUTHORITY-OUTCOME` with the three analytics in section 7.
- mitigation: create `TA0040-T1529-MIT-LIFECYCLE-AUTHORITY-RESILIENCE`; extend `MIT-000088` only with a child-specific application for deferred scheduling.
- claim keys: `TA0040-T1529-CLM-PARENT`, `TA0040-T1529-CLM-ORDERLY-STATE`, `TA0040-T1529-CLM-DEFERRED`, `TA0040-T1529-CLM-OUTER-PLANE`, `TA0040-T1529-CLM-BOUNDARIES`, `TA0040-T1529-CLM-DEFENSE`.
- case keys: `TA0040-T1529-CASE-NOTPETYA-DEFERRED-REBOOT`, `TA0040-T1529-CASE-PLAY-ESXI-POWER-OFF`.

zh：父行为有大量案例，但多数报告把重启解释为完成擦除、加密或载荷切换，不直接陈述匿迹动机。因此 Impact 行为 high，正常终态和延迟委托的匿迹机理 medium；外层控制面观察差异由事件模型直接支持，但 CISA Play 案例的主要动机仍是释放 VM 文件并加密。Windows 字段不能无条件移植到 Linux、macOS 或网络设备；缺少 caller/approval/outcome 时只能报告 unexplained transition。

en: The parent behavior has many cases, but most reporting explains reboot as completing wiping, encryption, or payload switching rather than explicitly stating a stealth motive. Impact behavior is high confidence, while ordinary-terminal-state and deferred-delegation stealth are medium confidence. The outer-plane observation difference is directly supported by event models, although the principal motive in the CISA Play case remains releasing VM files for encryption. Windows fields cannot be projected unchanged onto Linux, macOS, or network devices. Without caller, approval, and outcome, report only an unexplained transition.

## 5. 子技术双语字段草稿

### 5.1 延迟委托式生命周期转换 / Deferred-Delegated Lifecycle Transition

**summary**

- zh：攻击者预先登记未来关机或重启，让调度器稍后以受信运行身份完成系统转换，从而把原始 writer 与可用性影响分散到不同观察窗口。
- en: The adversary registers a future shutdown or reboot and lets a scheduler complete the transition later under a trusted runtime identity, dispersing the original writer and availability impact across observation windows.

**definition_and_concept**

zh：延迟委托式生命周期转换是攻击者创建或修改一次性任务、timer 或等价调度对象，使其在未来时间调用系统关机/重启控制并实际造成系统级访问中断。稳定变量是原始关机决定由持久调度定义保存、实际执行由另一 scheduler/runtime identity 稍后完成，而不是任务名称、延迟长度或操作系统。

en: Deferred-Delegated Lifecycle Transition occurs when an adversary creates or changes a one-time task, timer, or equivalent scheduler object that invokes system shutdown or reboot in the future and actually causes system-level access interruption. The stable variable is preservation of the original shutdown decision in a durable scheduled definition followed by later execution under another scheduler or runtime identity, rather than task name, delay length, or operating system.

zh：本子项要求 task registration、实际 trigger、shutdown process/API、完成的 lifecycle transition 和 availability result 能够闭合。一般恶意计划执行归调度技术；只有其具体结果是 T1529 的系统生命周期影响时才进入本子项。重启后加载另一载荷但没有独立访问中断时只保留 adjacent/precondition。

en: The child requires closure across task registration, actual trigger, shutdown process or API, completed lifecycle transition, and availability outcome. Generic malicious scheduled execution belongs to scheduling techniques. This child applies only when its concrete result is the T1529 system-lifecycle impact. A reboot that merely loads another payload without an independent access interruption remains adjacent or a precondition.

**stealth_characteristics**

zh：**延迟委托式生命周期转换**把恶意 writer 留在较早的 task registration 事件中，关机时点只出现 scheduler、SYSTEM 或服务账户启动的标准 lifecycle utility。若创建与执行相隔 10–60 分钟或更久，默认短窗口调查可能只保留一端；原 dropper 退出、任务自删或日志轮转进一步削弱归因。Task Scheduler Event 106/Security 4698、完整 task XML、creator、action、trigger、run-as、runtime instance、shutdown Event 1074 和 boot 事件仍可连接。

en: **Deferred-Delegated Lifecycle Transition** leaves the malicious writer in an earlier task-registration event, while shutdown time shows only a scheduler, SYSTEM, or service account launching a standard lifecycle utility. When creation and execution are separated by ten to sixty minutes or longer, a default short-window investigation may retain only one end. Dropper exit, task deletion, or log rotation further weakens attribution. Task Scheduler Event 106 or Security 4698, complete task XML, creator, action, trigger, run-as identity, runtime instance, shutdown Event 1074, and boot events remain joinable.

**scope_boundary_definition**

zh：纳入攻击者控制的未来 trigger 与实际系统关机/重启结果。即时调用、只在启动/登录时运行一般载荷、任务创建但未触发、shutdown 被取消或只注销用户不纳入。本子项可与 NJS-0075-002 的延期计划激活共同出现，但这里的判定还必须有完整系统生命周期和访问中断；调度对象本身不能替代 Impact 结果。

en: Include an adversary-controlled future trigger and an actual system shutdown or reboot outcome. Immediate invocation, general payload execution at boot or logon, an untriggered task, an aborted shutdown, or user logoff is excluded. The child can co-occur with NJS-0075-002 deferred scheduled activation, but this classification additionally requires the whole-system lifecycle and access interruption. The scheduler object does not substitute for the Impact result.

zh：Windows Update、安装器、补丁编排、硬件维护、合规重启和批准管理员任务是主要反例；离线设备补跑、时区/DST 变化和任务错过后重放也会改变实际时间。必须用完整定义、软件/变更 owner、approval 和结果排除，不能永久白名单 SYSTEM 或 taskhost。

en: Windows Update, installers, patch orchestration, hardware maintenance, compliance reboot, and approved administrator tasks are principal counterexamples. Offline catch-up, time-zone or daylight-saving changes, and replay after a missed trigger also change actual time. Exclusion requires complete definition, software or change owner, approval, and outcome rather than permanently allowing SYSTEM or taskhost.

**application_scenarios_and_threat_model**

zh：NotPetya/Petya 在感染后创建一次性 Scheduled Reboot Task，随机安排 10–60 分钟后由 `shutdown.exe /r /f` 重启。该延迟让擦除、传播和其他动作在重启前继续，也把任务创建与最终生命周期事件分开。案例证明变量存在和字段可检测性，但不证明延迟的主观目的就是匿迹。

en: NotPetya or Petya created a one-time Scheduled Reboot Task after infection and scheduled `shutdown.exe /r /f` for a random time ten to sixty minutes later. The delay allowed wiping, propagation, and other activity to continue before reboot and separated task creation from the final lifecycle event. The case proves the variable and detectable fields but not that stealth was the actor’s stated subjective purpose.

zh：攻击者需要创建/修改调度对象的权限、能在运行身份下执行 shutdown 的权利、可预测的系统时钟和足够驻留时间。任务被提前枚举、future-trigger 队列阻断、shutdown 被用户/系统取消、host 离线、任务凭据失效或应用阻止关机会使链失败。防守方应在登记时保存 immutable definition/creator/next-run，并让 watchlist 跨越执行和重启；只在关机时采集进程或只周期盘点当前任务会漏掉链的一端。

en: The adversary needs authority to create or modify a scheduler object, shutdown rights under the runtime identity, a predictable system clock, and sufficient residence time. Early task enumeration, future-trigger blocking, user or system cancellation, an offline host, expired task credentials, or an application preventing shutdown can break the chain. Defenders should preserve immutable definition, creator, and next-run at registration and carry a watchlist through execution and reboot. Process collection only at shutdown or periodic current-task inventory misses one end.

**mechanism / defense / limitations**

- mechanism: `NM-ST` primary; summary zh：跨时间与进程身份分散关机决定和结果；en: Disperse shutdown decision and outcome across time and process identity; evidence `REF-000601`; confidence medium.
- detection: `TA0040-T1529-NJA-DEFERRED-TASK-TO-BOOT` under new DET.
- mitigations: extend `MIT-000088` with this child application; also apply new lifecycle-authority MIT.

zh：Microsoft 样本分析直接给出 task command、随机 10–60 分钟和 Event 106 调查提示，但只覆盖一个 Windows 家族；不能据此设定通用恶意延迟阈值，也不能把所有一次性 reboot task 判恶。任务删除、时钟变化和日志禁用会破坏因果，未证明实际关机/访问中断时只能确认恶意调度候选。

en: Microsoft’s sample analysis directly supplies the task command, random ten-to-sixty-minute delay, and Event 106 investigation lead, but it covers one Windows family. It cannot define a universal malicious delay threshold or make every one-time reboot task malicious. Task deletion, clock changes, and disabled logging break causality. Without proof of actual shutdown and access interruption, only a malicious scheduling candidate is established.

### 5.2 目标外控制面生命周期转换 / Out-of-Target Control-Plane Lifecycle Transition

**summary**

- zh：攻击者从 hypervisor、云或等效外层管理面改变目标 VM/设备的电源状态，使目标内部没有原始请求进程并失去本地观察。
- en: The adversary changes a target VM or device power state from a hypervisor, cloud, or equivalent outer management plane, leaving no original requester process inside the target and terminating local observation.

**definition_and_concept**

zh：目标外控制面生命周期转换是攻击者在目标操作系统或设备之外的管理层调用 power-off、reset、reboot 或 guest shutdown，使目标实际离线或重启并中断合法访问。稳定变量是“决定与执行所在控制面不属于目标本地传感器观察域”；hypervisor、云品牌、BMC 产品和 VM 类型只是实现。

en: Out-of-Target Control-Plane Lifecycle Transition occurs when an adversary invokes power-off, reset, reboot, or guest shutdown from a management layer outside the target operating system or device, causing the target to go offline or restart and interrupting legitimate access. The stable variable is that the decision and execution control plane lies outside the target’s local sensor scope. Hypervisor, cloud brand, BMC product, and VM type are implementations.

zh：直接在目标内运行 `shutdown.exe`、`systemctl` 或设备 CLI 属父级核心，即使命令由远程 shell 发出；由 guest tools 接受外层请求时，若能证明原始 management request 与目标转换分离，仍可纳入本子项。单纯关闭一项 guest 服务、删除 VM、暂停而没有 T1529 生命周期语义，或只修改自动启动策略需分别评价。

en: Running `shutdown.exe`, `systemctl`, or device CLI inside the target remains parent core even when entered through a remote shell. A guest-tools request can qualify when the original management request is demonstrably separate from the target transition. Stopping one guest service, deleting a VM, suspending it without T1529 lifecycle semantics, or merely changing autostart policy requires separate assessment.

**stealth_characteristics**

zh：**目标外控制面生命周期转换**使 guest endpoint 看不到发起 power operation 的账户、来源 IP、API 或 shell session；强制 power-off 还可能没有 User32 1074 或本地干净 shutdown 序列。guest EDR、日志代理和业务进程与目标一起停止，事件调查只剩 heartbeat loss、网络断开和下次启动的 Event 41/6008。外层 vSphere Event 的 key、chainId、createdTime、userName、host、vm、fullFormattedMessage，以及 session IP/userAgent/ID 和 shell command 保留可归因证据。

en: **Out-of-Target Control-Plane Lifecycle Transition** prevents the guest endpoint from seeing the account, source IP, API, or shell session that initiated the power operation. A forced power-off may also omit User32 1074 and the local clean-shutdown sequence. Guest EDR, logging agents, and business processes stop with the target, leaving only heartbeat loss, network disappearance, and Event 41 or 6008 on the next boot. Outer vSphere Event fields such as key, chainId, createdTime, userName, host, vm, and fullFormattedMessage, together with session IP, user agent, session ID, and shell command, retain attribution evidence.

**scope_boundary_definition**

zh：纳入外层管理面到特定 target ID 的 power transition 以及目标系统级可用性结果；要求连接 actor/session、action、target VM/device、power state 与 guest/business health。只看到 guest heartbeat 消失不能证明外层控制，只有 vCenter/ESXi event 而目标状态未变也只是企图。Play ransomware 在 ESXi 上枚举并关闭全部运行 VM 是结论级实例。

en: Include an outer-management-plane power transition to a specific target ID and the target’s system-level availability outcome. Classification requires actor or session, action, target VM or device, power state, and guest or business health. Guest heartbeat loss alone does not prove outer control, and a vCenter or ESXi event without target state change is only an attempt. Play ransomware enumerating and powering off all running VMs from ESXi is a conclusion-level instance.

zh：HA isolation response、DRS/维护、管理员迁移、云 autoscaling、成本关机、灾备和数据中心故障是强反例。NJS-0111-004 观察域封装描述攻击活动在 guest 内运行而宿主看不到内部工件；本子项方向相反，攻击者在外层控制 guest 生命周期而 guest 看不到外层决定。二者不得因都涉及虚拟化而合并。

en: HA isolation response, DRS or maintenance, administrator migration, cloud autoscaling, cost shutdown, disaster recovery, and datacenter failure are strong counterexamples. NJS-0111-004 Observation-Domain Encapsulation covers adversary activity running inside a guest whose internal artifacts are invisible to the host. This child is the reverse direction: the adversary controls guest lifecycle from the outer layer while the guest cannot see the outer decision. They must not be merged merely because both involve virtualization.

**application_scenarios_and_threat_model**

zh：CISA 报告的 Play ESXi 变体在未给参数时关闭全部 VM，然后加密 `.vmdk`、`.vmem`、`.vmx` 等虚拟机文件；VM 访问中断发生在 hypervisor power control，后继文件加密是另一 Impact 结果。攻击者也可使用被盗 vCenter/cloud/BMC 身份对关键 VM 发出 reset 或 power-off，但只有存在相应实际证据时才能从能力推广到案例。

en: The Play ESXi variant reported by CISA powers off all VMs when run without arguments and then encrypts virtual-machine files such as `.vmdk`, `.vmem`, and `.vmx`. VM access interruption occurs through hypervisor power control, while later file encryption is a separate Impact result. An adversary can also use stolen vCenter, cloud, or BMC identity to reset or power off critical VMs, but capability should become a case only with corresponding observed evidence.

zh：攻击者需要 hypervisor/cloud/BMC 或等效管理权限、target inventory 知识和对 HA/自动恢复的理解；fleet power-off 可能要求 root 或批量 API。管理网隔离、MFA/PAM/JIT、host lockdown、按 VM 限权、不可篡改远程事件、HA rate limit 与双人批准会限制效果。防守方需把 management target ID 与 CMDB/guest ID 对齐，从控制面和 guest 外部健康探针独立保存数据；若日志只留在已陷 ESXi host，攻击者可同时清除原因。

en: The adversary needs hypervisor, cloud, BMC, or equivalent management authority, target-inventory knowledge, and understanding of HA or automatic restart. Fleet power-off may require root or bulk API authority. Segmented management networks, MFA, PAM, JIT, host lockdown, per-VM authorization, tamper-resistant remote events, HA rate limits, and dual approval constrain the effect. Defenders need management target IDs mapped to CMDB and guest IDs and independently retained control-plane and external guest-health data. If logs remain only on a compromised ESXi host, the actor can erase the cause together with the result.

**mechanism / defense / limitations**

- mechanism: `NM-BT` primary; summary zh：外层电源操作越出目标端点观察边界；en: Outer-plane power operations cross the target endpoint’s observation boundary; evidence `TA0040-T1529-REF-CISA-PLAY`, `TA0040-T1529-REF-VSPHERE-EVENT`; confidence high.
- detection: `TA0040-T1529-NJA-MANAGEMENT-PLANE-POWER-OUTCOME`.
- mitigation: new lifecycle-authority MIT with dedicated child application; do not reuse GuestOps execution mitigation by title similarity.

zh：CISA 和 VMware 资料直接证明 ESXi ransomware 关闭 VM 及 vSphere power event 字段，但没有量化 guest EDR 漏检率；“guest-only 分析失去发起者”是由控制面边界和日志结构支持的因果推断。强制 power-off、graceful guest shutdown、reset 和 HA failover 的 guest 痕迹不同，部署必须保留具体 operation；缺少外层 session 或 CMDB 映射时不能宣称攻击主体。

en: CISA and VMware materials directly establish ESXi ransomware VM power-off and vSphere power-event fields but do not quantify guest EDR miss rates. The conclusion that guest-only analysis loses the initiator is a causal inference supported by the control-plane boundary and logging structure. Forced power-off, graceful guest shutdown, reset, and HA failover produce different guest traces and must retain the exact operation. Without the outer session or CMDB mapping, the adversary principal cannot be claimed.

## 6. 结论级来源与共享对象候选

### 复用/扩展现有 Reference

- `REF-000870`，**reuse unchanged**：固定 ATT&CK 19.1 T1529，支持整机/VM/设备生命周期边界、Impact 和无 ATT&CK 子项。
- `REF-000601`，**reuse + extend locator/notes**：同一 Microsoft Petya 样本来源。现有对象用于传播研究，但原文还直接给出 Scheduled Reboot Task、随机 10–60 分钟、`schtasks /Create ... shutdown.exe /r /f` 和 Event 106 调查提示；Reference 身份相同，不得新建重复 REF。
- `REF-000294`，**reuse unchanged**：Microsoft WMI shutdown tracing，提供 CorrelationId、OperationId、ClientMachine、User、ClientProcessId 等从 Wmiprvse 结果回溯请求者的字段。

### 新 Reference 候选

| 临时键 | 来源 | 支持结论 |
|---|---|---|
| `TA0040-T1529-REF-MS-REBOOT-EVENTS` | Microsoft Learn, Troubleshoot unexpected reboots using system event logs, `https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-unexpected-reboots-system-event-logs` | Event 1074 requester/process/user/reason/type/comment；12/13/41/6008/6009 区分 clean 与 unexpected lifecycle。 |
| `TA0040-T1529-REF-MS-EXITWINDOWSEX` | Microsoft Learn, ExitWindowsEx, `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-exitwindowsex` | accepted shutdown state machine、force flags、reason、异步结果和 `SE_SHUTDOWN_NAME`。 |
| `TA0040-T1529-REF-MS-SHUTDOWN-RIGHTS` | Microsoft Learn, UserRights Policy CSP / Shut down the system | local/remote shutdown privilege and denial-of-service risk；支持最小权限措施。 |
| `TA0040-T1529-REF-MS-SHUTDOWN-CMD` | Microsoft Learn, shutdown, `https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/shutdown` | local/remote target、timeout、reason/comment、abort 与正常维护反例。 |
| `TA0040-T1529-REF-CISA-PLAY` | CISA AA23-352A #StopRansomware: Play Ransomware, `https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-352a` | ESXi variant 使用 `vim-cmd vmsvc/power.off` 关闭全部 VM 并加密 VM 文件。 |
| `TA0040-T1529-REF-VMWARE-ESXI-RANSOMWARE` | VMware Security, ESXi-Targeting Ransomware: Tactics and Techniques Part 2, `https://blogs.vmware.com/security/2022/10/esxi-targeting-ransomware-tactics-and-techniques-part-2.html` | 多个家族在加密前用 ESXi/vim-cmd power operations 关闭 VM；支持场景广度，不替代 CISA case。 |
| `TA0040-T1529-REF-VSPHERE-EVENT` | Broadcom vSphere Web Services API Event / VmPoweredOffEvent, `https://developer.broadcom.com/xapis/vsphere-web-services-api/latest/vim.event.Event.html` | event `key`, `chainId`, `createdTime`, `userName`, `host`, `vm`, `fullFormattedMessage`, `auditId`；VmPoweredOffEvent records completed power-off。 |

### Claim candidates

- `TA0040-T1529-CLM-PARENT`：攻击者完成主机、VM 或设备关机/重启并中断合法访问，构成 T1529；`REF-000870`。
- `TA0040-T1529-CLM-ORDERLY-STATE`：accepted shutdown/reboot 产生正常维护也会出现的 requester/reason/lifecycle terminal state，必须把 caller、authority、approval 与 availability outcome 连接；Microsoft lifecycle docs。
- `TA0040-T1529-CLM-DEFERRED`：Petya 的一次性 task 把 registration 与 10–60 分钟后的 reboot 分开，并提供可长期关联的定义和 Event 106；`REF-000601`。
- `TA0040-T1529-CLM-OUTER-PLANE`：ESXi power-off 可让 guest 离线而原始 actor/action 留在 hypervisor plane；CISA + vSphere Event docs。
- `TA0040-T1529-CLM-BOUNDARIES`：单服务停止、阻止生命周期、restricted boot、无控制请求的 endpoint crash 与 precursor-only reboot 分属相邻对象。
- `TA0040-T1529-CLM-DEFENSE`：local caller-to-lifecycle、task-to-boot 和 management-plane-to-guest outcome 是三种不可互换的分析路径；字段有来源支持，窗口是部署初值。

### Case candidates

- `TA0040-T1529-CASE-NOTPETYA-DEFERRED-REBOOT`：Microsoft 2017 样本分析；Petya 创建一次性 Scheduled Reboot Task，在当前时间后随机 10–60 分钟运行 `shutdown.exe /r /f`。只支持延期委托子项和 Windows 字段；传播/漏洞路径仍由既有 `CASE-000208` 负责。
- `TA0040-T1529-CASE-PLAY-ESXI-POWER-OFF`：CISA Play advisory；ESXi variant 枚举并 power off 所有运行 VM，随后加密 VM 文件。case 同时说明 VM availability 与文件加密须分开建模；支持外层控制 child。

## 7. 可实施 Detection Strategy 与 Analytics

### `TA0040-T1529-DET-LIFECYCLE-AUTHORITY-OUTCOME` — 生命周期控制权威至可用性结果谱系 / Lifecycle Authority to Availability-Outcome Lineage

**objective:** 不因一个 reboot/poweredOff 状态或命令命中单独定性；分别恢复本地 requester、延期 task writer 或外层 management actor，并证明 target 完成系统生命周期转换、实际访问中断且缺少匹配 approval。覆盖 parent 和两个 child，domains `[enterprise]`。

#### `TA0040-T1529-NJA-LOCAL-REQUEST-TO-LIFECYCLE`

**name:** 本地关机请求—生命周期—可用性关联 / Local Shutdown Request–Lifecycle–Availability Correlation。

**platforms:** `[Windows]`。

**logic:** 规范化进程创建、WMI operation 与 Windows User32 1074，保存 requester process、user/SID、logon/session、client machine、reason code/comment、shutdown type 和 remote target。将 accepted request 在十五分钟内连接 Kernel-General 13 或 clean shutdown，在后续三十分钟内连接 Kernel-General 12/6009 的新 boot；若出现 41/6008 则标记 dirty transition，不假定本地 requester。并行连接独立 health/heartbeat 的首次 unavailable/recovered 与 maintenance approval。只有未经批准 requester、实际 transition 和 system-level health loss 共同成立才输出 `impact_shutdown_confirmed`；命令/API 成功而 state 未变为 attempt。

**data requirements:**

- `endpoint-process`: channel `Security 4688, Sysmon Event 1, or EDR`; fields `event_time`, `asset_id`, `process_start_key`, `image`, `command_line`, `parent_process_start_key`, `account_sid`, `logon_id`, `source_host_or_ip`。
- `windows-shutdown-lifecycle`: channel `System User32/Kernel-General/Kernel-Power/EventLog`; fields `event_time`, `asset_id`, `event_id`, `requester_process`, `requester_user`, `reason_code`, `reason_comment`, `shutdown_type`, `boot_id_or_boot_time`, `clean_shutdown`, `result`。
- `wmi-operation-trace`: channel `Microsoft-Windows-WMI-Activity/Trace`; fields `event_time`, `correlation_id`, `group_operation_id`, `operation_id`, `namespace`, `method`, `client_machine`, `user`, `client_process_id`。
- `external-availability-and-approval`: fields `event_time`, `asset_id`, `probe_id`, `health_result`, `last_seen`, `first_unavailable`, `first_recovered`, `owner`, `approval_id`, `maintenance_window`, `expected_transition`。

**observables:** unapproved caller followed by 1074 and clean shutdown; Wmiprvse request traced to an unexpected client/process; no local clean request but dirty power transition and independent outage; transition reason/actor disagrees with approval.

**correlation:** request to lifecycle 15 minutes; shutdown through new boot 30 minutes; availability and recovery retained 24 hours. Dimensions `asset_id`, `process_start_key`, `account_sid`, `logon_id`, `correlation_id`, `shutdown_type`, `boot_id`, `approval_id`, `time`.

**false positives:** patch/update, driver/software install, approved administrator reboot, user shutdown, UPS/power fault, bugcheck, HA/automatic recovery, emergency incident containment.

**blind spots:** direct API without API/handle telemetry, local logs lost on shutdown, attacker-cleared logs, physical power/BMC event absent, clock skew, external probe mapped to wrong asset, approved account compromise.

**tuning:** baseline by asset role and maintenance cadence; require independent availability effect; never permanently allow administrator/SYSTEM or planned reason. For 41/6008 without requester, route to external-control and hardware evidence rather than infer a local attack.

#### `TA0040-T1529-NJA-DEFERRED-TASK-TO-BOOT`

**name:** 延期任务登记—触发—重启谱系 / Deferred Task Registration–Trigger–Reboot Lineage。

**platforms:** `[Windows]`。

**logic:** 在 task registration 时解析完整 XML/definition，规范化 stable task ID、creator、action path/arguments、run-as、trigger/next-run、definition digest 和 approval。将 future trigger 进入 watchlist；运行时连接 Task Scheduler run instance、scheduler child process、`shutdown.exe`/API、Event 1074 和 new boot/outage。初始重点检查创建后 24 小时内的一次性 shutdown/reboot task，但不以 10–60 分钟设恶意阈值。若 task 被删除，仍用已保存 definition 和 run ID 连接；仅创建未运行输出 candidate，仅运行无原始 writer 标记 lineage unresolved。

**data requirements:**

- `scheduled-task-registration`: channel `TaskScheduler Operational Event 106 plus Security 4698 or management audit`; fields `event_time`, `asset_id`, `task_id_or_path`, `task_xml`, `creator_sid`, `creator_process_id`, `action_path`, `arguments`, `run_as`, `trigger_time`, `next_run`, `definition_digest`。
- `scheduled-task-runtime`: channel `TaskScheduler Operational`; fields `event_time`, `asset_id`, `task_id_or_path`, `run_instance_id`, `actual_start`, `runtime_principal`, `scheduler_process_id`, `action_result`, `delete_time`。
- `process-and-lifecycle`: fields from prior analytic plus `run_instance_id`, `shutdown_process_start_key`, `event_1074_time`, `boot_time`。
- `task-change-approval`: fields `approval_id`, `asset_id`, `task_id_or_path`, `approved_definition_digest`, `owner`, `valid_from`, `valid_until`, `expected_reboot`。

**observables:** one-time task action resolves to forced shutdown/reboot; creator differs from approved patch controller; original process ended before scheduler child; task removed after run; same task/run connects to actual reboot and health loss.

**correlation:** preserve task from registration through scheduled time plus 15 minutes, initially capped at 24 hours for this child; retain full critical-task lifecycle 90 days under `MIT-000088`. Join scheduler child to Event 1074 within 2 minutes and boot/outage within 30 minutes. Dimensions `asset_id`, `task_id`, `definition_digest`, `creator_sid`, `runtime_principal`, `run_instance_id`, `scheduled_time`, `boot_id`, `approval_id`.

**false positives:** Windows Update, installers, patch management, backup/recovery, OEM support, compliance reboot, approved one-time operations, offline catch-up and DST/time-zone changes.

**blind spots:** Operational/Security task audit disabled, direct TaskCache manipulation without registry/file monitoring, task ID reuse, task deletion before collection, clock tampering, MDM schedule visible only in provider control plane.

**tuning:** allow only exact controller, signed action path, definition digest, target set, window and approval; blank/random task names and `/f` are risk features, not verdicts. Do not suppress every task run as SYSTEM.

#### `TA0040-T1529-NJA-MANAGEMENT-PLANE-POWER-OUTCOME`

**name:** 管理面电源操作—目标 VM—来宾结果关联 / Management-Plane Power Operation–Target VM–Guest Outcome Correlation。

**platforms:** `[ESXi, Virtualization]`。

**logic:** 从 vCenter/ESXi Event API、session 和 shell audit 规范化 power-off/reset/shutdown/reboot action，保留 event key、chainId/auditId、createdTime、userName、session/source、host 和 VM managed object ID。将 control event 在两分钟内连接 `VmPoweredOffEvent`/runtime power state，并用 CMDB 连接 guest asset ID、guest boot/shutdown event、agent heartbeat、network/service health。若 guest 无对应本地 clean shutdown requester而外层 unapproved action闭合，输出 `outer_plane_transition_confirmed`；十分钟内同一 session 对多 VM 的批量 action 形成 fleet incident，但每个 target 保留自己的 outcome。

**data requirements:**

- `virtualization-event`: channel `vCenter EventManager / ESXi hostd-vpxa`; fields `created_time`, `event_key`, `chain_id`, `audit_id`, `event_type`, `user_name`, `host_id`, `vm_id`, `full_formatted_message`, `result`。
- `management-session-shell`: channel `vCenter session events, ESXi shell/audit`; fields `event_time`, `session_id`, `user_name`, `source_ip`, `user_agent`, `command_or_api`, `target_vm_id`, `process_or_shell_id`, `result`。
- `vm-runtime-and-guest-health`: fields `event_time`, `vm_id`, `power_state`, `clean_power_off`, `guest_asset_id`, `guest_boot_id`, `local_shutdown_request_present`, `agent_heartbeat`, `network_health`, `business_health`。
- `virtualization-inventory-approval`: fields `vm_id`, `guest_asset_id`, `host_id`, `cluster_id`, `business_owner`, `criticality`, `approval_id`, `maintenance_window`, `allowed_power_operator`。

**observables:** unapproved vCenter/ESXi account or shell powers off VM; same session powers off many VMs; guest heartbeat disappears without local requester; power operation precedes VM-file encryption or outage, with encryption used only as context.

**correlation:** management request to power state 2 minutes; guest heartbeat/health 5 minutes; fleet clustering 10 minutes; approval and follow-on context 24 hours. Dimensions `management_server`, `session_id`, `user_name`, `source_ip`, `event_key`, `chain_id`, `host_id`, `vm_id`, `guest_asset_id`, `approval_id`, `time`.

**false positives:** HA isolation response, DRS/maintenance, planned migration, administrator shutdown, backup quiescence, autoscaling/cost policy, disaster recovery, datacenter outage.

**blind_spots:** logs retained only on compromised hypervisor, direct BMC/physical power, guest and VM ID mapping absent, encrypted/disabled remote logging, stolen approved admin account, time skew, guest agent already unhealthy.

**tuning:** baseline exact event type, actor/source, cluster role and target set; require remote immutable retention and CMDB mapping. Do not whitelist vCenter administrators or `vim-cmd`; rate and fleet size raise severity only with missing approval and target outcome.

## 8. Mitigation 设计

### `TA0040-T1529-MIT-LIFECYCLE-AUTHORITY-RESILIENCE` — 系统生命周期权限与可用性韧性 / System Lifecycle Authority and Availability Resilience

**measures**

1. `least-lifecycle-transition-authority`：限制 Windows `SeShutdownPrivilege`/remote shutdown、sudo/systemd power、network reload、vCenter/ESXi/cloud/BMC power operation；按主机/VM 集合授权，管理网隔离，强制 MFA/PAM/JIT，禁止共享 root 和无范围 fleet power。`preventive`。
2. `differently-authorized-transition-approval`：关键/批量关机和重启绑定 owner、双人或工单审批、精确 target set、operation、reason、窗口与到期；紧急操作使用独立 break-glass 审计。`governance`。
3. `cross-plane-lifecycle-audit`：把 local requester、task definition/runtime、vCenter/ESXi/cloud/BMC events 与 guest/业务 health 发送到攻击者不能同时清除的远程存储，并维护 management ID 到 guest/CMDB 映射。`detective-support`。
4. `bounded-restart-and-failover`：为关键系统演练 HA/failover/known-good boot 与依赖恢复；自动重启带速率限制、攻击 actor 隔离和循环停止保护，不盲目与攻击者反复 power-off 对抗。`containment`。
5. `evidence-preserving-power-recovery`：处置前保存 task/control session、event chain、guest last-seen、volatile-evidence 可用性和破坏上下文，撤销身份并恢复电源后验证数据、boot trust 和业务一致性。`containment`。

**parent application**

zh：按资产角色收紧本地、远程和外层生命周期权限，所有关键关机/重启都连接到不同权 approval 和外部 availability probe；未批准 request 与实际 outage 共现时先隔离主体/管理 session，再按演练顺序恢复。预期效果是让正常生命周期接口不再等同于无条件授权，缩小中断范围与持续时间并保留发起者。限制是物理断电、共同管理面失陷和合法紧急处置可能绕过或触发控制；自动恢复还可能重新启动已破坏系统或形成关机循环。

en: Tighten local, remote, and outer-plane lifecycle authority by asset role and join every critical shutdown or reboot to differently authorized approval and an external availability probe. When an unapproved request and actual outage co-occur, isolate the principal or management session before recovery in an exercised dependency order. The expected effect is to prevent ordinary lifecycle interfaces from implying unconditional authorization, reduce outage scope and duration, and preserve the initiator. Physical power loss, compromise of the shared management plane, and legitimate emergency response can bypass or trigger controls, while automatic recovery may restart a damaged system or enter a shutdown loop.

**deferred child application**

zh：限制能创建以 shutdown/reboot 为 action 的 task writer 和 runtime identity，把 one-time task 的 definition digest、creator、next-run、target、approval 与实际 boot 绑定；在未来触发前可撤销异常 task，并对关键系统要求双人审批。预期效果是关闭 writer 与结果的时间断点。限制是合法补丁高度依赖调度器，时钟/离线补跑改变触发时间，受管 controller 被攻陷时定义仍可能满足策略。该 application 与 `MIT-000088` 的调度定义/长期保留措施共同实施。

en: Restrict writers and runtime identities for tasks whose action is shutdown or reboot, and bind a one-time task’s definition digest, creator, next run, target, approval, and actual boot. Suspicious future triggers can be revoked before execution, and critical systems require dual approval. The expected effect is to close the temporal break between writer and outcome. Legitimate patching heavily depends on schedulers, clock or offline catch-up changes trigger time, and a compromised managed controller may still satisfy policy. Apply this application with `MIT-000088` scheduler-definition and long-retention measures.

**outer-plane child application**

zh：对 vCenter/ESXi/cloud/BMC power operations 使用隔离管理网、lockdown、按 VM 最小 RBAC、MFA/PAM/JIT、批量操作双人批准和远程不可变 event/session 保存；将每个 target VM 的 power outcome 与 guest health 和 owner 对齐。预期效果是减少单个 host/admin 静默关闭 fleet 的能力，并在 guest 离线时保留外层因果。限制是 hypervisor/root 与日志根同时失陷可伪造或删除记录，HA/DR 合法批量动作复杂，严格限制可能延迟紧急恢复。

en: Apply segmented management networks, lockdown, per-VM least RBAC, MFA, PAM, JIT, dual approval for bulk actions, and remote immutable event and session retention to vCenter, ESXi, cloud, or BMC power operations. Align each target VM power outcome with guest health and owner. The expected effect is to reduce the ability of one host or administrator to silently power off a fleet and preserve outer-plane causality after guests go offline. Simultaneous compromise of hypervisor or root and the logging root can falsify or erase records, HA or DR legitimately performs complex bulk actions, and strict controls can delay emergency recovery.

### `MIT-000088` extension

**resolution: extend, not create.** Measures for least scheduler admission, versioned action integrity, independent lifecycle audit and cross-window retention remain unchanged. Add one application for the deferred child:

- use: bind every scheduled shutdown/reboot definition to creator, exact action/arguments, runtime identity, next-run, target and time-bounded approval; place unapproved future triggers on a revocation queue and retain definition through boot.
- expected effect: task registration cannot age out before impact, and Task Scheduler/SYSTEM at event time no longer severs the original writer.
- limitations: legitimate patching, installers and recovery use the same scheduler; task audit gaps, direct backend manipulation and compromised managed controllers still defeat lineage. Do not add a generic parent application because the existing MIT does not govern immediate or outer-plane power operations.

## 9. 共享库查重与复用决议

已运行 `library_lookup.py` 搜索 `system shutdown reboot availability maintenance approval`、`scheduled reboot task shutdown one hour delayed lifecycle transition`、`hypervisor power off virtual machines guest telemetry ransomware`、`shutdown initiator boot id external availability correlation`、`lifecycle transition authority task registration power state`、`critical system reboot shutdown privilege resilience`，并对 T1529、NotPetya、Play、shutdown/WMI/VM power URL 和字段做精确 `rg` 检查。

| 对象 | 决议 | 原因 |
|---|---|---|
| `REF-000870` | **reuse** | 固定 T1529 identity 完全一致。 |
| `REF-000601` | **reuse + extend metadata** | 同一 Microsoft Petya source，新增使用其 scheduled reboot 段；不得复制 REF。 |
| `REF-000294` | **reuse** | WMI shutdown request attribution fields identity unchanged。 |
| `CASE-000208` NotPetya Mixed Internal Propagation | **split / no extend** | 现有 case 的 central event 是混合传播路径；延期 reboot 是不同事件与结论，新建 case。 |
| `DET-000213` / `NJA-000261` 业务服务控制到可用性 | **split** | 服务 state/health 与 whole-system boot/power evidence 不同，且不含 scheduler 或 hypervisor fields。 |
| `MIT-000194` 关键业务服务控制 | **split** | Measures 围绕 SERVICE_STOP/DACL 与 service failover，不能直接承担 SeShutdown/VM power/fleet governance。 |
| `DET-000076` / `NJA-000055` 电源状态与立足点寿命 | **adjacent / no reuse** | 检测阻止 lifecycle 并证明 foothold 存续；T1529 检测触发 transition 和 availability loss，因果方向相反。 |
| `MIT-000076` | **no extend** | 强制重启以清除易失入口，不是治理恶意重启权限；可能作为相邻控制但 application identity 不同。 |
| `DET-000087` / `NJA-000064` 调度对象生命周期 | **split** | 可提供 task writer/runtime 研究先例，但不含 shutdown lifecycle、boot 和 external availability confirmation；新增数据与确认门，Analytic 不能原样复用。 |
| `MIT-000088` | **extend** | Scheduler control purpose and measures remain unchanged；添加 deferred child-specific application 即可。 |
| `DET-000199` / `MIT-000182` restricted boot | **adjacent / no reuse** | 目标是 boot mode、防御组件缺失与 follow-on action，不是系统访问中断。 |
| `MIT-000080` ESXi GuestOps governance | **split / no extend** | Controls StartProgramInGuest/file transfer and Tools；VM power authority/action set differs, though isolated management and remote audit ideas inform the new MIT。 |
| `NJS-0111-004` observation-domain encapsulation | **adjacent, no merge** | guest 内执行逃离 host sensor；T1529 child 是 host/management action 逃离 guest sensor，方向和结果均不同。 |
| New DET/NJA/MIT | **create** | Strategy objective, outcome gates, concrete data and control measures are unique. |

未发现可直接复用的 T1529 Claim、case、DET、NJA 或 system-lifecycle MIT。正式分配前主 Agent 应重新运行 fuzzy duplicate audit，尤其核对同批 T1499 是否建立相同 dirty-reboot Analytic；T1499 只拥有 crash/resource-exhaustion cause，T1529 保留 lifecycle requester/control-plane cause。

## 10. 集成限制与验收点

1. 决策为 `adapt`；`original_attack_subtechniques_imported: false`；正式对象保持 `review`。
2. 支持两个 Niji 子项；不得按 shutdown/reboot、graceful/forced、platform、command 或 target type 再拆分。
3. reason-code camouflage 与 maintenance-window staggering 保持 `defer`，不分配 ID。
4. 每次确认必须有实际 lifecycle transition 与 system-level availability outcome；命令/API/task/power event without state result 只报 attempt。
5. 与 NJT-0185、NJT-0096、NJT-0172、T1499 和 precursor-only reboot 的边界须进入正式 scope；多标签需要各自独立结果证据。
6. 新 DET 含三个双向 NJA：local Windows、deferred Windows、external ESXi。Windows 字段不得伪装成跨平台通用字段；其他平台未来添加独立 Analytic。
7. 新 MIT 对 parent 和两个 children 建应用；`MIT-000088` 只扩展 deferred child application。
8. Analytics 的 2/5/10/15/30 分钟与 24 小时窗口是来源行为和工程可用性的初始值，正式对象必须明确按 shutdown timeout、boot time、task trigger 和 fleet size 调优，不声称来源测得通用阈值。
9. 完成共享库解析、ID sync、`make quality`、Bundle 和双语 Web 测试；未完成人工领域评审前不得发布。

**最终交接状态：** `adapt`；正式 Niji 子项 `2`（延迟委托式生命周期转换、目标外控制面生命周期转换）；defer `2`（reason camouflage、维护窗口/错峰）；reuse `REF-000870`, `REF-000294`，reuse+extend `REF-000601`, extend `MIT-000088`；create DET `1`、NJA `3`、system-lifecycle MIT `1`、claims/cases/references按本交接分配。
