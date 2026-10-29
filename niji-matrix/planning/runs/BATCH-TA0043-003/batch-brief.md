# BATCH-TA0043-003 研究与收敛约束

## 基线与范围

- 战术：TA0043 Reconnaissance / 目标侦查
- ATT&CK domain：enterprise-attack
- ATT&CK version：19.1
- 候选：T1593、T1594、T1596、T1597、T1681、T1682
- 本批次覆盖固定基线中尚未决策的全部父技术；批次完成不自动代表战术通过人工审查。

## 父技术边界

| 候选 | 直接信息或行为对象 | 与兄弟候选和既有技术的边界 |
|---|---|---|
| T1593 | 第三方公开网站、搜索引擎、社交平台和公开代码内容 | 受害者自有站点归 T1594；结构化技术观测归 T1596；信息内容按 NJT-0003 至 NJT-0006 归类时，以本候选的访问表面和匿迹实现为父技术边界 |
| T1594 | 由受害者控制或代表受害者运营的公开 Web 资产 | 第三方公开平台归 T1593；主动探测路径、目录或端点时与 NJT-0001 主动扫描区分；直接诱导表单响应时与 NJT-0007 区分 |
| T1596 | 第三方公开提供的结构化技术数据、索引和历史观测 | 一般 Web 内容归 T1593；付费或受限数据归 T1597；攻击者直接探测目标归 NJT-0001；目标网络信息内容可与 NJT-0005 建立关系但不复制分类 |
| T1597 | 需要付费、授权、私有访问或地下交易的封闭数据源 | 开放技术数据归 T1596；威胁厂商反馈若主要用于了解自身暴露或调整行动，优先归 T1681；非法取得数据源访问权属于前置行为 |
| T1681 | 威胁情报厂商、研究者或社区关于攻击者自身及同业活动的检测反馈 | 一般目标画像归 T1593/T1596/T1597；核心结果必须是感知防守可见性、公开归因或对手知识并据此支持调整 |
| T1682 | 公共 AI 服务对公开材料的聚合、推理、转换和生成 | 直接访问原始网站或数据库仍归相应搜索技术；本候选要求 AI 中介对侦查任务产生实质性综合、推断或生成作用；本地私有模型不在范围内 |

## 子技术规则

- 不读取或导入 ATT&CK 原子技术作为 Niji 子技术分类。
- 子技术按匿迹实现变量拆分，不按网站类型、数据库字段、供应商名称、AI 模型或媒介拆分。
- 公开、被动或第三方查询不自动构成匿迹；必须建立“行为设计 → 痕迹变化 → 防守观测影响 → 匿迹效果”的因果链。
- 对访问目标自有站点的行为，必须说明是普通浏览、请求节奏/来源变化，还是已越界成为主动扫描。
- 对威胁情报反馈，必须区分用于一般能力学习与用于评估自身暴露、改变可观测特征或规避检测的闭环。
- 对公共 AI 查询，必须同时讨论服务提供方可见性、提示词/账户日志和输出可靠性；不能把“使用 AI”本身视为隐蔽。
- Sub-agent 不分配正式 ID，不修改 matrix、references、claims、cases、detections、mitigations 或 relationships。

## 共享库线索

| 稳定键 | 类型 | 可能复用的候选 | 当前决议 |
|---|---|---|---|
| ATT&CK:T1593/T1594/T1596/T1597/T1681/T1682 | REF | 各自父候选 | create official parent references centrally after admission confirmation |
| CISA:AA24-038A / REF-000025 | REF/CASE | T1593、T1594 及既有 NJT-0006 | confirmed reuse candidate |
| RFC 9162 / REF-000036 | REF | T1596 | confirmed reuse candidate |
| RFC 9499 / REF-000037 | REF | T1596 | confirmed reuse candidate |
| RFC 9083 / REF-000038 | REF | T1596 | confirmed reuse candidate |
| OpenAI threat report / REF-000041 | REF | T1681、T1682 | confirmed reuse candidate; exact scope must be checked |
| MIT-000001 external exposure minimization | MIT | T1593、T1594、T1596、T1597 | extension candidate |
| DET-000012 external reconnaissance graph | DET | T1593、T1594、T1596、T1597 | extension candidate only if analytic logic remains unchanged |

## 并行安排

- 第一轮：T1593、T1594、T1596
- 第二轮：T1597、T1681、T1682
- 每个工作项暂存路径：`planning/runs/BATCH-TA0043-003/<ATTACK-ID>-handoff.yaml`
- 临时键前缀：`B43R3-<ATTACK-ID>`

## 收敛注意事项

- 重点检查“第三方查询表面”是否只是 NJT-0003 至 NJT-0006 的获取渠道；只有稳定、可独立防守的匿迹实现变量才保留为 Niji 子技术。
- 重点检查 T1596 的历史/代理观测与既有 NJS-0016 第三方观测的重叠；必要时建立 relationship 或复用 claim，而不复制子技术。
- 重点检查 T1597 与 T1681 在付费威胁情报中的重叠，按直接目的区分：目标数据采购 vs. 防守反馈感知。
- 重点检查 T1682 是否具有独立于查询对象的信息压缩、语义伪装、账户/会话隔离或输出污染风险。
- 暂不把无公开证据支持的“刻意选择缓存、匿名账户或提示词编码”直接写成已证实分类；可作为 hypothesis/defer 记录。
