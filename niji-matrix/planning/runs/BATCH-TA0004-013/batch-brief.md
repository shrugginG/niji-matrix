# BATCH-TA0004-013：T1078 单候选批次

## 固定基线、顺序与现有对象

唯一基线是 matrix.yaml 锁定的 MITRE ATT&CK Enterprise 19.1，不迁移版本。TA0004 十三个父候选顺序保持 T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078；前十二项已经逐批通过全部门禁。

| 本批顺序 | 总体顺序 | ATT&CK ID | 英文名称 | 现有决策 | 现有 Niji 对象 | 本批初态 |
|---|---:|---|---|---|---|---|
| 1 | 13 | T1078 | Valid Accounts | DEC-TA0001-T1078 retain（Initial Access）；TA0004 尚无独立决议 | NJT-0061 Valid Identity Entry；NJS-0061-001 Context-Aligned Identity Sign-In；NJS-0061-002 Reuse of Established Authenticated Sessions；DET-000053 / NJA-000027 / MIT-000052 | researching |

本批总体范围仅有固定第 13 项。它必须先独立完成 retain、adapt 或 exclude 决策；只有非排除且有证据的对象才进入正式扩展。四项固定 ATT&CK 子技术只作为研究宽度，Default、Domain、Local、Cloud Accounts 不导入、不翻译、不改名为 Niji 子技术。

## 单候选交付控制

T1078 单独成批，因为同一有效身份跨 Initial Access、Persistence、Privilege Escalation、Defense Evasion 与 Credential Access 复用，TA0004 必须把“有效登录”与“由身份/会话实际取得新增权限”分开，并处理账户状态、认证器、会话 token、资源授权及多个相邻 owner。完成明确的四项覆盖、开放 taxonomy 搜索、字段深度、权限结果门、防御对象决议、质量、Bundle、pipeline、reserved ID、review tests 与父/全部子项/防御对象双语 live Web QA 前，不更新本批为 complete。

## 研究问题与相邻边界

- 验证 parent qualification 是否应为 identifiable credential/session controller → accepted authentication or session reuse → actual resulting principal/session/token → positive effective-authority difference relative to attacker-controlled pre-state → first newly authorized protected-resource result；账户名、admin/root 角色、successful login 或 privileged API event 单独不充分。
- 检查现有两轴在 TA0004 下是否仍稳定：新登录情境贴合改变来源/设备/时间风险观察，既有认证会话复用省略重新认证链；不得按 Default/Domain/Local/Cloud、产品、协议、MFA、账户类型或日志字段机械增项。
- 与 NJT-0083 账户状态操纵、NJT-0099 runtime token 操纵、NJT-0098 临时提权事务、T1556 认证过程修改、T1136 新身份、Credential Access、T1133 remote service 和 T1539 web session cookie 窃取保持直接对象边界；前置秘密取得可共同映射，但 T1078 只拥有未修改有效凭据或已认证会话的实际使用。
- 七类共享库先查询，再作 reuse、extend、create、split 或 defer；公开案例若没有攻击者 pre-state 与目标 principal/session 的有效授权集合及首个 expected-deny/observed-allow 结果，不得升级为事件级 TA0004 结论。

## 验收约束

正式内容保持 YAML-only schema_version 2.0.0，逐段中英配对，lifecycle.status 为 review。每项机制需要行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果的完整链与结论级 evidence refs。DET 与 NJA 双向引用；MIT 对父与每个正式子项分别提供 target-specific use、expected effect、limitations。最终只能声明 TA0004 固定父候选开发完成；Niji-native gap、跨技术收敛和人工领域审查未完成前不得关闭战术。
