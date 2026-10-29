# BATCH-TA0004-001 研究与收敛约束

## 研究前冻结的前五项

以下顺序来自 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1 官方 Enterprise ATT&CK matrix 工作表。表中的“现有决策”只描述其他战术已经形成的决策；它不能替代 TA0004 下逐候选独立准入。

| 顺序 | ATT&CK ID | 英文父技术名称 | 现有决策 | 现有 Niji 对象 |
|---|---|---|---|---|
| 1 | T1548 | Abuse Elevation Control Mechanism | 无 | 无 |
| 2 | T1134 | Access Token Manipulation | 无 | 无 |
| 3 | T1098 | Account Manipulation | TA0003 retain，DEC-TA0003-T1098 | NJT-0083；NJS-0083-001、NJS-0083-002、NJS-0083-003 |
| 4 | T1547 | Boot or Logon Autostart Execution | TA0003 retain，DEC-TA0003-T1547 | NJT-0084；NJS-0084-001、NJS-0084-002、NJS-0084-003 |
| 5 | T1037 | Boot or Logon Initialization Scripts | TA0003 retain，DEC-TA0003-T1037 | NJT-0085；NJS-0085-001、NJS-0085-002 |

这五项是本次程序范围，不是五项正式 NJT 的产量承诺。每项必须先独立得到 retain、adapt 或 exclude；只有证据支持的非排除项才进入正式写入。T1098、T1547 和 T1037 必须先判断 TA0004 是否与现有对象共享同一直接对象、taxonomy 和防御语义，再决定 extend/reuse 或 split，不因已有 NJT 而自动复用。

## 固定基线完整父候选清单

TA0004 的完整固定展示顺序共十三项：T1548 Abuse Elevation Control Mechanism、T1134 Access Token Manipulation、T1098 Account Manipulation、T1547 Boot or Logon Autostart Execution、T1037 Boot or Logon Initialization Scripts、T1543 Create or Modify System Process、T1484 Domain or Tenant Policy Modification、T1611 Escape to Host、T1546 Event Triggered Execution、T1068 Exploitation for Privilege Escalation、T1055 Process Injection、T1053 Scheduled Task/Job、T1078 Valid Accounts。第六至第十三项只为冻结完整顺序，不在本次前五项开发范围内。

## 基线与交付批次

- 战术：TA0004 Privilege Escalation。
- ATT&CK domain：enterprise-attack。
- ATT&CK version：19.1；本程序不迁移版本。
- 总体程序候选：顺序 1–5，即 T1548、T1134、T1098、T1547、T1037。
- 当前交付批次候选：仅 T1548。
- 前一批次门禁状态：无前序 TA0004 批次；启动预检中 `make quality` 为 0 errors、0 warnings，共享库为 0 exact 和 0 unresolved possible duplicates，12 项基础设施测试通过，reserved ID 为 0。
- 本批次未通过证据、taxonomy、内容深度、防御、机器、Bundle 与双语 Web QA 前，BATCH-TA0004-002 不得进入正式 YAML 写入。

五项均采用单候选批次。T1548 和 T1098 具有 6+ ATT&CK 子项并触发第二轮 taxonomy；T1547 具有十四项子技术并强制单候选；T1134 的 Windows 令牌身份与进程谱系、T1037 的脚本生命周期与既有 Persistence 对象均要求独立威胁模型、防御和跨战术对象决议。

## 父技术边界

| 候选 | 直接行为对象 | 与兄弟候选和既有技术的边界 |
|---|---|---|
| T1548 | 攻击者利用或改变本来用于授权高权限操作的控制机制，使当前主体或操作获得更高有效权限 | T1134 的直接对象是 Windows 访问令牌及其安全上下文；T1098 改变既有身份的认证或授权边；T1547 与 T1037 以启动或登录生命周期状态为直接对象；T1068 以软件漏洞利用为直接对象。单纯具有管理员凭据、使用已经有效的高权限账户或执行普通高权限命令不自动属于 T1548 |

T1548 的 ATT&CK 父页面只锚定权限提升行为和 TA0004 映射。任何 Niji 子技术、匿迹机理、检测字段、缓解效果或案例结论必须得到同层级证据；无法达到结论级支持的轴保持 hypothesis、deferred 或 rejected。

## T1548 taxonomy breadth 先验

固定基线包含六项 ATT&CK 子技术，因此必须建立显式覆盖表并完成第二轮开放 taxonomy 搜索：

| ATT&CK 子技术 | 英文名称 | 代表的实现或行为维度 | 初始覆盖状态 |
|---|---|---|---|
| T1548.002 | Bypass User Account Control | Windows UAC 完整性级别与同意/自动提升边界 | pending |
| T1548.004 | Elevated Execution with Prompt | macOS 授权提示与用户批准边界 | pending |
| T1548.001 | Setuid and Setgid | Unix 文件权限位与执行身份转换 | pending |
| T1548.003 | Sudo and Sudo Caching | sudo 策略、授权提示与凭据时间戳缓存 | pending |
| T1548.006 | TCC Manipulation | macOS 隐私授权数据库与受保护资源访问 | pending |
| T1548.005 | Temporary Elevated Cloud Access | 云控制面限时高权限激活与审批生命周期 | pending |

研究必须逐项或逐簇将这些维度决议为 parent-core、niji-variable-candidate、adjacent-technique、evidence-deferred 或 not-stealth-distinct，并从其内部、跨簇和 ATT&CK 分类之外搜索攻击者可控的稳定匿迹变量。每个候选轴最终只能标为 formal、hypothesis、parent-core、adjacent、deferred 或 rejected，且要记录稳定性、痕迹变化、防守观察效果、前提、证据和防御差异。最终 Niji 子技术数由这些门禁决定，不以六项为配额。

## 子技术规则

- 不导入、翻译、合并改名或一一映射任何 ATT&CK 子技术。
- 不按操作系统、产品、控制机制名称、日志字段、权限目标或凭据介质拆分 Niji 子技术。
- 正式轴必须同时具备攻击者有意控制、持久边界、痕迹变化、防守观察效果、明确前提、结论级证据和有意义的检测或缓解差异。
- 每项正式机理必须形成行为设计到痕迹变化、再到防守观察影响和匿迹效果的完整因果链；`summary` 不使用句末标点。
- 六项 ATT&CK 子技术允许收敛为任意正式数量；若最终只有零或一项，主 Agent 必须逐轴给出 breadth-gap explanation。

## 共享库与证据门禁

研究前后均查询 references、claims、cases、detections、analytics、mitigations 和 relationships 七类共享库。每个候选对象明确记录 reuse、extend、create、split 或 defer，语义相同才允许复用。DET 只定义策略目标，NJA 保存可实施逻辑且双向引用；MIT 通过每个 `applications[].target_ref` 提供目标特定的 use、expected_effect 和 limitations。

| 稳定键 | 类型 | 可能复用的候选 | 当前决议 |
|---|---|---|---|
| ATTACK-v19-T1548 | REF | T1548 父行为和 TA0004 映射 | pending lookup |
| ELEVATION-CONTROL-STATE-LINEAGE | DET/NJA | 控制配置、授权结果与高权限后继活动关联 | pending semantic lookup |
| ELEVATION-CONTROL-GOVERNANCE | MIT | 最小权限、审批、配置完整性与临时权限生命周期 | pending semantic lookup |

固定 ATT&CK 页面不能统一支持子技术、机理、Analytic、Mitigation Application 或案例归因。每项重要边界、机理和子技术成立性必须建立原子 Claim 与结论级 Reference；证据只能支持父行为时，不扩写成更窄结论。

## 内容深度与验收

T1548 的 definition_and_concept、stealth_characteristics、scope_boundary_definition、application_scenarios、attacker_model、defender_model 和 research.limitations 必须逐项回答字段规范的全部问题。分段按论证需要决定，中英文逐段配对并保持相同范围、强度和限制。与 NJT-0001 的比较只检查字段责任、因果完整度、证据强度、威胁模型与自然表达，不复制其数量或长度。

正式写入后必须运行 `make quality`、构建该 NJT bundle、运行 `pipeline_status.py`、确认无未解释 reserved ID，并在 Review Web 运行 `npm test`。随后检查父项和全部子项的中英文页面、DET 到 NJA 展开、MIT 逐目标应用、证据与原始 YAML。所有新对象在没有人工领域审查时保持 `review`。

## 执行安排

- 本任务未请求 sub-agent 或并行研究，主 Agent 顺序完成当前单候选批次。
- T1548 暂存路径：`planning/runs/BATCH-TA0004-001/`。
- 后续批次只在当前门禁全部通过后创建正式 batch brief 和进入 canonical authoring。
- 需要重点检查的重叠：UAC/授权提示与用户同意，sudo 缓存与合法运维，TCC 访问权与传统权限提升，云临时提权与 T1098 授权边，以及 T1068 漏洞利用边界。
- 暂不进入正式分类的假设：提示压低、授权缓存利用、限时窗口对齐、合法管理路径拟态及配置可见性差异；它们必须逐一通过证据和 taxonomy 门禁。
