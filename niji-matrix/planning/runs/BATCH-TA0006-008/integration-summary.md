# BATCH-TA0006-008 集成摘要

T1003 经 `adapt/high` 形成 NJT-0177“操作系统认证材料提取”。固定八项 ATT&CK 子技术完成逐项覆盖和第二轮去名聚类，正式形成三项 NJS：可信凭据读取上下文转用、非活动认证存储视图提取、目录复制式认证材料导出。普通活动存储直接读取留在父级；低量、dump 加密和后继离线猜测不建项。

新增 1 NJT、3 NJS、1 决议、2 DET、3 NJA、1 MIT、6 Claim、1 受控实验 Case 和 8 Reference。复用或扩展替代存储视图、Volt Typhoon、DueDLLigence、目录复制检测和材料暴露恢复对象；DCSync 子项明确保留缺少完整在野 caller—response—output—use 链的限制。

质量：`make quality` 通过；0 错误、0 警告；重复审计 0 精确、0 待审；Reader prose 145 个父技术通过；Bundle NJT-0177 已构建；定向 Web 4/4、全量 Web 113/113。正式对象保持 `review`，等待人工领域评审。

完成日期：2026-09-27。
