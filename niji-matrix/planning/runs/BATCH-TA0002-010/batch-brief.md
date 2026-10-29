# BATCH-TA0002-010 T1648 / T1072 整改约束

- 总体任务范围是 Execution 剩余 NJT-0074～NJT-0082；本批处理 T1648/NJT-0076 与 T1072/NJT-0078。上一批 T1053 已通过五项 ATT&CK 子技术覆盖、内容、共享库、质量、Bundle 与 36 项 Web 门禁。
- 两个父技术都从管理面产生执行，但直接对象不同。T1648 的对象是云函数、集成或办公自动化实例对代码/动作的执行；T1072 的对象是企业软件部署/配置管理控制面通过既有 agent 向受管端点执行命令、包或脚本。云资源管理命令、CI/CD runner、普通远程 shell 和下游软件安装必须按直接执行边界分开。
- 固定 `enterprise-attack 19.1`，T1648 与 T1072 均无 ATT&CK 子技术，分别执行开放 taxonomy 检索。无服务器候选检查短驻实例、事件耦合、执行角色委托与代码包装；部署候选检查管理 agent 代理、目标集合 fan-out、批准窗口、现有 package/job 复用和新装 RMM。
- Denonia 和 Microsoft DART 案例只分别支持 Lambda 运行环境与 Microsoft Flow 自动化；不得推断未知部署路径。APT32 ePO、AvosLocker PDQ 与 Medusa BigFix/PDQ 支持管理 agent 和 fleet fan-out，但“分批低慢”或“批准窗口伪装”若无直接意图证据必须撤回或延期。
- 为两个父技术分别创建专用 DET/NJA/MIT。T1648 分析连接 function/flow 版本、trigger、execution role、invocation 与 API/网络结果；T1072 分析连接控制面 operator、package/script、target collection、agent receipt 与端点进程/影响。当前批次通过所有候选门禁前，不开始下一批正式写入。
