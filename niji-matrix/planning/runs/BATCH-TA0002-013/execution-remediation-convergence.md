# TA0002 Execution 整改收敛审查

本轮总体范围 NJT-0074～NJT-0082 已按六个顺序小批次完成，所有父技术、Niji 子技术、准入决策、结论级证据和目标特定防御均处于 `review`。九项整改没有按同一模板批量扩写；复杂 T1677、T1053、T1204 分别单候选处理，其他候选以共享边界为依据双件处理。

交叉边界已经统一：CI/CD runner 由 T1677 负责，企业部署 agent 由 T1072 负责，系统 service manager 由 T1569 负责，WMI provider 由 T1047 负责；shared module 标准/反射表示与 T1574 search-order、T1055 cross-process injection、T1106 API resolution 分开；T1204 只保存人类动作到首个执行的因果边，媒介、Phishing、exploit、interpreter、container/library/RMM 仍属于相邻对象。

共享库收敛后，过宽的 DET-000058/NJA-000032/NJA-000037/MIT-000057 与 DET-000059/NJA-000034/MIT-000058 已移到对应批次 `retired/` 并归档；NJA-000042 被 WMI 专用分析取代后归档；DET-000063/MIT-000060 仅保留 TA0003 NJT-0089 持久服务覆盖。新建的重复来源均复用既有规范对象，未保留 exact 或 unresolved possible duplicate。

跨技术开放缺口审查未发现需要 `add` 的稳定 Execution 父级。外部贡献事件分离、非 Windows 调度枚举抑制、软件部署批准窗口/低慢分批、serverless execution-role 独立子项、远程 shared-module 来源和 willing-insider 用户子项因直接意图证据不足或已被相邻对象覆盖而延期。正式 taxonomy 不以 ATT&CK 子技术数量为配额。

机器验证完成后 TA0002 计划可进入 `review`，但所有对象仍等待人工领域审查；本记录不授权 `published`。
