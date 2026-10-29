# BATCH-TA0003-009 人工审查整改记录

2026-09-12 横向审计发现 NJT-0090 及父子、DET/NJA/MIT 与 Claim 全部依赖单一 ATT&CK T1546 页面，两个子项没有独立案例，攻防模型与限制不足以说明谓词匹配率、CreatorSID/object ID、Broker callback、保留期、in-process action 和合法自动化反例。

整改保留原 `adapt` 与 18→2 taxonomy 结论，但引入 Microsoft 永久 WMI consumer、Sysmon WMI 19/20/21、WMI provider/tracing、Mandiant WMI 监控和 Solorigate binding。谓词轴只使用结构/红队证据并保持 mechanism `medium`，不把未公开的 Solorigate WQL 越级为其案例；Broker 轴使用 CASE-000115。DET/NJA 分离静态风险、匹配、Broker 与结果，MIT 增加可解析谓词、object/callback ID 和安全禁用。全套门禁通过后保持 `review`。
