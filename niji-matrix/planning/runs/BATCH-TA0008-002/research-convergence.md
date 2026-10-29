# BATCH-TA0008-002 五候选统一收敛

固定范围为 Enterprise ATT&CK 19.1，TA0008 九个父候选中的下一组五项。BATCH-TA0008-001 已通过全部机器、证据、双语和 Web 门禁。本文件记录主 Agent 收齐五份独立交接后的准入、分类、边界和共享库决议；ATT&CK 子项只留在规划层。

| 候选 | 准入 | 正式父项处理 | Niji 原生子项裁决 |
|---|---|---|---|
| T1080 Taint Shared Content | adapt，medium | 新建“共享对象污染后异机消费”父项，以共享对象受控改写、异机消费及首次攻击者结果为完成门。 | 2 项：既有对象内容或执行语义原位改变；共享导航入口目标绑定替身。DirSharePivot 为原作者客户取证与复现，按可证范围建立第二项；两项按对象语义与绑定关系，不按 Office/LNK 格式拆分。 |
| T1091 Replication Through Removable Media | retain，high | 跨 TA0001/TA0008 复用 NJT-0058 和现有两项 NJS；重写现有父子双语内容、校准机理与目标化防御。 | 新增 0；复用伪装式介质触发及自动播种两轴。TA0008 要求已控内部 A→同一介质→不同内部 B 接入并实际执行/可控结果。 |
| T1210 Exploitation of Remote Services | adapt，medium | 新建内网服务漏洞触发到异机可控结果父项，区分漏洞尝试、可能结果和确认结果。 | 0，taxonomy deferred。六项候选轴缺稳定可控匿迹变量或结论级证据；CVE、SMB/RDP 名称与漏洞扫描不是 NJS。 |
| T1534 Internal Spearphishing | adapt，high | 新建失陷内部身份→内部诱导消息→第二主体受控结果父项。 | 0，none-justified。Proofpoint 按主题归档警示回复的稳定默认视图遗漏变量已由 NJS-0111-001 拥有；可作为共现机理和案例，不能按 TA0008 场景重复子项。 |
| T1563 Remote Service Session Hijacking | adapt，medium | 新建接管已有认证远程传输或交互会话的父项。 | 2 项：既有认证 transport 上新增逻辑控制通道；已有交互会话的控制端重绑定（独占迁移或 shadow 并存共控为一个变量）。SSH 轴由 OpenSSH 规范与 USENIX 技术研究支持，缺野外 Case，保持 medium 并写限制；交互轴有 Mandiant MAZE 与 CrowdStrike 成功事件支持。 |

## 横向结果和兄弟边界

- T1080 的对象是已存在共享内容或导航绑定的恶意变化，必须有另一内部消费者。T1570 只负责独立文件到达；T1534 负责从内部主体发出的定向消息与收件者动作，不能把共享文档被打开自动算成发信。
- T1091 介质播种不等于从外网取得首个立足点；与 TA0001 共用父与子项，但需分别描述首次入口和内部 A→B 后续移动。现有 NJT-0058 及 NJS-0058-001/002 的模板化定义、威胁模型、机理和限制不满足 NJT-0001 深度，本批逐字段整改后才进入 review。
- T1210 的直接因果入口是目标服务漏洞，T1021 是新建合法服务会话，T1563 是接管既有认证传输/会话，T1550 是替代认证材料，T1570 是文件到达。利用成功与后来提权、执行或持久化可共现，但不可互为证据。
- T1534 的内部身份与消息可信度和 T1080 的共享对象完整性不同；反馈归档可由 NJT-0111 同时描述，却不能成为此处新的同义 NJS。
- T1563 两子项由控制对象区分：新 channel 仍在同一认证 transport 内，交互会话重绑定改变控制端。SSH agent forwarding 凭据滥用后新建连接、Matrix.org 事件和 UNC3886 新 SSH 流拦截不能被当作既有会话接管案例。

## 来源、案例与证据强度

- ESET 2020 Gamaredon 一个稳定 URL 同时支持 T1080 文档注入和 T1534 内部发信，分别建结论；其报告明言行动者偏重快速传播，不支持匿迹动机。
- ESET 2020 InvisiMole 白皮书 PDF 的 §5.2 支持 T1080 原有文件木马化，§5.1 支持 T1210 BlueKeep/EternalBlue 内网利用。博客是同源摘要，不另建“独立证据”。EternalBlue 目标有 SMB 会话、DoublePulsar 与 loader 结果，研究者未见实际 exploit code，必须保留此限制。
- T1080 的 DirSharePivot 原作者记录了共享盘现场、隐藏真实目录、同名导航替身与受害者点击后的正常目录显示和载荷执行；该证据按作者可见范围使用。Group-IB RedCurl 落地页未披露技术细节，不用它证明第二子项。
- T1091 原 REF-000105 URL/日期需更正到 Microsoft 2022-10-27 页面，REF-000106 日期需更正到 Check Point 实际发表日期。ESET USBStealer A→介质→B 是样本分析重构，不宣称某次企业事件已公开全链遥测；CASE-000109 只证明接收侧触发。
- T1534 的 Microsoft 2026 与 Proofpoint 2026 可支持第二账户失陷；Proofpoint 的归档规则是攻击者预设、服务器保留而日常 Inbox 看不到。ESET Gamaredon 仅支持内部发送，不证明该案例的第二账户结果。
- T1563 的 Mandiant MAZE 直接称 tscon 已用于合法 RDP 会话劫持；CrowdStrike 的 tscon 尝试受阻，但随后 RDS shadow 控制成功。两者均未公开每次会话 ID/4778/4779 完整链。SSH channel 子项只有实现文档与技术研究，不冒充现场案例。

## 共享库初步决议

- reuse：NJT-0058、NJS-0058-001/002、其既有固定 ATT&CK 来源与可证 Claims；REF-000377、REF-000379、REF-000474、REF-000475、REF-000301 等相同 URL；MIT-000053 和 MIT-000036 的相同控制概念需按目标扩应用。
- create：四项新父、四项新子及各候选特定 DET/NJA；新的 ESET Gamaredon 与 InvisiMole PDF 各只建一个 REF，DeviceProcessEvents 只建一个 REF。Case 按具体事件/环节决定，可同源但不可重复同一事实。
- split：T1080/T1534 的内容对象与消息主体；T1210/T1563 的漏洞触发与既有会话控制；T1534 与 NJT-0111 默认视图遗漏；T1080 与 T1570 的对象污染与独立文件传输。
- defer：T1210 六条未成立匿迹轴，T1534 主题归档新子项，T1091 元数据清理作为本父新子项，T1563 SSH 野外归因。任何有意低慢、完整来源路径或未见 exploit code 的声称不得通过模板化正文补足。

五项父与子项均须逐字段对照 NJT-0001 的责任和论证深度，防御对象按真实目标、数据字段、关联键、误报和盲区分别审核。正式 ID 尚未分配；本文件不是人工领域评审。
