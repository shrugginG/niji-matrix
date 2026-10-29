# T1112 注册表修改：准入后研究交接

本项已在本批 admission review 中裁定 adapt，正式 ID 需等待前项候选全部门禁后分配。固定父来源是 ATT&CK Enterprise 19.1 T1112，无 ATT&CK 子项。TA0003 已存在 NJT-0094 Registry 驻留/持久化，不应把它的隐藏键或跨 API 视图子项复制到 TA0112。建议父级直接对象是“本地 Registry 防御设置版本—实际消费者—有效安全结果”的链，而非 Registry 介质本身；集中域/租户策略分发由 NJT-0125 拥有，工具状态损伤可并记 NJT-0123，但不能替代本地 Registry 来源。

定义需限制在攻击者改写 Internet/IE 安全区域、Defender 审计或保护设置等受防守组件消费的 Registry 值，并使原本启用的检测、限制或响应实际下降。匿迹特性是写入可由普通 reg/API 产生，消费者稍后从 Registry 读取并表现为正常系统设置，writer 与保护结果分处两个日志/时间窗；残余是 4657 或 Sysmon 12/13/14、旧新值、SACL、进程/session、有效设置与受控功能验证。只见值写入、没有消费者采用，或篡改保护忽略改动，不得认定成功。

直接事件来源：Booz Allen Hamilton 对 2015 乌克兰电力攻击的技术报告在 BlackEnergy 样本分析中明确列出 in-registry Internet/IE 安全设置下降，并将其与 rundll32 和后继 C2 行为联系；这是样本和事件链分析，不能替所有环境证明每个控制都被关停。Microsoft 4657 只在目标 Registry SACL 设置 Set Value 审计时产生并保存 old/new，Sysmon 文档支持 Registry 写入与进程连接，但未覆盖所有读值。Microsoft Defender tamper protection 文档明确说明受保护的 Registry 改动可能表面成功而实际被拒绝，此反例必须在定义、Analytic 与研究限制中可见。

开放 taxonomy 搜索了保护设置压低、审计开关、账户/认证配置、隐藏键、启动项与用后回退。后四者多数归身份、NJT-0094、启动持久化或源对象，Registry 键名和目标产品不形成 NJS。尚无结论级证据证明本地 Registry 保护开关的多个稳定兄弟变量有不同残余或防守方法，建议零子项；不因 ATT&CK 无子项停止搜索。重要边界是“写入—消费—有效防御下降”，与 NJT-0125 的权威中心扇出不同。

Detection Strategy 应将 Registry old/new、writer、进程和消费者实际保护结果关联。Analytic 优先 4657（SACL 为前提）与 Sysmon 12/13、不同权的配置快照、Defender Effective settings 或独立功能测试，输出 mutation_only、adopted_but_blocked、effective_impairment；审计关闭和产品迁移需要变更单及受控 canary。Mitigation 应最小化敏感键写权限、预配 SACL、使用产品篡改保护、保留外部不可变快照并逐设置验证实际效果。不能拿 T1112 大量持久化/载荷存储案例冒充防御削弱实例。

双语正式正文须逐字段覆盖定义、特性、边界、BlackEnergy 场景、攻防模型、受信消费者 NM-BT 因果链、零子项理由、DET→NJA、MIT Application 和事件/平台限制。当前只作研究，未分配 NJT/NJS/CLM/DET/NJA/MIT。
