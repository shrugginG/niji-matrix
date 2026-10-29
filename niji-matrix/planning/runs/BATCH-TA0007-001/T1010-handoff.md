# T1010 Application Window Discovery / 应用窗口发现：只读研究交接

- 批次：`BATCH-TA0007-001`；工作项：`WORK-TA0007-T1010`；暂存键前缀：`D07-01-T1010-*`。
- 基线：工作区 `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx` 的 `techniques` 表。T1010 为 Enterprise 19.1 的 Discovery 父项，Windows、Linux、macOS，`is sub-technique=0`；以 `sub-technique of=T1010` 核对后为 **0 个 ATT&CK 子项**。在线 ATT&CK 页面可更新，只作来源说明，不替换本地冻结行。
- 研究性质：准入和暂存设计，供主 Agent 收敛。`original_attack_subtechniques_imported: false`。本文未分配正式 ID，未更动矩阵或共享库。

## 1. 准入建议：retain（中等置信度）

**中文理由。** 保留 T1010 原有的信息对象：攻击者读取当前或近期开放的应用窗口、标题、前台焦点或可见交互上下文，以判断用户正在使用什么、何时采取后续行动。冻结的 ATT&CK 行和多个研究案例直接证明父行为；Grandoreiro 在银行窗口标题命中之前不启动 C2，Attor 只对匹配进程名或窗口标题的应用截屏，显示窗口上下文可以控制恶意活动的出现时间与范围。匿迹价值来自这种有意设计和普通 GUI 查询较弱的默认可见性，而不是声称任何窗口查询本身都恶意或隐蔽。父定义保持 T1010，Niji 论证只纳入有证据的观察差异；未证明的事件式、平台式和辅助功能式细分暂缓。

**English rationale.** Retain T1010's original information object: an adversary reads open or recently active application windows, titles, foreground focus, or visible interaction context to learn what a user is doing and when to act. The frozen ATT&CK row and independent research cases establish the parent behavior. Grandoreiro withholds C2 until a banking window title matches, while Attor captures only selected applications whose process name or window title matches. Window context can therefore control when and where malicious follow-on activity appears. The stealth argument rests on this deliberate design and on limited default visibility into ordinary GUI reads; it does not classify every window query as malicious or stealthy. Keep unproven event, platform, and accessibility partitions deferred.

**准入范围。** 窗口状态是直接取得的信息对象；标题中偶然出现用户名、文档名或软件名不改变主归属。若只枚举 PID、可执行文件和进程名，归 T1057；只查已安装软件及版本，归 T1518；用窗口稳定性或用户活动判定分析环境并改变载荷，判断部分归 T1497。后续截屏、输入捕获、浏览器脚本注入、C2 通信各自保留其相邻技术归属；它们在此仅用于证明窗口查询的门控结果。

## 2. 结论级证据表

| 暂存源键 | 一手来源与可核查 URL | 精确支持 | 不支持或须限制的结论 |
|---|---|---|---|
| `D07-01-T1010-REF-ATTACK` | 本地固定工作簿上述 T1010 行；[MITRE T1010](https://attack.mitre.org/techniques/T1010/) | 父行为、Discovery、平台、无 ATT&CK 子项；官方列有窗口标题、前台窗口和工具实例 | 在线页随版本变化；不证明任何 Niji 子项、匿迹意图或具体日志字段 |
| `D07-01-T1010-REF-GRANDOREIRO24` | [ESET，Grandoreiro 长期跟踪](https://www.welivesecurity.com/en/eset-research/eset-takes-part-global-operation-disrupt-grandoreiro-banking-trojan/)，Background 第 54–55 行附近 | 周期检查浏览器前台窗口；银行相关标题匹配后才启动至少每秒一次的 C2 请求。支持“窗口谓词 → 后继网络活动”以及非目标情境下较少 C2 痕迹 | 并未证明窗口 API 调用完全无日志，也未证明所有 Grandoreiro 版本均如此；“降低检测概率”是由活动缺席推得，未量化 |
| `D07-01-T1010-REF-ATTOR` | [ESET，Attor 样本分析](https://www.welivesecurity.com/2019/10/10/eset-discovers-attor-spy-platform/)，目标应用与插件部分 | 仅对进程名或窗口标题含指定子串的应用截图；证明选择性后继收集 | 进程名与标题共同作谓词，不能把该案例说成纯标题门控；未测量截图减少幅度 |
| `REF-000245`（已有） | [ESET，BackSwap 样本分析](https://www.welivesecurity.com/2018/05/25/backswap-malware-empty-bank-accounts/) | WinEvent/可访问性对象与 URL、标题结合，识别银行转账情境后才注入脚本；证明事件驱动读取与门控后继输入可共存 | 既有 `CASE-000085`、`CLM-000449` 的语义中心是输入注入；不能直接用它们证明独立 T1010 匿迹子项或“事件式比轮询更难检测” |
| `D07-01-T1010-REF-WINAPI` | [Microsoft EnumWindows](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows)、[GetForegroundWindow](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getforegroundwindow)、[GetWindowText](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtexta) | 顶层窗口枚举、只取前台句柄与标题读取是不同的 API 语义；GetWindowText 对其他进程的控件文本有限制 | API 能力本身不是恶意案例；标题不能等同浏览器 URL、控件内容或所有应用窗口 |
| `D07-01-T1010-REF-WINEVENT` | [Microsoft SetWinEventHook](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook)、[WinEvents](https://learn.microsoft.com/en-us/windows/win32/winauto/what-are-winevents) | 客户端可选事件范围、进程/线程范围并接收窗口焦点、名称等事件；给事件式轴和辅助功能反例提供平台机制 | 注册 hook 不证明攻击意图，也不保证系统有默认可查询的 hook 注册日志 |
| `D07-01-T1010-REF-BENIGN` | [Microsoft UI Automation](https://learn.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32)、[辅助功能安全考虑](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-securityoverview)、[Power Automate 桌面 UI 动作](https://learn.microsoft.com/en-us/power-automate/desktop-flows/actions-reference/uiautomation) | 屏幕阅读器、自动化测试、桌面流程合法获取窗口信息；Power Automate 可获取标题、按标题定位和等待窗口焦点 | `uiAccess` 只约束特定受保护 UI 访问；不能把禁用该标志称为普遍阻止 EnumWindows 或窗口标题读取 |
| `REF-000366`（已有） | [Microsoft Sysmon 事件说明](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-events) | Event 1 为进程创建，3 为网络连接，10 为跨进程访问；可作为来源/后继关联 | **Event 10 不记录普通 EnumWindows/GetForegroundWindow 调用**。ATT&CK DET0097 的 `AccessedFunction` 示例不能当作 Sysmon 10 的原生字段保证 |
| `D07-01-T1010-REF-DET0097` | [MITRE DET0097](https://attack.mitre.org/detectionstrategies/DET0097/) | 官方提出跨平台窗口查询检测方向与脚本、进程关联线索 | 其通道清单需按实际产品核验；Linux `/proc/*/window` 不是通用窗口映射保证；本文不照搬其字段假设 |
| `D07-01-T1010-REF-ADJACENT` | [MITRE T1057](https://attack.mitre.org/techniques/T1057/)、[T1518](https://attack.mitre.org/techniques/T1518/)、[T1497](https://attack.mitre.org/techniques/T1497/) | 分别锚定进程清单、已安装软件、分析环境判断的相邻对象 | 不能仅凭工具同时调用窗口与进程 API 就把所有行为并入 T1010 |

**原子结论候选。** `D07-01-T1010-CLM-PARENT`：恶意样本利用窗口标题或前台状态选择后续目标，父级 T1010 与匿迹研究相关；证据为固定行、Grandoreiro、Attor，置信度 medium。`D07-01-T1010-CLM-GATE`：当窗口谓词未匹配时，Grandoreiro 不启动 C2，匹配后启动高频 C2；这是条件导致网络痕迹出现与否的直接案例事实，置信度 high，推论“低于常驻通信的可观察性”降为 medium。`D07-01-T1010-CLM-TELEMETRY`：标准 Sysmon 10 记录跨进程访问，不能单独证实 GUI API 调用；由 Microsoft 文档与 API 语义共同支持，置信度 high。`D07-01-T1010-CASE-GRANDOREIRO`：若新建案例，仅写 ESET 实际分析的前台窗口、标题谓词和 C2 门控；不推断具体 API、感染规模或检测失败率。

## 3. ATT&CK 广度先验与 Niji 原生变量搜索

固定子项数为 **0**，子项 ID 清单为空，代表维度为空；没有 ATT&CK 子项覆盖行。仍从“行为设计 → 痕迹变化 → 防守观察”开放搜索。不是按 Windows/Linux/macOS、窗口/标题/焦点字段、API/脚本、工具家族或攻击目标命名 NJS。

| 候选轴与暂存决议 | 攻击者可控变量及前提 | 痕迹变化和防守差异 | 证据与理由 |
|---|---|---|---|
| **窗口上下文门控后继活动**，建议正式子项 1 个，主 Agent 审核 | 可配置标题/前台状态谓词；已有交互桌面及可读取窗口状态；只有匹配时启动 C2、截图或其他动作 | 非目标情境下缺少后继网络/收集事件，目标情境出现短时高强度链；检测须关联窗口谓词、同一主体及后继结果，而非仅数 API 次数 | Grandoreiro 为直接“无匹配无 C2”证据，Attor 为选择性截图证据；BackSwap 支持相邻输入门控但不扩张结论。**匿迹效果是中等置信度推断，不是来源声称的测量值** |
| 事件触发读取相对于轮询，`evidence-deferred` | 注册焦点/名称变化 hook，等待事件再读，而非固定频率调用；需要消息循环或可访问性接口 | 可能减少无变化期间的查询次数，但保留 hook 注册和回调；防守需看注册、来源与结果 | BackSwap 与 Microsoft 证明可实现，尚缺同等任务下的可核查痕迹比较和独立于窗口门控的防御价值，暂不成项 |
| 仅取前台窗口相对于全窗口枚举，`evidence-deferred` | 攻击者选择 `GetForegroundWindow` 等单对象读取；必须等待目标成为前台 | 理论上少读非前台对象，可能降低调用/结果体量；但更易漏目标 | Microsoft 仅证明 API 范围差异，Grandoreiro 使用前台还同时依赖标题门控；现有证据不能拆成独立稳定匿迹边界 |
| 借辅助功能/UI 自动化或可信窗口管理器，`evidence-deferred` | 取得 UIA/WinEvent 或自动化环境能力，可能寄生合法使用 | 预期来源显示为合法 GUI 客户端，归因可能变难；需进程和业务 owner 证据 | Microsoft 证明合法用途与权限条件，缺 T1010 恶意样本证明“借可信客户端掩护窗口发现”；不能因接口名称直接归 NM-FD |
| 窗口稳定性用于沙箱判定，`adjacent-technique` | 多次比较前台句柄或活动度并以此决定载荷是否执行 | 改变分析环境中的后继行为 | T1010 提供观察原语；**判定沙箱并抑制载荷的因果中心属 T1497**。不把此目的复制为 T1010 子项 |
| 普通全窗口清单，`parent-core` | 获取顶层窗口及标题清单 | 有本地 GUI 查询痕迹，可能随后外传；没有独立受控匿迹变化 | 固定 ATT&CK 行与 EnumWindows 能力支持父行为，不足以单独定义 NJS |

建议 `subtechnique_taxonomy.coverage: established`，仅在主 Agent 接受第一行的独立性与证据链后；否则为 `deferred`，不以“0 个 ATT&CK 子项”推出 `none-justified`。拟议正式 Niji 子项数 **1**，不预设编号。第二轮高广度审查未由固定基线触发；上表已额外检查四种非 ATT&CK 轴。

## 4. 父级双语核心字段建议

**名称 / summary。** 应用窗口发现 / Application Window Discovery。中文：攻击者读取开放窗口及其前台交互上下文，以选择信息收集或后续动作的时机；条件化使用可让关键活动仅在目标窗口出现时留下痕迹。English: An adversary reads open windows and foreground interaction context to choose what to collect or when to act; conditional use can confine consequential traces to moments when a target window appears.

**definition_and_concept。** 中文：应用窗口发现是从当前交互桌面读取顶层窗口、窗口标题、前台焦点及可见应用上下文，以判断用户实际打开并使用的应用或工作内容。其直接目的在于为后续选择收集对象、操作时机或需规避的界面提供情境，而不是枚举一切进程或安装记录。窗口可能暴露目标软件或文档线索，但所读对象仍是活动 GUI 状态。English: Application Window Discovery reads top-level windows, titles, foreground focus, and visible application context on an interactive desktop to learn which applications or work items a user actually has open. Its immediate purpose is to inform later collection, timing, or interaction with a relevant interface, rather than enumerate every process or installed package. A title may reveal a software or document clue, but the queried object remains live GUI state.

**stealth_characteristics。** 中文：窗口查询可在已有进程内通过普通桌面接口完成，不必生成新的枚举命令进程；只看标准进程创建事件的防守方可能看见该进程却看不见具体窗口读取。攻击者若把后继行为限制在匹配的标题和焦点状态，非目标时间缺少截图或通信，短时基线更难把等待状态与目标出现后的动作连为一链。残余是 API/脚本/事件 hook 痕迹、运行身份、窗口状态变化和命中后的网络或收集结果；有 GUI API 传感器及会话关联时可恢复。English: A window read can occur through ordinary desktop interfaces inside an existing process without spawning an enumeration utility. A defender limited to process creation may see that process but miss the specific GUI read. When the adversary gates follow-on behavior on title and focus, non-target periods lack screenshots or communications and short baselines may separate waiting from action. API, script, or event-hook activity, actor identity, window-state transitions, and post-match network or collection outcomes remain observable when suitable instrumentation and session correlation are available.

**scope_boundary_definition。** 中文：纳入以开放窗口、标题或前台状态为直接对象的敌手查询，及作为这些查询结果之条件的后继动作谱系；父级不要求证明每次查询都具有匿迹目的。只查进程列表归 T1057，只查安装清单归 T1518；若把窗口活动解释为虚拟机或沙箱证据并据此停用载荷，判定逻辑归 T1497。屏幕阅读器、自动化测试、桌面流程、窗口管理与远程协助也会读取相同状态，应按拥有者、会话、授权用途和后继结果区分。English: Include adversarial queries whose direct object is an open window, title, or foreground state, plus the lineage of actions conditioned on those results; the parent does not require every query to have a stealth motive. A process inventory belongs to T1057 and an installed-software inventory to T1518. When window activity is interpreted as virtual-machine or sandbox evidence and suppresses a payload, the environment judgment belongs to T1497. Screen readers, automated tests, desktop flows, window managers, and remote support read similar state and require owner, session, approved-purpose, and outcome context to distinguish them.

**application_scenarios。** 中文：在已进入的交互式工作站或桌面会话中，攻击者可等待银行、通信、文档或安全工具窗口出现，再选择截屏、输入监控、操纵或 C2 通信的时机。Grandoreiro 和 Attor 分别说明按前台银行标题启动通信及按窗口/进程匹配截屏；它们不证明所有平台都实施相同门控。English: In an accessed interactive workstation or desktop session, an adversary may wait for a banking, communications, document, or security-tool window before selecting the time for capture, input monitoring, manipulation, or C2. Grandoreiro and Attor respectively illustrate C2 activation on a foreground banking title and screenshots selected by window or process match; neither establishes identical behavior across platforms.

**attacker_model。** 中文：攻击者需要在能够访问目标图形会话的进程中执行代码或脚本，并取得足够的窗口句柄、标题或可访问性状态；预先知道目标字符串会提高门控的选择性。仅有服务端/无头执行或不同桌面会话时可能得不到目标窗口；读取控件正文还受到 API 和权限边界限制。English: The adversary needs code or script execution with access to the target graphical session and enough window handles, captions, or accessibility state to evaluate a predicate; prior knowledge of target strings improves selectivity. A service, headless context, or another desktop session may not see the target window, and control text is further limited by API and privilege boundaries.

**defender_model。** 中文：防守方至少能保留进程身份与父链、用户/会话、脚本日志和后继网络或文件事件；只有配备经验证的 GUI API/WinEvent 传感器才可直接观测窗口读取与 hook。缺少该传感器时，Sysmon 1/3/10 无法单独还原窗口谓词，只能做来源与结果的低置信关联。窗口标题可能包含个人或业务敏感数据，建议端点本地分类或受控哈希，需保留足以验证命中关系的安全映射。English: A defender can at minimum retain process lineage, user and session, script logging, and later network or file events. Direct observation of window reads and hooks requires validated GUI API or WinEvent instrumentation. Without it, Sysmon 1, 3, and 10 cannot reconstruct a window predicate and support only lower-confidence source-to-outcome correlation. Titles may contain personal or business data; endpoint-side categorization or controlled hashing should retain a safe way to verify a match.

**stealth_mechanism 候选。** `NM-BT`，primary，medium。摘要：中文“常规进程遥测遗漏进程内窗口读取”；English “Routine process telemetry misses in-process window reads”。中文分析：进程内调用普通 GUI 读接口时，标准进程创建记录不会表示读取了哪个窗口，Sysmon 10 也不是 GUI 调用事件；防守方若只看这些通道，能看到宿主而不能看到关键发现动作。把命中后的网络/收集事件与可验证的 GUI API、脚本或 hook 记录及同一会话关联，可重新建立因果。此机理是由 API 和遥测定义推导出的观察盲点，不是“系统永不记录窗口查询”的断言；无传感器时可能必须保留低置信度。English analysis: An in-process call to an ordinary GUI read API does not appear as a window read in process-creation logs, and Sysmon 10 is not a GUI-call event. A defender using only those channels sees the host process but misses the discovery action. Joining post-match network or collection activity to validated GUI API, script, or hook records within the same session can restore the causal chain. This is an inferred monitoring gap from API and telemetry definitions, not a claim that Windows can never record a window query. Evidence: WINAPI, Sysmon, Grandoreiro, Attor.

**limitations。** 中文：案例主要来自 Windows 桌面恶意样本；不把 Windows API 语义外推成 Linux/macOS 的采集或审计保证。现有资料直接证明行为与门控，未提供受控实验测量误报率、调用量差异或检测成功率；若无法采集窗口谓词或目标状态，应把精确门控检测降级为假设。正常辅助功能和桌面自动化可产生相同局部信号，不能仅凭 API、标题关键词或签名状态定性。English: The strongest cases concern Windows desktop malware; Windows API semantics do not establish Linux or macOS collection and audit guarantees. Sources directly show behavior and gating but provide no controlled false-positive, call-volume, or detection-rate measurements. If the predicate or target state is unavailable, precise gate detection remains a hypothesis. Legitimate accessibility and desktop automation can create the same local signals, so an API, title keyword, or signature status alone cannot establish maliciousness.

## 5. 拟议子项：窗口上下文门控活动 / Window-Context-Gated Activity

**暂存键** `D07-01-T1010-CHILD-CONTEXT-GATE`；提议置信度 medium；`lineage.attck_subtechnique_inherited: false`。名称强调攻击者控制的**谓词与后继激活条件**，不按银行、浏览器、窗口字段或 OS 分项。主 Agent 可进一步审查名称是否需限定为“发现”；后继截图/C2/注入仍属于各自技术。

**definition_and_concept。** 中文：攻击者持续或反复读取窗口标题、焦点或可见交互状态，只有满足目标谓词时才启动后继恶意功能。发现动作给出条件输入，子项边界是这一条件如何安排活动的出现，而非后继功能本身。English: The adversary repeatedly reads window titles, focus, or visible interaction state and activates a malicious follow-on capability only when a target predicate is satisfied. Discovery supplies the condition; this child concerns how that condition schedules activity, rather than owning the follow-on capability itself.

**stealth_characteristics。** 中文：窗口上下文门控活动使恶意截图、通信或输入只在目标窗口出现的会话片段中留下结果，平时仍可有轻量窗口查询或等待痕迹。它降低非目标时段的结果暴露，并把发现与后续效果拉到不同观察时刻；当传感器能同时看到谓词、目标窗口状态和后继结果时，门控链反而可以被识别。English: Window-Context-Gated Activity confines screenshots, communications, or input effects to session segments in which the target window appears, while lighter window reads or waiting activity may persist. It reduces off-target outcome exposure and separates discovery from later effects in time. Instrumentation that sees the predicate, target window state, and follow-on result can instead identify the gating chain.

**scope_boundary_definition。** 中文：只有窗口/焦点状态真实控制后继活动且存在可核查的缺席与出现差异时纳入；普通标题清单、按进程名选目标、持续截屏和只观察 URL 但不读窗口者不自动归入。Grandoreiro 是较纯的标题门控案例；Attor 的进程名与标题双谓词须保留混合条件；BackSwap 的窗口/URL/交易联合谓词主要作为相邻输入链证据。English: Include only cases in which window or focus state actually controls follow-on activity and a verifiable absent-versus-present outcome difference exists. A plain title inventory, process-name-only selection, continuous screenshots, or URL-only observation does not qualify automatically. Grandoreiro is the clearer title-gated case; Attor retains its mixed process-name and title predicate, and BackSwap's combined window, URL, and transaction predicate chiefly supports the adjacent input chain.

**application_scenarios / attacker_model。** 中文：适用于攻击者已驻留用户图形会话、目标应用只间歇出现的场景；攻击者须维护目标标题或状态谓词并容忍等待、标题变化和漏命中。English: It applies when an adversary resides in a user's graphical session and the target application appears intermittently; the adversary must maintain a title or state predicate and tolerate waiting, title changes, and missed matches.

**defender_model。** 中文：防守方需同会话的窗口状态时间线、查询主体和后继网络/截图/输入事件，才能检验“目标出现前后”的结果差异；仅有进程创建或单个 C2 告警无法确认门控。English: The defender needs a same-session timeline of window state, querying actor, and follow-on network, screenshot, or input events to test the before-and-after outcome difference. Process creation alone or one C2 alert cannot establish the gate.

**机制与限制。** 候选 `NM-BT`，primary，medium。摘要：中文“未命中窗口条件时后继活动不进入常规观察”；English “Follow-on activity stays outside routine observation until the window condition matches”。中文分析：攻击者以活动窗口状态作门，非目标会话中的普通样本运行或短时观察只见进程和轻量查询，未见被抑制的通信或收集；目标窗口出现后才有后继结果。防守方若没有可复现的目标窗口状态，会低估能力；若记录窗口谓词、会话变化和结果，仍可恢复条件链。English analysis: The adversary gates action on live window state, so an ordinary short run outside the target context may show only a process and light queries while communications or collection remain suppressed. Results appear when the target window appears. Without a reproducible target state, the defender may underestimate capability; with predicate, session-state, and outcome records, the conditional chain remains recoverable. **`NM-ST` 暂缓**：条件激活本身不等于在时间或空间上分散信号，不能为凑机理强行映射。现有研究未测量相同载荷在有/无门控下的检测率，不能声称“不可检测”或所有后继功能均被抑制。

## 6. 可实施防御暂存设计

### `D07-01-T1010-DET-WINDOW-LINEAGE`：窗口查询主体—目标状态—后继结果关联

**目标 / Objective.** 中文：识别非预期主体读取窗口状态后，按特定标题/焦点条件才产生网络或收集活动的链；同时把普通窗口管理、辅助功能与自动化流程作为明确反例。English: Identify unexpected actors that read window state and produce network or collection activity only after a specific title or focus condition, while explicitly testing window management, accessibility, and desktop automation as counterexamples. Domain `enterprise`；本设计经验证部分先限 Windows 交互桌面，Linux/macOS 覆盖 `defer`，不可借 ATT&CK 多平台列表声称已实现。

### `D07-01-T1010-NJA-GUI-GATE`：Windows 关联分析

1. **数据要求。** 必需一条经本地试验确认的 EDR/应用自有 GUI 遥测：`timestamp`, `actor_process_guid` 或稳定 PID+创建时间，`user_sid`, `session_id`, `operation`（例如 EnumWindows/GetForegroundWindow/GetWindowText/SetWinEventHook），`target_window_handle` 或脱敏稳定键，`target_process_id`（可用时），`title_class_or_controlled_hash`（可用时），`result_status`。对脚本实现可用 PowerShell 4104/模块日志补足调用文本，但不能假定它看见已编译程序内部 API。另需进程来源：Sysmon 1 或等价进程事件的 `process_guid`, `image`, `command_line`, `parent_process_guid`, `user_sid`；后继结果至少一种：启用的 Sysmon 3/EDR 网络事件的 `process_guid`, `destination`, `timestamp`，或产品自有截图、文件创建、输入注入审计。窗口焦点时间线由 GUI 传感器或受控会话探针提供；Windows 标准事件日志本身不保证这些字段。
2. **逻辑。** 按进程身份与登录会话聚合 GUI 查询，记录调用范围、窗口状态和可用谓词。对候选进程，比较目标标题/焦点首次出现之前与之后的后继结果；若出现重复读取、较窄的匹配条件、命中后短时 C2/截图/输入结果，且来源不是已批准的同会话 GUI 工作流，输出“门控嫌疑”。单次读取、单个标题字符串或单次连接只作为线索。窗口状态/谓词缺失时只输出“异常窗口查询”低置信结果，不能声称验证了门控。
3. **关联。** 初始试验窗口为同一 `host_id + user_sid + session_id + actor_process_guid` 内命中前后各 5 分钟，长驻样本另保留 24 小时窗口状态摘要；这些数字是**部署起点假设**，须用正常软件与已知样本校准。跨 PID 重用以 ProcessGuid 或进程创建时间解决；注入到可信进程时还需模块/线程来源，否则只得到宿主级结果。
4. **误报与调优。** 屏幕阅读器、Power Automate/RPA、自动化测试、远程协助、窗口管理器及用户写的桌面脚本可读标题并按窗口条件操作。按签名、部署包、owner、会话、批准动作、目标范围和工单建立可审计基线；不要按 `user32.dll`、某个浏览器或一个签名永久放行。对敏感标题先在端点分类或加密哈希；调查授权后再解密最小必要样本。
5. **盲区。** 默认 Sysmon 10 是跨进程访问而非 EnumWindows 记录；Sysmon 3 可被配置关闭且现有连接不一定生成新事件。内存内 API 解析、API hook 绕行、进程注入、无 GUI 会话、受保护桌面、标题动态变化、端到端加密和缺失截图审计都会降低结论强度。ATT&CK DET0097 可启发策略，但其 `AccessedFunction` 不能未经产品验证写成 Sysmon 原生字段。

### `D07-01-T1010-MIT-GUI-OBSERVATION`：GUI 观察面治理

**Measure A：交互会话与辅助功能身份治理（exposure-reduction / governance）。** 清点需读取跨应用窗口的屏幕阅读器、RPA、测试、远程支持和窗口管理组件，记录发布者、安装来源、业务 owner、可访问会话和预期目标范围；对需 `uiAccess` 的高完整性 UI 访问遵循 Microsoft 签名、受信安全安装位置及清单要求，并限制不必要的高权限桌面会话。预期效果是减少未管理的高权限 GUI 观察面并提供可靠基线；**不阻断普通用户态标题查询**。

**Measure B：窗口查询与后继效果来源保留（detective-support）。** 在高价值交互终端试点经验证的 GUI API/WinEvent 传感器，保留进程/会话键和目标类别，并与进程、网络和收集结果关联；用短期原始标题、长期脱敏类别或受控哈希兼顾复核与隐私。预期效果是使门控活动可归因；代价是性能、误报和敏感标题处理，不是预防控制。

**Measure C：按具体动作控制后继能力（preventive / containment）。** 通过应用控制、最小权限、受控截图/自动化能力和出站策略限制未授权主体在命中后执行收集或通信；发现异常时先保全会话与谓词证据，再隔离恶意进程/规则，不批量禁用辅助功能。预期效果是降低门控命中后的危害，但不能消除窗口信息本身的读取。应用应分别针对父项与获准的子项写 `target_ref`，主 Agent 才能填正式引用。

## 7. 共享库复用、创建与边界决议

| 对象 | 建议 | 理由 |
|---|---|
| `REF-000245` BackSwap、`REF-000366` Sysmon | `reuse` | URL 和语义已存在；分别只用于事件/输入相邻例子与日志能力边界 |
| `CASE-000085`、`CLM-000449` | `defer` 对 T1010 的 subject 扩展 | 既有主张是活动会话输入注入，不能按词面相似直接扩展为独立窗口发现或匿迹证明；若主 Agent 需要交叉引用，先审核同一命题是否仍成立 |
| Grandoreiro 2024、Attor、Microsoft Win32/UIA/Power Automate、MITRE T1010/DET0097 | `create` 引用暂存键 | 当前共享库精确检索未找到这些 canonical URL；由主 Agent 做最终 URL 去重与分配 |
| `D07-01-T1010-CLM-*` 与 Grandoreiro 案例 | `create`，若主 Agent 审核通过 | 原子命题、证据强度和主体范围与现有 BackSwap 对象不同；Attor 暂作来源支撑，是否另建 Case 依主 Agent 的案例门槛 |
| DET / NJA | `create` 或与未来 T1057/T1518 防御 `split` | 需要 GUI 查询、会话/窗口键与门控结果；现有进程或软件发现目的及数据模型不等价。DET 与 NJA 必须双向连接，主体只直接引用 DET |
| MIT | `create`；若有完全相同的 GUI 观察治理对象再 `extend` | 已有 `MIT-000069` 管永久 callback，`MIT-000087` 管输入设备/执行，不能因 BackSwap 或 hook 词相同就把普通窗口查询纳入；本案含窗口观察基线与逐目标应用 |
| REL | `defer` | 与 T1057/T1518/T1497 的边界已在本交接描述；没有必须写成正式关系对象的独立语义证据 |

## 8. 集成时的限制与核对点

主 Agent 应重新按 canonical URL 查重，再决定正式 Claim/Case/DET/NJA/MIT 及父子范围；本文暂存键不能直接进入正式 YAML。对于子项，重点复核“窗口谓词本身”和截图/C2/输入门控之间的因果链，以及条件缺席时的 `NM-BT` 观察盲点是否达到字段门槛。若机制证据无法达到字段门槛，把该轴保留在研究规划并标记 `deferred`，不要为满足“至少一机理”而借相邻技术事实。无经验证 GUI 传感器时，Analytic 只能输出较弱的间接链，不得声称观察到 EnumWindows。其他平台的检测字段、事件式与前台式独立子项、辅助功能伪装和实际检测效果均需另证据后再推进。
