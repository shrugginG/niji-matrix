# BATCH-TA0003-016 人工审查局部整改记录

2026-09-12 审计确认 NJT-0096 的单一变量边界合理，但 NJS-0096-001 的攻防模型和限制无法证明状态转换本会终止具体入口。整改要求 power request/policy writer、预期 sleep/lock/hibernate/reboot、依赖 PID/session/token 与跨边界继续活动完整连接，加入 always-on、备份、媒体、会议、工业和维护反例，并保留“少创建制品”为 medium 推断。子项升级到 1.0.0 并保持 `review`。
