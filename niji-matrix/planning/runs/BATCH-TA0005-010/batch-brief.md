# BATCH-TA0005-010 研究与收敛约束

- 基线 enterprise-attack 19.1；候选 T1202；前一批已通过全部门禁。
- 直接对象是受信系统实用程序作为命令发起者与真实命令或载荷之间的执行代理；与仅限开发工具的 NJT-0080 分离。
- 固定基线无子技术。Forfiles、PCA、WSL、ScriptRunner、SSH 配置等工具差异共享 caller—utility—command—outcome 链，不按工具拆分，拟 none-justified。
