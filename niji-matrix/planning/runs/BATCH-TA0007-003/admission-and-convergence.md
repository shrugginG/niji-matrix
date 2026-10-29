# BATCH-TA0007-003 五候选准入与跨技术收敛

本记录由主 Agent 在五份独立 sub-agent 研究交接全部可审阅后作出，先于新 NJT/NJS 与语义共享库 ID 分配。固定依据为 ATT&CK Enterprise 19.1；五项父候选均无 ATT&CK 子技术，但每项完成了开放式 Niji 变量搜索。

| 候选 | 主审准入 | 正式集成 | 子技术收敛 |
|---|---|---|---|
| T1613 Container and Resource Discovery | **retain，medium** | 新建父级 NJT，直接对象为容器集群、节点、命名空间、工作负载、镜像和部署资源图 | Kubernetes/Docker 接口、namespace/selector、分页/watch、节点局部视图和多来源节奏均缺独立匿迹因果；新增 NJS 0，taxonomy `deferred` |
| T1622 Debugger Evasion | **retain，high** | 跨战术复用 `NJT-0106`、`NJS-0106-001/-002`、DET/NJA/MIT；仅扩展 NJT tactic_refs 加 TA0007，并建立 TA0007 独立 decision | 既有两项 NJS 已按状态门控与调试通道饱和划分；线程隐藏/拒绝附加仍 deferred，新增 NJS 0 |
| T1652 Device Driver Discovery | **adapt，medium** | 新建父级 NJT，明确驱动包、安装、加载/活动、地址和设备能力的结果语义 | 接口、权限/版本、驱动类别及发现目的不能形成稳定兄弟边界；新增 NJS 0，taxonomy `deferred` |
| T1482 Domain Trust Discovery | **adapt，medium** | 新建“身份信任拓扑发现”父级，域/林为高置信，跨租户 partner policy 为能力支持的中等置信扩展 | 缓存、限域查询、多源拼接和属性投影缺同案痕迹与防御差；新增 NJS 0，taxonomy `deferred` |
| T1083 File and Directory Discovery | **retain，medium** | 新建父级 NJT，直接对象为主机或网络文件系统路径、名称、层级、存在性与列表属性 | 索引化查询、窄谓词、时间稀释和多来源分散缺结论级对照；新增 NJS 0，taxonomy `deferred` |

## 统一边界

T1613 只管容器资源图，容器 exec 与创建分别保留给 T1609/T1610；IaaS 资源图归 NJT-0139。T1652 只管驱动事实，后继 BYOVD、漏洞利用、驱动加载和基于驱动结果的 T1497 行为另记。T1482 只到信任边 partner/direction/type/attributes；信任修改、票据滥用、远程认证和横向移动是后继。T1083 只到文件系统命名空间事实；浏览记录解析归 NJT-0138，云对象 key 归 NJT-0141，正文读取、打包与外传归 Collection/Exfiltration。

T1622 的 Discovery 目的和 Stealth 结果是同一状态检查、结果及分支事务：检查得到“是否被调试”的环境事实，随后同一结果门控退出、诱饵或载荷释放。战术不同不足以 split。NJT-0106 保留原始 decision_ref，TA0007 的新决策从战术侧反向指向同一 NJT，符合已有 NJT-0078 跨战术复用模式。

## 证据与防御结论

四个新父级分别需要独立数据模型：T1613 使用 Kubernetes audit 与经验证的 Docker 请求/进程通道；T1652 使用原生工具、注册表或经验证 API telemetry，并区分查询成功与有效结果；T1482 使用 AD/LDAP/IdentityQueryEvents 与 Graph activity 的不同分支；T1083 使用 Windows 本地/SMB 命名空间事件与 POSIX 进程/audit 分支。它们不得共享换名 Analytic。

四个新父级的 stealth mechanism 均需校准：T1613 的合法资源盘点外观为 low-to-medium NM-FD；T1652、T1482、T1083 的合法管理/枚举外观为 medium NM-FD。事件证明恶意使用，不证明固定漏报率或主观避审动机。所有 deferred 轴只保留在规划层，不预留 NJS、Claim 或 MIT Application。

所有新对象保持 draft，直至共享库查重、ID 同步、Schema/规划、reader-prose、Bundle、全套 Web 测试及中英文实际渲染通过；随后升 review 等待人工领域评审。
