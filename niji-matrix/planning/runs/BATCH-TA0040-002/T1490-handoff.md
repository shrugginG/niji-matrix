# T1490 research handoff — BATCH-TA0040-002

Research staging only. Every proposed new object uses the `TA0040-T1490-` prefix. This handoff allocates no formal ID and changes no canonical decision, matrix object, shared library, tactic plan, batch brief, or integration summary.

## Admission recommendation

**Candidate:** ATT&CK Enterprise 19.1 T1490, Inhibit System Recovery / 抑制系统恢复. **Recommendation:** `adapt`. **Parent confidence:** `high`. **ATT&CK child inventory:** zero. `original_attack_subtechniques_imported: false`.

**准入理由（中文）：** ATT&CK T1490 直接描述攻击者删除恢复副本、快照或备份目录，关闭恢复功能，或更改备份与版本策略，使受害组织在后续数据破坏、加密或系统故障后无法按预期恢复。该行为明确服务于 Impact，且大量勒索软件和破坏行动已观察到删除卷影副本、禁用 WinRE 或移除备份。Niji 应保留这一直接对象，但将范围改写为“恢复链能力状态被攻击者削弱，而生产数据与业务健康视图可以暂时保持不变”。这种延迟显现使仅观察当前业务可用性或生产端点的防守方无法及时判断真实恢复能力，形成候选自身的匿迹问题。

**Admission rationale (English):** ATT&CK T1490 directly covers adversary deletion of recovery copies, snapshots, or backup catalogs, disabling recovery functions, and changes to backup or version policy that deny expected restoration after later data destruction, encryption, or system failure. The behavior clearly serves Impact, and ransomware and destructive operations have repeatedly been observed deleting shadow copies, disabling WinRE, or removing backups. Niji should retain the direct object while adapting the scope to adversary degradation of recovery-chain capability whose production data and current business-health view can remain apparently normal. That delayed manifestation leaves defenders who observe only present availability or production endpoints unable to assess actual recoverability promptly.

**Scope notes / 范围说明:** The direct object is the capability chain used to restore: recovery points, snapshots, backup catalogs, recovery configuration, recovery keys, protected copies, and the authority or dependency needed to use them. The parent completes when the expected restore path is materially reduced or lost; a present production outage is not required. A recovery-control change without proven loss is a pre-impact attempt until state or policy outcome confirms impairment.

中文：直接对象是恢复所依赖的能力链，包括恢复点、快照、备份目录、恢复配置、恢复密钥、受保护副本及使用它们所需的权限或依赖。预期恢复路径被实质缩小或消失时父行为成立；当前生产业务不必已经中断。只有恢复控制变更而未核实能力状态时，应先记为事前企图，不能直接声称恢复已经失败。

## Mandatory adjacent boundaries

- **NJT-0156 Data Destruction / 数据销毁:** 删除同一技术对象时，按对象的业务角色划界。删除当前业务文件、对象或有效内容并使当前用途丧失归 NJT-0156；删除为故障后恢复而保留的独立副本、快照或恢复点归 T1490。一个 `DeleteObject`、文件删除或生命周期事件本身不决定归类。 / When the same deletion verb is used, classify by the object's business role. Loss of current business files, objects, or useful content belongs to NJT-0156; deletion of an independent copy, snapshot, or recovery point retained for post-failure restoration belongs to T1490. A `DeleteObject`, file deletion, or lifecycle event alone does not decide the classification.
- **NJT-0157 Data Encrypted for Impact / 为影响而加密数据:** 加密生产数据并以密钥控制阻止当前读取归 NJT-0157；加密只用于恢复的备份或快照、撤销其恢复密钥，且直接结果是恢复路径失效时归 T1490。两者可以共现，必须分别保存生产数据状态和恢复点状态。 / Encryption of production data that denies current reading through key custody belongs to NJT-0157. Encryption of recovery-only backups or snapshots, or loss of their restore keys, belongs to T1490 when the direct result is a failed restore path. Both can co-occur and require separate production-data and recovery-point state.
- **Backup-product defensive impairment / 备份产品防御损伤:** 停止备份代理、关闭产品告警、删除安全日志或破坏备份产品的检测能力，而现有恢复点及恢复权限仍可用，属于 TA0112 防御损伤或相应服务停止边界。只有这些动作实际移除、阻断或使预期恢复链不可用时，才同时形成 T1490；不能用产品名称或服务停止自动推断恢复点损失。 / Stopping a backup agent, suppressing product alerts, deleting security logs, or impairing a backup product's detection while existing recovery points and restore authority remain usable belongs to TA0112 defense impairment or the applicable service-stop boundary. T1490 additionally applies only when the action removes, blocks, or makes the expected restore chain unusable; product names and stopped services do not prove recovery-point loss.
- **Current business outage / 当前业务中断:** T1490 can be completed while production remains healthy; the impact becomes visible when restoration is needed or a recovery assurance check fails. If the action itself stops a business service, shuts down a host, or destroys current data, record the corresponding Impact technique independently. Do not treat later outage severity as evidence of the original stealth mechanism.

## Taxonomy breadth review

The fixed ATT&CK 19.1 inventory has no T1490 sub-techniques. Open-ended Niji research nevertheless examined: direct recovery-point deletion; policy-driven delayed expiration; disabling recovery software or alerts; use of native utilities; cross-account or cross-region recovery targeting; gradual deletion; selective retention of decoy recovery points; recovery-key revocation; and corruption that appears as a successful backup. Product, platform, artifact type, and command name were rejected as taxonomy keys.

**Provisional result:** one Niji-native child candidate, `TA0040-T1490-CHILD-DEFERRED`, **Deferred Policy-Driven Recovery Expiration / 策略驱动的延迟恢复点到期**, at `medium` confidence. Its stable variable is the separation of the adversary's policy decision from later service execution across time, identity, and telemetry plane. Direct deletion, recovery-feature disablement, and loss of restore keys remain parent-core because current evidence does not establish a second stable stealth partition with a distinct defensive method.

**Zero-child rule:** zero children is not the current recommendation. If primary review requires a named victim incident for formal child admission, defer this child and set the parent taxonomy to `deferred`, not `none-justified`: AWS documentation and Mandiant defensive guidance establish a plausible, observable variable, but public reporting does not trace one named victim from a malicious retention update through service expiration to failed restoration. Do not manufacture a CASE to promote confidence.

### Axis resolutions

| Examined axis | Resolution | Reason |
|---|---|---|
| Direct shadow-copy, snapshot, catalog, or recovery-point deletion | `parent-core` | Direct behavior; artifact type and utility do not create a stealth partition. |
| Policy or lifecycle change followed by service expiration | `niji-variable-candidate` | Separates initiating actor from later recovery-point loss across time, identity, and telemetry plane. |
| Stop backup agent, suppress backup alerts, delete product logs | `adjacent-technique` | Defense impairment unless recovery capability itself becomes unavailable; notification suppression is not a T1490 child. |
| Native `vssadmin`, `wbadmin`, `bcdedit`, `wmic`, or service API | `not-stealth-distinct` | Tool legitimacy alone does not prove changed defender observation and overlaps system-utility proxying. |
| Shadow copy, cloud snapshot, ESXi snapshot, firmware image | `not-stealth-distinct` | Platform and recovery-artifact types are implementation dimensions. |
| Cross-account or cross-region deletion | `evidence-deferred` | Could alter correlation scope, but evidence reviewed here does not establish a stable adversary design and distinct trace effect. |
| Slow deletion below thresholds | `evidence-deferred` | No conclusion-level source establishes deliberate T1490 pacing and a distinct detection window. |
| Leave decoy recovery points while removing usable dependencies | `evidence-deferred` | Plausible state divergence but no observed technical case and field-level evidence. |
| Corrupt a backup while job status remains successful | `evidence-deferred` | High-value hypothesis; current sources recommend restore testing but do not establish an attacker-controlled successful-status trace. |
| Revoke or lose recovery keys | `parent-core` | Direct recovery-chain impairment; more evidence is needed before a trace-distinct key-state child. |

## Proposed parent field content

**Name / 名称:** 抑制系统恢复 / Inhibit System Recovery.

**Summary / 摘要:** 攻击者削弱恢复副本、配置、密钥或权限链，使生产面在暂时正常时已经失去预期恢复能力，并利用生产健康视图与恢复状态之间的差异延迟发现。 / Adversaries degrade recovery copies, configuration, keys, or authority so expected restoration is already lost while production can appear healthy, using the gap between production health and recovery state to delay discovery.

### Definition and concept / 定义与概念

中文：抑制系统恢复是攻击者删除、禁用、缩短保留、加密或以权限变化阻断恢复点、卷影副本、备份目录、恢复环境、恢复密钥及相关恢复配置，使组织在数据损坏、加密、删除或系统故障后无法按既定流程恢复。直接目标是恢复能力，不是当前生产数据本身；恢复对象可以继续显示在目录中，但若关键密钥、依赖或权限链已失效，恢复能力仍可能被抑制。

English: Inhibit System Recovery is adversary deletion, disablement, retention reduction, encryption, or authority changes that block recovery points, shadow copies, backup catalogs, recovery environments, recovery keys, or related recovery configuration, preventing restoration after data damage, encryption, deletion, or system failure. The direct target is recoverability rather than current production data. A recovery object can remain listed while loss of a required key, dependency, or authority chain still inhibits restoration.

中文：概念单位是预期恢复路径的能力状态及其变化，而非某个命令、备份厂商或介质。必须记录被保护生产对象、对应恢复点、保留与锁定状态、恢复权限和最近验证结果，才能判断攻击是否只造成恢复风险、已缩小恢复窗口，还是已使特定恢复路径不可用。

English: The conceptual unit is the capability state and transition of an expected recovery path, not a command, backup vendor, or medium. Determination requires the protected production resource, corresponding recovery point, retention and lock state, restore authority, and latest validation outcome to distinguish elevated recovery risk, a shortened recovery window, and an unusable restore path.

### Stealth characteristics / 匿迹特性

中文：抑制系统恢复可以在生产文件仍可读取、应用仍可服务且主机健康检查正常时完成。攻击者把变化施加在恢复面后，当前业务指标通常不产生与恢复损失等量的异常；只监测生产端点或当前可用性的防守方会把“没有故障”误当成“仍可恢复”，直至后继破坏或演练才发现恢复链断裂。这一潜伏差异改变的是发现时机和观察位置，并不使备份管理操作本身不可见。

English: Inhibit System Recovery can complete while production files remain readable, applications continue serving, and host health checks stay normal. After the adversary changes the recovery plane, current business metrics need not show an anomaly proportional to recovery loss. Defenders watching only production endpoints or present availability can mistake “no failure” for “recoverable” until later impact or an exercise exposes the broken chain. This latent divergence changes discovery time and observation location; it does not make backup-management actions invisible.

中文：恢复控制面仍会留下身份、命令或 API、恢复点 ARN/ID、策略差分、锁状态、计算到期时间和删除结果；Windows 主机也可留下 `vssadmin`、`wbadmin`、`bcdedit`、`REAgentC` 或 WMI 的进程链。独立保存恢复状态、控制面审计和定期恢复验证会显著压缩匿迹效果。合法保留到期、容量清理、故障修复及灾备演练产生相似痕迹，必须结合审批、对象关键性和实际恢复状态判断。

English: The recovery control plane still exposes identity, command or API, recovery-point ARN or ID, policy diff, lock state, calculated expiry, and deletion outcome. Windows hosts can retain process lineage for `vssadmin`, `wbadmin`, `bcdedit`, `REAgentC`, or WMI. Independently retained recovery-state inventories, control-plane auditing, and scheduled restore validation substantially reduce the stealth effect. Legitimate retention expiry, capacity cleanup, repair, and disaster-recovery exercises create similar traces and require approval, object criticality, and actual restore state for discrimination.

### Scope boundary definition / 范围边界界定

中文：纳入对已存在恢复材料的删除、加密、不可逆保留缩短或密钥破坏，以及对恢复环境、备份计划、版本策略或恢复权限的改变，只要变化使既定恢复目标或恢复时间窗实质失效。恢复控制变更若被拒绝、及时回滚且恢复点仍满足 RPO/RTO，只能记录为企图。正常备份轮转与获批保留到期是反例；未经测试的备份只能说明未知状态，不能自动推断已被攻击。

English: Include deletion, encryption, irreversible retention reduction, or key destruction affecting existing recovery material, and changes to recovery environments, backup plans, version policy, or restore authority when they materially defeat an established recovery target or window. A recovery-control change that is denied or promptly rolled back while recovery points still meet RPO/RTO is an attempt only. Normal rotation and approved retention expiry are counterexamples; an untested backup is unknown rather than proof of adversary impairment.

中文：当前业务对象被删除或覆写归 NJT-0156，当前业务内容因未授权密钥控制变为密文归 NJT-0157。只停用备份产品的检测、日志或告警而恢复点仍可用归防御损伤；当前服务停止、关机或业务中断按直接结果另记。恢复点同时是一个数据对象并不改变这一边界，分类依据它在事件发生前承担的恢复角色。

English: Deletion or overwrite of the current business object belongs to NJT-0156, and unauthorized ciphertext/key custody denying current business reading belongs to NJT-0157. Disabling only a backup product's detection, logging, or alerting while recovery points remain usable belongs to defense impairment. Current service stop, shutdown, or business outage is recorded by its own direct result. A recovery point's implementation as a data object does not change the boundary; classification follows its pre-event recovery role.

### Application scenarios / 应用场景

中文：在勒索或破坏载荷释放前，攻击者可删除 Windows 卷影副本和备份目录、禁用 WinRE，或从虚拟化管理面删除虚拟机快照，使后继数据加密或销毁更难回滚。在云备份环境，攻击者可直接删除恢复点，也可缩短恢复点保留期或移除持续备份规则，让服务在稍后按配置使恢复点到期。生产工作负载可能在这些动作发生后继续运行，攻击者因而获得从恢复损伤到公开影响之间的时间窗口。

English: Before ransomware or destructive payload release, an adversary can delete Windows shadow copies and backup catalogs, disable WinRE, or remove VM snapshots through a virtualization management plane so later encryption or destruction is harder to roll back. In cloud backup environments, the adversary can delete recovery points directly or shorten retention and remove continuous-backup rules so the service expires recovery points later according to configuration. Production workloads may continue after these actions, giving the adversary a window between recovery damage and overt impact.

### Attacker model / 攻击方模型

中文：攻击方需要能修改恢复状态的本地主机高权限，或备份、虚拟化、云控制面中的删除和策略权限，并需识别哪些恢复点、保留规则、密钥或环境支撑关键业务。直接删除追求快速确定性；策略驱动到期需要攻击者容忍服务调度与保留窗口，并让恶意配置在响应前保持有效。不可变锁、跨账户隔离、独立身份和被验证的离线副本会阻断或缩小效果。

English: The adversary needs local host privilege capable of changing recovery state or deletion and policy authority in backup, virtualization, or cloud control planes, plus knowledge of the recovery points, retention rules, keys, or environments supporting critical business services. Direct deletion favors speed and certainty. Policy-driven expiry requires tolerance for service scheduling and retention windows and persistence of the malicious configuration before response. Immutable locks, cross-account isolation, separate identity, and validated offline copies block or reduce the effect.

### Defender model / 防守方模型

中文：防守方可观察主机进程和命令行、Windows 恢复状态清单、备份控制面审计、恢复点清单、锁与保留配置、备份完成或删除事件及恢复演练结果。高质量判断需要把生产资源映射到其恢复点和 RPO/RTO，并跨身份、区域、账户及长于保留变化的时间窗关联。只监测生产 EDR、只统计备份作业成功、缺少策略历史或从不执行恢复验证时，会形成核心盲区。

English: Defenders can observe host process and command line, Windows recovery-state inventory, backup control-plane audit, recovery-point inventory, lock and retention configuration, backup completion or deletion events, and restore-exercise results. High-quality assessment maps production resources to recovery points and RPO/RTO and correlates across identity, region, account, and a horizon longer than retention changes. Production-only EDR, backup-success counts without restore tests, missing policy history, and absent restore validation create the core blind spots.

### Supported parent stealth mechanism

`TA0040-T1490-MECH-RECOVERY-VIEW` — `NM-BT`, primary. **Summary zh:** 恢复能力损失留在生产健康视图之外. **Summary en:** Recovery loss remains outside the production-health view. **Analysis zh:** 攻击者在恢复面删除副本、禁用配置或撤销恢复依赖，导致真实恢复能力下降，而生产服务与当前数据仍能保持正常痕迹；仅观察生产健康的防守方不会获得与损失相称的告警，并将异常推迟到恢复请求或验证时，形成行为透明。恢复控制面审计、独立状态清单和演练仍可恢复因果。 **Analysis en:** The adversary removes copies, disables configuration, or revokes restore dependencies in the recovery plane, reducing actual recoverability while production services and current data retain normal traces. A defender observing production health does not receive an alert proportional to the loss and discovers the anomaly only at restore request or validation, producing Behavioral Transparency. Recovery control-plane audit, independent state inventory, and exercises can restore causality. **Evidence:** E1, E8, E9, E10. **Confidence:** `medium` for the stealth causal generalization; `high` for the recovery-state facts.

### Parent taxonomy narrative / 父级分类叙述

中文：当前建议只设“策略驱动的延迟恢复点到期”一个原生子项，划分变量是攻击者的恢复破坏决策是否由策略变更转化为稍后以服务身份执行的到期事件。直接恢复点删除、卷影副本删除、恢复环境禁用和恢复密钥损失仍属于父级核心，因为它们的工具、平台和对象类型不形成独立匿迹变量。子项与 NJT-0156 的委托执行式数据销毁共享“委托执行”机制，但直接对象不同：前者消除恢复角色，后者消除当前业务数据用途。

English: The current proposal establishes one native child, Deferred Policy-Driven Recovery Expiration. Its variable is whether the adversary's recovery-destruction decision is converted by a policy change into a later service-identity expiry event. Direct recovery-point deletion, shadow-copy deletion, recovery-environment disablement, and restore-key loss remain parent core because tool, platform, and object type do not form independent stealth variables. The child shares delegated execution mechanics with NJT-0156's delegated data destruction, but its direct object differs: this child removes a recovery role, while the NJT-0156 child removes current business-data utility.

## Proposed child `TA0040-T1490-CHILD-DEFERRED`

**Name / 名称:** 策略驱动的延迟恢复点到期 / Deferred Policy-Driven Recovery Expiration. **Existence confidence:** `medium`; no named victim CASE.

### Definition and concept / 定义与概念

中文：策略驱动的延迟恢复点到期是攻击者修改备份计划、恢复点生命周期或持续备份关联，使恢复副本在未来由备份服务按新策略自动到期或删除。稳定变量是恶意决策与破坏执行在时间、身份和遥测平面上分离：攻击者留下控制面策略写入，服务稍后产生恢复点消失结果。

English: Deferred Policy-Driven Recovery Expiration is adversary modification of a backup plan, recovery-point lifecycle, or continuous-backup association so the backup service automatically expires or deletes recovery copies later under the new policy. The stable variable is separation of malicious decision and destructive execution across time, identity, and telemetry plane: the adversary leaves a control-plane policy write, while the service later produces recovery-point loss.

### Stealth characteristics / 匿迹特性

中文：策略驱动的延迟恢复点到期把一个低频管理变更转化为稍后的正常服务生命周期结果。只监测直接 `DeleteRecoveryPoint`、当前恢复点数量或短窗身份活动的防守方，可能看到服务到期而不能从结果事件直接识别原始操作者；生产面在到期前后仍可正常。策略前后差分、`CalculatedLifecycle.DeleteAt`、原始操作者、`BackupDeleted` 结果及 RPO 缺口仍可关联。

English: Deferred Policy-Driven Recovery Expiration converts one low-frequency administrative change into a later normal service-lifecycle outcome. A defender watching only direct `DeleteRecoveryPoint`, current recovery-point count, or short-window identity activity may see service expiry without identifying the original actor from the result event, while production remains normal before and after expiry. Before-and-after policy, `CalculatedLifecycle.DeleteAt`, initiating actor, `BackupDeleted` outcome, and the resulting RPO gap remain correlatable.

### Scope boundary definition / 范围边界界定

中文：纳入恶意缩短已有恢复点生命周期，或移除持续备份规则并让现有恢复点按保留期稍后自动删除的行为。直接删除恢复点留在父级；对业务数据桶设置生命周期并删除当前业务对象归 NJS-0156-001。获批成本优化、合规保留变化、测试计划清理和保留期自然届满是反例。策略变化必须指向恢复角色对象，并在预期 RPO/RTO 上产生实质风险或结果。

English: Include malicious shortening of an existing recovery point's lifecycle or removal of a continuous-backup rule that lets the existing recovery point be deleted automatically after retention. Direct recovery-point deletion remains parent core. A lifecycle rule deleting current business objects belongs to NJS-0156-001. Approved cost optimization, compliance retention change, test-plan cleanup, and natural expiry are counterexamples. The policy change must target a recovery-role object and materially threaten or violate expected RPO/RTO.

### Application scenarios and threat model / 应用场景与威胁模型

中文场景：在 AWS Backup 中，攻击者可对周期恢复点调用 `UpdateRecoveryPointLifecycle`，将 `DeleteAfterDays` 改为较短值；服务计算 `DeleteAt` 并在到期后执行删除。对持续备份，攻击者可删除唯一持续备份规则，AWS Backup 保留原保留期并在其届满时自动删除恢复点。该路径不要求攻击者在影响时逐个发出删除请求。

English scenario: In AWS Backup, an adversary can call `UpdateRecoveryPointLifecycle` on periodic recovery points to shorten `DeleteAfterDays`; the service calculates `DeleteAt` and deletes after expiry. For continuous backups, the adversary can remove the only continuous-backup rule, after which AWS Backup remembers the prior retention period and automatically deletes the recovery point when it elapses. The path does not require the adversary to issue one delete request per recovery point at impact time.

中文攻击方：攻击者需要修改恢复点生命周期或备份计划的权限、关键恢复点与保留窗口知识，以及等待服务到期的时间。合规模式 Vault Lock 会拒绝生命周期更新或提前删除；错误的恢复点选择、保留期过长、跨账户副本或及时回滚会降低效果。

English attacker: The adversary needs recovery-point lifecycle or backup-plan modification authority, knowledge of critical recovery points and retention windows, and time to wait for service expiry. Compliance-mode Vault Lock denies lifecycle updates or early deletion. Wrong point selection, long retention, cross-account copies, or prompt rollback reduce effect.

中文防守方：防守方需要 CloudTrail 管理事件、策略或生命周期前后快照、响应中的计算到期时间、恢复点清单、Vault Lock 状态、`BackupDeleted` 服务事件及资源到恢复点映射。关联窗口必须延伸到计算到期时间和服务删除延迟；只保存短期 CloudTrail 或只监测直接删除会断开谱系。

English defender: The defender needs CloudTrail management events, before-and-after plan or lifecycle state, calculated expiry in the response, recovery-point inventory, Vault Lock state, `BackupDeleted` service events, and resource-to-recovery-point mapping. Correlation must extend to calculated expiry and service deletion delay; short CloudTrail retention or direct-delete-only monitoring breaks lineage.

### Supported child stealth mechanism

`TA0040-T1490-MECH-DEFERRED` — `NM-BT`, primary. **Summary zh:** 服务到期将策略操作者与恢复点损失分离. **Summary en:** Service expiry separates the policy actor from recovery-point loss. **Analysis zh:** 攻击者缩短生命周期或移除持续备份规则，恶意决策只出现在控制面写入；服务在未来按自身身份和调度删除恢复点。结果侧监测看到正常到期而缺少原操作者，短窗分析难以解释恢复点为何消失；连接策略版本、计算到期时间和服务删除事件可恢复因果。 **Analysis en:** The adversary shortens lifecycle or removes a continuous-backup rule, leaving the malicious decision only in a control-plane write. The service later deletes the recovery point under its own identity and schedule. Outcome-only monitoring sees normal expiry without the original actor, and a short-window analytic cannot explain why the recovery point disappeared; joining policy versions, calculated expiry, and service deletion restores causality. **Evidence:** E6, E7, E9. **Confidence:** `medium`.

### Child research limitation / 子项研究限制

中文：AWS 官方文档直接证明生命周期更新、计算到期和服务自动删除行为，Mandiant 建议监控未授权的保留与备份策略变更，足以建立受约束的攻击路径和防御差异。公开资料尚未给出一个命名受害者从恶意策略写入到自动到期及恢复失败的完整链条，因此不得制造 CASE，也不得把所有短保留策略视为攻击。其他云或备份产品只有取得相同字段和执行语义后才能纳入。

English: AWS documentation directly establishes lifecycle updates, calculated expiry, and automatic service deletion, while Mandiant recommends monitoring unauthorized retention and backup-policy changes. This supports a bounded attack path and distinct defensive method. Public reporting does not trace a named victim end to end from malicious policy write through automatic expiry and failed restore, so no CASE should be invented and short retention alone cannot be treated as malicious. Other clouds or backup products require their own field and execution evidence before inclusion.

## Defense candidates

### `TA0040-T1490-DET-RECOVERY-STATE` — Recovery-State Transition and Outcome Correlation / 恢复状态转换与结果关联

**Strategy objective:** detect unauthorized reduction of recoverability by joining initiating action, resulting recovery state, and protected-resource coverage. Cover parent and provisional child. Use two analytics because endpoint recovery and AWS Backup expose materially different fields and time horizons.

#### `TA0040-T1490-NJA-WINDOWS`

**Name:** Windows Recovery-Control Command and State Differential / Windows 恢复控制命令与状态差分.

**Logic:** From Microsoft Defender XDR `DeviceProcessEvents`, select execution of `vssadmin.exe`, `wbadmin.exe`, `diskshadow.exe`, `bcdedit.exe`, `reagentc.exe`, `wmic.exe`, PowerShell, or command shells with arguments that delete shadows/catalogs, disable recovery, change boot recovery policy, or invoke WMI shadow-copy deletion. Preserve `Timestamp`, `DeviceId`, `DeviceName`, `FileName`, `ProcessCommandLine`, `ProcessId`, `ProcessUniqueId`, `AccountSid`, `AccountName`, `InitiatingProcessFileName`, `InitiatingProcessCommandLine`, `InitiatingProcessUniqueId`, `SHA1`, `FolderPath`, and `ReportId`. Join the process chain on `DeviceId` and process identifiers over 10 minutes. Within 30 minutes, compare an independently collected recovery-state inventory before and after the action: shadow-copy IDs/count and creation times, WinRE enabled state, backup catalog/version IDs, and approved change ID. Promote only a successful state reduction or a command combined with later ransomware/destruction evidence; keep denied or unchanged state as an attempt.

**Data requirements:** (1) MDE `DeviceProcessEvents` with the fields above; (2) an organization-owned recovery inventory with `asset.id`, `collection.time`, `shadow_copy.id`, `shadow_copy.created`, `winre.status`, `backup_catalog.id`, `backup_version.id`, `state_hash`, `approved_change.id`; (3) critical-asset and maintenance baselines. The inventory is a custom source; do not attribute its state fields to MDE.

**Observables:** recovery-control command under an unusual account or parent; drop in recoverable snapshots/catalog entries; WinRE changing enabled→disabled; sequence of recovery inhibition followed by encryption or destruction.

**Correlation:** process lineage 10 minutes; action-to-state verification 30 minutes; optional ransomware-chain correlation 6 hours following Microsoft's hunting precedent. Dimensions: `DeviceId`, `ProcessUniqueId`, `InitiatingProcessUniqueId`, `AccountSid`, normalized command family, recovery object ID, state collection time.

**False positives:** approved disaster-recovery exercises, OS repair, snapshot rotation, backup migration, storage-capacity maintenance, vendor-supported cleanup.

**Blind spots:** direct COM/API calls without distinctive command text, unmanaged hosts, disabled MDE, missing prior inventory, remote storage-side deletion, renamed or in-memory tooling, a backup state that exists but cannot actually restore.

**Tuning:** baseline administrative principals and change tickets per critical asset, but never globally allow `SYSTEM`, backup service accounts, or native utilities. Distinguish attempt, confirmed state loss, and failed restore. Require a stricter approval match rather than a higher count on domain controllers and recovery servers. **Evidence:** reuse REF-000598 for fields; E1, E2, E3 for command/state semantics. The Microsoft example threshold of multiple ransomware signs is a hunting example, not a universal T1490 threshold.

#### `TA0040-T1490-NJA-AWS`

**Name:** AWS Backup Policy, Recovery-Point, and Service-Expiry Lineage / AWS 备份策略、恢复点与服务到期谱系.

**Logic:** In CloudTrail, identify `backup.amazonaws.com` calls including `DeleteRecoveryPoint`, `UpdateRecoveryPointLifecycle`, `UpdateBackupPlan`, `DeleteBackupPlan`, `DeleteBackupSelection`, and `DeleteBackupVaultLockConfiguration`. For direct deletion, alert immediately on an unapproved successful request and aggregate distinct recovery-point ARNs per principal and vault over a tunable 15-minute window. For lifecycle changes, capture prior and returned lifecycle, especially `DeleteAfterDays` and `CalculatedLifecycle.DeleteAt`, compare against minimum retention and approval, then retain the join until `DeleteAt` plus the documented service deletion delay. Correlate subsequent `BackupDeleted` service events and recovery-point inventory loss by vault, ARN, account, and Region. Map affected recovery points back to protected `resourceArn` and compute whether surviving points still meet RPO. A policy change is pre-impact; actual deletion or an RPO gap confirms outcome.

**Required CloudTrail fields:** `eventTime`, `eventSource`, `eventName`, `awsRegion`, `recipientAccountId`, `userIdentity.type`, `userIdentity.arn` or `principalId`, `sessionContext.attributes.mfaAuthenticated`, `sourceIPAddress`, `userAgent`, `requestParameters.backupVaultName`, `requestParameters.recoveryPointArn`, lifecycle request fields, `responseElements.calculatedLifecycle.deleteAt` when returned, `eventID`, `errorCode`, `errorMessage`. For service outcomes: `serviceEventDetails.state`, `backupVaultName`, `recoveryPointArn`, `resourceArn`, and completion time where present. Supplement with `DescribeBackupVault` lock state, recovery-point inventory, criticality, RPO/RTO, policy version, and approval ID.

**Correlation:** direct-delete burst 15 minutes; plan/lifecycle change immediately; deferred outcome through `CalculatedLifecycle.DeleteAt` plus 8 hours because AWS documents randomized deletion within eight hours after expiration. Dimensions: account, Region, vault name/ARN, recovery-point ARN, resource ARN, initiating principal, policy version, calculated expiry, event ID.

**False positives:** approved retention reduction, resource decommission, test-vault cleanup, cost-control changes, migration between backup plans, legitimate deletion of expired or orphaned recovery points.

**Blind spots:** deletion through a source service outside AWS Backup, missing organization trails or insufficient retention, cross-account copies omitted from inventory, service events without original user identity, compromised approved principals, a listed recovery point that fails restoration for unlogged dependency reasons.

**Tuning:** maintain minimum retention and allowed policy hashes per workload tier, separate denied and successful calls, treat compliance-locked vault failures as attempts, and avoid global suppression for root or backup administrators. Require restore tests for assurance; inventory alone cannot prove recoverability. **Evidence:** reuse REF-000524 for generic record fields; E5–E8 for AWS Backup-specific APIs, fields, timing, and locks.

### Mitigation resolutions

**`MIT-000158` candidate `extend`:** the existing **Data-Retention Authority and Independent Recovery Protection** object has an exact reusable measure, `protected-independent-copies`, covering immutable or separately administered copies and restore exercises. Add a T1490 parent application only if the control meaning remains unchanged: keep at least one recovery copy outside production-writer authority and regularly restore the real workload. Expected effect is survival of a recovery route when local shadows or online recovery points are removed. Limitation: a copy in the same identity/control plane is not independent, and periodic testing does not preserve current production availability. Do not reuse its S3 lifecycle-rule application or wording for the proposed AWS Backup child.

**`TA0040-T1490-MIT-RECOVERY-CONTROL` candidate `create` (or `split` after primary review):** **Recovery-Control Authority and Immutable Vault Governance / 恢复控制权限与不可变保管库治理.** Measures: (1) separate production and recovery administration; grant delete, lifecycle-update, plan-delete, lock-change, snapshot-delete, and recovery-key rights only to break-glass roles with phishing-resistant MFA and independent audit; (2) place critical recovery points in compliance-mode immutable vaults or equivalent WORM retention after validating grace period and retention bounds, with cross-account/logically isolated copies; (3) maintain a protected resource→recovery point→key→restore dependency map and exercise full restoration against RPO/RTO.

**Parent application:** protect shadow copies and cloud recovery points from the same principals that modify production, deny unneeded recovery-destructive utilities or APIs, alarm on state reduction, and preserve a validated independent copy. Expected effect: constrains immediate deletion and leaves a usable recovery route. Limitations: local shadow copies are not a substitute for independent backup; application control can disrupt legitimate administration; governance-mode locks remain removable by privileged users; compliance mode becomes immutable after grace and can impose cost or retention mistakes.

**Deferred-child application:** enforce minimum retention and compliance Vault Lock so `UpdateRecoveryPointLifecycle` cannot shorten existing protected recovery points below policy; version backup plans and alert on any retention or continuous-rule removal. Expected effect: prevents or exposes separation of policy write from later service expiry. Limitations: existing points created before lock keep earlier lifecycle settings, continuous backups have product-specific behavior, and a separate unprotected copy or source-service snapshot may still be deleted. **Evidence:** E8, E9, E10, E11.

## Evidence and source candidates

| Key | Primary source and locator | Supports and limits |
|---|---|---|
| E1 `TA0040-T1490-REF-ATTACK` | [MITRE ATT&CK Enterprise v19 T1490](https://attack.mitre.org/versions/v19/techniques/T1490/), description, platforms, no-subtechnique inventory, DET0329 | Parent behavior/tactic and breadth anchor only; create new REF. |
| E2 `TA0040-T1490-REF-VSS` | [Microsoft Volume Shadow Copy Service](https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service), “How shadow copies are used” and “VssAdmin” | Shadow copies provide recovery and VssAdmin creates/deletes/lists them; create new REF. |
| E3 `TA0040-T1490-REF-MS-HUNT` | [Microsoft Defender XDR: Find ransomware with advanced hunting](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-find-ransomware), signs and consolidated query | Concrete process/command correlation and example 6-hour grouping; not a universal threshold; create new REF. |
| E4 `REF-000598` | [DeviceProcessEvents schema](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table) | Exact MDE process fields; reuse existing REF. |
| E5 `TA0040-T1490-REF-AWS-BACKUP-CT` | [Logging AWS Backup API calls with CloudTrail](https://docs.aws.amazon.com/aws-backup/latest/devguide/logging-using-cloudtrail.html), DeleteRecoveryPoint example and BackupDeleted/BackupJob events | Exact AWS Backup event fields; create new REF, while generic CloudTrail fields reuse REF-000524. |
| E6 `TA0040-T1490-REF-AWS-UPDATE-LIFECYCLE` | [UpdateRecoveryPointLifecycle API](https://docs.aws.amazon.com/aws-backup/latest/APIReference/API_UpdateRecoveryPointLifecycle.html), request and response | `DeleteAfterDays`, `CalculatedLifecycle.DeleteAt`, automatic expiry; create new REF. |
| E7 `TA0040-T1490-REF-AWS-BACKUP-DELETE` | [AWS Backup deletion](https://docs.aws.amazon.com/aws-backup/latest/devguide/deleting-backups.html), automatic deletion and continuous backup behavior | Service deletion timing and outcome semantics; create new REF. |
| E8 `TA0040-T1490-REF-AWS-VAULT-LOCK` | [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html), modes, grace time, immutable behavior, DescribeBackupVault fields | Prevention effect and limits; create new REF. |
| E9 `TA0040-T1490-REF-MANDIANT-DESTRUCTIVE` | [Mandiant: Proactive Preparation and Hardening Against Destructive Attacks, 2026](https://cloud.google.com/blog/topics/threat-intelligence/preparation-hardening-destructive-attacks), backup-policy monitoring and immutable recovery sections | Threat model, detection opportunity, and mitigation; not a named policy-expiry victim; create new REF. |
| E10 `TA0040-T1490-REF-MANDIANT-IRE` | [Mandiant: Isolated Recovery Environments](https://cloud.google.com/blog/topics/threat-intelligence/isolated-recovery-environments-modern-cyber-resilience), Backup Blind Spot and IRE characteristics | Production/recovery separation and isolation control; create new REF. |
| E11 `TA0040-T1490-REF-CISA-GUIDE` | [CISA StopRansomware Guide](https://www.cisa.gov/stopransomware/ransomware-guide), backup and recovery preparation | Offline backups and regular availability/integrity restore testing; create new REF. |
| E12 `TA0040-T1490-REF-CISA-GHOST` | [CISA/FBI/MS-ISAC Ghost ransomware advisory PDF](https://www.cisa.gov/sites/default/files/2025-02/aa25-050a-stopransomware-ghost-cring-ransomware.pdf), T1490 paragraph | Observed VSS service disablement and shadow-copy deletion; create REF and parent CASE candidate only. |
| E13 `REF-000524` | [AWS CloudTrail record contents](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html) | Generic record identity, method, Region, source, request, and error fields; reuse existing REF. |

## Shared-library lookup and resolutions

Executed `library_lookup.py` with: `inhibit system recovery`; `shadow copy recovery backup deletion`; `immutable recovery backup vault lock`; `DeleteRecoveryPoint`; `DeviceProcessEvents table`; `AWS Backup CloudTrail DeleteRecoveryPoint`; `AWS Backup Vault Lock`; `CISA StopRansomware offline backups restore test`; `Volume Shadow Copy Service vssadmin delete shadows`; `Proactive Preparation Hardening destructive attacks 2026`; `ATT&CK T1490`; `Ghost Cring ransomware shadow copies`; `RansomHub vssadmin delete shadow copies`; and `Medusa shadow copies backup`.

- **References:** reuse `REF-000598` for MDE process fields and `REF-000524` for generic CloudTrail fields. No exact canonical URL exists for E1–E3 or E5–E12. `REF-000275` is the same Medusa advisory identity but its current locator and CASE-000098 cover fleet deployment, not recovery deletion; extending its locator could support a new T1490 claim, but CASE-000098 must not be extended because its central case meaning is deployment. `REF-000649` models indirect lifecycle deletion of business cloud data and may support the generic delegated-execution contrast, but it does not prove recovery-point role and is not sufficient for the child.
- **Cases:** propose `TA0040-T1490-CASE-GHOST-SHADOWS` from E12 for parent behavior. No CASE for deferred policy expiry. Do not reuse CASE-000098 or CASE-000147; their meanings are Medusa deployment and Ragnar guest isolation.
- **Claims:** create narrow bilingual candidates: `TA0040-T1490-CLM-PARENT-ROLE` (loss of recovery-role artifacts is distinct from current-data loss; E1/E2); `TA0040-T1490-CLM-LATENT-VIEW` (recovery loss can precede current outage and requires recovery-plane observation; E9/E10); `TA0040-T1490-CLM-DEFERRED` (AWS lifecycle policy determines automatic recovery-point expiry and calculated deletion; E6/E7); `TA0040-T1490-CLM-WINDOWS-DETECTION` (specific process fields plus state inventory are needed; E3/E4); `TA0040-T1490-CLM-AWS-DETECTION` (CloudTrail exposes recovery-point identity and principal; E5/E13); `TA0040-T1490-CLM-VAULT-LOCK` (compliance lock denies lifecycle/delete changes after grace; E8).
- **Detection objects:** `DET-000174` and `NJA-000190` are close fuzzy matches because they connect a policy write to later service deletion, but they are S3 business-object lifecycle logic with bucket/rule/object fields. T1490 needs backup vault, recovery-point ARN, calculated lifecycle, resource mapping, RPO and restore state. Recommendation: **split/create**, not reuse. No existing Windows recovery-state NJA matched.
- **Mitigations:** recommend **extend** `MIT-000158` only for its semantically identical independent protected-copy/restore-exercise measure and a new parent application. Its S3 lifecycle-rule measure does not directly govern AWS Backup recovery lifecycle. Create or split `TA0040-T1490-MIT-RECOVERY-CONTROL` for recovery-admin separation, immutable vault control, minimum retention and lock governance.
- **Relationships:** no existing relationship candidate found. Parent-child, DET/NJA, and Mitigation Application links should be written only after formal IDs exist.

## Evidence coverage and content review

**Parent behavior:** E1, E2, E12. **Boundary:** E1 plus NJT-0156/NJT-0157 canonical scopes. **Parent mechanism:** E8–E10, calibrated medium. **Child existence/mechanism:** E6, E7, E9, medium and no CASE. **Detection fields:** E3–E7, E13. **Mitigation:** E8–E11. **Unsupported/deferred:** cross-account deletion topology, slow pacing, decoy points, false-success corruption, and a generalized recovery-key child.

Compared with NJT-0001 by field responsibility: the parent and provisional child each define the direct object and purpose, stealth variable, trace change, defender-observation effect, residual evidence, inclusion/exclusion, adjacent techniques, scenario, attacker capability, defender telemetry, mechanism chain, evidence strength, and limitations. The two NJAs have separate field sets, horizons, false positives, and blind spots. No reader-facing canonical prose was script-generated.

## Final research limitations

中文：公开证据充分证明攻击者会删除卷影副本、恢复点与备份，并证明生产面与恢复面需要独立观察；但“业务仍运行”只说明潜伏窗口，不证明每个攻击者都以匿迹为主观目的。AWS 文档证明策略驱动的自动到期语义，Mandiant 证明该控制面需要防御监控，却没有命名受害者完整案例，因此子项不得提升为高置信。恢复点存在也不等于可恢复，只有受控恢复测试能验证关键依赖；测试失败还可能由正常故障、版本不兼容或凭据过期造成。

English: Public evidence establishes adversary deletion of shadow copies, recovery points, and backups and the need to observe production and recovery separately. Continued business operation creates a latent window but does not prove that every adversary subjectively sought stealth. AWS documentation establishes policy-driven automatic expiry and Mandiant establishes the need to monitor that control plane, but no named victim case completes the chain, so the child must not be raised to high confidence. Recovery-point presence does not prove restorability; only controlled restore tests validate dependencies, and test failure can also result from benign faults, version incompatibility, or expired credentials.

**Integration status:** pending primary-agent review after all five candidate handoffs. The primary agent must converge T1489/T1490 backup-service boundaries, resolve reuse/split decisions, allocate IDs, write canonical objects, run quality/build/Web gates, and keep lifecycle at `review` until human domain review.
