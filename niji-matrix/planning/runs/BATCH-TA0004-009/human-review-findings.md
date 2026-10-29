# BATCH-TA0004-009 人工可读审阅记录

## 候选准入与权限结果

- T1546 独立决议为 retain，通过新增 DEC-TA0004-T1546 跨战术复用 NJT-0090“持久事件触发注册”及两个既有 NJS；没有复制技术或增加 taxonomy 对象。TA0004 结论链固定为 writer/caller pre-state → exact registration object/version → predicate match → Broker/consumer effective context → positive authority difference → first newly authorized result。
- ATT&CK 的 higher-permission proxy、root/SYSTEM 标签、WmiPrvSE、trusted parent 或 action launch 均不足以单独证明提权。CASE-000115 只保留持久注册与来源分离结论，因为公开材料没有 writer pre-state、actual consumer token 和 first newly authorized result。

## Taxonomy breadth

- 固定 ATT&CK 19.1 的十八项子技术均以 ID、英文名、行为维度和逐项 disposition 记录；第二遍检查还覆盖 authority distance、registration-to-activation separation、post-use reversion、action indirection、state shape、cadence/fanout 和分类外维度。
- 最终正式 Niji 子技术仍为 2：NJS-0090-001 控制 candidate/match set 与时间密度；NJS-0090-002 控制 result-side visible initiator 与 provenance break。不能减少，因为二者痕迹、关联主键和防御动作不同；不能增加，因为权限差属于父级成功门，回退和跨 host 范围缺结论级证据，加载/脚本/启动/服务/scheduler 有相邻 owner，平台、产品、路径、工具和字段分区没有稳定匿迹边界。
- 十八项 ATT&CK 子项没有被导入或改名为 Niji 子项；它们只是广度先验和覆盖检查输入。

## 字段、证据与防御对象

- 逐字段对照 NJT-0001 后，NJT-0090 与两个子项都新增了 TA0004 的权限适用性、边界、场景、攻击者/防守者模型和限制。Broker 子项的新增 mechanism 明确行为设计 → consumer-side authority/provenance 痕迹变化 → 局部观察无法归回 registrant → 来源遮蔽效果，并以 Microsoft 与 ATT&CK 结论级材料校准。
- 七库决议：reuse 既有 references/claims/CASE-000115；create REF-000353..354 和 CLM-000557..558；extend DET-000070、NJA-000049、MIT-000069；split 无；REL defer。新证据直接锚定 WMI permanent subscription security、CreatorSID 与 LocalSystem consumer，而不把单一 WMI 实现泛化为全部 T1546。
- DET-000070 ↔ NJA-000049 仍双向引用，新增 `persistence_confirmed`、`authority_unresolved`、`elevation_confirmed` 和 `dual_result_confirmed` 等显式输出；MIT-000069 的三个 target application 均独立补充 authority confinement、expected effect 和 limitations。

## 门禁与状态

- `make quality`：1421 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 350 References、436 Claims、103 Cases、69 DET、73 NJA、67 MIT、0 REL。
- `dist/techniques/NJT-0090.json` 已构建；pipeline 为 TA0004 inventory 13、decision 9、technique 9、subtechnique 20、gap pending；reserved ID 为 0。
- Review Web `npm test` 63/63；Headless Chrome 实际渲染父、两个子项、DET、NJA、MIT 的 zh/en 共 12 页，标题、章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 正式对象 lifecycle.status 为 review，尚无人工领域 reviewer。总体进度 9/13；BATCH-TA0004-010 可进入 T1068 研究，TA0004 仍 active，Niji-native gap、跨技术收敛与人工领域审查均未完成。
