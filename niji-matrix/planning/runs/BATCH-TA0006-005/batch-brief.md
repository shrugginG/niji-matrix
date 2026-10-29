# BATCH-TA0006-005 T1556 Modify Authentication Process 复杂单候选

本批属于本轮下五项总体范围，正式写入必须等待 BATCH-TA0006-003 与 004 全部门禁通过。固定 ATT&CK Enterprise 19.1。T1556 有九项固定子项，触发逐项覆盖表、第二轮 taxonomy 与零/一子项广度解释。已有 TA0003 的 NJT-0093 及两个原生子项承载 Persistence 结果；研究必须优先判断 reuse/extend/split，而不是为 TA0006 复制父技术。TA0112 的独立计划也把防御削弱结果视为另一直接对象。

Credential Access 的直接结果是认证组件、过滤器、提供者、联合链或策略变化导致凭据、秘密或认证材料被捕获、存储或暴露。选择性后门秘密接受与范围化策略例外若只产生持久认证结果，由 NJT-0093 已有分类拥有；密码过滤器、Network Provider、PAM、可逆加密等只有在可证实材料获取结果时才属于 TA0006。单纯增加认证器/账户状态归 T1098，中心防御策略损伤归 TA0112，伪造令牌/票据归 T1606/T1558。

Sub-agent 使用 TA0006-005-T1556 临时键，只写 research-T1556.yaml，不分配 ID或修改规范区。交接须完成九项覆盖表和第二轮原生变量搜索，明确已有 NJT-0093 的跨战术复用条件、是否需新增原生子项、父级字段改写影响，以及 Credential Access 专属 DET/NJA/MIT。不能为战术计数另建同义 NJT。
