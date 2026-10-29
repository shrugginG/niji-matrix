# TA0003 Persistence 已有对象整改收敛记录（2026-09-12）

## 范围

本轮整改处理审计标记的 11 个既有父技术，不开发 TA0003 固定基线剩余候选：NJT-0055、NJT-0087、NJT-0089、NJT-0090、NJT-0091、NJT-0092、NJT-0093、NJT-0094、NJT-0095、NJT-0096、NJT-0097。

## 候选结果

| 对象 | 整改性质 | 主要收敛 |
|---|---|---|
| NJT-0093 | 完整重开 | Skeleton Key、Solorigate、UNC3944；组件/联合信任与策略例外分支；DET-000073→NJA-000052、MIT-000073 全面扩展 |
| NJT-0094 | 完整重开 | FIN7 parent consumer 链与 Kovter/Sysinternals null/API 子项分层；同快照等价权限检测与安全清除 |
| NJT-0090 | 完整重开 | Microsoft permanent WMI consumer、Mandiant 谓词、Solorigate binding；谓词选择性与 Broker 来源分离 |
| NJT-0091 | 完整重开 | UNC5174 self-patch、PG_MEM、NetSky.P；有向排除、before/after 与 surviving entry |
| NJT-0055 | 完整重开 | 删除跨 TA0001 名称替换模板；Heartbleed/token 与风险情境两个变量；新增 DET-000094→NJA-000071、MIT-000095 |
| NJT-0087 | 局部补强 | 重写父级场景/攻防模型和 NJS-0087-001；保留两个已达标兄弟项 |
| NJT-0089 | 局部补强 | 重写两个子项攻防模型；服务身份替换复用 REF-000289..292；SDDL 轴保持无 Case、medium |
| NJT-0092 | 局部补强 | 扩充 tag/digest、缓存、registry audit、签名 admission 和跨实例生命周期 |
| NJT-0095 | 局部补强 | 扩充 Office trusted surface、Trust Center、add-in/template inventory 与合法扩展反例 |
| NJT-0096 | 局部补强 | 强制 power request/policy—预期状态边界—依赖 PID/session—继续活动链 |
| NJT-0097 | 局部补强 | 扩充 measurement coverage/firmware readback 与 boot source/image/running state 链 |

Case 仍为空的 NJT-0089、0092、0095、0096、0097 没有为了数量制造活动案例；其局部整改使用已有技术/官方来源并在限制中明确结论层级。

## 共享库

- 新建 REF-000303..316（其中 303..316 并非连续全部由本轮占用范围外对象；本轮实际新增 303..316 中相应 14 项），扩展 REF-000230。
- 新建 CASE-000110..121。
- 新建 DET-000094、NJA-000071、MIT-000095。
- 扩展 NJT-0090/0091/0093/0094 的现有 DET→NJA 与 MIT，扩展相关 Claim 与决策。
- 共享库重复审计为 0 exact、0 unresolved possible、1 reviewed similarity。

## 深度复核

11 个父技术、20 个子技术整改后，中文核心阅读字段的中位数为父级 2242、子级 1929.5；最短子级为 1315。子技术攻击者模型、防守方模型和限制中位数分别为 281、331.5、263。字符数只用于验证此前系统性压缩已消失，不作为内容配额。

## 最终门禁

- 正式对象：1307；15 tactics、65 techniques、147 subtechniques。
- 内容与规划：0 errors、0 warnings。
- 基础设施测试：12/12。
- Review Web：58/58。
- Bundle：NJT-0055、0087、0089、0090、0091、0092、0093、0094、0095、0096、0097 均成功构建。
- reserved ID：0。
- lifecycle：全部保持 `review`，没有创建 `published`。

## 战术状态

本轮整改关闭了“已有 17 项中的已识别质量问题”，不关闭 TA0003。固定 ATT&CK 19.1 Persistence 清单仍为 17/22，剩余 5 个父候选、Niji-native gap analysis 与人工领域审查仍待完成；战术继续为 `active / partial`。
