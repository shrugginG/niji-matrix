# BATCH-TA0007-002 五候选准入与跨技术收敛

本记录在阅读五份独立 sub-agent 交接后由主 Agent 作出，先于 NJT/NJS 及语义共享库 ID 分配。固定依据是本地 ATT&CK Enterprise 19.1 `techniques` 工作表中属于 TA0007 的父行；五项均无 ATT&CK 子技术，但每项已开放搜索多个 Niji 匿迹变量。此处的准入是批次结论，不能把研究者建议直接当正式矩阵事实。

| 候选 | 主审准入 | 直接信息对象 | Niji 分类收敛 |
|---|---|---|---|
| T1217 Browser Information Discovery | **adapt，medium** | 已保留的浏览站点、历史与配置上下文 | 父级限于从已有浏览记录恢复入口。CISA 书签枚举和 Volexity ICONICSTEALER 历史提取是直接恶意事实；“本次无相应新导航”是架构推断。同步副本、时间谓词、分批重读及浏览器内扩展路径均缺独立恶意/防守证据；正式 NJS 0，taxonomy `deferred`。 |
| T1580 Cloud Infrastructure Discovery | **retain，medium** | IaaS 资源实体、配置与关系图 | Expel 证明被盗 IAM 键读取桶、实例和数据库并有后继动作。有效身份下的正常只读表象可归 `NM-FD`，但没有实测漏报。聚合索引/state 替代、跨身份/区域拆分、条件查询和分页不正式化；NJS 0，taxonomy `deferred`。 |
| T1538 Cloud Service Dashboard | **exclude，medium-high** | GUI 控制台路径，可显示相邻对象的信息 | GUI 是信息获取路径，未证实相对相同资源、服务或对象查询具有独立稳定的匿迹变量和专属防御。AWS ConsoleLogin 与服务请求可能保留，GCP Data Access 取决于启用；排除不等于否认控制台恶意使用。无 NJT/NJS，也不为排除项创建专属 DET/NJA/MIT。 |
| T1526 Cloud Service Discovery | **adapt，medium** | 服务能力、启用/运行状态与安全/日志覆盖 | 收紧宽泛 ATT&CK 实例示例，与 T1580 具体资源图区分。Storm-0501 报告证明真实攻击者测绘防护状态；GCP Service Usage 的特定读取无审计是技术事实，但并未证明该演员选用它规避。父级 `NM-BT` 只描述有条件观察面，置信度校准为 hypothesis/medium；NJS 0，taxonomy `deferred`。 |
| T1619 Cloud Storage Object Discovery | **retain，medium** | 已知容器内部对象键、前缀与清单元数据 | Unit 42 证明攻击者使用存储浏览工具和对象访问；其 ListObjects 调用来自单独受控实验，受害环境没有对象数据日志，不能合并为同案实测。授权只读清单的正常作业表象可条件性归 `NM-FD`；清单报告转读、prefix 分段和多身份节奏缺恶意对照，NJS 0，taxonomy `deferred`。 |

## 跨候选归属规则

T1217 的历史 URL/书签是浏览上下文；已存在账户标识集合由 NJT-0131 主持，当前应用窗口由 NJT-0132 主持，密码、Cookie、令牌和网页正文读取另按直接对象判定。浏览器记录中的偶然用户名不改变主归属。

云侧按本次想回答的问题划分：T1526 问“哪项服务或防护能力已启用/覆盖”；T1580 问“有哪些实例、桶、快照、数据库、网络及关系”；T1619 问“已知桶内有哪些对象键/前缀”。后继下载对象正文、修改防护或创建资源分别归其后续技术。T1538 的 GUI 可作为三者的路径上下文，不能因界面不同自动复制父技术。混合响应只在两个实际目的均有证据时多标签，不按返回字段机械多归属。

四个获准父项分别有不同遥测与防御对象：浏览器端点文件读及客户端基线、IaaS 跨服务资源管理读和后继变更、服务/防护状态查询及审计覆盖、存储对象数据面列表与报告读取。不得用同一 Analytic 或 MIT 文本替换名称。`REF-000379` 可支撑配置过 SACL 的 4663；`REF-000366` 可支撑进程/网络事件边界；`REF-000513` 是 S3 文档同 URL，应先延展精确 locator 再按结论复用。已有 DET-000118 针对低覆盖区域的资源创建，不直接复用为 T1580 的资源读取策略；DET-000105 管原始卷绕过对象视图，与 T1619 正常云列表不同。

## 证据限制与机理门槛

AWS 当前 S3 CloudTrail 官方表在普通 `AWS::S3::Object` 行列出 `ListObjects`，未列 `ListObjectsV2`；V2 在 Express、Access Point、Outposts 等行出现。不能据遗漏断言普通桶 V2 必定无记录；目标环境需用受控请求、数据事件选择器或 server access log 核实。Azure Blob 数据面需配置 StorageBlobLogs 导出，GCP 列对象属于需显式启用的 Data Access `DATA_READ`；云“无日志”常是配置或接口特定盲区，不是四种父行为共有的内在属性。

所有研究中的工具能力、正常工作流、架构推断和在野事件分开处理。正式机理只能写行为设计→痕迹变化→防守观察→匿迹效果，且在限制中指出尚无攻击者主观避审计指令或实测检测率。四项正式父技术不能因无子项而缩写双语正文；每项仍须有独立 DET、可实施 NJA、逐目标 MIT、原子 Claim 与适当 Case。T1538 只保留有证据的排除决策。所有对象留 `draft` 直到质量、Bundle、Web 和双语页面过门禁，随后才升 `review` 待人工领域评审。
