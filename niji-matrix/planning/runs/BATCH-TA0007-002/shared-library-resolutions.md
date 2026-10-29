# BATCH-TA0007-002 共享库身份决议

主 Agent 在五份研究交接齐备、父/子边界和准入收敛后，按 canonical URL 与语义对象复核。下列决议先于正式 REF/CLM/CASE/DET/NJA/MIT ID 分配。

## 来源

- `reuse`: `REF-000379` 仅支持配置 SACL 后的 Windows 4663；`REF-000366` 支持 Sysmon 进程/网络事件边界；`REF-000206` 支持 AWS Systems Manager 的控制台/代码请求审计边界；`REF-000422` 仅作 T1538/T1526 排除错误外推的已修复漏洞对照。
- `extend`: `REF-000513` 与 AWS S3 CloudTrail 页面具有同一规范 URL。保留原 Get/Put 结论，增加页面中 `ListObjects` 的普通对象数据事件定位，以及 `ListObjectsV2` 在当前表的资源类型差异说明；不能据表格遗漏宣称普通桶 V2 无记录。
- `create`: 五个 ATT&CK 19.1 父来源；CISA BeagleBoyz、Volexity 3CX、Chrome 漫游配置、Edge 历史策略；Expel AWS 入侵、CloudTrail 管理读、CloudTrail 事件字段、EC2 DescribeInstances；AWS ConsoleLogin、GCP Audit 概览；Microsoft Storm-0501、Google Service Usage audit 与 services.list 接口、AWS GuardDuty CloudTrail/GetDetector、Azure Activity Log；Unit 42 Bling Libra、AWS ListObjectsV2 API、AWS S3 server access log、Azure Blob 监控、GCP Storage audit。各 URL 已对当前共享库精确比对，除 S3 CloudTrail 页面外未发现已有同 URL REF。
- 不把同一个攻击活动按来源文章重复建立案例：Volexity 3CX 与 Mandiant 3CX 是同一事件；本批以 Volexity 原始样本分析建立一次 CASE。CISA 联合通告是多事件综合，不单独建离散案例。Unit 42 的实际受害环境与其受控 S3 Browser 试验必须分层，当前不建 T1619 专属 CASE。

## 语义对象

- `create`: 四项获准父级各自一组原子行为/机理 Claim、一个检测目标 DET、至少一个可实施 NJA、一个逐目标 MIT。各项的直接对象、日志通道、正常反例、调优与控制动作不同，不共用“云只读异常”通用 Analytic。T1217 的 3CX、T1580 的 Expel、T1526 的 Storm-0501 各建一个范围受限 CASE。
- `split`: `DET-000118` 是低覆盖区域资源**创建**谱系，不可直接扩为 T1580 的资源**读取**；`DET-000105` 是原始卷读取与对象视图差，不可直接扩为 T1619 的云对象列表；`DET-000140` 的身份副本读取不等于 T1217 浏览历史读取。MIT-000124 的层级迁移控制不等于 T1526 读取服务防护状态。
- `defer`: T1538 不建立 NJT/NJS 或专属 DET/NJA/MIT；四个父级的研究性原生轴暂不分配 NJS、子项 Claim 或子项 Application。任何来源的工具能力不升级为在野案例或量化检测效果。

最终 ID 与复用范围以正式对象、重复审计和 integration summary 为准。
