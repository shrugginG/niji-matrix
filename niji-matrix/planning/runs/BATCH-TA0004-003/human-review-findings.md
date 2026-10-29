# BATCH-TA0004-003 人工可读审阅记录

## 候选准入与跨战术对象决议

- T1098 在 TA0004 下独立决议为 `retain`。ATT&CK 19.1 明确说明账户状态修改可通过新增角色、权限或更高权限 Valid Account 造成提权。
- 直接对象仍是既有身份上的认证器、授权边或设备信任状态，与 TA0003 的 NJT-0083 相同；正式结果采用跨战术扩展复用，不新增 NJT 或副本 NJS。NJT-0083 的 canonical origin/decision 仍是 DEC-TA0003-T1098，TA0004 的独立准入由 DEC-TA0004-T1098 表达。
- TA0004 最小链为 `pre-state → mutation → propagation/token refresh → post-state authority delta → first newly-authorized privileged outcome`。同等权限恢复只承担 Persistence，不能因目标账户等级高而直接推断提权。

## Taxonomy breadth

- 七项固定子技术已逐项覆盖：T1098.001/.004 归并行认证路径，.002/.003/.006/.007 归间接授权图，.005 归身份绑定设备信任；没有导入 ATT&CK 子技术。
- 第二轮检查 credential lifetime、账户级 policy exception、direct/nested role、立即/延迟使用、owner displacement、device-claim 授权和 SID-History ownership。
- 最终仍为三个 Niji 子技术，新增数为零。不能增加：其余轴均为参数、相邻技术、deferred 或机械平台拆分。不能减少：认证器、授权边和设备 claim 使用不同 stable key、求值过程、反例和撤销动作。

## 内容、证据与防御

- NJT-0083 与三个子项均补充 TA0004-specific definition、scope、scenario、attacker/defender model 和 limitation；内容分别围绕 target identity entitlement、graph diff 和 device-policy before/after 编写，没有套用 T1134 token 或 T1548 broker 模板。
- REF-000143 扩展为同时锚定 TA0003/TA0004 与 authority-delta 限制；其余十项既有 Reference、两项 Case 和七项机制/存在 Claim 复用。新建 CLM-000540（TA0004 relevance）与 CLM-000541（双输出 detection）。
- DET-000064 与 NJA-000043 复用相同 mutation-use stable key，并增加独立“账户操纵权限提升链”输出、pre/post authority 数据、exact edge evaluation path 与 newly-authorized outcome；没有复制一套 TA0004 防御。
- MIT-000063 新增 effective-authority before/after gate，并在 parent application 中补充跨域 mutation approval、graph/policy diff、token refresh 与全原因回滚。三个既有 child application 保持各自认证器、图、设备恢复边界。

## 校验、Bundle 与 Web QA

- `make quality`：1364 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。
- Bundle `dist/techniques/NJT-0083.json` 已重建；pipeline 为 TA0004 inventory 13、decision 3、technique 3、subtechnique 8、gap pending；reserved ID 为 0。
- Review Web 的既有 T1098 regression contract 已更新为跨战术复用及第五 mitigation measure；`npm test` 58/58。
- Headless Chrome 实际渲染 NJT-0083、三个 NJS、DET-000064、NJA-000043、MIT-000063 的 zh/en，共 14 页；标题、核心字段、语言状态、父/子/DET/NJA/MIT/CASE 链接与每页 raw YAML 均无缺失。

## 状态

本批保持 `review`，无人工领域 reviewer。前五候选进度为 3/5；下一批 T1547 含十四项 ATT&CK 子技术，按规则单候选交付。TA0004 战术未关闭。
