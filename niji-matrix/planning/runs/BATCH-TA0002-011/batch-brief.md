# BATCH-TA0002-011 T1053 单候选整改约束

- 总体任务范围是 Execution 剩余 NJT-0074～NJT-0082；本批只处理 T1053/NJT-0075。BATCH-TA0002-014 已通过证据、内容、共享库、质量、Bundle 与 34 项 Web 门禁。
- 固定 `enterprise-attack 19.1` 的 T1053 有五项 ATT&CK 子技术：T1053.002 At、.003 Cron、.005 Scheduled Task、.006 Systemd Timers、.007 Container Orchestration Job。它们只作为平台与调度实现的宽度先验，不导入 Niji taxonomy。
- T1053 的直接对象是调度器保存触发条件并在未来时间、事件或状态满足时启动命令、脚本、程序或工作负载。单纯 sleep loop、应用内部 timer、立即执行而未建立调度对象，以及只讨论 Persistence/Privilege Escalation 的结果不属于本 Execution 对象。
- 第一轮覆盖必须跨 Windows、Unix/systemd 与 Kubernetes 调度面检查命名/情境合形、观察窗口外延期、状态枚举抑制、一次性短驻代理、远程调度和触发类型；第二轮用 Tarrask、Nitrokod、Serpent 与真实伪装任务案例检验每个候选的稳定性、痕迹变化和防御差异。
- 旧 DET-000063/NJA-000041/MIT-000060 同时覆盖 T1053、T1569 与 T1047，无法保持目标特定逻辑。本批为 T1053 新建专用 DET/NJA/MIT，并仅移除旧对象中 NJT-0075 及其子项的反向关联，其他候选留待各自批次处理。
- 正式内容使用 YAML-only 2.0、成对双语自然段与 NJT-0001 字段责任。当前批次未通过 evidence、taxonomy、content-depth、defense、duplicate、Bundle 和 Web QA，不启动下一批正式写入。
