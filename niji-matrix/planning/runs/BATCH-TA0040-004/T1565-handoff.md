# T1565 Data Manipulation research handoff

`batch_ref: BATCH-TA0040-004`  
`work_item_ref: WORK-TA0040-T1565`  
`temporary_key_prefix: TA0040-T1565-`  
`status: research-only; integration pending`  
`baseline: Enterprise ATT&CK 19.1`  
`formal IDs allocated: none`

## Recommendation

**Adapt; high confidence; two formal Niji children proposed.** Proposed bilingual admission rationale:

> 数据操纵通过插入、删除或改变仍可被系统或人员消费的数据值、消息或运行时结果，使业务流程、组织理解或决策基于错误状态，直接损害 TA0040 下的数据完整性。Niji 应把正式范围适配为两类跨 stored/transmitted/runtime 状态仍稳定的匿迹设计：恶意值保持业务语法、关系和行为外观，因而像正常记录；或同一业务对象在权威记录、消息、报表和运行时视图之间被攻击者塑造成不一致表示，使某一观察面隐藏真实变化。FIN13 直接证明伪造交易模仿合法行为，APT38/DYEPACK 直接证明数据库、打印消息和 PDF 运行时显示被协同操纵以隐藏 SWIFT 欺诈。[E1][E2][E3]
>
> Data Manipulation inserts, deletes, or changes values, messages, or runtime results that remain consumable by systems or people, causing business processes, organizational understanding, or decisions to rely on false state and directly harming data integrity under TA0040. Niji should adapt the formal scope to two stealth designs stable across stored, transmitted, and runtime states: malicious values preserve business syntax, relationships, and behavioral appearance so they resemble normal records, or the adversary makes one business object inconsistent across authoritative record, message, report, and runtime view so one observation plane conceals the real change. FIN13 directly establishes fraudulent transactions that mimic legitimate behavior, while APT38/DYEPACK directly establishes coordinated manipulation of databases, printer-bound messages, and PDF runtime display to hide SWIFT fraud.[E1][E2][E3]

The parent behavior and both variables are high-confidence. ATT&CK's three state partitions are used only to prove coverage and representation diversity; they are not imported as NJS.

## Required boundary convergence

- **Manipulated but consumable versus NJT-0156 Data Destruction:** T1565 requires that a data object, message, or result remains parseable/readable/processable but carries a false or attacker-selected value that affects process or decision. NJT-0156 owns deletion, overwrite, or object loss that removes intended usability. Deleting one database row can be T1565 when the database remains valid and the missing row falsifies a business record; indiscriminate deletion making the dataset unavailable is destruction. State the consumer result rather than infer from the SQL verb.[E1][L1]
- **Versus NJT-0157 Data Encrypted for Impact:** T1565 leaves data consumable under normal application parsing or keys, though incorrect. NJT-0157 leaves current content unreadable under organizational keys. Encrypted fields intentionally used by an approved application remain consumable only after normal decryption; attacker encryption that breaks this path is NJT-0157, not manipulation.[L2]
- **Versus NJT-0187 Defacement:** NJT-0187 owns unauthorized human-facing content whose visible presentation under an organization identity is the direct impact. T1565 owns business values, messages, records, or runtime results changed to influence a workflow, understanding, or decision. A sanitized PDF hiding a fraudulent transaction is T1565 because the display is an observation of business data; an overt replaced website or banner communicating an attacker message is NJT-0187.[E3][L3]
- **Versus T1657 Financial Theft:** fraudulent transaction data, payment instructions, beneficiary values, or concealed reports are T1565 before settlement and remain evidence of manipulation afterward. T1657 requires completed monetary/digital-asset transfer, extortion payment, or equivalent realized loss to an attacker/beneficiary. One operation may map to both only when data manipulation and actual transfer are independently proven; intent, credentials, or a staged transaction alone do not establish completed theft.[E2][E3][E11]
- **Versus indicator removal/defense impairment:** altering logs or local displays solely to erase attack traces can also belong to the TA0005 evidence/telemetry owners; PHASEJAM-style false health or upgrade feedback is already represented by NJT-0123/NJT-0167. Do not duplicate those children under T1565 unless a separate business-data integrity outcome exists.[E1]

## ATT&CK child coverage and native-axis review

Fixed ATT&CK 19.1 child count: **3**. Breadth trigger: examine at least two materially different axes; this research examined five and proposes two children. Future NJS objects set `lineage.attck_subtechnique_inherited: false`.

| ATT&CK child | Planning-only resolution | Niji conclusion |
| --- | --- | --- |
| T1565.001 Stored Data Manipulation | `niji-variable-candidate` plus `parent-core` remainder | APT38 database-row changes contribute to cross-representation divergence; FIN13 transaction creation supports business-conforming values. Storage location itself does not define a child.[E2][E3][E4] |
| T1565.002 Transmitted Data Manipulation | `niji-variable-candidate` | DYEPACK's printer-bound SWIFT message manipulation and clipboard-address replacement show changes at a handoff; they contribute to representation/provenance analysis, while transport/protocol remains implementation.[E3][E5] |
| T1565.003 Runtime Data Manipulation | `niji-variable-candidate` | DYEPACK.FOX changes PDF data as viewed so operator-visible representation hides fraudulent records; this supports cross-representation divergence rather than a “runtime” child.[E3][E6] |

Open-ended axes examined:

| Candidate Niji axis | Trace and defender-observation effect | Resolution |
| --- | --- | --- |
| Business-semantic conformity | Changed values remain schema-valid and mimic normal transaction patterns, weakening syntactic and isolated-record rules | **Formal child 1: Business-Conforming Value Manipulation**.[E2] |
| Cross-representation integrity divergence | The same business object differs across database, message, printer/PDF/UI, or external settlement; one trusted view hides another | **Formal child 2: Cross-Representation Integrity Divergence**.[E3] |
| Incremental low-amount accumulation | Each change is small while cumulative value becomes large over weeks/months | `evidence-deferred` as a separate child. FIN13 proves the pattern, but current defense can remain a secondary long-window dimension of child 1 rather than a stable sibling independent of semantic conformity.[E2] |
| Authoritative metadata/audit co-mutation | Data and checksum/manifest/audit are changed together so local verification passes | `adjacent/evidence-deferred`. PHASEJAM supports local manifest/feedback co-mutation, but its direct object is appliance image/defense integrity; no broad T1565 business-data evidence supports a separate child.[E1] |
| State location: stored/transmitted/runtime | Different acquisition points and tools | `not-stealth-distinct`; ATT&CK breadth prior only. The same Niji variable can cross all three states.[E4][E5][E6] |
| Record type, database, protocol, file format, renderer, or vendor | Changes implementation and field mapping | `not-stealth-distinct`; no child by medium/product. |
| Actual asset transfer after manipulation | Value leaves victim control | `adjacent outcome`; T1657 once completed.[E11] |

## Proposed parent content (`TA0040-T1565-PARENT`)

Name: **低可区分数据完整性操纵 / Low-Distinguishability Data Integrity Manipulation**  
Aliases: `Data Manipulation`, `T1565`  
Summary:

> 攻击者改变仍可被消费的业务数据，并通过语义合形或跨表示观察差异，让错误值像正常记录或只在未被核对的视图中显现。
>
> Adversaries change business data that remains consumable and use semantic conformity or cross-representation observation differences so false values resemble normal records or appear only in an unreconciled view.

### `definition_and_concept`

> 低可区分数据完整性操纵是攻击者插入、删除或修改业务记录、消息字段、事务属性、配置值或运行时结果，使系统与人员仍能解析、读取或处理对象，却基于攻击者选择的错误状态执行流程、形成理解或作出决定。直接对象是被消费的数据语义及其业务结果，不是 SQL/API 命令、存储/传输/内存位置、文件格式或工具名称。[E1]
>
> Low-Distinguishability Data Integrity Manipulation is adversary insertion, deletion, or modification of business records, message fields, transaction attributes, configuration values, or runtime results so systems and people can still parse, read, or process the object but execute a workflow, form understanding, or make a decision from attacker-selected false state. The direct object is consumed data semantics and business outcome, not a SQL or API command, storage or transmission or memory location, file format, or tool name.[E1]

> Niji 的正式范围要求操纵主动改变防守观察：恶意值要么符合目标业务的合法外观，使字段验证和单记录规则继续通过；要么同一对象在权威源、传输、报表、运行时视图或外部 counterpart 之间产生攻击者控制的不一致，使受信观察面返回经过净化或替换的状态。普通错误数据、公开破坏和没有观察差异的改值不进入适配后的正式范围。[E2][E3]
>
> Formal Niji scope requires manipulation to actively change defensive observation: either malicious values conform to the target business's legitimate appearance so field validation and isolated-record rules continue to pass, or one object diverges under adversary control across authoritative source, transmission, report, runtime view, or external counterpart so a trusted observation plane returns sanitized or substituted state. Ordinary bad data, overt damage, and value changes without an observation difference remain outside the adapted formal scope.[E2][E3]

### `stealth_characteristics`

> 低可区分数据完整性操纵不以格式损坏为必要结果。合形值可满足类型、范围、引用关系和常见交易外观，只在跨主体、受益人、时间或累计金额后显出异常；跨表示操纵则让数据库、消息、报表或 UI 的一个版本看似正常，使依赖单一“权威”视图的守方遗漏矛盾。两者都保留业务可消费性，同时降低基于解析失败、hash 单点或显著离群值的检测能力。[E2][E3]
>
> Low-Distinguishability Data Integrity Manipulation need not damage format. Conforming values can satisfy type, range, referential relationships, and common transaction appearance, surfacing only across principals, beneficiaries, time, or cumulative amount. Cross-representation manipulation makes one database, message, report, or UI version appear normal, causing defenders dependent on one authoritative view to miss contradictions. Both preserve business consumability while weakening detection based on parse failure, one-point hash, or conspicuous outliers.[E2][E3]

> 残余包括写入主体与应用、CDC before/after、事务/record version、trace/request ID、业务 object ID、批准/双人复核、受益方/金额/时间序列、源—消息—输出 semantic digest、组件版本/hash、外部 ack/statement 和最终 settlement。独立 append-only 变更源、跨表示规范化和外部对账能够恢复因果；共享服务账户、缺少前态、非确定渲染和所有表示同时被控会削弱证据。[E7][E8][E9][E10]
>
> Residual evidence includes writer principal and application, CDC before and after state, transaction or record version, trace or request ID, business-object ID, approval or dual control, beneficiary or amount or time sequence, source-to-message-to-output semantic digest, component version or hash, external acknowledgement or statement, and final settlement. Independent append-only change sources, cross-representation canonicalization, and external reconciliation recover causality. Shared service accounts, missing prior state, nondeterministic rendering, and compromise of every representation weaken evidence.[E7][E8][E9][E10]

### `scope_boundary_definition`

> 纳入要求攻击者控制一个数据语义变化，变化后的对象仍被至少一个真实 consumer 成功解析/处理，且业务流程、理解或决定相对可信前态发生可说明的错误结果，同时能证明语义合形或跨表示差异。只存在数据库写入、字段变化、hash 不同、异常 UI 或用户投诉最多是 integrity anomaly；必须连接 writer、object version、consumer 和 outcome。[E1][E7]
>
> Inclusion requires an adversary-controlled semantic data change, successful parsing or processing of the changed object by at least one real consumer, an explainable false business-process, understanding, or decision outcome relative to trusted prior state, and evidence of semantic conformity or cross-representation difference. A database write, field change, different hash, unusual UI, or user complaint alone is an integrity anomaly. Writer, object version, consumer, and outcome must be joined.[E1][E7]

> 不可读/不可恢复的数据归 NJT-0156 或 NJT-0157；直接面向受众的未经授权展示消息归 NJT-0187。资金、数字资产或等价价值实际转移后另记 T1657；仅构造交易或隐藏记录仍是 T1565。正常纠错、账务冲正、schema migration、舍入/本地化、批准批处理、缓存延迟和 A/B 展示是反例。删除日志或伪造防御健康若直接目的为隐藏攻击或削弱工具，还需交由相应 TA0005/TA0112 owner。[E11][L1][L2][L3]
>
> Unreadable or unrecoverable data belongs to NJT-0156 or NJT-0157. Unauthorized display messages directly targeting an audience belong to NJT-0187. Actual transfer of money, digital assets, or equivalent value additionally maps to T1657; constructing a transaction or hiding its record remains T1565. Ordinary correction, reversal, schema migration, rounding or localization, approved batch processing, cache delay, and A/B display are counterexamples. Log deletion or forged defensive health whose direct purpose is hiding attack or weakening a tool also belongs to the relevant TA0005 or TA0112 owner.[E11][L1][L2][L3]

### `application_scenarios_and_threat_model`

Application scenarios:

> 攻击者长期研究金融、ERP、结算或其他关键业务流程后，可以通过应用、脚本或数据库入口插入看似正常的交易/记录，或在记录、打印消息和运行时报表之间隐藏同一欺诈活动。FIN13 以模仿合法行为的交易逐步累积收益；APT38 用 DYEPACK 修改 SWIFT 记录并在打印/PDF 观察面删除痕迹。类似设计也可影响库存、配置、计量、分析或运营决策，但需各自业务语义证据。[E2][E3]
>
> After long study of finance, ERP, settlement, or another critical business process, an adversary can use an application, script, or database path to insert transactions or records that appear normal, or hide one fraudulent activity across records, printer messages, and runtime reports. FIN13 accumulated proceeds through transactions mimicking legitimate behavior. APT38 used DYEPACK to change SWIFT records and remove traces from printer or PDF observation. Similar designs can affect inventory, configuration, metering, analytics, or operational decisions, but each needs its own business-semantic evidence.[E2][E3]

Attacker model:

> 攻击者需要写入业务对象或影响其转换/渲染的权限，理解 schema、约束、正常值分布、审批、受益关系和消费链，并获得测试反馈以避免触发拒绝。合形操纵要求精确业务知识；跨表示操纵要求控制一个或多个 transformer/renderer 并知道哪个视图被审查。最小写权、职责分离、独立日志、端到端签名和外部对账提高成本。[E2][E3]
>
> The adversary needs authority to write business objects or influence their transformation or rendering, understanding of schema, constraints, normal-value distribution, approvals, beneficiary relationships, and consumption chain, and test feedback to avoid rejection. Conforming manipulation requires precise business knowledge. Cross-representation manipulation requires control of one or more transformers or renderers and knowledge of the view reviewers use. Least write authority, separation of duties, independent logs, end-to-end signing, and external reconciliation raise cost.[E2][E3]

Defender model:

> 防守方保留业务对象的稳定 ID、权威前态、CDC/数据库审计、应用 trace、审批与 owner、每次转换/传输/渲染的输入输出关系、外部 counterpart/settlement 以及 consumer 结果，并能按 transaction/object/version/trace 跨分钟到月关联。只做 schema validation、只信本地数据库或只检查 UI/PDF 会漏掉两类子项；没有独立外部事实时所有表示可被共同伪造。[E7][E8][E9][E10]
>
> Defenders retain stable business-object IDs, authoritative prior state, CDC or database audit, application trace, approval and owner, input-output relationships for every transformation, transmission, or rendering, external counterpart or settlement, and consumer outcome, with correlation by transaction, object, version, and trace from minutes to months. Schema validation alone, trust in the local database alone, or UI/PDF inspection alone misses the children. Without an independent external fact, every representation can be forged together.[E7][E8][E9][E10]

### `stealth_mechanisms`

1. `NM-FD`, role `primary`, confidence `high`. Summary: **合形恶意值借用正常业务记录的结构与行为特征 / Conforming malicious values borrow the structure and behavior of normal business records**

> 攻击者根据目标流程生成符合字段类型、关系、金额范围和常见操作路径的错误值，数据继续通过解析与单记录规则并被正常 consumer 使用；恶意语义与合法记录共享特征，守方需要跨时间、主体、受益关系和累计结果才能区分，形成特征伪装。FIN13 的现场观察直接证明交易模仿合法行为。[E2]
>
> The adversary uses knowledge of the target process to generate false values conforming to field type, relationships, amount range, and common operational path. The data continues through parsing and isolated-record rules and is consumed normally. Malicious semantics share features with legitimate records, requiring cross-time, principal, beneficiary, and cumulative-outcome analysis to distinguish them and producing Feature Disguise. FIN13 field observations directly establish transactions mimicking legitimate behavior.[E2]

2. `NM-BT`, role `secondary`, confidence `high`. Summary: **攻击者控制的表示差让受信观察面返回被净化状态 / Adversary-controlled representation differences make a trusted observation plane return sanitized state**

> 攻击者改变数据库/消息中的业务状态并同步修改报表、打印内容或运行时渲染，使审查者看到的表示省略欺诈事实；实际处理与受信显示分离，若防守只查询该观察面，关键变化不进入有效分析，形成行为透明。跨 representation ID、semantic digest、外部 ack 和 settlement 对账能恢复。[E3]
>
> The adversary changes business state in a database or message and also modifies reports, print content, or runtime rendering so the reviewed representation omits the fraudulent fact. Actual processing separates from trusted display, and if defenders query only that observation plane the critical change never enters effective analysis, producing Behavioral Transparency. Cross-representation IDs, semantic digests, external acknowledgements, and settlement reconciliation recover it.[E3]

### `subtechnique_taxonomy`

> 子技术按防守为何接受错误数据划分。业务合形值操纵让单一对象本身符合 schema 与业务常态，检测需要语义基线、累计序列、writer 和 approval；跨表示完整性分歧让同一对象的不同表示不一致，检测需要端到端 object/version/provenance 与独立对账。前者可以只有一个表示，后者即使每个单独表示都看似正常也因表示间矛盾成立；两者可共现但互不蕴含。
>
> Children are divided by why defenders accept false data. Business-Conforming Value Manipulation makes an individual object itself fit schema and business norms, requiring semantic baseline, cumulative sequence, writer, and approval. Cross-Representation Integrity Divergence makes representations of one object inconsistent, requiring end-to-end object, version, and provenance plus independent reconciliation. The first can occur with one representation, while the second can exist even when every individual representation looks normal because their contradiction is decisive. They can co-occur without implying each other.

> ATT&CK stored/transmitted/runtime 子项全部覆盖但不导入。数据状态、协议、数据库、文件格式、renderer 和 vendor 仅决定取证位置。增量低额作为 child 1 的 secondary temporal dimension 保留；完成资产转移、公开展示破坏和防御反馈伪造维持相邻 owner。
>
> ATT&CK stored, transmitted, and runtime children are all covered but not imported. Data state, protocol, database, file format, renderer, and vendor determine evidence location only. Incremental low amounts remain a secondary temporal dimension of child one. Completed asset transfer, overt display damage, and forged defensive feedback retain adjacent owners.

### `research.limitations`

> FIN13 和 APT38 来源直接支持两个子项，但都集中于金融流程，不能证明所有业务系统使用相同约束、表示链或窗口。业务“正常”由本地规则、季节性、用户群和产品版本决定；semantic digest 也需领域规范化。数据库 CDC 可证明 before/after，却不自动证明攻击者、业务错误或 consumer 采用；外部 counterpart 若同样被控则不能作为独立真值。[E2][E3][E7][E8]
>
> FIN13 and APT38 sources directly support both children but concentrate on financial workflows and do not establish identical constraints, representation chains, or windows for every business system. Business normality depends on local rules, seasonality, population, and product version, while semantic digests require domain normalization. Database CDC establishes before and after state but does not automatically prove adversary, business error, or consumer adoption. An external counterpart under the same compromise is not an independent truth source.[E2][E3][E7][E8]

## Proposed child 1 (`TA0040-T1565-CHILD-BUSINESS-CONFORMING-VALUES`)

Name: **业务合形值操纵 / Business-Conforming Value Manipulation**  
Summary:

> 攻击者构造符合 schema、业务关系和常见行为的错误值，使记录继续被正常处理并逃过孤立规则。
>
> Adversaries construct false values conforming to schema, business relationships, and common behavior so records continue through normal processing and evade isolated rules.

### Definition and concept

> 业务合形值操纵以恶意语义保持目标业务的可接受结构和局部行为为稳定变量。攻击者插入或修改交易、计量、库存、配置或其他业务对象，使类型、必填字段、引用、金额/范围和单步审批看似有效，却把流程结果导向攻击者选择。数据位置与工具不构成边界。[E2]
>
> Business-Conforming Value Manipulation uses malicious semantics that preserve acceptable structure and local behavior of the target business as its stable variable. The adversary inserts or changes a transaction, meter, inventory item, configuration, or another business object so types, required fields, references, amount or range, and one-step approval appear valid while the workflow moves toward an attacker-selected result. Data location and tool do not define the boundary.[E2]

### Stealth characteristics

> 业务合形值操纵让 parser、schema、单字段范围和一次交易阈值继续通过，恶意记录混入正常数据。异常可能只在同一 actor/beneficiary 的累计金额、长时序频率、关系图或 application-to-database writer 差异中显现。CDC、审批、peer baseline、累计序列和最终业务结果仍可观察。[E2][E7]
>
> Business-Conforming Value Manipulation lets parsers, schemas, one-field ranges, and per-transaction thresholds continue to pass, mixing the malicious record into normal data. Anomaly may appear only in cumulative amount for one actor or beneficiary, long-horizon frequency, relationship graph, or application-to-database writer difference. CDC, approval, peer baseline, cumulative sequence, and final business outcome remain observable.[E2][E7]

### Scope boundary

> 纳入要求记录可被正常 consumer 成功处理、恶意值符合至少一组本地语义/行为规则、攻击者控制 writer 或输入，并产生错误业务影响。随机损坏、解析失败、明显离群值和单纯低金额不自动属于本项。合法费用、拆分结算、批量导入、测试、纠错和季节性微交易是反例。
>
> Inclusion requires successful processing by a normal consumer, malicious values fitting at least one local semantic or behavioral rule set, adversary control of writer or input, and a false business impact. Random damage, parse failure, conspicuous outlier, and a low amount alone do not qualify. Legitimate fees, split settlement, batch import, testing, correction, and seasonal microtransactions are counterexamples.

### Application scenario

> 攻击者长期观察金融应用和正常交易后，使用已有应用入口、脚本或直接数据库能力创建与客户、金额、渠道和审批外观相容的伪造交易。单笔收益保持不起眼，长期累计形成重大影响；即使后续完成转账另记 T1657，合形记录本身仍是 T1565 证据。[E2]
>
> After long observation of a financial application and normal transactions, an adversary uses an existing application path, script, or direct database capability to create fraudulent transactions compatible with customer, amount, channel, and approval appearance. Individual proceeds remain inconspicuous while long-term accumulation creates material impact. Even when completed transfer additionally maps to T1657, the conforming record remains T1565 evidence.[E2]

### Attacker model

> 攻击者需要领域知识、写权限、正常分布与约束信息以及测试反馈，能够让错误值通过目标 workflow，并可能在发现后休眠再返回。字段级 JIT 写权、独立审批、累计限额和 counterpart 复核会缩小安全操作空间。
>
> The adversary needs domain knowledge, write authority, normal distributions and constraints, and test feedback sufficient for false values to pass the target workflow and can go dormant after discovery before returning. Field-scoped JIT write authority, independent approval, cumulative limits, and counterpart review shrink the safe operating space.

### Defender model

> 防守方按业务对象建立 writer、approval、peer、beneficiary 和 consumer 基线，并跨 24 小时、30 日和更长历史累计；仅依赖 schema 或固定单笔阈值会遗漏。共享服务账户、合法 insider、批处理和新产品分布会弱化归因，需要 before/after 与独立结果补证。
>
> Defenders build writer, approval, peer, beneficiary, and consumer baselines by business object and accumulate over 24 hours, 30 days, and longer history; schema or a fixed per-record threshold alone misses the behavior. Shared service accounts, legitimate insiders, batch processing, and new-product distributions weaken attribution and require before-and-after plus independent outcome evidence.

### Mechanism, defense, and limitations

`NM-FD`, primary, high confidence. Summary: **恶意业务值保留正常记录的结构与局部行为 / Malicious business values preserve normal-record structure and local behavior**.

> 攻击者把错误值约束在目标业务接受的类型、关系、金额和操作序列内，痕迹继续呈现为正常 consumer 可处理的合法形态；字段验证和单笔规则难以分类为恶意，形成特征伪装。跨记录累计、writer/approval 差异和独立 settlement 揭示错误语义。[E2]
>
> The adversary constrains false values to types, relationships, amounts, and operation sequences accepted by the target business, leaving traces in a legitimate form processable by normal consumers. Field validation and per-record rules have difficulty classifying the record as malicious, producing Feature Disguise. Cross-record accumulation, writer or approval differences, and independent settlement expose the false semantics.[E2]

Detection coverage: parent Strategy plus `TA0040-T1565-NJA-CONFORMING-CUMULATIVE-MANIPULATION`. Mitigation coverage: shared Mitigation and child-one application. Temporary claims: `TA0040-T1565-CLM-CONFORMING-VALUES` and `TA0040-T1565-CLM-CONFORMING-DETECTION`; case candidate `TA0040-T1565-CASE-FIN13-CONFORMING-TRANSACTIONS`.

> FIN13 直接证明金融交易的合形与增量累积，但不能提供适用于所有行业的阈值。无完整 before image、审批或最终结果时，检测只能证明异常数据变化；攻击者若控制应用身份和批准链，writer 合法性会失效，必须依靠独立累计与 counterpart。
>
> FIN13 directly establishes financial-transaction conformity and incremental accumulation but cannot provide thresholds for every industry. Without a complete before image, approval, or final outcome, detection proves only anomalous data change. If the adversary controls application identity and approval, writer legitimacy fails and independent accumulation and counterpart evidence become necessary.

## Proposed child 2 (`TA0040-T1565-CHILD-CROSS-REPRESENTATION-DIVERGENCE`)

Name: **跨表示完整性分歧 / Cross-Representation Integrity Divergence**  
Summary:

> 攻击者让同一业务对象在记录、消息、报表或运行时视图中呈现不一致状态，使受信观察面隐藏真实变化。
>
> Adversaries make one business object present inconsistent state across records, messages, reports, or runtime views so a trusted observation plane hides the real change.

### Definition and concept

> 跨表示完整性分歧以同一稳定业务 object ID 的多个表示被攻击者控制地分叉为变量。数据库行、传输消息、打印作业、PDF/UI、外部回执或结算状态中至少两个表示对关键语义字段不一致，且某个 consumer/observer 接受其中错误表示。表示类型和传输介质只是证据位置。[E3]
>
> Cross-Representation Integrity Divergence uses attacker-controlled branching among multiple representations of one stable business-object ID. At least two representations among database row, transmitted message, print job, PDF or UI, external acknowledgement, or settlement state disagree on critical semantic fields, and a consumer or observer accepts the false representation. Representation type and transport medium are evidence locations only.[E3]

### Stealth characteristics

> 跨表示完整性分歧让每个局部系统都可能显示格式正确、来源熟悉的内容；异常只存在于 representation 间。APT38 修改数据库记录、去往打印机的消息及运行时 PDF 显示以移除欺诈痕迹，依赖本地查询或报表的守方因此看不到真实交易。稳定 ID、semantic digest、生成组件 hash、外部 ack 和 settlement 仍能揭示。[E3]
>
> Cross-Representation Integrity Divergence allows each local system to show correctly formatted content from a familiar source, with anomaly existing only between representations. APT38 changed database records, printer-bound messages, and runtime PDF display to remove fraud traces, causing defenders relying on local queries or reports to miss the real transaction. Stable ID, semantic digest, producing-component hash, external acknowledgement, and settlement still reveal it.[E3]

### Scope boundary

> 纳入要求同一业务对象至少两个可比表示、攻击者控制的差分、一个真实 consumer 接受错误表示，以及可说明的业务/观察结果。正常舍入、本地化、脱敏、最终一致性、缓存、模板版本和 redaction 是反例；没有稳定 object/version 对齐时只报告 reconciliation anomaly。公开展示的攻击者消息以展示为直接影响时归 NJT-0187。[L3]
>
> Inclusion requires at least two comparable representations of one business object, an adversary-controlled differential, a real consumer accepting the false representation, and an explainable business or observation outcome. Ordinary rounding, localization, redaction, eventual consistency, caching, template version, and sanitization are counterexamples. Without stable object or version alignment, report only a reconciliation anomaly. An overt attacker message whose direct impact is display belongs to NJT-0187.[L3]

### Application scenario

> 在 SWIFT 环境中，攻击者可以生成或执行欺诈交易，再修改本地 SQL 历史、打印消息或 PDF 打开时的内容，使员工复核看到已净化记录，而远端支付网络或 counterpart 已处理另一状态。该场景也可推广到 ERP、库存、配置或分析管线，但必须证明各表示和 consumer。[E3]
>
> In a SWIFT environment, an adversary can create or execute fraudulent transactions and then alter local SQL history, printer messages, or content as a PDF is opened so reviewers see a sanitized record while the remote payment network or counterpart has processed another state. The scenario can extend to ERP, inventory, configuration, or analytic pipelines only when each representation and consumer is established.[E3]

### Attacker model

> 攻击者需要控制至少一个转换器、消息中间件、数据库、renderer 或报告路径，并知道审查者依赖的表示；若要共同修改多个本地表示，还需稳定 object key、格式/模板知识和测试反馈。端到端签名、隔离 renderer 和外部回执会提高必须同步攻陷的平面数量。
>
> The adversary needs control over at least one transformer, message middleware, database, renderer, or reporting path and knowledge of the representation reviewers trust. Coordinated modification of several local representations additionally requires a stable object key, format or template knowledge, and test feedback. End-to-end signatures, isolated renderers, and external receipts increase the number of planes that must be compromised together.

### Defender model

> 防守方需要端到端 object/transaction ID、每次 transform 输入输出、组件 version/hash、独立外部 receipt/statement 和可规范化 semantic digest。所有本地表示同时被控时，只有外部或硬件保护事实源仍独立；缺少稳定 ID 时只能做时间和内容近似对齐并降低置信度。
>
> Defenders need end-to-end object or transaction ID, every transform input and output, component version or hash, an independent external receipt or statement, and a canonical semantic digest. When all local representations are controlled, only an external or hardware-protected fact source remains independent. Without a stable ID, only approximate temporal and content alignment is possible and confidence must be lowered.

### Mechanism, defense, and limitations

`NM-BT`, primary, high confidence. Summary: **受信视图返回净化表示而真实处理状态位于另一链路 / A trusted view returns a sanitized representation while actual processing state resides on another path**.

> 攻击者让真实业务处理、数据库历史和审查者使用的输出表示分叉，并使受信 renderer/report 返回省略欺诈事实的状态；关键交易发生却未进入该观察面，防守把“无记录”解释为“未发生”，形成行为透明。稳定 object ID、跨表示 semantic digest 和外部 ack/settlement 能恢复。[E3]
>
> The adversary branches actual business processing, database history, and the output representation used by reviewers and makes the trusted renderer or report return state omitting the fraudulent fact. The critical transaction occurs without entering that observation plane, so defenders interpret no record as no event, producing Behavioral Transparency. Stable object ID, cross-representation semantic digest, and external acknowledgement or settlement recover it.[E3]

Detection coverage: parent Strategy plus `TA0040-T1565-NJA-CROSS-REPRESENTATION-RECONCILIATION`. Mitigation coverage: shared Mitigation and child-two application. Temporary claims: `TA0040-T1565-CLM-REPRESENTATION-DIVERGENCE` and `TA0040-T1565-CLM-REPRESENTATION-DETECTION`; case candidate `TA0040-T1565-CASE-APT38-DYEPACK-REPRESENTATION-DIVERGENCE`.

> APT38 直接证明同一 SWIFT 活动在数据库、打印和 PDF 视图上的操纵，但公开报告不会为每个 victim 提供完整 transaction ID、外部 ack 和所有 hash。动态报表、非确定模板和最终一致性会造成正常差分；缺少独立表示时不能把一个被篡改 view 当作唯一真值。
>
> APT38 directly establishes manipulation of one SWIFT activity across database, print, and PDF views, but public reporting does not provide complete transaction IDs, external acknowledgements, and every hash for each victim. Dynamic reports, nondeterministic templates, and eventual consistency create legitimate differentials. Without an independent representation, one manipulated view cannot serve as the sole truth.

## Evidence and shared-library candidates

Suggested parent Claims: `TA0040-T1565-CLM-ADAPT`, `TA0040-T1565-CLM-CONSUMABLE-BOUNDARY`, `TA0040-T1565-CLM-STATE-COVERAGE`, and `TA0040-T1565-CLM-DEFENSE`. Child Claims and Cases are named above.

### Evidence ledger

| Key | Primary source and locator | Supported conclusion and limit |
| --- | --- | --- |
| E1 | Existing `REF-000883`, MITRE ATT&CK 19.1 [T1565 Data Manipulation](https://attack.mitre.org/versions/v19/techniques/T1565/), definition and parent examples | Exact reuse. Parent integrity behavior and three-child inventory; does not establish Niji children alone. |
| E2 | Sygnia IR, [Elephant Beetle](https://www.sygnia.co/threat-reports-and-advisories/elephant-beetle-an-organized-financial-theft-operation/), key points and attack phase 3 | FIN13 observed legitimate business process, created fraudulent transactions mimicking legitimate behavior, and siphoned incremental amounts; financial-sector case, not universal thresholds. |
| E3 | Mandiant/FireEye, [APT38: Un-usual Suspects](https://www.mandiant.com/sites/default/files/2021-09/rpt-apt38-2018-web_v5-1.pdf), DYEPACK section | Database-row, printer-message, and PDF runtime manipulation hiding SWIFT fraud; supports cross-representation child and actual financial-transfer context. |
| E4 | MITRE ATT&CK 19.1 [T1565.001](https://attack.mitre.org/versions/v19/techniques/T1565/001/), definition/examples | Stored-state coverage only; not imported. |
| E5 | MITRE ATT&CK 19.1 [T1565.002](https://attack.mitre.org/versions/v19/techniques/T1565/002/), definition/examples | Handoff/transmitted-state coverage only; not imported. |
| E6 | MITRE ATT&CK 19.1 [T1565.003](https://attack.mitre.org/versions/v19/techniques/T1565/003/), definition/examples | Runtime-view coverage only; not imported. |
| E7 | Debezium, [PostgreSQL connector change-event structure](https://debezium.io/documentation/reference/stable/connectors/postgresql.html), change-event value | Real `before`, `after`, `op`, `source`, `source.ts_ms`, transaction/offset fields for an implementable CDC analytic; tool-specific. |
| E8 | OpenTelemetry, [Database client span semantic conventions](https://opentelemetry.io/docs/specs/semconv/db/database-spans/), attribute table | Real `db.system.name`, `db.namespace`, `db.collection.name`, `db.operation.name`, `db.query.summary`, response/error and server fields; does not provide row before/after. |
| E9 | NIST [Research Data Framework](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/1500-18/NIST.SP.1500-18r2.html), provenance definition | Provenance as attributed record of origin, generation, processing, and alterations; research-data context needs adaptation to enterprise business objects. |
| E10 | NIST [SP 1800-26 Data Integrity](https://www.nccoe.nist.gov/publication/1800-26/VolB/index.html), Detect/Respond architecture | Integrity monitoring, prior-state collection, logging, containment and response principles; not a business-semantic detector or threshold source. |
| E11 | MITRE ATT&CK 19.1 [T1657 Financial Theft](https://attack.mitre.org/versions/v19/techniques/T1657/), definition | Realized monetary-resource loss boundary; user requires completed transfer be kept separate. |
| L1 | Existing `NJT-0156 Data Destruction` | Formal local owner for deletion/overwrite making data unavailable. |
| L2 | Existing `NJT-0157 Data Encrypted for Impact` | Formal local owner for unreadability under organizational keys. |
| L3 | Existing `NJT-0187 Defacement` | Formal local owner for actual unauthorized human-facing display result under organization identity. |

## Exact shared-library lookup and resolution advice

Required `library_lookup.py` searches were run for `data manipulation`, `APT38 DYEPACK`, `Elephant Beetle`, `change data capture before after`, `data integrity provenance`, `cross representation reconciliation`, `NIST SP 1800 26`, `APT38 Un-usual Suspects`, `Sygnia organized financial theft operation`, `Debezium PostgreSQL connector`, `OpenTelemetry database spans`, and `NIST Research Data Framework provenance`.

- **Reuse `REF-000883`** exactly for the fixed T1565 parent.[E1]
- No exact reference match was returned for Sygnia Elephant Beetle, APT38 report, Debezium CDC, OpenTelemetry database spans, NIST RDaF, or NIST SP 1800-26. Recommend `create` after URL-level catalog check.
- `CASE-000241` covers APT38 shell-history `ignorespace`, a different event and proposition. Create a new DYEPACK cross-representation Case.
- No Elephant Beetle case exists; create a FIN13 conforming-transaction Case with the report's two-year observation context and explicit limits.
- `MIT-000152 Shared-Object Authority and Consumer Integrity Governance` protects shared documents/installers and cross-host execution, not business-value semantic invariants or multi-representation reconciliation. Do not extend by generic “integrity” similarity.
- `DET-000112` and nearby representation-differential Analytics concern obfuscated artifacts and execution, not business-object truth. New DET/NJA identities are required.
- Recommended resolutions: References `reuse REF-000883` plus `create` six; Claims `create`; Cases `create` two; Strategy `create`; Analytics `create` two; Mitigation `create`; Relationships defer until formal targets exist.

## Defense design

### Detection Strategy `TA0040-T1565-DET-WRITER-SEMANTICS-REPRESENTATION-OUTCOME`

Name: **写入者—业务语义—表示—结果谱系 / Writer–Business Semantics–Representation–Outcome Lineage**. The Strategy first proves a data change was consumed and affected a process or decision, then uses one Analytic for semantically conforming cumulative manipulation and another for cross-representation reconciliation. Domain `enterprise`; initial implementation targets database-backed financial/business workflows.

### Shared data requirements

1. `change-data-capture`, channel Debezium-style CDC: `payload.before`, `payload.after`, `payload.op`, `payload.source.db`, `payload.source.schema`, `payload.source.table`, `payload.source.ts_ms`, `payload.source.txId` or transaction ID, `payload.source.lsn` or log offset, `payload.ts_ms`, `payload.transaction.id/total_order/data_collection_order`, record key.[E7]
2. `database-client-span`, channel OpenTelemetry traces: `trace_id`, `span_id`, `parent_span_id`, `service.name`, `user.id` when permitted, `db.system.name`, `db.namespace`, `db.collection.name`, `db.operation.name`, `db.query.summary`, `db.response.status_code`, `error.type`, `server.address`, `server.port`, start/end time. Avoid sensitive full query text/parameters unless policy explicitly allows.[E8]
3. `business-object-ledger`, channel application transaction/event journal: `business_object_id`, `event_id`, `record_version`, `event_type`, `actor_id`, `account_id`, `beneficiary_id`, `amount`, `currency`, `source_channel`, `business_process_id`, `status`, `created_at`, `posted_at`, `approver_id`, `approval_id`, `record_hash`, `previous_event_hash`.
4. `representation-provenance`, channel message/report/render pipeline: `business_object_id`, `record_version`, `representation_id`, `representation_type`, `input_representation_ids`, `producer_component_id`, `producer_version`, `producer_hash`, `generated_at`, `semantic_digest`, `content_hash`, `destination`, `render_session_id`, `trace_id`, `message_id`, `print_job_id`.
5. `external-counterpart-settlement`, channel payment network/counterparty/external statement: `business_object_id`, `network_message_id`, `ack_id`, `counterparty_id`, `amount`, `currency`, `status`, `settled_at`, `statement_version`, `receipt_hash`, `signature_result`.
6. `business-change-approval`, channel workflow/change management: `approval_id`, `request_id`, `requested_by`, `approved_by`, `owner_id`, `object_scope`, `allowed_fields`, `expected_before`, `expected_after`, `reason`, `window_start`, `window_end`, `status`.
7. `consumer-outcome`, channel application/user workflow: `timestamp`, `business_object_id`, `consumer_id`, `consumer_component_id`, `representation_id`, `action`, `decision`, `result`, `error_code`, `downstream_object_id`, `trace_id`.

### Analytic 1 `TA0040-T1565-NJA-CONFORMING-CUMULATIVE-MANIPULATION`

Logic:

1. Normalize CDC before/after into a business-object diff and join database writer/application span, approval, and application event by record key, transaction ID, trace ID, and time. Mark direct database writes with no expected service/trace or changed protected fields outside approved scope.
2. Validate parse/schema/referential constraints. A record that fails basic consumption belongs to corruption/destruction triage; this Analytic focuses on records accepted by the normal consumer.
3. Compute semantic features specific to the workflow: actor/account/beneficiary relationships, amount and currency, source channel, approval route, time, peer cohort, historical frequency, and sequence. Compare isolated record and cumulative behavior over **15 minutes, 24 hours, and 30 days**, using at least **90 days** for seasonal/peer baselines. These are reviewable starting windows, not universal thresholds.
4. Establish child 1 when an unauthorized/adversary-linked writer or workflow anomaly produces values that pass local rules and resemble peers, yet cumulative beneficiary/actor/process outcome becomes materially inconsistent with approvals or counterpart. Do not label every fraud anomaly as cyber manipulation without writer/state evidence.
5. Join settlement. If funds/assets actually transfer to an adversary beneficiary, add T1657 relationship; if only record/instruction changed, keep T1565 only.

Observables: application identity directly inserts transactions without matching request/approval; individually small records accumulate to one beneficiary; database before/after fits schema but deviates from actor's long-term relationship graph; writer process or service differs from approved business path.

False positives: fee posting; microtransaction business; split settlement; correction/reversal; migration/backfill; month-end batch; test data; new product/customer cohort; approved emergency operation.

Blind spots: missing before image; shared database account; encrypted/tokenized values; attacker controls application and approval; semantic model lacks local context; sparse legitimate history; insider with valid workflow; external settlement unavailable.

Tuning: bind baselines to process, product, currency, actor role, beneficiary type, calendar and application version; bind exceptions to approval/object/field/time; separately score provenance, semantic plausibility, cumulative result, and settlement; retain anomaly without attribution when writer is unresolved.

### Analytic 2 `TA0040-T1565-NJA-CROSS-REPRESENTATION-RECONCILIATION`

Logic:

1. Assign or recover one stable `business_object_id`/message ID across source record, transmitted message, print job, PDF/report/UI and external acknowledgement. Record each producer and input/output representation.
2. Canonicalize only business-significant fields, excluding allowed formatting, localization, ordering, timestamp, redaction and template variation. Compute a `semantic_digest` per representation and keep content hash plus producer version.
3. Within **five minutes** of each transformation/handoff, compare input/output semantic fields and approval; within **24 hours** reconcile source/local views with an independently controlled counterparty, settlement, statement, or append-only journal. For delayed reports, use workflow-specific SLA rather than force five minutes.
4. Establish child 2 when attacker-linked component/writer causes an unauthorized semantic difference, one consumer accepts the false representation, and independent representation/outcome preserves the conflicting state. One mismatched hash without canonical semantic difference remains formatting/integrity anomaly.
5. For APT38-like cases, join SWIFT/network acknowledgement and settlement to local DB/print/PDF. A local sanitized history plus external processed transaction is high-confidence; if all local and external sources share one compromise domain, lower independence confidence.

Observables: external acknowledgement has a transaction absent from local report; DB record and PDF share object ID but critical amount/beneficiary/status differs; renderer/component hash changes before sanitized output; print message body differs from signed source message without approved transform.

False positives: rounding; timezone/currency conversion; localization; masking/redaction; template upgrade; cache/eventual consistency; replay/retry; PDF nondeterminism; partial report; authorized data correction.

Blind spots: no stable ID; all representations compromised; encrypted payload not canonicalizable; external statement delay; missing producer hash; nondeterministic transformation; separate systems use incompatible semantics; clock skew.

Tuning: define canonical fields and permitted transforms per business object/version; version semantic-digest rules; test normal rounding/redaction/cache; require independent source for high confidence; keep raw evidence and canonicalization version for reproducibility.

### Mitigation `TA0040-T1565-MIT-SEMANTIC-INTEGRITY-PROVENANCE-RECONCILIATION`

Name: **业务语义完整性、端到端来源与独立对账 / Business-Semantic Integrity, End-to-End Provenance, and Independent Reconciliation**.

Measures:

1. `mediated-least-write-authority` (`preventive`): restrict direct database/file/message writes, separate business operator, application service, approver, and database administrator; use field/object-scoped JIT authority and managed write APIs.
2. `tamper-evident-change-history` (`detective-support`): retain CDC before/after, actor/application, transaction/log offset, object version and immutable remote copy; protect history under different authority from production writers.[E7][E10]
3. `semantic-invariants-and-cumulative-limits` (`preventive`): validate cross-field/relationship rules, beneficiary/amount/sequence, dual control and cumulative windows rather than schema and per-record bounds alone.
4. `end-to-end-representation-provenance` (`detective-support`): propagate stable object/version/trace IDs, producer identity/version/hash, approved transform and semantic digest through message, report, print and UI paths.[E9]
5. `independent-reconciliation-and-recovery` (`containment`): compare local state with a separately controlled counterpart/settlement/statement, freeze disputed objects, preserve representations, restore trusted values and replay dependent decisions.[E10]

Parent application:

> 对低可区分数据完整性操纵，把业务对象写入、转换、显示和最终结果建模为一条带稳定 ID 的事务谱系；限制写权，保存不可由生产 writer 删除的前后态，执行语义/累计验证，并以独立 counterpart 对账。发现分歧时冻结相关对象/批次、保全所有表示和审批，恢复可信版本后重新计算受影响决策。
>
> For Low-Distinguishability Data Integrity Manipulation, model business-object write, transformation, display, and final outcome as one transaction lineage with a stable ID. Restrict write authority, retain before and after state that production writers cannot delete, perform semantic and cumulative validation, and reconcile against an independent counterpart. On divergence, freeze the object or batch, preserve every representation and approval, restore a trusted version, and recompute affected decisions.

Expected effect:

> 攻击者必须同时攻陷独立写入、审计、审批和对账平面，否则会留下可检测的语义或来源差异。
>
> The adversary must compromise independent write, audit, approval, and reconciliation planes together or leave detectable semantic or provenance differences.

Limitations:

> 复杂流程与隐私约束可能阻止完整值或日志留存；密码完整性不能证明业务事实正确，错误回滚还可能撤销合法纠错。
>
> Complex workflows and privacy constraints can prevent retention of full values or logs. Cryptographic integrity does not prove business truth, and incorrect rollback can reverse legitimate corrections.

Child 1 application:

> 对业务合形值操纵，使用 relation/beneficiary/amount/channel/time 的跨字段规则、同类与 owner 基线、24 小时和 30 日累计限额及独立审批；禁止生产应用身份直接绕过 workflow 写关键表，异常记录先隔离再结算。
>
> For Business-Conforming Value Manipulation, use cross-field rules over relationships, beneficiary, amount, channel, and time, peer and owner baselines, 24-hour and 30-day cumulative limits, and independent approval. Prevent production application identities from bypassing workflow to write critical tables directly, and quarantine anomalous records before settlement.

Expected effect:

> 局部有效但累计恶意的记录能在形成重大结果前被区分和隔离。
>
> Locally valid but cumulatively malicious records become distinguishable and can be quarantined before material outcome.

Limitations:

> 业务演化会造成基线漂移，insider 可满足审批，低量产品缺少统计样本，僵硬规则可能阻断合法客户。
>
> Business evolution creates baseline drift, insiders can satisfy approvals, low-volume products lack statistical support, and rigid rules can block legitimate customers.

Child 2 application:

> 对跨表示完整性分歧，把 transaction/object ID、version、producer 和 semantic digest 传播到数据库、消息、报表、打印/PDF/UI 与外部 ack；关键转换使用签名/受保护组件并定期从独立 counterpart 重建同一对象，不能把本地报表作为唯一真值。
>
> For Cross-Representation Integrity Divergence, propagate transaction or object ID, version, producer, and semantic digest through database, message, report, print or PDF or UI, and external acknowledgement. Use signed or protected components for critical transforms and periodically reconstruct the same object from an independent counterpart rather than treating a local report as sole truth.

Expected effect:

> 被净化的本地视图会与独立保留的处理证据冲突，从而暴露被操纵的 transform 和受影响对象。
>
> A sanitized local view conflicts with independently retained processing evidence and exposes the manipulated transform and affected object.

Limitations:

> 动态渲染和合法脱敏需要准确规范化，所有表示可能共享同一失陷管线，外部 counterpart 也可能延迟或不可用。
>
> Dynamic rendering and legitimate redaction require accurate canonicalization, every representation can share one compromised pipeline, and external counterpart access can be delayed or unavailable.

Resolution: `create`. Existing integrity mitigations protect artifacts, shared files, images, or specific policy objects; none has the same business-semantic invariants, multi-representation provenance, and independent reconciliation measures.

## Content-depth and integration checks

- Parent and both children cover definition, direct purpose, trace changes, residual observations, scope/counterexamples, scenario, attacker/defender models, mechanisms, evidence, limitations, and defense at NJT-0001 field responsibility depth.
- Do not place ATT&CK child IDs/names or coverage rows in formal YAML. The planning table above is the only imported breadth context.
- Preserve “consumable but false” as the hard parent boundary and real consumer/business outcome as completion. CDC change alone remains anomaly.
- Dual-map T1657 only for completed value transfer; do not infer it from fraudulent record creation. Keep display defacement, destruction, and encryption owners separate.
- Reuse only `REF-000883`; all other References/Cases/Claims and DET/NJA/MIT candidates require central duplicate resolution and allocation.
- Formal child stealth paragraphs must begin with exact bilingual names. Strategy↔Analytics are bidirectional; parent/children point to Strategy, never NJA directly.
- Keep lifecycle `review` after schema, quality, bundle, duplicate, bilingual Web/API, tactic closure, and human-content gates. This handoff allocates no IDs and modifies no canonical/shared/plan object.
