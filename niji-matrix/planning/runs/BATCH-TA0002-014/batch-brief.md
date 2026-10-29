# BATCH-TA0002-014 T1677 单候选整改约束

- 总体任务范围是 Execution 剩余的 NJT-0074～NJT-0082；本交付批次只处理 T1677/NJT-0074。上一批 BATCH-TA0002-012 已通过结论级证据、字段深度、共享库、Schema、Bundle 与 32 项 Review Web 门禁。
- T1677 的直接行为对象是由 CI/CD runner 实际解释或执行的流水线定义、引用构建输入或外部贡献数据。仓库凭据窃取、制品投毒、依赖投毒和部署平台终端执行只有在形成 runner 执行链时才属于本技术；否则分别归供应链、凭据或 T1072 等相邻对象。
- 固定 `enterprise-attack 19.1` 中 T1677 没有 ATT&CK 子技术，因此执行开放 taxonomy 检索，不把页面列举的 direct、indirect、public pipeline execution 机械导入为 Niji 子项。候选轴必须证明攻击者可控变量、痕迹变化、观察影响和防御差异。
- 重点检验三个既有 Niji 轴：受信流水线定义注入、间接构建输入激活和外部贡献情境门控。SolarWinds SUNSPOT、XZ 构建注入、Trivy 流水线事件与 GitHub `pull_request_target`/untrusted-input 研究分别只能支持其直接观察到的结论；研究演示不得冒充现场攻击案例。
- 为 T1677 创建流水线专用 DET/NJA/MIT，不复用仅标题相似的通用执行对象。分析必须关联定义或引用输入变更、触发上下文、runner 权限、job 执行、制品和出站结果；缓解必须覆盖评审、隔离、最小权限、不可变引用和构建来源证明。
- 正式内容保持 YAML-only 2.0、成对双语自然段和 NJT-0001 字段责任。当前批次未通过 evidence、taxonomy、content-depth、defense、duplicate、Bundle 与 Web QA 前，不开始下一批正式写入；九项总体范围不构成一次性生成许可。
