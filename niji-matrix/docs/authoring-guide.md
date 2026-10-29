# 单技术编写指南

本文说明从候选到正式 Technique/Sub-technique 包的操作顺序。字段的权威语义与逐项约束见[单个技术与子技术字段规范](technique-field-specification.md)，防御对象见[检测与缓解对象规范](defense-object-specification.md)，结构与质量参照 [NJT-0001](njt-0001-exemplar.md)。

## 一、先准入，再建对象

先固定 ATT&CK 基线，阅读战术计划、相邻技术和现有共享对象，并完成 `retain`、`adapt`、`exclude` 或 `add` 决策。只有非 `exclude` 候选才能分配 NJT/NJS 并创建正式目录。

Niji 子技术不得继承 ATT&CK 子技术。其分类依据必须是稳定的匿迹变量、造成的痕迹变化和对防守观察的影响。

## 二、父子共享字段

父技术和子技术必须按相同职责编写以下核心字段：

1. `name`、`summary`、`aliases`；
2. `definition_and_concept`；
3. `stealth_characteristics`；
4. `scope_boundary_definition`；
5. `application_scenarios_and_threat_model.application_scenarios`；
6. `attacker_model` 与 `defender_model`；
7. `stealth_mechanisms`；
8. `defense`、`evidence`、`research.limitations`、`lifecycle`。

父技术另有 `classification` 与 `subtechnique_taxonomy`；子技术另有 `parent_ref` 与 `lineage`。不得自行增加近义字段、展示字段或自由章节。

## 三、自然段与结构化关系

定义、匿迹特性、范围、场景、攻防模型、机理分析和限制使用一至四段中英文成对的完整自然段。不要把一句连贯论述拆成“行为定义、目的、对象、效果”等微型字段，也不要使用项目符号拼正文。

需要查询、复用或生成表格的内容才使用结构化数组和 ID：机理、子技术、Strategy、Analytic、Mitigation、Measure、Application、Claim、Case、Reference 和生命周期。

子技术的第一段 `stealth_characteristics` 必须直接以当前子技术的准确中英文名称开头，不使用“本子技术的主要匿迹特性是”等模板句。

## 四、匿迹机理

每个父技术和子技术至少有一项实际成立的机理。单项机理包含：

```yaml
- mechanism_ref: NM-ST
  role: primary
  summary:
    zh: 用于表格的简短说明
    en: Short table summary
  analysis:
    paragraphs:
      - zh: 连续解释行为设计、痕迹变化、防守影响与匿迹效果。
        en: A coherent causal analysis.
  evidence_refs: [REF-000000]
  confidence: hypothesis
```

`summary` 保持此字段名且结尾不加句号。每个 `evidence_ref` 还必须出现在对象的 `evidence.reference_refs` 中。正式 YAML 只保存已映射机理，不保存 `unmapped_mechanisms`。

## 五、子技术分类

零个子技术可以是有效结果，但必须在父级 taxonomy 中说明原因。存在子技术时：

- 使用 `NJS-<父 NJT 四位号>-<三位子序号>`；
- 中间父级段必须与 `parent_ref` 一致；
- 兄弟项依据匿迹变量和防守效果划分，不按工具、产品、扫描目标、信息类别或 ATT&CK 子技术划分；
- 每个子技术都完整编写父子共享字段，不能依赖父级正文补齐基本语义。

## 六、检测与缓解

Technique/Sub-technique 只引用 Detection Strategy（DET）与 Mitigation（MIT）。

- DET 定义总体检测目标、适用对象、域和 NJA 列表；
- NJA 定义可实施逻辑、结构化数据要求与字段、可观测信号、关联窗口与维度、误报、盲区和调优；
- DET 与 NJA 必须双向一致，DET 的证据必须覆盖其 Analytic 的证据；
- MIT 将可复用 `measures` 与逐目标 `applications` 分开；`applications[].target_ref` 是适用性的唯一事实源。

## 七、证据、共享库和生命周期

关键事实、边界、机理与子技术成立性使用原子 Claim 和可定位 Reference。Case 只在来源确实记录活动过程时建立，不能把父级行为证据升级为某个子技术证据。

创建 REF、CLM、CASE、DET、NJA、MIT、REL 前先查重；并行研究由主 Agent 统一分配和写入正式 ID。

机器质量门禁、Bundle 和 Web QA 通过后生命周期保持 `review`；只有人工领域审查完成后才能进入 `published`。

## 八、验收

```bash
make quality
python3 scripts/build_technique_bundle.py NJT-xxxx
python3 scripts/pipeline_status.py
python3 scripts/allocate_id.py list --status reserved
```

随后在 Review Web 中检查父技术和每个子技术的中英文页面、固定栏目、机理表和分析、DET→NJA 展开、MIT 措施/应用、证据导航、生命周期与原始 YAML。
