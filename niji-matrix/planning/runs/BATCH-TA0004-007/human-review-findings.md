# BATCH-TA0004-007 人工可读审阅记录

## 候选准入与权限结果

- T1484 独立决议为 adapt，新建 NJT-0100“集中策略与信任状态篡改”。直接对象是权威 policy/trust object 的完整版本、作用域和 consumer 语义，不是下游任务、服务、进程或 token 名称。确认链为 lower writer/pre-state → exact object/version → scope/propagation/evaluation → principal/session/token → positive authorization delta → first newly authorized operation。
- GPO applied、trust established、Domain/Global Admin 名称、privileged token 字符串和防御被关闭都不能替代权限结果。只削弱防御的 policy 保留 Defense Impairment；计划任务、服务或载荷执行转交各自 owner。

## Taxonomy breadth

- 固定两项 T1484.001 Group Policy Modification 与 T1484.002 Trust Modification 已逐项覆盖，均作为实现而未导入/翻译。开放搜索检查 existing-object semantic mutation、narrow scope、propagation、direct/transitive trust、approved workflow、precedence/inheritance、one-to-many fanout、post-use reversion、name/metadata 与 platform/medium/field/target。
- 最终正式 Niji 子技术为 1：NJS-0100-001“用后策略状态回退”。不能减少：其 stable key 是同一对象 pre-state—malicious version—restored version 的有界区间，current snapshot 可正常但 consumer/token/session/side effect 仍需追踪，检测和恢复明显不同。不能增加：其他轴已分别收敛为 parent-core、NJT-0093/NJT-0083 adjacent、deferred 或 rejected，没有第二个兼具稳定控制键、独立痕迹/观察、结论证据与防御 owner 的轴。
- 子项 confidence 为 medium，case_refs 为空。ATT&CK 明确支持临时 modify—act—revert，但没有公开完整实战链；未用父页或 Solorigate/GPO 案例越级证明回退。

## 字段、证据与防御对象

- 逐字段对照 NJT-0001 后，definition 回答直接对象和战术结果，stealth characteristics 回答痕迹/观察/残余/限制，scope 同时处理纳入、排除、反例与相邻 owner；application scenarios 分开 GPO 与 federation，但威胁模型以能力、反馈、版本/复制和保留可见性为中心，不按平台复制模板；research limitations 明确父页、两案例、审计缺口和重开 taxonomy 的条件。
- NJT/NJS 的 NM-BT、NM-ST 均显式形成行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果，并只引用主体 reference_refs 中的结论级 evidence；中英文逐段范围、结论强度、confidence 和限制一致。
- 七库决议：reuse REF-000304；extend CASE-000111；create REF-000338..344、CLM-000548..551、CASE-000126、DET-000097、NJA-000077、MIT-000098；split authentication-specific DET-000073/NJA-000052/MIT-000073 与通用 authoritative-policy owner；REL defer。CASE-000126 只证明集中 GPO fanout，不证明提权/回退；CASE-000111 明确缺少完整权限差。
- DET-000097 ↔ NJA-000077 双向引用并分级输出 policy_state_anomaly、consumer_adoption、authority_unresolved、elevation_confirmed、post_use_reversion、restored_state_with_residual_authority。MIT-000098 为 NJT-0100 与 NJS-0100-001 分别提供 use、expected_effect、limitations，恢复必须延伸到 token/session、endpoint authority 与 resource side effects。

## 门禁与状态

- `make quality`：1393 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 340 References、429 Claims、101 Cases、68 DET、71 NJA、66 MIT、0 REL。
- `dist/techniques/NJT-0100.json` 已构建；pipeline 为 TA0004 inventory 13、decision 7、technique 7、subtechnique 16、gap pending；reserved ID 为 0。
- Review Web `npm test` 61/61；Headless Chrome 实际渲染父、子、DET/NJA/MIT 的 zh/en 共 10 页，标题、章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 正式对象 lifecycle.status 为 review，尚无人工领域 reviewer。总体进度 7/13；BATCH-TA0004-008 可进入 T1611 研究，TA0004 仍 active，Niji-native gap、跨技术收敛与人工领域审查均未完成。

