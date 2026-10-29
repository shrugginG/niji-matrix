# BATCH-TA0002-007 T1129 / T1127 整改约束

- 总体任务范围是 Execution 剩余 NJT-0074～NJT-0082；本批处理 T1129/NJT-0077 与 T1127/NJT-0080。上一批 T1648/T1072 已通过独立证据、taxonomy、专用防御、质量、Bundle 与 39 项 Web 门禁。
- T1129 的直接对象是进程通过平台 loader 或自定义映射器把共享模块代码映射并调用；T1127 的直接对象是签名开发工具解释 project/build/deployment 输入并代理执行。DLL 搜索顺序劫持归 T1574，跨进程注入归 T1055，普通 Native API 解析归 T1106，CI runner 执行归 T1677。
- 固定 `enterprise-attack 19.1`。T1129 无 ATT&CK 子项，开放检查标准 loader、同进程模块承载、内存反射映射、UNC/远程模块、模块化插件与跨进程注入边界。T1127 有 T1127.001 MSBuild、.002 ClickOnce、.003 JamPlus，只作为三类工具实现宽度先验，并检查外部/本地输入代理、inline/in-process task、网络来源和 child-process 结果。
- Astaroth 与 PipeMon 分别支撑 loader 进程内模块承载和 reflective module；Frankenstein 与 AkaiRyū 支撑 MSBuild project 输入代理和编译执行。Microsoft loader/MSBuild 文档用于实现语义，研究来源不得把工具能力升级为攻击者现场意图。
- 为 T1129 与 T1127 分别创建 DET/NJA/MIT。模块分析连接 process、module/file backing、loader call、memory region/thread 与结果；开发工具分析连接 utility provenance、project/input digest、task factory/inline code、child/module/network 与应用控制策略。旧通用 DET-000059/NJA-000034/MIT-000058 在新包接管全部正式对象后移入可恢复 retired 并归档。
