# BATCH-TA0112-011 目录复制来源错位开发

基线固定为 matrix.yaml 的 MITRE ATT&CK Enterprise 19.1。本批只处理 T1207 Rogue Domain Controller；TA0112 总体剩余范围仍为 T1207、T1688、T1553，后两项分别保留在 BATCH-TA0112-012 与 BATCH-TA0112-013。BATCH-TA0112-006 已通过内容、规划、共享库、Bundle、100 项 Web 与双语 API 门禁并进入 review。本批未通过候选级证据、taxonomy、正文、防御、机器、Bundle 和 Web 门禁前，不进入 T1688 正式写入。

T1207 在固定基线没有 ATT&CK 子技术，适用普通开放 taxonomy 搜索，不能据此直接收敛为零 NJS。候选直接对象不是 Mimikatz、DCShadow 工具名或 Domain Controller 设备类别，而是攻击者把未批准主机/身份临时或复用地纳入目录复制权威，使目录更改以受信复制来源被合法 DC 接受，并把原始写入活动移出正常来源 DC 的日志链。必须证明 controller identity/registration、DRS 复制请求、合法 DC 接受和目标目录对象变化的闭环。

开放审查至少覆盖：新建并快速撤销 server/nTDSDSA/SPN 的短生命周期注册、复用 inactive/stale controller registration、非 DC 主机发起 DRSUAPI、originating DSA GUID 与批准 inventory 不一致、复制元数据或日志删除，以及目标账户/ACL/schema/credential 变化。注册与复制是同一攻击链的阶段，不能机械拆成兄弟 NJS；只有出现稳定替代路径、独立痕迹和不同防御关联时才正式划分。inactive registration 复用若缺少结论级攻击者证据则 defer。

边界上，DCSync 从合法 DC 拉取秘密属于 Credential Access；域策略内容变化由 NJT-0125 负责；新增持久账户/ACL/信任或凭据结果由对应 Persistence、Privilege Escalation 或 Credential Access 对象负责；正常 DC promotion/demotion、灾备恢复、站点迁移和复制拓扑维护是反例。T1207 只拥有伪造/未批准复制来源导致的防守观察与来源归因差。

共享库先按 ATT&CK ID、Microsoft 文档 URL、UncoverDCShadow 仓库和语义指纹查重。固定 ATT&CK 页面只锚定父行为；MS-DRSR 支持协议语义，Microsoft Defender for Identity 支持注册/复制检测面，UncoverDCShadow 支持短生命周期对象与正常 promotion 的差异，但研究复现不得写成在野事件。准入与 taxonomy 收敛前不分配 NJT/NJS、Claim、Case、DET、NJA 或 MIT。正式对象使用完整双语自然段并对照 NJT-0001；人工领域评审前保持 review。

## 集成结果

T1207 经 adapt 形成 NJT-0171“目录复制来源错位”，没有建立 NJS。父项要求未批准 controller identity、成功 DRS 事务、合法 DC 接受和目录对象结果闭环；新建注册、push 与撤销是顺序阶段，失活 registration 复用缺少结论级案例。新增 6 个 Reference、4 个 Claim、1 个 Detection Strategy、2 个 Detection Analytic 和 1 个 Mitigation；没有把 UncoverDCShadow POC 写成在野 Case。

最终门禁：内容 2818 个对象、0 错误、0 警告；规划 2965 条 ID 记录、0 错误、0 警告；共享库 0 精确重复、0 待审可能重复，REF-000747/REF-000752 以事件 4739/4929 语义差记录 split；139 个父技术正文审计与 12 个基础设施测试通过。NJT-0171 Bundle 已构建，Review Web 102/102 与双语 API 通过。所有新对象保持 review。
