# BATCH-TA0004-005 人工可读审阅记录

## 候选与对象决议

- T1037 在 TA0004 下独立决议为 retain。固定 ATT&CK 19.1 父页只支持“某些”初始化脚本因以更高权限运行而可能提权；正式门槛是 lower writer/pre-state → exact content version and changed line → higher-authority lifecycle interpreter token → positive authority delta → first newly-authorized outcome。
- 同用户登录脚本、root 写/root 执行的 RC 脚本、高权限父体、系统路径、computer scope 或中央扇出均不能单独证明提权。没有完整权限结果链时只输出脚本异常或 Persistence。
- 直接对象仍是 NJT-0085 的生命周期脚本内容，因此跨战术扩展复用 NJT-0085 与两个 NJS，不新建 NJT/NJS；TA0003 decision 保持 canonical，TA0004 由 DEC-TA0004-T1037 独立表达。

## Taxonomy breadth

- 五项固定子技术已逐项覆盖：T1037.004 在保留既有正文时支持 NJS-0085-001，T1037.003 的一份中央版本到多主体消费支持 NJS-0085-002；其余及不满足条件的实例留在父级，没有导入 ATT&CK 子技术。
- 开放搜索检查 whole-script replacement/new script、writer-interpreter authority transition、signing/policy bypass、early-boot sensor gap、conditional branches、path/name mimicry 和 platform/language/medium。整体替换和权限差为 parent-core；控制绕过 adjacent；early boot、条件分支和路径借用 deferred；平台/语言/介质 rejected。
- 最终正式数仍为 2，新增 0。不能增加：没有第三个同时满足稳定可控、独立 trace/observation 和防御 owner 的轴。不能减少：内联轴使用 same path/mostly same body 的 old/new 行级键，扇出轴使用 upstream version/client applied-version set，关联、反例和恢复均不同。

## 内容、证据与防御

- NJT-0085 与两项 NJS 均增加候选特定的 TA0004 定义、范围、场景、攻击者/防守者模型、完整机制因果链和限制；特别保留现场内联案例不证明提权、网络登录脚本按用户权限运行、GPO startup script 的 Local System consumer 不证明低权限 writer 等约束。
- REF-000154 扩展 TA0004 条件，REF-000176 扩展 Local System startup context；其余六项 Reference、两项 Case 和七项既有 Claim 复用。新建并消费 CLM-000544（TA0004 relevance）与 CLM-000545（dual-output detection）。
- DET-000066 分开输出 content anomaly、Persistence 与 proven elevation；NJA-000045 新增第七类 authority-transition 数据，保存 writer/pre-state authorization set、interpreter token、delta、first outcome 及 elevated/same-authority/unresolved 客户端集合。MIT-000065 新增第六项 writer-interpreter boundary measure，并覆盖高权限结果撤销。

## 门禁与状态

- make quality：1370 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库目录为 331 References、423 Claims、100 Cases、67 DET、70 NJA、65 MIT、0 REL。
- dist/techniques/NJT-0085.json 已重建；pipeline 为 TA0004 inventory 13、decision 5、technique 5、subtechnique 13、gap pending；无 reserved ID。
- Review Web npm test 58/58；Headless Chrome 实际渲染父、2 个子项、DET/NJA/MIT 的 zh/en 共 12 页，标题、核心字段、语言状态、交叉链接和 raw YAML 均无缺失。
- 本批保持 review，没有人工领域 reviewer。本次前五候选进度 5/5；TA0004 仍 active 且未关闭，其余八个父候选、Niji-native gap、跨技术收敛和人工领域审查仍待完成。
