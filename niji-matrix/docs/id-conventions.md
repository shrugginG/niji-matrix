# ID 与路径规范

本文与[字段规范](technique-field-specification.md)及 [NJT-0001 范例](njt-0001-exemplar.md)共同约束对象身份。历史全局连续式 NJS 编号只保留在迁移归档中，不得重新用于正式内容。

## ID

| 对象 | 格式 | 示例 |
|---|---|---|
| 战术 | 继承 ATT&CK ID | `TA0043` |
| 技术准入决策 | `DEC-<TACTIC>-<CANDIDATE>` | `DEC-TA0043-T1595` |
| 匿迹技术 | `NJT-` 加四位全局序号 | `NJT-0001` |
| 匿迹子技术 | `NJS-<父 NJT 四位号>-<三位子序号>` | `NJS-0001-001` |
| 匿迹机理 | `NM-` 加固定短码 | `NM-ST` |
| 参考来源 | `REF-` 加六位序号 | `REF-000001` |
| 主张 | `CLM-` 加六位序号 | `CLM-000001` |
| 案例 | `CASE-` 加六位序号 | `CASE-000001` |
| 检测策略 | `DET-` 加六位序号 | `DET-000001` |
| 检测分析 | `NJA-` 加六位序号 | `NJA-000001` |
| 缓解措施 | `MIT-` 加六位序号 | `MIT-000001` |
| 关系 | `REL-` 加六位序号 | `REL-000001` |

匿迹技术采用矩阵级 NJT ID。匿迹子技术采用父级自包含 ID：中间四位必须等于父 NJT 的四位号，末尾三位在该父技术内顺序分配。ATT&CK ID 只能记录在来源字段中，不能作为 Niji Matrix 主键。

## 路径

目录采用 `<ID>-<英文短名>`：

```text
TA0043-reconnaissance/
NJT-0001-active-scanning/
NJS-0001-001-temporal-dilution-scanning/
```

英文短名用于人类阅读，不参与对象身份判断。重命名目录不会改变对象 ID。

## 稳定性

- 已发布 ID 永不复用。
- 并行开发前由主 Agent集中预留 ID；NJS 必须使用 `scripts/allocate_id.py reserve NJS --parent NJT-xxxx`，Sub-agent 不得自行编号。
- 正式对象写入后将预留状态更新为 `consumed`；未使用且尚未形成对象的预留可以标记为 `released`，但为保留审计轨迹不会重新分配。
- `planning/id-reservations.yaml` 是并发协调记录，不是发布知识对象。
- 一批正式对象写入后可以运行 `scripts/allocate_id.py sync`，批量将对应预留标记为 `consumed`。
- 对象废弃时保留原文件，设置 `lifecycle.status: deprecated`。
- 对象合并或替代时，使用 relationship 保存指向，不覆盖历史对象。
- 子技术的 ID 父级段必须与 `parent_ref` 一致，但 `parent_ref` 仍是正式父子关系来源；不得只依赖字符串截取建立关系。
