# BATCH-TA0112-003 集中策略与云层级边界

基线锁定为 enterprise-attack 19.1。本批总体程序范围是 TA0112 固定的 18 个父候选；当前交付仅包含 T1484 Domain or Tenant Policy Modification 和 T1666 Modify Cloud Resource Hierarchy。前序 BATCH-TA0112-002 的准入、证据、taxonomy、双语正文、防御、质量、Bundle、Web 与 API 门禁已通过，无未解释 reserved ID。本批两项直接对象相邻但不相同：前者是既有权威策略版本的防御效果，后者是资源在云层级中的位置及其继承控制覆盖。为了逐候选保持独立研究，分别设置 handoff、证据决议、原生子项和防御对象；任何一项未完成都不进入 BATCH-TA0112-004 正式写入。候选数不保证 NJT/NJS 数。

T1484 必须与已存在的 NJT-0100 划清结果边界。NJT-0100 仅在消费者采用策略版本后向攻击主体增加实际资源权限时成立；纯关闭 Defender、审计或响应控制而没有正向权限差属于 TA0112。GPO 和 trust 是 ATT&CK 的两个实现子项，只作研究上下文，不作为 Niji 子项。必须复核集中发布、作用域选择性和用后回退三个候选轴，只有结论级证据显示稳定痕迹差异时才正式化。微软 2026 GPO 勒索事件被阻断，支持攻击意图与控制面扇出，不得虚构成功防御关闭。

T1666 的直接对象是云账户、订阅、项目或组织单元的父子关系及由此决定的继承策略、集中日志和检测覆盖，而不是改写策略内容。无 ATT&CK 子项仍需开放搜索：已有资源迁离受管层级、在低覆盖位置新建资源、跨租户转移以及仅账单/组织重排分别审查。需要证明迁移或新建后的控制覆盖相对批准基线实际减少；仅调用 LeaveOrganization、CreateAccount 或创建订阅不自动证明失明。与 T1484 的边界以“policy version 改变还是 resource ancestry 改变”为准，与 T1578 云计算对象生命周期保持独立。

共享库先按官方 URL、ATT&CK ID 与语义指纹查重。T1484 可复用 REF-000338、REF-000341、REF-000342、REF-000344 和 CASE-000126，但必须保留“被阻断”限制。T1666 需核对 ATT&CK 父页、AWS Organizations LeaveOrganization、CloudTrail 组织 trail、Control Tower enrollment、Google Cloud move project 与 Microsoft Peach Sandstorm 事件。现有 DET-000097/NJA-000077/MIT-000098 服务于提权结果，不得只替换术语后复用为防御削弱；策略内容差分与层级 ancestry 差分必须各有可实施数据源。

正式写作按 NJT-0001 的字段责任逐候选审查，父子双语自然段分别覆盖定义、匿迹特性、范围、场景、攻防观察、机理、证据限制；不得把 ATT&CK 子项、平台、产品、OU 名称或 API 名称机械转成 NJS。临时研究文件仅放在本批目录；脚本只用于 ID、机械序列化、校验和构建。人工领域评审前均保持 review。
