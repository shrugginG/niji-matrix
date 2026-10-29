# 内容架构

## 1. 三层知识结构

```text
ATT&CK 战术
└── Niji Technique
    └── Niji Evasion Sub-technique
```

战术层继承 `matrix.yaml` 固定版本的 ATT&CK Enterprise 战术。技术候选按父技术进行 `retain`、`adapt`、`exclude` 或 `add` 准入；被排除候选只保留决策，不建立正式技术包。

匿迹子技术是 Niji Matrix 原生对象，回答“父技术通过哪一种稳定匿迹变量改变痕迹及防守观察”。它不继承 ATT&CK 子技术。编号为 `NJS-<父 NJT 四位号>-<三位子序号>`，但显式 `parent_ref` 仍是关系权威来源。

## 2. 统一字段合同

Technique 与 Sub-technique 共享一套固定阅读字段：

```text
身份
定义与概念
匿迹特性分析
范围边界界定
应用场景与威胁模型
  ├── 应用场景
  └── 威胁模型
      ├── 攻击者模型
      └── 防守方模型
匿迹机理
检测与缓解引用
证据
研究限制
生命周期
```

父技术另有 `classification` 与 `subtechnique_taxonomy`；子技术另有 `parent_ref` 与 `lineage`。字段责任详见[字段规范](technique-field-specification.md)，现行结构与写作基线见 [NJT-0001 范例](njt-0001-exemplar.md)。

结构化不等于碎片化：普通说明使用成对完整自然段；需要查询、复用和生成表格的机理、子技术、防御、证据与生命周期使用结构化对象。技术目录禁止 Markdown 正文和展示定义。

## 3. 四种匿迹机理

- `NM-DO`：数据遮蔽；
- `NM-BT`：行为透明；
- `NM-FD`：特征伪装；
- `NM-ST`：时空释痕。

正式对象只记录确实成立的机理。每个映射保存角色、无句末标点的 `summary`、自然因果分析、证据和置信度。未采纳机理只属于研究交接或评审记录。

## 4. 证据与防御图

```text
Reference ─supports→ Claim
Claim ─justifies→ Technique / Sub-technique / mechanism
Case ─demonstrates→ Technique / Sub-technique

Technique / Sub-technique ─references→ Detection Strategy (DET)
Detection Strategy ─contains→ Detection Analytic (NJA)
Detection Strategy ─detects→ Technique / Sub-technique

Technique / Sub-technique ─references→ Mitigation (MIT)
Mitigation ─defines→ Measure
Mitigation Application ─targets→ Technique / Sub-technique
```

DET 定义检测目标与对象，NJA 保存可实施分析和数据要求；MIT 保存可复用控制措施，并通过逐目标 Application 描述用法、预期效果和限制。详细合同见[防御对象规范](defense-object-specification.md)。

## 5. 四个层次的真相源

| 层次 | 职责 | 是否发布 |
|---|---|---|
| `matrix/` 与七类共享库 | 规范研究内容和对象关系 | 是 |
| `planning/` | 批次、交接、ID 预留、重复项决议 | 否 |
| `schemas/`、`templates/`、规范文档 | 可执行形状与作者约束 | 否 |
| `dist/` | 从规范 YAML 构建的消费数据 | 是，禁止手改 |

网站和 Review Web 是消费端，不得成为第二内容源，也不得以自由页面逻辑弥补字段缺失。

## 6. 质量与生命周期

`make quality` 联合执行 Schema、语义引用、规划、重复项与契约测试。Bundle 构建检查对象聚合，Review Web 检查固定板块与跨对象呈现。

开发状态和发布状态分离：

- batch `active`：研究进行中；
- batch/Technique `review`：内容完整、机器通过并完成 Web QA，等待人工审查；
- `published`：人工领域审查已记录；
- `deprecated`：身份保留但不再作为当前分类。

完整流程见[批次开发工作流](batch-development-workflow.md)。
