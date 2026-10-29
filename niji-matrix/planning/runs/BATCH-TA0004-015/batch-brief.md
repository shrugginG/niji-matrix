# BATCH-TA0004-015 语义整改约束

- 候选：T1098 / NJT-0083，T1547 / NJT-0084，T1037 / NJT-0085。
- 批次理由：三者均为 TA0003 对象复用于 TA0004，共享 writer–consumer 权限边界过度扩写问题，但分别保留身份状态、自启映射与初始化脚本的独立语义。
- 保留既有 ID、taxonomy、证据和防御对象；只修复正式读者正文。
- 不把权限差、ATT&CK 广度记录、检测输出状态或批次自证重复写入 Technique/Sub-technique。
- 完成候选级语义审查、质量、Bundle、pipeline、reserved ID 和双语 Web 门禁后才进入下一批。
