# BATCH-TA0004-002 人工可读审阅记录

## 候选准入与 taxonomy

- T1134 独立决议为 `adapt`，形成 `NJT-0099`；没有导入或翻译 ATT&CK 子技术。
- 固定 19.1 基线的五项子技术均已覆盖，并额外完成开放式第二轮搜索。正式 Niji 子技术为 `NJS-0099-001` 进程驻留式有效身份替换、`NJS-0099-002` 新进程权威谱系解耦、`NJS-0099-003` 休眠令牌权限选择性激活。
- 数量不能减少：线程 TID 有效身份、进程创建多源谱系与同一 token 权限位状态机使用不同 stable key、观察面、误报、窗口和缓解动作。数量不能增加：token 来源/类型/模拟级别/API/工具/权限名不是独立匿迹变量，SID-History 归既有 NJS-0083-002，纯 PPID 断树无 TA0004 结果，延迟使用与最小权限集保持 deferred/hypothesis。

## 字段责任与证据

- 父技术和三个子技术的 definition、stealth characteristics、scope boundary、application scenarios、attacker model、defender model 和 limitations 均按 NJT-0001 字段责任逐项审查；正文针对 Windows token 安全模型、TID、AuthenticationId、Creator/Target Subject、actual/displayed parent 和 privilege delta 编写，没有复用 T1548 的通用威胁模型或限制。
- 每项正式 mechanism 均写出行为设计、痕迹变化、防守观察影响与匿迹效果。受控机理仅使用 `NM-BT`、`NM-FD`、`NM-ST`，所有 mechanism 都有结论级 `evidence_refs` 和校准 confidence。
- ATT&CK T1134 页面只承担父行为、TA0004 映射和五项广度；Microsoft 文档分别支持 token、SetThreadToken、CreateProcessWithTokenW、显式父体、AdjustTokenPrivileges 和 4688 字段语义。Lotus Blossom 只支持另一进程 token/权限工具的父级案例；PipeMon 支持 PPID 重启与 SeLoadDriverPrivilege 序列；SUNSPOT 支持 SeDebugPrivilege 激活与后继进程内存访问；DarkGate 只支持显示层匿迹，未被用来单独证明 TA0004。
- SID-History 的 ATT&CK 位置被保留在覆盖表，但按直接对象把目录持久授权边归给 NJS-0083-002；这不否认它进入后继访问令牌。

## 共享对象与防御决议

- `REF-000252`（SUNSPOT）与 `REF-000281`（PipeMon）经 locator/notes 扩展后复用；另建 `REF-000326` 至 `REF-000335`，没有复制已有来源。新建七项原子 Claim 与三项事实范围不同的 Case。
- DET-000096 双向引用 NJA-000074、NJA-000075、NJA-000076，分别恢复线程有效身份来源、新进程 caller/parent/token 权威谱系和权限位前后态—消费结果；Strategy evidence 覆盖所有 Analytic evidence。
- MIT-000097 对父技术及三个子技术分别提供候选特定的 `use`、`expected_effect` 与 `limitations`，覆盖用户权限/句柄、模拟 broker、带 token/选定父体创建、权限位消费和不可变谱系。
- Relationships 为 `defer`；相邻 owner 已由 decision 与 scope 明确，不制造无额外语义的 REL。

## 机器、Bundle 与双语 Web QA

- `make quality`：1361 个对象，0 errors、0 warnings；planning 0/0；重复审计 0 exact、0 unresolved possible、1 reviewed similar；12 项基础设施测试通过。
- Bundle：`dist/techniques/NJT-0099.json` 构建成功。`pipeline_status.py` 显示 TA0004 inventory 13、decision 2、technique 2、subtechnique 5，gap 仍为 pending；reserved ID 为 0。
- `tool/niji-matrix-review` 的 `npm test` 为 58/58。
- Headless Chrome 通过 Review Web live API 实际渲染父技术、三个子技术、DET、三个 NJA 和 MIT，并切换 zh/en，共检查 18 页；标题、核心段落、语言状态、父/子/DET/NJA/MIT/CASE 必要链接与每页原始 YAML 均无缺失。

## 状态

本批次为 `review`，尚无人工领域审查者，不得设为 `published`。前五候选总体进度为 2/5；下一批为 T1098。TA0004 其余父候选、Niji-native gap、跨技术收敛与人工审查均未完成，战术未关闭。
