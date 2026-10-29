# T1496 research handoff — BATCH-TA0040-002

Research staging only. Every proposed new object uses temporary prefix `TA0040-T1496-`. No formal NJT/NJS/REF/CLM/CASE/DET/NJA/MIT/REL ID is allocated, and no canonical decision, matrix object, shared library, tactic plan, brief, or integration summary is modified.

## Admission recommendation

**Candidate:** ATT&CK Enterprise 19.1 T1496 Resource Hijacking / 资源劫持. **Recommendation:** `adapt`. **Parent confidence:** `high`. **Fixed ATT&CK children:** T1496.001 Compute Hijacking, T1496.002 Bandwidth Hijacking, T1496.003 SMS Pumping, T1496.004 Cloud Service Hijacking. `original_attack_subtechniques_imported: false`.

**准入理由（中文）：** T1496 的直接行为是攻击者未经授权占用受害组织的计算、网络、消息或托管服务能力，完成挖矿、代理转售、短信套利、垃圾消息或模型推理等攻击者任务，并把资源、配额、费用或可用性影响留给受害方。该行为明确属于 Impact 且有在野案例支撑。Niji 应保留直接资源消耗语义，但改写为研究攻击者如何控制消耗时间包络或执行观察面，使资源支出与批准业务更难区分。只有部署载荷、取得凭据或建立持久化，尚未产生未授权资源使用或费用/配额影响时，不足以完成父技术。

**Admission rationale (English):** T1496 directly covers unauthorized adversary use of a victim's compute, network, messaging, or managed-service capacity for mining, proxy resale, SMS fraud, spam delivery, model inference, or another adversary task, leaving resource, quota, cost, or availability impact with the victim. The behavior clearly serves Impact and is supported by observed campaigns. Niji should retain the direct consumption semantics while adapting the subject to how adversaries control the consumption envelope or execution observation plane so the expenditure is harder to distinguish from approved business use. Payload deployment, credential acquisition, or persistence without unauthorized usage or cost/quota effect does not complete the parent.

## Required cross-technique boundaries

- **Workload execution / 工作负载执行:** Process start, container `exec`, serverless invocation, scheduled task, script, or SaaS API call records how work begins. T1496 requires the successor resource consumption, metered transaction, quota use, cost, or capacity effect. Preserve the execution object as a precursor and join it to the impact; do not replace it with Resource Hijacking merely because a miner or proxy binary appears.
- **Credentials / 凭据:** Secret theft, valid-account use, API-key exposure, and privilege escalation establish authority. T1496 begins when that authority is used for unauthorized resource-consuming transactions. Credential rotation can stop further consumption but does not retroactively prove what resource was used.
- **C2:** Mining-pool, reverse-proxy, or operator traffic may coordinate the activity and supplies useful correlation. A C2 channel without measurable victim-resource use is not T1496, while provider-side metered consumption can occur without an endpoint C2 process visible to the victim.
- **Persistence:** Cron, launchd, scheduled tasks, Run keys, containers, and remote-management tools may keep a consumer running. Persistence and resource impact remain separately recorded; an activity-gated miner can stop and restart without changing the persistence object's classification.
- **NJT-0091 Exclusive Foothold Control / 排他立足点控制:** Removing a competing miner or persistence object while the operator's own foothold survives belongs to NJT-0091. The later compute or bandwidth use belongs to T1496. Killing a legitimate business workload only to free capacity is not competitor eviction; it may be Service Stop plus Resource Hijacking. The identity and direction of the removed object decide the boundary.
- **NJT-0121 Low-Coverage Cloud-Region Workload Placement / 低覆盖云区域工作负载放置:** Selection of an unused, unapproved, or weakly monitored Region belongs to NJT-0121. Unauthorized compute, AI, network, or messaging consumption in that Region belongs to T1496. Region name or coverage cannot define a new T1496 child; one event may reference both parents.
- **Denial of Service:** T1496 uses victim capacity to complete an attacker task, with service degradation or quota exhaustion as a possible consequence. T1498/T1499 make availability degradation the direct objective. A resource graph should preserve both only when evidence supports both purposes/outcomes.
- **Financial Theft:** Resource hijacking shifts usage costs or generates attacker revenue from consumed capacity; it does not directly transfer a victim's existing funds or settle a fraudulent financial transaction as T1657 does.

## ATT&CK-child breadth record and coverage resolutions

ATT&CK's four children divide resource and monetization forms. They are research clusters, not Niji output units. Niji open search examined five materially different variables: activity-conditioned temporal gating; provider-brokered metered execution; cross-asset utilization dilution; victim-IP attribution transfer; and low-coverage Region placement. The first two satisfy stable-variable, trace-change, sibling-boundary, evidence, and defense-difference gates. The others are parent-core, adjacent, or deferred.

| ATT&CK 19.1 child | Represented dimension | Planning-only resolution | Niji reasoning |
|---|---|---|---|
| T1496.001 Compute Hijacking | CPU/GPU/container/VM compute use and mining monetization | `niji-variable-candidate` plus `parent-core` | Compute is not a child key. Microsoft directly observed a miner closing its consumer when the device was active and restarting in idle conditions, supporting the activity-gated axis; ordinary sustained mining remains parent-core. |
| T1496.002 Bandwidth Hijacking | Proxy, scanning, torrent, or botnet bandwidth and IP use | `parent-core`; attribution-transfer axis `evidence-deferred` | Bandwidth type and proxyware name are implementations. Victim-IP attribution transfer is plausible, but reviewed evidence does not yet establish a stable cross-resource variable with a defensive method independent of network-flow/C2 analysis. |
| T1496.003 SMS Pumping | Public form triggers, provider messaging transaction, per-message cost and revenue-share abuse | `niji-variable-candidate` | Contributes to provider-brokered metered consumption: the attacker's request causes a provider-side billable transaction under the victim's account. “SMS” is not imported as the child boundary. |
| T1496.004 Cloud Service Hijacking | SaaS messaging, LLM inference, service quota and cost | `niji-variable-candidate` | Contributes to provider-brokered metered consumption: execution and metering occur in the provider plane, outside host process sensors. “Cloud service” is not imported as a child. |

**Proposed Niji children:** (1) `TA0040-T1496-CHILD-ACTIVITY` Activity-Gated Residual-Capacity Consumption / 活动门控的剩余容量消耗 at `high` existence confidence; (2) `TA0040-T1496-CHILD-BROKERED` Provider-Brokered Metered Consumption / 提供方代理的计量资源消耗 at `medium` confidence. The two axes can coexist but remain distinguishable: the first requires a closed-loop activity signal that changes *when* resource use runs; the second requires provider-side execution and metering that changes *where* consumption is observed. Neither is defined by resource type, product, or monetization form.

**Breadth-gap explanation:** four ATT&CK resource categories converge to two Niji variables because compute/bandwidth/SMS/SaaS types do not by themselves change traces or defender observation. Compute supplies direct evidence for the temporal gate. SMS and hosted AI supply evidence for the provider-metered execution plane. Bandwidth remains parent-core; a possible attribution-transfer variable is deferred. A second taxonomy pass is not formally triggered for four ATT&CK children, but the open search above examined more than two independent axes as required.

## Proposed parent field content

**Name / 名称:** 资源劫持 / Resource Hijacking.

**Summary / 摘要:** 攻击者未经授权消耗受害方资源完成自身任务，并通过活动门控或提供方计量执行使消耗更像正常容量波动或合法服务交易。 / Adversaries consume victim resources for their own tasks and use activity gating or provider-metered execution to make the usage resemble normal capacity variation or legitimate service transactions.

### Definition and concept / 定义与概念

中文：资源劫持是攻击者在未获资源所有者授权的情况下，使用受控主机、容器、云账户、网络出口、消息平台或托管服务执行攻击者任务，从而消耗计算周期、带宽、消息额度、模型令牌、服务配额或费用预算。直接对象是可计量资源及其所有权，影响可以表现为费用上升、配额耗尽、性能下降、服务容量被挤占或受害身份承担外部滥用声誉。

English: Resource Hijacking is adversary use of a controlled host, container, cloud account, network egress, messaging platform, or managed service without the resource owner's authorization to perform an adversary task, consuming compute cycles, bandwidth, messages, model tokens, service quota, or spending budget. The direct object is a metered resource and its ownership. Impact can appear as cost growth, quota depletion, degraded performance, displaced capacity, or external abuse attributed to the victim identity.

中文：概念锚是主体或入口、实际消费动作、资源计量、预期 owner/用途以及费用、配额或可用性结果的完整链。挖矿、代理、短信、AI 和垃圾消息只是用途；同一资源可被不同用途劫持，同一用途也可跨本地进程与托管服务实现。Niji 只把有证据改变消耗时间包络或观察平面的实施方式正式化为子项。

English: The conceptual anchor is a complete chain among principal or entry point, actual consumption action, resource meter, expected owner and purpose, and cost, quota, or availability outcome. Mining, proxying, SMS, AI, and spam are uses rather than taxonomy units. One resource can serve multiple illicit uses, and one use can span local processes and managed services. Niji formalizes as children only implementations with evidenced changes to the consumption envelope or observation plane.

### Stealth characteristics / 匿迹特性

中文：持续满载矿工或突发消息滥用容易产生显著性能和账单峰值。攻击者可以读取用户空闲、GPU 使用或其他竞争负载，并只在剩余容量出现时启动消费者，让用户可感知的卡顿和忙时异常下降；也可以让云或通信提供方在受害账户下执行计量事务，使主机 EDR 看不到对应工作进程，生产侧只出现看似有效的 API 或表单请求。两种设计分别改变时间包络和执行观察面。

English: A continuously saturated miner or a burst of messaging abuse creates conspicuous performance and billing spikes. An adversary can read user idle state, GPU usage, or competing workload and run the consumer only when residual capacity appears, reducing user-visible slowdown and busy-period anomalies. The adversary can instead make a cloud or communications provider execute metered transactions under the victim account, leaving no corresponding worker process in host EDR and only apparently valid API or form requests on the production side. These designs change the time envelope and execution observation plane respectively.

中文：进程 lineage、CPU/GPU/网络计量、会话锁定与解锁、服务主体、请求 ID、目标号码、模型 ID、输入输出令牌、配额和费用仍可观察。长期 owner 基线、活动状态关联、按主体计量和服务端事务日志会缩小匿迹收益。合法后台批处理、自动扩缩容、夜间维护、OTP 峰值、营销活动和模型负载测试产生相似痕迹，必须用批准用途、资源 owner、转换结果和后继输出区分。

English: Process lineage, CPU/GPU/network meters, session lock and unlock, service principal, request ID, destination number, model ID, input/output tokens, quota, and cost remain observable. Long-term owner baselines, activity-state correlation, per-principal metering, and provider transaction logs reduce the stealth benefit. Legitimate background batches, autoscaling, overnight maintenance, OTP peaks, marketing campaigns, and model load tests create similar traces and require approved purpose, resource owner, conversion outcome, and successor output for separation.

### Scope boundary definition / 范围边界界定

中文：纳入攻击者实际使用受害方资源完成自身任务，并能证明消费、费用、配额或容量影响以及相应匿迹变量的行为。只创建实例、取得 shell、调用一次无成本探测 API、安装代理或保存凭据属于前置阶段；必须连接资源计量或服务交易。费用异常本身也不充分，需排除获批扩容、业务增长、价格变化和配置错误。

English: Include actual adversary use of victim resources for an adversary task when consumption, cost, quota, or capacity effect and the relevant stealth variable can be established. Instance creation, obtaining a shell, one non-billable probe, installing a proxy, or retaining credentials are precursor stages until joined to a resource meter or service transaction. Cost anomaly alone is also insufficient and requires exclusion of approved scaling, business growth, price changes, and configuration mistakes.

中文：工作负载执行、凭据取得、C2 和持久化保留各自对象。按低覆盖区域放置资源归 NJT-0121；选择性驱逐竞争恶意驻留归 NJT-0091；直接以耗尽或崩溃为目标归拒绝服务。资源种类、云厂商、矿池、消息产品、电话号码国家和收益方式均不能单独形成 NJS。

English: Workload execution, credential acquisition, C2, and persistence retain their own objects. Placement in a low-coverage Region belongs to NJT-0121; selective eviction of competing malicious footholds to NJT-0091; resource exhaustion or crash as the direct objective to denial of service. Resource type, cloud provider, mining pool, messaging product, destination country, and revenue form cannot independently define an NJS.

### Application scenarios / 应用场景

中文：在用户端点上，攻击者可部署 GPU/CPU 矿工并依据空闲输入、游戏或流媒体负载暂停和恢复，在用户不易感知的窗口消耗剩余容量。在云原生环境，攻击者可在已有容器、虚拟机或新实例运行矿工/代理。在托管服务环境，攻击者可使用窃取的云凭据调用模型推理，或通过公开 OTP 表单驱动消息提供方为攻击者控制的号码发送大量短信；受害方承担令牌、消息、配额和费用。

English: On an interactive endpoint, an adversary can deploy a GPU or CPU miner and pause or resume it according to idle input, gaming, or streaming load, consuming residual capacity during less noticeable windows. In cloud-native environments, the adversary can run miners or proxies in existing containers, VMs, or new instances. In managed services, stolen cloud credentials can invoke model inference, while a public OTP form can drive a messaging provider to send large volumes to attacker-controlled numbers; the victim bears tokens, messages, quota, and cost.

### Attacker model / 攻击方模型

中文：攻击者需要执行消费者进程或调用计量服务的权限、将收益或后继任务接回自身的控制路径，以及足够长的驻留或凭据有效期。活动门控还需可读取用户/负载状态并可靠暂停消费者；提供方计量消费需有效 API/表单入口、额度和可用服务。限额、短期凭据、强 owner 绑定、全区域审计、事务级速率限制和资源隔离会降低收益或暴露活动。

English: The adversary needs authority to execute a consumer process or invoke a metered service, a control path returning profit or downstream work, and sufficient foothold or credential lifetime. Activity gating additionally needs visibility into user or workload state and reliable pausing of the consumer. Provider-metered consumption needs a valid API or form entry point, quota, and enabled service. Limits, short-lived credentials, strong owner binding, all-Region audit, transaction-level rate control, and resource isolation reduce yield or expose the activity.

### Defender model / 防守方模型

中文：防守方可观察进程、资源性能计数、网络连接、用户会话状态、云身份与 API、提供方调用日志、令牌/消息使用、费用和配额。判断需要把资源计量映射到 owner、批准工作负载及请求来源，并在分钟级活动切换和日/周费用基线之间保持多尺度关联。只设“持续高 CPU”阈值会漏看活动门控，只看主机 EDR 会漏看提供方执行，只看月账单则发现过晚。

English: Defenders can observe processes, resource performance counters, network connections, user-session state, cloud identity and API, provider invocation logs, token or message use, cost, and quota. Assessment maps resource meters to owner, approved workload, and request origin and maintains multiscale correlation across minute-level activity transitions and daily or weekly spending baselines. A sustained-high-CPU threshold misses activity gating, host-only EDR misses provider execution, and monthly billing detects too late.

### Supported parent mechanisms

`TA0040-T1496-MECH-ACTIVITY` — `NM-ST`, primary. **Summary zh:** 消费被移动到空闲窗口并在竞争活动出现时收缩. **Summary en:** Consumption shifts into idle windows and contracts when competing activity appears. **Analysis zh:** 攻击者持续读取用户空闲或 GPU/业务负载，并在竞争活动出现时终止消费者、空闲恢复后重启。资源痕迹从持续高负载变为跨时间分散且与用户活动负相关的片段，局部阈值和用户体验难以还原完整消耗，形成时空释痕。长期活动—资源相关仍能揭示闭环。 **Analysis en:** The adversary continuously reads idle or GPU/business load and terminates the consumer when competing activity appears, restarting after idle returns. Resource traces change from sustained load to time-dispersed segments negatively correlated with user activity, making local thresholds and user experience less able to reconstruct total consumption and producing Spatiotemporal Trace Dilution. Long-horizon activity-to-resource correlation still reveals the loop. **Evidence:** E2. **Confidence:** `high` for the observed Windows/GPU case, `medium` across resource types.

`TA0040-T1496-MECH-BROKERED` — `NM-BT`, secondary. **Summary zh:** 提供方执行把消耗移出受害主机传感器. **Summary en:** Provider execution moves consumption outside victim host sensors. **Analysis zh:** 攻击者提交看似有效的模型、消息或验证请求，实际计算或发送由提供方完成并计入受害账户；主机进程和本地资源视图没有对应工作，防守方必须转向身份、服务调用和计量日志，形成行为透明。事务 ID、主体、目标、令牌/消息和费用仍能关联。 **Analysis en:** The adversary submits apparently valid model, messaging, or verification requests while the provider performs and meters the actual compute or delivery to the victim account. Host process and local-resource views contain no corresponding work, forcing defenders to identity, service-call, and metering logs and producing Behavioral Transparency. Transaction ID, principal, destination, tokens or messages, and cost remain joinable. **Evidence:** E3–E6. **Confidence:** `medium`; provider transaction semantics are high confidence, while the malicious cross-service Niji axis lacks one end-to-end named victim case.

### Parent taxonomy narrative / 父级分类叙述

中文：原生分类按攻击者改变的观察变量划分。活动门控的剩余容量消耗使用用户或工作负载状态闭环控制消费者启停，需要进程、性能和活动切换关联；提供方代理的计量资源消耗让外部提供方执行并计费，需要入口请求、服务主体、事务与用量/费用关联。前者改变“何时消耗”，后者改变“在哪里执行与观察”。资源类型和收益形式留在父级。

English: The native taxonomy separates the defender-observation variable changed by the adversary. Activity-Gated Residual-Capacity Consumption uses user or workload state in a closed loop to start and stop the consumer and requires process, performance, and activity-transition correlation. Provider-Brokered Metered Consumption has an external provider execute and meter the task and requires entry request, service principal, transaction, and usage or cost correlation. The former changes when consumption occurs; the latter changes where work executes and is observed. Resource and monetization forms remain parent-level implementations.

中文：两项可共现但边界可检验：没有活动反馈的低速矿工不属于第一项；本地主机发出的云 API 只有在工作由提供方执行并计入受害账户时属于第二项。低覆盖区域、可信进程伪装、竞争者驱逐和跨资产扩散由相邻技术或待证轴处理，不能用来补足子项数量。

English: The children can co-occur but have testable boundaries. A slow miner without activity feedback does not qualify for the first. A cloud API issued from a local host qualifies for the second only when the provider performs the work and meters it to the victim account. Low-coverage Region placement, trusted-process disguise, competitor eviction, and cross-asset spread remain adjacent or deferred and cannot be used to inflate child count.

## Proposed child `TA0040-T1496-CHILD-ACTIVITY`

**Name / 名称:** 活动门控的剩余容量消耗 / Activity-Gated Residual-Capacity Consumption. **Confidence:** `high` for existence; `medium` beyond interactive compute.

### Definition and concept / 定义与概念

中文：活动门控的剩余容量消耗是攻击者持续读取用户空闲、GPU/CPU 使用、前台应用或业务负载状态，并按该反馈自动暂停、终止、启动或恢复未授权资源消费者，只在剩余容量窗口执行攻击者任务。稳定变量是活动状态与消费启停之间的闭环，而不是平均利用率低、夜间运行或使用某种矿工。

English: Activity-Gated Residual-Capacity Consumption is continuous adversary reading of user idle state, GPU or CPU usage, foreground applications, or business load and automatic pausing, termination, start, or resume of an unauthorized resource consumer according to that feedback, running the adversary task only in residual-capacity windows. The stable variable is the closed loop between activity state and consumer transitions, not low average utilization, overnight execution, or a particular miner.

### Stealth characteristics / 匿迹特性

中文：活动门控的剩余容量消耗把持续资源占用改造成空闲期间上升、用户或业务活动出现时快速下降的片段。用户在交互时较少遇到卡顿，短窗高负载规则也可能只见间歇峰值；但资源曲线对锁定/解锁、输入空闲或 GPU 竞争事件的重复负相关、消费者进程启停、矿池连接及累计费用仍可恢复。

English: Activity-Gated Residual-Capacity Consumption changes sustained usage into segments that rise while idle and rapidly fall when user or business activity appears. Users experience less slowdown during interaction, and short-window high-load rules may see only intermittent peaks. Repeated negative correlation with lock/unlock, input idle, or GPU contention, consumer process transitions, mining-pool connections, and cumulative cost remain recoverable.

### Scope boundary definition / 范围边界界定

中文：纳入以可观测活动反馈控制未授权消费者启停的行为。普通低优先级任务、操作系统节能、获批空闲批处理、备份、索引和按需自动扩缩容是反例。固定定时或低 CPU 上限没有活动反馈时留在父级或其他时间调度对象；因分析工具出现而完全拒绝激活的行为可同时涉及执行护栏，但必须另证资源消费闭环。

English: Include unauthorized consumers whose transitions are controlled by observed activity feedback. Ordinary low-priority tasks, OS power management, approved idle-time batches, backup, indexing, and demand autoscaling are counterexamples. A fixed schedule or CPU cap without activity feedback remains parent-level or another scheduling object. Refusing all activation when an analysis tool appears can additionally involve execution guardrails, but the resource-consumption loop requires separate proof.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：Microsoft 2026 年观察到一条 GPU 挖矿链收集空闲秒数、持续 GPU 使用、游戏/流媒体状态和矿工状态，并每五秒检查；设备不空闲或 GPU 使用高时终止矿工，条件恢复后再编排挖矿。该案例直接支持活动门控，不代表所有矿工或所有剩余容量任务使用相同五秒周期。

English scenario: Microsoft observed a 2026 GPU-mining chain that collected idle seconds, sustained GPU use, gaming or streaming state, and miner state and checked every five seconds. It terminated miners when the device was not idle or GPU use was high and orchestrated mining when conditions returned. The case directly supports activity gating but does not establish the same five-second period for every miner or residual-capacity task.

中文攻击方：攻击者需要驻留代码、用户/负载活动传感、消费者进程控制和足以获利的空闲容量；还要避免频繁启停导致崩溃或明显事件。多人终端、headless 服务器、GPU 虚拟化和不可见工作负载会降低门控判断。活动状态日志、持续硬件计量和进程起止保留使闭环可追踪。

English attacker: The adversary needs resident code, a user or workload activity sensor, control over the consuming process, and enough idle capacity for yield, while avoiding crashes or conspicuous events from frequent transitions. Multi-user endpoints, headless servers, GPU virtualization, and invisible workloads reduce gating reliability. Activity-state logs, continuous hardware meters, and retained process transitions make the loop traceable.

中文防守方：防守方需要分钟级或更细的进程 CPU/GPU 指标、进程唯一身份、锁定/解锁或空闲状态及网络/费用累计，并保留至少覆盖多个活动周期的长窗。只采主机总 CPU 无法可靠归因进程；只在用户报障时采样则正好落入门控盲区。

English defender: The defender needs per-process CPU or GPU metrics at minute or finer resolution, stable process identity, lock/unlock or idle state, and cumulative network or cost data retained across multiple activity cycles. Host-total CPU alone cannot reliably attribute a process, and sampling only during user complaints lands directly in the gating blind spot.

### Supported mechanism and limitation

Mechanism is `TA0040-T1496-MECH-ACTIVITY` / `NM-ST` above, evidence E2, high for the observed case. **Limitation zh:** 单个锁定后负载上升不能证明恶意，门控者可读取并非审计的 GPU 状态或输入 API；防守分析必须验证同一消费者反复随活动转换并有未授权资源用途。Microsoft 案例还包含进程空洞、排除项、持久化和 C2，它们是相邻行为，不能当作子项边界。 **Limitation en:** One post-lock load increase does not prove maliciousness, and the gate can read GPU state or input APIs not audited by defenders. Detection must establish repeated same-consumer transitions with activity and unauthorized resource purpose. The Microsoft case also includes process hollowing, exclusions, persistence, and C2; these are adjacent behaviors rather than child boundaries.

## Proposed child `TA0040-T1496-CHILD-BROKERED`

**Name / 名称:** 提供方代理的计量资源消耗 / Provider-Brokered Metered Consumption. **Confidence:** `medium`; Bedrock/Twilio execution and metering semantics are directly documented, while the cross-service malicious axis has no single end-to-end named victim case.

### Definition and concept / 定义与概念

中文：提供方代理的计量资源消耗是攻击者通过受害方账户、API 密钥或公开业务入口提交请求，由外部托管服务实际执行计算、消息、通信或其他资源任务，并将用量、配额或费用计入受害方。稳定变量是消费者执行位置从受害主机移至提供方数据面，而受害环境主要保留身份、入口请求和计量记录。

English: Provider-Brokered Metered Consumption is adversary submission of requests through a victim account, API key, or public business entry point while an external managed service performs the compute, messaging, communications, or other resource task and meters usage, quota, or cost to the victim. The stable variable is movement of consumer execution from the victim host to the provider data plane, leaving primarily identity, entry request, and metering records in the victim environment.

### Stealth characteristics / 匿迹特性

中文：提供方代理的计量资源消耗不会在受害主机产生与令牌生成、短信发送或 SaaS 批处理等量的本地 CPU/进程痕迹。攻击可借有效身份或正常 OTP 表单呈现为合法业务交易，主机监测和局部应用日志只能看见入口。服务调用日志、主体 ARN/SID、请求 ID、目标号码、转换率、模型令牌、调用次数、配额与费用仍可将入口和消费结果连接。

English: Provider-Brokered Metered Consumption does not create local CPU or process traces on the victim host proportional to token generation, SMS delivery, or SaaS batch work. Valid identities or ordinary OTP forms can make the requests appear to be legitimate business transactions, leaving host monitoring and local application logs with only the entry point. Service invocation logs, principal ARN or SID, request ID, destination number, conversion rate, model tokens, invocation count, quota, and cost can still join entry to consumption outcome.

### Scope boundary definition / 范围边界界定

中文：纳入提供方实际执行且计入受害账户的未授权计量事务。仅探测服务是否启用、查询配额、窃取密钥或调用无计费错误请求是前置活动；必须出现服务用量或攻击者任务结果。正常 AI 应用、验证码、营销消息、负载测试和获批批处理是反例。若工作在受害 VM/容器内执行，应归父级或活动门控子项，而不是因为它位于“云”中就归本项。

English: Include unauthorized metered transactions actually executed by a provider and charged or counted to the victim account. Probing service enablement, reading quota, stealing a key, or making a non-billable error request is precursor activity until service use or adversary-task output occurs. Normal AI applications, verification messages, marketing, load tests, and approved batches are counterexamples. Work executed inside a victim VM or container remains parent-level or activity-gated and does not enter this child merely because it is “cloud.”

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：Sysdig 观察到攻击者用窃取的云凭据探测十种托管 LLM 服务、检查日志配置，并使用与 OAI Reverse Proxy 相符的 user-agent 尝试调用模型；反向代理可把被盗账户资源转售给第三方，而账户所有者承担费用。SMS pumping 中，攻击者反复提交公开 OTP/验证入口，使 Twilio 等提供方向其号码集合发送短信；服务端 `sid`、`to`、`conversionStatus` 与费用字段记录交易。

English scenario: Sysdig observed actors using stolen cloud credentials to test ten hosted LLM services, query logging configuration, and attempt model calls with a user-agent matching OAI Reverse Proxy. A reverse proxy can resell the compromised account's resources to third parties while the account owner pays. In SMS pumping, an adversary repeatedly submits a public OTP or verification entry point, causing a provider such as Twilio to send messages to an attacker-controlled number set; provider `sid`, `to`, `conversionStatus`, and price fields record the transaction.

中文攻击方：攻击者需要可调用服务的凭据或可自动化公开入口、可用额度和把结果返回自身的代理/号码/任务链。共享角色、长效 API 密钥、无请求 owner 标签、宽松 OTP 限流及默认关闭的详细调用日志增加成功率。短期身份、逐应用凭据、提供方限速、预算和强制事务日志会限制。

English attacker: The adversary needs service-call credentials or an automatable public entry point, available quota, and a proxy, number set, or task chain returning results. Shared roles, long-lived API keys, absent request-owner tags, weak OTP rate limits, and detailed invocation logging disabled by default improve success. Short-lived identity, per-application credentials, provider rate control, budgets, and mandatory transaction logging constrain it.

中文防守方：防守方需要把入口请求、云/服务身份、提供方事务、计量单位和成本统一到一个 owner。Bedrock 调用日志提供 `identity.arn`、`requestId`、`modelId` 及输入输出令牌；Twilio Verify 提供 `sid`、`to`、`conversionStatus`、`channel` 及时间。共享身份、未启用调用日志、跨区域服务、提供方日志延迟和无法取得公开入口来源 IP 时形成盲区。

English defender: The defender needs to unify entry request, cloud or service identity, provider transaction, metered unit, and cost under one owner. Bedrock invocation logs provide `identity.arn`, `requestId`, `modelId`, and input/output token counts. Twilio Verify supplies `sid`, `to`, `conversionStatus`, `channel`, and time. Shared identities, disabled invocation logging, cross-Region service, provider-log delay, and missing public-entry source IP create blind spots.

### Supported mechanism and limitation

Mechanism is `TA0040-T1496-MECH-BROKERED` / `NM-BT` above. **Limitation zh:** Sysdig 的 2024 观察直接证明凭据探测、日志配置查询和模型调用尝试，并以成本模型说明潜在费用；其当时验证阶段未运行合法业务查询，不能把估算的每日费用写成已结算损失。Twilio 文档证明日志和 pumping 模式，但不是命名受害事件。不同提供方只有验证计量字段和日志覆盖后才能加入。 **Limitation en:** Sysdig's 2024 observation directly establishes credential testing, logging-configuration inquiry, and attempted model invocation and models potential cost; no legitimate model queries ran during the verification phase, so estimated daily cost cannot be stated as settled victim loss. Twilio documents logs and pumping patterns but is not a named victim event. Other providers require verified metering fields and log coverage before inclusion.

## Detection and analytic candidates

### `TA0040-T1496-DET-ACTIVITY` — Activity-State to Resource-Consumer Correlation / 活动状态到资源消费者关联

**Objective:** detect a process whose resource consumption repeatedly expands in idle/residual windows and contracts on user or workload activity, targeting the parent and activity-gated child.

#### `TA0040-T1496-NJA-ACTIVITY-WINDOWS`

**Logic:** Collect Windows/Azure Monitor `Perf` samples for `Process` or `Process V2` `% Processor Time` and `ID Process` at one-minute resolution. Use `TimeGenerated`, `Computer`, `_ResourceId`, `ObjectName`, `CounterName`, `InstanceName`, `CounterValue`, and `CounterPath` to map utilization to a PID, then join MDE `DeviceProcessEvents` on device, PID and creation time/`ProcessUniqueId`, preserving `FileName`, `FolderPath`, `ProcessCommandLine`, `AccountSid`, `SHA1`, `InitiatingProcessUniqueId`, and signer metadata. Add Security 4800/4801 or 4802/4803 with `TimeCreated`, `Computer`, `SubjectUserSid`, `LogonId`, and `SessionId`, or an approved session-specific idle sensor based on `GetLastInputInfo`. Optional GPU-engine telemetry must expose device, timestamp, PID/engine, and utilization; do not pretend Azure `Perf` supplies it when not collected.

Build per-process one-minute utilization series. In a rolling 24-hour investigation horizon, identify repeated transitions where the same process rises after lock/idle and drops or terminates within a locally tuned interval after unlock/user/GPU activity, then resumes in a later idle window. Require at least several cycles as an environment-tuned hypothesis and compare the process, owner, schedule, and resource curve to approved idle jobs. Join optional `DeviceNetworkEvents` through `InitiatingProcessUniqueId` for persistent mining/proxy destinations and accumulate daily CPU/GPU time; a mining-pool indicator raises confidence but is not mandatory.

**Correlation:** event-to-performance 1–2 minutes; transition pairing 10 minutes around activity change; behavior horizon 24 hours and baseline 30 days. Dimensions: device/resource ID, process unique ID or PID+creation time, session/logon ID, account SID, executable hash, resource counter, destination.

**Observables:** repeated negative correlation between interactive activity and the same consumer; unfamiliar process consuming only while idle; consumer termination at analysis/user processes and later recreation; cumulative off-hours usage inconsistent with owner baseline.

**False positives:** approved idle maintenance, antivirus scan, search indexing, backup, software compilation, render jobs, distributed-compute clients, GPU driver behavior, power management, and scheduled batch workloads.

**Blind spots:** 4800/4801 auditing disabled by default, no idle or GPU telemetry, PID reuse without process-start key, multi-session hosts, headless servers, consumer hidden in a trusted/hollowed process, resource use below sampling resolution, and workload feedback not based on user state.

**Tuning:** register approved idle jobs with owner, executable hash/path, schedule, expected counter range and destinations. Do not globally allow signed/system processes because the observed case used hollowed Microsoft-signed utilities. Tune transition count and interval per device role; preserve low-confidence cumulative-use anomalies on servers where user-state gating is inapplicable. **Evidence:** E2, E7–E10; reuse REF-000598 and REF-000604 for MDE schema fields.

### `TA0040-T1496-DET-BROKERED` — Entry-to-Provider Meter and Cost Attribution / 入口到提供方计量与费用归因

**Objective:** detect provider-executed resource transactions that lack an approved application owner, targeting the parent and provider-brokered child. Use distinct service analytics; provider fields are not interchangeable.

#### `TA0040-T1496-NJA-BEDROCK`

**Logic:** Enable Amazon Bedrock model invocation logging per Region and collect JSON fields `timestamp`, `accountId`, `region`, `requestId`, `operation`, `modelId`, `identity.arn`, `requestMetadata`, `input.inputTokenCount`, and `output.outputTokenCount`. Join CloudTrail by request/principal/time to `eventName`, `userIdentity.arn`, `accessKeyId`, `sourceIPAddress`, `userAgent`, `awsRegion`, `requestParameters.modelId`, `errorCode`, and `eventID`, including prior `GetModelInvocationLoggingConfiguration` and access-probe calls. Aggregate calls and tokens by principal, application/inference profile, model and Region over 15 minutes and 24 hours; compare approved principal-source-user-agent-model tuples and daily token/cost budgets. Flag sustained metered use from a new origin or reverse-proxy user-agent, missing owner metadata, unexpected model/Region, or a new service enablement followed by consumption. Treat a ValidationException probe as reconnaissance until successful token use appears.

**Correlation:** CloudTrail-to-invocation ±5 minutes and request ID where available; burst 15 minutes; owner/cost horizon 24 hours; 30-day principal/model baseline. Dimensions: account, Region, identity ARN/session, access key, source IP, user-agent, request ID, model ID, application profile/request metadata.

**False positives:** new AI application release, load/performance test, batch inference, cross-Region failover, model migration, shared developer role, and approved proxy gateway.

**Blind spots:** invocation logging disabled by default, unsupported endpoints (for example documented `bedrock-mantle` differences), prompt bodies absent from CloudTrail, shared roles obscuring end users, cost data delayed, cross-account proxy, or malicious use within a high-volume approved application.

**Tuning:** require per-application inference profiles or request metadata where supported, short-lived roles, owner registry, allowed source networks/user-agents, and separate budgets by principal/model. Never suppress a shared production role globally; retain source/user-agent and model deltas. Use CloudWatch `Invocations`, `InputTokenCount`, and `OutputTokenCount` for account/model totals when detailed logs are unavailable, while marking lost principal attribution. **Evidence:** E3, E5, E6, E11, E12; reuse REF-000524 for generic CloudTrail fields.

#### `TA0040-T1496-NJA-TWILIO-VERIFY`

**Logic:** Join the public application's OTP/verification request log (`timestamp`, request ID, source IP, user-agent, account/session or device identifier, endpoint, requested destination) to Twilio Verify attempts by `sid`/application transaction mapping and time. Consume Twilio fields `sid`, `accountSid`, `serviceSid`, `dateCreated`, `dateUpdated`, `to`, `channel`, `conversionStatus`, status/intervention where available, plus country derived from E.164 and pricing/message status where the corresponding product log provides it. Over a 5-minute rolling window and 24-hour cost horizon, compare request rate, distinct destinations, sequential/high-cost prefixes, unconverted ratio, source-to-destination fan-out and provider blocks with endpoint and campaign baseline. A high request count without a provider transaction is an application abuse attempt; completed/provider-metered sends establish resource consumption.

**Correlation:** entry request to provider transaction 2 minutes; abuse burst 5 minutes; conversion/cost outcome 24 hours. Dimensions: application, endpoint, source IP/device/session, request ID, Verify `sid`, service/account SID, destination prefix/country, channel, time.

**False positives:** customer sign-in spikes, product launch, incident-driven reauthentication, travel, marketing/notification campaign mistakenly using Verify, QA/load tests, and carrier delivery failures.

**Blind spots:** application does not preserve request-to-Verify mapping, source IP lost behind CDN without trusted forwarded fields, distributed bot sources, provider log delay, numbers distributed across countries, legitimate conversion occurs, or another SMS provider exposes different fields.

**Tuning:** rate-limit by source/device/account and destination prefix rather than one global total; maintain expected conversion and country-cost baselines per endpoint; never whitelist a high-volume public endpoint without conversion analysis. **Evidence:** E4 and E13.

## Mitigation candidates

### `TA0040-T1496-MIT-OWNERSHIP` — Resource Ownership, Quota, and Independent Metering / 资源所有权、限额与独立计量

**Measures:** (1) assign every compute/network/messaging/AI resource and credential an owner, approved purpose, budget/quota, Region, and expiry; (2) enforce per-workload or per-principal CPU, GPU, network, message, token and spending bounds where the platform supports them; (3) collect usage independently of the workload and automate containment when unowned consumption exceeds a tuned bound; (4) separate production identities from billing/usage review and preserve daily cost anomaly root causes.

**Parent application:** inventory metered resources across host, container, cloud and SaaS planes, deny unowned service enablement and quota changes, and join usage/cost to owner before allowing continued consumption. Expected effect: limits yield and converts unidentified consumption into an actionable owner violation. Limitations: low-rate theft can stay within caps; billing is delayed; a compromised approved owner may remain under budget; strict quotas can impair legitimate bursts.

### `TA0040-T1496-MIT-ACTIVITY` — Interactive Endpoint Compute Authorization and Residual-Capacity Limits / 交互端计算授权与剩余容量限制

**Measures/application for activity child:** enforce application control and EDR protections on interactive endpoints, protect Defender exclusions and process integrity, deny unapproved persistent miners, restrict mining/proxy egress, and set process/container/job resource caps where available. Maintain an approved idle-job registry and investigate consumers that repeatedly track activity state. Expected effect: blocks common consumer launch or limits yield even when it gates itself, while making ownerless idle use distinguishable. Limitations: trusted signed tools or process hollowing can bypass simple path allowlists, resource caps do not establish intent, mining pools can use relays, and user endpoints still need legitimate maintenance.

### `TA0040-T1496-MIT-BROKERED` — Metered-Service Least Privilege and Transaction Admission / 计量服务最小权限与事务准入

**Measures/application for provider child:** use short-lived, per-application identities and keys; deny unused AI/messaging services and model access; require application inference profiles or request owner metadata; enable invocation and provider transaction logs in every allowed Region; apply per-principal token/message quotas and budget alarms; protect public OTP endpoints with server-side rate limits, device/account controls, destination-risk checks, provider Fraud Guard and a bot challenge such as CAPTCHA. Expected effect: prevents broad shared credentials or public forms from silently converting requests into victim-paid service work and bounds residual cost. Limitations: CAPTCHA and rate limits can be bypassed by distributed human-like traffic; valid compromised applications may remain within normal volume; detailed model logging can contain sensitive prompts and requires protected retention; budgets may alert after spend.

**Shared-library resolution:** MIT-000119 is adjacent only; its identity is Region allowlisting and all-Region observability for NJT-0121, so use it when a T1496 event also exploits a low-coverage Region but do not extend it as the resource-consumption mitigation. MIT-000140 protects cloud protection-state read authority and is not a usage/quota control. New mitigation candidates are required unless the primary agent finds exact semantic matches after all batch handoffs.

## Evidence and conclusion-level sources

| Key | Primary source and locator | Support and limit |
|---|---|---|
| E1 `TA0040-T1496-REF-ATTACK` | [MITRE ATT&CK Enterprise v19 T1496](https://attack.mitre.org/versions/v19/techniques/T1496/) and fixed 19.1 STIX inventory | Parent behavior/tactic, four-child planning breadth; does not establish Niji taxonomy. New REF. |
| E1a–d `TA0040-T1496-REF-ATTACK-CHILD-*` | Versioned [T1496.001](https://attack.mitre.org/versions/v19/techniques/T1496/001/), [.002](https://attack.mitre.org/versions/v19/techniques/T1496/002/), [.003](https://attack.mitre.org/versions/v19/techniques/T1496/003/), [.004](https://attack.mitre.org/versions/v19/techniques/T1496/004/) | Planning-only implementation clusters and coverage resolutions; never imported as NJS. New REF candidates or retain only in handoff if parent REF suffices. |
| E2 `TA0040-T1496-REF-MS-ACTIVITY-GATED` | [Microsoft: From poisoned search results to GPU mining](https://www.microsoft.com/en-us/security/blog/2026/05/26/poisoned-search-results-gpu-mining-cryptojacking-campaign-abusing-screenconnect-microsoft-net-utilities/), Host reconnaissance and Mining orchestration/activity tracking | Direct observed activity-gated miner, idle seconds, GPU load, process termination. New REF and CASE candidate. |
| E3 `TA0040-T1496-REF-SYSDIG-LLMJACKING` | [Sysdig: LLMjacking—Stolen Cloud Credentials Used in New AI Attack](https://www.sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack), Breadth, reverse proxy, InvokeModel/CloudTrail, logging-configuration sections | Observed credential/service probes, proxy user-agent and attempted use; modeled $46k/day is potential, not realized loss. New REF and CASE candidate. |
| E4 `TA0040-T1496-REF-TWILIO-FRAUD-LOGS` | [Twilio: Analyze—Investigate](https://www.twilio.com/docs/usage/fraud-response-guide/analyze), Verify Logs and field tables | Exact Verify/message fields and SMS-pumping patterns; documentation, not named victim case. New REF. |
| E5 `TA0040-T1496-REF-BEDROCK-INVOCATION-LOG` | [AWS Bedrock model invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html), supported operations and log-entry schema | Exact principal/request/model/token fields; logging disabled by default and endpoint limits. New REF. |
| E6 `TA0040-T1496-REF-BEDROCK-METRICS` | [AWS Bedrock runtime metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-runtime-metrics.html), runtime metric table | Invocation and token totals; metric dimensions may lack principal attribution. New REF. |
| E7 `TA0040-T1496-REF-AZURE-PERF` | [Azure Monitor Perf table](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/perf) and [queries](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/queries/perf) | Exact performance-counter fields and one-minute/15-minute examples; mapping to process requires collected process counters. New REF. |
| E8 `REF-000598` | [MDE DeviceProcessEvents schema](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table) | Exact process identity/lineage fields. Reuse. |
| E9 `TA0040-T1496-REF-WINDOWS-ACTIVITY` | [Microsoft advanced audit policy](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/advanced-audit-policy-configuration) and [GetLastInputInfo](https://learn.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-getlastinputinfo) | Lock/unlock events and session-specific idle API semantics; auditing defaults/limitations. New REF(s). |
| E10 `REF-000604` | [MDE DeviceNetworkEvents schema](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkevents-table) | Process-linked network fields. Reuse. |
| E11 `REF-000524` | [AWS CloudTrail record fields](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html) | Generic principal/source/request/error fields. Reuse. |
| E12 `TA0040-T1496-REF-AWS-COST-ANOMALY` | [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/getting-started-ad.html), root cause and impact fields | Account/Region/service/usage-type and expected/actual spend; delayed cost is detective support. New REF. |
| E13 `TA0040-T1496-REF-ATTACK-SMS-DET` | [ATT&CK DET0156](https://attack.mitre.org/detectionstrategies/DET0156/) | Provider/application SMS detection dimensions and tunable fields; ATT&CK detection design, not child evidence. New REF. |
| E14 `TA0040-T1496-REF-SYSDIG-LABRAT` | [Sysdig/CSA LABRAT report](https://cloudsecurityalliance.org/blog/2023/12/04/labrat-stealthy-cryptojacking-and-proxyjacking-campaign-targeting-gitlab) | Same actor deploys cryptomining and proxyjacking; stealth components belong adjacent techniques and do not create resource-type NJS. New REF and optional parent CASE. |

## Shared-library lookup and reuse record

Executed `library_lookup.py` with: `resource hijacking`; `cryptojacking CPU idle GPU activity`; `LLMjacking Sysdig InvokeModel`; `SMS pumping Twilio Verify`; `proxyjacking bandwidth`; `Azure Monitor Perf table CPU`; `Microsoft GPU cryptojacking idle`; and `metered cloud service usage billing`. Direct URL search found no canonical source matching E1–E7, E9, E12–E14.

- **Reference reuse:** reuse `REF-000598` for MDE process fields, `REF-000604` for process-linked network fields, and `REF-000524` for generic CloudTrail record fields. `REF-000219`/CASE-000074 concern Kubernetes `exec` execution lineage and do not by themselves prove a resource meter or stealth axis; do not extend solely because the report title mentions cryptojacking. `REF-000237`/CASE-000082 similarly prove miner activation via COR_PROFILER and remain useful execution context, but do not replace E2's activity-gate evidence.
- **Case candidates:** create `TA0040-T1496-CASE-MS-ACTIVITY-GATED` from E2. E3 can support `TA0040-T1496-CASE-SYSDIG-LLM-ACCESS-PROBE` only as a credential/service-probe precursor; it must not be presented as realized metered consumption because no legitimate model query ran in the verification phase. Optional `TA0040-T1496-CASE-LABRAT-MULTIRESOURCE` from E14 supports parent co-use of compute and bandwidth, not either child. There is no qualified provider-brokered child CASE in this handoff. Do not extend CASE-000074 or CASE-000082 unless primary review confirms their existing central facts already include measured unauthorized resource consumption.
- **Claim candidates:** `TA0040-T1496-CLM-PARENT` (unauthorized metered resource use and impact; E1/E14); `TA0040-T1496-CLM-ACTIVITY-GATE` (consumer stops when device active/GPU busy and resumes under idle orchestration; E2); `TA0040-T1496-CLM-BROKERED-LLM` (stolen cloud identity invokes provider models while victim pays; E3); `TA0040-T1496-CLM-BROKERED-SMS` (public verification entry drives provider-metered SMS and low conversion; E4); `TA0040-T1496-CLM-ENDPOINT-FIELDS` (E7–E10); `TA0040-T1496-CLM-BEDROCK-FIELDS` (E5/E6/E11); `TA0040-T1496-CLM-COST-LIMIT` (cost anomaly root causes lag the underlying transaction; E12).
- **Detection reuse:** DET-000118/NJA-000106/NJA-000127 detect Region placement and control asymmetry for NJT-0121; they may co-cover one incident but do not detect ownerless consumption or activity gating. DET-000151/NJA-000159 detect GuardDuty state inquiries, not metered service use. No exact DET/NJA match exists; create the two strategies and three analytics proposed above.
- **Mitigation reuse:** MIT-000119 applies when Region choice is also present but its measures cannot substitute for resource quotas, per-principal metering, or transaction admission. MIT-000140 governs protection-state reads. No exact mitigation identity matched; create target-specific candidates and let the primary agent decide whether parent-wide ownership and child-specific controls remain separate objects.
- **Duplicate governance:** resource type, miner/proxy name, cloud provider, monetization, and destination geography do not justify new shared objects. Every candidate must resolve centrally as create/split/defer after the other batch handoffs.

## Rejected and deferred axes

| Axis | Resolution | Reason |
|---|---|---|
| Cross-node/account dilution of small consumers | `evidence-deferred` | Spatial dilution is plausible NM-ST, but reviewed reports show spread for scale and access, not conclusion-level intentional per-node threshold evasion with a distinct defense. |
| Victim IP / reputation attribution transfer | `evidence-deferred` | Proxyjacking can burden victim identity, but evidence reviewed here does not yet separate a stable T1496 child from bandwidth flow, proxy/C2 and abuse-attribution controls. |
| Low-coverage Region selection | `adjacent-technique` | Fully owned by NJT-0121; T1496 records consumption outcome only. |
| Trusted binary/process identity or rootkit hiding CPU | `adjacent-technique` | Process injection, artifact visibility reshaping, or identity disguise owns the hiding method; resource use remains T1496. |
| Competitor miner termination | `adjacent-technique` | NJT-0091 owns selective competing-foothold eviction; T1496 owns subsequent consumption. |
| Quota increase before consumption | `parent-core/precursor` | A capacity policy change can enable more consumption but is not resource use until metered work occurs; policy-change technique may also apply. |
| Fixed low CPU limit or nighttime schedule | `not-stealth-distinct` unless feedback exists | Rate or time alone lacks the closed-loop activity variable and may be ordinary scheduling. |

## Research and content-depth limitations

中文：Microsoft 案例对活动门控提供高质量在野证据，但仅直接证明 Windows 交互终端上的 GPU 挖矿；扩展到 CPU、带宽或服务器业务负载必须降低置信度。Sysdig 直接观察凭据探测、日志配置查询和模型调用尝试，并发现反向代理线索，但其 2024 验证阶段没有运行合法业务模型查询，潜在每日费用不是已发生损失。Twilio 文档给出可实施字段和 pumping 模式，不构成独立受害案例。账单、配额和性能异常都可能由正常增长产生，必须恢复 owner、批准用途和实际交易。

English: Microsoft's case provides strong field evidence for activity gating but directly establishes only GPU mining on interactive Windows endpoints; extension to CPU, bandwidth, or server workload requires lower confidence. Sysdig directly observed credential testing, logging-configuration inquiry, attempted model use, and reverse-proxy evidence, but no legitimate model queries ran during the 2024 verification phase and potential daily cost is not realized loss. Twilio provides implementable fields and pumping patterns rather than a victim case. Billing, quota, and performance anomalies can all arise from normal growth and require owner, approved purpose, and actual transaction recovery.

Compared with NJT-0001 by field responsibility, the parent and both children each define direct behavior, stable stealth variable, trace change, defender-observation difference, residual evidence, inclusion/exclusion, scenario, attacker prerequisites, defender visibility, mechanism, evidence strength, and limitations. The endpoint, Bedrock, and Twilio analytics use distinct real fields, windows, false positives, and blind spots. Formal prose must remain candidate-specific during primary integration.

**Integration status:** pending all five handoffs, primary cross-technique convergence, shared-library duplicate resolution, formal ID allocation, YAML authoring, quality/build/Web QA, and human review. Only this staging handoff was written.
