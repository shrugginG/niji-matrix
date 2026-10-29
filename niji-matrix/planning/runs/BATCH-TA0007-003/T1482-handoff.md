# T1482 Domain Trust Discovery / 域信任发现：只读研究交接

工作项 `WORK-TA0007-T1482`；批次 `BATCH-TA0007-003`；临时键前缀 `D07-03-T1482-*`。本文只提交主 Agent 待收敛的研究结果；未分配 NJT/NJS/REF/CLM/CASE/DET/NJA/MIT 正式 ID，未修改正式矩阵、共享库、TA0007 计划或 ID 预留。文中的 `formal` 只表示建议进入父级正式内容，不代表已取得正式对象身份。

## 1. 准入结论与固定基线

**建议 `adapt`，整体置信度 medium；域/林父行为置信度 high，租户扩展置信度 medium；正式 Niji 子项 0，taxonomy `deferred`。** 固定 ATT&CK Enterprise 19.1 工作簿 `data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx` 的 `T1482` 行记录 `Domain Trust Discovery`、战术 `Discovery`、平台 `Windows`、`is sub-technique=0`；批次清单确认没有 `T1482.*` 子技术，因此固定版 ATT&CK 子项数为 `0`、ID 为 `[]`，且 `original_attack_subtechniques_imported: false`。固定 19.1 的 DET0007/AN0016 把 `nltest`、PowerShell、Win32/.NET API 和 LDAP 信任枚举列为检测对象，但不证明任何 Niji 子项或规避效果。

**准入理由（zh）：** T1482 的稳定直接对象是身份信任拓扑：域、林或租户身份边界之间有哪些信任边，边的方向、类型、属性、伙伴身份与可达含义是什么。Microsoft 对 `DsEnumerateDomainTrusts`、trusted-domain 结构和 Microsoft Entra 跨租户访问策略的文档证明这些信息是可查询、可区分且能影响身份边界可达性的独立对象；Microsoft 对 Storm-0501 的调查以及 CISA 对 Akira 和伊朗行为者的联合通告直接证明攻击者会查询域/林信任信息。Niji 应把父级从仅限 Windows 多域/林的表述适配为“身份信任边界发现”，同时明确租户策略读取目前只有能力和审计依据，没有本轮一手恶意案例。

**Admission rationale (en):** T1482 has a stable direct object: identity trust topology, consisting of trust edges among domains, forests, or tenant identity boundaries and their direction, type, attributes, partner identity, and reachability meaning. Microsoft documentation for `DsEnumerateDomainTrusts`, trusted-domain structures, and Microsoft Entra cross-tenant access policies establishes that these are queryable, distinguishable facts that govern identity-boundary reachability. Microsoft's Storm-0501 investigation and CISA advisories for Akira and Iranian actors directly establish adversarial domain or forest trust discovery. Niji should therefore adapt the Windows-only parent into Identity Trust Boundary Discovery while stating that the tenant-policy branch currently has capability and audit evidence but no first-party malicious case in this review.

**零 NJS 理由（zh）：** 本轮检查了合法管理表象、权威查询与缓存视图、全图与定向边查询、时间和来源分布、返回属性投影以及跨本地/租户观察面的变化。现有材料能证明攻击行为、合法管理反例、接口能力和可用日志字段，却没有同一事件中的攻击者选择—痕迹变化—防守效果对照，也没有独立缓解价值的实测结论。所有未证轴均保持 `defer`；不按 AD/Entra、LDAP/API/CLI、域/林/租户、信任类型或产品拆 NJS。

**Why zero NJS (en):** The review examined legitimate-administration appearance, authoritative queries versus cached views, full-graph versus targeted-edge queries, distribution over time or sources, returned-attribute projection, and movement between on-premises and tenant observation planes. The evidence establishes adversarial behavior, legitimate counterexamples, interface capabilities, and available telemetry fields, but it does not provide a same-incident comparison from attacker choice through trace change to defender effect or a measured, independently useful mitigation difference. Every unproven axis remains deferred, and no child is partitioned by AD versus Entra, LDAP/API/CLI, domain/forest/tenant, trust type, product, or tool.

## 2. 一手证据与支持边界

| 临时证据键 | 来源与共享库建议 | 直接支持 | 不支持或必须校准 |
|---|---|---|---|
| `D07-03-T1482-REF-ATTACK19` | [MITRE ATT&CK v19 T1482](https://attack.mitre.org/versions/v19/techniques/T1482/) 及本地 19.1 工作簿；优先核查既有基线 REF 后 `reuse/extend`，否则按版本化 URL `create` | 固定父行为、Discovery 映射、Windows 平台、0 个 ATT&CK 子技术及 procedure 清单 | 不证明租户扩展、Niji 子项、匿迹机理、检测字段完整性或检测效果 |
| `D07-03-T1482-REF-DET0007` | 本地 19.1 `detectionstrategies.xlsx` 第 493 行、`analytics.xlsx` 第 17 行及映射行；[ATT&CK DET0007](https://attack.mitre.org/detectionstrategies/DET0007/)；建议 `create` 或并入版本化 ATT&CK REF | AN0016 的目标是 `nltest`、`Get-ADTrust`、`GetAllTrustRelationships`、Win32/.NET API 与 LDAP 枚举；映射列出 Sysmon 1/7/10、PowerShell 和 Security 4662 | 没有给出可直接部署的阈值、完整字段合同或实测性能；Sysmon 模块加载或进程访问不能单独证明调用了某个函数 |
| `D07-03-T1482-REF-STORM0501` | [Microsoft Threat Intelligence: Storm-0501](https://www.microsoft.com/en-us/security/blog/2024/09/26/storm-0501-ransomware-attacks-expanding-to-hybrid-cloud-environments/)；建议 `create` | Microsoft 观察到攻击者在入侵后使用原生 Windows 工具（包括 `nltest.exe`）查找一般域信息和 domain forest trust，随后进入凭据访问与横向移动 | 未披露完整命令行、返回边、LDAP/API 字段或规避选择；云枢纽部分不证明其读取了跨租户访问策略 |
| `D07-03-T1482-REF-CISA-IRAN` | [CISA/FBI/NSA AA24-290A](https://www.cisa.gov/sites/default/files/2024-10/aa24-290a-iranian-cyber-actors-conduct-brute-force-and-credential-access-activity.pdf)；建议 `create` | 行为者使用 `nltest /domain_trusts` 和 `/domain_trusts/all_trusts` 了解受害环境中的 trusted domains，并另行查询域控制器、管理员与主机 | 不能把同一通告中的账户、组、主机和后继利用合并为 T1482；未证明 `/all_trusts` 是为匿迹选择 |
| `D07-03-T1482-REF-CISA-AKIRA` | [CISA/FBI/EC3/NCSC-NL AA24-109A](https://www.cisa.gov/sites/default/files/2024-04/aa24-109a-stopransomware-akira-ransomware_2.pdf)；建议 `create` | Akira 关联命令包括 `nltest /DOMAIN_TRUSTS`，与域控、组和进程发现并列 | 只证明恶意父行为；不证明缓存、定向、低速或分布式轴 |
| `D07-03-T1482-REF-MS-DSENUM` | [Microsoft DsEnumerateDomainTrusts](https://learn.microsoft.com/en-us/windows/win32/api/dsgetdc/nf-dsgetdc-dsenumeratedomaintrustsa)；建议 `create` | 认证域用户可取得指定域的信任数据；flags 可区分直接入站、直接出站、林成员与树根；非 DC 可使用最长约五分钟的未过期缓存 | 文档证明架构，不证明攻击者有意利用缓存、查询一定不触达 DC 或检测一定漏报 |
| `D07-03-T1482-REF-MS-TRUSTSTRUCT` | [TRUSTED_DOMAIN_INFORMATION_EX](https://learn.microsoft.com/en-us/windows/win32/api/ntsecapi/ns-ntsecapi-trusted_domain_information_ex)、[trustDirection](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/5026a939-44ba-47b2-99cf-386a9e674b04)、[trustAttributes](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/e9a2d23c-c31e-4a6f-88a0-6646fdb51a3c) 与 [TDO essential attributes](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/c9efe39c-f5f9-43e9-9479-941c20d0e590)；建议按 canonical URL 分别 `create` | 信任对象包含伙伴名称/SID、direction、type、attributes、林信息与认证相关属性，足以界定父级信息对象 | 不证明读取者目的或某一属性查询构成独立 NJS |
| `D07-03-T1482-REF-MS-NLTEST` | [Microsoft Nltest](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc731935%28v%3Dws.11%29)；建议 `create` | `/domain_trusts` 是列出既有信任关系的合法管理用法，为强正常反例 | 合法能力文档不是攻击案例，也不证明命令天然低噪声 |
| `D07-03-T1482-REF-MS-IDENTITYQUERY` | [Microsoft Defender XDR IdentityQueryEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identityqueryevents-table)；建议 `create` | 表可提供 AD 对象查询的 `Timestamp, ActionType, Application, QueryType, QueryTarget, Query, Protocol` 与账户字段，适合信任查询语义分析 | 只有部署 Defender for Identity/Sentinel/Entra 相应数据时才有记录；具体 ActionType 必须在目标租户 schema 中验证 |
| `D07-03-T1482-REF-MS-XTENANT` | [Microsoft Entra cross-tenant access overview](https://learn.microsoft.com/en-us/entra/external-id/cross-tenant-access-overview) 与 [Graph list partners](https://learn.microsoft.com/en-us/graph/api/crosstenantaccesspolicy-list-partners?view=graph-rest-1.0)；建议分别 `create` | 跨租户策略有 inbound/outbound、partner、trust 和同步语义；持有 `Policy.Read.All` 等权限的主体可列出 partner configurations | 只证明能力、权限和返回模型；本轮没有攻击者读取该资源的第一方案例 |
| `D07-03-T1482-REF-MS-GRAPHLOG` | [Microsoft Graph activity logs](https://learn.microsoft.com/en-us/graph/microsoft-graph-activity-logs-overview)；建议 `create` | Graph 请求可记录 `RequestUri, RequestMethod, AppId, UserId, IPAddress, DeviceId, Roles, Scopes, SessionId, ResponseStatusCode, ResponseSizeBytes` 等字段 | 需 P1/P2、Azure 诊断设置和保留；成功响应不证明攻击者实际使用了所有返回信息 |
| `D07-03-T1482-REF-MS-1644` | [Microsoft Event 1644 LDAP query guidance](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/event1644reader-analyze-ldap-query-performance)；建议 `create` | 1644 可在满足阈值和诊断配置时记录 DC 处理的昂贵、低效或慢 LDAP 搜索 | 不是完整 LDAP 审计，普通且高效的 trustedDomain 查询可能不出现；不应作为唯一通道 |

建议原子 Claim 分为：`D07-03-T1482-CLM-PARENT`（域/林信任拓扑发现）、`D07-03-T1482-CLM-TENANT-SCOPE`（跨租户策略是同类身份边界拓扑，置信度 medium）、`D07-03-T1482-CLM-DUAL-USE`（恶意与合法管理可使用同形原生查询）、`D07-03-T1482-CLM-BOUNDARY`（发现止于取得拓扑，后继票据/移动另记）和 `D07-03-T1482-CLM-ZERO-NJS`（当前无轴通过正式子项门禁）。建议三个互不合并的 Case：`D07-03-T1482-CASE-STORM0501`、`D07-03-T1482-CASE-CISA-IRAN`、`D07-03-T1482-CASE-AKIRA`。跨租户读取 Case 保持 `defer`。

## 3. 父行为、事务终点与硬边界

父行为的直接对象是**身份信任边界图**。节点是域、林或租户组织；边至少包含 partner、方向、类型、属性、传递/隔离语义及可达含义。事务在攻击者获得足以选择后续边界、目标或身份路径的信任事实时结束。命令、API、LDAP、PowerShell、管理门户和 Graph 只是取得同一信息对象的入口，不是 NJS 身份。

| 相邻对象 | 归属判据 | 与 T1482 的硬边界 |
|---|---|---|
| T1087 Account Discovery / `NJT-0131` | 直接问题是有哪些账户、UPN、SID 或身份名单 | T1482 问域/林/租户之间信任哪一方、方向和属性；查询返回 owner 或管理员名称不自动转成账户发现，除非账户集合也是独立求取对象 |
| T1069 Permission Groups Discovery | 直接问题是组、成员与权限角色 | `Domain Admins`、`Enterprise Admins` 枚举归组权限；信任边允许哪一身份域被接受归 T1482。CISA 通告中的两类命令必须分开标注 |
| T1615 Group Policy Discovery | 直接问题是 GPO 内容、链接、优先级和有效策略 | 信任属性不是 GPO；随后读取影响跨域访问的 GPO 需独立证据 |
| 网络主机/域控制器/服务发现 | 直接问题是哪些主机、DC、IP、端口或服务可达 | `nltest /dclist` 与主机扫描归相邻发现；`/domain_trusts` 的对象才是信任边。发现 DC 不等于发现信任方向或类型 |
| T1484 Domain or Tenant Policy Modification 与 `NJT-0100` | 写入、删除或改变 domain trust、federation 或 tenant policy | T1482 只读并取得拓扑；创建、修改、禁用或回退信任是另一事务，不能由一次 read 推断 write |
| 票据滥用、SID-History、Kerberoasting 与横向移动 | 使用发现结果伪造/重放票据、改变令牌或访问远程资源 | T1482 到取得信任事实为止；后继必须有独立票据、认证或远程访问结果。DET 可把后继作为优先级上下文，但不能把它设为确认发现的必需条件 |
| `NJT-0106` 环境检查 | 读取环境条件并据此显式门控、改变或停止后续行为 | 单纯取得信任拓扑归 T1482。只有证据表明“某信任是否存在”直接控制继续/退出分支时，才可把门控事务另行标记 NJT-0106；不得复用其子项替代 T1482 |
| 正常反例 | AD 健康、域/林迁移、并购整合、身份治理、访问审查、跨租户协作配置、审计、故障排查和事件响应 | 工具名、成功查询、认证用户或 `Policy.Read.All` 本身都不判恶；需主体职责、来源、批准窗口、查询对象、范围变化和后继上下文 |

## 4. Niji 原生轴：formal / defer / reject

固定版 ATT&CK 子项为 0，适用普通广度触发。本轮完成开放式搜索；没有 formal NJS。

| 轴与临时键 | 攻击者变量 → 痕迹变化 → 防守观察差 | 决议 |
|---|---|---|
| `D07-03-T1482-AX-01` 合法管理表象借用 / Legitimate administrative appearance borrowing | 使用 `nltest`、PowerShell、目录查询或获准 Graph 读取 → 请求保留真实工具/身份/对象但与健康检查、迁移和治理读取同形 → 单事件难以区分控制者目的，需职责与后继关联 | **`formal: parent-core`**，建议父级 `NM-FD`；不拆 NJS。Storm-0501/CISA 证明恶意原生查询，Microsoft 管理文档证明合法同形用途，但未量化漏报 |
| `D07-03-T1482-AX-02` 缓存或既存信任视图复用 / Cached or preexisting trust-view reuse | 从非 DC 的未过期缓存或已保存输出取得拓扑 → 当前可能缺少新的权威目录请求，转而留下本地调用/文件/进程痕迹 → 仅看 DC 查询的分析可能漏掉当前取图 | **`defer`**。Microsoft 证明 `DsEnumerateDomainTrusts` 的五分钟缓存语义，但无恶意案例、攻击者可控命中条件或同案检测差；不得复用 `NJS-0131-001`，其对象是账户身份视图 |
| `D07-03-T1482-AX-03` 全图与限域边查询 / Full-graph versus scoped-edge enumeration | 选择 `/all_trusts`、直接入/出站 flags、特定伙伴或定向 LDAP 条件 → 返回边数、命令参数和可能的查询扇出变化 → 只按广度计数的检测可能降分 | **`defer`**。CISA 证明 `/domain_trusts` 与 `/all_trusts` 均被使用，接口文档证明 scope 可控；没有证据表明窄查询出于规避、改变了告警或需要独立缓解 |
| `D07-03-T1482-AX-04` 多源或低速信任图拼接 / Distributed or low-rate trust-graph assembly | 跨主机、身份或时间分段查询不同边 → 每个局部窗口只见少量关系 → 单源短窗难重建完整图 | **`defer`**。属于稳定候选变量，但本轮没有实际恶意分工、可归属同一控制者的证据或实测窗口差；仅进入 NJA 的长窗调优 |
| `D07-03-T1482-AX-05` 返回属性投影 / Projected trust-attribute retrieval | 只选择 tenantId、direction、type、attributes 或同步状态 → 响应大小和暴露字段减少，请求 URI/filter 可能仍可见 → 依赖全对象或高响应量的检测可能弱化 | **`defer`**。Graph `$select/$expand` 与 LDAP 属性选择证明能力，不证明恶意使用或独立防御价值；属性类别不能直接成为 NJS |
| `D07-03-T1482-AX-06` AD/Entra、LDAP/API/CLI、域/林/租户或信任类型拆分 | 改变实现、平台或数据字段 → 日志通道不同，但直接信息对象仍是身份信任边界图 | **`reject`** 作为 NJS；这些差异只用于数据源分支、权限前提和边界测试 |
| `D07-03-T1482-AX-07` 以认证/票据主动验证可达性 | 对发现边发起 Kerberos、远程登录或资源访问 → 产生认证和服务结果 → 可确认实际可用路径 | **`reject`** 作为 T1482 NJS；这是后继票据使用或横向移动。可与 discovery 关联，但必须保持独立归属 |

**收敛：** `proposed_niji_child_count: 0`；`subtechnique_taxonomy.coverage: deferred`；`subtechnique_refs: []`。AX-01 只进入父级机理；AX-02 至 AX-05 全部未证并 `defer`；AX-06/07 `reject`。不为任何轴预留 NJS 或共享库正式 ID。

## 5. 父级双语核心字段

**临时父键与名称：** `D07-03-T1482-PARENT`；身份信任边界发现 / Identity Trust Boundary Discovery。

**summary** — 中文：攻击者查询域、林或租户身份边界之间的信任伙伴、方向、类型、属性与可达含义，以选择后续跨边界路径；这些读取常与合法目录健康、迁移和身份治理查询同形。 English: An adversary queries partners, direction, type, attributes, and reachability meaning across domain, forest, or tenant identity boundaries to select later cross-boundary paths; these reads often resemble legitimate directory health, migration, and identity-governance queries.

**definition_and_concept** — 中文：身份信任边界发现是在已取得目录、主机或租户策略读取能力后，恢复身份系统之间允许哪一方接受另一方认证或声明的关系图。域/林侧对象包括 trusted-domain partner、方向、类型、属性、林成员与传递语义；租户侧对象包括 partner-specific inbound/outbound access、信任声明和同步关系。其直接成果是信任边界图，而不是账户名单、组成员、主机清单或实际登录结果。CLI、LDAP、Win32/.NET、PowerShell 和 Graph 只是读取路径，不定义技术边界。 English: Identity Trust Boundary Discovery occurs after an adversary gains directory, host, or tenant-policy read capability and reconstructs the graph describing which identity system accepts another system's authentication or claims. Domain and forest facts include trusted-domain partners, direction, type, attributes, forest membership, and transitivity semantics; tenant facts include partner-specific inbound or outbound access, trusted claims, and synchronization relationships. The direct result is a trust-boundary graph rather than an account list, group membership, host inventory, or completed sign-in. CLI, LDAP, Win32 or .NET, PowerShell, and Graph are read paths rather than technique boundaries.

**stealth_characteristics** — 中文：信任拓扑读取经常是合法 AD 健康、迁移、身份治理和跨租户协作管理的必要动作，攻击者使用相同原生工具、查询语义或获准读取权限时，请求本身通常不编码恶意目的。单条 `nltest`、PowerShell、LDAP 或 Graph GET 仍可见，但其可区分性取决于调用主体是否承担信任管理职责、来源是否受管、范围和频率是否符合批准任务，以及是否出现独立的票据或横向移动结果。缓存视图、未启用的 Graph 活动日志、未部署的身份查询传感器和不完整命令行会造成观察缺口；明显的 `/all_trusts`、陌生父进程、非常见来源或异常 Graph app/session 仍是残余信号。 English: Trust-topology reads are often necessary for legitimate AD health, migration, identity governance, and cross-tenant collaboration administration. When an adversary uses the same native tools, query semantics, or entitled read permissions, the request normally does not encode malicious purpose. An individual `nltest`, PowerShell, LDAP, or Graph GET can remain visible, but distinguishability depends on whether the caller owns trust administration, whether the origin is managed, whether scope and cadence match an approved task, and whether separate ticket or lateral-movement outcomes follow. Cached views, disabled Graph activity logs, absent identity-query sensors, and incomplete command lines create observation gaps, while `/all_trusts`, an unusual parent process, an unexpected source, or an anomalous Graph app or session remain residual signals.

**scope_boundary_definition** — 中文：纳入攻击者有意取得域、林或租户之间的信任伙伴、方向、类型、属性、传递性、信任声明或同步关系，以判断身份边界与潜在可达路径。排除仅列账户、组、GPO、域控制器、主机、服务或网络连接的查询；这些对象即使与同一命令序列相邻，也按各自直接问题另记。创建、修改、删除或恢复信任，以及伪造票据、利用 SID History、Kerberoast、远程认证和横向移动均是后继行为。合法 AD 健康、并购迁移、身份治理、访问审查、故障排查和事件响应可产生同形读取，不能仅以工具、权限或查询成功判恶。 English: Include intentional acquisition of trust partners, direction, type, attributes, transitivity, trusted claims, or synchronization relationships among domains, forests, or tenants for reasoning about identity boundaries and potential paths. Exclude queries whose direct object is accounts, groups, GPOs, domain controllers, hosts, services, or network connections; even when adjacent in one command sequence, those objects retain their own classifications. Creating, modifying, deleting, or restoring trust and forging tickets, abusing SID History, Kerberoasting, remote authentication, or lateral movement are successor behaviors. Legitimate AD health, merger migration, identity governance, access review, troubleshooting, and incident response can issue identical reads, so tool name, permission, or query success alone does not establish maliciousness.

**application_scenarios** — 中文：攻击者在取得普通域身份、受控 Windows 主机、目录查询路径或租户策略读取令牌后，可先绘制信任边界，再选择需要高价值凭据、票据能力或跨环境访问的后续路线。Storm-0501 在被入侵网络中用原生工具寻找 domain forest trust；CISA 通告记录行为者运行普通和 all-trusts 形式。租户侧，持有 `Policy.Read.All` 或支持角色的主体可以列出 partner configurations，但本轮没有第一方恶意案例，因此该场景保持能力支持和 medium 置信度。 English: After obtaining an ordinary domain identity, a controlled Windows host, a directory-query path, or a tenant-policy read token, an adversary can map trust boundaries before selecting later routes that require privileged credentials, ticket capabilities, or cross-environment access. Storm-0501 used native tools to find domain forest trust in compromised networks, and CISA advisories record both ordinary and all-trusts forms. On the tenant side, a principal with `Policy.Read.All` or a supported role can list partner configurations, but this review found no first-party malicious case, so that scenario remains capability-supported at medium confidence.

**attacker_model** — 中文：域/林分支至少需要能够在域上下文中认证并执行查询、调用目录接口或访问相应 LDAP/RPC 路径；Microsoft 文档说明普通认证域用户即可调用 `DsEnumerateDomainTrusts`。攻击者还需理解方向、类型和属性如何映射到可能路径，但实际利用通常需要另外的凭据、票据或远程访问能力。租户分支需要可用令牌以及 `Policy.Read.All`、`Policy.ReadWrite.CrossTenantAccess` 或支持角色，且受条件访问、会话、云边界和 API 可用性约束。 English: The domain and forest branch requires an identity authenticated in the domain context plus an ability to execute a query, call a directory interface, or reach the relevant LDAP or RPC path; Microsoft documents that an authenticated domain user can call `DsEnumerateDomainTrusts`. The adversary must also understand how direction, type, and attributes map to potential paths, while exploitation normally requires separate credentials, tickets, or remote-access capability. The tenant branch requires a usable token and `Policy.Read.All`, `Policy.ReadWrite.CrossTenantAccess`, or a supported role and remains constrained by Conditional Access, session state, cloud boundary, and API availability.

**defender_model** — 中文：防守方可联合终端进程谱系和命令行、PowerShell script block、Defender for Identity 的 `IdentityQueryEvents`、经验证的目录对象访问事件以及 Microsoft Graph activity logs。每个通道覆盖不同入口：进程事件看不见内存内函数参数，1644 不是完整 LDAP 审计，4662 只有在对象审计实际配置并验证时才有意义，Graph 请求日志需预先启用且不会保存完整响应语义。防守方应按主体、来源、信任对象、查询范围、session/app 与批准任务关联，并把后继认证或横向移动仅作为独立加权证据。 English: Defenders can combine endpoint process lineage and command lines, PowerShell script blocks, Defender for Identity `IdentityQueryEvents`, validated directory-object access events, and Microsoft Graph activity logs. Each channel covers a different entry: process events do not reveal in-memory function arguments, 1644 is not complete LDAP auditing, 4662 is useful only when object auditing has been configured and validated, and Graph request logging must be enabled in advance and does not preserve complete response semantics. Defenders should correlate principal, origin, trust object, query scope, session or app, and approved work, treating later authentication or lateral movement only as independent severity evidence.

**stealth mechanism candidate** — `NM-FD`，`primary`，`medium`。摘要 zh：`借用合法信任管理查询表象降低单事件恶意可区分性`；summary en: `Borrow legitimate trust-administration query appearance to reduce single-event distinguishability`。分析 zh：攻击者使用原生 `nltest`、PowerShell、目录接口或获准 Graph 读取来取得信任图时，请求的主体、对象和方法可与健康检查、迁移或治理任务相同，单事件无法直接表达攻击目的；防守方必须引入职责、来源、范围、批准窗口和后继结果才能恢复判断。Microsoft 与 CISA 的事件证明恶意原生枚举，Microsoft 管理文档证明同形合法用途；证据未测量漏报率，也不支持把所有信任发现概括为低噪声。 Analysis en: When an adversary uses native `nltest`, PowerShell, directory interfaces, or an entitled Graph read to obtain a trust graph, the principal, object, and method can match health, migration, or governance work, so a single event does not directly express malicious purpose. Defenders must add role, origin, scope, approved window, and successor context to recover the distinction. Microsoft and CISA incidents establish malicious native enumeration, while Microsoft administrative documentation establishes identical legitimate use. The evidence does not measure miss rates and does not show that every trust-discovery implementation is quiet.

**subtechnique_taxonomy** — 中文：本轮不建立正式子技术。合法管理表象是父级共同机理；缓存视图、范围收敛、分布式拼接和属性投影缺少恶意选择与防守效果的结论级证据；平台、接口、资源字段和信任类型不能形成兄弟边界。 English: No formal child is proposed in this pass. Legitimate-administration appearance is a parent-wide mechanism; cached views, scope reduction, distributed assembly, and attribute projection lack conclusion-level evidence for adversary choice and defender effect; platforms, interfaces, resource fields, and trust types do not define sibling boundaries.

**research limitations** — 中文：公开一手案例证明攻击者查询域/林信任，但没有把同一事件的命令、目录请求、返回边、缓存命中、告警结果和后继路径完整联结。租户部分只有 Microsoft 的策略、权限和日志能力材料，没有攻击者读取 partner configurations 的第一方案例。固定 ATT&CK AN0016 提供通道线索，但没有阈值或实测效果；缓存、窄查询、低速和多源轴必须继续 `defer`，直到出现同案痕迹对照或可重复测量。 English: First-party incident reporting establishes adversarial domain and forest trust queries but does not join commands, directory requests, returned edges, cache hits, alert outcomes, and successor paths in one event. The tenant branch has Microsoft policy, permission, and logging documentation but no first-party case of an adversary reading partner configurations. Fixed ATT&CK AN0016 supplies channel clues without thresholds or measured effectiveness. Cached, scoped, low-rate, and distributed axes must remain deferred until a same-incident trace comparison or repeatable measurement becomes available.

**子级双语核心字段状态：** `proposed_subtechniques=[]`。没有任何轴具备足以安全书写为正式 NJS 的名称、summary、定义、匿迹特性、威胁模型、机理与独立防御引用；AX-02 至 AX-05 的双语名称只是研究标签，不得序列化为未编号子技术。

## 6. 可实施防御候选：DET → NJA 与 MIT

### 6.1 Detection Strategy

**`D07-03-T1482-DET-TRUST-GRAPH`（建议 `create`）— 身份信任拓扑读取归属与后继关联 / Attribution and Successor Correlation for Identity Trust-Topology Reads。** 目标是在域/林和租户观察面识别取得信任 partner、direction、type、attributes 或 reachability 的查询，把主体、来源、查询语义和成功结果同批准的健康、迁移与治理任务比较，并将后继认证或横向移动保持为独立的优先级上下文。域为 `enterprise`；未来 `detects_refs` 只指向新父级临时对象解析后的 NJT。

固定 ATT&CK DET0007/AN0016 可作为目标和通道线索，但 Niji Strategy 不能直接复刻其一行描述。建议两个 NJA 分担 AD 与 tenant 数据面；两者共享检测目标，逻辑、字段、误报和盲区不同。

### 6.2 `D07-03-T1482-NJA-AD`：域/林信任查询语义与主体谱系

**名称：** 域/林信任查询语义与主体谱系 / Domain and Forest Trust-Query Semantics and Principal Lineage。

**Logic zh：** 先从进程和 PowerShell 记录规范化明确的信任枚举语义，例如 `nltest` 的 trust 参数、`Get-ADTrust`、`GetAllTrustRelationships` 以及针对 `objectClass=trustedDomain` 或 trust partner/direction/type/attributes 的查询。再从 `IdentityQueryEvents` 提取 query、target、protocol、application 与账户身份，按账户 SID/UPN、主机、应用、来源和时间与进程谱系联结；目标部署若验证了 4662 对 trusted-domain 对象的读取审计，可作为对象级补充，1644 仅用于满足其记录阈值的 LDAP 查询。以主体—来源—会话为单位在初始 30 分钟窗口构建所查询的 partner/范围图，并与至少 14 日的 AD 健康、迁移、IAM、备份和响应基线比较。后续 Kerberos、远程登录或横向移动只提高优先级，不作为确认 discovery 的必需条件。30 分钟和 14 日均为需本地回放校准的工程起点。

**Logic en:** Normalize explicit trust-enumeration semantics from process and PowerShell records, including trust parameters to `nltest`, `Get-ADTrust`, `GetAllTrustRelationships`, and queries for `objectClass=trustedDomain` or trust partner, direction, type, or attributes. Extract query, target, protocol, application, and account identity from `IdentityQueryEvents`, then join them to process lineage by account SID or UPN, host, application, origin, and time. Where the deployment has validated 4662 read auditing for trusted-domain objects, use it as object-level support; use 1644 only for LDAP queries that meet its configured recording thresholds. Build the queried partner and scope graph per principal, origin, and session over an initial 30-minute window and compare it with at least 14 days of AD health, migration, IAM, backup, and response baselines. Later Kerberos, remote-logon, or lateral-movement outcomes raise priority but are not required to establish discovery. Both windows are engineering starting points requiring local replay calibration.

**Data requirements：**

| `source_type` | 通道 | 必需字段 |
|---|---|---|
| `endpoint-process-lineage` | Sysmon Event 1、Security 4688 或经验证 EDR | `timestamp, host_id, user_or_sid, process_guid_or_start_key, image, command_line, parent_guid_or_parent_start_key, signer, hash` |
| `powershell-script-block` | PowerShell Operational 4104 或等效内容遥测 | `timestamp, host_id, user_or_sid, process_id_or_runspace, script_block_id, script_text_or_hash, path` |
| `identity-directory-query` | Defender XDR `IdentityQueryEvents` | `Timestamp, ActionType, Application, QueryType, QueryTarget, Query, Protocol, AccountName, AccountDomain, AccountUpn, AccountSid, AccountObjectId`；目标租户可用时再加入已验证的设备、IP 与 report 字段 |
| `directory-object-read` | 经 SACL 与字段回放验证的 Security 4662；可选 | `timestamp, dc, subject_sid, object_name_or_dn, object_type, access_mask, properties, result_or_event_record_id` |
| `ldap-diagnostic-query` | Directory Service 1644；只作补充 | `timestamp, dc, client_identity_or_ip_when_available, search_base, filter, attributes, visited_count, returned_count, duration` |
| `approved-trust-reader-register` | AD 健康/迁移/IAM/响应任务台账 | `principal, source_host, application_or_script_hash, expected_query_scope, schedule, ticket, owner, expiry` |

**Observables：** 非信任管理主体或非管理源运行 trust 枚举；新父进程/脚本对 `trustedDomain` 或 trust 属性发起查询；同一会话从直接关系扩展到 all-trusts/forest；服务账号从新主机或新 application 发起信任图读取；查询后出现独立的跨域认证结果。模块加载和进程访问只能作弱上下文，不能声称看见了具体 API 调用。

**False positives：** AD 健康评估、域/林迁移、并购整合、身份治理、目录同步、权限审查、故障排查、授权红队和事件响应。**Blind spots：** 内存内 API 没有参数遥测；非 DC 缓存可减少新目录请求；未部署 MDI/IdentityQueryEvents；4662 SACL 未配置或事件量过高；1644 不记录普通高效查询；命令行截断、脚本混淆和合法管理身份被盗。**Tuning：** 例外必须绑定主体、来源主机、脚本/应用、查询 scope、工单和有效期；不得按 Microsoft 签名、`nltest.exe`、PowerShell 或管理员组永久放行。先以 trust 对象和新主体/来源做评分，再以 `/all_trusts`、范围扩张和后继结果加权。

### 6.3 `D07-03-T1482-NJA-TENANT`：跨租户 partner-policy 读取归属

**名称：** 跨租户 Partner Policy 读取归属 / Cross-Tenant Partner-Policy Read Attribution。

**Logic zh：** 在已启用 Microsoft Graph activity logs 的租户中，筛选对 `/policies/crossTenantAccessPolicy/default`、`/partners` 及其 `$select/$expand` 变体的成功或失败 GET；按 `UserId/ServicePrincipalId/AppId + SessionId/UniqueTokenId + IPAddress/DeviceId + TimeGenerated` 归一化会话，并保留 Roles、Scopes、UserAgent、RequestUri、状态和响应字节数。与获准的 Security Reader、Global Reader、身份治理、迁移和 Teams/B2B 管理任务台账比较；新 app、非管理来源、异常 token、首次读取或短窗遍历多个 partner 配置提高优先级。CrossTenantAccessSettings 审计日志用于关联策略变更，不能替代 read 请求日志。初始会话窗口 30 分钟、主体和 app 基线 30 日，均需按租户管理周期校准。

**Logic en:** In tenants where Microsoft Graph activity logs are enabled, select successful and failed GET requests to `/policies/crossTenantAccessPolicy/default`, `/partners`, and their `$select` or `$expand` variants. Normalize sessions by `UserId` or `ServicePrincipalId` or `AppId`, `SessionId` or `UniqueTokenId`, `IPAddress` or `DeviceId`, and `TimeGenerated`, preserving roles, scopes, user agent, request URI, status, and response size. Compare them with approved Security Reader, Global Reader, identity-governance, migration, and Teams or B2B administration records. A new app, unmanaged origin, anomalous token, first-seen read, or traversal of multiple partner configurations raises priority. CrossTenantAccessSettings audit logs correlate policy changes but do not substitute for read-request logs. Use an initial 30-minute session and 30-day principal/app baseline, calibrated to the tenant's administration cycle.

**Data requirements：** `microsoft-graph-activity` 通道需 `TimeGenerated,AadTenantId,RequestMethod,RequestUri,ResponseStatusCode,ResponseSizeBytes,AppId,ServicePrincipalId,UserId,IPAddress,DeviceId,UserAgent,Roles,Scopes,SessionId,UniqueTokenId,SignInActivityId,RequestId,OperationId`；`entra-signin-context` 可用时需 `timestamp,user_or_service_principal,app_id,session_id,ip,device_id,conditional_access_status,risk,authentication_result`；批准读取台账需 `principal_or_app,role_or_scope,management_origin,expected_resource_path,schedule,ticket,owner,expiry`。

**False positives：** Microsoft Entra 管理中心、跨租户访问评审、并购迁移、多租户组织治理、Teams shared channels、B2B 支持、安全审计和授权自动化。**Blind spots：** Graph activity logs 未启用、许可/保留不足、Microsoft 后台应用噪声、响应内容不在日志、令牌在批准 app 中被滥用、攻击者读取先前导出的配置副本。**Tuning：** 按 principal/app、role/scope、管理网络/设备、resource path 和工单建立到期基线；保留首次来源、scope 提升和异常 session，即使 app 在批准清单中。没有该日志时 tenant 分支必须标为 unavailable，不能以策略变更审计推断读取。

### 6.4 Mitigation

**`D07-03-T1482-MIT-TRUST-GOVERNANCE`（建议 `create`）— 身份信任拓扑最小化与读取问责 / Identity Trust-Topology Minimization and Read Accountability。**

**Description zh：** 维护域、林和租户 partner 的权威信任清单，记录方向、类型、属性、业务 owner、依赖、批准和到期；移除已无业务用途的信任或 partner-specific 配置，并把信任读取任务限定在受管身份、管理主机、应用和窗口。域侧启用并验证进程、PowerShell、目录查询及必要的定向对象审计；租户侧按最小角色和权限授予 `Policy.Read.All` 等读取能力，使用短期/JIT 管理和受管设备，并启用 Graph activity logs。网络分段和敏感域隔离降低已发现边的后继可用性，但不能代替读取问责。

**Description en:** Maintain an authoritative inventory of domain, forest, and tenant partners with direction, type, attributes, business owner, dependency, approval, and expiry. Remove trusts or partner-specific configurations with no remaining business purpose, and confine trust-read work to managed identities, administration hosts, applications, and windows. On the domain side, enable and validate process, PowerShell, directory-query, and necessary targeted object auditing. On the tenant side, grant policy-read capabilities such as `Policy.Read.All` through least roles and permissions, short-lived or JIT administration, and managed devices, and enable Microsoft Graph activity logs. Network segmentation and sensitive-domain isolation reduce the later utility of a discovered edge but do not replace read accountability.

**Measures：**

1. `authoritative-trust-inventory-and-retirement` / 权威信任清单与退役：定期核对 domain/forest trust 和 tenant partner 的方向、类型、属性、依赖、owner 与到期，删除无主、过期或重复关系，并保留变更与回滚记录。 / Reconcile direction, type, attributes, dependencies, owner, and expiry for domain or forest trusts and tenant partners; retire orphaned, expired, or duplicate relationships and preserve change and rollback records.
2. `least-trust-read-authority` / 信任读取最小权限：租户侧限制 `Policy.Read.All`、相关 reader/admin 角色和应用同意，采用 PIM/JIT、短期会话和受管设备。域侧承认认证用户可能获得基础信任数据，不以未经验证的 ACL 收紧承诺全面阻止枚举，而把高价值管理身份、远程入口和后继能力最小化。 / Restrict tenant `Policy.Read.All`, related reader or admin roles, and app consent through PIM or JIT, short sessions, and managed devices. On the domain side, recognize that authenticated users may obtain basic trust data; do not promise complete prevention through unvalidated ACL tightening, and instead minimize high-value administration identities, remote entry, and successor capabilities.
3. `managed-query-path-and-audit-validation` / 受管查询路径与审计验证：登记健康、迁移、IAM 与响应任务的主体、主机、脚本/app、scope 和时间；用受控 trust query 定期验证 endpoint、PowerShell、IdentityQueryEvents、4662/1644（适用时）和 Graph request 日志的字段、路由及保留。 / Register principal, host, script or app, scope, and time for health, migration, IAM, and response work; regularly issue controlled trust queries to validate fields, routing, and retention across endpoint, PowerShell, IdentityQueryEvents, applicable 4662 or 1644, and Graph request logs.
4. `discovered-path-utility-reduction` / 已发现路径效用收缩：对敏感域和跨租户应用采用分段、最小资源授权和明确 inbound/outbound 范围，使“知道信任边”不自动转化为可用横向路径。 / Use segmentation, minimum resource authorization, and explicit inbound or outbound scope for sensitive domains and cross-tenant applications so knowledge of a trust edge does not automatically become a usable lateral path.

**未来父级 Application：** `use` zh：对身份信任边界发现，压缩无业务必要的信任边与 tenant partner 配置，把读取权限和任务固定到有 owner、来源、scope、时间和审计验证的管理路径，并对敏感边限制后继认证与资源范围。`expected_effect` zh：攻击者可获知的有效路径减少，非批准读取更容易与健康/迁移任务区分，已发现边也更难直接转化为横向移动。`limitations` zh：认证域用户仍可能取得基础信任数据，合法工具和授权 reader 可被盗用；删除或限制信任可能中断业务、迁移和协作；缓存或已导出副本不会自动撤回，Graph/MDI/对象审计有许可、成本、隐私和事件量要求。 `use` en: For Identity Trust Boundary Discovery, reduce trusts and tenant-partner configurations without a business need, bind read authority and jobs to managed paths with an owner, origin, scope, time, and validated audit, and limit successor authentication and resource scope across sensitive edges. `expected_effect` en: The set of useful paths exposed to an adversary shrinks, unauthorized reads become easier to distinguish from health or migration work, and a discovered edge is less likely to become immediate lateral movement. `limitations` en: Authenticated domain users may still obtain basic trust data, and legitimate tools or entitled readers can be compromised. Removing or restricting trust can disrupt business, migration, and collaboration; cached or exported copies are not retracted, and Graph, MDI, or object auditing carries licensing, cost, privacy, and event-volume constraints.

## 7. 共享库决议

| 对象 | 决议 | 理由与限制 |
|---|---|---|
| 固定 ATT&CK 19.1 基线 REF | `reuse/extend` 优先 | 若现有宽基线对象已以同一版本化 URL 标识，只扩 locator/notes；不得复制同一 canonical URL。T1482 专页若不存在可 `create` |
| `D07-03-T1482-REF-STORM0501/CISA-IRAN/CISA-AKIRA/MS-DSENUM/MS-TRUSTSTRUCT/MS-NLTEST/MS-IDENTITYQUERY/MS-XTENANT/MS-GRAPHLOG/MS-1644` | `create`，主 Agent 做最终 URL 查重 | 当前只读 catalog/文本查询没有发现 T1482、trustedDomain、IdentityQueryEvents 或 cross-tenant policy 的精确共享对象；每条只承担其实际证据层级 |
| `D07-03-T1482-CLM-PARENT/TENANT-SCOPE/DUAL-USE/BOUNDARY/ZERO-NJS` | `create` | 五项命题的主体和置信度不同；tenant scope 不能并入高置信域/林恶意案例 |
| `D07-03-T1482-CASE-STORM0501/CISA-IRAN/CISA-AKIRA` | `create`，保持三个事件身份 | 主体、时间范围、调查机构与中心事实不同；不得合并为“通用 nltest 案例”。跨租户恶意读取 Case `defer` |
| `DET-000140` / `NJA-000145` / `MIT-000129`（账户既存身份视图） | `split/create`，不 extend 为 T1482 | 其目标是账户/地址簿身份集合和端点副本读取；T1482 的对象、AD/Graph 通道、正常基线和控制动作不同。缓存轴的概念相似不足以复用 NJS 或防御身份 |
| `MIT-000052`（remote identity trust controls） | `reuse` 作边界，**不新增 T1482 application** | 该对象控制 trusted relationship entry 和跨租户委托进入，面向入口而非拓扑 read；可说明后继风险，不能替代 T1482 read governance |
| `MIT-000098` 与 `NJT-0100`（authoritative trust/policy mutation） | `reuse` 作写入边界，**不 extend coverage** | 对象是 trust/policy 变更、版本和恢复；T1482 是只读发现。其日志可被新 NJA 关联为后继，但不能冒充 read 检测 |
| `NJT-0106` 及 `NJS-0106-001/-002` | `reuse` 作条件门控边界，**不复用为 T1482 子项** | 查询信任事实不等于环境检查规避；只有有证据的“按信任存在与否改变行为”才另行关联 |
| `D07-03-T1482-DET-TRUST-GRAPH/NJA-AD/NJA-TENANT/MIT-TRUST-GOVERNANCE` | `create` | 当前共享库没有同一目标、数据合同和控制概念；AD 与 tenant NJA 数据平面实质不同但可归于同一 DET |
| AX-02 至 AX-05 对应 Claim、NJS、DET 或 MIT application | `defer` | 缺恶意选择、同案痕迹对照、实测防守效果和正式 target_ref；不得预留语义 ID |
| T1482 → 票据滥用/横向移动关系 | `defer` 到父级分配且 Case 关系收敛后再 `create` | 一手材料支持 discovery 后存在后继机会，但关系源端尚无正式 NJT，且不同事件的后继强度不一致 |

## 8. 交接门禁自检

- `recommendation.decision: adapt`；整体 `confidence: medium`；域/林父行为 high，tenant extension medium；`original_attack_subtechniques_imported: false`。
- 固定 Enterprise ATT&CK 19.1 子项 `0 / []`；正式 NJS `0`；taxonomy `deferred`。
- 已检查 7 个轴并给出 `formal-parent-core / defer / reject`；所有未证轴明确 `defer`，没有按产品、平台、API、工具、资源字段或信任类型拆 NJS。
- 父级双语字段覆盖 summary、定义、匿迹特性、范围、场景、攻击者模型、防守方模型、机理、taxonomy 与限制；无未编号子项正文。
- 父行为一手证据由 Microsoft Threat Intelligence 与 CISA 事件材料支撑；Microsoft 协议/API/日志文档只用于架构、字段、合法反例和检测能力，不升级为恶意案例。
- DET 定义具体目标；AD 与 tenant 两个 NJA 提供实际通道、字段、关联窗口与键、误报、盲区和调优；MIT 提供可实施 Measure 及父级 use/effect/limitations。
- 账户、组、GPO、主机、信任写入、票据滥用、横向移动和 NJT-0106 环境检查均已划界；AD 健康、迁移、身份治理和跨租户协作已作为强正常反例。
- 已给出 `reuse/extend/create/split/defer` 共享库决议；未分配正式 ID，未修改正式矩阵或共享库。
- 主 Agent 集成前仍须执行 canonical URL/事件身份/语义指纹最终查重、人工双语等价审查、编号、`make quality`、Bundle 与中英文 Web QA。
