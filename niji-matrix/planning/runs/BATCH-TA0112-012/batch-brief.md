# BATCH-TA0112-012 受限启动防御覆盖缺口开发

基线固定为 matrix.yaml 的 MITRE ATT&CK Enterprise 19.1。本批只处理 T1688 Safe Mode Boot；BATCH-TA0112-011 已以 NJT-0171、0 个 NJS、质量 0/0、Bundle、102/102 Web 和双语 API 进入 review。后续 T1553 仍在 BATCH-TA0112-013；本批未通过候选级门禁前不得正式写入 T1553。

候选直接对象不是 bcdedit、BCD 文件、SafeBoot Registry 或 ransomware 工具，而是攻击者使主机实际进入受限启动 session，导致正常启动时应在场的防御 driver/service/sensor 缺席，并在该缺口窗口内产生可验证的后继恶意结果。只修改 BCD、只重启或仅观察 EDR 离线都不足；必须关联 boot intent、实际 boot mode、expected-versus-loaded defense set 和 follow-on outcome。

固定基线没有 ATT&CK 子技术，仍需开放搜索。重点审查：Safe Mode minimal 与 networking 是否只是运行需求，是否存在独立匿迹差；攻击者仅借用受限启动默认允许集与主动把 payload/service/COM 加入 SafeBoot allowlist 是否形成稳定变量；一次性 Safe Mode 与持久 safeboot flag 是否属于时长而非分类；BCD、Registry、服务和远程会话分别留下何种痕迹。平台、命令、ransomware 家族和 Safe Mode 变体名称不得直接成为 NJS。

初步边界：正常故障排查、驱动回滚、灾备、DSRM 和管理员批准的维护以工单/console/session/outcome 排除；通用 BCD 或 Registry 修改分别由配置 owner 解释，防御工具主动停用归 NJT-0123，版本/启动信任降级归 NJT-0127。T1688 只拥有实际受限 boot 导致防御覆盖差及其窗口内结果；加密/Impact 是后继行为。

共享库按 ATT&CK ID、Microsoft SafeBoot/Startup Settings/BCDEdit URL、CISA 公告和 Sophos/ESET 报告查重。Microsoft 文档支持受限启动与允许集语义；Sophos Snatch 可直接支持 BCD、SafeBoot service enrollment、实际重启、防御缺席与加密结果；ESET Embargo 和 CISA LockBit 支持其他实现。研究/事件结论严格区分，不把产品页面当通用成功证明。正式内容对照 NJT-0001，建立专用 boot-session 防御分析与逐目标缓解，保持 review 等待人工评审。

## 集成结果

T1688 经 adapt 形成 NJT-0172“受限启动防御覆盖缺失”与 NJS-0172-001“受限启动载荷存活注册”。新增 6 个 Reference、5 个 Claim、2 个 Case、1 个 Detection Strategy、2 个 Detection Analytic 和 1 个 Mitigation；共享 ESET Embargo 原始文章复用并扩展 REF-000359。初建的重复 REF-000759 已删除并永久归档，所有引用、Bundle 与计划均同步到 canonical source。

最终门禁：内容 2838 个对象、0 错误、0 警告；规划 2985 条 ID 记录、0 错误、0 警告；共享库 0 精确重复、0 待审可能重复；140 个父技术正文审计与 12 个基础设施测试通过。NJT-0172 Bundle 已重建，Review Web 104/104 与双语 API 通过。父技术、子技术和新防御对象保持 review。
