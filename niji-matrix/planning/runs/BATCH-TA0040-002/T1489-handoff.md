# T1489 Service Stop research handoff

`batch_ref: BATCH-TA0040-002`  
`work_item_ref: WORK-TA0040-T1489`  
`temporary_key_prefix: TA0040-T1489-`  
`status: research-only; integration pending`  
`baseline: Enterprise ATT&CK 19.1`  
`formal IDs allocated: none`

## Recommendation

**Adapt; medium confidence; zero formal Niji children.** Proposed bilingual admission rationale:

> 服务停用把业务服务或承载业务功能的进程从可用状态转为停止、禁用或无法提供功能，直接造成合法用户不能继续使用服务，符合 TA0040 的影响目的。ATT&CK T1489 同时包含公开的大规模停机、防御工具停用、恢复服务停用以及为后续加密或销毁释放文件锁等不同目的；Niji 应把正式范围适配为有独立匿迹设计的业务服务停用，即攻击者借服务自身接受的正常控制路径取得有序停止，使恶意状态变化与获批维护共享控制接口和终态外观。Prestige 在实际受害行动中硬编码 `net.exe stop MSSQLSERVER` 以便后续加密，Windows 服务模型则表明 `ControlService` 会把标准停止请求交给服务，并由服务按 `STOP_PENDING` 到 `STOPPED` 的正常状态机报告结果。[E1][E2][E3][E4]
>
> Service Stop changes a business service or a process providing business functionality from available to stopped, disabled, or unable to serve legitimate users, directly satisfying the Impact purpose of TA0040. ATT&CK T1489 also spans overt mass outage, defensive-tool impairment, recovery-service impairment, and stops used to release file locks for later encryption or destruction. Niji should adapt the formal scope to business-service stopping with an independent stealth design: the adversary uses the service's accepted control path to obtain an orderly stop, giving the malicious state change the same control interface and terminal appearance as approved maintenance. Prestige hard-coded `net.exe stop MSSQLSERVER` in observed victim operations to prepare for encryption, while the Windows service model shows that `ControlService` forwards a standard stop request and the service reports the result through its normal `STOP_PENDING` to `STOPPED` state machine.[E1][E2][E3][E4]

The fixed parent behavior and actual Prestige use are high-confidence. The narrower conclusion that the orderly control-path trace can camouflage malicious intent is **medium**: platform documentation proves the trace equivalence and the incident proves attacker use, but the incident report attributes the stop to encryption reliability rather than explicitly claiming that the actor selected it to evade detection. Canonical prose must retain this calibration.

## Required boundary convergence

- **Business service versus TA0112/NJT-0123:** T1489 owns loss of a business function such as database, messaging, Web, industrial application, or virtualization workload availability. NJT-0123 owns stopping or degrading antivirus, EDR, security sensors, logging agents, alerting, or response tooling when the direct result is reduced defensive capability. A mixed ransomware target list must be split by each service's role; one command or malware family does not collapse the owners. NJT-0123 already includes whole-capability unavailability and must not be duplicated as a T1489 child.[E1][L1]
- **Recovery service versus T1490:** stopping backup, snapshot, catalog, or recovery services to prevent creation or use of recovery material belongs to T1490 even if the same service-control primitive is used. T1489 may describe simultaneous business-service loss, but the recovery-capability conclusion is separate.[E10]
- **Service stop versus T1529:** T1489 changes one or more services or hosted applications while the operating system or hypervisor can remain running. T1529 owns shutdown or reboot of the host, VM, or network device and the resulting host lifecycle interruption.[E9]
- **Precursor versus T1486/T1485:** stopping MSSQL, Exchange, a VM, or another business application can release locks or make a datastore accessible. The stop remains a T1489 event if it independently removes the service from legitimate use; the later content encryption is T1486/NJT-0157 and later deletion or overwrite is T1485/NJT-0156. Evidence of the stop cannot substitute for evidence that data was encrypted or destroyed, and later encryption cannot prove that the earlier stop had a stealth design.[E1][E2][E8]
- **Crash and resource exhaustion:** an attacker-issued service stop or disable is distinct from T1499 resource exhaustion and from an accidental crash. A forced process kill qualifies only when it is attacker-directed and makes the business service unavailable, but it falls outside this adapted formal scope unless another supported trace-shaping design is demonstrated.

## Taxonomy breadth review and zero-child justification

Fixed ATT&CK 19.1 child count: **0**. Represented dimensions: none. Breadth trigger: ordinary open-ended search. Proposed Niji child count: **0**; `subtechnique_taxonomy.coverage: none-justified`.

| Candidate stealth axis examined | Trace change and defender effect | Resolution |
| --- | --- | --- |
| Orderly control-path stop versus abnormal termination | SCM forwards an accepted stop control and the service reports normal pending/stopped states; a state-only observer sees the same terminal form as approved administration rather than an abnormal service failure | **Parent-core admission variable.** It defines the adapted parent scope; making it the only child would duplicate the entire formal parent.[E3][E4][E5] |
| Command wrapper (`net`, `sc`, PowerShell) versus direct `ControlService` API | Wrapper use creates an explicit process/command line; direct API use can omit that wrapper while the service state result remains the same | **Not-stealth-distinct as a child.** The distinction is implementation and telemetry availability. Defenders should support both paths in one Analytic; current sources do not establish a stable sibling taxonomy or explicit evasion intent.[E3][E6][E7] |
| Transient stop versus disabled start type | A stop changes current state; configuration disablement also prevents later start and may add configuration events | **Parent-core / impact-duration distinction.** Persistence of unavailability changes recovery work, but evidence does not establish a separate stealth effect.[E4][E5] |
| One carefully selected service versus many services | Fewer state changes can produce less volume, while mass stops are conspicuous | **Evidence-deferred.** Prestige proves one MSSQL stop and Microsoft hunting provides a mass-stop heuristic, but neither proves that target count was selected to evade thresholds. Service role or count alone cannot define NJS.[E2][E8] |
| Stop during a maintenance window or with a maintenance-like account | Time and actor may fit an approved administrative baseline | **Evidence-deferred.** Plausible camouflage, but no conclusion-level source in this review proves attacker-controlled alignment with a real maintenance window or ticket context. |
| Cross-host staggered or low-rate stop | Events would be separated across time or assets and could evade short local thresholds | **Evidence-deferred.** No T1489 source reviewed establishes deliberate staggering or a supported correlation horizon. |
| Defensive, backup, or recovery service selection | Stops remove observation or recovery capability | **Adjacent technique.** Owned by NJT-0123 or T1490 according to target role and direct result, not Niji children of business Service Stop.[E10][L1] |
| VM or host power-off | Host lifecycle rather than an individual service state changes | **Adjacent technique.** Owned by T1529 when the VM/host is shut down or rebooted.[E9] |

Zero children are appropriate because the only supported stable stealth variable is the parent's formal admission boundary. Command/API form, platform, service type, target count, current-state versus start-mode persistence, and downstream payload are implementations or adjacent outcomes. A future child would require evidence for a second attacker-controlled variable, its distinct trace and observation effect, prerequisites, scenario, and different detection or mitigation logic.

## Proposed parent content (`TA0040-T1489-PARENT`)

Name: **业务服务停用 / Business Service Stop**  
Aliases: `Service Stop`, `T1489`  
Summary:

> 攻击者通过服务接受的正常控制路径有序停止业务服务，使合法功能中断并让恶意停用在状态层看似常规管理操作。
>
> Adversaries orderly stop business services through accepted control paths, interrupting legitimate functionality while making malicious disablement resemble ordinary administration at the state layer.

### `definition_and_concept`

> 业务服务停用是攻击者使数据库、消息、Web、工业应用、文件共享、虚拟化工作负载或其他业务功能从运行状态转为停止、禁用或不能继续服务合法用户。直接对象是服务可用性及其消费结果；服务管理命令、API、进程终止方式、服务名称和平台只是实现。服务仍登记在系统中、底层数据仍存在或主机仍运行，都不否定已经发生的业务可用性损失。[E1][E5][E11]
>
> Business Service Stop is adversary action that moves a database, messaging, Web, industrial application, file-sharing, virtualization workload, or another business function from running to stopped, disabled, or unable to serve legitimate users. The direct object is service availability and its consumer outcome; service-management commands, APIs, process-termination methods, service names, and platforms are implementations. The service can remain registered, its underlying data can survive, and its host can remain running while business availability has still been lost.[E1][E5][E11]

> Niji 的正式概念进一步要求有证据的匿迹设计。当前成立的设计是攻击者让服务管理器转交标准停止请求，使服务按自身状态机完成清理并报告正常的停止终态。恶意意图因此不编码在终态本身，防守方必须把控制者、命令或 API、授权变更、维护审批与业务结果重新连接；单纯崩溃、资源耗尽或公开批量杀进程不进入这一适配范围。[E2][E3][E4]
>
> The formal Niji concept additionally requires an evidenced stealth design. The supported design has the adversary make the service manager deliver a standard stop request so the service performs its own cleanup and reports an ordinary stopped terminal state. Malicious intent is therefore absent from the terminal state itself, and defenders must reconnect the controller, command or API, authority, maintenance approval, and business result. A crash, resource exhaustion, or overt mass process kill alone does not enter this adapted scope.[E2][E3][E4]

### `stealth_characteristics`

> 业务服务停用的核心匿迹特性是控制意图与状态结果分离。Windows SCM 接受 `SERVICE_CONTROL_STOP` 后，由服务从运行态经过停止待定状态进入停止态；同一套接口也服务于正常维护。攻击者使用这一控制路径时，状态清单和健康面只显示熟悉的“已停止”，不会自动说明停止由恶意主体发起或为了后续加密。与未报告 `SERVICE_STOPPED` 的异常终止相比，有序停止还会减少崩溃或失败这一类区分特征。[E3][E4][E5]
>
> Business Service Stop separates control intent from state outcome. After Windows SCM accepts `SERVICE_CONTROL_STOP`, the service moves from running through stop-pending to stopped, using the same interface used for ordinary maintenance. When an adversary uses this path, state inventory and health monitoring show the familiar “stopped” result without inherently identifying a malicious initiator or the intent to enable later encryption. Compared with termination that fails to report `SERVICE_STOPPED`, an orderly stop also removes crash or failure as a distinguishing feature.[E3][E4][E5]

> 残余痕迹包括 `net.exe`、`sc.exe` 或 PowerShell 等控制进程及命令行、调用账户与登录会话、SCM 状态变化、启动类型、依赖服务变化、应用健康失败、维护单据缺口以及后续数据操作。若攻击者直接从载荷调用 SCM API，命令包装器可能不存在，但调用进程、服务句柄访问或独立业务探针仍可能恢复因果；若端点传感器随服务一起失效，则应转向不同权的集中日志和外部健康面。[E3][E6][E7][E8]
>
> Residual traces include controller processes and command lines such as `net.exe`, `sc.exe`, or PowerShell, the calling account and logon session, SCM state changes, start mode, dependent-service changes, application-health failures, missing maintenance authorization, and follow-on data operations. A payload calling the SCM API directly can omit a command wrapper, but caller-process telemetry, service-handle access, or an independent business probe can still recover causality. If endpoint sensing fails with the service, defenders need differently authorized centralized logs and an external health plane.[E3][E6][E7][E8]

### `scope_boundary_definition`

> 纳入攻击者有意控制的业务服务停止或禁用，其结果必须使组织期望提供的业务功能实际不可用，并且证据能够连接正常控制路径与较低可区分的状态外观。服务“已停止”本身不够；判定还需要目标的业务职责、控制主体或进程、未获批上下文以及健康或用户结果。正常补丁、升级、故障转移、容量维护、管理员排障、依赖服务编排、崩溃恢复与许可证问题均是强反例。[E3][E8][E11]
>
> Scope includes adversary-controlled stop or disablement of a business service that actually makes an expected organizational function unavailable, with evidence joining the ordinary control path to a less distinguishable state appearance. “Stopped” alone is insufficient; classification also requires the target's business role, the controlling principal or process, lack of approval, and a health or user outcome. Normal patching, upgrade, failover, capacity maintenance, administrator troubleshooting, dependency orchestration, crash recovery, and licensing failures are strong counterexamples.[E3][E8][E11]

> 安全产品、遥测代理或响应服务被停用并直接削弱防御时归 NJT-0123；备份、快照、恢复目录或恢复环境的服务被停用并直接损害恢复能力时归 T1490。整个主机、虚拟机或网络设备被关机或重启归 T1529。为后续加密或销毁释放文件锁可以与本技术构成事件链，但文件内容随后变成密文归 NJT-0157，删除或覆写归 NJT-0156；本技术不以勒索载荷、服务类别或后继结果替代自身证据。[E1][E2][E9][E10][L1]
>
> Stopping a security product, telemetry agent, or response service belongs to NJT-0123 when it directly impairs defense. Stopping backup, snapshot, recovery-catalog, or recovery-environment services belongs to T1490 when it directly harms recovery. Shutdown or reboot of an entire host, VM, or network device belongs to T1529. Releasing file locks for later encryption or destruction can form an event chain with this technique, but ciphertext belongs to NJT-0157 and deletion or overwrite belongs to NJT-0156. A ransomware payload, service category, or successor outcome cannot replace evidence of this technique.[E1][E2][E9][E10][L1]

### `application_scenarios_and_threat_model`

Application scenarios:

> 在勒索或破坏行动进入数据处理阶段前，攻击者可使用已取得的本地管理员会话、远程管理通道或载荷内服务 API，有序停止 MSSQL、Exchange、Web 应用或虚拟化相关业务服务。停止既会立即中断合法业务，也可能释放应用持有的数据文件，使后继加密或删除能够覆盖更多内容。Prestige 以硬编码的 `net.exe stop MSSQLSERVER` 展示了这一链；分类时仍须把服务可用性、后继内容状态和恢复能力分别记录。[E1][E2][E8]
>
> Before ransomware or destructive operations enter data processing, an adversary can use an acquired local administrator session, remote management channel, or an in-payload service API to orderly stop MSSQL, Exchange, a Web application, or a virtualization-related business service. The stop immediately interrupts legitimate business and may also release application-held data files so later encryption or deletion covers more content. Prestige demonstrates this chain with hard-coded `net.exe stop MSSQLSERVER`; classification must still record service availability, successor content state, and recovery capability separately.[E1][E2][E8]

Attacker model:

> 攻击者需要对目标服务拥有 `SERVICE_STOP` 或等价控制权限，知道服务身份、依赖关系和哪些业务数据会因停止而解除占用，并能承受停机可能立即暴露行动。命令包装器便于自动化但留下进程与参数；直接 API 调用减少独立包装器，却仍需要调用进程和服务句柄。不可停止的服务、受保护服务 DACL、不同权控制面、集群仲裁、快速故障转移和操作审批会限制效果。[E3][E5][E11]
>
> The adversary needs `SERVICE_STOP` or equivalent control authority over the target, knowledge of service identity and dependencies and of business data whose locks will be released, and tolerance for outage exposing the operation. Command wrappers ease automation but leave process and argument traces; a direct API call removes the separate wrapper but still requires a caller process and service handle. Non-stoppable services, protected service DACLs, differently authorized control planes, cluster quorum, rapid failover, and operational approval constrain the effect.[E3][E5][E11]

Defender model:

> 防守方假定保存服务清单和业务 owner、Service Control Manager 状态、进程创建与命令行、账户和登录会话、远程会话来源、维护审批以及独立业务健康探针，并能按设备、服务、主体、进程、时间和变更单关联。仅查看当前服务状态无法判断操作者；仅检测 `net.exe` 或 `sc.exe` 会遗漏 PowerShell、WMI 和直接 API；只把停机当作可用性告警又会失去与后继文件活动的攻击链联系。[E3][E6][E7][E8]
>
> The defender is assumed to retain a service inventory and business owner, Service Control Manager state, process creation and command line, account and logon session, remote-session origin, maintenance approval, and an independent business-health probe, with correlation by device, service, principal, process, time, and change record. Current service state alone cannot identify the operator. Detection limited to `net.exe` or `sc.exe` misses PowerShell, WMI, and direct APIs, while treating the outage only as an availability alert loses its attack-chain relationship to successor file activity.[E3][E6][E7][E8]

### `stealth_mechanisms`

- `mechanism_ref: NM-FD`; role `primary`; confidence `medium`.
- Summary: **有序停止让恶意中断呈现常规管理终态 / Orderly stopping gives malicious interruption an ordinary administrative terminal state**
- Analysis:

> 攻击者经服务管理器发送服务已声明接受的停止控制，服务执行自身清理并报告停止待定和停止终态；痕迹从异常崩溃或强制终止变为正常管理也会产生的状态序列。只消费服务状态或可用性面板的防守方难以从终态区分恶意与维护，形成特征伪装。进程与 API 调用者、服务控制权限、审批上下文和不同权健康探针仍能揭示矛盾；由于公开案例未明确陈述攻击者以伪装为选择动机，置信度保持 medium。[E2][E3][E4][E5]
>
> The adversary sends a stop control that the service declares it accepts through the service manager, allowing the service to perform its own cleanup and report stop-pending and stopped terminal states. The trace changes from abnormal crash or forced termination to a state sequence also produced by normal administration. A defender consuming only service state or an availability dashboard has difficulty distinguishing malicious action from maintenance at the terminal state, producing Feature Disguise. Process or API caller, service-control authority, approval context, and a differently authorized health probe can still reveal the contradiction. Confidence remains medium because the public incident does not explicitly state camouflage as the actor's selection motive.[E2][E3][E4][E5]

Rejected mechanisms: `NM-ST` is unsupported because neither Prestige nor the platform sources establish deliberate low-rate or cross-host staggering. `NM-BT` is not assigned merely because command-line-only analytics miss direct APIs; the service state remains visible, and a sensor-coverage gap alone does not prove attacker exploitation of an unobserved domain. `NM-DO` is reserved for actual impairment of defensive observation and therefore belongs to NJT-0123 when a security or logging service is the target.

### `subtechnique_taxonomy`

> 当前 taxonomy 为 `none-justified`。有序控制路径是本父技术进入正式 Niji 范围的共同变量，不能再复制成与父级同义的单一子技术。命令包装器、直接 API、PowerShell、WMI、服务类型和操作系统只是实现；临时停止与启动类型禁用改变影响持续时间；目标数量和业务类别改变严重度与调优，不自动改变匿迹机理。
>
> The current taxonomy is `none-justified`. Orderly use of the control path is the common variable admitting this parent into formal Niji scope and cannot be duplicated as a single child synonymous with the parent. Command wrappers, direct APIs, PowerShell, WMI, service type, and operating system are implementations. A transient stop versus disabled start mode changes impact duration, while target count and business category change severity and tuning without automatically changing the stealth mechanism.

> 维护窗口贴合、跨主机渐进停用和远程控制面分离仍是开放研究轴，但缺少结论级攻击证据、稳定兄弟边界或独立防御差异。防御工具、恢复服务和整机生命周期已有相邻 owner；在这些证据缺口解决前，零子技术比按工具、平台或影响对象强行拆分更可审查。
>
> Maintenance-window alignment, gradual cross-host stopping, and remote control-plane separation remain open research axes, but they lack conclusion-level adversary evidence, stable sibling boundaries, or independent defensive differences. Defensive tools, recovery services, and whole-host lifecycle already have adjacent owners. Until those evidence gaps close, zero children are more reviewable than partitions forced by tool, platform, or impact target.

### `research.limitations`

> ATT&CK 19.1 和 Microsoft Prestige 报告确证业务服务停用及其对后继加密的前置作用，Microsoft 平台资料确证标准停止请求、服务状态机、停止权限和异常终止边界。公开来源没有证明 Prestige 的操作者以伪装维护为明确意图，也没有给出所有目标环境中 SCM 事件、EDR API 调用和业务探针的统一字段覆盖；因此父级 Feature Disguise 结论为 medium，直接 API、时间贴合和低速分布轴保持 deferred。Windows 证据不能自动外推到 systemd、launchd、ESXi 或云服务控制面，跨平台正式扩展需要逐平台事件与权限证据。[E1][E2][E3][E4][E5]
>
> ATT&CK 19.1 and Microsoft's Prestige report establish business-service stopping and its precursor role for later encryption, while Microsoft platform documentation establishes the standard stop request, service state machine, stop authority, and abnormal-termination boundary. Public sources do not show that the Prestige operator explicitly intended to resemble maintenance, nor do they provide uniform SCM-event, EDR-API, and business-probe field coverage for every target environment. The parent's Feature Disguise conclusion is therefore medium, and direct-API, temporal-alignment, and low-rate distribution axes remain deferred. Windows evidence cannot be automatically generalized to systemd, launchd, ESXi, or cloud control planes; each platform needs its own event and authority evidence before formal extension.[E1][E2][E3][E4][E5]

## Evidence and shared-library candidates

Suggested temporary claims:

- `TA0040-T1489-CLM-ADAPT`: T1489 is adapted to business-service stopping whose accepted control path yields an ordinary administrative terminal state, with medium stealth confidence.
- `TA0040-T1489-CLM-ORDERLY-STATE`: `ControlService` plus service-reported stop states changes the trace from abnormal failure to ordinary stopped-state sequence.
- `TA0040-T1489-CLM-BOUNDARY`: target role and direct result separate business availability, defensive capability, recovery capability, host lifecycle, and data content outcomes.
- `TA0040-T1489-CLM-ZERO-CHILD`: implementation form, duration, target type, and count do not pass independent Niji child gates.

Suggested case: `TA0040-T1489-CASE-PRESTIGE-MSSQL-STOP`. Scope it narrowly to Microsoft's observation that Prestige hard-coded `C:\Windows\System32\net.exe stop MSSQLSERVER` before encryption in attacks against transportation and logistics organizations in Ukraine and Poland. The case supports parent behavior and the normal control-path implementation. It does **not** independently establish maintenance camouflage or a Niji child.[E2]

### Evidence ledger

| Key | Primary source and locator | Supported conclusion and limit |
| --- | --- | --- |
| E1 | MITRE ATT&CK 19.1 [T1489 Service Stop](https://attack.mitre.org/versions/v19/techniques/T1489/), description, platforms, no-subtechnique inventory | Parent behavior, Impact mapping, business service unavailability, and precursor relation to T1485/T1486; does not prove a Niji stealth mechanism. |
| E2 | Microsoft Threat Intelligence, [New “Prestige” ransomware](https://www.microsoft.com/en-us/security/blog/2022/10/14/new-prestige-ransomware-impacts-organizations-in-ukraine-and-poland/), Malware analysis | Observed victim campaign and hard-coded `net.exe stop MSSQLSERVER` before encryption; does not state camouflage intent. |
| E3 | Microsoft Learn, [Stopping a Service](https://learn.microsoft.com/en-us/windows/win32/services/stopping-a-service), `ControlService`, dependencies, and state loop | Standard manager-mediated stop path and required status checks. |
| E4 | Microsoft Learn, [Service State Transitions](https://learn.microsoft.com/en-us/windows/win32/services/service-status-transitions) and [Winsvc.h](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/), stopped-state/failure definitions | Normal pending-to-stopped state reporting and distinction from failure without a stopped report. |
| E5 | Existing `REF-000336`, Microsoft Learn [Service Security and Access Rights](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights), `SERVICE_STOP` and DACL table | Exact reuse. Stop authority, status query, DACL, and warning against untrusted stop rights. |
| E6 | Microsoft Learn, [Event 4688](https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4688), XML fields and command-line policy | Process, subject, logon, process ID, image, parent, elevation, and optional command-line fields; command line is disabled by default. |
| E7 | Microsoft Learn, [DeviceProcessEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table), schema table | Exact MDE process fields used by the proposed Analytic; only applies where MDE is deployed. |
| E8 | Microsoft Defender XDR, [Find ransomware with advanced hunting](https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-find-ransomware), net-stop query and intent table | `net.exe ... stop` hunt and two-minute multi-command example; sample threshold is not universal and direct APIs remain blind. |
| E9 | MITRE ATT&CK 19.1 [T1529 System Shutdown/Reboot](https://attack.mitre.org/versions/v19/techniques/T1529/), description | Whole-host or VM lifecycle boundary. |
| E10 | MITRE ATT&CK 19.1 [T1490 Inhibit System Recovery](https://attack.mitre.org/versions/v19/techniques/T1490/), description | Recovery service/copy boundary. |
| E11 | Microsoft Learn, [Start, Stop, Pause, Resume, and Restart SQL Server Services](https://learn.microsoft.com/en-us/previous-versions/sql/database-engine/configure-windows/start-stop-pause-resume-restart-sql-server-services), service status and connection behavior | Business-service role, administrative stop methods, privilege, and availability effects; not adversary evidence. |
| L1 | Existing Niji `NJT-0123 Defensive Tool Function Impairment` | Formal local scope owner for security-tool, sensor, logging-agent, and response-function impairment. It is a boundary object, not evidence for T1489. |

## Exact shared-library lookup and resolution advice

Required `library_lookup.py` searches were run for `service stop`, `critical service stop`, `ransomware services`, `service control manager`, `MSSQL service stop`, `Prestige ransomware`, `Find Ransomware with Advanced Hunting`, `Service Security and Access Rights`, and `Stopping a Service`.

- **Reuse `REF-000336`** exactly. Its canonical URL and locator directly cover `SERVICE_STOP`, DACLs, state-query rights, and the risk of granting stop rights to untrusted users.[E5]
- `DET-000092`, `NJA-000069`, and `MIT-000093` were the closest semantic matches. They govern service-based **execution**, service definitions, manager children, and create/start/delete transactions. T1489 needs stop-to-business-outage correlation, approved-maintenance comparison, and availability controls. Recommend **split/create** new DET/NJA/MIT identities rather than extending the execution objects by name similarity.
- `REF-000290` and `REF-000291` discuss service execution rather than stopping a business service; do not reuse them as conclusion-level T1489 evidence.
- `REF-000275` and `REF-000760` are existing CISA ransomware sources whose current canonical locators support deployment tooling or Safe Mode. Their source pages may mention service actions, but the stored locator and existing claims do not support this candidate's orderly-stop conclusion. Do not extend without a new source-level review.
- No exact canonical match was returned for the fixed T1489 page, Microsoft Prestige report, Microsoft stopping/state-transition docs, event 4688, DeviceProcessEvents, Defender ransomware hunt, or SQL service-management page. Recommend **create** reference objects after the primary Agent reruns URL-level lookup against the refreshed catalog.
- No existing Claim, Case, DET, NJA, MIT, or Relationship returned with the same semantic identity as the proposed parent admission, Prestige MSSQL-stop case, stop-to-outage Analytic, or business-service availability control. Recommended resolutions: Claims `create`; Prestige case `create`; DET/NJA `create`; MIT `create` or `split` after comparing its measures with MIT-000093.

## Defense design

### Detection Strategy `TA0040-T1489-DET-BUSINESS-SERVICE-STOP-LINEAGE`

Name: **业务服务控制—停机结果谱系 / Business Service Control–Outage Lineage**. Detect an unapproved control or configuration action that moves a registered critical business service into stopped/disabled state and produces an external availability failure. Keep later encryption/destruction as severity and relationship context rather than as proof of the stop. Domain `enterprise`; initial platform `Windows` only until systemd, launchd, ESXi, and cloud fields receive separate evidence.

### Detection Analytic `TA0040-T1489-NJA-WINDOWS-SERVICE-STOP-OUTCOME`

**Data requirements and real fields**

1. `windows-process-audit`, channel `Security/4688`: `TimeCreated`, `Computer`, `SubjectUserSid`, `SubjectUserName`, `SubjectLogonId`, `NewProcessId`, `NewProcessName`, `ProcessCommandLine`, `CreatorProcessName`, `TokenElevationType`. Enable Audit Process Creation and command-line inclusion; command line is otherwise empty.[E6]
2. `endpoint-process`, channel `Microsoft Defender XDR DeviceProcessEvents`: `Timestamp`, `DeviceId`, `DeviceName`, `FileName`, `FolderPath`, `ProcessCommandLine`, `ProcessId`, `ProcessUniqueId`, `AccountSid`, `AccountName`, `LogonId`, `IsProcessRemoteSession`, `ProcessRemoteSessionIP`, `ReportId`. Use `(Timestamp, DeviceName, ReportId)` as event uniqueness and `ProcessUniqueId` to avoid PID reuse.[E7]
3. `service-state`, channel `Windows System / Service Control Manager plus periodic Win32_Service inventory`: `timestamp`, `computer`, `provider_name`, `event_id`, `event_record_id`, `service_name`, `display_name`, `old_state`, `new_state`, `start_mode`, `process_id`, `path_name`, `start_name`. Normalize locally because SCM event payloads and event availability differ by Windows version; Win32_Service supplies `Name`, `DisplayName`, `State`, `StartMode`, `ProcessId`, `PathName`, and `StartName`.[E4]
4. `business-health`, channel specific to the organization's monitoring system: `timestamp`, `asset_id`, `service_id`, `check_id`, `endpoint`, `result`, `response_code`, `latency_ms`, `consecutive_failures`. This source must be authorized and hosted independently enough that the service stop cannot silence its only health record.
5. `service-inventory-change`, channel CMDB/change management: `asset_id`, `service_id`, `business_role`, `criticality`, `owner`, `expected_controller`, `approved_operator`, `change_id`, `window_start`, `window_end`, `expected_action`, `dependency_group`.
6. Optional `file-outcome`, channel MDE `DeviceFileEvents` or equivalent: `Timestamp`, `DeviceId`, `ActionType`, `FolderPath`, `FileName`, `InitiatingProcessUniqueId`, `InitiatingProcessAccountSid`. This is used only to link a service stop to later T1486/T1485 activity.

**Logic**

1. Normalize `net(.exe) stop <service>`, `sc(.exe) stop <service>`, PowerShell `Stop-Service`, WMI `StopService`, and approved management controllers into `service_control(stop, service_id)`. Resolve display name to stable service name through inventory. A process match is evidence of a request, not proof of successful stop.
2. Within **two minutes**, join a stop request to `new_state=Stopped`, `start_mode=Disabled`, or disappearance of the service process for the same device and service. Within **five minutes**, require an external health check failure or consumer connection failure for high-confidence business impact. A critical service may alert from one unapproved confirmed stop; do not require a mass threshold.
3. Compare actor, remote-session origin, controller image/path, service, action, device role, and time against a specific unexpired change record. A change exception must bind all these dimensions. `SYSTEM`, a signed Microsoft binary, or an expected SCM terminal state must never be a global allowlist.
4. Maintain a second branch for `Stopped/Disabled + health failure` without a matching wrapper process. Score it as unattributed and investigate direct API, WMI, management-agent, telemetry loss, crash, and failover explanations. If API-call telemetry exists, join caller process ID, API `ControlService`, target service, control code, and result; do not declare those fields universally available.
5. Over the next **thirty minutes**, link the stop to concentrated writes/renames/read failures in the service's datastore, or to a canonical NJT-0156/NJT-0157 alert. This raises severity and records the precursor relationship; it does not merge the techniques. For multi-host campaigns, aggregate unexpected critical-service stops by actor, source host, parent process, or payload hash over **one hour**, but learn thresholds from the fleet baseline. Microsoft's ten distinct `net stop` commands in two minutes is a useful hunt example, not a default production threshold.[E8]

**Observables**

- An elevated or remote session launches `net.exe stop MSSQLSERVER`, SCM reports stopped, and the database endpoint fails without a matching approved change.
- A critical business service transitions cleanly to stopped, its health probe fails, but no wrapper process is present; nearby unusual elevated processes or management requests indicate an API-mediated stop.
- Several service stops on peer systems share an actor/source/process/hash and are followed by datastore rewrites or encryption alerts.

**Correlation dimensions:** `device_id`, `service_id`, `business_role`, `dependency_group`, `subject_sid/account_sid`, `logon_id`, `process_unique_id/new_process_id`, `remote_session_ip/source_host`, `controller_image`, `command`, `change_id`, `health_check_id`, `datastore_root`, `time`.

**False positives:** approved patching and upgrades; DBA-controlled maintenance; cluster failover or dependency orchestration; service recovery tests; backup windows that legitimately stop applications; an application crash followed by administrator stop/restart; emergency incident response. Require a concrete change scope rather than a broad maintenance-window suppression.

**Blind spots:** direct API calls without API telemetry; disabled 4688 command line; missing or version-dependent SCM state events; service names localized or supplied only as display names; PID reuse without unique process ID; the endpoint sensor or log forwarder stopping with the host; remote controller request IDs not propagated to the target; external health probes sharing the failed service; attackers using a compromised approved operator during a valid change.

**Tuning:** inventory only services with a documented business role and owner; set criticality and expected controller per asset role; baseline normal stop/start cadence, dependency order, and health-check delay; bind exceptions to service, device scope, actor, controller hash, action, ticket, and expiry; retain an unattributed-state branch; validate the two/five/thirty-minute joins during controlled maintenance without turning observed maximums into universal thresholds.

### Mitigation `TA0040-T1489-MIT-CRITICAL-SERVICE-CONTROL-RESILIENCE`

Name: **关键业务服务控制与可用性韧性 / Critical Business Service Control and Availability Resilience**.

Measures:

1. `least-stop-authority` (`preventive`): remove `SERVICE_STOP`, `SERVICE_CHANGE_CONFIG`, DACL-write, remote SCM, WMI, and equivalent service-control authority from workload and ordinary administrator identities; grant JIT authority to managed operator roles from controlled origins, with MFA and ticket binding. Microsoft explicitly identifies `SERVICE_STOP` as the right required to stop a service and warns against granting it to untrusted users.[E5]
2. `approved-stop-transaction` (`governance`): require a named business owner, service/device scope, expected controller, start and end time, and recovery plan for critical stops. Preserve the request, process/API caller, service state, and ticket in a centralized different-authority log.
3. `independent-health-and-failover` (`containment`): monitor business endpoints from outside the service's host and prepare an owner-approved failover or restart runbook. Failover must verify data consistency and dependency order before taking traffic; repeated unauthorized stops should isolate the controller identity rather than create an infinite restart loop.
4. `service-definition-and-dacl-integrity` (`detective-support`): inventory service DACL, start mode, binary path, account, dependencies, recovery policy, and expected health probe; alert on unauthorized stop-right or disabled-start changes before the outage path is exercised.

Parent application:

> 对业务服务停用，将 MSSQL、Exchange、Web、工业应用和关键虚拟化服务的停止权限从通用本地管理员及工作负载身份中收缩，要求短期审批主体和受管来源；把控制请求、状态终态和外部健康失败送入不同权日志。检测到未获批停止后，撤销控制会话并按服务 owner 预先验证的依赖顺序执行故障转移或恢复，而不是仅依赖同一主机自动重启。
>
> For Business Service Stop, remove stop authority over MSSQL, Exchange, Web, industrial applications, and critical virtualization services from generic local administrators and workload identities, requiring short-lived approved principals and managed origins. Send control request, terminal state, and external health failure to a differently authorized log. After an unapproved stop, revoke the controlling session and use the service owner's prevalidated dependency order for failover or recovery instead of relying only on same-host automatic restart.

Expected effect:

> 攻击者需要先取得受控服务权限或审批面，恶意停止更可能在状态生效前被拒绝，或在业务探针失败时保留可归因控制谱系；独立故障转移缩短单实例停止造成的业务不可用时间。
>
> The adversary must first obtain governed service authority or the approval plane, making a malicious stop more likely to be denied before state change or to retain attributable control lineage when the business probe fails. Independent failover shortens the business outage caused by stopping one instance.

Limitations:

> 拥有域、集群或集中管理控制权的攻击者仍可停用多个实例或篡改审批。严格 DACL 会妨碍补丁与事件响应；未经数据一致性验证的自动重启或故障转移可能扩大数据库损坏，攻击者也可反复停止形成振荡。该缓解不阻止后继加密或销毁，相关数据与恢复控制仍须分别实施。
>
> An adversary controlling the domain, cluster, or centralized manager can still stop multiple instances or tamper with approval. Strict DACLs can obstruct patching and incident response. Automatic restart or failover without data-consistency validation can amplify database damage, and repeated adversary stops can cause oscillation. This mitigation does not prevent successor encryption or destruction, which still require separate data and recovery controls.

Resolution advice: compare the above measures with MIT-000093. Because the latter's identity is service **execution** governance and contains target integrity and manager-child controls, the preferred outcome is `create` a business-availability mitigation. If the primary reviewer chooses `extend`, add only a target-specific application and document why the existing control purpose genuinely covers stop authorization, external health, and recovery; do not silently broaden it by title.

## Content-depth and integration checks

- The parent draft covers definition, direct purpose, stealth trace change, residual observations, included/excluded behavior, normal counterexamples, application, attacker prerequisites, defender visibility, supported mechanism, taxonomy, evidence limits, and defense at NJT-0001 field responsibility depth.
- No formal child is proposed; `lineage.attck_subtechnique_inherited` is therefore inapplicable. Record fixed child count zero and the open-axis table only in planning metadata.
- Canonical evidence should include the fixed T1489 page, Prestige case source, Windows stop/state sources, and reused `REF-000336`; defense objects also need 4688, DeviceProcessEvents, Defender hunting, and SQL service-management references.
- Keep Windows-specific conclusions platform-scoped. Do not add systemd, launchd, ESXi, or cloud data fields by analogy.
- If primary review rejects the medium-confidence intentional-camouflage inference, the correct fallback is **exclude**, not retention of generic Service Stop without a supported mechanism.
- If integrated, lifecycle remains `review` after schema, quality, bundle, bilingual Web/API, duplicate, and human-content gates. This handoff allocates no canonical IDs and changes no formal or shared object.
