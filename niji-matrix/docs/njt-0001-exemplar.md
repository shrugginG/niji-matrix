# NJT-0001 规范范例

NJT-0001“主动扫描”是后续 Niji Matrix 技术开发的结构与质量范例。应当学习它的合同形状和研究方法，不得复制其结论、对象数量、机理数量、子技术数量或证据规模。

## 一、规范技术包

```text
matrix/tactics/TA0043-reconnaissance/
├── decisions/DEC-TA0043-T1595.yaml
└── techniques/NJT-0001-active-scanning/
    ├── technique.yaml
    └── subtechniques/
        ├── NJS-0001-001-temporal-dilution-scanning/subtechnique.yaml
        ├── NJS-0001-002-distributed-source-scanning/subtechnique.yaml
        ├── NJS-0001-003-source-attribution-obfuscation/subtechnique.yaml
        ├── NJS-0001-004-fragmented-probe-scanning/subtechnique.yaml
        └── NJS-0001-005-probe-feature-camouflage/subtechnique.yaml
```

配套防御对象示例：

- `detections/DET-000001-long-horizon-scan-correlation.yaml`；
- `analytics/NJA-000001-long-horizon-scan-correlation.yaml`；
- `mitigations/MIT-000001-external-exposure-minimization.yaml`。

## 二、父技术展示了什么

- `definition_and_concept` 与 `stealth_characteristics` 各负其责。
- `scope_boundary_definition` 使用连贯自然段界定纳入、排除与相邻对象。
- 应用场景、攻击者模型和防守方模型显式分开。
- `stealth_mechanisms` 只列实际成立的机理；每项都有角色、无句末标点的摘要、因果分析、证据和置信度。
- taxonomy 用稳定匿迹变量和防守观察效果划分子技术。
- 防御字段引用可复用的 DET 和 MIT，不嵌入展示文本。
- Claim、Case、Reference、研究限制和 lifecycle 各有明确职责。

## 三、子技术展示了什么

- 子技术 ID 的父级段与 NJT-0001 一致。
- 子技术具备与父技术相同的核心阅读字段。
- 子技术只增加 `parent_ref` 与不继承 ATT&CK 子技术的 lineage。
- 第一段匿迹特性分析以准确子技术名称直接开头。
- 五个兄弟项分别按时间、真实来源分布、来源归因、报文可检查性和可见特征划分，而不是按 ATT&CK 子技术、工具或扫描目标划分。
- 每个子技术引用真正适用于自身行为的检测与缓解对象。

## 四、防御对象展示了什么

- DET-000001 定义总体检测目标、适用对象和 Analytic 集合。
- NJA-000001 保存可实施的 logic、数据要求、关联、误报、盲区和调优。
- MIT-000001 将可复用 Measure 与针对 NJT-0001 的 Application 分开。
- Strategy 与 Analytic 双向连接；Technique 不直接引用 Analytic。
- Mitigation 的 `applications[].target_ref` 是适用性的唯一事实源。

## 五、如何使用深度基线

NJT-0001 的价值不在于字数，而在于各字段完整承担职责：定义说明行为与直接目的后，再固定概念边界；匿迹特性说明核心矛盾、可控痕迹属性和残余可观察性；范围同时给出纳入、排除、相邻对象与正常反例；威胁模型分别描述攻击者能力和防守观察条件；限制区分不同证据所能支持的结论层级。

审查新对象时应逐项确认这些问题得到回答。较短内容在论证本来简单时可以成立，较长内容如果只是模板扩展仍不合格。一个多候选批次若所有父技术都采用相同的一段式结构，或所有子技术共享相同限制和威胁模型，应视为需要逐候选重写的信号。

## 六、不得照搬什么

- 五个子技术不是目标数量；零个或其他数量均可能合理。固定基线 ATT&CK 子技术数量可以作为研究广度先验，触发覆盖表和第二轮 taxonomy 搜索，但不得成为 NJT-0001 或其他父技术的输出配额。
- 三种机理不是规定数量；每个对象只记录自身成立的机理。
- `high` 置信度不是默认值。
- 主动扫描的证据不能支持另一个候选。
- 名称、范围、场景、威胁假设、Analytic 和 Mitigation 必须独立研究。
- NJT-0001 的页面效果不能成为新增自由字段或手工表格的理由。

## 七、使用范例审查新对象

1. 将新父技术或子技术的顶层键、字段顺序和字段责任与 NJT-0001 对照，不以字数或对象数量代替语义审查。
2. 根据[字段规范](technique-field-specification.md)逐项核对内容责任。
3. 根据[防御对象规范](defense-object-specification.md)核对 DET→NJA 和 MIT Application。
4. 确认共享对象经过查重、复用决议和正式 ID 分配。
5. 运行 `make quality` 并构建该技术 Bundle。
6. 在 Review Web 中检查中英文、全部固定板块和跨对象跳转。
7. 未记录人工领域审查前保持 `lifecycle.status: review`。
