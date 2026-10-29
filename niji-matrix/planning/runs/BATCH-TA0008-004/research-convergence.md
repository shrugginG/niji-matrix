# BATCH-TA0008-004 T1550 主 Agent 收敛与 TA0008 关闭前提

- 准入：adapt；新建以“已生成替代材料的呈现与接受”为直接对象的父项。材料取得属于 NJT-0178 等 Credential Access 对象，链外伪造属于 NJT-0166/T1606/T1558，认证过程修改属于 NJT-0093/T1556，旧会话控制者接管属于 NJT-0151。
- 固定 4 个 ATT&CK 子项均有覆盖裁决。正式新增 1 项 Niji 原生子项：验证器介导的替代证明新建认证。稳定变量是当前 verifier/KDC/token endpoint 接受已生成材料并产生 fresh context 或 target proof，而当前操作者未执行原始秘密或交互因素链。
- 资源直接接受既有 access token/Cookie/session state 的连续使用已由 NJS-0061-002 拥有；外部远程网关重放由 NJS-0055-001 拥有，不按材料名在 T1550 下复制。跨设备/设备指纹贴合由 NJS-0061-001/NJS-0050-004 或绑定控制承担。
- hash、TGT/service ticket、refresh/sign-in-session material 是实现宽度。authority 派生 proof 与 target-ready material 直接 validation 作为两个 NJA 分支，不拆成互斥 NJS，因为同一 TGT→TGS→service 或 refresh→access token 链可连续跨越两者。
- audience/SPN/scope、材料寿命、设备绑定是验证和缓解维度；攻击者未必控制原件 claims 或固有寿命，且已有 owner，因此不建额外 NJS。1 个输出来自共享库查重，不是把 4 个 ATT&CK 子项改名合并。
- 防御：新建 1 DET、2 NJA、1 MIT；扩展 DET-000053/NJA-000027 的父级 resource-local 分支，扩展 MIT-000052 父级应用；MIT-000187 继续负责材料取得面，不能替代 presentation/verifier 控制。
- 证据：UNC6692 Pass-the-Hash 是正式野外 Case；Microsoft Overpass 内容是检测场景而非具名受害事件。官方 4776/4768/4769、NTLM/Kerberos 规范、RFC 6750、Token Protection、Credential Guard、认证 Silo 与 NTLM 限制按字段和产品覆盖范围使用。
- T1550 全部门禁通过后，主 Agent还须核对 TA0008 九个父候选、gap analysis、跨技术重复决议、ID 状态、Bundle/Web/API 和人工评审状态，才能把 tactic plan 置于 review。所有对象保持 review，人工领域评审仍待进行。
