# BATCH-TA0004-001 人工可读审阅记录

## 候选准入与 taxonomy

- T1548 决议为 `adapt`，形成 `NJT-0098`；未导入任何 ATT&CK 子技术。
- 固定 19.1 基线的六项子技术已经逐项/逐簇覆盖，并完成第二轮开放搜索。
- 正式 Niji 子技术为两个：`NJS-0098-001` 受信提权中介谱系借用，`NJS-0098-002` 短寿命权限窗口激活。
- 数量不能减少：谱系图关联与权限有效区间具有不同 stable key、误报、盲区和缓解动作。数量不能增加：剩余轴要么按平台/控制名拆实现，要么仅有 hypothesis/deferred 证据。

## 字段责任与证据

- 父技术和两个子技术的 definition、stealth characteristics、scope boundary、application scenarios、attacker model、defender model 和 limitations 均与 NJT-0001 的字段责任逐项比较；没有复制其数量或正文。
- 每项正式 mechanism 都明确写出行为设计、痕迹变化、防守观察影响与匿迹效果，并有结论级 `evidence_refs`。
- ATT&CK T1548 页面只支持父行为、TA0004 映射、六项广度和 DET0345 先验；UAC、sudo、PIM、PIM audit、service-account impersonation、PPPC/TCC、Administrator Protection 与 Glupteba 各自支持更窄结论。
- Glupteba 案例只归因其 HKCU handler→CompMgmtLauncher/fodhelper→system-level child 链，不扩张到活动的其他行为。临时窗口缺少同等级活动案例，正文已明确限制。

## 共享对象决议

- References、Claims、Case、DET、NJA 与 MIT 均为 `create`；DET/NJA/MIT 相对于持久身份、一般 IPC broker 和执行选择对象为语义 `split`。
- DET-000095 双向引用 NJA-000072 与 NJA-000073。前者实现宿主 requester—control—intermediary—outcome 谱系，后者实现临时权限 interval。
- MIT-000096 为 NJT-0098 和两个 NJS 分别提供 `use`、`expected_effect` 与 `limitations`；没有替换名称式 application。
- Relationships 为 `defer`，因为当前边界不需要额外有向语义。

## 机器、Bundle 与 Web QA

- `make quality`：1331 个对象，0 errors，0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础设施测试通过。
- Bundle：`dist/techniques/NJT-0098.json` 构建成功。
- `pipeline_status.py`：TA0004 为 13 项完整 inventory、1 项 decision、1 个 technique、2 个 subtechnique，gap 仍为 pending。
- reserved ID：0。
- `tool/niji-matrix-review` 的 `npm test`：58/58 通过。
- headless Chrome 从 Review Web live API 实际渲染父技术、两个子技术、DET、两个 NJA 和 MIT，并切换 zh/en，共检查 14 页；标题、核心段落、生命周期与父/子/DET/NJA/MIT/CASE 必要链接均无缺失。

## 状态

本批次为 `review`，尚无人工领域审查者，不得设为 `published`。前五候选总体进度为 1/5；TA0004 其余父候选、Niji-native gap、跨技术收敛与人工审查均未完成，战术未关闭。
