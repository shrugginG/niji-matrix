# BATCH-TA0004-010 人工可读审阅记录

## 候选准入与权限结果

- T1068 独立决议为 adapt，形成 NJT-0102“脆弱权限转换利用”。成立链固定为 caller/context pre-state → exact vulnerable component/version 与 reachability → attacker-controlled trigger/interface → vulnerable transition → post-state effective authority → positive authority difference → first newly authorized result。
- CVE 或脆弱版本存在、exploit 文件/参数、request、exception/crash/BSOD、shell 与 root/SYSTEM/kernel 标签只能支持 exposure、attempt 或中间状态；缺少脆弱转换因果和正权限差时不得确认。本边界与 NJT-0098 的正常授权控制路径、NJT-0099 的 token carrier、T1055 的无漏洞跨进程写入及 NJT-0101 的隔离边界 crossing 分开。

## Taxonomy breadth

- 固定 ATT&CK 19.1 的 T1068 没有子技术，但仍执行开放搜索和第二轮检查：漏洞语义/触发接口、版本与上下文门控、clean success、admission trust、结果载体、回退，以及 ATT&CK 外的来源、观测、时间和证据完整性维度。
- 最终正式 Niji 子技术为 1：NJS-0102-001“预受信脆弱组件权限枢转”。它固定 exact vulnerable version 因签名、publisher、allow policy 或系统角色获得实际 event-time admission，再由攻击者 controller 经接口产生 kernel/更高权限效果；由此改变 visible provenance、关联键与 block/allow 防御。
- 不能减少，因为父级任意 vulnerability trigger 链不能替代 admission decision、load/interface、controller request 与 kernel effect 的独立证据和治理；不能增加，因为 version gating 与 fault-suppressed success 仍是假设，普通语义混淆和权限结果是 parent-core，token/injection/escape/loader/cleanup 归相邻 owner，CVE、driver、产品、平台、漏洞类、工具、介质和日志字段均未形成稳定匿迹边界。

## 字段、证据与防御对象

- 逐字段对照 NJT-0001 后，父与子对象的定义、匿迹特性、范围、场景、attacker/defender model 和限制均多段双语配对。父级 NM-DO 与子项 NM-FD 均完整说明行为设计 → 痕迹变化 → 防守观察/归因影响 → 匿迹效果，并以 PwnKit、Dirty Pipe、CrowdStrike、ESET 和 Microsoft 结论级材料校准；没有把 ATT&CK 父页当作统一证据。
- 七库决议：reuse REF-000243；create REF-000355..361、CLM-000559..563、CASE-000129..130、DET-000099、NJA-000080、MIT-000100；extend/split 无；REL defer。PwnKit case 明确是研究演示且不证明现场匿迹意图；Embargo case 支持成功 BYOVD effect，但 event-time Code Integrity admission 仍需本地 telemetry。
- DET-000099 ↔ NJA-000080 双向引用，分级 exposure、attempt、exploit observed、pretrusted pivot、authority unresolved/no gain、elevation confirmed 和 telemetry integrity risk。MIT-000100 的父、子 applications 各自包含 use、expected effect 和 limitations，没有以改名方式批量生成。

## 门禁与状态

- `make quality`：1441 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 357 References、441 Claims、105 Cases、70 DET、74 NJA、68 MIT、0 REL。
- `dist/techniques/NJT-0102.json` 已构建；pipeline 为 TA0004 inventory 13、decision 10、technique 10、subtechnique 21、gap pending；reserved ID 为 0。
- Review Web `npm test` 65/65；Headless Chrome 实际渲染父、子项、DET、NJA、MIT 的 zh/en 共 10 页，标题、章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 正式对象 lifecycle.status 为 review，尚无人工领域 reviewer。总体进度 10/13；BATCH-TA0004-011 可进入 T1055 研究，TA0004 仍 active，Niji-native gap、跨技术收敛与人工领域审查均未完成。
