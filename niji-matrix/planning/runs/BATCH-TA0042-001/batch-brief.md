# BATCH-TA0042-001 研究与收敛约束

## 基线与范围

- 战术：TA0042 Resource Development / 攻击准备
- ATT&CK domain：enterprise-attack
- ATT&CK version：19.1
- 候选：T1650、T1583、T1586、T1584、T1587、T1585、T1683、T1588、T1608
- 本批次覆盖固定基线中的全部 9 个父技术；九个候选必须逐项决策，但不保证产生九个正式 Niji 技术。

## 父技术边界

| 候选 | 直接信息或行为对象 | 与兄弟候选和既有技术的边界 |
|---|---|---|
| T1650 | 已经存在的目标系统或网络访问权、会话、入口或经纪交付 | 不等同于购买工具/恶意软件的 T1588；不把获取后的登录、横移或持久化纳入本父行为 |
| T1583 | 通过购买、租用、注册、试用或合法申请取得的行动基础设施 | 与 T1584 的区别是资源取得方式不依赖攻陷第三方；账户创建本身归 T1585 |
| T1586 | 被接管的既有社交、邮件、云或服务账户 | 与 T1585 的区别是继承真实账户历史、关系与信誉；实际账户攻陷步骤属于相应访问技术，TA0042 只描述其被准备为后续资源 |
| T1584 | 被接管的第三方域名、DNS、服务器、云资源、Web 服务或网络设备 | 与 T1583 的区别是资源所有权/控制权来自攻陷；与 T1586 按主要受控对象区分账户和基础设施 |
| T1587 | 攻击者内部研发的恶意软件、利用、协议、证书或其他能力 | 与 T1588 的区别是内部开发而非外部取得；一般内容生成归 T1683；实际执行不在本父行为 |
| T1585 | 新创建并培育的行动账户、人物身份或服务身份 | 与 T1586 的区别是不继承真实账户历史；T1593/NJS-0024 只覆盖用于研究的假名账户，本候选覆盖资源建立与培育 |
| T1683 | 为身份、欺骗、社交工程、诈骗或影响行动生成的文字、音频、图像、视频和叙事 | 与 T1587 的能力代码边界以输出直接用途区分；向目标发送/展示内容属于下游行为，生成本身在此 |
| T1588 | 从外部购买、窃取、下载、许可或取得的恶意软件、工具、利用、证书、漏洞信息或 AI 能力 | 与 T1587 的区别是外部来源；与 T1650 的区别是取得能力而非具体目标访问权 |
| T1608 | 把已开发/取得的能力上传、安装、配置或布置到受控基础设施以供后续取用 | 与 T1587/T1588 的区别是部署状态转换；与下游投递、执行、C2 或钓鱼按直接行为边界区分 |

## 子技术规则

- 不读取或导入 ATT&CK 原子技术作为 Niji 子技术分类。
- 子技术必须由资源匿迹实现变量区分，不能按域名/VPS/服务器、社交/邮件/云账户、恶意软件/利用/证书、文字/音视频等 ATT&CK 媒介或资源类型直接拆分。
- 每项候选必须证明“资源准备设计 → 可见痕迹变化 → 防守观测影响 → 后续匿迹效果”，仅拥有资源或使用常见服务不自动构成匿迹。
- 区分资源准备阶段与后续使用阶段；后续使用可以作为效果或关系证据，但不能反向吞并父行为。
- 对合法云、Web、广告或 AI 服务，必须分别说明提供方可见性、滥用日志和受害者侧可见性。
- 对被盗账户/基础设施，必须区分继承信誉与真实主体受害痕迹；“可信”不等于不可检测。
- 对自研/外取能力，必须说明供应链、构建、签名、样本谱系或重用痕迹如何影响归因和检测。
- Sub-agent 不分配正式 ID，不修改 matrix、references、claims、cases、detections、mitigations 或 relationships。

## 共享库线索

| 稳定键 | 类型 | 可能复用的候选 | 当前决议 |
|---|---|---|---|
| ATT&CK:T1650/T1583/T1586/T1584/T1587/T1585/T1683/T1588/T1608 | REF | 各自父候选 | create official parent references centrally after admission confirmation |
| CISA:AA23-320A / REF-000031 | REF/CASE | T1650、T1586、T1588 | confirmed reuse candidate; exact behavior scope required |
| Mandiant UNC3944 / REF-000032 | REF/CASE | T1650、T1586 | confirmed reuse candidate |
| Microsoft/OpenAI threat AI / REF-000041 | REF | T1587、T1683、T1588 | reuse candidate only where the documented behavior matches |
| GTIG AI threat tracker / REF-000043 | REF | T1587、T1683、T1588 | reuse candidate; separate generation from downstream delivery |
| CASE-000008 Scattered Spider identity enrichment | CASE | T1650、T1586 | extension candidate only if the same campaign facts are used |
| MIT-000013 sender domain authentication | MIT | T1585、T1586、T1683 | reuse candidate for downstream trust abuse; not sufficient alone |
| MIT-000017 indicator-independent detection | MIT | T1584、T1587、T1588、T1608 | reuse candidate where lineage preservation is unchanged |

## 并行安排

- 第一轮：T1650、T1583、T1586
- 第二轮：T1584、T1587、T1585
- 第三轮：T1683、T1588、T1608
- 每个工作项暂存路径：`planning/runs/BATCH-TA0042-001/<ATTACK-ID>-handoff.yaml`
- 临时键前缀：`B42R1-<ATTACK-ID>`

## 收敛注意事项

- 重点检查“来源/取得方式”是否只是资源分类轴；只有产生独立可观察痕迹和防守控制边界时才保留子技术。
- 重点检查 T1583 与 T1584 的基础设施信誉、归因分离和服务噪声重叠，避免分别复制同一云/代理/托管匿迹模式。
- 重点检查 T1585 与 T1586 的人物身份、账户历史、关系图和信任继承，按新建培育与接管继承区分。
- 重点检查 T1587、T1588、T1608 的代码谱系与供应链痕迹，按开发来源、取得来源和部署状态转换区分。
- 重点检查 T1683 的身份/内容拟态是否应成为独立资源技术，还是由下游 NJT-0007 等技术吸收；生成行为必须具备自身可防守边界。
- 重点检查 T1650 的经纪交付、历史会话和访问年龄是否形成不同于凭据获取/有效账户使用的资源匿迹因果链。
- 暂不把常见云服务、免费试用、加密货币付款、AI 生成或开源工具使用本身直接视为匿迹；证据不足者记录为 defer。
