# BATCH-TA0007-002 逐候选语义门禁复核

本复核依据五份 sub-agent 交接、正式父技术和防御 YAML、固定 Enterprise 19.1 工作簿、NJT-0001 的字段责任及本批跨技术收敛记录。机器与 Web 全局门禁须另行完成，以下不把 API 可解析等同于人工领域审查。

| 候选 | 父级行为与来源层级 | 原生分类结论 | 独立防御目标与实现前提 | 研究限制 |
|---|---|---|---|---|
| T1217 / NJT-0138 | CISA 联合通告直接报告书签枚举；Volexity 对 3CX 样本直接记录历史标题和 URL 提取。浏览记录的“本次不需新导航”是架构推断。 | 本地已存记录读取属于父级；同步副本、时间选择、分批和扩展路径缺案例与独立防御差，`deferred`/0 NJS。 | DET-000149→NJA-000157 要求对实际浏览器配置路径配置并验证 4663 ReadData，接进程与暂存/外联；MIT-000138 管历史保留与读访问问责。 | 500 条上限不是“最近 500 条”；CISA 多事件综合不立单案；合法恢复/备份会读相同文件。 |
| T1580 / NJT-0139 | Expel 实际观察被盗 IAM 键的 ListBuckets、DescribeInstances 与 DescribeDBInstances 及后继操作；未观察到跨键分工或规避目标。 | 预存资源视图、跨账户/区域拼接、条件过滤和分页只留假设，`deferred`/0 NJS。 | DET-000150→NJA-000158 需组织 CloudTrail 管理读、批准 CSPM/IaC 台账及后继变更；MIT-000139 管读权限范围和区域/账户审计覆盖。 | 单条只读事件与正常盘点同形；CloudTrail 不给完整返回资源集，Expel 对停止实例 API 的一句描述不作为已证状态转换。 |
| T1538 / exclude | 固定 ATT&CK 行证明 GUI 发现行为；AWS ConsoleLogin/服务事件及 GCP Audit 说明“GUI 无审计”并非普遍真命题。 | GUI 是三类信息对象的路径，缺独立痕迹变量、专属 Analytic 和 Mitigation，不建 NJT/NJS。 | 邻项各自从资源、服务状态或对象列表设计防御；不为排除项造一套换名防御。 | 不否认恶意控制台浏览；若有同信息页面到后端请求到审计的同案对照可重审。 |
| T1526 / NJT-0140 | Microsoft Storm-0501 直接证明防护状态被理解并用于后续选择；GCP 官方确认 ListServices 不产生审计，AWS GuardDuty 可记录。两者不是同案同路径。 | 服务快照、按覆盖门控和跨范围读缺同案证据，`deferred`/0 NJS。父级 NM-BT 保持 `hypothesis`，不把 Storm 案例写为 GCP 无日志事件。 | DET-000151→NJA-000159 先在 AWS GuardDuty 已收管理事件的范围内实施 ListDetectors/GetDetector 与后继变化关联；MIT-000140 管状态读权限、独立覆盖快照及无日志路径治理。 | GCP 官方无日志方法不能被开启 Data Access 修复；AWS Analytic 不冒充 GCP/Azure 覆盖，后者明确为盲区。 |
| T1619 / NJT-0141 | AWS/Azure/GCP 接口证明桶内对象键列表；Unit 42 实际案只证明工具与对象访问，ListObjects 来自另行实验。 | prefix/分页、预存 Inventory 转读及分散时序无同案恶意与防御对照，`deferred`/0 NJS。 | DET-000152→NJA-000160 分别消费已启用的 S3 ListObjects 数据事件与 server access log 的桶内列表请求；MIT-000141 管 List 权限和逐云数据面日志。 | 当前 AWS 表普通对象行未列 V2，不能据遗漏断言不记；server access log 尽力投递，GCP DATA_READ 和 Azure 诊断需启用。 |

四个父级的双语字段均分别回答定义/目的、受控痕迹与残余、纳入/排除及正常反例、使用场景、攻击前提、防守观察、机理因果和结论级限制。防御对象没有共用仅替换名称的 Analytic：T1217 看端点读，T1580 看管理面资源图，T1526 看服务保护状态，T1619 看存储数据面。各字段以 NJT-0001 的问题覆盖与论证深度对照，不以相同篇幅或机制/NJS 数量作为目标。
