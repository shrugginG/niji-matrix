# T1083 File and Directory Discovery / 文件与目录发现：第二轮只读研究交接

批次：`BATCH-TA0007-003`；工作项：`WORK-TA0007-T1083`；临时键前缀：`D07-03-T1083-*`；固定基线：MITRE ATT&CK Enterprise `19.1`；研究日：2026-09-27。

本文件只提交研究、准入、taxonomy、防御和共享库决议。未分配正式 NJT/NJS/REF/CLM/CASE/DET/NJA/MIT/REL ID，未修改正式矩阵或共享库。第一轮的 T1613 `retain/0 NJS`、T1622 `retain + reuse NJT-0106/NJS-0106-001/-002`、T1652 `adapt/0 NJS` 只用于边界复核，不作为 T1083 结论证据。

## 1. 准入建议先行

**建议：`retain`；父级置信度 `high`；`original_attack_subtechniques_imported: false`。固定 ATT&CK 19.1 子技术为 `0 / []`。本轮建议正式 Niji 子技术 `0`，taxonomy coverage 为 `deferred`。**

**中文理由。** T1083 具有独立且稳定的 Discovery 信息对象：攻击者取得主机或网络文件系统中的路径、文件和目录名称、层级、存在性以及不读取正文即可返回的属性，用这些结果选择后继目标。固定 19.1 STIX 锚定该父行为、TA0007 归属和零 ATT&CK 子项；CISA 联合通告记录国家支持行为者用 `dirsb.bat` 从网络主机收集文件夹和文件名，另一份 NSA/CISA 联合通告基于红蓝队、hunt 和事件响应经验确认攻击者会以命令、开源工具和定制恶意软件发现并分类文件。父行为因此应保留，不需要改变直接对象。

T1083 的主要难点是恶意枚举与搜索索引、备份、杀毒、开发工具、用户文件浏览和运维脚本共用文件系统读语义。Trend Micro 对 Mimic 的样本分析进一步证明恶意软件可调用合法 Everything 组件按文件名和扩展名定位加密目标；Everything 官方文档证明其可从 NTFS 索引和 USN Journal 提供文件名而不读取文件正文。这形成“索引化命名空间查询”候选轴和真实观察面差异，但现有材料没有证明 Mimic 为规避目录枚举检测而选择该路径，也没有同案比较目录遍历与索引查询痕迹或验证查询日志。因此本轮不把该轴升级为 NJS；窄谓词、低速分批和多来源分散同样缺结论级证据，全部 `defer`。

**English rationale.** T1083 has a distinct and stable Discovery information object: paths, file and directory names, hierarchy, existence, and attributes returned without reading file contents on a host or network filesystem. An adversary uses those results to choose later targets. The fixed 19.1 STIX baseline anchors the parent behavior, its TA0007 mapping, and a zero-child ATT&CK inventory. A CISA joint advisory records state-sponsored actors using `dirsb.bat` to gather folder and file names from network hosts, while an NSA/CISA joint advisory based on red-team, hunt, and incident-response work confirms that adversaries use commands, open-source tools, and custom malware to discover and categorize files. The parent therefore warrants retention without changing its direct object.

The main T1083 difficulty is that malicious enumeration shares filesystem-read semantics with search indexing, backup, antivirus, development tools, user browsing, and operations scripts. Trend Micro's Mimic analysis also establishes malicious use of legitimate Everything components to locate encryption targets by filename and extension. Everything documentation establishes that NTFS indexes and the USN Journal can supply filenames without reading file contents. This creates a plausible indexed-namespace-query axis and an architectural observation shift. The available evidence does not establish that Mimic selected the path to evade directory-enumeration detection, compare same-case traversal and indexed-query traces, or validate query logging. This review therefore does not promote that axis to NJS. Narrow predicates, low-rate batching, and distributed origins likewise lack conclusion-level support and remain deferred.

## 2. 一手证据与结论边界

| 证据键 | 来源与定位 | 当前可支持的结论 | 不得外推 |
|---|---|---|---|
| `REF-000625` | MITRE ATT&CK Enterprise 19.1 STIX，`enterprise-attack-19.1.json` 中 active T1083 attack-pattern、TA0007 kill-chain phase 和 child inventory | 固定基线父行为、Discovery 归属、平台语境、零 ATT&CK 子项 | 不证明任何 Niji 子项、匿迹意图、传感器覆盖或检测效果；建议主审扩展 locator 后复用 |
| `D07-03-T1083-REF-CISA-ENERGY` | CISA/FBI/DOE `AA22-083A`，File and Directory Discovery 行 | 行为者使用 `dirsb.bat` 从网络内主机收集 folder/file names；直接支持父行为和网络文件系统语境 | 不证明读取了文件正文、打包、外传、规避意图或使用索引 |
| `D07-03-T1083-REF-CISA-MISCONFIG` | NSA/CISA `AA23-278A`，Table 19 Discovery | 红蓝队、hunt 和 IR 经验支持以命令、开源工具或定制恶意软件发现并分类文件；同时说明后继可能寻找口令和敏感资料 | 不能把“搜索期望信息”直接写成已读取内容、已取得凭据或已完成 Collection |
| `D07-03-T1083-REF-TREND-MIMIC` | Trend Micro/TrendAI，Mimic ransomware 技术分析，Everything32.dll 与命令参数段 | 样本调用合法 Everything 功能按目标文件查询，支持恶意索引化命名空间查询的存在；`-dir/-e` 等参数说明目标范围可控 | 样本目标主要是后继加密；来源不证明规避目录检测、在真实受害环境漏报或 Everything 查询日志必然不可见 |
| `D07-03-T1083-REF-VOID-OPTIONS` | voidtools Everything Options，NTFS/USN indexing 段 | Everything 使用 USN Change Journal 维护 NTFS 索引，可限定被索引文件夹；索引是独立命名空间视图 | 产品架构不证明攻击者实际查询、查询意图或防守产品效果 |
| `D07-03-T1083-REF-VOID-SERVICE` | voidtools Everything Service，Security 段 | 本地用户可通过服务取得 NTFS 文件名清单，服务只提供文件名而不能读取文件正文 | 不证明所有版本、部署模式或其他索引器具有相同权限和日志 |
| `REF-000623` | Microsoft Windows command-line process auditing | 启用 Audit Process Creation 和命令行策略后，Security 4688 可保存进程与命令行 | 默认命令行可能为空；内存内 API、GUI 和远控内建浏览不一定产生独立工具命令 |
| `REF-000463` | Microsoft PowerShell logging | 启用 Script Block Logging 后，PowerShell Operational 4104 保存脚本块 | 不覆盖未启用策略、其他解释器或原生 API |
| `REF-000379` | Microsoft Windows Security event 4663 | 对配置了相应 SACL 的目录，4663 可记录实际使用的 `ListDirectory` 权限、对象、主体和进程 | 不是全盘默认遥测；缺事件不能推出没有枚举 |
| `REF-000474` | Microsoft Windows Security event 5145 | Detailed File Share audit 可记录 SMB 共享访问检查的主体、源地址、共享、相对目标和请求权限 | 5145 是访问检查；单条事件不证明成功取得完整目录结果，更不证明读取正文 |
| `D07-03-T1083-REF-LINUX-GETDENTS` | Linux man-pages `getdents/getdents64(2)` | `getdents64` 返回目录项名称和类型，支持 Linux 目录枚举观察对象定义 | 不证明 auditd 默认记录该 syscall、路径可由单条事件恢复或调用具有恶意意图 |
| `D07-03-T1083-REF-LINUX-AUDITCTL` | Linux audit `auditctl(8)` | audit syscall rules 可按 syscall/arch/字段记录，规则过多会产生性能成本 | 不证明所有发行版默认启用、无丢失或全局 `getdents64` 审计适合生产部署 |
| `D07-03-T1083-REF-MS-ABE` | Microsoft DFS Access-based Enumeration | ABE 可隐藏用户无权访问的文件夹；真正阻止已知路径访问仍依赖 share/NTFS 权限；存在性能代价 | ABE 不是内容访问控制，也不能撤回已复制或已索引的名称 |

证据分层结论：`REF-000625` 与两份 CISA 材料充分支持父级 retain；Trend Micro 与 voidtools 文档只把索引轴推进到“真实恶意使用 + 架构可行”，没有完成“规避选择 + 同案痕迹差 + 独立防御验证”的 NJS 门禁。Microsoft 与 Linux 文档支持可实施数据要求和限制，不证明检测率。

### 新 Reference 候选的 canonical URL

| 临时键 | canonical URL | source type / accessed |
|---|---|---|
| `D07-03-T1083-REF-CISA-ENERGY` | `https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-083a` | government advisory / 2026-09-27 |
| `D07-03-T1083-REF-CISA-MISCONFIG` | `https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-278a` | government advisory / 2026-09-27 |
| `D07-03-T1083-REF-TREND-MIMIC` | `https://www.trendaisecurity.com/fr/resources-insights/trendai-security-blog/new-mimic-ransomware-abuses-everything-apis-for-its-encryption-p` | primary malware analysis / 2026-09-27 |
| `D07-03-T1083-REF-VOID-OPTIONS` | `https://www.voidtools.com/support/everything/options/` | official product documentation / 2026-09-27 |
| `D07-03-T1083-REF-VOID-SERVICE` | `https://www.voidtools.com/support/everything/everything_service/` | official product documentation / 2026-09-27 |
| `D07-03-T1083-REF-LINUX-GETDENTS` | `https://www.man7.org/linux/man-pages/man2/getdents64.2.html` | primary system interface documentation / 2026-09-27 |
| `D07-03-T1083-REF-LINUX-AUDITCTL` | `https://man7.org/linux/man-pages/man8/auditctl.8.html` | primary system interface documentation / 2026-09-27 |
| `D07-03-T1083-REF-MS-ABE` | `https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/enable-access-based-enumeration-on-a-namespace` | official documentation / 2026-09-27 |

正式共享对象写入时保留精确 locator 与上述“不外推”限制；若 canonical URL 重定向，只更新 URL 身份，不扩张结论范围。

## 3. 范围和相邻边界

| 边界 | T1083 纳入 | 排除或并记规则 |
|---|---|---|
| `NJT-0138` 浏览器信息发现 | 若攻击者只找到浏览器数据库、profile 或历史文件的路径，路径发现仍是 T1083 | 解析历史、书签、URL 和浏览设置属于 NJT-0138；Cookie、密码和 token 按 Credential Access 判断 |
| `NJT-0141` 云存储对象发现 | 挂载或 SMB/NFS 呈现为文件系统语义且结果为路径/目录项时可归 T1083 | 对象服务内 key、prefix 和对象元数据列表归 NJT-0141，即使控制台显示“文件夹” |
| `T1135` 网络共享发现 | 已知 share/mount 内继续列目录与文件名归 T1083 | 发现 share 名称、服务器和可用共享本身归 T1135；一个命令可分别产生两类结果 |
| TA0009 内容收集 | 仅取得路径、名称、层级、存在性和列表属性属于 T1083 | 打开并读取正文、复制文件、从共享取数据、批量收集、暂存、压缩和外传分别归相应 Collection/Exfiltration 对象；列表事件不能证明这些结果 |
| 凭据搜索 | 通过名称、扩展名或路径谓词定位可能含凭据的文件，可同时记录 T1083 的路径发现 | 打开文件、解析内容并取得口令、密钥、token 或配置秘密属于凭据访问；“搜索 password 字样”不自动证明凭据已取得 |
| 隐藏文件与目录 | 列表返回 hidden/system/dotfile 等属性仍是 T1083 的父级属性结果 | 创建、设置或使用隐藏属性来隐藏对象属于 Hidden Files and Directories；不能按 hidden 属性另拆 NJS |
| 文件属性 | 列表或 stat 类结果中的大小、时间、类型、所有者和权限可作为父级发现结果 | 修改属性、时间戳或 ACL 是后继行为；哈希或正文检查若读取内容需按直接动作另判 |
| 索引、备份和安全清单 | 攻击者实际查询已有清单以取得路径时仍可作为 T1083 实现；索引视图候选轴另审 | 合法搜索索引、备份 catalog、杀毒扫描、EDR inventory、开发构建和取证是强反例；仅“系统中存在索引”不构成攻击 |
| 用户浏览与运维 | 用户或管理员通过 Explorer、Finder、shell、IDE、文件管理器或脚本列目录与恶意行为同形 | 必须依靠身份、父进程、主机角色、范围、时间、批准作业及后继动作区分；工具名或单次 `ls/dir` 不能定性 |

## 4. Niji taxonomy 多轴审查

固定 ATT&CK 19.1 子项为 `0 / []`，breadth trigger 为 `ordinary`；零子项未用于提前停止搜索。本轮从读取位置、查询谓词、节奏、来源分布、接口和对象类别六个方向审查。

| 临时键 / 轴 | 行为设计 → 痕迹变化 → 防守观察差 | 决议 | 门禁理由 |
|---|---|---|---|
| `D07-03-T1083-AX-01` 合法枚举功能外观 | 攻击者使用 `dir/find/PowerShell/Everything` 或同等文件浏览能力 → 事件与用户浏览、索引、备份、杀毒及运维重叠 → 单事件难以分类目的 | **`formal-parent-core`**；支持父级 `NM-FD`，不拆 NJS | CISA 与 Mimic 材料支持恶意使用正常功能，且正常反例客观存在；变量是父行为的共同可区分性问题，没有稳定兄弟边界 |
| `D07-03-T1083-AX-02` 索引化命名空间查询 | 查询已有或并发建立的命名空间索引/catalog，而不为本次匹配逐层遍历每个父目录 → 观察面转到索引服务、数据库、MFT/USN、query IPC 或 catalog 访问，目录 `ListDirectory/getdents` 可能减少 → 只监控 `dir/find` 或逐目录读取的分析可能失去目标选择信号 | **`defer`**；最强 NJS 候选，`NM-BT` 仅 hypothesis | Mimic + Everything 架构支持恶意查询和痕迹迁移的可行性，但不证明规避选择、同案痕迹对照、查询遥测或检测差；索引、备份、杀毒是强正常反例 |
| `D07-03-T1083-AX-03` 窄谓词与目标范围 | 按已知根路径、名称、扩展名、时间或属性只返回候选 → 输出和后继访问量可下降 → 基于全盘递归或数量阈值的分析可能变弱 | **`defer`** | Mimic 支持名称/扩展名筛选，CISA 支持广域枚举，但底层实现可能仍遍历全部目录；没有稳定的 trace 边界、规避意图或独立防御验证 |
| `D07-03-T1083-AX-04` 时间稀释与分批枚举 | 长时间、小批量或在正常用户会话中逐步列举 → 局部窗口内目录数降低 → 短窗口阈值可能不触发 | **`defer`**，`NM-ST` hypothesis | 当前来源没有攻击者故意节流、跨窗口重构或漏报证据；合法交互浏览天然呈相同节奏 |
| `D07-03-T1083-AX-05` 多主机、会话或身份分散 | 将网络文件系统范围分配给多个来源或凭证 → 单来源只留下局部目录访问 → 需跨源按 share/path 聚合 | **`defer`**，`NM-ST` hypothesis | CISA `dirsb.bat` 支持网络内多主机父行为，不支持同一目标范围被故意分散；缺 source assignment 和检测效果 |
| `D07-03-T1083-AX-06` CLI/GUI/API/原生函数/远控内建浏览 | 更换实现接口会改变进程、脚本和 API 遥测 | **`reject`** 作为 NJS | 接口和工具可替换，直接信息对象不变；这些是 NJA 分支与 blind spot，不是稳定 stealth taxonomy |
| `D07-03-T1083-AX-07` Windows/Linux/macOS/网络设备、路径类型或文件类别 | 平台、路径、扩展名、隐藏属性、local/remote 分区改变实现与数据源 | **`reject`** 作为 NJS | 属平台、资源类别或目标类别拆分，会无限扩张；应留在父级范围和分析适配中 |

**taxonomy 结论。** 正式 NJS 为 `0`。`coverage: deferred`，因为 AX-02 具备可复审价值但未过结论级证据门禁；不使用 `none-justified`。后续若要 formalize AX-02，至少需要：同一攻击样本或受害环境中索引查询与直接遍历的受控 trace 对照；索引 query/service/catalog 的实际可采字段；攻击者选择该读取位置的直接或可重复证据；独立于产品名称的 sibling 边界；以及不同 DET/NJA/MIT 的验证。AX-03/04/05 需要对应参数、时间或来源分配及防守效果证据，不得因“理论上更少事件”升级。

## 5. 父级双语核心字段草案

### summary

- **zh：** 文件与目录发现是攻击者取得主机或网络文件系统中的路径、文件和目录名称、层级、存在性及列表属性，以选择后继访问、收集、执行或影响目标的行为。
- **en:** File and Directory Discovery obtains paths, file and directory names, hierarchy, existence, and listing attributes from a host or network filesystem so an adversary can select targets for later access, collection, execution, or impact.

### definition_and_concept

- **zh：** 本技术的直接结果是文件系统命名空间事实，而不是文件正文。结果可以来自当前目录列表、递归搜索、路径存在性或属性查询、已知网络共享内浏览，或对保存路径和名称的索引视图进行实际查询。命令、GUI、远控文件浏览器、脚本、原生 API 和自定义工具只是实现；分类依据是攻击者取得了哪些路径、名称、层级和属性。
- **en:** The direct result of this technique is a filesystem namespace fact rather than file content. Results may come from a current-directory list, recursive search, path-existence or attribute query, browsing inside a known network share, or an actual query of an indexed view that stores paths and names. Commands, GUIs, remote file browsers, scripts, native APIs, and custom tools are implementations; classification follows the acquired paths, names, hierarchy, and attributes.

- **zh：** 发现完成后，攻击者可能读取、复制、压缩、加密、删除或执行所选文件，但这些是独立后继动作。一个枚举事务可以同时提供名称和属性，也可以失败、返回部分结果或受权限、挂载、重解析点、索引时效及网络视角限制；“执行过搜索工具”不能替代实际结果语义。
- **en:** After discovery, an adversary may read, copy, archive, encrypt, delete, or execute selected files, but those are separate successor actions. An enumeration transaction may return names and attributes together, fail, or produce only a partial result because of permissions, mounts, reparse points, index freshness, or network perspective. Execution of a search utility does not substitute for result semantics.

### stealth_characteristics

- **zh：** 文件枚举大量存在于正常搜索、用户浏览、备份、杀毒、开发、资产盘点和运维中。攻击者可借用同一系统工具、签名程序或标准接口，使进程和读访问在单事件层面接近日常活动；恶意性通常要从非常用父进程或主体、异常根路径和范围、非批准时段以及紧邻的文件读取、暂存、打包、加密或删除恢复。目录名称和查询行为仍可能留在进程、脚本、文件系统或共享审计中。
- **en:** File enumeration is common in normal search, user browsing, backup, antivirus, development, inventory, and operations. An adversary can use the same system utilities, signed programs, or standard interfaces, making process and read events resemble routine activity at the single-event level. Malice usually requires an unusual parent or principal, abnormal roots and scope, an unapproved time, and adjacent file reads, staging, archiving, encryption, or deletion. Directory names and query behavior can still remain in process, script, filesystem, or share audit.

- **zh：** 索引或 catalog 查询还可能把当次目标选择从逐目录读取转移到索引服务、MFT/USN、数据库或 query IPC。该迁移是当前的 hypothesis：它可形成对只监控递归遍历分析的盲点，但索引建立、服务启动、catalog 访问与后继对象打开仍是残余痕迹，且本轮没有在真实攻击中验证漏报。
- **en:** An index or catalog query may also move present target selection from per-directory reads to an index service, MFT or USN activity, a database, or query IPC. This shift remains a hypothesis: it can create a gap for analytics limited to recursive traversal, while index construction, service start, catalog access, and later object opens remain residual traces. This review has no in-the-wild validation of a miss.

### scope_boundary_definition

- **zh：** 纳入本机和已知网络文件系统内路径、名称、目录层级、存在性以及不打开正文即可取得的大小、时间、类型、所有者、权限或隐藏属性。已知 share 内列目录属于本技术，而发现 share 本身属于 T1135；挂载为文件系统的存储按返回语义判断，云对象服务中的 key/prefix 列表归 NJT-0141。仅定位浏览器数据库路径属于本技术，解析其保留浏览上下文归 NJT-0138。
- **en:** Include paths, names, directory hierarchy, existence, and size, time, type, owner, permission, or hidden attributes obtainable without opening file content on local and known network filesystems. Listing inside a known share belongs here, while discovery of the share itself belongs to T1135. Storage mounted as a filesystem follows returned semantics, whereas key and prefix lists from an object service belong to NJT-0141. Locating a browser database path belongs here; parsing retained browsing context belongs to NJT-0138.

- **zh：** 排除文件正文读取、复制、批量收集、暂存、压缩和外传；凭据或秘密只有在实际读取并识别后才进入凭据访问。设置隐藏属性或把对象放入隐藏位置属于隐藏行为，列出该对象只属于发现。搜索索引、备份、杀毒、开发工具、用户文件管理器和批准运维脚本是强反例，必须以主体、批准作业、范围、时间、主机角色和后继动作判定，不能把路径、扩展名或工具名称单独当恶意指标。
- **en:** Exclude reading file contents, copying, bulk collection, staging, archiving, and exfiltration. Credentials or secrets enter Credential Access only after content is actually read and identified. Setting a hidden attribute or placing an object in a hidden location is concealment, while listing that object is discovery. Search indexing, backup, antivirus, development tools, user file managers, and approved operations scripts are strong counterexamples. Classification requires principal, approved job, scope, time, host role, and successor behavior rather than a path, extension, or tool name alone.

### application_scenarios

- **zh：** 攻击者在取得主机执行权或可浏览的网络文件系统身份后，常先定位用户目录、配置、业务文档、虚拟磁盘、备份、工具或目标扩展名，再决定读取、打包、加密、删除或执行哪些对象。交互式操作者可能从当前目录逐步浏览，自动化载荷可能递归遍历多个根，或借已有索引快速筛选名称；只有发现步骤属于本技术。
- **en:** After obtaining host execution or an identity that can browse a network filesystem, an adversary may locate user directories, configuration, business documents, virtual disks, backups, tools, or target extensions before deciding what to read, archive, encrypt, delete, or execute. An interactive operator may browse from the current directory, while an automated payload may traverse several roots or query an existing index for names. Only the discovery step belongs to this technique.

### attacker_model

- **zh：** 攻击者需要能够在目标主机执行查询、使用远控文件浏览能力、调用文件系统接口，或以有效身份访问已知共享、挂载点或索引服务。可见范围受有效 list/traverse 权限、share 与文件系统 ACL、用户上下文、容器或 mount namespace、网络路径、索引覆盖和时效限制。取得路径名不等于取得正文读取权；更高权限可以扩大视图，但不是所有枚举的前提。
- **en:** The adversary needs authority to execute a query on the host, use a remote file-browser capability, call filesystem interfaces, or access a known share, mount, or index service with a valid identity. Effective list and traverse permissions, share and filesystem ACLs, user context, container or mount namespace, network path, and index coverage and freshness bound the visible scope. Learning a pathname does not establish content-read authority, and elevated privilege can expand the view without being required for every enumeration.

### defender_model

- **zh：** 防守方至少需要进程和命令行或脚本、身份与登录会话、目标主机角色、批准的索引/备份/杀毒/运维作业，以及可选的目录或共享访问遥测。Windows 4688 命令行和 PowerShell 4104 均需显式策略；4663 仅覆盖有匹配 SACL 的对象；5145 是共享访问检查。Linux 全局 syscall 审计成本高，`getdents64` 单事件也不一定恢复路径。防守方应把缺失事件保留为 unknown，而不是“未枚举”，并把发现与后继内容读取或影响分开关联。
- **en:** Defenders need at least process and command-line or script telemetry, identity and logon session, target host role, approved indexing, backup, antivirus, and operations jobs, and optional directory or share access telemetry. Windows 4688 command lines and PowerShell 4104 require explicit policy; 4663 covers only objects with matching SACLs; 5145 is a share access check. Global Linux syscall auditing is costly, and a `getdents64` event does not necessarily recover a path by itself. Missing events must remain unknown rather than “not enumerated,” and discovery must be correlated separately from later content reads or impact.

### stealth_mechanisms

`D07-03-T1083-MECH-01` — `NM-FD`, role `primary`, confidence `medium`。

- **summary zh：** 借正常文件浏览与盘点功能降低恶意枚举的可区分性
- **summary en:** Borrow normal file-browsing and inventory functions to reduce the distinguishability of malicious enumeration
- **analysis zh：** 攻击者通过系统命令、标准 API、签名搜索工具或远控内建浏览取得路径，使进程和目录读语义与用户浏览、索引、备份、杀毒和运维接近。该设计没有消除事件，却削弱了单条命令、进程或 ListDirectory 事件的分类价值；防守方必须引入主体、父进程、范围、主机角色、批准作业和后继结果才能恢复恶意上下文。CISA 父行为材料和 Mimic 对合法 Everything 组件的使用支持这种功能外观汇合，但没有量化具体产品漏报率。
- **analysis en:** An adversary obtains paths through system commands, standard APIs, a signed search utility, or a remote tool's built-in browser, making process and directory-read semantics resemble user browsing, indexing, backup, antivirus, and operations. Events are not removed, but one command, process, or ListDirectory event loses classification value. Defenders need principal, parent, scope, host role, approved job, and successor outcome to recover malicious context. CISA parent-behavior evidence and Mimic's use of legitimate Everything components support this functional convergence without measuring a product miss rate.
- **evidence keys:** `D07-03-T1083-REF-CISA-ENERGY`, `D07-03-T1083-REF-CISA-MISCONFIG`, `D07-03-T1083-REF-TREND-MIMIC`, `D07-03-T1083-REF-VOID-SERVICE`

### subtechnique_taxonomy narrative

- **zh：** 本轮不按操作系统、CLI/GUI/API、工具、路径类别、文件扩展名、本地/网络、隐藏属性或后继用途拆 NJS。索引化命名空间查询是唯一具备真实恶意使用和架构观察差的候选，但缺规避选择、同案 trace 对照及 query telemetry 验证，保持 deferred；窄谓词、节奏和多来源分散也缺稳定兄弟边界与独立防御证据。因此正式子项为零，coverage 保持 deferred，主 Agent 不应为本批数量预留 NJS。
- **en:** This review does not create NJS partitions by operating system, CLI, GUI, API, tool, path category, extension, local versus network location, hidden attribute, or successor purpose. Indexed namespace querying is the only candidate with both real malicious use and an architectural observation difference, but it lacks an evasion-choice conclusion, a same-case trace comparison, and validated query telemetry. Narrow predicates, cadence, and distributed origins also lack stable sibling boundaries and independent defense evidence. The formal child count is therefore zero with deferred coverage, and the primary agent should not reserve an NJS to satisfy batch count.

### research.limitations

- **zh：** 公开父级案例通常不提供完整命令输出、枚举成功范围、权限失败、对象数量或发现到后继读取的逐文件时间线。Mimic 分析证明 Everything 查询能力及目标使用，却不证明真实受害环境的索引 query 记录、目录事件减少、攻击者规避动机或检测漏报。Windows 4663/5145、PowerShell 和 Linux audit 的可用性取决于策略、SACL/rule、版本、保留、事件量和传感器实现；返回名称集合通常不在日志中。当前结论可支持父级、NM-FD 和父级防御，不支持任何正式 NJS 或量化阈值。
- **en:** Public parent cases generally omit complete command output, successful scope, permission failures, object counts, and per-file timelines from discovery to later reads. Mimic analysis establishes Everything query capability and target use but not victim-side query records, reduced directory events, adversarial evasion motive, or a detection miss. Windows 4663 and 5145, PowerShell, and Linux audit availability depends on policy, SACL or rule, version, retention, event volume, and sensor implementation, and logs often omit the returned name set. Current evidence supports the parent, NM-FD, and parent defense, but no formal NJS or quantified threshold.

## 6. Deferred 子项核心字段（研究稿，非 NJS）

`D07-03-T1083-SUB-INDEX` **索引化命名空间查询 / Indexed Namespace Query**；status `hypothesis`；decision `defer`；若未来获准，`lineage.attck_subtechnique_inherited: false`。划分变量是**当次路径发现所读取的视图**，不是 Everything、Windows Search、备份或杀毒产品类别。

- **summary zh：** 攻击者查询已物化的路径/名称索引或 catalog 取得目标，使当次目标选择不必逐层列举源目录。
- **summary en:** An adversary queries a materialized path-and-name index or catalog for targets, so present selection need not enumerate source directories level by level.
- **definition zh：** 候选要求攻击者实际向保存文件系统路径或名称的索引、catalog 或离线清单发出查询并用返回结果选目标。仅安装索引器、系统中存在 `Everything.db`、备份作业生成 manifest，或恶意载荷随后逐目录遍历都不足够。索引可以预先存在，也可由攻击工具建立，但必须把 query/result 与后继目标选择连接起来。
- **definition en:** The candidate requires an adversary to query an index, catalog, or offline inventory that stores filesystem paths or names and to use returned results for target selection. Merely installing an indexer, finding `Everything.db`, generating a backup manifest, or later traversing directories is insufficient. The index may preexist or be built by the attack tooling, but query and result must be linked to later target selection.
- **stealth zh：** 索引化命名空间查询把当次匹配从每个源目录的 ListDirectory/getdents 转到索引服务、数据库、MFT/USN、catalog 文件或 query IPC；只监控递归命令和目录读取的防守方可能看不到选择谓词与结果。索引建立、服务生命周期、catalog 访问、query IPC 及后继文件打开仍是残余痕迹，陈旧或不完整索引也会限制结果。
- **stealth en:** Indexed Namespace Query shifts present matching from ListDirectory or getdents on each source directory to an index service, database, MFT or USN activity, catalog file, or query IPC. A defender limited to recursive commands and directory reads may miss the selection predicate and result. Index construction, service lifecycle, catalog access, query IPC, and later file opens remain residual traces, and a stale or partial index constrains results.
- **scope zh：** 纳入 filename/path index、备份目录清单或安全 inventory 的实际恶意查询；读取 catalog 正文仅在其直接目的是恢复路径清单时参与本候选。搜索正文内容、云对象 key 列表、浏览历史解析及读取候选文件正文分别按相邻对象判断。合法桌面搜索、备份恢复、杀毒/EDR inventory、资产管理、开发工具和取证是强反例。
- **scope en:** Include actual malicious queries of filename or path indexes, backup catalogs, or security inventories. Reading catalog content participates only when its direct purpose is to recover a path inventory. Content search, cloud-object key lists, browser-history parsing, and reading selected file contents follow neighboring objects. Desktop search, backup restoration, antivirus or EDR inventory, asset management, development tools, and forensics are strong counterexamples.
- **scenario zh：** 攻击者在可使用已有索引服务或取得 catalog 后，以名称、扩展名、路径或属性筛选业务文档、虚拟磁盘、备份或其他后继目标；Mimic 对 Everything API 的使用是实现证据，但当前不证明 stealth intent。
- **scenario en:** After gaining access to an existing index service or catalog, an adversary filters business documents, virtual disks, backups, or other successor targets by name, extension, path, or attribute. Mimic's use of Everything APIs is implementation evidence without establishing stealth intent.
- **attacker model zh：** 攻击者需要查询服务、IPC、数据库或 catalog 的实际读取权，理解覆盖范围和时效，并能把返回路径用于后继动作；若需自行建立索引，还可能需要读 MFT/USN 或广域目录权限并留下明显建立痕迹。
- **attacker model en:** The adversary needs actual query or read authority over a service, IPC endpoint, database, or catalog, knowledge of coverage and freshness, and the ability to use returned paths in later actions. Building a new index may require MFT, USN, or broad directory authority and can leave conspicuous construction traces.
- **defender model zh：** 防守方需获得索引服务安装/启动、服务主体、数据库或 catalog 访问、query IPC 或产品 query audit，并与后继目标路径打开关联。Everything 官方材料不承诺默认 query log；没有 query 内容时只能识别风险入口或异常服务生命周期，不能确认搜索谓词。
- **defender model en:** Defenders need index-service installation and start, service principal, database or catalog access, query IPC or provider query audit, joined to later opens of returned paths. Everything documentation does not promise a default query log. Without query content, defenders can identify an exposed entry or abnormal service lifecycle but cannot confirm the search predicate.
- **mechanism:** `NM-BT`，`hypothesis`。架构资料支持观察面迁移，Trend Micro 支持恶意查询；缺同案目录事件差分、攻击者规避选择和部署验证，故不得进入正式子项。
- **limitations zh：** 产品可能为每次查询先重建索引、退化为 folder crawl 或不记录 query；结果可能来自旧快照。索引查询和后继加密/收集不能合并为一个动作。取得受控 trace、query 字段和正常基线前保持 defer。
- **limitations en:** A product may rebuild an index for each run, fall back to a folder crawl, omit query logs, or return a stale snapshot. The index query and later encryption or collection remain separate actions. Defer until controlled traces, query fields, and a normal baseline are available.

## 7. 可实施 DET / NJA 提案

### `D07-03-T1083-DET-NAMESPACE` — `create`

**名称：文件系统命名空间枚举谱系与范围异常 / Filesystem Namespace Enumeration Lineage and Scope Anomaly。**

- **目标 zh：** 识别主体通过命令、脚本、原生进程或共享访问取得异常文件系统路径清单，并把枚举与批准作业及后继文件动作分开关联；策略检测的是命名空间发现，不把文件正文读取、打包或加密算作同一结果。
- **Objective en:** Identify a principal obtaining an anomalous filesystem path inventory through commands, scripts, native processes, or share access, then correlate enumeration separately with approved jobs and later file actions. The strategy detects namespace discovery and does not treat content reads, archiving, or encryption as the same result.
- **覆盖：** future parent T1083 only；domain `enterprise`。两个实施分析按真实数据通道拆分，不按平台拆 NJS。

### `D07-03-T1083-NJA-WINDOWS` — Windows 本地与 SMB 命名空间枚举

**状态建议：`create`，阈值在部署回放后进入 review。**

**数据要求：**

1. `windows-process-creation`，channel `Security/4688` 或等价 EDR process channel；必需 `timestamp, host_id, subject_user_or_sid, subject_logon_id, new_process_id_or_guid, process_image, command_line, creator_process_id_or_guid, creator_process_image`。4688 command line 需单独启用；缺命令行时保留 unknown。
2. `powershell-script-block`，channel `Microsoft-Windows-PowerShell/Operational/4104`；必需 `timestamp, host_id, event_id, script_block_id, message_number, message_total, script_block_text`，并以 host/time/runspace 或可用 process identity 连接进程。
3. `windows-object-access`，channel `Security/4663`；只在批准的高价值根配置成功审计和对应 SACL，必需 `timestamp, host_id, subject_sid, subject_logon_id, process_id, process_name, object_name, object_type, access_mask, accesses`；筛选目录 `ListDirectory`，不要求全盘 SACL。
4. `windows-detailed-file-share`，channel `Security/5145`；必需 `timestamp, server_id, subject_sid, subject_logon_id, source_ip, source_port, share_name, share_local_path, relative_target_name, access_mask, access_list, result`。5145 只作共享访问检查证据。
5. `approved-filesystem-reader-registry`；channel `null`；必需 `owner, principal, process_hash_or_signer, parent_role, host_role, allowed_roots_or_shares, operation_class, schedule, change_or_job_id, valid_from, valid_to`。
6. 可选 `endpoint-directory-query`；channel `null`，仅当本地传感器实测；字段 `timestamp, host_id, process_guid, thread_id, operation, normalized_path, result_code, entry_count_if_available`。不能假定所有 EDR 提供返回名称或 API 名。

**逻辑 zh：** 先从 4688/4104 恢复 `dir /s`, `tree`, `where /r`, `forfiles`, `Get-ChildItem -Recurse` 和语义相同的命令或脚本，但工具名只产生候选。按 `host + subject_logon_id + process lineage` 在初始 30 分钟内连接 4663 ListDirectory 或 5145 对多个相对路径的访问检查，计算不同根、目录、share、敏感区域和错误结果，并与批准 reader registry 比较。对没有可见命令的进程，以经验证的 directory-query telemetry 或一个主体在多个异常 share/path 的 5145 序列补充。最后在同一进程/会话后 60 分钟连接文件 open/read、复制、归档、加密或删除作为置信增强，但分别输出 `namespace_enumeration` 与 `successor_activity`，不把后继动作反推成已发生的枚举。

**Logic en:** First recover `dir /s`, `tree`, `where /r`, `forfiles`, `Get-ChildItem -Recurse`, and semantically equivalent commands or scripts from 4688 and 4104, treating utility names only as leads. Join 4663 ListDirectory events or 5145 checks across relative paths by host, subject logon ID, and process lineage over an initial 30 minutes; calculate distinct roots, directories, shares, sensitive areas, and error results and compare them with the approved-reader registry. For processes without visible commands, use validated directory-query telemetry or a principal's sequence of 5145 activity across abnormal shares and paths. Join file opens or reads, copies, archives, encryption, or deletion over the following 60 minutes only to raise confidence, emitting `namespace_enumeration` and `successor_activity` separately rather than inferring enumeration from the successor.

**关联：** short window `30m` per process/session；successor window `60m`；long-horizon rollup `24h` for the same `host or file_server + principal + normalized root/share`。这些是工程初值，须按备份、AV、索引、构建和交互会话周期回放。

**维度：** `host_id, file_server_id, subject_sid, subject_logon_id, source_ip, process_guid, parent_guid, normalized_root_or_share, normalized_relative_path, operation_class, approved_job_id, time_bucket`。

**误报：** Windows Search/Everything 等索引器、备份和恢复、杀毒/EDR 扫描、DLP、资产盘点、IDE/构建、软件部署、用户 Explorer 浏览、管理员故障排查、迁移、取证、文件服务器容量或权限检查。

**盲区：** 4688 命令行/4104 未启用；远控工具或恶意代码进程内调用 API；4663 缺 SACL 或事件量被抑制；5145 未启用、只表示 access check 或路径被截断；FUSE/非 SMB 网络文件系统；合法身份与批准父进程被滥用；返回名称集合和 query 谓词不可见；索引查询不产生目录事件。

**调优：** 以 `owner + principal + host role + signed image/hash + parent role + roots/shares + cadence + job/change ID + expiry` 绑定例外，不永久放行 Microsoft 签名、Explorer、PowerShell、备份账户、杀毒进程或某个路径前缀。服务器与工作站分开建基线；敏感 share 的低频新来源优先于单纯数量。只在 SACL 可承受的高价值根部署 4663，并监控 audit policy/SACL 变化和日志丢失。

### `D07-03-T1083-NJA-POSIX` — POSIX 目录项枚举谱系

**状态建议：`create`，要求目标发行版和 sensor 验证。**

**数据要求：**

1. `linux-process-exec`，channel `auditd EXECVE/SYSCALL` 或等价 process telemetry；必需 `timestamp, host_id, auid, uid, session_id, pid_or_process_entity_id, ppid_or_parent_entity_id, exe, comm, argv, cwd, success, exit_code`。
2. `linux-directory-syscall`，channel `auditd SYSCALL` 或经验证的 eBPF/EDR channel；仅在性能测试通过的服务器/高价值范围启用，必需 `timestamp, host_id, auid, uid, session_id, pid, exe, syscall, arch, success, exit_value`；若传感器可得，再加 `fd, resolved_path, mount_id, inode, entry_count`。`getdents/getdents64` 单独不能保证恢复 path。
3. `posix-approved-reader-registry`，字段与 Windows 批准 reader 对齐，并增加 `container_or_mount_namespace, service_unit, package_or_binary_digest`。
4. 可选网络文件系统服务端审计，必须逐 NFS/Samba/设备部署验证实际 channel 和字段；未验证前不写成必需源。

**逻辑 zh：** 从 `ls`, `find`, `locate`, `tree` 及等价 shell/script 进程建立候选，按 `host + auid/session + process lineage` 连接 cwd、root arguments 和可得的 `getdents/getdents64` 计数。对自定义二进制，只有 directory syscall/verified sensor 与异常根、非批准主体或后继对象操作结合时提升。全局 getdents 审计可能造成巨大事件量，不应作为默认；优先按关键服务、容器、路径或短期 hunt 范围启用，并把 audit lost/backlog 作为 telemetry health。

**Logic en:** Seed candidates from `ls`, `find`, `locate`, `tree`, and equivalent shell or script processes, joining current directory, root arguments, and available `getdents` or `getdents64` counts by host, audit user or session, and process lineage. Raise custom binaries only when directory-syscall or validated sensor data combines with abnormal roots, an unapproved principal, or successor object actions. Global getdents auditing can create excessive volume and is not a default. Prefer critical services, containers, paths, or time-bounded hunts, and treat audit lost and backlog counters as telemetry health.

**窗口与维度：** `30m` process/session，`24h` rollup；`host_id, auid, session_id, process_entity_id, parent_entity_id, container_or_mount_namespace, normalized_root, inode_or_mount_id, approved_job_id, time_bucket`。

**误报：** shell 用户浏览、cron 运维、包管理、备份、索引器、杀毒、安全扫描、配置管理、容器镜像构建、编译和测试、日志轮转、取证。

**盲区：** audit 未启用或丢事件、bi-arch rule 错配、全局 syscall 规则因性能被移除、路径不能从 fd 恢复、静态或内存内工具、内核/FUSE/网络文件系统视角、container namespace 映射缺失、索引/catalog 查询绕开目录 syscall。

**调优：** 分发行版、主机角色、service unit、container image/digest、auid、根路径和时段建基线；例外有 owner 和到期。先用 exec lineage 与关键根审计，再谨慎增加 syscall 范围；不得仅因 `ls` 或 `find` 命令存在告警。

### Deferred index branch

`D07-03-T1083-NJA-INDEX` 不建议现在 formalize。未来实施前须证明一个实际 channel 能提供 `timestamp, host_id, principal, client_process, index_service_or_catalog, query_expression_or_hash, requested_scope, result_count_or_status, index_freshness`，并能连接后继 path open。当前可记录 Everything service/install/start、合法组件异常落地、catalog 数据库读取和后继文件访问作为 hunt 线索，但不能把这些代理信号写成“已观察查询结果”。

## 8. 可实施 MIT 提案

### `D07-03-T1083-MIT-NAMESPACE` — `create`

**名称：文件系统命名空间最小可见性与枚举治理 / Filesystem Namespace Least Visibility and Enumeration Governance。**

**description zh：** 将 list/traverse 权限、网络共享可见性、索引/catalog 暴露、批准 reader 身份和目录审计作为一项治理事务。控制目标是缩小失陷身份可见的路径范围并为异常枚举留下可关联证据，同时保持搜索、备份、杀毒、开发和运维所需功能。

**description en:** Govern list and traverse authority, network-share visibility, index or catalog exposure, approved reader identities, and directory audit as one transaction. The control narrows the path namespace visible to a compromised identity and preserves evidence for anomalous enumeration while retaining required search, backup, antivirus, development, and operations functions.

**Measures：**

1. `least-list-and-traverse-authority` / 最小 list 与 traverse 权限，`preventive`：按角色收紧本地目录、share 和 mount 的 list/traverse/read-attributes 权限，分离普通用户、服务账户、备份、索引、杀毒与管理员身份；定期验证有效权限和继承，移除 everyone/domain-wide visibility 及过期 JIT 例外。 / Tighten local-directory, share, and mount list, traverse, and read-attribute rights by role; separate ordinary users, service accounts, backup, indexing, antivirus, and administrator identities; validate effective and inherited rights and remove broad or expired visibility.
2. `access-based-share-visibility` / 基于访问的共享可见性，`exposure-reduction`：对适用 SMB/DFS 共享启用并测试 Access-based Enumeration，使无权访问的名称不在正常列表中出现，同时以 share/NTFS 权限阻止已知路径直接访问。记录 CPU/延迟基线并对高负载共享分阶段部署。 / Enable and test Access-based Enumeration on suitable SMB or DFS shares so names without access rights do not appear in normal listings, while share and NTFS permissions still block direct access to known paths. Record CPU and latency baselines and stage rollout on high-load shares.
3. `index-and-catalog-query-governance` / 索引与 catalog 查询治理，`exposure-reduction`：登记批准的搜索、备份、杀毒、DLP 和资产 inventory 服务及其 owner、身份、覆盖根和 query clients；限制服务/IPC/catalog 数据库访问和本地安装权限，在业务允许时排除高敏根，并以应用控制阻止未批准索引器或便携搜索工具。 / Register approved search, backup, antivirus, DLP, and asset-inventory services with owner, identity, covered roots, and query clients; restrict service, IPC, catalog-database, and local-install access; exclude highly sensitive roots where operations permit; and use application control against unapproved indexers or portable search tools.
4. `targeted-enumeration-audit-and-baseline` / 定向枚举审计与基线，`detective-support`：启用并验证 4688 command line、4104、重点目录 4663 SACL、文件服务器 Detailed File Share 以及经性能测试的 Linux process/syscall telemetry；维护批准 reader 台账，定期以受控查询验证路由、字段、关联和保留。 / Enable and validate 4688 command lines, 4104, targeted 4663 SACLs, Detailed File Share auditing, and performance-tested Linux process or syscall telemetry; maintain an approved-reader registry and use controlled queries to test routing, fields, correlation, and retention.
5. `enumeration-to-successor-response` / 枚举到后继动作处置，`containment`：确认异常枚举后保全进程、会话、query、根路径和结果线索，冻结相关远程会话或 token，隔离必要主机，并分别调查后继读取、凭据取得、暂存、打包、加密和删除；不能以阻断后继动作替代对发现范围的确认。 / After anomalous enumeration, preserve process, session, query, roots, and result leads; freeze the relevant remote session or token, isolate hosts as needed, and investigate later reads, credential acquisition, staging, archiving, encryption, and deletion separately. Blocking a successor does not replace establishing discovery scope.

**未来父级 application：**

- **use zh：** 对 T1083 将用户、服务和远程会话绑定到最小路径/share 可见范围，治理索引/catalog 入口，并把批准 reader 与进程、脚本、目录和共享审计持续比较。
- **use en:** For T1083, bind users, services, and remote sessions to the minimum path and share visibility, govern index and catalog entries, and continuously compare approved readers with process, script, directory, and share audit.
- **expected effect zh：** 减少失陷身份可列出的名称和层级，使异常主体、范围、来源及后继动作更易关联，并避免只靠工具名检测。
- **expected effect en:** Reduce names and hierarchy enumerable by a compromised identity, make anomalous principal, scope, origin, and successor activity easier to correlate, and avoid reliance on tool names alone.
- **limitations zh：** 本机用户仍可列出其正常可见路径；ABE 不阻止已知路径访问且可能增加服务器负载；备份、索引、杀毒和开发常需广域读取；被盗批准身份可保持正常外观；catalog 副本和离线清单无法由源目录 ACL 撤回；严格权限或审计可能破坏业务或产生高事件量。
- **limitations en:** A local user can still enumerate normally visible paths. ABE does not block access to a known path and can add server load. Backup, indexing, antivirus, and development often need broad reads. A stolen approved identity can retain a normal appearance, catalog copies and offline inventories cannot be revoked by source-directory ACLs, and aggressive permissions or auditing can disrupt operations or create high event volume.

对 `D07-03-T1083-SUB-INDEX` 只保留条件性设计：限制 index service/query IPC/catalog DB 及报告文件访问，记录 query client，并审计后继 path open；预期恢复替代观察面；限制为 provider 无 query log、离线副本、索引陈旧和攻击者自行重建。该 application 在子项获准前不得写入正式 MIT。

## 9. 共享库 reuse / extend / create / split / defer 决议

| 对象或临时键 | 建议 | 语义与去重理由 |
|---|---|---|
| `REF-000625` | **`extend` locator/notes 后 `reuse`** | canonical URL 已存在；增加 T1083 parent behavior、TA0007 mapping 和 0-child inventory，不复制 19.1 STIX REF |
| `REF-000623` | `reuse` | 4688 与 command-line 配置前提完全相同；不扩写为 API 枚举可见性 |
| `REF-000463` | `reuse` | 4104 channel 和启用前提完全相同；不证明其他解释器 |
| `REF-000379` | **`extend` locator 后 `reuse`** | 同一 4663 URL；locator 增加目录 `ListDirectory` 权限及 SACL 前提，不另建 REF |
| `REF-000474` | **`extend` locator 后 `reuse`** | 同一 5145 URL；增加目录/共享访问检查和 AccessList 用途，继续保留“不是完成结果”限制 |
| `D07-03-T1083-REF-CISA-ENERGY`, `REF-CISA-MISCONFIG`, `REF-TREND-MIMIC`, `REF-VOID-OPTIONS`, `REF-VOID-SERVICE`, `REF-LINUX-GETDENTS`, `REF-LINUX-AUDITCTL`, `REF-MS-ABE` | `create`，主审按 canonical URL 最终查重 | 当前精确 URL/标题检索未命中；每项分别支持父案例、攻击样本、索引架构、系统调用、审计前提或缓解限制，不能相互代替 |
| `D07-03-T1083-CLM-PARENT` | `create` | 原子命题：路径、名称、层级、存在性和列表属性构成独立 Discovery 结果，固定版与 CISA 共同支持 |
| `D07-03-T1083-CLM-BOUNDARY` | `create` | 原子命题：路径列表不证明正文读取、凭据取得、打包或外传；用于约束 Technique 与 DET |
| `D07-03-T1083-CLM-NMFD` | `create` | 原子机制命题：恶意枚举与正常浏览/盘点功能外观汇合，使单事件难以分类；不包含索引盲点 |
| `D07-03-T1083-CLM-AUDIT` | `create` | 原子数据命题：4688/4104/4663/5145 和 Linux syscall 依赖配置且结果语义不同，缺事件不能证明未枚举 |
| `D07-03-T1083-CLM-INDEX` | `defer` | 只可写 hypothesis：观察面可从目录遍历迁移至 index/catalog；缺规避选择、同案 trace 和 query telemetry，不进正式 Claim |
| `D07-03-T1083-CASE-DIRSB` | `create`，范围受限 | CISA 联合通告提供离散行为事实：国家支持行为者用 `dirsb.bat` 收集网络主机文件夹/文件名；不附加内容读取或规避结论 |
| Mimic CASE | `defer` | Trend Micro 是样本/家族技术分析，不是足以建立受害者、时段和离散事件身份的 canonical Case；可支撑 REF/CLM，不制造事件 CASE |
| `NJA-000102` / `DET-000114`（已存在的关键对象跳过与破坏结果） | `split`，不 extend | 该分析需要枚举、排除谓词、处理/保留集合和破坏结果，检测选择性影响；T1083 检测路径发现本身并明确分离后继加密/擦除 |
| `NJT-0138` 与其 DET/NJA/MIT | `split`，仅作 boundary reuse | 浏览历史数据库读取和浏览上下文解析的数据与目标不同；找到该数据库路径仍由 T1083 独立表达 |
| `NJT-0141` 与其 DET/NJA/MIT | `split`，仅作 boundary reuse | 云对象 key/prefix 和 provider data-event 不等于主机/网络文件系统目录项；不能把云 List Analytic 改标题复用 |
| Collection 文件读/打包 DET/NJA/MIT | `split`，只关联 successor | 内容 open/read、copy、archive 与 namespace list 的数据、阶段和结论不同；文件读防御不得冒充目录发现防御 |
| `D07-03-T1083-DET-NAMESPACE`, `NJA-WINDOWS`, `NJA-POSIX`, `MIT-NAMESPACE` | `create` | 当前共享库没有相同检测目标、数据模型和控制应用；Windows/POSIX 是同一父策略的实施分析，不是 NJS |
| `D07-03-T1083-NJA-INDEX`、`SUB-INDEX` 及其 Claim/MIT application | `defer` | query channel 与字段未验证，target_ref 不存在；不得预留正式 ID 或提前写共享对象 |
| Discovery → Collection/Impact 关系 | `defer` 至父级分配后逐案例决定 | CISA/Trend 只能支持各自有限后继语境；不能用临时键创建 REL，也不能把一般“用于后继”写成离散案例关系 |

## 10. 研究门禁、自检和交接结论

- `recommendation.decision: retain`；父级 `confidence: high`；`original_attack_subtechniques_imported: false`。
- 固定 ATT&CK 19.1 子项 `0 / []`；已完成开放式多轴搜索；正式 Niji child `0`；taxonomy `coverage: deferred`，因为索引轴可复审但未过证据门禁。
- 7 个轴已逐项给出 `formal-parent-core / defer / reject`；没有按产品、平台、API、路径、文件类别或资源类别拆 NJS。
- 父行为由固定版和 CISA 一手材料支持；Mimic/Everything 只支持索引候选的恶意使用与架构，不越级证明匿迹意图或检测失败。
- 父级双语草案覆盖定义、匿迹特性、范围、场景、攻击者模型、防守方模型、机理、taxonomy 和限制；deferred 子项具备双语核心字段并明确缺口。
- DET 定义命名空间发现目标；Windows 与 POSIX NJA 分别列真实通道、必需字段、逻辑、窗口、维度、误报、盲区和调优；索引 query 未验证，保持 deferred。
- MIT 给出最小 list/traverse 权限、ABE、index/catalog 治理、定向审计和响应 Measure，以及逐父目标 use/effect/limitations；ABE 限制和正常业务成本均已保留。
- 与 NJT-0138、NJT-0141、T1135、TA0009、凭据搜索、隐藏文件及文件读取/打包边界已逐项固定；索引、备份、杀毒、开发、用户浏览和运维反例进入父级与 Analytic。
- 已按 canonical URL、事件身份和语义目标给出 `reuse/extend/create/split/defer`；未分配正式 ID，未修改正式矩阵或共享库。
- 与 NJT-0001 的比较结论：字段职责和因果链已覆盖；没有复制其子项数量、机制数量或防御对象数量。正式化前仍需主 Agent 完成五候选横向收敛、共享库最终查重、受控 telemetry 验证、schema 写入、Bundle、quality 与中英文 Web QA。

**主 Agent 可直接采用的收敛建议：retain T1083，建立父级 NJT 与父级 DET/NJA/MIT，当前不分配 NJS；把 Indexed Namespace Query 留为带明确证据门的 deferred 候选。**
