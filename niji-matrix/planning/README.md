# 研究开发规划层

`planning/` 保存矩阵开发过程中的批次、候选、ID 预留、重复项决议和研究交接，不属于网站发布知识对象。

```text
planning/
├── id-reservations.yaml       # 主 Agent 管理的正式 ID 预留
├── duplicate-resolutions.yaml # 已审查的语义相似项决议
├── schemas/                   # 规划对象 Schema
├── templates/                 # brief、handoff 和 integration summary
├── tactics/                   # 各战术持续开发计划
├── runs/                      # 批次暂存区
└── archives/                  # 迁移与归档清单
```

## 规则

- 正式知识内容写入 `matrix/` 与七类共享库：`references/`、`claims/`、`cases/`、`detections/`、`analytics/`、`mitigations/`、`relationships/`。
- Sub-agent 只在 `runs/<batch-id>/` 的独立路径提交研究交接，不分配正式 ID，不修改规范矩阵或共享库。
- 主 Agent 负责准入收敛、共享库判重、父级自包含 NJS 编号、正式写入和质量门禁。
- 规划对象和临时键不得被正式 Technique、Sub-technique 或共享对象引用。
- NJT-0001 是正式内容范例；规划材料不能覆盖其字段规范，也不能把旧批次产量当作新批次数量目标。

## 启动

1. 运行 `make quality`、`pipeline_status.py` 和 reserved ID 查询。
2. 在 `planning/tactics/<TA-ID>.yaml` 登记 batch 与 work item。
3. 从 `batch-brief.md` 模板建立候选、相邻对象和共享库边界。
4. 将批次设为 `active`、工作项设为 `researching`。
5. 生成共享库目录后再开展研究。
6. 研究者必须阅读 [字段规范](../docs/technique-field-specification.md)、[防御对象规范](../docs/defense-object-specification.md)和 [NJT-0001 范例](../docs/njt-0001-exemplar.md)。

## 收尾

1. 从 `batch-integration-summary.yaml` 记录决策、ID、共享对象处置和质量结果。
2. 执行 `allocate_id.py sync`，确认没有未解释的 reserved ID。
3. 将工作项设置为 `excluded`、`review` 或 `published`。
4. 机器校验完成只能进入 `review`，不能替代人工领域审查。
5. 战术候选未处理完时，`candidate_inventory.status` 必须保持 `partial`。

详细流程见 [批次开发工作流](../docs/batch-development-workflow.md)。
