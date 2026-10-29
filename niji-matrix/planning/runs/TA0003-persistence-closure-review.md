# TA0003 Persistence 战术收口审查

## 固定范围与结果

基线为 MITRE ATT&CK Enterprise 19.1。固定 22 个父候选全部具有独立准入决策，并全部进入正式矩阵 `review`：T1098、T1197、T1547、T1037、T1671、T1554、T1136、T1543、T1546、T1668、T1133、T1525、T1556、T1112、T1137、T1653、T1542、T1053、T1505、T1176、T1205、T1078。其正式归宿为 22 个 NJT，TA0003 下可见 49 项 Niji 原生 NJS。ATT&CK 子技术仅作研究广度先验，没有作为 Niji 子项导入。

最后四项的独立准入为：T1505 `retain`→NJT-0225，T1176 `retain`→NJT-0226，T1205 `adapt`→跨战术复用 NJT-0120，T1078 `retain`→跨战术复用 NJT-0061。前两个各形成两项新 NJS，后两个完整复用既有 matcher 与身份观察变量；持续性只作为父级结果门。

## 跨技术所有权收敛

- 身份与认证链：NJT-0061 只拥有未修改有效身份/会话的接受与使用，NJT-0083 拥有账户、认证器、角色和授权状态修改，NJT-0088 拥有新身份创建，NJT-0093 拥有认证过程 decision 与秘密路径。远程服务 NJT-0055 是承载路径，不能替代身份结果门。
- 调度、启动与事件链：NJT-0075 拥有 scheduler 保存的 trigger-to-action 对象，NJT-0084 拥有启动/登录 lifecycle descriptor，NJT-0085 拥有初始化脚本内容，NJT-0089 拥有 durable service definition，NJT-0090 拥有独立 predicate-event-broker-action 注册。systemd timer 可共映射调度与 service，但直接对象不合并。
- 软件内容与扩展链：NJT-0087 拥有既有 host binary 内容破坏，NJT-0092 拥有未来置备的内部 image lineage，NJT-0225 拥有服务器软件扩展、请求与启动路径，NJT-0226 拥有浏览器/IDE 等宿主扩展状态，NJT-0095 保留 Office 专属启动面。服务器/client 宿主和持久注册对象分别闭合，不按 DLL/插件名称合并。
- 网络与入口链：NJT-0120 拥有 signal matcher 到隐藏功能激活，持久映像/启动项/service 仍由其载体技术拥有；NJT-0055 拥有外部远程服务连接，NJT-0061 拥有被接受身份，NJT-0091 拥有排除竞争入口。相同 C2 结果不消除入口机制差异。
- 平台连续性：NJT-0096 通过抑制休眠/关机延长易失立足点，NJT-0097 在 OS 前启动流与 attestation 边界持久，NJT-0225 的 VIB 只在其服务器组件包与加载对象范围内成立；启动层、供电状态和服务器包身份分别保留。
- Registry 只在 NJT-0094 中拥有驻留状态介质与 API 差分；具体 autostart、service、event、身份或组件用途仍返回其行为 owner，避免按介质重复。

## Niji 原生缺口审查

开放搜索覆盖 identity/session continuity、认证 decision、账户和设备信任、scheduler、启动与 service lifecycle、事件谓词、Registry、host binary、内部 image、服务器/client 扩展、Office、云应用集成、远程服务、网络信号、固件/boot 与电源连续性。当前未发现同时满足独立父行为、稳定攻击者可控匿迹变量、结论级证据和差异化防御的额外 Niji 原生父级，`gap_analysis.status` 因此为 `complete`。

以下轴保留 defer 或相邻归属，而不是为关闭战术强制正式化：T1053 的 retry/catch-up/互相重建式 resilient re-entry；T1505 的 memory-only 组件和受信 runtime 共驻；T1176 既有 extension identity 的恶意更新与目标活动谓词；T1205 有状态序列 matcher 在缺少跨重启载体证据时的 Persistence；T1078 identity-pool rotation 与 low-rate/business-hour re-entry。后续若出现新的结论级事件和独立防御责任，可以重开候选。

## 防御、质量与发布状态

22 个正式父技术均具备 `available` Detection Strategy 和 Mitigation；49 项 NJS 按稳定变量产生。最终门禁检查 4083 个对象，Schema 与规划 0 错误、0 警告，共享库 0 精确重复、0 待审可能重复，12 项基础测试与 140 项 Review Web 测试通过。最后四项 Bundle 为 NJT-0225、NJT-0226、NJT-0120 和 NJT-0061。

机器闭环不等于人工发布。TA0003 计划设置为 `review`，taxonomy/evidence/bilingual 标记 `passed`，正式对象保持 `review` 且 reviewers 为空；只有完成独立人工领域评审后才可进入 `published` 或人工批准的完成状态。
