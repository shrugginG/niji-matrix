# BATCH-TA0004-008 人工可读审阅记录

## 候选准入与权限结果

- T1611 独立决议为 adapt，新建 NJT-0101“隔离工作负载至宿主权限逃逸”。确认链固定为 container/guest pre-state → exact boundary primitive 或 Broker request → effective host context/canonical host resource → positive authority difference → first host-only authorized outcome。
- container UID 0、privileged、hostPID/hostNetwork、hostPath/device/socket、CVE 命中、exploit crash、宿主凭据字符串或 shell 位于 host filesystem 都不是成功结论。漏洞利用事实归相邻 T1068；新工作负载执行、持久服务调和和镜像复现分别由 NJT-0067、NJT-0089、NJT-0092 持有。

## Taxonomy breadth

- 固定 ATT&CK 19.1 的 T1611 没有子技术，但仍执行开放式搜索和第二遍检查，覆盖 direct crossing、visible actor continuity、canonical resource identity、runtime/callback brokerage、异步激活、短暂清理、多层边界、orchestrator lifecycle、漏洞/capability 前提、目标介质及平台/产品/字段分区等十一类维度。
- 最终正式 Niji 子技术为 2：NJS-0101-001“宿主资源命名空间别名投射”和 NJS-0101-002“宿主 Broker 逃逸来源转换”。不能减少：前者由原容器进程直接访问宿主规范资源，以 namespace/mapping/inode/handle 为主键；后者由宿主 daemon/helper 或新 workload 产生结果，以 caller/request/transaction/context 为主键，visible actor 与控制措施相反。不能增加：其余轴已收敛为 parent-core、adjacent、hypothesis/deferred 或 rejected，没有第三个轴同时通过稳定可控、sibling 边界、痕迹改变、观察影响、场景、结论证据和差异化防御门禁。
- 两个子项均非 ATT&CK 子项导入。资源 alias 与 Broker 可以在同一攻击链并列，但一个不包含另一个；按 Linux/Windows/ESXi、Docker/Kubernetes、CVE、mount、socket、device、工具或日志字段拆分均被拒绝。

## 字段、证据与防御对象

- 逐字段对照 NJT-0001 后，definition 明确隔离边界与权限差；stealth characteristics 区分跨层痕迹、别名语义和来源转换；scope 同时给出纳入、排除、相邻 owner 和合法运维反例；application scenarios 分开 Linux/Kubernetes、Windows container 与 VM/hypervisor；attacker/defender model 规定能力、反馈、跨层 identity 和分级结果；research limitations 限制公开案例的授权集完整度与平台推广。
- 每项 mechanism 形成行为设计 → 异构痕迹或身份/资源语义变化 → 防守方局部观察/归因受损 → Boundary Traversal、Data Obscuration 或 Feature Disguise 效果，并只引用结论层级匹配的 evidence_refs；Broker 泛化的攻击者匿迹意图校准为 medium。
- 七库决议：reuse REF-000213；extend 无；create REF-000345..352、CLM-000552..556、CASE-000127..128、DET-000098、NJA-000078..079、MIT-000099；split alias 与 Broker analytics；REL defer。CASE-000073/075/076 保持相邻 container entry/deployment 范围，不因名称相近扩展。
- DET-000098 ↔ NJA-000078/NJA-000079 双向引用。前者解析 container alias 到 canonical host object，后者连接 original request 到 host Broker transaction/outcome；共同坚持 pre/post authorization difference 与首个 host-only allow/result。MIT-000099 为 parent、alias child、Broker child 各自提供 use、expected_effect、limitations，并把恢复扩展到宿主 effect、runtime/hypervisor 完整性和不可独立验证节点的重建。

## 门禁与状态

- `make quality`：1416 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 348 References、434 Claims、103 Cases、69 DET、73 NJA、67 MIT、0 REL。
- `dist/techniques/NJT-0101.json` 已构建；pipeline 为 TA0004 inventory 13、decision 8、technique 8、subtechnique 18、gap pending；reserved ID 为 0。
- Review Web `npm test` 63/63；Headless Chrome 实际渲染父、两个子项、DET、两个 NJA、MIT 的 zh/en 共 14 页，标题、章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 正式对象 lifecycle.status 为 review，尚无人工领域 reviewer。总体进度 8/13；BATCH-TA0004-009 可进入 T1546 研究，TA0004 仍 active，Niji-native gap、跨技术收敛与人工领域审查均未完成。

