# BATCH-TA0112-013 信任裁决输入与控制面颠覆开发

基线固定为 matrix.yaml 的 MITRE ATT&CK Enterprise 19.1。本批只处理最后候选 T1553 Subvert Trust Controls。BATCH-TA0112-012 已以 NJT-0172、1 个 NJS、共享来源收敛、质量 0/0、104/104 Web 与双语 API 进入 review；本批完成后需另做 TA0112 全战术 gap/convergence/closure 审查，不能仅因 18 项都有文件就自动关闭。

T1553 在固定基线有 6 个 ATT&CK 子项：T1553.001 Gatekeeper Bypass、.002 Code Signing、.003 SIP and Trust Provider Hijacking、.004 Install Root Certificate、.005 Mark-of-the-Web Bypass、.006 Code Signing Policy Modification。必须建立逐簇覆盖表并完成第二轮 taxonomy。ATT&CK 子项只作为信任输入/消费者/平台广度，不复制名称或数量。

候选直接对象是安全 consumer 对恶意/未受信对象给出“允许、可信、无警告或较低审查”的实际裁决差。父技术必须闭合 attacker-controlled trust input/state、consumer verification decision 与 accepted execution/connection/content outcome。只有签名、证书、Registry、quarantine/MOTW 变化或 unsigned execution 都不足。

第一轮至少审查四条稳定轴：

- 对象携带/借用可验证的签名、证书或 notarization evidence，而 consumer policy 不变；
- 攻击者把新 root/anchor 加入信任图，使后继对象/会话链到该 anchor 后被接受；
- 攻击者改写 verifier policy、provider/SIP 或 enforcement state，使原本应拒绝的输入通过；
- 攻击者移除或绕开 per-object provenance constraint（Zone.Identifier、com.apple.quarantine 或容器继承差），使 consumer 不进入受限路径。

第二轮必须检查 Gatekeeper 的签名/notarization、policy override、quarantine/provenance 三种不同路径是否分别归上述轴；SIP/provider 与 code-sign policy 是否同属 evaluator state；root certificate 的后继结果与 network AiTM、code execution 的相邻 owner；Code Signing 与既有 NJT-0087 二进制内容破坏、NJT-0114 可见身份伪装的边界；MOTW/Quarantine 与 NJT-0112 事后证据擦除的边界。对象、平台、证书类型、文件格式、工具和 ATT&CK 名称不得成为 NJS。

共享库按 ATT&CK ID/版本 URL、Microsoft/Apple 规范 URL、公告/报告 URL 和语义指纹查重。PipeMon 原始 ESET 报告 REF-000281 可扩展 code-signing 事实；其他 child 来源优先使用 Apple/Microsoft 官方语义、Objective-See MaMi、Kaspersky BlueNoroff 与结论级技术报告。Detection 必须以 trust_input_id—consumer_id—policy/version—decision—outcome 为主线，并为四项原生变量提供不同数据分支；Mitigation 每个 NJT/NJS 有独立 Application。人工评审前全部保持 review。

## 集成结果

T1553 经 adapt 形成 NJT-0173“信任裁决输入颠覆”与四项 NJS：对象信任证明借用、信任锚图扩展、验证策略与提供者改写、对象来源约束移除。六项 ATT&CK 子项全部有 coverage resolution 并完成第二轮 taxonomy。新增 15 个 Reference、9 个 Claim、3 个 Case、1 个 Detection Strategy、4 个 Detection Analytic 和 1 个 Mitigation；复用 REF-000594，扩展 REF-000281。

最终门禁：内容 2877 个对象、0 错误、0 警告；规划 3023 条 ID 记录、0 错误、0 警告；共享库 0 精确重复、0 待审可能重复，REF-000200/REF-000772 按 PowerShell consumer 与 VBS/sealed-policy 控制语义记录 split；141 个父技术正文审计与 12 个基础设施测试通过。NJT-0173 Bundle 已构建，Review Web 106/106 与双语 API 通过。所有正式对象保持 review。
