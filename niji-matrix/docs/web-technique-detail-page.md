# 匿迹技术详情页 YAML-only 映射

本映射是[技术与子技术字段规范](technique-field-specification.md)及[防御对象规范](defense-object-specification.md)的消费端呈现合同；页面不得新增内容语义或容忍规范字段缺失。NJT-0001 是现行呈现范例。

Review Web 使用统一字段生成父技术和子技术详情页。

## 固定阅读结构

1. 页头：名称、摘要和生命周期。
2. 定义与概念：`definition_and_concept`。
3. 匿迹特性分析：`stealth_characteristics`。
4. 范围边界界定：`scope_boundary_definition`。
5. 应用场景与威胁模型：先显示应用场景，再分为攻击者模型和防守方模型。
6. 匿迹机理：只显示 `stealth_mechanisms` 中实际成立的机理。
7. 父技术额外显示子技术分类说明和子技术表。
8. 检测策略：由 `defense.detections.strategy_refs` 生成 Strategy 表；进入策略后可继续查看 NJA Analytic、数据要求、关联、误报、盲区和调优。
9. 缓解措施：由 `defense.mitigations.mitigation_refs` 生成表格；详情显示结构化措施和逐目标应用。
10. 案例、主张、参考资料、研究限制和研究治理。

## 机理表

每行显示机理、角色、`summary` 和置信度。Summary 用于表格且无句末标点；详细 `analysis.paragraphs` 在下方以自然段展示。不显示未映射机理。

## 父子同构

父技术和子技术使用相同的正文、威胁模型、机理、防御、证据和生命周期渲染器。只有父技术显示 classification 与 subtechnique taxonomy，只有子技术显示 parent 和 lineage。

## 防御对象

Detection Strategy 和 Analytic 是两个独立对象。Mitigation 的措施与应用均由 YAML 数组生成表格。页面不读取 Markdown，也不接受作者提供的列定义或 HTML。
