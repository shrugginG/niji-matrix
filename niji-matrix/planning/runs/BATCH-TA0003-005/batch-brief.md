# BATCH-TA0003-005 研究与收敛约束

## 基线与范围

- 战术：TA0003 Persistence；ATT&CK enterprise-attack 19.1。
- 总体候选：T1098、T1197、T1547、T1037、T1671、T1554、T1136、T1543、T1546、T1668。
- 当前候选：T1671 Cloud Application Integration，单候选；云应用对象、OAuth 授权、自动化工作流与身份状态边界复杂。
- 前批门禁：BATCH-TA0003-004 已通过证据、内容、质量、Bundle、15 项 Web 测试及双语 DOM QA。
- 当前批未通过前不开始下一批。

## 边界与分类

T1671 的直接对象是租户内可长期运行或持续获授权的云应用集成、连接器或工作流。T1098 负责既有用户/服务主体的凭据与授权边；T1546 负责事件订阅触发执行；T1053 负责时间调度；仅授权一次 API 调用不构成持久集成。不得按 Microsoft/Google/SaaS、OAuth scope、应用类型或 ATT&CK 子项拆分。

优先评估“既有业务应用身份挪用”与“业务流程合形集成”变量；若来源只证明恶意应用或同意授权，不能证明稳定观察差异，则 taxonomy 置为 deferred。父级机理也必须分别得到控制面—应用活动关联和正常集成外观证据。

## 共享与门禁

逐项查询 T1671、OAuth illicit consent、云应用审计、DET/MIT；与 T1098 的 DET-000064/NJA-000043/MIT-000063 按直接对象和数据逻辑决定 reuse/extend/split。父行为用固定 ATT&CK 与云厂商/威胁调查，防御字段用官方审计与响应资料。正文按 NJT-0001 字段责任独立编写，脚本只用于查重、ID、序列化、校验、Bundle 与 Web QA。
