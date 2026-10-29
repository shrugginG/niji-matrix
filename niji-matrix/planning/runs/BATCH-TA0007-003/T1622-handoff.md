# T1622 Debugger Evasion / 调试器规避：TA0007 只读研究交接

工作项 `WORK-TA0007-T1622`；批次 `BATCH-TA0007-003`；临时键前缀 `D07-03-T1622-*`。本交接仅基于批次 brief、`DEC-TA0005-T1622.yaml` 与 NJT-0106 现有父子及防御包，固定 ATT&CK Enterprise 19.1。本文只提交研究，不分配正式 ID，不修改正式矩阵或共享库。

## 1. 结论

**TA0007 独立准入建议为 `retain`，置信度 high；集成建议为 `reuse + extend`，拒绝 `split`。** TA0007 应建立自己的 T1622 准入决议并指向既有 `NJT-0106`；`NJT-0106.classification.tactic_refs` 应由 `[TA0005]` 扩展为 `[TA0005, TA0007]`。父技术、两个现有 Niji 子技术和全部专用防御对象继续复用，不在 TA0007 下复制第二套目录、正文或语义对象。

**新增 NJS 数为 0。** TA0007 复用已经成立的 `NJS-0106-001` 与 `NJS-0106-002`，不表示为 TA0007 新建两个子项。调试状态发现与状态驱动的退出、诱饵或载荷保留属于同一行为事务；战术目的增加没有产生新的稳定匿迹变量、痕迹拓扑或防守观察差异。调试通道饱和仍是 T1622 父包已成立的另一条干扰路径，也不因跨战术纳入而改名或复制。

### 准入理由（zh）

T1622 的直接信息对象是程序是否处于调试观察之下，以及调试通道是否能够完整承载分析事件。读取调试标志、追踪状态、断点或异常差异会得到可用于后继决策的环境事实，因此在 TA0007 下具有独立的 Discovery 目的；当同一结果进一步控制退出、诱饵路径或载荷释放时，它同时产生 TA0005 的观察规避效果。两种战术观察的是同一检查、同一状态结果和同一后继分支，不构成两个可分离的技术事务。既有 NJT-0106 已完整表达状态检查、行为门控、通道干扰、残余痕迹和合法反例，故 TA0007 应保留候选并复用该包，只扩展战术归属。

### Admission rationale (en)

T1622 directly concerns whether a program is under debugger observation and whether the debug channel can carry analysis events completely. Reading debugger flags, tracing state, breakpoints, or exception differences yields an environmental fact that can shape successor behavior, giving the behavior an independent Discovery purpose under TA0007. When that same result controls exit, a decoy path, or payload release, it also produces the observation-evasion effect represented under TA0005. Both tactics refer to the same check, state result, and successor branch rather than two separable technical transactions. NJT-0106 already covers the checks, behavior gating, channel interference, residual traces, and legitimate counterexamples, so TA0007 should retain the candidate, reuse the package, and extend only its tactic membership.

## 2. 父行为证据与证据边界

| 现有对象 | 支持的结论 | 不能推出的结论 |
|---|---|---|
| `REF-000386` | ATT&CK 19.1 T1622 锚定调试器检测、行为改变、线程隐藏、异常处理和调试输出干扰等父行为；`DEC-TA0005-T1622` 与 batch brief 共同确认该候选的固定来源和现有父包。 | ATT&CK 父页不能单独证明每个 Niji 原生轴、Analytic 字段、阈值或缓解效果。 |
| `REF-000414` | Microsoft 文档证明程序可查询用户态调试器存在状态，并可依据返回值改变行为。 | 只证明接口语义；单次调用不能证明恶意目的或稳定行为收敛。 |
| `REF-000415`、`CASE-000138` | P2PInfect 读取 `TracerPid`，并在 `strace` 条件下以特定结果退出，直接支持“调试状态 → 后继分支”因果。 | 单一 Linux 样本不能证明所有平台、字段和调试器实现都具有相同痕迹。 |
| `REF-000416`、`CASE-000139` | Dridex 以大量 `OutputDebugStringW` 调用淹没调试日志，直接支持观察通道饱和。 | 不能把普通异常、少量调试输出或所有线程操作都归为通道饱和；该案例也不单独证明 Discovery 目的。 |
| `CLM-000584`、`CLM-000585` | 支持父技术的两条因果路径和现有 taxonomy 收敛：状态门控与通道饱和具有不可互换的检测方法。 | 不支持按 API、平台、字段、产品或战术名称增加兄弟子项。 |
| `CLM-000621`、`CLM-000622` | 分别支持两个现有 NJS 的稳定变量、痕迹变化和防守差异。 | 不支持线程隐藏/拒绝附加成为第三个正式子项。 |

证据分层结论：父行为与两个既有子项均有结论级支持；TA0007 的独立准入由“调试状态是后继行为所使用的环境事实”成立。现有证据不足以建立第三个 NJS，也没有证据表明 TA0007 需要与 TA0005 分裂为同义父技术。

## 3. Niji 原生轴复核

固定版 ATT&CK 子技术数为 `0`，ID 为 `[]`，`original_attack_subtechniques_imported: false`。零子项不免除开放搜索；本轮按稳定变量、痕迹变化和防守观察差异复核如下。

| 原生轴 | 可控变量与因果链 | 决议 |
|---|---|---|
| 调试状态条件化行为收敛 | 攻击者控制调试状态检查与后继分支关系 → 被调试运行只留下查询、提前退出、诱饵或缺失载荷 → 单次被调试分析无法观察真实路径；需要调试开启/关闭/透明插桩结果差分。 | **formal，reuse `NJS-0106-001`**。证据与专用防御已成立，不新建 NJS。 |
| 调试观察通道饱和 | 攻击者控制低价值调试或异常事件的密度 → 有意义状态转折被巨量重复事件包围，通道可能丢失、截断或延迟 → 防守方需分析事件价值、通道健康和外部结果。 | **formal，reuse `NJS-0106-002`**。证据与专用防御已成立，不新建 NJS。 |
| 线程隐藏与拒绝附加 | 攻击者可能隐藏线程、拒绝调试器附加或分离进程 → 调试器视图可能缺少线程或失去控制 → 理论上需要跨层线程状态及附加结果差分。 | **defer / parent-core**。现有包只由父页证明实现存在，缺独立结论级来源和不可互换的子级防御边界。 |
| API、状态字段、操作系统、调试器产品 | 更换 `IsDebuggerPresent`、`TracerPid`、PEB、断点、异常类型或工具 → 改变实现细节，但仍落入状态门控或通道饱和的既有痕迹拓扑。 | **reject**。实现和载体不是稳定匿迹变量。 |
| 仅搜索调试器进程名、窗口名或字符串 | 搜索得到工具存在信息，但若未与退出、诱饵、载荷保留或观察通道损坏相连，只能证明环境发现。 | **reject as NJS / boundary**。有稳定后继差分时归 `NJS-0106-001`；无差分时不满足 NJT-0106 的 Niji 匿迹因果门禁。 |

**分类结论：** 现有两个 NJS 已覆盖可证且防御不可互换的变量。TA0007 本轮新增正式子项 `0`；defer 轴不得预留 ID，reject 轴不得以新名称复制正文或防御。

## 4. `reuse + extend` 与 `split` 判定

| 判定问题 | 结果 |
|---|---|
| 直接对象是否不同 | 否。TA0007 与 TA0005 都读取同一调试观察状态，或作用于同一调试观察通道。 |
| 行为事务是否可分 | 否。检查、状态结果和后继分支形成一个连续事务；按战术名称拆分会重复该事务。 |
| 痕迹拓扑是否不同 | 否。状态查询、追踪字段、异常、线程状态、调试输出以及后继结果保持相同。 |
| 防御目标是否不同 | 否。仍由调试状态—行为结果差分和通道饱和分析检测，并由观察韧性控制缓解。 |
| 是否需要新父正文或同义子项 | 否。既有 NJT/NJS 已完整承担字段责任。 |

因此拒绝 `split`。主 Agent 集成时应创建 TA0007 自己的 retain 决议并令其 `resulting_technique_ref` 指向 `NJT-0106`；只扩展 `NJT-0106.classification.tactic_refs`。现有 technique 的单值 `classification.decision_ref` 可继续指向原始 `DEC-TA0005-T1622`，额外 TA0007 决议从战术侧反向指向同一 NJT；不得复制 technique 目录。

一个表示限制需要在主审中保留：`NJS-0106-002` 的直接行为是干扰调试通道，本身未必产生“学到调试状态”的 Discovery 结果。它仍属于完整 T1622 父包，但事件级 TA0007 归因应要求状态或调试工件被实际读取并用于后继判断；只有通道洪泛而无状态学习的事件应按 TA0005 语境解释。该限制不构成拆分同义父技术的理由。

## 5. 父级双语核心字段：复用 NJT-0106

以下内容用于确认 TA0007 复用后的字段语义；建议保持现有正式正文，不另写第二套父技术。

**name / summary**

- zh：调试器规避。攻击者检查或干扰调试环境，并依据结果隐藏核心功能、退出或改变执行，使分析人员只能观察受限路径。
- en: Debugger Evasion. Adversaries inspect or interfere with a debugging environment and hide core functions, exit, or alter execution according to the result, limiting analysts to a restricted path.

**definition_and_concept**

- zh：调试器规避是程序识别调试观察状态或主动削弱调试通道，并使所得状态或通道条件控制后续执行的行为。TA0007 所关注的信息结果是是否存在调试观察；TA0005 所关注的匿迹结果是退出、诱饵、载荷保留或观察完整性下降。二者共享同一行为事务。API、平台和工具只是实现，只有与调试观察目的及后继行为差异相连时才纳入。
- en: Debugger Evasion occurs when a program identifies debugger observation or actively weakens the debug channel and allows the resulting state or channel condition to control successor execution. TA0007 concerns the learned fact of whether debugger observation exists, while TA0005 concerns exit, decoy execution, payload withholding, or reduced observation completeness. Both are views of one behavioral transaction. APIs, platforms, and tools are implementations and qualify only when connected to debugger observation and a successor behavior difference.

**stealth_characteristics**

- zh：同一程序可在被观察与未被观察时呈现不同路径，或用大量低价值事件稀释有意义状态转折。防守方可能只看到退出、诱饵、缺失的后继载荷或被噪声占据的调试记录。残余痕迹包括状态查询、追踪文件读取、异常模式、线程操作、密集调试字符串和检查后的稳定分支；受控差分、多视角插桩及外部文件网络观察可恢复因果。
- en: The same program can present different paths under observed and unobserved conditions or dilute meaningful state transitions with large volumes of low-value events. A defender may see only exit, a decoy, an absent successor payload, or a noise-filled debug record. Residual traces include state queries, tracing-file reads, exception patterns, thread operations, dense debug strings, and stable post-check branches; controlled differential, multiview instrumentation, and external file or network observation can recover causality.

**scope_boundary_definition**

- zh：纳入以识别调试器、隐藏调试可见执行、阻止附加、操纵异常或淹没调试通道为目的，并实际改变分析可见性或后继行为的活动。单次 API、字符串或进程名不足以定性。合法反篡改、反作弊、DRM、崩溃处理、性能分析和开发诊断是强反例；虚拟机/沙箱环境检查、普通进程发现、安全工具发现和单纯耗时行为保留给相邻技术。
- en: Scope includes activity intended to identify a debugger, hide debugger-visible execution, prevent attachment, manipulate exceptions, or flood the debug channel when it actually changes analysis visibility or successor behavior. One API call, string, or process name is insufficient. Legitimate anti-tamper, anti-cheat, DRM, crash handling, profiling, and developer diagnostics are strong counterexamples. Virtual-machine or sandbox checks, ordinary process discovery, security-tool discovery, and mere time consumption remain with adjacent techniques.

**application_scenarios_and_threat_model**

- zh：载荷可在入口、解包、网络通信或下一阶段释放前检查调试标志、`TracerPid`、PEB、断点、异常传递或时间差，发现观察后退出、执行诱饵或保留载荷；也可隐藏线程或持续产生调试噪声。攻击者需要理解目标平台调试语义并控制分支或事件生成，但会受到状态伪造、多视角观察、资源消耗和误判真实目标的限制。防守方需观察查询、异常、线程、输出、进程寿命及文件网络结果，并保留调试开启、关闭和透明插桩对照；单一用户态调试器、缺少内核视图或没有对照运行形成主要盲区。
- en: A payload may check debugger flags, `TracerPid`, PEB state, breakpoints, exception delivery, or timing before entry, unpacking, networking, or next-stage release, then exit, run a decoy, or withhold the payload after observation is found; it may also hide threads or generate sustained debug noise. The adversary must understand platform debugging semantics and control branching or event generation, but state forgery, multiview observation, resource cost, and false rejection of a real target constrain the design. The defender needs visibility into queries, exceptions, threads, output, process lifetime, and file or network outcomes together with debugging-on, debugging-off, and transparent-instrumentation controls. A single user-mode debugger, missing kernel visibility, or no control run creates major blind spots.

**stealth mechanisms**

- `NM-BT` primary：调试状态把核心行为门控在分析观察之外 / Debug state gates core behavior outside analysis observation。查询后的退出或载荷保留把完整执行痕迹收敛为状态读取和替代分支，使未进入运行的真实路径无法被直接观察；复用 `REF-000386/414/415`，high。
- `NM-FD` secondary：异常与调试输出噪声稀释有意义分析信号 / Exception and debug-output noise dilute meaningful analysis signals。高密度低价值事件把少量真实状态转折埋入重复噪声，迫使通道丢失、采样或降低分析深度；复用 `REF-000386/416`，high。

**limitations**

- zh：状态门控证据集中于 Windows 接口语义与一个 Linux 样本，不能跨平台类推具体字段；合法保护软件会使用相同查询。通道饱和的高置信结论限于可观察的高密度低价值事件及其通道影响，不能扩展到所有异常或线程操作。没有调试开关结果差分、事件价值/密度和通道健康证据时，应只记录父行为线索，不确认恶意匿迹。
- en: State-gating evidence is concentrated in Windows interface semantics and one Linux sample and does not generalize individual fields across platforms; legitimate protection software uses the same queries. High confidence for channel saturation is limited to observable high-density low-value events and their channel effect and does not extend to every exception or thread operation. Without debugger-state outcome differential or evidence of event value, density, and channel health, record only a parent-level lead rather than confirmed malicious stealth.

## 6. 子级双语核心字段：复用既有两个 NJS

### `NJS-0106-001` 调试状态条件化行为收敛 / Debug-State-Conditioned Behavior Contraction

**summary / definition：** zh：程序读取调试器存在状态，并在被调试时稳定退出、进入诱饵路径或保留核心载荷；稳定变量是调试状态对真实后继行为的负向门控，而非 API 或操作系统。en: A program reads debugger-presence state and consistently exits, selects a decoy path, or withholds a core payload when debugging is present; the stable variable is negative gating of true successor behavior by debugger state rather than an API or operating system.

**stealth / scope：** zh：调试开启与关闭条件下出现不同控制流、载荷阶段和外部结果；需把状态读取连接到退出、缺失解码、子进程、文件或网络阶段。单次查询、字符串或调试器进程发现不足；虚拟机/沙箱门控属于相邻技术，通道饱和归 `NJS-0106-002`。en: Debugging-on and debugging-off conditions produce different control flow, payload stages, and external outcomes; a state read must connect to exit or missing decoding, child-process, file, or network stages. One query, string, or debugger-process discovery is insufficient. Virtual-machine or sandbox gating belongs to an adjacent technique, and channel saturation belongs to `NJS-0106-002`.

**scenario / models / mechanism：** zh：载荷在核心阶段前读取调试状态，发现观察后终止或不释放后继阶段。攻击者需要可靠状态访问和分支控制；防守方按样本和进程 start key 比较调试开启、关闭与透明插桩运行。`NM-BT` 为 primary，证据 `REF-000414/415`，high。en: A payload reads debugger state before a core stage and terminates or withholds the successor when observation is found. The adversary needs reliable state access and branch control; the defender compares debugging-on, debugging-off, and transparent-instrumentation runs by sample and process start key. `NM-BT` is primary with `REF-000414/415`, high confidence.

**limitations：** zh：缺少未调试对照、外部结果或透明观察时，只能证明查询存在；合法反作弊、DRM 和反篡改是主要反例。en: Without an undebugged control, external outcomes, or transparent observation, only the query is established; legitimate anti-cheat, DRM, and anti-tamper software are primary counterexamples.

### `NJS-0106-002` 调试观察通道饱和 / Debug Observation-Channel Saturation

**summary / definition：** zh：程序反复生成无意义调试消息或异常事件，占用调试通道的事件、存储和分析预算；稳定变量是高密度低价值事件对观察通道资源的消耗。en: A program repeatedly generates meaningless debug messages or exception events to consume debug-channel event, storage, and analyst budgets; the stable variable is consumption of observation-channel resources by high-density low-value events.

**stealth / scope：** zh：可审查事件序列被改变为少量有效状态转折与巨量重复噪声的混合，通道可能采样、丢失、截断或延迟。判定需同时看到密度、重复性、低信息价值、核心执行继续和通道影响；存在 `OutputDebugString` 或异常本身不足。en: A reviewable event sequence becomes a mixture of a few meaningful transitions and massive repetitive noise, causing sampling, loss, truncation, or delay. Classification requires density, repetition, low information value, continued core execution, and channel effect together; the presence of `OutputDebugString` or an exception alone is insufficient.

**scenario / models / mechanism：** zh：loader 可在解包或主载荷执行期间循环输出调试字符串。攻击者需要持续生成通道可接收的事件而不阻断关键路径；防守方观察每进程/线程事件率、模板、队列、丢失、存储、CPU 和噪声期间的外部结果。`NM-FD` 为 primary，证据 `REF-000416`，high。en: A loader may loop over debug-string emission while unpacking or running its main payload. The adversary must sustain events accepted by the channel without blocking the critical path; the defender observes per-process or per-thread event rate, templates, queue, loss, storage, CPU, and external outcomes during noise. `NM-FD` is primary with `REF-000416`, high confidence.

**limitations：** zh：Dridex 证据不能推广到所有异常或线程操作；开发调试、压力测试、崩溃风暴和模糊测试可产生相似密度。只有通道资源或信号完整性确受影响时才确认。en: The Dridex evidence does not generalize to every exception or thread operation; development debugging, stress tests, crash storms, and fuzzing can produce similar density. Confirm the child only when channel resources or signal integrity are materially affected.

## 7. DET / NJA / MIT 复用决议

### 状态门控路径

**`DET-000103`：reuse unchanged。** 检测目标仍是调试状态与后继结果之间的稳定条件关系，覆盖 `NJT-0106` 和 `NJS-0106-001`。TA0007 没有改变检测主体，因此无需复制或扩展 `detects_refs`。

**`NJA-000088`：reuse unchanged。** 按 `sample.hash` 与 `process.start_key` 记录调试状态 API、`/proc` 追踪字段、PEB、断点/异常检查及后继分支；对同一样本执行调试开启、关闭和透明插桩重运行，比较退出码、进程寿命、解码、子进程、文件与网络结果。窗口覆盖每次样本完整寿命并延伸到正常下一阶段触发上限；关键关联维度为主机、样本、进程 start key、debug state、operation、branch 和 payload stage。误报包括反作弊、DRM、软件保护、崩溃处理和调试测试；盲区包括用户态插桩绕过、内核状态不可见、非确定样本和无对照运行。调优必须按签名、产品、版本和业务用途建立合法基线，不能以函数名或一次退出告警。

### 通道饱和路径

**`DET-000122`：reuse unchanged。** 检测目标仍是高密度低价值调试/异常事件对通道丢失、存储、延迟和分析预算的影响，覆盖 `NJT-0106` 与 `NJS-0106-002`。

**`NJA-000108`：reuse unchanged。** 按进程和线程归一调试字符串模板、异常类型、数量和信息增益，并关联队列深度、丢失/采样计数、截断、日志字节、CPU、处理延迟及噪声期间的子进程、文件和网络结果。窗口覆盖进程内噪声区间及紧邻外部结果；维度为主机、进程 start key、线程、事件类型、模板和载荷阶段。误报包括详细开发调试、压力测试、崩溃风暴、模糊测试和诊断采样；盲区包括无队列/丢失指标、静默截断和样本绕开已观察通道。调优应按环境建立密度与模板基线，限速时保留总量、丢失、模板数和核心状态转折，不使用跨产品固定阈值。

### 缓解

**`MIT-000105`：reuse unchanged。** 现有三个 Measure——透明多视角插桩、调试状态差分重执行、调试通道资源边界与可观察压缩——已经直接适用于 `NJT-0106`、`NJS-0106-001` 和 `NJS-0106-002`。TA0007 复用相同 target refs，不新增 Application。

实施效果与限制保持现有结论：多视角和差分运行可恢复被状态门控隐藏的路径；每进程/线程资源边界、重复模板压缩和丢失指标可限制通道洪泛。它们增加分析时间和基础设施成本，可能受非确定行为、多层环境检查和日志实现差异影响；限速或压缩还可能丢失低频高价值事件，须保留未压缩样本用于调优。

## 8. 共享库与集成决议

| 对象 | 决议 | 限制或主 Agent 动作 |
|---|---|---|
| `NJT-0106` | **reuse + extend** | 只增加 `TA0007` 到 `classification.tactic_refs`；不复制目录，正文原则上复用。 |
| `NJS-0106-001`、`NJS-0106-002` | **reuse unchanged** | 新增 NJS 为 0；不得按 Discovery 名称重建同义子项。 |
| `REF-000386/414/415/416` | **reuse unchanged** | 证据强度保持各自层级；不由父页越级证明子项或检测效果。 |
| `CLM-000584/585/621/622` | **reuse unchanged** | 已覆盖父级相关性、taxonomy 边界和两个子项存在性；不新建 TA0007 同义 Claim。 |
| `CASE-000138/139` | **reuse unchanged** | P2PInfect 只支持状态门控；Dridex 只支持通道饱和，二者不可交叉扩张。 |
| `DET-000103/122`、`NJA-000088/108` | **reuse unchanged** | 检测目标、数据、关联和调优均由行为决定，未因战术增加而变化。 |
| `MIT-000105` | **reuse unchanged** | 既有 Applications 已指向同一 NJT/NJS；无需按战术增加重复 Application。 |
| TA0007 的 T1622 准入决议 | **create by primary agent** | `decision: retain`，`resulting_technique_ref: NJT-0106`，证据复用现有 REF；本研究者不写正式 decision。 |
| 新 REF/CLM/CASE/DET/NJA/MIT/REL | **create: none** | 没有语义缺口；不分配共享 ID。 |
| 线程隐藏/拒绝附加第三子项 | **defer** | 等待独立结论级来源、稳定痕迹差和不可互换防御。 |

## 9. 主审集成限制与验收点

1. TA0007 的 retain 决议必须明确“Discovery 是同一调试状态事务的信息目的”，不能把战术名称当作 split 理由。
2. `NJT-0106` 只扩展战术归属；保留原始 `decision_ref`，由 TA0007 决议反向指向既有 NJT。若现行校验器要求其他结构，应按既有跨战术技术先例处理，不能复制 NJT。
3. 新增正式 NJS、共享语义对象和关系均为 0；defer/reject 轴不得预留 ID。
4. TA0007 事件级归因要求实际取得调试状态或调试工件信息；纯通道洪泛主要表达 TA0005 的干扰目的。父级战术继承无法表达每个子项对每个战术的强度差异，这是当前模型限制。
5. 单次 API、进程名、字符串、异常或高事件量均不足以定性。合法反篡改、反作弊、DRM、崩溃处理、性能分析、开发诊断和压力测试必须保留为显式反例。
6. 现有父子与防御包仍处于 `review`，没有人工领域 reviewer。主 Agent 完成 tactic ref、决议和计划更新后，应重新执行质量、Bundle 与双语 Web 门禁；本交接不声称这些集成门禁已经通过。

**最终交接状态：** `retain`；`reuse NJT-0106 + extend tactic_refs with TA0007`；复用 `NJS-0106-001/-002`；新增 NJS `0`；`split` 拒绝；新共享对象 `0`；线程隐藏/拒绝附加继续 `defer`。
