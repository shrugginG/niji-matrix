# TA0112 Defense Impairment 战术收口审查

## 固定范围与结果

基线为 MITRE ATT&CK Enterprise 19.1。固定 18 个父候选均已有准入决策：T1686、T1685、T1484、T1689、T1687、T1222、T1556、T1578、T1666、T1112、T1601、T1599、T1690、T1207、T1688、T1553、T1600 共 17 项进入正式矩阵 review，T1647 exclude。TA0112 正式矩阵只统计这 17 个父技术；其下共有 27 项 Niji 原生 NJS。Stealth/TA0005、跨战术复用来源和外部研究候选不计入该进度。

## 跨技术收敛

- NJT-0123 拥有具体防御工具能力/范围/入库/反馈损伤；NJT-0172 拥有启动策略造成的组件缺席窗口。Safe Mode 中显式删除/重命名工具可双重映射，但受限 boot 的覆盖差不并入工具状态。
- NJT-0125 拥有集中策略发布和 consumer adoption；NJT-0162 拥有本地 Registry writer—consumer—结果；NJT-0173 只拥有 trust input/state 对实际 verifier decision 的改变。相同 Registry/Policy 介质不构成重复。
- NJT-0127 拥有 capability version rollback，NJT-0167 拥有网络设备运行内存/持久映像完整性，NJT-0128 拥有实际会话/材料加密强度。版本、映像和密码结果分别闭合。
- NJT-0161 拥有 security artifact access-right cause，NJT-0123 拥有最终工具功能；只有 ACL 变化不足以确认工具损伤。
- NJT-0126 拥有 cloud hierarchy ancestry/治理范围，NJT-0163 拥有 compute lineage 的控制注册或取证连续性；组织节点和实例生命周期不合并。
- NJT-0124 拥有单一 firewall enforcement state，NJT-0168 要求批准 path graph、bridge state 和双侧流量的端到端分段失效。
- NJT-0170 只处理 interactive command history 在持久化前的整体/选择性抑制；security telemetry pipeline 归 NJT-0123，事后删除归 NJT-0112。
- NJT-0171 拥有未批准 replication origin—DRS transaction—合法 DC 接受—directory outcome；policy/account/ACL/credential 内容结果由 NJT-0125、认证、权限或凭据对象继续负责。
- NJT-0173 拥有 object/anchor/verifier/provenance input 对 named trust consumer 决策的改变；二进制内容破坏、可见身份、网络 AiTM、一般证据擦除和人际信任分别归 NJT-0087、NJT-0114、网络对象、NJT-0112 与 NJT-0118。

## Niji 原生缺口审查

没有发现可独立建立 add 父技术的稳定 TA0112 缺口。以下轴保留 defer，而不是为了关闭战术强制正式化：

- T1207 复用 inactive/stale controller registration 的独立变量缺少直接案例和不同处置证据。
- T1688 Minimal/Networking 与一次/持续 safeboot 分别只是连接能力与时长，不是独立匿迹因果；其他 OS 的 restricted boot 缺少同等结论级证据。
- T1553 provider/policy child 有架构与 POC 支持，但没有为每类 provider 创建在野 Case；平台、证书类型和容器格式不再拆分。
- 中央策略/防御设置的 post-use reversion、作用域例外和同权证据污染在现有父项中作为检测/限制处理，当前不足以建立新父技术。

## 防御与发布状态

Review API 审计确认 17 个正式父技术均为 review，全部具备 available Detection Strategy 和 Mitigation；27 个 NJS 均从稳定变量产生。18 个 decision 中 17 项指向正式父技术，DEC-TA0112-T1647 为 exclude。机器门禁和 Web 门禁通过不等于 published；计划整体设置为 review，taxonomy/evidence/bilingual 标记 passed，reviewers 仍为空，等待人工领域审查。
