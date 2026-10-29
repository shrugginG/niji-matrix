# 匿迹技术与匿迹子技术字段规范

本文是所有正式 `technique` 与 `evasion-subtechnique` 的权威字段规范。JSON Schema 约束数据形状，本文约束字段含义、内容责任、写作质量、对象归属和审查要求。[NJT-0001 主动扫描](../matrix/tactics/TA0043-reconnaissance/techniques/NJT-0001-active-scanning/technique.yaml)及其子技术是结构范例。

## 规范用语

- “必须”表示 Schema 或审查不可豁免的要求。
- “不得”表示正式内容中禁止出现的做法。
- “应当”表示默认要求；偏离时必须在评审记录中说明理由。
- “可以”表示按研究对象实际情况选择。

## 一、共同约定

### 1. 双语值

所有面向读者的内容必须在同一个对象中成对保存中文与英文：

```yaml
zh: 中文内容
en: English content
```

自然段按段落逐项配对。中英文必须表达相同的范围、结论强度、置信度和限制，不得出现一方缩写、遗漏或把推断强化为事实。

### 2. 自然段板块

叙述板块使用固定形状：

```yaml
paragraphs:
  - zh: 一段完整、自然、可以连续阅读的中文论述。
    en: A complete and coherent English paragraph.
```

每个板块必须包含一至四段。每一项必须是完整自然段，不得是标题、标签、句子碎片、项目符号、编号列表、Markdown 表格、HTML 或 UI 指令。分段依据论证和可读性，不依据“一个变量拆一个字段”。

### 3. 内容充分性与反模板化

一至四段是 Schema 允许的结构范围，不表示所有字段都应压缩为一段，也不表示必须复制 NJT-0001 的段落数或字数。每个板块必须完整回答本规范为该字段列出的全部问题；当定义、工作过程、范围反例、威胁假设或证据限制无法在一段中自然展开时，应按论证关系分段。

跨候选统一使用一段式结构、完全相同的研究限制、通用攻防模型，或只替换技术名称和痕迹名的机理分析，均视为内容审查警报。只有语义确实相同且评审记录说明原因时才可复用表述。脚本可以序列化已审阅内容和执行机械更新，但不得代替候选级研究并批量生成正式读者正文。

### 4. ID 与引用

- 父技术：`NJT-xxxx`。
- 子技术：`NJS-xxxx-yyy`；`xxxx` 必须等于父 NJT 四位序号，`yyy` 是该父技术内三位子序号。
- `parent_ref` 是父子关系的权威来源，同时必须与子技术 ID 中的父级段一致。
- 所有正式引用必须解析到规定类型的对象。
- 正式 ID 只能由主 Agent 通过分配器生成，研究者不得自行编造。

## 二、父技术与子技术共同顶层字段

以下字段在父技术和子技术中全部必填。

| 字段 | 类型 | 含义与约束 |
|---|---|---|
| `schema_version` | 字符串 | 必须为 `2.0.0`。 |
| `type` | 枚举 | 父技术为 `technique`；子技术为 `evasion-subtechnique`。 |
| `id` | 稳定 ID | 必须符合对象类型及父级自包含编号规则。 |
| `name` | 双语短名称 | 稳定的读者名称；除非对象本身就是工具专属概念，不以工具名代替技术边界。 |
| `summary` | 双语短文本 | 页头简介，概括对象做什么以及其匿迹意义。 |
| `aliases` | 字符串数组 | 只保存已确立的别名；没有则为 `[]`。 |
| `definition_and_concept` | 自然段板块 | 基础定义、直接行为、直接目的与概念含义。 |
| `stealth_characteristics` | 自然段板块 | 当前对象具体具备哪些匿迹特性，以及为何增加识别、关联、区分或归因难度。 |
| `scope_boundary_definition` | 自然段板块 | 纳入、排除、判定标准、正常相似行为和相邻对象边界。 |
| `application_scenarios_and_threat_model` | 结构对象 | 应用场景，以及显式分开的攻击者模型和防守方模型。 |
| `stealth_mechanisms` | 结构数组 | 当前对象实际成立的机理；至少一项。 |
| `defense` | 结构对象 | Detection Strategy 和 Mitigation 的覆盖状态与引用。 |
| `evidence` | 结构对象 | Claim、Case 与 Reference 引用。 |
| `research.limitations` | 自然段板块 | 证据缺口、正常相似行为、推断限制和置信度变化条件。 |
| `lifecycle` | 结构对象 | 状态、语义版本、日期、贡献者和审查者。 |

## 三、定义与概念

`definition_and_concept` 必须回答：

1. 这是什么行为；
2. 它的直接目标是什么；
3. 它如何服务于所在战术或父技术；
4. 它与工具、数据类型、介质或偶然条件有何区别。

这里可以自然提到匿迹，但不得替代专门的匿迹特性分析，也不得写成范围规则列表或四机理逐项分析。NJT-0001 使用两个连续自然段：第一段定义主动交互和目的，第二段固定“主动探测”这一概念边界。

## 四、匿迹特性分析

`stealth_characteristics` 必须说明：

1. 哪些痕迹属性被改变；
2. 防守方的哪些判断因此更困难；
3. 仍然残留哪些可观察痕迹；
4. 哪些条件会限制匿迹效果。

本字段描述对象自身特性，不需要反复罗列四机理术语。父技术应自然点出技术名称；子技术的第一段必须直接以当前子技术准确的中文和英文名称开头，不得使用“本子技术的主要匿迹特性是”等模板句。

## 五、范围边界界定

本字段必须用自然段同时界定纳入行为、排除行为和相邻对象。应当明确区分攻击者有意控制的匿迹变量与拥塞、配置、合法运维、兼容性行为、测量活动等正常原因造成的相似现象。

介质、产品、字段类别、目标类型或工具名称本身不得成为子技术边界，除非它确实代表独立且稳定的匿迹变量，并造成可论证的防守观察差异。

## 六、应用场景与威胁模型

固定结构如下：

```yaml
application_scenarios_and_threat_model:
  application_scenarios:
    paragraphs: [...]
  threat_model:
    attacker_model:
      paragraphs: [...]
    defender_model:
      paragraphs: [...]
```

### 应用场景

必须说明攻击者在什么攻击阶段、环境、目标条件和操作触发下使用当前对象，以及它服务于何种后续目的。它回答“什么时候、在哪里、为什么使用”，不重复定义。

### 攻击者模型

必须说明实现当前对象所需的前提与能力。按对象实际情况覆盖访问条件、资源、知识、反馈、时间容忍度、协同、报文或应用控制能力和操作限制。不得为了让一个子技术看似成立而凭空假定能力。

### 防守方模型

必须说明匿迹结论所针对的观察模型，包括传感器、遥测、保留时间、规范化、关联范围、基线、残余痕迹和盲区。本字段描述防守方“能够看到什么”，不得写成具体检测步骤。

## 七、匿迹机理

每项 `stealth_mechanisms` 包含：

| 字段 | 含义与约束 |
|---|---|
| `mechanism_ref` | 指向一个规范 `NM-*`；同一主体内不得重复。 |
| `role` | `primary` 表示主导机理，`secondary` 表示真实但次要的机理。 |
| `summary` | 用于表格的双语短说明；字段名保持 `summary`，中英文结尾均不得有句号等句末标点。 |
| `analysis` | 用完整自然段解释行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果。 |
| `evidence_refs` | 至少一个支持来源，且必须同时出现在主体 `evidence.reference_refs`。 |
| `confidence` | `hypothesis`、`low`、`medium` 或 `high`，按证据校准。 |

正式 Technique/Sub-technique 只记录已成立的机理。未采纳或证据不足的机理只能进入研究交接、集成摘要或评审记录，不得保存为 `unmapped_mechanisms`。

## 八、检测与缓解引用

固定结构示例：

```yaml
defense:
  detections:
    coverage: available
    strategy_refs: [DET-000001]
  mitigations:
    coverage: available
    mitigation_refs: [MIT-000001]
```

`coverage` 只能是 `available`、`not-applicable` 或 `deferred`。

- `available` 必须包含至少一个正确类型的引用。
- `not-applicable` 与 `deferred` 必须使用空引用数组，并提供双语自然段 `rationale`。
- 父技术可以汇总直接适用于自身或其正式子技术的 Strategy/Mitigation。
- 子技术引用的防御对象必须直接适用于该子技术。

DET、NJA 和 MIT 的详细字段见[检测与缓解对象规范](defense-object-specification.md)。

## 九、证据

- `claim_refs`：至少一项原子结论，用于支持准入相关性、边界、机理、子技术成立性、检测、缓解或其他重要判断。
- `case_refs`：零项或多项已记录活动案例；没有合格案例时保持空数组，不为填字段而制造案例。
- `reference_refs`：主体直接依赖的全部来源，必须覆盖每项机理使用的来源。

固定版本 ATT&CK 父页面用于锚定父行为和战术映射，不自动证明新提出的 Niji 子技术、匿迹机理、检测数据假设、缓解效果或案例归因。每项实质边界、机理和子技术成立性必须有结论层级相匹配的证据；证据只能支持父行为时，应降低置信度、标记 hypothesis 或 defer，而不是用扩写补足证据。

案例证明范围不得超过来源。来源只证明攻击者使用了父级行为时，不得把它升级成某个具体子技术的证据。

## 十、生命周期

- `draft`：仍在编写或存在未解决集成问题。
- `review`：Schema、候选级内容深度审查、语义校验、测试、Bundle 和 Web QA 已通过，等待人工领域审查。
- `published`：已经人工领域审查，至少有一名 reviewer。
- `deprecated`：保留历史身份，但不再作为当前分类使用。

`version` 使用 `major.minor.patch`；`created` 和 `modified` 使用 ISO 日期；contributors 记录作者，reviewers 记录人工领域审查者。人工审查发现系统性浅薄、证据越级或模板化正文时，相关对象应退回 `draft`，修订并重新通过全部门禁后方可恢复 `review`。

## 十一、父技术专有字段

### classification

`classification.tactic_refs` 保存所属战术。`classification.origin` 记录 `attack-retained`、`attack-adapted` 或 `niji-added` 及固定 ATT&CK 来源。`classification.decision_ref` 必须解析到反向指向本 NJT 且结论一致的准入决策。

### subtechnique_taxonomy

`subtechnique_taxonomy.narrative` 说明子技术划分变量、兄弟项覆盖、禁止使用的分类基础以及为何这些子技术共同构成稳定分类。ATT&CK 派生父技术还必须在批次规划材料中记录固定基线 ATT&CK 子技术数量、维度与覆盖决议，并按 niji-matrix-authoring 的 taxonomy breadth control 完成触发的第二轮审查；这些 ATT&CK 对照信息属于研究元数据，不写入正式 Technique YAML。ATT&CK 数量可以提高研究广度要求，但不得成为正式 Niji 子技术的最低数、目标数或比例。

`coverage` 只能是：

- `established`：必须存在至少一个子技术引用；
- `none-justified`：研究后确认没有稳定子技术划分；
- `deferred`：可能存在划分，但证据或边界尚不足。

子技术引用必须唯一、父子双向一致并符合父级自包含编号。

## 十二、子技术专有字段

`parent_ref` 指向唯一 NJT 父技术。`lineage.attck_subtechnique_inherited` 必须为 `false`。子技术通过父级继承战术语境，不重复保存父级 `classification`，也不得继续定义下一层后代。

## 十三、规范字段顺序

为便于人工审查，正式文件应与模板保持相同顺序：

1. 身份；
2. 父级的 classification，或子级的 parent/lineage；
3. 定义与概念；
4. 匿迹特性分析；
5. 范围边界界定；
6. 应用场景与威胁模型；
7. 匿迹机理；
8. 父级子技术分类；
9. 检测与缓解；
10. 证据；
11. 研究限制；
12. 生命周期。
