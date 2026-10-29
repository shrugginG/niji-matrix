# BATCH-TA0112-005 Plist 介质与防御结果边界

本批固定使用 `matrix.yaml` 的 MITRE ATT&CK Enterprise 19.1 基线，只处理 TA0112 正式候选 T1647 Plist File Modification。前三批和五候选 BATCH-TA0112-004 已通过证据、taxonomy、双语正文、防御、质量、Bundle 与 Web 门禁并保持 review；TA0112 正式矩阵当前完成 9/18。本批候选数不预设 NJT 或 NJS 数量，T1647 必须先完成 retain、adapt 或 exclude 准入判断。

T1647 的直接介质是 macOS property list。ATT&CK 父项同时描述 Info.plist、Dock/LaunchPad presentation、LaunchAgent/LaunchDaemon、re-opened applications 和动态链接环境变量，覆盖隐藏呈现、执行和持久化等不同结果。TA0112 只能保留 plist key-value 变化直接削弱可验证防御控制或观察能力的分支；创建恶意 LaunchAgent、修改现有启动项、服务定义替换和动态加载路径分别需要与 NJT-0084、NJT-0089 及相应执行/持久化 owner 划界。隐藏窗口、LSUIElement 与 Dock/LaunchPad 替换还需与 TA0005 的 NJT-0111 工件可见性重塑划界，不能因 ATT&CK 把行为放在 Defense Impairment 就重复正式父技术。

ATT&CK 19.1 的 T1647 没有子项，仍须开放搜索：应用 UI/默认枚举遗漏、可信应用身份或 Dock 指向重绑定、启动/登录消费、环境变量/加载语义、关闭安全工具设置以及正常开发/部署改动。Niji 子项只在攻击者可控变量、痕迹变化、防守观察差和目标化防御均独立时成立；plist 类型、XML/二进制格式、路径、工具、应用名称和 key 名不得作为 NJS。若已有 NJT owner 完整覆盖直接结果，或公开案例只支持执行/持久化/可见性而不支持独立防御削弱，必须 exclude，而不是为形式完整新增对象。

证据至少需要固定 ATT&CK 父页、Apple 对 Info.plist/Launch Services 消费语义的官方说明，以及 XCSSET 等直接技术报告。每项案例严格区分 plist 写入、OS/Launch Services 消费、用户/防守观察差和后继结果；不从“修改了 LSUIElement”推断安全工具关闭。共享库先按 ATT&CK ID、官方 URL 和语义指纹查重。准入收敛前不分配 NJT/NJS、Claim、Case、DET、NJA、MIT 或 REL；exclude 只写决策与必要 Reference，不创建不存在的防御包。

若候选准入，正式父子内容按 NJT-0001 字段责任完整覆盖定义、匿迹特性、范围、场景、攻防模型、机理、证据和限制，并建立目标化 DET→NJA 与 MIT Application。若候选排除，决策必须逐项说明已存在的 owner、未成立的独立防御结果及重新评估条件。批次结束仍需查重、ID 同步、`make quality`、Review Web 测试和 API 0 issue；人工领域评审前保持 review。
