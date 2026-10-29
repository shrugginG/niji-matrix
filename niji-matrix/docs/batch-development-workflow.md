# 匿迹技术批次开发工作流

本文说明如何使用项目级 niji-matrix-authoring Skill，启动并完成一个由多个 ATT&CK 父技术候选组成的正式研究批次。

## 一、工作单元

三个层级承担不同职责：

| 层级 | 含义 |
|---|---|
| 战术 | 持续开发和最终验收范围 |
| 批次 | 一次连续任务实际处理的候选集合 |
| 技术候选 | 准入研究和正式编写的原子工作单元 |

一次批次可以处理同一战术中的多个候选，但批次完成不等于战术完成。用户在一个任务中给出的候选清单是总体项目范围，不等于一个同时编写的交付批次；同一任务可以连续完成多个小批次。只有完整候选清单、全部准入决策、Niji 缺口分析和战术级交叉审查均完成，才能关闭一个战术。

### 总体范围与交付批次

默认每个交付批次处理一至三个 ATT&CK 父候选；证据、分类、威胁模型或防御设计复杂的候选应单独成批。超过三个候选的批次必须在 batch brief 中说明扩大规模的理由，并证明每个候选仍有独立证据审查和内容深度门禁。上下文压缩、任务耗时或尽快关闭战术的愿望都不能降低质量标准。

当前批次中的每个候选必须通过证据、准入、分类、双语正文、防御对象、机器校验、Bundle 和 Web QA 后，下一批才能进入正式写入。相邻候选可以提前研究，但不得提前污染正式 ID 和共享库决议。

## 二、启动前提

正式启动前必须确认：

1. 当前工作目录可以发现项目级 niji-matrix-authoring Skill；
2. matrix.yaml 中的 ATT&CK domain 和 version 已锁定；
3. 候选是 ATT&CK 父技术，不把 ATT&CK 原子技术作为 Niji 子技术；
4. 对应战术计划存在于 planning/tactics/；
5. 当前正式矩阵、规划层和共享库审计通过；
6. Web 审阅工具能够读取当前矩阵。

预检命令：

    cd niji-matrix
    make quality
    python3 scripts/pipeline_status.py
    python3 scripts/allocate_id.py list --status reserved

如果存在校验错误、未解释的重复项或其他批次遗留的 reserved ID，应先处理再启动。

## 三、选择和登记批次

### 1. 锁定候选

按照 matrix.yaml 指定的固定 ATT&CK 版本，从目标战术页面或版本化数据中选取父技术，并记录：

- ATT&CK ID；
- 英文父技术名称；
- 候选中文工作名；
- 页面或 STIX 来源；
- 候选顺序；
- 已存在的决策或技术；
- 该父技术在固定基线中的 ATT&CK 子技术数量、ID、所代表的实现/行为维度，以及适用的 taxonomy breadth trigger。

五个 ATT&CK 候选表示五项候选必须完成准入判断，不表示必须产生五项正式 Niji 技术。若总体任务包含约十个或更多候选，应把完整清单登记为项目范围，再按默认一至三项拆成连续交付批次，而不是一次性进入正式编写。

### 2. 分配批次和工作项名称

使用以下格式：

    BATCH-<TACTIC-ID>-<三位批次号>
    WORK-<TACTIC-ID>-<ATTACK-ID或NIJI候选号>

例如：

    BATCH-TAxxxx-001
    WORK-TAxxxx-Txxxx

### 3. 更新战术计划

在 planning/tactics/<TA-ID>.yaml 中：

- 把批次加入 batches；
- 把候选加入 work_items；
- 将批次状态设为 active；
- 将工作项状态设为 researching；
- 更新 candidate_inventory.last_synced；
- 保持 candidate_inventory.status 为 partial，直到战术完整清单建立。

运行：

    python3 scripts/validate_planning.py

## 四、建立批次共同约束

复制 planning/templates/batch-brief.md 到：

    planning/runs/<batch-id>/batch-brief.md

主 Agent 在分派研究前填写：

- 总体任务候选清单与当前交付子集；
- 当前批次规模及其理由；
- 前一批次的证据、内容、机器和 Web 门禁状态；
- 候选列表；
- 每个父技术的直接信息或行为对象；
- 候选之间的边界；
- 与已有 Niji 技术的边界；
- 不允许继承 ATT&CK 子技术；
- 公开或被动行为必须具备何种匿迹因果链；
- 本批次共享库复用和临时键规则；
- 每个 ATT&CK 父候选的子技术广度先验、覆盖决议要求与第二轮 taxonomy 条件。

这份 brief 是所有并行研究者共同遵守的分类约束。

## 五、共享库预检

研究前生成当前库目录：

    make catalog
    python3 scripts/audit_duplicates.py --fail-on exact

对已知来源执行查询：

    python3 scripts/library_lookup.py --doi <DOI>
    python3 scripts/library_lookup.py --url <URL>
    python3 scripts/library_lookup.py --text "<标题或概念>"

处理原则：

- 已有完全相同来源直接复用；
- 语义完全相同的案例、检测、缓解或主张扩充适用对象；
- 同名但因果、数据源或适用范围不同的对象拆分；
- 不确定对象使用临时键并等待主 Agent 决议。

每项候选都必需的 ATT&CK 父技术官方页面可以由主 Agent 提前集中建库。NJT、NJS、Claim、Case、Detection Strategy、Detection Analytic、Mitigation 和 Relationship 应等待准入与分类收敛后再分配，避免为被舍弃或合并的候选浪费编号。

## 六、并行研究

### 1. 并行方式

根据可用并发槽位分轮次执行。例如五项候选可采用：

    第一轮：候选 A、B、C
    第二轮：候选 D、E

主 Agent 在并行期间负责：

- 维护批次计划；
- 维护共享来源候选；
- 通知其他代理已经发现的公共来源；
- 为下一轮刷新共享库目录；
- 准备跨技术边界。

### 2. Sub-agent 合同

每名 Sub-agent 必须：

- 读取项目 Skill、字段规范、防御对象规范、NJT-0001 范例、共享库规则和 batch brief；
- 只研究一个候选；
- 先给出 retain、adapt 或 exclude；
- 从匿迹实现变量独立提出 Niji 子技术；
- 记录 ATT&CK 子技术数量与维度作为广度先验，不导入其分类；3–5 项时审查至少两个候选匿迹轴，6+ 时提交覆盖表与第二轮 taxonomy 结果；
- 为每个机理建立行为—痕迹—防守影响因果链；
- 查询已有全局库；
- 已确认对象使用正式 ID，新对象使用唯一临时键；
- 不分配正式 ID；
- 不修改 matrix、references、claims、cases、detections、analytics、mitigations 或 relationships；
- 报告直接证据、推断、假设和限制。

推荐临时键：

    <批次缩写>-<候选ID>-REF-01
    <批次缩写>-<候选ID>-SUB-01
    <批次缩写>-<候选ID>-CLM-01

### 3. 交接内容

交接应包含：

- 准入结论和置信度；
- 父技术的定义与概念、匿迹特性、范围边界界定、应用场景及攻防威胁模型；
- 父级机理映射；
- 子技术名称、区分变量、因果链和证据；
- ATT&CK 子技术数量、ID、维度聚类、逐项或逐簇覆盖决议、候选匿迹轴、第二轮状态及数量差异解释；
- 已有全局对象复用建议；
- 新 Reference、Claim、Case、Detection Strategy、Detection Analytic、Mitigation 和 Relationship 候选；
- 延迟或拒绝建立的分类及原因；
- 双语核心内容。

交接应结构清晰而不是复制大段原文，并记录结论级证据覆盖与 NJT-0001 字段责任对照。固定版本 ATT&CK 父页面只锚定父行为和战术映射，不能自动支持全部 Niji 子项、机理、检测假设、缓解效果或案例结论。优先使用 planning/templates/technique-research-handoff.yaml。若运行环境无法写入交接文件，Sub-agent 必须在最终消息中返回同样结构，主 Agent 将结果写入批次集成摘要。

## 七、轮次间共享库协调

每轮结束后，主 Agent：

1. 汇总所有临时来源和语义对象；
2. 按 DOI、RFC、ATT&CK ID、公告 ID、规范 URL 和语义指纹判重；
3. 将同一来源统一为一个临时键或正式 REF；
4. 向下一轮代理发布更新后的共享候选；
5. 重新生成 library catalog。

如果两个代理同时发现同一 CISA 公告，应按公告编号合并为一个 Reference 和一个 Case，而不是按各自技术复制。

## 八、主 Agent 收敛

主 Agent 将所有候选放在一起进行：

- 父技术信息对象去重；
- 子技术行为变量去重；
- ATT&CK 子技术广度先验与 Niji 输出差异审查，重点检查 6+ ATT&CK 子项却只收敛为 0–1 个 Niji 子项的候选是否过早停止；
- 与已有 Niji 技术的边界检查；
- 四种机理强度校准；
- 案例证据层级限制；
- 检测数据源和逻辑去重；
- 缓解措施受控对象去重；
- 跨技术关系设计；
- 双语结论一致性检查；
- 逐字段与 NJT-0001 比较问题覆盖、论证深度和自然表达；
- 检查跨候选相同限制、通用威胁模型和仅替换名称的机理分析。

临时候选必须归入以下一种决议：

| 决议 | 含义 |
|---|---|
| reuse | 完全复用现有对象 |
| extend | 复用现有对象并扩充适用对象或证据 |
| create | 创建新的全局规范对象 |
| split | 表面相似但语义不同，分别保留 |
| defer | 证据不足，暂缓进入正式矩阵 |

已审查的疑似重复项写入 planning/duplicate-resolutions.yaml。

## 九、正式 ID 和写入顺序

准入和分类收敛后，由主 Agent 集中预留：

    python3 scripts/allocate_id.py reserve NJT --count <数量> --owner <batch-id>
    python3 scripts/allocate_id.py reserve NJS --parent NJT-xxxx --count <数量> --owner <batch-id>
    python3 scripts/allocate_id.py reserve REF --count <数量> --owner <batch-id>

其他全局对象同样使用 CLM、CASE、DET、NJA、MIT、REL 类型。

脚本只可序列化已经逐候选审阅的内容、执行机械字段排序、ID 操作、构建和校验；不得通过替换候选名称批量生成正式读者正文、准入理由、Claim、机理因果链、子技术分类、Analytic 逻辑或 Mitigation Application。生成式草稿必须停留在批次暂存目录，经逐候选语义重写后才能进入正式库。

建议写入顺序：

1. References；
2. Claims、Cases、Detection Strategies、Detection Analytics、Mitigations、Relationships；
3. admission decisions；
4. YAML-only 2.0 technique.yaml（包含全部成对双语读者内容）；
5. YAML-only 2.0 evasion sub-technique YAML（与父技术共享核心字段，使用父级自包含 NJS ID）；
6. 战术计划和 batch integration summary。

正式对象写入并通过基本解析后执行：

    python3 scripts/allocate_id.py sync

确认没有悬空预留：

    python3 scripts/allocate_id.py list --status reserved

## 十、校验、构建和 Web 审阅

### 1. 内容深度门禁

在机器校验前逐个审查父技术和子技术。每个自然段字段必须回答字段规范中的全部问题；一至四段是结构范围，不是默认写一段。与 NJT-0001 的比较关注字段责任、因果完整度、证据强度、不确定性和双语自然度，不强制复制其段落数、字数或对象数量。跨候选统一一段式、完全相同的研究限制、通用威胁模型或只替换名称的机理分析，除非确有相同语义并记录理由，否则均不得通过。ATT&CK 子技术数量只作为研究广度先验：3–5 项触发多轴检查，6+ 项触发覆盖表与第二轮 taxonomy，10+ 项默认单候选批次；它不构成 Niji 子技术最低数、目标数或比例。高广度父技术收敛为 0–1 个子项时，必须记录其他候选轴为何在稳定性、痕迹变化、证据、兄弟边界或防御差异门禁失败。

### 2. 完整质量门禁

    make quality

必须满足：

- 正式内容 0 errors、0 warnings；
- 规划层 0 errors、0 warnings；
- 共享库 0 exact duplicates；
- 所有基础设施测试通过；
- 没有未解释的 possible duplicate。

### 3. 构建技术包

对每个 retain、adapt 或 add 的技术执行：

    python3 scripts/build_technique_bundle.py NJT-xxxx

exclude 候选只保存准入决策，不构建不存在的技术。

### 4. Web 审阅

在 niji-matrix-review 中运行：

    npm test

然后检查：

- 战术、技术和子技术导航；
- 中文和英文切换；
- 技术与子技术目录不包含 Markdown，页面不存在自由章节或手写表格；
- 定义、范围、上下文、防御和限制呈现为连续自然段，没有微型字段卡或项目符号堆砌；
- 由 YAML 字段生成的定义与概念、匿迹特性、范围边界、应用场景、攻防威胁模型、完整机理因果链与研究限制；
- Claim、Case、Detection Strategy、Detection Analytic、Mitigation 和 Reference；
- 跨对象跳转；
- 生命周期、版本和源文件；
- API issues 为 0。

## 十一、批次收尾

复制 planning/templates/batch-integration-summary.yaml，记录：

- 每项候选决策；
- 正式技术和子技术 ID；
- 复用、扩充和新建的共享对象；
- 延迟分类；
- 判重决议；
- 校验、测试、构建和 Web 结果。

更新战术计划：

- 工作项设置为 excluded、review 或 published；
- 批次设置为 review；
- 只有人工领域审查完成后才设置 published 或 complete；
- 人工审查发现系统性浅薄、证据越级或模板化正文时，将相关工作项和正式对象退回 draft，并重新执行候选级门禁；
- 战术仍有候选未处理时，candidate inventory 保持 partial。

## 十二、现行范例

正式内容统一以 [NJT-0001 规范范例](njt-0001-exemplar.md)为结构与质量基线，并同时遵守[技术与子技术字段规范](technique-field-specification.md)和[防御对象规范](defense-object-specification.md)。

范例要求复制的是字段责任、自然段写法、父子同构、父级自包含 NJS 编号、机理证据链、DET→NJA 组织以及 MIT 逐目标应用；不得复制其五个子技术、三类机理、证据数量或结论。历史批次材料只保留过程审计价值，不再定义现行内容合同。

## 十三、推荐调用方式

在当前项目中提出类似请求：

    使用 $niji-matrix-authoring，基于 matrix.yaml 中固定的 ATT&CK 基线，
    在 TAxxxx 下把指定父技术登记为总体任务范围，并默认拆成每批一至三项的连续交付批次；复杂候选单独成批。
    严格遵循字段规范与 NJT-0001 范例，使用受控并行研究，
    由主 Agent 统一完成准入、分类收敛、七类共享库去重、ID 分配、
    双语自然段写入、DET→NJA 与 MIT 应用建模、校验、构建和 Web QA。
    不得继承 ATT&CK 子技术；应把固定基线 ATT&CK 子技术数量作为研究广度先验并完成触发的覆盖/第二轮审查，但不得把它变成 Niji 输出配额；不得为了满足数量而强制保留候选，不得用名称替换模板批量生成正式正文；
    当前批次未通过结论级证据、字段深度、机器和双语 Web 门禁前，不得开始下一批正式写入。

任务结束时应同时交付正式内容、批次摘要、质量结果和“该批次完成但战术是否完成”的明确说明。
