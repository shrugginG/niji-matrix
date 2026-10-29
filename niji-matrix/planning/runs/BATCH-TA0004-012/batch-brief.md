# BATCH-TA0004-012 Batch Brief

## 固定基线与顺序

- 唯一基线：`matrix.yaml` 锁定的 `enterprise-attack` `19.1`；本批不迁移版本。
- TA0004 冻结候选总数为 13；前 11 项已完成候选决议。本批只处理固定顺序第 12 项 T1053，不提前写入第 13 项。
- 第 12 项：T1053 — Scheduled Task/Job（计划任务/作业）。现有跨战术决议为 `DEC-TA0002-T1053`（retain）；现有 Niji 对象为 `NJT-0075` “Stealth-Conforming Scheduled Execution / 匿迹贴合的计划执行”与 `NJS-0075-001..004`。TA0004 尚无独立决议，必须先验证跨战术复用和权限结果门。
- 第 13 项：T1078 — Valid Accounts（有效账户）。现有跨战术决议为 `DEC-TA0001-T1078`（retain）；现有 Niji 对象为 `NJT-0061` 与 `NJS-0061-001..002`。TA0004 尚无独立决议；仅登记为下一批，不在本批正式写入。

## 单候选交付控制

- 本批候选数为 1。T1053 的固定 ATT&CK 子技术数为 5，需逐项/逐簇覆盖并进行开放匿迹变量搜索；若复用现有四个 NJS，仍须证明各轴在 TA0004 下的权限语义和防御差异，而不是沿用 TA0002 结论。
- 在 T1053 完成 evidence、taxonomy breadth、字段责任、共享防御对象决议、`make quality`、NJT-0075 Bundle、pipeline、reserved ID、`npm test` 和父/四子及相关防御对象的中英文 live Web QA 前，不开始 T1078 正式 YAML。
- lifecycle 保持 `review`；未完成人工领域审查，不得设置 `published`。

## 本批待回答问题

- T1053 是否在 TA0004 retain：必须证明 scheduler definition/submitter、scheduler authority、triggered execution context 和首个 source 原本无权完成的资源结果，而不是由 root/SYSTEM 用户名或高权限 task label 倒推。
- 固定五项 ATT&CK 子技术 `.002 At`、`.003 Cron`、`.005 Scheduled Task`、`.006 Systemd Timers`、`.007 Container Orchestration Job` 如何覆盖到 parent-core、现有 NJS、adjacent、deferred 或 rejected；并重新检查 ATT&CK 内、跨分类及 ATT&CK 外候选轴。
- 现有 NJS-0075-001 baseline conformity、002 long-horizon deferral、003 enumeration suppression、004 ephemeral one-shot brokerage 是否都满足 TA0004 的 attacker-controlled trace variable、权限结果与目标特定防御门；最终数量为何不增不减。
- 七类共享库中的现有 `REF/CLM/CASE/DET/NJA/MIT/REL` 应分别 reuse、extend、create、split 或 defer；现有 `DET-000087` ↔ `NJA-000064` 与 `MIT-000088` 是否可在不泛化的前提下扩展 TA0004 authority lineage。
