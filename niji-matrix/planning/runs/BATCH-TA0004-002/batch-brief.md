# BATCH-TA0004-002 研究与收敛约束

## 研究前冻结的前五项

以下顺序来自 `matrix.yaml` 锁定的 MITRE ATT&CK Enterprise 19.1 官方 Enterprise ATT&CK matrix 工作表。现有跨战术对象只能作为共享对象候选，不能替代 TA0004 下的独立 retain、adapt 或 exclude 决策。

| 顺序 | ATT&CK ID | 英文父技术名称 | 现有决策 | 现有 Niji 对象 |
|---|---|---|---|---|
| 1 | T1548 | Abuse Elevation Control Mechanism | TA0004 adapt，DEC-TA0004-T1548 | NJT-0098；NJS-0098-001、NJS-0098-002 |
| 2 | T1134 | Access Token Manipulation | 无 | 无 |
| 3 | T1098 | Account Manipulation | TA0003 retain，DEC-TA0003-T1098 | NJT-0083；NJS-0083-001、NJS-0083-002、NJS-0083-003 |
| 4 | T1547 | Boot or Logon Autostart Execution | TA0003 retain，DEC-TA0003-T1547 | NJT-0084；NJS-0084-001、NJS-0084-002、NJS-0084-003 |
| 5 | T1037 | Boot or Logon Initialization Scripts | TA0003 retain，DEC-TA0003-T1037 | NJT-0085；NJS-0085-001、NJS-0085-002 |

这五项是总体任务范围，不是五项正式 NJT 的产量承诺。当前批次只研究 T1134；其准入结论和 Niji 子技术数量均由证据与 taxonomy 门禁决定。T1098、T1547 和 T1037 后续仍需分别判断 TA0004 是否应复用、扩展或拆分已有 Persistence 对象。

## 固定基线完整父候选清单

TA0004 的冻结展示顺序共十三项：T1548 Abuse Elevation Control Mechanism、T1134 Access Token Manipulation、T1098 Account Manipulation、T1547 Boot or Logon Autostart Execution、T1037 Boot or Logon Initialization Scripts、T1543 Create or Modify System Process、T1484 Domain or Tenant Policy Modification、T1611 Escape to Host、T1546 Event Triggered Execution、T1068 Exploitation for Privilege Escalation、T1055 Process Injection、T1053 Scheduled Task/Job、T1078 Valid Accounts。第六至第十三项只冻结顺序，不进入本次前五项开发。

## 基线与交付批次

- 战术：TA0004 Privilege Escalation。
- ATT&CK domain：enterprise-attack。
- ATT&CK version：19.1；本程序不迁移版本。
- 当前交付批次候选：仅 T1134。
- 前一批次门禁：BATCH-TA0004-001 已完成；T1548 的证据、taxonomy、字段深度、防御对象、机器校验、Bundle 与双语 Web QA 均通过。
- 本批次所有门禁通过前，BATCH-TA0004-003 不得进入正式 YAML 写入。

五项均采用单候选批次。T1134 虽含五项 ATT&CK 子技术、未触发 6+ 强制覆盖表规则，但 Windows 令牌类型、进程/线程承载体、身份与权限位变化、进程谱系以及 SID-History 相邻技术边界共同构成复杂 taxonomy 和防御设计，因此单独交付。

## 父技术边界

| 候选 | 直接行为对象 | 与兄弟候选和既有技术的边界 |
|---|---|---|
| T1134 | Windows 访问令牌所表达的有效安全上下文，以及令牌向线程或进程的绑定和使用 | T1548 以提权控制路径及其授权事务为对象；T1098/NJT-0083 以身份主体的持久认证或授权边为对象；T1055 以代码进入另一进程的执行地址空间为对象；T1068 以软件漏洞利用为对象。仅创建新进程、改变显示父进程或拥有管理员凭据，不自动构成 T1134 的 TA0004 行为 |

T1134 父页面只能锚定父级行为与 TA0004 映射。Niji 子技术、匿迹机理、检测关联、缓解效果和案例归因必须另有结论级证据；PPID 欺骗若不伴随更高安全上下文，只作为隐匿或谱系操纵的相邻语义，不由本 TA0004 对象扩张吸收。

## T1134 taxonomy breadth 先验

固定基线包含五项 ATT&CK 子技术。研究至少检查两个实质不同的匿迹轴，并逐项或逐簇记录覆盖决议：

| ATT&CK 子技术 | 英文名称 | 代表的实现或行为维度 | 初始覆盖状态 |
|---|---|---|---|
| T1134.002 | Create Process with Token | 以既有或新建令牌启动不同安全上下文的新进程 | pending |
| T1134.003 | Make and Impersonate Token | 从凭据创建登录会话/令牌并在线程上模拟 | pending |
| T1134.004 | Parent PID Spoofing | 显式选择父进程并可能继承其上下文，改变可见谱系 | pending |
| T1134.005 | SID-History Injection | 修改目录对象 SID-History，使后续令牌包含额外授权 SID | pending |
| T1134.001 | Token Impersonation/Theft | 复制既有令牌并绑定到线程、现有进程或新进程 | pending |

首轮候选轴包括：保持进程载体而替换线程有效身份；以外来令牌创建进程并解耦创建者、显示父级与安全上下文谱系；在同一令牌内选择性激活已有权限位；延迟保存并使用令牌；令牌来源、令牌类型和模拟级别差异；以及 SID-History 持久授权边。每个轴必须最终标为 formal、hypothesis、parent-core、adjacent、deferred 或 rejected，并记录攻击者可控性、边界稳定性、痕迹变化、观察/关联/归因效果、前提、证据和防御差异。

最终正式 Niji 子技术数不得按五项 ATT&CK 子技术设定配额，也不得按 API、工具、产品、Windows 版本、令牌字段、进程名称或目标权限拆分。零个子技术允许；任何正式轴必须同时通过全部匿迹变量门禁。

## 共享库与证据门禁

研究前后查询 references、claims、cases、detections、analytics、mitigations 和 relationships 七类共享库。先按稳定键和语义查重，再为每个对象记录 reuse、extend、create、split 或 defer；只有语义、适用目标和因果结论相同才复用。

| 稳定键/语义 | 类型 | 可能复用的候选 | 当前决议 |
|---|---|---|---|
| ATTACK-v19-T1134 | REF | T1134 父行为与 TA0004 映射 | pending lookup |
| TOKEN-CARRIER-EFFECTIVE-IDENTITY-LINEAGE | DET/NJA | 令牌来源、线程/进程承载体、登录会话、创建者与高权限后继活动的关联 | pending semantic lookup |
| TOKEN-PRIVILEGE-DELTA-OUTCOME | DET/NJA | 已有权限位启用、令牌变更与首个敏感操作的关联 | pending semantic lookup |
| WINDOWS-TOKEN-AUTHORITY-GOVERNANCE | MIT | 令牌权限最小化、特权 API/用户权限约束、句柄保护与谱系保真 | pending semantic lookup |

ATT&CK 页面不能统一支持子技术、机理、Analytic、Mitigation Application 或案例结论。定义、边界、正式轴、每项机理和防御对象都必须有原子 Claim 与适当层级 Reference；无法达到结论强度的候选轴保持 hypothesis 或 deferred。

## 内容深度与验收

T1134 的 definition_and_concept、stealth_characteristics、scope_boundary_definition、application_scenarios、attacker_model、defender_model 和 research.limitations 必须完整回答字段规范问题。中英文逐段配对并保持相同范围、强度和限制；威胁模型必须明确令牌访问权、所需 Windows 权限、载体选择、跨遥测关联假设及正常管理噪声，不能复用 T1548 的通用正文。

正式写入后运行 `make quality`、构建该 NJT bundle、运行 `pipeline_status.py`、确认无未解释 reserved ID，并在 Review Web 运行 `npm test`。随后检查父项、全部正式子项、DET/NJA、MIT 逐目标应用、证据和原始 YAML 的中英文页面。所有新对象在没有人工领域审查时保持 `review`。

## 执行安排

- 本任务未请求 sub-agent 或并行研究，主 Agent 顺序完成当前单候选批次。
- T1134 暂存路径：`planning/runs/BATCH-TA0004-002/`。
- 在 taxonomy、证据、共享对象和准入结论收敛前不分配正式 ID、不写 canonical YAML。
- 重点重叠：线程级模拟与进程级安全上下文、PPID 欺骗与纯谱系隐匿、SID-History 与 T1098/NJT-0083 持久授权边、权限位启用与 T1548 控制路径、代码注入与 T1055。
- 首轮开放假设：进程内有效身份替换、令牌谱系解耦进程创建、选择性权限位激活、延迟令牌使用及最小权限集激活。它们必须逐一通过证据和 taxonomy 门禁。
