# 规范对象模板

新对象必须从对应模板开始，并同时阅读字段规范与现行范例。模板定义形状，Schema 执行结构约束，规范文档定义字段语义与写作质量。

## 模板清单

| 对象 | 模板 | 权威说明 |
|---|---|---|
| 技术准入决策 | `technique-decision.yaml` | [编写指南](../docs/authoring-guide.md) |
| Technique | `technique/technique.yaml` | [字段规范](../docs/technique-field-specification.md)与 [NJT-0001 范例](../docs/njt-0001-exemplar.md) |
| Evasion Sub-technique | `subtechnique/subtechnique.yaml` | 同上 |
| Detection Strategy | `detection.yaml` | [防御对象规范](../docs/defense-object-specification.md) |
| Detection Analytic | `analytic.yaml` | 同上 |
| Mitigation | `mitigation.yaml` | 同上 |
| Reference | `reference.yaml` | 共享库治理规则 |
| Claim | `claim.yaml` | 共享库治理规则 |
| Case | `case.yaml` | 共享库治理规则 |
| Relationship | `relationship.yaml` | 共享库治理规则 |

## 使用规则

1. 先完成准入、范围与共享库查重，再由主 Agent 分配正式 ID。
2. NJS 必须使用 `allocate_id.py reserve NJS --parent NJT-xxxx` 分配。
3. 复制对应模板并替换全部 `__REQUIRED__`、零值示例 ID 和示例内容。
4. 不删除必填字段，不增加同义字段、自由章节、Markdown 或页面布局字段。
5. Technique/Sub-technique 必须按模板顺序保留全部共同字段和各自专有字段。
6. DET 与 NJA 双向连接；NJA 的数据字段、误报、盲区与调优不得留空。
7. MIT 的 `applications[].target_ref` 是适用关系的唯一事实源。
8. 补齐所有被引用的规范对象，执行 `make quality`，构建 Bundle 并完成 Web QA。

模板目录本身不会被正式内容校验器扫描，但契约测试会检查模板、Schema 与 NJT-0001 的共同字段是否持续一致。
