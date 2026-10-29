# T1652 Device Driver Discovery / 设备驱动程序发现研究交接

## 准入建议

建议 `adapt`，父级置信度 high，原生子项 0，taxonomy `deferred`。固定 ATT&CK Enterprise 19.1 行确认 T1652 是 Discovery 父项且无 ATT&CK 子技术。HOPLIGHT 查询 `HKLM\Software\WBEM\WDM`，INC Ransomware 检查 Print to PDF/XPS 驱动，Medusa 使用 `driverquery`，Remsec 检测安全产品活动驱动；这些案例共同支持保留驱动事实这一独立信息对象。Niji 应将驱动包、安装状态、加载/活动状态、加载地址和设备能力明确分层，避免把工具输出当作权威状态。

`Adapt` is recommended with high confidence for the parent, zero formal native children, and deferred taxonomy. The fixed Enterprise ATT&CK 19.1 row confirms T1652 as a Discovery parent with no ATT&CK children. HOPLIGHT queried `HKLM\Software\WBEM\WDM`, INC Ransomware checked Print to PDF and XPS drivers, Medusa used `driverquery`, and Remsec identified active security-product drivers. These observations support retaining local driver facts as a distinct information object. Niji should separate package presence, installation state, loaded or active state, load address, and device capability rather than treating utility output as authoritative state.

## 证据界线

- ATT&CK T1652 固定父页：锚定父行为和平台，不证明 Niji 子项或匿迹效果。
- Microsoft `EnumDeviceDrivers`：返回系统驱动加载地址；Windows 11 24H2 起，无 `SeDebugPrivilege` 时调用仍可成功但地址全为 `NULL`。全空结果不是“无驱动”。
- Microsoft Installed Driver Package Inventory：推荐 `PnPUtil /enum-drivers` 建第三方驱动包清单，并指出 `driverquery` 输出可能误导。驱动包存在不等于当前加载。
- ATT&CK 的 HOPLIGHT、INC、Medusa、Remsec 过程资料分别证明注册表、功能存在性、系统工具和安全驱动识别，但每项不能越级证明其他结果语义。

## Niji 原生轴

| 轴 | 痕迹与防守差异 | 决议 |
|---|---|---|
| 查询结果状态：包/安装/加载/能力 | 不同数据源可能返回不同状态，调用成功也可能只有空值；分析必须保留 `unknown` | 父级结构变量；不拆 NJS |
| 结果可信度与版本/权限 | 24H2 与 `SeDebugPrivilege` 改变 EnumDeviceDrivers 可用结果 | 检测上下文，`defer` 子项 |
| 工具/注册表/API 读取路径 | 进程、注册表和 API telemetry 不同，但接口可替换 | `not-stealth-distinct` |
| 面向安全产品的驱动解析 | 需要版本化 driver→product 映射；仅驱动名不能证明目的 | 父级/相邻 Security Software Discovery；`defer` |
| 驱动指标门控后继行为 | 若虚拟化驱动或易受攻击驱动决定后续执行，可能形成 T1497/BYOVD 等结果 | 相邻技术，非 T1652 NJS |
| 厂商/驱动类别 | 产品分类不稳定、会无限扩张 | `reject` |

正式 NJS 为 0。后续子项至少需要多个独立恶意案例、稳定状态边界和不同检测/缓解方法。

## 范围边界

T1652 只负责取得本机驱动名称、版本、存在性、安装/加载状态、地址或能力。普通应用清单归 Software Discovery；服务状态与进程清单分别归 System Service Discovery 和 Process Discovery。若驱动明确映射到防护产品，可附加 Security Software Discovery；若驱动指标决定在虚拟化/沙箱中退出或变更行为，可附加 T1497。获取、安装或加载易受攻击驱动、触发驱动漏洞和实际 BYOVD 是后继行为，必须与发现事件分开。

T1652 owns acquisition of local driver names, versions, presence, installation or load state, addresses, and capabilities. Ordinary applications, services, and processes remain under their corresponding discovery techniques. Explicit mapping from a driver to a protection product may also support Security Software Discovery; a driver indicator that gates behavior in a virtualized or sandbox environment may also support T1497. Acquiring, installing, loading, exploiting, or abusing a vulnerable driver is a later act and must remain separate from discovery.

## 父级双语核心内容

**Definition.** 设备驱动程序发现是攻击者查询本机驱动及其元数据，以理解主机功能、防护组件、虚拟化线索或潜在后继机会的行为。它可通过系统工具、API 或驱动相关注册表读取完成，但分类依据是取得的驱动事实，而不是接口名称。 / Device Driver Discovery queries local drivers and metadata to understand host function, defensive components, virtualization clues, or later opportunities. System utilities, APIs, or driver-related registry reads can implement it, but the acquired driver fact rather than interface name defines the behavior.

**Stealth characteristics.** 驱动枚举经常与资产管理、兼容性和故障排查使用同一已签名工具或系统接口，单条进程/API 事件的恶意性难判；驱动查询、命令行、注册表访问和后继结果仍可见。结果语义若未结合系统版本、权限和权威资产基线，防守方还可能把空值、包存在或误导输出解释成真实加载状态。 / Driver enumeration often uses the same signed utilities and system interfaces as inventory, compatibility, and troubleshooting, making one process or API event hard to classify. Query, command-line, registry, and later outcome traces remain. Without operating-system version, privilege, and authoritative asset context, defenders may also mistake null values, package presence, or misleading output for actual loaded state.

**Threat models.** 攻击者至少需要执行查询工具或调用接口的本机权限；获取加载地址还受系统版本和 `SeDebugPrivilege` 限制。防守方需要进程谱系、命令行、注册表读取或经验证的 API telemetry，以及按主机角色维护的驱动资产基线。合法资产、打印支持、诊断、安全产品与驱动更新是主要反例。 / The adversary needs local authority to run a query or call an interface; retrieving load addresses also depends on OS version and `SeDebugPrivilege`. Defenders need process lineage, command line, registry read or validated API telemetry, and driver-asset baselines by host role. Asset inventory, print support, diagnostics, security products, and driver maintenance are major counterexamples.

**Mechanism candidate.** `NM-FD`, medium: 攻击者借用原生驱动清单工具或接口，使查询外观接近日常资产与故障排查；单事件难辨目的，结合罕见调用者、结果语义和后继行为才能恢复判断。现有案例证明恶意枚举，未量化漏报。 / `NM-FD`, medium: the adversary uses native driver-inventory tools or interfaces whose appearance resembles routine asset and troubleshooting work. Purpose is hard to classify from one event and requires rare-caller, result-semantics, and follow-on context. Incidents establish malicious enumeration, not a measured miss rate.

## DET / NJA 建议

建立一个“驱动事实查询谱系”策略，至少含两个分析分支：

1. **原生工具与注册表读取。** 数据要求：进程 `timestamp, host_id, user_id, process_guid, image, command_line, parent_guid, signer, hash`；注册表 `path, action, value`。匹配 `driverquery.exe`、`pnputil.exe /enum-drivers` 和 `HKLM\Software\WBEM\WDM` 读取，按主机角色、账户、父进程与维护窗口基线；不得把 PnPUtil 结果标为 loaded，也不得把一次注册表打开写成取得具体字段。
2. **EnumDeviceDrivers 结果语义。** 仅在 EDR/API sensor 经验证时使用 `api_name, return_value, result_count, null_count, os_build, token_privileges`；24H2 无 SeDebugPrivilege 且全 NULL 表示尝试未取得有效地址。普通日志不见 API、内存内调用和结果缓冲区缺失是盲区。

误报包括资产清单、驱动部署、打印支持、取证、性能与安全工具。调优不可按 Microsoft 签名或工具名永久放行；例外应绑定 owner、主机角色、版本、路径和期限。若能取得查询结果，可用版本化 driver→security-product 映射提高置信度，但无结果时只报一般驱动发现。

## MIT 建议

- `detective-support`：维护驱动包/安装/加载状态、版本、签名和哈希的权威基线，给分析提供结果解释与后继 BYOVD 检查。
- `preventive`：按主机角色限制未授权代码执行，减少自定义 API/注册表查询机会；原生工具仍可被滥用。
- `exposure-reduction`：审计并收缩非必要 `SeDebugPrivilege`。这只在受支持 Windows 版本降低有效加载地址返回，不能阻止工具、注册表或其他接口发现。

逐目标应用应说明：控制不能全面阻止本机合法发现；主要效果是提高查询归因、降低高价值地址结果与约束后继异常驱动使用。限制包括旧版系统、API 可见性、合法诊断需求和本地基线维护成本。

## 共享库决议与限制

复用现有 Microsoft vulnerable-driver 与 driver-block 来源只用于后继 BYOVD/治理边界，不把它们当作发现证据。建议新建 T1652 固定父来源、EnumDeviceDrivers 文档、Microsoft driver inventory 文档，以及确有精确过程事实时的 HOPLIGHT/INC/Medusa/Remsec来源；检测与缓解应 `create/split`，不能扩充现有驱动加载策略。

研究限制：公开案例缺父进程、频率、输出与完整后继时间线；HOPLIGHT 未披露返回字段；driverquery 结果不权威；PnPUtil 只证明包；当前结论主要支持 Windows，不能无证扩到 Linux/macOS。发现目的通常不能由一次查询确认，不能自动推断安全软件识别、T1497 或 BYOVD 选择。
