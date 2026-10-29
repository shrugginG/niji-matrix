# T1485 Data Destruction research handoff

`batch_ref: BATCH-TA0040-001`  
`work_item_ref: WORK-TA0040-T1485`  
`temporary_key_prefix: TA0040-T1485-`  
`status: research-only; integration pending`  
`baseline: Enterprise ATT&CK 19.1`  
`formal IDs allocated: none`

## Admission recommendation

**Adapt; medium confidence.** Proposed bilingual decision rationale:

> 数据销毁通过删除或覆写业务数据、文件及对象，使合法使用者无法继续按原用途访问，符合 TA0040 的影响目的。ATT&CK T1485 同时涵盖并不具匿迹设计的公开破坏，因此在 Niji 中应适配为攻击者有意改变破坏发起者、执行时点或可见数据状态与真实损失之间关系的销毁行为。云存储生命周期规则是证据最充分的实例：恶意规则变更与后来由存储服务执行的删除分属控制面和数据面，单看对象删除容易漏掉原始决策者；直接批量删除和普通覆写仍是父级参照行为，却不能仅凭破坏结果获得 Niji 子项资格。[E1][E2][E3][E4]
>
> Data destruction removes or overwrites business data, files, or objects so legitimate users can no longer use them as intended, which meets the purpose of TA0040. ATT&CK T1485 also includes overt destruction without a stealth design, so Niji should adapt it to destruction in which the adversary intentionally changes the relationship between the initiating actor, execution time, or visible data state and the actual loss. A cloud storage lifecycle rule is the best supported instance: the malicious rule change and later service-executed deletion appear in separate control and data planes, and an observer who sees only object deletion can miss the original decision maker. Direct bulk deletion and ordinary overwriting remain parent-level reference behaviors, but their harmful result alone does not qualify them as Niji children.[E1][E2][E3][E4]

This is a scope adaptation, not a claim that all T1485 executions are stealthy. Confidence in the **documented AWS pathway** is high; confidence that every destructive campaign intentionally exploits the observation split is low. Do not attach a real-world incident case to the proposed child unless one is found. The Palo Alto Networks analysis is threat modeling and simulation, not a verified victim incident.[E4]

## ATT&CK breadth and cross-technique resolution

Fixed-baseline child count **1**: `T1485.001` Lifecycle-Triggered Deletion, representing cloud storage lifecycle policy and storage-service trigger. Coverage resolution: **`niji-variable-candidate`** only. Its source behavior supports the candidate axis, but its platform, title, and full extension are not imported. The formal child, if accepted, is limited to an attacker-controlled **control-plane-to-data-plane agency split** that changes attribution and detection; an ordinary legitimate lifecycle rule and a direct object delete do not satisfy it. No second taxonomy pass is triggered by a one-child ATT&CK inventory.

Axes examined:

| Axis | Decision | Reason |
| --- | --- | --- |
| Delegated, asynchronous destruction after a destructive control-plane change | **Formal Niji child proposed** | Stable control variable; policy-write and service-executed deletion have different principals, times, and telemetry; control-plane correlation is a distinct defense.[E3][E4][E5][E6] |
| Delete versus overwrite while keeping the file path | `evidence-deferred` | These are documented destructive implementations, but current sources do not show that attackers use the namespace/contents difference to reduce observation. Overwrite can be conspicuous and may overlap T1565 if integrity distortion rather than loss is the direct result.[E1][E10] |
| Slow or distributed file destruction | `evidence-deferred` | A threshold-evasion story is plausible but no conclusion-level T1485 evidence presently establishes deliberate rate or source dispersion. Do not turn a generic low-and-slow motif into a child. |
| Selective preservation of critical paths or hosts | `adjacent-technique` | Already owned by NJT-0117 and its two children. The T1485 parent may link or mention co-occurrence, but must not replicate its selection-axis child. |
| Executing a wiper inside an unobserved guest | `adjacent-technique` | Observation-domain encapsulation is already NJS-0111-004; the host/guest sensor boundary is independent of the destructive target. |
| Disk sector or boot-structure erasure | `adjacent-technique` | Direct destructive object belongs to T1561, not T1485; file-level damage within a disk can coexist but should not blur the parent boundary.[E1] |

Proposed formal Niji child count: **1**. No ATT&CK child is inherited; `lineage.attck_subtechnique_inherited: false`.

## Parent content proposal (temporary key `TA0040-T1485-PARENT`)

Name: **数据销毁 / Data Destruction**. Summary: **攻击者有意使文件或数据对象失去原有用途，并利用执行与观察的分离推迟或混淆对破坏来源的判断。 / Adversaries deliberately make files or data objects unusable while separating execution from observation to delay or confuse attribution of the loss.**

### `definition_and_concept`

> 数据销毁是攻击者删除或覆写可识别的文件、数据对象及其有效内容，使业务数据不再按原用途被读取或处理的影响行为。直接结果是可用性损失，严重程度从可由版本恢复的逻辑删除到无法从现存副本恢复的内容损坏不等；“销毁”不应被自动等同于物理不可恢复。概念单位是受影响的数据对象及其消费结果，不是具体删除命令、文件扩展名或云产品。[E1][E7][E8]
>
> Data Destruction is an impact behavior in which an adversary deletes or overwrites identifiable files, data objects, or their useful contents so business data can no longer be read or processed as intended. The immediate result is loss of availability, ranging from logical deletion recoverable from a version to content damage that cannot be recovered from surviving copies; “destruction” must not automatically imply physical irrecoverability. The conceptual unit is the affected data object and its consumer outcome, not a particular deletion command, file extension, or cloud product.[E1][E7][E8]

> 在 Niji 范围内，销毁还须有可指认的匿迹设计：攻击者让一次有权控制的操作在另一时间或另一执行主体下兑现为数据损失，或通过另有证据支持的方式改变守方看到的损失表象。父级容纳直接删除和覆写作为边界比较，但仅将能够证明“行为设计→痕迹变化→防守观察差异”的变体纳入正式匿迹分类；例如单纯使用 `rm` 或 `del`、备份失效及灾难恢复不足并不足以证明匿迹。[E1][E3][E4]
>
> Within Niji scope, destruction also needs an identifiable stealth design: an operation under adversary control must materialize as data loss at a different time or under a different executing principal, or change the defender-visible appearance of loss in another evidenced way. The parent uses direct deletion and overwrite as boundary comparators, but only variants with a demonstrable behavior-design → trace-change → defender-observation chain enter the formal stealth taxonomy. Merely using `rm` or `del`, failed backup, or weak disaster recovery does not establish stealth.[E1][E3][E4]

### `stealth_characteristics`

> 数据销毁的匿迹特性最清楚地体现在“谁写下破坏决策”和“谁执行删除”分离时：一个控制面策略变更可以在稍后由存储服务异步转成大量对象过期事件。只监视对象 API 或单个短窗口的防守方可能把服务主体和常规到期当作原因，遗漏写入规则的账户及规则覆盖范围；控制面日志、原始规则差分、过期通知、对象版本和业务读取失败仍是可连接的残余痕迹。[E3][E4][E5][E6][E8]
>
> The stealth property of Data Destruction is clearest when the actor who writes the destructive decision differs from the actor that performs deletion: one control-plane policy change can later become many asynchronous, service-executed expiration events. A defender monitoring only object APIs or a short window may treat the service principal and ordinary expiry as the cause and miss the account and rule scope that initiated it. Control-plane logs, policy diffs, expiry notifications, object versions, and business read failures remain linkable residual traces.[E3][E4][E5][E6][E8]

> 该效果取决于守方是否把配置事件与结果事件按桶、规则、对象范围和时间关联；若具备原始配置快照、实时通知或受保护版本，归因分离和实际损失均会下降。相反，大规模直接删除或覆写通常产生密集的文件访问、对象删除或服务中断信号，不应仅因动作发生在夜间就宣称被稀释。[E3][E5][E6][E9]
>
> The effect depends on whether defenders join configuration and outcome events by bucket, rule, object scope, and time. Original configuration snapshots, live notifications, or protected versions weaken the attribution split or actual loss. Mass direct deletion or overwrite usually produces concentrated file-access, object-deletion, or service-disruption signals; a nighttime execution alone does not establish dilution.[E3][E5][E6][E9]

### `scope_boundary_definition`

> 纳入目标是攻击者使业务数据、文件或对象按原用途不可用且能说明匿迹观察差异的销毁行为。应先核验对象是否真的失去可用性：S3 开启版本控制时，删除标记会隐藏当前版本而保留旧版本；非版本桶的生命周期过期可以永久移除对象。区分“当前视图不可见”和“无法恢复”对证据、优先级和缓解效果都有实质意义。[E1][E7][E8]
>
> The included object is adversary destruction that makes business data, files, or objects unusable as intended and has a supported stealth observation difference. First establish whether the object actually lost availability: with S3 versioning, a delete marker hides the current version while older versions remain; lifecycle expiry in an unversioned bucket can remove the object permanently. Distinguishing “absent from the current view” from “unrecoverable” materially changes evidence, priority, and mitigation assessment.[E1][E7][E8]

> 排除为清理攻击工具和日志而删文件的 TA0005 指示器移除、以加密和密钥控制直接妨碍读取的 T1486、以磁盘扇区或引导结构为直接目标的 T1561、以剥夺恢复副本和快照为直接目标的 T1490，以及仍能使用但值已被恶意改变的 T1565。合法保留期届满、获批迁移、容量清理、用户误删及常规备份轮转可能产生相同事件，只有操作者、审批、规则差分、目标重要性和后续业务结果相连后才能分类。[E1][E2][E3][E5]
>
> Exclusions are TA0005 indicator removal that deletes attacker tools or logs, T1486 when encryption and key control directly deny reading, T1561 when disk sectors or boot structure are the direct target, T1490 when recovery copies or snapshots are directly denied, and T1565 when data remains usable but its values are maliciously changed. Legitimate retention expiry, approved migration, capacity cleanup, accidental deletion, and ordinary backup rotation can create the same events; classification requires a join among operator, approval, rule diff, target criticality, and downstream business outcome.[E1][E2][E3][E5]

### `application_scenarios_and_threat_model`

Application scenarios:

> 攻击者在已取得对象存储配置权限后，可能把原本为归档或长期保留设计的生命周期规则改成覆盖业务前缀或非当前版本的快速删除。该方案适合希望在单次低频控制面变更后由平台执行大范围破坏的场景，也适合在勒索或业务中断前抹去关键存储对象；它不要求攻击者逐一访问对象，但销毁结果会受版本、保留锁和异步调度影响。[E2][E3][E4][E7][E9]
>
> After obtaining object-storage configuration authority, an adversary may change lifecycle rules originally designed for archiving or long retention into rapid deletion over business prefixes or noncurrent versions. This fits an operation seeking broad damage from a single low-frequency control-plane change followed by platform execution, including destruction of critical objects before extortion or disruption. It does not require the adversary to access each object, but versions, retention locks, and asynchronous scheduling affect the outcome.[E2][E3][E4][E7][E9]

Attacker model:

> 攻击者至少需要可修改目标数据所在桶生命周期配置的身份、对数据布局或前缀及保留期的认识，以及维持配置到服务执行的时间窗口。以 AWS 为例，该操作要求 `s3:PutLifecycleConfiguration`；对象直接删除权限并非该路径的必要条件。若不能控制保留规则、不了解版本状态，或保护版本受到 Object Lock 约束，就可能只造成可恢复的视图消失或无法删除受保护版本。[E3][E4][E7][E9][E11]
>
> The adversary needs an identity authorized to change lifecycle configuration on the bucket containing target data, knowledge of data layout or prefixes and retention periods, and time for the configuration to remain until service execution. In AWS, the path requires `s3:PutLifecycleConfiguration`; direct object-delete permission is not necessary. Inability to control the rule, ignorance of versioning state, or Object Lock on protected versions can leave only recoverable disappearance from the current view or prevent deletion of protected versions.[E3][E4][E7][E9][E11]

Defender model:

> 防守方假定可采集存储桶控制面管理事件、规则版本或配置快照、对象删除或过期通知，以及对象版本与关键业务读取结果。若只采集用户发起的对象数据事件，服务发起的生命周期删除可能被独立过滤；若只查看过期通知，其主体是存储服务而非最初的规则修改者。跨平面关联必须保留桶 ID、规则 ID、前缀或标签过滤器、版本状态、变更主体和时间；无历史配置快照时，难以证明规则覆盖范围曾被恶意扩大。[E5][E6][E12]
>
> Defenders are assumed to collect bucket control-plane management events, rule versions or configuration snapshots, object-deletion or expiration notifications, and object versions and critical business-read outcomes. If collection covers only user-initiated object data events, service-initiated lifecycle deletion may be filtered separately; if it covers only expiration notifications, the principal is the storage service rather than the earlier rule editor. Cross-plane correlation needs bucket ID, rule ID, prefix or tag filters, versioning state, changing principal, and time. Without historical configuration snapshots, showing that the rule's scope was maliciously expanded is difficult.[E5][E6][E12]

### Mechanism and taxonomy proposal

- `NM-BT` **primary**, medium confidence for parent and high for the child. Summary **控制面决策借服务执行跨越单一对象监测视野 / Control-plane decisions use service execution beyond an object-only monitoring view**. Analysis: attacker-controlled policy write → later platform-generated lifecycle deletion with service principal → object-only observer loses original actor and rule context → causality remains concealed until control-plane and data-plane records are joined. Evidence [E3][E4][E5][E6][E12]. This is a **coverage/logic blind spot**, not an assertion that all lifecycle events evade full monitoring.
- Reject `NM-ST` on current evidence. The delay separates control and result, but the final deletion can be a mass event and is not inherently diluted below a local threshold. `NM-FD` also lacks evidence that the rules were made to resemble approved retention schedules. Keep both in planning only.
- Parent taxonomy narrative should state that the proposed child varies the **execution authority and observability relation**, while immediate deletion or overwrite remains parent core, and selective exclusions/guest isolation are owned by other NJT/NJS objects. Do not use storage vendor, file type, destructive tool, or ATT&CK child label as a child boundary.

### `research.limitations`

> 官方资料确证文件与对象销毁及生命周期规则的权限、执行和事件形态；Palo Alto Networks 的云勒索分析明确把间接删除描述为无需访问对象且更难由对象访问监控发现。然而，公开资料未把此候选中的某个实际受害事件完整追溯为“恶意规则写入→服务过期→业务不可用”，因此子项存在性主要由可复现平台机制与攻击路径分析支持，案例引用应保持为空。具体规则生效延迟、对象最终可恢复性和守方是否真的漏检均依赖部署条件，需要在真实资产上核验。[E1][E3][E4][E5][E7][E9]
>
> Official sources establish file and object destruction and lifecycle-rule permissions, execution, and event shapes; the Palo Alto Networks cloud-ransomware analysis explicitly describes indirect deletion as avoiding object access and making object-access monitoring less effective. Public sources do not trace a particular victim incident end to end from malicious rule write to service expiry to business unavailability, so child existence rests chiefly on reproducible platform mechanics and attack-path analysis, and case references should remain empty. Actual rule execution delay, recoverability, and whether a defender misses the activity depend on deployment conditions and need validation on real assets.[E1][E3][E4][E5][E7][E9]

## Proposed Niji child (temporary key `TA0040-T1485-CHILD-AGENCY-SPLIT`)

Name: **委托执行式数据销毁 / Delegated-Execution Data Destruction**. This title is intentionally different from ATT&CK's `Lifecycle-Triggered Deletion`: the stable variable is the attacker-to-service **execution agency split**, not the platform feature alone. For current evidence, the supported implementation is a cloud storage lifecycle rule; do not claim other policy engines until separately evidenced. Summary: **攻击者改写销毁规则，让存储服务稍后执行删除，使原始操作者与损失事件分离。 / An adversary changes a destructive rule so the storage service later deletes objects, separating the original operator from the loss event.**

Definition:

> 委托执行式数据销毁是攻击者改变一个会由平台自动消费的删除规则，把目标对象的后续移除交给存储服务。其直接目标仍是让数据失去业务用途；子项的分类变量是规则写入者与实际删除者在主体、时间和遥测平面上的分离，而不是“云对象”这种介质，也不是仅仅使用生命周期功能。[E2][E3][E4]
>
> Delegated-Execution Data Destruction is an adversary change to a deletion rule consumed automatically by a platform, leaving subsequent removal of target objects to the storage service. The direct goal is still to deprive business processes of usable data. The child variable is separation of the rule writer and actual deleter across principal, time, and telemetry plane, rather than the cloud-object medium or simple use of lifecycle functionality.[E2][E3][E4]

Stealth characteristics (first paragraph begins with exact bilingual names):

> 委托执行式数据销毁把一次人工规则变更转成稍后的服务主体过期事件；对象级审计会见到 `s3.amazonaws.com`、`Lifecycle Expiration` 或服务发起的生命周期数据事件，而不会在每个受损对象上直接给出最初修改规则的用户。规则变更、通知、对象键、删除标记和版本历史仍可恢复这条因果链；若守方同步观察两平面，优势迅速减弱。[E5][E6][E12]
>
> Delegated-Execution Data Destruction converts one human rule change into later service-principal expiry events. Object-level auditing can show `s3.amazonaws.com`, `Lifecycle Expiration`, or service-initiated lifecycle data events without directly identifying the user who originally changed the rule for every affected object. The rule change, notifications, object keys, delete markers, and version history can still reconstruct the causal chain; simultaneous visibility into both planes sharply reduces the advantage.[E5][E6][E12]

Scope:

> 纳入有证据表明攻击者改动已启用的删除规则，使其覆盖关键对象或缩短到期条件，并由平台后续执行删除的情况。正常保留期到期、获批规则变更、直接 `DeleteObject`、单独删备份、在容器或虚拟机内执行删除均不属于本项。即使对象出现 404，也须检查它是否只是版本化存储中的删除标记，不能把可恢复的当前视图消失写成已证实的永久毁损。[E3][E5][E7][E8]
>
> Include cases with evidence that an adversary changed an enabled deletion rule to cover critical objects or shorten expiry and the platform subsequently performed deletion. Ordinary retention expiry, approved rule changes, direct `DeleteObject`, separate backup removal, and deletion performed inside a container or VM are outside this child. Even when an object returns 404, check whether this is only a delete marker in versioned storage; recoverable absence from the current view is not proven permanent destruction.[E3][E5][E7][E8]

Application scenario:

> 在控制业务数据桶配置但缺少逐对象删除权限时，攻击者可改动面向前缀、标签或非当前版本的生命周期规则，让存储服务在下一次评估中移除符合条件的对象。若告警只针对大量用户发起的删除 API，请求时点的控制面写入与后来的服务事件可能落在不同值班和查询窗口；恢复团队仍可凭历史规则、事件通知及受保护版本追查和恢复。[E3][E4][E5][E7]
>
> When an adversary controls a business-data bucket configuration but lacks per-object delete permission, a lifecycle rule scoped by prefix, tags, or noncurrent version can cause the storage service to remove eligible objects at a later evaluation. Alerts focused on large numbers of user-initiated delete APIs may separate the control-plane write from later service events across shifts and query windows. Historical rules, event notifications, and protected versions still support investigation and recovery.[E3][E4][E5][E7]

Attacker model:

> 需要修改生命周期规则的权限、对被保护桶和过滤器的知识，以及等待异步执行的容忍度。攻击者可能拥有合法或被盗管理员身份，但不必枚举每个对象；版本控制、Object Lock、不同对象的到期条件和配置修复会限制范围或阻止永久损失。[E3][E4][E7][E9][E11]
>
> The attacker requires permission to modify lifecycle rules, knowledge of protected buckets and filters, and tolerance for asynchronous execution. The identity may be legitimate or stolen, but need not enumerate every object. Versioning, Object Lock, object-specific eligibility, and configuration repair can constrain the scope or prevent permanent loss.[E3][E4][E7][E9][E11]

Defender model:

> 防守方具备 CloudTrail 管理事件、桶规则快照、S3 EventBridge 或生命周期通知、版本清单和业务重要性标签，并以桶和规则为中心关联。若只保留对象数据事件或在选择器中排除 `s3lifecycle.amazonaws.com`，会失去关键结果视角；若只看通知，则难以确定更早的规则变更主体。S3 异步执行和午夜记账时间也不宜被误当成精确发起时点。[E5][E6][E12]
>
> The defender has CloudTrail management events, bucket-rule snapshots, S3 EventBridge or lifecycle notifications, version inventory, and business-criticality labels, and correlates by bucket and rule. Keeping only object data events or excluding `s3lifecycle.amazonaws.com` in selectors removes a key outcome view; seeing only notifications makes the earlier rule-changing actor hard to identify. S3 asynchronous execution and midnight marker timestamps must not be mistaken for the exact initiation time.[E5][E6][E12]

Mechanism: `NM-BT` primary, confidence **high for AWS trace mechanics, medium for adversary intent in a specific environment**. Summary **存储服务执行掩盖先前规则写入主体 / Storage-service execution obscures the earlier rule writer**. Causal analysis: malicious rule change → service-scheduled expiration and service principal → object-only rule loses actor and policy context → delayed attribution. Evidence [E3][E4][E5][E6][E12]. Child evidence references should include all mechanism sources; case refs `[]` pending victim-level case. Limitations: same as parent but emphasize native service changes, eligible-object uncertainty, versioning and Object Lock. Do not claim that the service event is absent: AWS explicitly documents both CloudTrail lifecycle data events and EventBridge/S3 notifications.[E5][E6][E12]

## Defense objects (new temporary keys; main Agent resolves reuse/create)

### `TA0040-T1485-DET-ENDPOINT`: destructive file-loss correlation

Coverage **parent**, `enterprise`, Windows file servers with explicit audit SACL on selected critical paths. Objective: identify sustained destruction of business data from file-delete signals and subsequent missing-data impact, while retaining the process and account responsible. Analytic `TA0040-T1485-NJA-WIN-DELETE`:

- Sources and required fields: Windows Security **4663** (`ObjectName`, `AccessMask` or `Accesses`, `ProcessId`, `SubjectUserSid`, `HandleId`, `TimeCreated`, `Computer`) with DELETE access; optionally **4660** (`HandleId`, `ProcessId`, `TimeCreated`) to confirm completed deletion, since 4660 lacks the object name. Join 4663/4660 on host, handle, process, and short time. Microsoft cautions that 4663 can also cover rename and requires SACL; do not count every 4663 as confirmed loss.[E13][E15]
- Logic: for each asset, account, process and critical root, aggregate distinct affected objects and proportion of baseline inventory over **10–30 minutes**. Alert when deletion attempts or confirmed deletions sharply exceed the asset's scheduled maintenance baseline **and** affect multiple business directories or coincide with application read failures. Use a local adaptive threshold rather than a universal file count; preserve paths and event IDs for triage. Link account/process to change ticket and approved cleanup job. A Windows-only analytic is intentionally narrower than ATT&CK's platform list.
- False positives: approved cleanup, log rotation, deployment rollback, bulk migration, retention jobs. Blind spots: SACL absent, Security log cleared, rename versus deletion ambiguity, process telemetry missing, direct storage-controller or hypervisor deletion outside host audit. Mitigation route below should preserve independent backups and log collection. This analytic does not by itself prove stealth and belongs to the adapted parent's destructive-outcome detection, not the Niji child.

### `TA0040-T1485-DET-POLICY`: control-plane to service-deletion lineage

Coverage **parent and proposed child**, `enterprise`, AWS S3. Objective: detect a newly destructive lifecycle configuration **before** service execution and link it to later expiration outcomes. Analytic `TA0040-T1485-NJA-S3-LIFECYCLE`:

- Sources and fields: CloudTrail S3 **management event** `eventName=PutBucketLifecycle` or `PutBucketLifecycleConfiguration`, `eventTime`, `userIdentity.arn`, `sourceIPAddress`, `requestParameters.bucketName`, response status; independently fetch and preserve the normalized *before/after* lifecycle JSON (`Rules[].ID`, `Status`, `Filter.Prefix` or tags, `Expiration.Days/Date`, `NoncurrentVersionExpiration.NoncurrentDays`, `ExpiredObjectDeleteMarker`) because the exact CloudTrail request shape can vary. S3 EventBridge `detail-type=Object Deleted`, `detail.bucket.name`, `detail.object.key`, `detail.reason=Lifecycle Expiration`, `detail.deletion-type`, `time`; or S3 Lifecycle notifications' `eventName`, `userIdentity.principalId`, `s3.bucket.name`, `s3.object.key`, `s3.configurationId`. Join by bucket plus rule/filter-eligible object set; the rule ID may be available in lifecycle notification `configurationId` but **do not assume it is always identical to `Rules[].ID` without local validation**.[E5][E6][E11][E12]
- Logic: at configuration write, compute whether an enabled `Expiration` or `NoncurrentVersionExpiration` was introduced, shortened, broadened from a prefix/tag filter, or made to cover protected business keys; join approved change record, identity baseline, and bucket criticality. Raise a **pre-impact** alert immediately when an unauthorized change expands destructive reach. Over the next **72 hours or the configured expiry horizon, whichever is longer**, join service-origin lifecycle outcomes and actual object-version state to the triggering configuration revision; upgrade severity on multiple critical objects, failed reads, or permanent version removal. Do not require object events to fire before alerting, because the response opportunity exists at rule mutation.[E3][E5][E6][E7]
- False positives: approved retention-policy rollout, storage-cost cleanup, test bucket changes, migration of old object versions. Blind spots: missing CloudTrail management trail, no versioned config snapshots, EventBridge/notifications disabled, lifecycle operations filtered out of CloudTrail data events, asynchronous execution lag, object lock or versioning causing a delete marker rather than permanent loss. Tune with bucket owner, approved rule digest, expected retention floor and protected prefix inventory; never globally suppress service-origin expiration, because its significance comes from the earlier rule change.[E5][E6][E7][E9][E12]

### `TA0040-T1485-MIT-DATA-PRESERVATION`: independent version and recovery protection

Concept: preserve retrievable copies of critical objects and reduce unilateral destructive authority. Measures: (1) enable versioning and object-level WORM retention where required; test recovery of a protected version, recognizing delete markers can still hide the current view; (2) keep recovery copies in a separate account or control domain and exercise restore; (3) gate lifecycle-rule modification through narrowly scoped `s3:PutLifecycleConfiguration`, change approval, and alerting, and deny it for ordinary workload identities. Do **not** claim a bucket policy that denies object deletion stops S3 Lifecycle: AWS states lifecycle actions still run.[E7][E9][E11][E14]

- Parent application: protect business object families and file shares with tested, separately controlled recoverable copies; reduce successful permanent loss and improve reconstruction of which items changed. This does not prevent the live data view from disappearing or restore availability automatically, and endpoint wipers may still destroy unprotected local copies.
- Child application: apply Object Lock to protected S3 versions, constrain and approve `PutBucketLifecycle`, and monitor rule diffs plus expiry events. This blocks deletion of protected versions during retention and exposes the control-plane origin, but delete markers can still make the current object appear absent; governance-mode bypass permissions and an insufficient retention window weaken the effect.[E7][E9][E11]

## Shared-library lookup and resolution suggestions

The required `library_lookup.py --text` searches were run for `data destruction`, `lifecycle`, `bulk delete`, `object lock`, and `file deletion`. Fuzzy matches from those queries were inspected and did not establish semantic identity for a T1485 claim, case, strategy, analytic, or mitigation. Direct repository URL search confirms **`REF-000513`** already stores the AWS S3 CloudTrail logging page [E12] and can be **reused** for management/data event distinction. The other evidence URLs below had no exact URL match in `niji-matrix/references/` at research time; the primary Agent should recheck the catalog before `create`. `NJT-0117` and `NJS-0111-004` are **scope neighbors**, not reusable T1485 children. Proposed DET/NJA/MIT identities above are **create or split** candidates; do not extend unrelated endpoint, artifact, or generic recovery objects on title similarity alone.

Suggested atomic new claims, all temporary: `TA0040-T1485-CLM-ADAPT` (scope adaptation), `TA0040-T1485-CLM-AGENCY` (policy-to-service actor split), `TA0040-T1485-CLM-VERSION` (view loss differs from permanent loss), `TA0040-T1485-CLM-DETECTION` (configuration-outcome correlation). Suggested case: **none** for the child; a CaddyWiper parent case may be created only if separately scoped to the observed file/partition destruction [E10] and never used to support the lifecycle child. New reference candidates: [E1]–[E11], [E13]–[E15], after canonical URL lookup.

## Evidence ledger (primary sources and claim-level limits)

| Key | Primary URL and locator | Supports; does not support |
| --- | --- | --- |
| E1 | MITRE ATT&CK 19.1 [T1485](https://attack.mitre.org/versions/v19/techniques/T1485/), description and T1561 distinction | File/object destruction, overwrite versus pointer removal, Impact mapping and boundary; no automatic stealth intent. |
| E2 | MITRE ATT&CK 19.1 [T1485.001](https://attack.mitre.org/versions/v19/techniques/T1485/001/), description | Lifecycle-triggered cloud deletion and permission example; research-only ATT&CK child. |
| E3 | AWS [Expiring objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html), versioning table and asynchronous removal | Service action delay, version-state dependent effects; not proof of a victim incident. |
| E4 | Palo Alto Networks [Ransomware in the Cloud](https://www.paloaltonetworks.com/blog/cloud-security/ransomware-data-protection-cloud/), “Indirect Deletion Using Lifecycle Policy” | Explicit attacker model and claimed stealth from avoiding direct object access; simulation/threat analysis, not victim attribution. |
| E5 | AWS [S3 Lifecycle notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configure-notification.html), expiration event example | `LifecycleExpiration` event kinds, service principal, bucket/key/configuration fields; notifications must be enabled. |
| E6 | AWS [S3 EventBridge events](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html), Object Deleted reason and deletion-type | Distinguishes lifecycle expiry from direct DeleteObject and permanent removal from marker creation. |
| E7 | AWS [Object Lock considerations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html), lifecycle and delete markers | Protected versions resist lifecycle deletion; markers may still hide current view. |
| E8 | AWS [Working with delete markers](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html), 404/current-version behavior | Delete marker makes object appear deleted while data version remains. |
| E9 | AWS [Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html), WORM and governance/compliance modes | Retention limits deletion/overwrite; mode and bypass limitations. |
| E10 | ESET [CaddyWiper](https://www.welivesecurity.com/2022/03/15/caddywiper-new-wiper-malware-discovered-ukraine/), observed Ukraine systems | Destructive victim activity at parent level, including data and partition damage; not lifecycle child evidence. |
| E11 | AWS [S3 API permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-policy-actions.html), `PutBucketLifecycle` row | `s3:PutLifecycleConfiguration` is required for rule modification. |
| E12 | AWS [CloudTrail S3 events](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html) and [advanced selectors](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/filtering-data-events.html), lifecycle event source example | Management/data-plane distinction and possibility of excluding `s3lifecycle.amazonaws.com`; canonical first URL already `REF-000513`. |
| E13 | Microsoft [Security event 4660](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4660), event description and 4663 guidance | 4660 confirmation and lack of object name; 4663 DELETE access is useful but may include rename. |
| E14 | AWS [Bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html), lifecycle note | Bucket policy does not block service lifecycle deletion after rule exists. |
| E15 | Microsoft [Security event 4663](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4663), event XML and file monitoring guidance | Supplies object, handle, access, process and subject fields plus SACL requirement; requires careful DELETE semantics. |

## Integration checks for the primary Agent

- Resolve T1485 against T1486, T1561, T1490, T1565 and TA0005 indicator removal; do not let T1485 absorb encryption, disk structure wipe, recovery suppression, integrity distortion, or log cleanup.
- Confirm the single child does not duplicate NJT-0117 selective exclusions, NJS-0111-004 observation-domain encapsulation, or any TA0005 scheduling/guardrail subtype. Its relation is a storage **decision-to-execution agency split**.
- Create/extend exact library identities only after main-agent lookup. Reuse `REF-000513` where applicable. If canonical authoring cannot retain the child-specific evidence limits, defer the child instead of broadening claims.
- Compare every bilingual field with NJT-0001's responsibility checklist. Parent and child paragraphs above are substantive drafts; the main Agent should check schema shape and remove planning citations from final reader prose while attaching canonical evidence refs.
- Keep canonical lifecycle `review` after quality, bundle and Web gates; this handoff itself has no formal ID, decision, or published object.
