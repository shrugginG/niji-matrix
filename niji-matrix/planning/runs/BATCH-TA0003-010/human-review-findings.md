# BATCH-TA0003-010 人工审查整改记录

2026-09-12 审计发现 NJT-0091 父子、Claim、DET/NJA/MIT 全部只依赖 ATT&CK T1668，子技术攻防模型和限制不足，原 `high` 机理没有区分排除行为、噪声变化和攻击者匿迹意图；没有案例证明自身入口确实存续。

整改保留两个开放搜索变量，引入 UNC5174 的 exploit—后门账户—self-patch、PG_MEM 的后门用户/新 cron/miner—竞争进程清除，以及 NetSky.P 自身传播—Bagle Run key 删除。父级与竞争清除机理校准为 `medium`，UNC5174 入口关闭因目的和顺序直接可见保持 `high`。DET/NJA 以有向 actor→target、before/after inventory 和 surviving entry 为必要条件，MIT 强制独立变更来源、证据保全与全路径重建。机器与 Web 门禁通过后保持 `review`。
