# BATCH-TA0007-003 共享库身份决议

- **复用/扩展 T1622 包：** NJT-0106 增加 `TA0007` tactic_ref；复用 NJS-0106-001/-002、REF-000386/414/415/416、CLM-000584/585/621/622、CASE-000138/139、DET-000103/122、NJA-000088/108 和 MIT-000105。TA0007 只新增独立准入决策，不新建同义语义对象。
- **复用来源：** REF-000211/212/375 支持 Kubernetes audit、授权与 ServiceAccount；REF-000360/361 支持后继 vulnerable-driver 边界；REF-000382 支持 T1482 的 Storm-0501 边界但不越级证明租户读取；REF-000625 扩展 T1083 固定 STIX locator；REF-000379/474 支持 Windows 对象与共享审计。
- **新建来源：** REF-000817..REF-000841，按 canonical URL 查重后分别支持 T1613、T1652、T1482 和 T1083；工具能力不冒充在野案例。
- **新建语义对象：** CLM-000892..899、CASE-000259..262、DET-000207..210、NJA-000249..256、MIT-000189..192。四套防御的数据面分别为 Kubernetes/Docker、驱动工具/注册表/API、AD/Graph 和 Windows/POSIX 命名空间，不能按“枚举”共同标题合并。
- **拆分边界：** 既有容器执行/部署策略只作后继边界；BYOVD/驱动加载策略不覆盖驱动发现；账户与信任控制不等同拓扑 read；浏览历史、云对象键与 Collection 文件读取不等同文件系统命名空间枚举。
- **defer：** 四个新父级的原生细分轴不创建 NJS、Claim 或 MIT Application。T1622 的线程隐藏/拒绝附加维持既有 deferred。
