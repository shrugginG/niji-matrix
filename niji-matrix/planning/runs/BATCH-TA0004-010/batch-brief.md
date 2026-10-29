# BATCH-TA0004-010 研究与收敛约束

## 固定候选与总体进度

唯一基线是 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1，不迁移版本。TA0004 十三个父候选顺序保持：T1548、T1134、T1098、T1547、T1037、T1543、T1484、T1611、T1546、T1068、T1055、T1053、T1078。前九项已经逐批通过；当前总体剩余范围为第 10–13 项。

| 批次 | 顺序 | ATT&CK 父技术 | 现有决策与 Niji 对象 | 状态 |
|---|---:|---|---|---|
| BATCH-TA0004-010 | 10 | T1068 Exploitation for Privilege Escalation | 预检未发现以 T1068 为 origin 的正式决议或 NJT | active |
| BATCH-TA0004-011 | 11 | T1055 Process Injection | 待独立准入 | planned |
| BATCH-TA0004-012 | 12 | T1053 Scheduled Task/Job | TA0002 DEC-TA0002-T1053；NJT-0075 | planned |
| BATCH-TA0004-013 | 13 | T1078 Valid Accounts | TA0001 DEC-TA0001-T1078；NJT-0061 | planned |

T1068 按漏洞利用事实、权限结果和匿迹变量相互耦合的证据复杂度作为单候选批次。它未通过证据、开放 taxonomy、字段、防御对象、机器校验、Bundle 与双语 Web QA 前，不开始 T1055 正式 YAML 写入。候选必须独立得到 retain、adapt 或 exclude；先前技术把漏洞利用划给 T1068 只是 ownership 边界，不等于自动准入。当前 reserved ID 为零。

## 当前候选 T1068

T1068 的固定英文名为 Exploitation for Privilege Escalation，固定基线没有 ATT&CK 子技术。零子项不允许直接得出零个 Niji 子技术；本批仍须从漏洞触发输入、exploit path、异常与恢复表面、权限转换、victim/target 选择、时序及跨传感器可见性执行开放式匿迹变量搜索。

直接对象暂定为 adversary-controlled exploit attempt 利用软件弱点，使原始主体或执行上下文跨越权限边界并完成首个新授权结果。仅命中 CVE、发送 exploit-shaped input、目标 crash、获得 shell、进程显示为 root/SYSTEM、读取高权限路径或报告称“privilege escalation”均不能替代 pre-state authority、vulnerable transition、post-state effective authority 和 first newly authorized result。若证据只支持漏洞事实而不支持稳定匿迹轴，可保留父级而不创建子技术；若父行为本身不满足 Niji 匿迹准入，则必须 exclude，而不能因 ATT&CK 战术映射强行建立 NJT。

## Taxonomy breadth 与相邻边界

开放搜索至少检查：

- exploit trigger 的形状、合法协议/系统调用/文件或设备接口承载与输入异常度；
- exploit chain 的单步/多步、用户态/内核态或 broker 路径，但不按 CVE、平台或漏洞类别机械分区；
- reliable crash、retry、failed probes、resource exhaustion、telemetry disruption 与 clean success 的痕迹差异；
- victim、CPU/core、namespace、tenant、host、service version 与时机选择是否为攻击者可控稳定匿迹键；
- 权限转换后沿原进程/线程继续、产生新主体、借受信 broker 落地或修改 token 的可见 actor 差异，以及与 T1134、T1055、T1611 的 owner 边界；
- heap spray、ROP/JOP、race shaping、memory corruption、logic flaw、signed module、driver 和 exploit kit 等实现是否只是工具/漏洞前提；
- first privileged effect 前后清理、故障抑制、日志/审计破坏、回退或短暂权限窗口；
- 利用本身、控制面授权绕过 NJT-0098、账户/令牌变化 NJT-0083/NJT-0099、跨隔离边界 NJT-0101、进程注入 T1055 与后续持久化之间的归属。

formal 轴必须同时满足攻击者可控稳定键、持久 sibling 边界、痕迹属性改变、观察/关联/归因效果变化、明确前提与场景、结论级证据和差异化检测/缓解。exploit success、CVE family、目标产品、平台、语言、内存区域、payload、工具、目标类型或日志字段不能直接成为 Niji 子项。

## 证据、共享库与门禁

先查询 references、claims、cases、detections、analytics、mitigations、relationships，并检查 NJT-0098、NJT-0099、NJT-0101 与现有 vulnerability/exploit 相关案例。ATT&CK 父页只锚定父行为、TA0004 映射及零子项；候选匿迹轴、权限差、检测假设、缓解效果和案例必须使用结论层级匹配的厂商技术材料、研究论文或事件证据。七库逐项决议 reuse、extend、create、split 或 defer；DET/NJA 必须双向引用，MIT applications 对父及每个正式子项分别给出 use、expected_effect、limitations。

正式内容继续采用 YAML-only `schema_version: 2.0.0` 和逐段中英配对。每项 mechanism 必须形成行为设计 → 痕迹变化 → 防守观察影响 → 匿迹效果；完成后逐字段对照 NJT-0001，运行 `make quality`、构建 Bundle、pipeline/reserved-ID 检查、Review Web `npm test`，并实际渲染父技术、全部子技术及 DET/NJA/MIT 中英文页面与跨对象引用。所有 lifecycle.status 保持 review；本批完成只推进到 10/13，不声明 TA0004 关闭。
