# BATCH-TA0004-013 人工可读审阅记录

## 候选准入与权限结果

- T1078 独立决议为 retain；TA0004 复用并扩展 NJT-0061“匿迹化有效身份使用”及两个既有 NJS，并新增 NJS-0061-003，不复制父技术或改写原 DEC-TA0001-T1078 lineage。父级 TA0004 链固定为攻击者已控低权前态 → 未修改的精确有效凭据/会话 → accepted authentication/continuation → 实际 result principal/session/token 与事件时授权 → 正权限差 → 首个攻击者资源操作 → expected-deny/observed-allow。
- 成功登录、凭据持有、admin/root/Global Administrator 标签、Windows 4672、异常来源或一次高权 API 均不足。未认证外部者取得首个立足点只属于 Initial Access；相同有效权限的身份切换明确输出 same_authority_use；缺 controller、前态或事件时授权快照则保持 authority_unresolved。

## Taxonomy breadth

- Enterprise ATT&CK 19.1 的四项子技术已逐项覆盖：Default、Domain、Local 与 Cloud Accounts 都是 parent-core 实现范围，不导入或改名为 Niji 子技术。开放与第二轮搜索还检查角色贴合操作、低速/业务时段、凭据或会话取得、账户/认证器/权限变更、runtime token、认证因子，以及平台、协议、产品、目标和字段分区。
- 最终正式 Niji 子技术数为 3：保留 NJS-0061-001“情境贴合的身份登录”和 NJS-0061-002“既有认证会话续用”，新增 medium-confidence NJS-0061-003“低反馈身份选择”。不能减少，因为三轴分别改变新登录风险特征、认证事件密度与所有者/交互反馈，并需要不同检测数据和缓解；不能增加，因为角色贴合缺独立结论证据，低速仍是假设，权限差是父级门，其他候选有相邻 owner 或只是机械分区。

## 字段、证据与防御对象

- 父与三子均形成独立 definition、scope、scenario、attacker/defender model、机制因果链和 limitations。低反馈轴的官方资料能证明休眠敏感用户、stale service account 与缺少交互监控的高权服务身份带来专门风险和治理差异，但不能揭示每次攻击者选择意图，因此正式保留而将机制置信度校准为 medium。
- 七库决议：reuse REF-000094、067、070、111、112、147、327 与 CLM-000222/223/246；create DEC-TA0004-T1078、REF-000376–382、CLM-000575–577、NJS-0061-003；extend NJT-0061、两个既有 NJS、CASE-000121、DET-000053、NJA-000027、MIT-000052；split 无；CASE-000043 与 REL defer。Storm-0501 仅作混合权限路径参考，不因缺少事件级前态和首个授权差而升级为本地 confirmed elevation case。
- DET-000053 与 NJA-000027 保持双向引用。Analytic 以 context、session、feedback 三个不可替代分支关联账户生命周期、认证/会话、端点安全上下文、事件时授权与资源 allow/deny，并分层输出 identity_anomaly、accepted_identity_use、privileged_session、authority_unresolved、same_authority_use 与 elevation_confirmed。MIT-000052 新增权限最小化、会话约束/撤销验证和低反馈身份生命周期措施，父与三个子项均有两段独立 use、expected effect 与 limitations。

## 门禁与状态

- `make quality`：1492 个对象，schema 0/0、planning 0/0、重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 377 References、455 Claims、109 Cases、71 DET、76 NJA、69 MIT、0 REL。
- `dist/techniques/NJT-0061.json` 已重建；pipeline 为 TA0004 inventory 13、decision 13、technique 13、subtechnique 32、gap pending；reserved ID 为 0。
- Review Web `npm test` 71/71；Headless Chrome 实际渲染父、三子、DET、NJA、MIT 的 zh/en 共 14 页，名称、必需章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 正式对象 lifecycle.status 全部保持 review，尚无人工领域 reviewer。固定基线十三个父候选的开发已完成；TA0004 仍为 active，Niji-native gap、跨技术收敛和人工领域审查尚未完成，因此不得声明战术关闭。
