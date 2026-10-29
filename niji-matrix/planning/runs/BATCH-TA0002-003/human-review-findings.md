# TA0002 Execution 人工审阅整改记录

## 审阅结论

2026-09-10 的人工领域审阅确认，TA0002 的两次原始开发批次虽然通过 Schema、规划、重复审计、Bundle 和 Review Web 机器门禁，但父技术与子技术的读者正文普遍未达到 NJT-0001 所展示的字段责任和论证深度。该问题属于系统性语义缺口，不是局部措辞问题。

量化抽查显示，20 个父技术的定义、匿迹特性、范围边界、应用场景、攻击者模型、防守方模型和研究限制均统一压缩为单段；每个父技术只有一个固定版本 ATT&CK Reference、一个父级 Claim 和零个 Case。40 个子技术的研究限制只有两种批次模板，且多项威胁模型、机理分析和 Mitigation Application 具有明显的名称替换式结构。

## 治理处置

- 保留 NJT-0063 至 NJT-0082、现有 NJS、共享库对象和 consumed ID，不释放或复用编号。
- 将 TA0002 父技术、子技术、准入决策、专属 Claim、DET、NJA 和 MIT 退回 draft；固定版本 Reference 保持规范身份。
- 将原 BATCH-TA0002-001 与 BATCH-TA0002-002 标记 paused，保留其机器验证记录作为历史审计材料。
- 将总体计划恢复为 active，candidate inventory 保持 complete，taxonomy、evidence、bilingual 与 gap analysis 重新进入 in-progress。
- 按一至三个候选的受控批次重新研究；当前只激活 BATCH-TA0002-003，对 T1197 / NJT-0063 进行试点重写。

## 试点验收要求

NJT-0063 及其现有子技术必须重新完成结论级证据、准入、子技术成立性、逐字段双语正文、机理因果链、DET→NJA、MIT Application、NJT-0001 字段责任对照、Bundle 和双语 Web QA。试点通过机器门禁后仍保持 review；在人工确认其深度基线前，其余整改批次不进入正式写入。
