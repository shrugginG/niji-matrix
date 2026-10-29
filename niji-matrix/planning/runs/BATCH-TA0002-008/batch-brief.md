# BATCH-TA0002-008 T1651 / T1675 整改约束

- 固定 `enterprise-attack 19.1`；前序 BATCH-TA0002-004 全部门禁通过后，本批处理 NJT-0064 与 NJT-0068。两者均跨管理面与来宾，但云租户命令服务和 ESXi Guest Operations 的身份、代理与日志边界不同，不合并正式对象或防御对象。
- T1651 开放检索覆盖 Azure VM Run Command/Extension、AWS Systems Manager、控制面审计、来宾代理与现场滥用；既有两子项必须分别证明跨层痕迹分离和维护情境伪装。
- T1675 开放检索覆盖 Guest Operations API、vmtoolsd 父级、来宾认证缺口、ESXi `vmware.log` 残余与 UNC3886/VIRTUALPITA 案例；不得按 API 方法、来宾 OS、漏洞或工具拆分。
- 两项均不得把“使用合法管理功能”等同于匿迹；必须描述攻击者控制条件、观察断点、残余、反证和合法替代解释。正式防御对象按云管理与 ESXi 分开创建。
