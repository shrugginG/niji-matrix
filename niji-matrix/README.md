# 匿迹技战术矩阵（Niji Matrix）

本项目是匿迹技战术矩阵的规范化内容源，用于规划、研究、编写、审查和维护战术、匿迹技术、匿迹子技术及其证据与防御对象。未来矩阵系统必须以本仓库中通过校验与审查的 YAML 为唯一内容源，不得从页面布局或 Markdown 正文反向定义知识对象。

## 核心层级

```text
ATT&CK 战术（原样继承，固定基线版本）
└── 匿迹技术（对 ATT&CK 父技术逐项保留、调整、舍弃，并允许新增）
    └── 匿迹子技术（Niji Matrix 原生分类，不继承 ATT&CK 子技术）
```

四种匿迹机理——数据遮蔽、行为透明、特征伪装、时空释痕——是技术层的规范分析维度。正式技术或子技术只记录在当前对象上确实成立且具有证据的机理。

## 权威规范与范例

后续开发必须同时遵循以下规范：

- [单个技术与子技术字段规范](docs/technique-field-specification.md)：字段语义、写法、双语要求、父子差异和审查约束；
- [检测与缓解对象规范](docs/defense-object-specification.md)：Detection Strategy、Detection Analytic 与 Mitigation 的职责和连接规则；
- [NJT-0001 规范范例](docs/njt-0001-exemplar.md)：现行结构与写作质量基线；
- [单技术编写指南](docs/authoring-guide.md)与[审查清单](docs/review-checklist.md)；
- [批次开发工作流](docs/batch-development-workflow.md)。

NJT-0001“主动扫描”是结构与质量范例。新对象应复用它的字段职责、自然段风格、父子边界方法和防御对象组织方式，但不得复制它的结论、证据、机理数量或子技术数量。

## 目录

```text
niji-matrix/
├── matrix.yaml                 # 矩阵清单、ATT&CK 基线和层级政策
├── matrix/tactics/             # 战术 → 技术 → 匿迹子技术
├── mechanisms/                 # 四种匿迹机理规范定义
├── references/                # 来源
├── claims/                    # 可独立审查的研究主张
├── cases/                     # 过程案例
├── detections/                # Detection Strategy
├── analytics/                 # Detection Analytic
├── mitigations/               # 缓解措施及逐目标应用
├── relationships/             # 跨对象关系
├── planning/                  # 批次、ID 预留和研究交接
├── schemas/                   # JSON Schema
├── templates/                 # 规范对象模板
├── docs/                      # 编写、编号、审查与架构规范
├── scripts/                   # 校验、构建、查重和 ID 工具
└── dist/                      # 生成数据，不手工编辑
```

技术包采用固定路径和 YAML-only 结构：

```text
TAxxxx-tactic-name/
├── tactic.yaml
├── decisions/
└── techniques/
    └── NJT-xxxx-technique-name/
        ├── technique.yaml
        └── subtechniques/
            └── NJS-xxxx-yyy-subtechnique-name/
                └── subtechnique.yaml
```

子技术编号中的 `xxxx` 必须等于父技术 NJT 的四位序号；`yyy` 是父技术内的三位子序号。显式 `parent_ref` 仍是父子关系的唯一权威来源。

## YAML-only 2.0 内容契约

Technique 与 Evasion Sub-technique 使用 Schema 2.0.0，并共享定义与概念、匿迹特性分析、范围边界界定、应用场景与攻防威胁模型、匿迹机理、防御、证据、研究限制和生命周期等核心字段。父技术另有分类和子技术分类法；子技术另有父引用和非继承谱系。

正文板块使用一至四段中英文配对的完整自然段。禁止 Markdown 正文、Markdown 表格、HTML、UI 布局字段、句子碎片和为页面卡片而拆出的微型字段。机理、子技术、Strategy、Analytic、Mitigation、Claim、Case 和 Reference 使用结构化对象及 ID 关系，由消费端生成表格和导航。

检测严格区分：

```text
Technique/Sub-technique → Detection Strategy (DET)
Detection Strategy      → Detection Analytic (NJA)
Technique/Sub-technique → Mitigation (MIT) → per-target application
```

Strategy 定义检测目标与适用对象；Analytic 定义可实施的逻辑、数据字段、可观测信号、关联、误报、盲区和调优；Mitigation 将可复用措施与逐目标应用分开。

## 开发一项技术

1. 读取 `matrix.yaml`、战术计划、相邻技术边界和共享库。
2. 在 `decisions/` 完成 `retain`、`adapt`、`exclude` 或 `add` 准入判断。
3. 只有非 `exclude` 候选才能分配 NJT/NJS 并建立正式包。
4. 严格按字段规范和模板写父技术；从匿迹变量、痕迹变化和防守观察影响独立提出子技术。
5. 查询并复用七类共享库：Reference、Claim、Case、Detection Strategy、Detection Analytic、Mitigation 与 Relationship。
6. 由主 Agent 统一分配正式 ID；并行研究只使用已确认 ID 或临时键。
7. 运行完整质量门禁、构建 Bundle，并在 Review Web 中检查中英文固定栏目。

项目级技能调用方式：

    使用 $niji-matrix-authoring，按照 NJT-0001 范例和字段规范开发指定候选。

## 常用命令

从本目录运行：

```bash
make quality
python3 scripts/library_catalog.py
python3 scripts/library_lookup.py --text "候选名称或特征"
python3 scripts/allocate_id.py reserve NJS --parent NJT-xxxx --count 1 --owner <batch-id>
python3 scripts/allocate_id.py sync
python3 scripts/build_technique_bundle.py NJT-xxxx
python3 scripts/pipeline_status.py
python3 scripts/allocate_id.py list --status reserved
```

`make quality` 必须达到正式内容、规划、重复项与契约测试全部通过。机器校验通过只允许对象进入 `review`；只有人工领域审查完成后才能标记 `published`。

NJT-0001 的聚合构建示例：

```bash
python3 scripts/build_technique_bundle.py NJT-0001
```

输出为 `dist/techniques/NJT-0001.json`，该文件由脚本生成，不应手工编辑。

Review Web 位于 `../tool/niji-matrix-review/`，直接读取规范 YAML，不保存另一份内容源。

## 内容边界

- `matrix/` 与七类共享库是人工维护的规范知识源。
- `planning/` 是开发协调层，不能被正式对象引用。
- `dist/` 是生成数据，不接受人工修改。
- ATT&CK 数据只用于战术基线、父技术候选清单和来源追溯。
- 网站和审阅工具只能消费已通过契约校验的内容，不能用页面差异反向容忍字段漂移。
