# BATCH-TA0004-011 人工可读审阅记录

## 候选准入与权限结果

- T1055 独立决议为 adapt，形成 NJT-0103“跨进程执行上下文嵌入”。父级链固定为 identifiable source/controller → exact target process instance → cross-process write/map/load request → dispatch → target-context malicious instruction；TA0004 再要求 source pre-state 到 target/post-state 的正权限差以及首个 expected-deny/observed-allow 资源结果。
- ProcessAccess/ptrace/task handle、memory write/RWX、DLL path、remote thread/APC/callback、target 名称或后继网络行为只能支持 exposure、attempt、staged 或局部信号。注入已确认但权限相等时明确为 non-elevating；缺 source pre-state、target authority 或 resource decision 时保持 authority unresolved。

## Taxonomy breadth

- 固定 ATT&CK 19.1 的十二项子技术已逐项覆盖并执行第二轮 taxonomy。标准 DLL 与 ptrace/procfs 介质留 parent-core；PE/unbacked payload 收敛到 NJS-0103-001；thread hijack、APC、TLS、window、vDSO、ListPlanting 的既有 carrier 收敛到 NJS-0103-002；hollowing/doppelgänging 收敛到 NJS-0103-003；第二轮跨分类搜索得到 payload purpose 与 target role 合形的 NJS-0103-004。
- 最终正式 Niji 子技术数为 4。不能减少，因为 backing/content、carrier pre-state、birth file/section/image/first instruction、role/approved-code/first action 分别需要不同的证据和防御数据面；不能增加，因为 long-lived target 仍是假设，multi-process segmentation 和 post-use restoration 延后，普通权限差留父级，相邻 loader/broker/token/exploit/container/direct-syscall/obfuscation 各有 owner，API、平台、产品、工具、目标名或 ATT&CK 实现名均不是稳定匿迹边界。

## 字段、证据与防御对象

- 父与四个子对象均逐字段对照 NJT-0001；definition、stealth、scope、scenarios、attacker/defender model 和 limitations 为多段中英配对。每项机制完整写出行为设计 → backing/dispatch/provenance/role 痕迹变化 → 防守观察与归因影响 → 匿迹效果；公开案例不具权限快照，未越级证明 TA0004。
- 七库决议：reuse REF-000108、REF-000243、REF-000279；create REF-000362..367、REF-000369..371、CLM-000564..571、CASE-000131..134、DET-000100、NJA-000082/083、MIT-000102；Analytic 按 memory/dispatch 与 birth/role split；REL defer。质量审计发现新 REF-000368 与既有 REF-000108 URL 精确重复，已把所有消费者改为 reuse REF-000108，删除重复文件并 archive 该 consumed ID；REF-000281/286/333 仅作查询到的有限工具上下文，未进入正式结论。
- DET-000100 与 NJA-000082/083 双向引用。前者覆盖 source-target memory/load、dispatch、execution、authority result，后两者分别实现 memory/backing/flow 与 birth/role 数据链。MIT-000102 为 NJT-0103 和四个 NJS 各有独立 use、expected effect、limitations，没有通过替换名称批量生成。

## 门禁与状态

- `make quality`：1472 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 366 References、449 Claims、109 Cases、71 DET、76 NJA、69 MIT、0 REL。
- `dist/techniques/NJT-0103.json` 已构建；pipeline 为 TA0004 inventory 13、decision 11、technique 11、subtechnique 25、gap pending；reserved ID 为 0。
- Review Web `npm test` 67/67；Headless Chrome 实际渲染父、四子、DET、两 NJA、MIT 的 zh/en 共 18 页，名称、章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 正式对象 lifecycle.status 为 review，尚无人工领域 reviewer。总体进度 11/13；BATCH-TA0004-012 可进入 T1053，TA0004 仍 active，Niji-native gap、跨技术收敛与人工领域审查均未完成。
