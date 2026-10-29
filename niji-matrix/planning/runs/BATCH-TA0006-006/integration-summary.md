# BATCH-TA0006-006 集成摘要

## 准入与分类

- T1111：`adapt/high` 为 NJT-0174“多因素认证证明截获”，正式 NJS 为短时单次证明截获、认证证明生成状态复制；绑定认证器代理因完整事件链不足暂缓。
- T1621：`adapt/high` 为 NJT-0175“攻击者驱动的多因素认证挑战生成”，正式 NJS 为受信挑战重复压力、跨信道请求情境同步；高频明确视为增加痕迹，不作为时空释痕。
- ATT&CK 父项均无子技术；四项 NJS 来自材料寿命、challenge 序列和跨信道因果，不按 MFA 介质、产品或厂商划分。

## 正式对象

新增 2 个 NJT、4 个 NJS、2 个准入决议、2 个 Detection Strategy、4 个 Detection Analytic、2 个 Mitigation、9 个 Claim、6 个 Case 和 15 个 Reference。扩展 REF-000731、DET-000194/197/115、MIT-000175/180/116 及 T1621 的既有关系权威证据映射；没有创建 relationship 对象。

## 质量与状态

- `make quality`：通过；内容与规划为 0 错误、0 警告。
- 共享库：0 组精确重复、0 组待审可能重复、4 组已审查相似项。
- Reader prose：143 个父技术及其子技术通过。
- Bundle：NJT-0174、NJT-0175 已构建。
- Review Web：定向测试 2/2；全量测试 109/109；Repository snapshot issues 为空。
- ID：44 个分配型对象已同步消费；正式对象保持 `review`，等待人工领域评审。

完成日期：2026-09-27。
