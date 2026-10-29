# T1222 文件与目录权限修改：准入后研究交接

本项已在本批 admission review 中裁定 adapt，正式 ID 需等待 T1687 完成全部门禁后分配。固定父来源为 ATT&CK Enterprise 19.1 T1222，两个 ATT&CK 子项 T1222.001 Windows Permissions 和 T1222.002 Linux and Mac Permissions 只代表平台实现广度，不进入正式 NJS。建议父级直接对象是安全工具或保护性文件工件的“有效 DACL/POSIX 权限—消费者执行/读取结果”，不是文件权限 API 或特定产品。

定义应明确攻击者在已有访问权下改写安全组件二进制、配置、日志或策略工件的权限/所有权，使防御消费者无法按预期运行、读取或保护它们。匿迹特性是安全进程/调度仍可能存在，但访问控制在文件边界阻止加载或更新；残余是 writer、旧新 ACL/owner、继承来源、对象 hash、失败的访问或功能性 canary。单纯 chmod、takeown、icacls 或 Everyone 授权不构成完成结果。应用场景是投放银行木马或勒索活动前，针对能阻断恶意动作的安全产品工件；攻击者需写 DAC/owner 权限并了解消费者身份，防守方需把权限变更与进程启动、文件访问失败和独立产品结果连成链。

直接来源：ESET Research 2020 Grandoreiro 调查明确记录它对 Trusteer 主要二进制执行拒绝 ACL 改写，并说明其尝试破坏该保护产品。该来源直接支持恶意权限修改和目标/意图，但不证明每台设备产品最终失效；Case 必须保留 attempt 与 effective outcome 差。Microsoft DACL/ACE 文档解释拒绝 ACE 的排序和有效权限，Windows Security 4670 在目标 SACL 配置满足时提供旧新 security descriptor，4663 或产品错误可辅助消费结果。Linux auditctl 的属性变更 watch 是非 Windows 数据先验，不应从 Windows 案例外推 Linux 在野行为。

taxonomy 已审查 Windows 与 Linux/Mac 实现、拒绝保护工具执行、扩大攻击者写权、改变审计对象权限、继承 ACL 漂移。平台不是变量；“扩大写权”常是后续篡改前提而非直接失防，日志访问变化可由 NJT-0123 或事件擦除结果承载。当前公开直接案例只稳定支持父级的有效访问边界损伤，不足以确立独立可重复的 NJS 防守观察；建议零子项，并将拒绝执行与写权扩张的候选差留在研究限制。若以后证据同时证明两个变量的不同残余和检测恢复动作，再重新划分。

Detection Strategy 应按受保护文件对象及消费者身份关联权限写入、有效权限计算和失败/成功消费，不能只查 icacls 进程。Analytic 在 Windows 读取 4670 旧新 SDDL、writer logon session、对象路径/file ID/签名 hash、受影响 SID 与访问请求结果，条件允许时加 4663；必须校正 SACL 缺失、继承 ACL、合法产品升级。Mitigation 要锁定安全产品二进制/配置的 owner 与 WRITE_DAC/WRITE_OWNER、保留不同权 ACL 基线，升级后验证工具真实启动与保护功能。与 NJT-0123 可并记工具结果，但本父级拥有权限边界变化的原因链。

双语正式正文需逐字段写定义、特性、纳排、勒索/银行木马场景、攻防模型、NM-BT 机理、原生 taxonomy、DET→NJA、MIT Application 与证据限制。ESET Grandoreiro 是尝试证据，不得升格为普遍成功关闭 Trusteer。当前只作研究，未分配 NJT/NJS/CLM/DET/NJA/MIT。
