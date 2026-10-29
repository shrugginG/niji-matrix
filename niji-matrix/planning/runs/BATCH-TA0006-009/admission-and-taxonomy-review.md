# BATCH-TA0006-009 T1528 准入与原生分类裁决

T1528 裁决 `adapt`，正式父义为“应用访问令牌取得 / Application Access Token Acquisition”。完成点是完整 access token、refresh material 或等价应用授权材料实际进入攻击者控制接收端；授权、签发、路径发现、读取尝试、有效性判断、后继呈现、资源接受和资源访问分别记录。

正式 NJS：

1. 签发返回面令牌取得：攻击者控制或借用合法 token service/metadata/connected-app 返回接收端，使新签发材料直接到达攻击者控制面。
2. 持久令牌工件读取：从文件、Secret、投影卷、仓库或 durable cache 成功返回已存在的完整 token；对象路径和厂商不构成分类。
3. 易失运行态令牌提取：从 process/job memory、environment、临时脚本、broker/IPC 等易失边界复制 token；TeamPCP 的 runner.worker 事件提供高置信直接链。

材料有效性是跨子项结果分级，不建独立子项。T1606/NJT-0166 拥有权威签发链外的新材料构造，T1550 与 NJT-0061 拥有令牌呈现、接受和身份使用，T1539 拥有 Web session Cookie；从管理保管库或散落配置取得同一 token 时可分别与 NJT-0147/T1552 并列，但必须各有取得路径和材料类型证据。

REF-000070/178 复用；CASE-000064 只扩展父级 subject，用于证明 token 已在攻击者控制及撤销需求，取得路径未知，不能支持任何 NJS。新建 1 DET、4 NJA（三条取得路径加撤销传播验证）和 1 MIT；扩展 MIT-000052 的全 audience 撤销与实际拒绝验证，MIT-000066 只覆盖 connected-app return 子集。
