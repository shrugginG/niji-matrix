# 内容贡献规范

所有贡献必须围绕明确的研究对象，并以 [NJT-0001 规范范例](docs/njt-0001-exemplar.md)作为结构与质量基线。范例用于约束写法和对象关系，不构成其他候选的证据或数量指标。

## 强制要求

1. 不改变 `matrix.yaml` 中已固定的 ATT&CK 战术基线；基线升级单独审议。
2. 新技术内容必须有对应准入决策；`exclude` 不建立正式技术包。
3. 匿迹子技术必须由本研究独立定义，不继承 ATT&CK 子技术。
4. Technique/Sub-technique 必须遵守 [字段规范](docs/technique-field-specification.md)、Schema 2.0.0 和对应模板。
5. 父子对象共享核心阅读字段，只允许规范规定的父级或子级专有字段。
6. 子技术 ID 使用 `NJS-<父 NJT 四位号>-<三位子序号>`，并与 `parent_ref` 一致。
7. 每个正式技术或子技术至少关联一种实际成立的匿迹机理；每项机理必须具有无句末标点的 `summary`、自然因果分析、证据和置信度。
8. 正文使用成对完整自然段，不得写 Markdown 正文、手工表格、HTML、UI 布局数据、项目符号碎片或空白占位。
9. 关键事实、边界和机理判断必须可追溯到 Reference/Claim；推断和假设必须显式标注。
10. Detection Strategy、Detection Analytic 与 Mitigation 必须遵守 [防御对象规范](docs/defense-object-specification.md)。
11. ID 一经登记不得复用；废弃对象保留身份和替代关系。
12. 机器校验通过只能进入 `review`；`published` 必须记录人工领域审查。

## 共享库与并行开发

创建或扩充 REF、CLM、CASE、DET、NJA、MIT、REL 前必须查询共享库。并行研究期间只有主 Agent 可以分配正式 ID 和写入七类规范共享库；研究者只使用已确认的正式 ID 或唯一临时键，并通过 `planning/templates/technique-research-handoff.yaml` 交接。

正式写入前，主 Agent 必须把每个临时候选处理为 `reuse`、`extend`、`create`、`split` 或 `defer`。

```bash
python3 scripts/library_catalog.py
python3 scripts/library_lookup.py --text "候选名称或特征"
python3 scripts/audit_duplicates.py --fail-on exact
python3 scripts/allocate_id.py reserve NJS --parent NJT-xxxx --count <n> --owner <batch-id>
python3 scripts/allocate_id.py sync
```

## 提交与审查范围

单项技术提交必须同时包含并审查：

- 准入决策和分类来源；
- 父技术的全部必填字段；
- 完整且边界互斥的子技术分类；
- 机理因果链和证据覆盖；
- Reference、Claim 与可选 Case；
- DET→NJA 检测结构和 MIT 逐目标应用；
- 生命周期、双语等价性和研究限制；
- Bundle 与 Review Web 呈现。

多技术批次必须按照 [批次开发工作流](docs/batch-development-workflow.md)登记、分派、收敛和验收。

## 质量门禁

提交前从 `niji-matrix/` 运行：

```bash
make quality
python3 scripts/build_technique_bundle.py NJT-xxxx
python3 scripts/pipeline_status.py
python3 scripts/allocate_id.py list --status reserved
```

并从 `tool/niji-matrix-review/` 运行：

```bash
npm test
```

要求：正式内容和规划均为 0 error、0 warning；无精确重复或未决疑似重复；全部契约测试通过；Bundle 构建成功；Web API 无 issue；无未解释的 reserved ID。
