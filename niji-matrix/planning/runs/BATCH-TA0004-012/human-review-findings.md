# BATCH-TA0004-012 人工可读审阅记录

## 候选准入与权限结果

- T1053 独立决议为 retain；TA0004 复用并扩展 NJT-0075“匿迹化计划执行”及四个既有 NJS，不复制技术对象、不改原 DEC-TA0002-T1053 lineage。父级权限链固定为 submitter/pre-state authority → exact scheduler object/version → admission/trigger → actual runtime principal/token/capability/ServiceAccount → first attacker action → positive authority difference → first expected-deny/observed-allow resource result。
- 任务创建、root/SYSTEM、RunLevel、ServiceAccount、scheduler parent 或成功码任一单点都不足。普通 user crontab、user timer、default ServiceAccount、已有管理员提交的高权任务及同权限执行明确保持 non-elevating；缺 submitter、actual runtime 或资源决议则保持 authority unresolved。

## Taxonomy breadth

- 固定 Enterprise ATT&CK 19.1 的五项子技术已逐项覆盖：At、Cron、Systemd Timers、Container Orchestration Job 留 parent-core，只有满足既有变量门时才映射；Scheduled Task 的 Guloader、Nitrokod、Tarrask、Serpent 案例分别支持四个现有 Niji 轴。第二轮继续检查 runtime identity、scheduler parentage、既有任务身份替换、credential/logon type、jitter/catch-up、remote submission、action proxy 与 post-run restoration。
- 最终正式 Niji 子技术数仍为 4，新增 0。不能减少，因为基线合形、观察窗口外延期、状态枚举抑制与短驻一次性代理分别需要资产定义基线、长周期 watchlist、标准—原始—执行差分和分钟级生命周期关联；不能增加，因为 runtime authority 和 scheduler broker 是父级共同门，身份替换/登录类型证据不足，其他轴收敛到既有子项或相邻技术，平台、账户、API、命令和字段分区被拒绝。

## 字段、证据与防御对象

- 父与四子均补齐独立 TA0004 definition、scope、scenario、attacker/defender model、mechanism causal chain 与 limitations；Tarrask 被明确校准为“已有 SYSTEM 后隐藏任务”的匿迹证据，不被改写成提权案例。四项公开恶意案例均缺完整权限端点，事件级提权依赖本地遥测。
- 七库决议：reuse REF-000127、259–266 与 CASE-000090–093；create DEC-TA0004-T1053、REF-000372–375、CLM-000572–574；extend NJT-0075、四个 NJS、DET-000087、NJA-000064、MIT-000088；split 无；REL defer。新增官方证据覆盖 Windows task security context、Cronie owner/username、systemd service credentials 和 Kubernetes ServiceAccount。
- DET-000087 与 NJA-000064 保持双向引用。Analytic 现有 10 类数据、10 项 observables、4 类 false positives、6 类 blind spots，并分级输出 scheduler anomaly、execution confirmed、non-elevating、authority unresolved、elevation confirmed 和 telemetry integrity risk。MIT-000088 新增 runtime least authority、authority-lineage retention 和 effect recovery 三项措施；父与四子各有两段独立 use、expected effect、limitations。

## 门禁与状态

- make quality：1480 个对象，schema 0/0、planning 0/0、重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 370 References、452 Claims、109 Cases、71 DET、76 NJA、69 MIT、0 REL。
- dist/techniques/NJT-0075.json 已构建；pipeline 为 TA0004 inventory 13、decision 12、technique 12、subtechnique 29、gap pending；reserved ID 为 0。
- Review Web npm test 69/69；Headless Chrome 实际渲染父、四子、DET、NJA、MIT 的 zh/en 共 16 页，名称、章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 正式对象 lifecycle.status 全部保持 review，尚无人工领域 reviewer。总体进度 12/13；BATCH-TA0004-013 可进入 T1078，TA0004 仍 active，Niji-native gap、跨技术收敛与人工领域审查均未完成。
