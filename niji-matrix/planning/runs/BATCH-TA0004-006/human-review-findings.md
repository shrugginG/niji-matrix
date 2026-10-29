# BATCH-TA0004-006 人工可读审阅记录

## 候选准入与权限结果

- T1543 在 TA0004 下独立决议为 retain，并扩展复用 TA0003 的 NJT-0089。确认门是 lower writer/pre-state → exact service object/definition version → manager adoption → actual execution account/token/security context → positive authorization delta → first newly authorized operation。
- ATT&CK 的 administrator-created、root/SYSTEM-executed 说明建立可能性，不证明每个事件已经提权。若 writer 已有等同权限、user service 同权限运行、定义没有被 manager 消费或没有新获准结果，只能输出 definition anomaly 或 Persistence。
- 直接对象和 stable keys 未改变，所以保留 DEC-TA0003-T1543 为 canonical origin，新建 DEC-TA0004-T1543 表达独立战术决议；不新建重复 NJT。

## Taxonomy breadth

- 固定五项子技术 T1543.001–.005 已逐项覆盖；Launch Agent、systemd、Launch Daemon 和 Container Service 均按实现留在父级，Windows Service 直接支持既有身份替换与对象权限导致的枚举差。没有导入或改名 ATT&CK 子技术。
- 开放搜索检查新服务名称拟态、目标/参数替换、账户/执行上下文转换、延迟/restart-only 激活、分布式 desired-state 扇出、瞬时 create—start—delete、目标正文/加载、权限前提和 platform/manager/medium。权限结果与延迟是 parent-core；命名、瞬时执行、目标内容/加载和权限修改 adjacent；分布式扇出 deferred；平台/manager/介质/账户/日志字段 rejected。
- 最终正式数为 2，新增 0。不能增加：没有第三个同时具备稳定可控键、独立 trace/observation、防御 owner 与结论级证据的轴。不能减少：NJS-0089-001 使用 same object identity 的 definition/target old—new 键并改变实体区分，NJS-0089-002 使用 same object 的 principal/API presence 与 ACL 键并改变观察覆盖，两者反例、数据与恢复不同。

## 证据、内容与防御

- 新建 REF-000336（Microsoft Service Security and Access Rights）与 REF-000337（LocalSystem Account），并消费 CLM-000546（TA0004 relevance）与 CLM-000547（dual-output detection）。REF-000182、CLM-000365/366 与 CASE-000103 已按原语义扩展；CASE-000103 明确不证明权限 delta。
- NJT-0089 和两个 NJS 在所有必需字段增加候选特定 TA0004 段落。NM-FD、NM-BT 与父级 NM-ST 均完整表达行为设计→痕迹变化→防守观察影响→匿迹效果，跨战术 confidence 统一校准为 medium。
- DET-000063 与 NJA-000041 保持双向引用，新增 definition_anomaly、persistence_restored、elevation_confirmed、authority_unresolved 四类输出和 service-authority-transition 数据。MIT-000060 新增 writer-runtime authority separation，并对 NJT-0089 与两个 NJS 分别给出 use、expected effect、limitations 及 privileged side-effect rollback。

## 门禁与状态

- `make quality`：1375 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础测试通过。共享库为 333 References、425 Claims、100 Cases、67 DET、70 NJA、65 MIT、0 REL。
- `dist/techniques/NJT-0089.json` 已重建；pipeline 为 TA0004 inventory 13、decision 6、technique 6、subtechnique 15、gap pending；无 reserved ID。
- Review Web `npm test` 59/59；Headless Chrome 实际渲染父、2 个子项、DET/NJA/MIT 的 zh/en 共 12 页，标题、章节、语言状态、交叉链接和 raw YAML 均无缺失。
- 所有正式对象保持 review，尚无人工领域 reviewer。总体进度 6/13；BATCH-TA0004-007 可进入 T1484 研究，但 TA0004 仍 active，Niji-native gap、跨技术收敛与人工领域审查尚未完成。
