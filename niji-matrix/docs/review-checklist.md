# 单技术审查清单

本清单与[字段规范](technique-field-specification.md)、[防御对象规范](defense-object-specification.md)及 [NJT-0001 范例](njt-0001-exemplar.md)配套使用。

## 准入与分类

- [ ] 已固定唯一战术与 ATT&CK 基线版本。
- [ ] 已完成 `retain`、`adapt`、`exclude` 或 `add` 决策，决策和 Technique origin 一致。
- [ ] `add` 已证明现有父技术不能覆盖该缺口。
- [ ] ATT&CK 子技术未进入 Niji 子技术候选或正式数据。
- [ ] 与同战术及相邻战术技术的边界已比较。

## 父技术字段

- [ ] Schema 为 2.0.0，顶层键只包含规范字段且顺序遵循模板。
- [ ] `definition_and_concept` 与 `stealth_characteristics` 是两个独立顶层板块。
- [ ] 定义、匿迹特性、范围边界、应用场景、攻击者模型、防守方模型和研究限制各负其责。
- [ ] 正文是一至四段完整自然段，没有项目符号碎片、Markdown、HTML 或 UI 布局说明。
- [ ] 中英文逐段配对，范围、强度、置信度和限制等价。
- [ ] taxonomy 说明稳定划分变量、兄弟覆盖和禁止的分类基础。
- [ ] taxonomy coverage 与实际 child refs 一致。

## 匿迹子技术

- [ ] ID 为 `NJS-<父 NJT 四位号>-<三位子序号>`，父级段与 `parent_ref` 一致。
- [ ] 父子引用双向一致，子技术只有一个父级，`attck_subtechnique_inherited: false`。
- [ ] 子技术具有与父技术相同的全部核心阅读字段。
- [ ] 第一段匿迹特性分析以子技术准确的中文/英文名称直接开头。
- [ ] 每个子技术由稳定匿迹变量、痕迹变化和防守观察影响定义。
- [ ] 兄弟子技术边界可判定，无无法解释的重叠或遗漏。
- [ ] 未按工具、产品、介质、目标类别或 ATT&CK 子技术机械拆分。
- [ ] 假设性子技术明确标注，未伪装为已证实事实。

## 匿迹机理

- [ ] 每个父技术/子技术至少存在一项实际成立的机理。
- [ ] 每项机理具有唯一 `mechanism_ref`、角色、`summary`、自然因果分析、证据和置信度。
- [ ] `summary` 简短、适合表格且中英文均无句末标点。
- [ ] analysis 连贯解释行为设计 → 痕迹变化 → 防守影响 → 匿迹效果。
- [ ] 每个机理 `evidence_ref` 同时存在于主体 `evidence.reference_refs`。
- [ ] 正式对象不包含 `unmapped_mechanisms`。

## 证据与共享库

- [ ] 关键事实、边界和机理判断有原子 Claim 与可定位 Reference。
- [ ] 来源元数据、日期、定位信息和访问日期完整。
- [ ] Case 未超出来源支持层级，父级证据未被误当为特定子技术证据。
- [ ] REF、CLM、CASE、DET、NJA、MIT、REL 已查重并正确复用。
- [ ] 临时键已全部处理为 reuse、extend、create、split 或 defer。
- [ ] 所有正式引用可解析且类型正确。

## Detection Strategy 与 Analytic

- [ ] Technique/Sub-technique 的检测引用指向 DET，不直接指向 NJA。
- [ ] DET 定义目标、适用对象、域与至少一个 Analytic。
- [ ] DET↔NJA 引用双向一致，NJA 只属于一个 Strategy。
- [ ] NJA 具有可实施 logic，而不是空白或重复 Strategy 描述。
- [ ] 每项 data requirement 有来源、名称和非空 required_fields。
- [ ] observables、correlation window/dimensions、false positives、blind_spots、tuning_guidance 均非空且具体。
- [ ] DET evidence 覆盖全部关联 NJA 的 evidence。
- [ ] DET 确实适用于当前主体，或父技术所列的至少一个子技术。

## Mitigation

- [ ] MIT 具有总体说明和至少一个可实施 measure。
- [ ] 每个 application 的 target 唯一，且具有 use、expected_effect 与 limitations。
- [ ] `applications[].target_ref` 是适用性的唯一事实源，不存在重复 `mitigates_refs`。
- [ ] MIT 确实适用于当前主体，或父技术所列的至少一个子技术。

## 工程与页面质量

- [ ] Schema、模板、字段规范和 Review Web 映射一致。
- [ ] `make quality` 达到 0 error、0 warning、0 未决重复并通过全部契约测试。
- [ ] `build_technique_bundle.py NJT-xxxx` 成功。
- [ ] `npm test` 通过，API issues 为 0。
- [ ] 中英文父/子页面均显示固定板块；表格均由 YAML 结构关系生成。
- [ ] 原始 YAML、跨对象导航、生命周期、版本和来源路径正确。
- [ ] `allocate_id.py list --status reserved` 无未解释记录。
- [ ] 机器通过后状态为 `review`；只有记录人工领域审查后才为 `published`。
