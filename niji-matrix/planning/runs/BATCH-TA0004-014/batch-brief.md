# BATCH-TA0004-014 语义整改约束

## 基线与范围

- 战术：TA0004 Privilege Escalation / 权限提升
- ATT&CK 基线：enterprise-attack 19.1
- 当前批次：T1078 / NJT-0061 与 T1053 / NJT-0075
- 范围：只修复正式 Technique/Sub-technique 读者正文的字段责任、双语自然度和产物边界；保留现有 ID、准入决议、taxonomy、证据、DET/NJA/MIT 和引用关系。
- 批次理由：两者都是跨战术复用对象，并把 TA0004 权限结果门重复扩写到几乎所有读者字段，适合作为首个对照整改批次。

## 正文约束

- 父技术只在 definition 或 scope 中保留一处简洁的 TA0004 成立边界，不在场景、攻防模型、机理和限制中重复。
- 子技术通过父级继承战术语境，除非兄弟边界确有必要，不重述 TA0004 证明门。
- elevation_confirmed、authority_unresolved、expected-deny/observed-allow 等输出状态和事件关联步骤只保留在 DET/NJA。
- ATT&CK 子项覆盖、第二轮搜索、数量增减理由和候选轴决议只保留在 planning 记录。
- 中文不使用成串英文标识符替代自然表达；必要平台字段仅作例证。

## 验收

- 逐个对照 NJT-0001 的字段责任，不对齐字数。
- 运行 make quality、构建 NJT-0061/NJT-0075 Bundle、检查 pipeline 和 reserved IDs、运行 Review Web npm test。
- 本批次未通过前，BATCH-TA0004-015 不进入正式 YAML 写入。
