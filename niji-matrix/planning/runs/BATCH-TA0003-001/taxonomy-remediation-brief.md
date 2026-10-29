# BATCH-TA0003-001 T1098 taxonomy breadth 整改

固定 ATT&CK Enterprise 19.1。T1098 有 7 项 ATT&CK 子技术，触发显式覆盖表与第二轮 taxonomy；当前 1 个 Niji 子项过宽地合并了凭据、认证方法、设备、角色和委托，必须按痕迹与防御差异重新审查。

本轮候选轴为：并行认证路径增补、间接授权图增补、身份绑定设备信任附着、凭据寿命重置循环和账户特定安全策略例外。逐项按稳定攻击者变量、trace change、defender effect、场景、证据与 DET/MIT 差异决定 formal/hypothesis/defer。ATT&CK 名称和七项数量只作广度先验，不成为输出配额。

整改期间 NJT-0083、现有子项、决策与防御对象退回 draft；在质量、Bundle、18+ Web 测试和中英 DOM QA 重新通过前不开始 T1547 整改或原 BATCH-TA0003-008。
