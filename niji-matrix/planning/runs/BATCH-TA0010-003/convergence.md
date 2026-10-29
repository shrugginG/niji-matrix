# BATCH-TA0010-003 主 Agent 最终战术收敛

两份 sub-agent 交接完成并通过 YAML/双语检查后，主 Agent统一完成本决议。ATT&CK 19.1 子技术只作为广度先验。

## ATT&CK 候选准入

- T1567：retain。保留向已有合法外部 Web 服务、API 或 Webhook 提交失窃数据并由服务接收/转交的父语义。
- T1537：adapt。固定页面混有不一定属于同服务跨账户控制权转移的普通云上传实例；Niji 正式范围收紧到同一服务内另一账户或租户取得访问控制或独立副本。

## 正式 Niji 子技术

- T1567：
  - 共享服务接收者归因遮蔽：外层只见合法 SaaS 域/TLS，真实接收者隐藏在 tenant/account/chat/repository 标识后。
  - 服务对象会合式外传：在外部服务新建持久对象，攻击者以后从服务取回。
  - 服务工作流转交外传：配置 Webhook/integration，由 SaaS 自身把数据持续推送到攻击者端点。
- T1537：
  - 原对象跨账户授权投射：对象 ID 连续，跨账户 grant/link/ownership 使第二主体获得访问；撤销只影响未来访问。
  - 跨账户持久副本脱离：snapshot/copy/backup 在目标账户形成新对象，源侧撤销不能收回。

T1567.001/.002/.003/.004 均解析为服务或载体实现，不导入 NJS。T1537 零 ATT&CK 子项仍完成开放分类搜索。

## Niji 原生缺口准入

- 新增“受害服务响应式拉取外传 / Victim-Service Response Pull Exfiltration”，decision=add。
- 直接行为：攻击者把已收集数据写入受害者自有、面向外部的 Web/邮件等服务路径，再由外部请求触发服务响应，把数据送出。
- 该行为不属于 T1567，因为提供内容的是受害者服务而非外部 Web 服务；不属于 T1537，因为没有同服务账户控制权转移；不要求相对既有 C2 使用替代协议，因此不稳定归 T1048；只有暂存而无外部取回仍归 NJT-0134。
- Dark Halo 的 OWA 路径、公开 HTTPS URL 与外部取回提供结论级证据。复用 REF-000509、REF-000514、REF-000924 和 CASE-000183。
- 当前只证实一个稳定方向/所有权变量；按 Web/邮件产品、文件扩展名或归档形式拆分没有独立防御价值，因此父技术使用 none-justified，不创建 NJS。
- 新建专用 DET/NJA；MIT-000136 的受控暂存落点、Web 服务职责分离和独立审计 measures 不变，精确新增本对象 application。

## 共享库决议

- T1567 复用 REF-000625、REF-000640、REF-000923、REF-000924、REF-000604、REF-000632；扩展 CASE-000214 到 T1567 父项时不改变 Bazar/Conti 使用 Rclone+MEGA 与限速事实。
- T1567 新建 7 个来源；T1537 新建 9 个来源。不存在相同 URL 的既有 Reference。
- T1567 新建 2 DET/3 NJA/1 MIT，并为 MIT-000156、MIT-000200 增加目标专用 applications。
- T1537 新建 1 DET/2 NJA/1 MIT。MIT-000141、MIT-000166 与本项 grant/copy/receiver-result 控制身份不同，保持 split。
- Niji gap 新建 1 DET/1 NJA，扩展 MIT-000136；CASE-000183 复用并扩展 subject_refs。
- OilRig 的同一 OneDrive/Exchange 关系同时承担 C2 与回传时归 NJT-0192；Shai-Hulud 私有仓库迁往攻击者账户部分归 T1537，只有本机秘密创建新服务对象与 Actions→Webhook 部分归 T1567。

## 战术闭合

完成本批后，固定 ATT&CK Enterprise 19.1 的 9 个 TA0010 父候选均有准入决策；正式矩阵包含 9 个 ATT&CK 来源父技术和 1 个 Niji 原生 gap 技术。战术级 gap、跨技术边界、共享库、防御覆盖和机器/Web 门禁全部通过后，TA0010 计划可进入 review；所有正式对象仍等待人工领域评审。
