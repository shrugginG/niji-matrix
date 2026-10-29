# BATCH-TA0005-007 研究与收敛约束

- 基线 enterprise-attack 19.1；复杂单候选 T1564；前一批已通过全部门禁。
- 固定基线有 14 个 ATT&CK 子技术，触发显式覆盖表和第二轮 taxonomy。它们只作研究广度输入，不导入、翻译或改名。
- 正式候选轴：默认视图遗漏、替代地址空间、检查表示与运行状态分离、观察域封装。
- 工具、平台、介质、字段、目标类型和 ATT&CK 子技术名称不构成边界。
- Email Hiding Rules 与 File/Path Exclusions 进入默认视图遗漏；NTFS attributes、resource forks、xattrs、hidden FS、bind mounts 进入替代地址空间；VBA stomping 与 process argument spoofing 进入表示分离；Run Virtual Instance 进入观察域封装；Ignore Process Interrupts 因主要改变控制与存活而非工件可见性，记 adjacent/not-stealth-distinct。
