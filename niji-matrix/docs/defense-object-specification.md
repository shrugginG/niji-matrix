# 检测与缓解对象字段规范

本文是 Detection Strategy（`DET-*`）、Detection Analytic（`NJA-*`）与 Mitigation（`MIT-*`）的权威字段规范。DET-000001、NJA-000001 和 MIT-000001 是结构范例。

## 一、Detection Strategy

Strategy 定义“要检测什么”，并组织一项或多项可以实施的 Analytic。它不得吸收 Analytic 的实现细节。

| 字段 | 含义与约束 |
|---|---|
| `schema_version` | 必须为 `2.0.0`。 |
| `type` | 必须为 `detection-strategy`。 |
| `id` | 规范 `DET-xxxxxx`。 |
| `name` | 双语策略名称。 |
| `summary` | 用于页头和表格的简明检测目标。 |
| `description` | 用自然段说明策略范围，以及所属 Analytic 如何分工。 |
| `detects_refs` | 至少一个 NJT/NJS 检测对象。 |
| `domains` | 至少一个 `enterprise`、`mobile` 或 `ics`。 |
| `analytic_refs` | 至少一个 NJA 对象。 |
| `evidence_refs` | 支持策略的来源，并必须覆盖关联 Analytic 使用的来源。 |
| `lifecycle` | 状态、版本、日期、贡献者和审查者。 |

每个 `analytic_ref` 必须解析为 NJA，并通过 `strategy_ref` 反向指回本 DET。Strategy 的身份由检测目标、覆盖主体、域和 Analytic 集合共同决定。

## 二、Detection Analytic

Analytic 定义实现一个 Strategy 的具体、可执行或可实施的分析方法。检测页面中的“检测分析”不得为空，也不得只重复 Strategy 的概述。

| 字段 | 含义与约束 |
|---|---|
| `schema_version` | 必须为 `2.0.0`。 |
| `type` | 必须为 `detection-analytic`。 |
| `id` | 规范 `NJA-xxxxxx`。 |
| `strategy_ref` | 唯一所属 DET，必须与 Strategy 的 `analytic_refs` 双向一致。 |
| `name` | 双语分析名称。 |
| `summary` | 简明说明分析输出或检测结果。 |
| `domains` | 适用域。 |
| `platforms` | 平台限制；只有确实平台无关或尚无法限定时才使用 `[]`。 |
| `logic` | 连贯的分析步骤、关联方式和判定逻辑。 |
| `data_requirements` | 结构化数据来源、通道与必需字段。 |
| `observables` | 分析实际消费的具体可观测信号。 |
| `correlation.window` | 必需观察时长。 |
| `correlation.dimensions` | 源、目标、时间、会话、工具指纹等机器可读关联键。 |
| `false_positives` | 可能产生相似信号的正常原因；至少一项。 |
| `blind_spots` | 遥测或逻辑失去可靠性的条件；至少一项。 |
| `tuning_guidance` | 基线、白名单、阈值和环境适配方法，同时说明如何避免消除覆盖。 |
| `evidence_refs` | 支持逻辑及数据假设的来源。 |
| `lifecycle` | 状态和审查历史。 |

### 数据要求

每项 `data_requirements` 必须包含：

- `source_type`：稳定机器短名；
- `name`：双语人类名称；
- `channel`：已知时填写具体产品或日志通道，否则为 `null`；
- `required_fields`：实现该分析所必需的规范字段名，至少一项。

只有数据源确实能够提供声明字段或可观测信号时才能列入。不得用产品名称作为 Analytic 的身份。

## 三、Mitigation

Mitigation 定义可复用的控制概念、可执行措施，以及它针对各 NJT/NJS 的具体应用。

| 字段 | 含义与约束 |
|---|---|
| `schema_version` | 必须为 `2.0.0`。 |
| `type` | 必须为 `mitigation`。 |
| `id` | 规范 `MIT-xxxxxx`。 |
| `name` | 双语控制名称。 |
| `summary` | 简明总体风险降低效果。 |
| `description` | 用自然段解释控制目的、范围和基本作用。 |
| `domains` | 适用域。 |
| `measures` | 一项或多项可实施控制措施。 |
| `applications` | 每个 NJT/NJS 应用一项，目标不得重复。 |
| `evidence_refs` | 支持来源。 |
| `lifecycle` | 状态和审查历史。 |

### Measure

- `key`：MIT 内稳定且唯一的本地短名；
- `name`：双语措施名称；
- `description`：需要实施什么；
- `control_type`：`preventive`、`exposure-reduction`、`cost-increasing`、`detective-support`、`containment` 或 `governance`。

Measure 描述可以跨技术复用的控制动作，不重复逐技术应用说明。

### Application

- `target_ref`：一个 NJT 或 NJS；
- `use`：如何对该目标实施本缓解措施；
- `expected_effect`：它改变何种痕迹、机会、成本或防守能力；
- `limitations`：无法阻止什么、在何种条件下失效或存在代价。

同一 Mitigation 内 `target_ref` 必须唯一。`applications[].target_ref` 是适用性的唯一事实源，不再维护重复的 `mitigates_refs`。

## 四、Technique/Sub-technique 防御引用

当 Technique/Sub-technique 的 `coverage: available` 时，必须引用 DET 或 MIT。被引用对象必须直接适用于当前主体；父技术也可以引用适用于其正式子技术的对象。不得仅因标题相似而建立引用。

## 五、复用与拆分

- 检测目标、主体范围、域和 Analytic 集合不变时复用 Strategy。
- 逻辑、数据要求、关联模型和调优不变时复用 Analytic。
- 控制概念与 Measure 不变时复用 Mitigation，并为新主体增加 Application。
- 数据要求、检测逻辑、控制动作或风险降低机理实质不同则拆分对象。

## 六、批量开发中的语义深度

批量候选不能共享一个只替换技术名称的通用防御实现。DET 可以复用共同检测目标，但每个 NJA 必须保留可实施且与覆盖主体一致的数据、关联和调优逻辑；MIT 可以复用控制概念，但每个 Application 必须具体说明目标行为的受控面、预期痕迹或机会变化以及目标特有限制。

固定版本 ATT&CK 页面所列 Detection Strategy 或 Mitigation 可以作为设计线索，但不会自动证明 Niji 对象中的数据字段、关联窗口、阈值、控制效果或限制。正式防御对象必须具有结论层级相匹配的来源或明确校准的推断。机器可解析和引用双向连通只是最低门禁。
