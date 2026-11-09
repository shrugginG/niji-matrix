"""Literal candidate-specific primary edits; called only after all handoffs return.

No prose expansion by name substitution. Extra data contracts describe the actual
conditional branches in the reviewed analytics and do not claim deployed sensors.
"""
from copy import deepcopy


def paragraph(zh, en):
    return {'zh': zh, 'en': en}


def object_key(o):
    return o.get('key', o.get('temporary_key'))


def apply_primary_edits(attack, source):
    h = deepcopy(source)
    p = h['proposed_content']
    analytics = {object_key(o): o for o in h['defense_candidates']['detection_analytics']}
    if attack == 'T1201':
        a = analytics['B016-T1201-NJA-WINDOWS']
        a['logic']['paragraphs'][0] = paragraph(
            '基础分支从启用完整命令行的 4688 记录解析 net 或 net1 的 accounts 只读语义，保留 /domain 等目标范围；带设置参数的请求转给策略修改分析，帮助或语法错误保留原状态。按主机、登录 ID、进程 ID 和创建时间恢复可验证的进程谱系，避免 PID 重用。事件记录的创建主体不一定代表新进程的实际安全上下文；目标主体字段依版本和记录而定，缺失时保持未知。仅有启动事件时输出 policy_query_attempt，不推断进程退出、读取成功或具体约束。',
            'The base branch parses read-only accounts semantics in net or net1 from event 4688 with full command lines, retaining scope such as /domain. Route setting arguments to policy-mutation analysis and retain help or syntax-error context. Recover verifiable lineage by host, logon ID, process ID, and creation time to avoid PID reuse. The recorded creator need not represent the new process security context; target-subject fields depend on event version and availability and remain unknown when absent. A launch alone yields policy_query_attempt rather than process completion, read success, or particular constraints.')
        a = analytics['B016-T1201-NJA-AWS']
        a['logic']['paragraphs'][1] = paragraph(
            '对比同一账号的密码更新界面、账号管理作业与角色来源，来源网络、会话角色或用途明显偏离时产生调查候选，十五分钟内的其他目录或认证相关操作只用于排序。无错误只能作为服务处理状态的线索，responseElements 对只读操作通常为空，不能声称已经从审计恢复最小长度、复杂性或锁定阈值。本分析保留请求层结论；客户端返回内容的采集与验证属于另行部署的结果分析。',
            'Compare with password-change interfaces, account-management jobs, and role origins in the same account, producing survey candidates for material deviations in network origin, session role, or purpose. Other directory or authentication-related operations within fifteen minutes affect ranking only. Absence of an error is an indication of service processing, while responseElements is generally null for read-only operations; audit does not reconstruct minimum length, complexity, or lockout thresholds. This analytic retains request-level conclusions. Collecting and validating client responses requires a separately deployed result analysis.')
        a['correlation']['dimensions'] = [x for x in a['correlation']['dimensions'] if x != 'request_id']
        a['tuning_guidance']['paragraphs'].append(paragraph(
            '将缺失 errorCode、errorMessage 和不适用的角色会话字段规范化为 null，保留事件而不因空字段丢弃成功或直接 IAM 用户请求。role_session 从 userIdentity 的会话结构派生，非角色调用保留未知或不适用。',
            'Normalize absent errorCode, errorMessage, and inapplicable role-session fields to null, retaining successful and direct IAM-user requests rather than discarding them. Derive role_session from userIdentity session structure and keep non-role callers unknown or not applicable.'))
        a = analytics['B016-T1201-NJA-SAMR']
        a['logic']['paragraphs'][1] = paragraph(
            '以精确接口与操作匹配的告警作为请求证据，flow_id、源/目的地址以及可得的 SMB session_id 和 RPC call_id 用于上下文旁证，不作为跨多个命名管道或绑定的唯一调用标识。绑定事件中的接口列表不能证明同流每个请求都属于该接口；基础分支依赖解析器正确执行接口匹配，关联条件不足时保持请求命中而不重建完整调用。对未登记来源或偏离正常密码管理流程的请求产生调查候选。SMB status 和 RPC RESPONSE 只证明对应层状态；本分析不输出 SAMR 应用成功或密码约束内容，需要返回值时另部署经过 NDR 验证的解码与结果来源。',
            'Use alerts from exact interface and operation matching as request evidence. flow_id, endpoint addresses, and available SMB session_id and RPC call_id provide context rather than a unique call identity across multiple named pipes or bindings. An interface list in a bind event does not assign every request in the flow to that interface. The base branch relies on correct parser interface matching; inadequate association retains the request hit without reconstructing a complete call. Investigate unregistered origins or deviations from normal password-management work. SMB status and RPC RESPONSE establish their respective layer states. This analytic does not report SAMR application success or password constraints; returned values require separately deployed NDR-validated decoding and result data.')
        a['tuning_guidance']['paragraphs'].append(paragraph(
            '关联分支中的 request、opnum 和接口字段按事件类型允许为空；接口信息主要位于绑定记录。用同流多命名管道和多接口测试确认规则引擎的关联，不能只用 flow_id 与 call_id 推定应用层结果。',
            'Allow request, opnum, and interface fields to be null according to event kind in the correlation branch; interface information mainly occurs in bind records. Test multiple named pipes and interfaces in one flow to verify rule-engine association, and never infer application results from flow_id and call_id alone.'))

    if attack == 'T1120':
        p['application_scenarios_and_threat_model']['threat_model']['attacker_model']['paragraphs'][0] = paragraph(
            '攻击者需要能提交具有外围设备查询语义的请求，或保有能够解释设备变更反馈的应用、服务或会话；实际取得事实是需要另行确认的结果。普通用户可访问的设备元数据和需要额外设备访问权限的操作不同，不能统一假设管理员权限。通知驱动实现还需要保持处理上下文存活、正确解释通知类型，并接受未发生变更时没有新增事实；设备打开或内容读取可能仍被访问控制拒绝。',
            'The adversary needs to submit requests with peripheral-query semantics or retain an application, service, or session that can interpret device-change feedback. Acquiring facts is a separately confirmed outcome. Ordinary-user metadata access differs from operations requiring additional device authority, so administrator access is not universally assumed. Notification-driven implementations need a live handling context, correct notification interpretation, and tolerance for no new facts while no change occurs. Device opening or content reading may remain denied.')
        p['stealth_characteristics']['paragraphs'][1] = paragraph(
            '有意把反复枚举改为等待设备变更反馈，可以使安静阶段主要保留接收上下文与存活进程，把补充查询集中到实际变更附近。这样会削弱依赖重复执行或短窗口查询量的分析，但接收关系、消息处理、后续设备访问及输出仍可作为关联点；默认广播不要求每次都能观察到显式注册。高频插拔、重放事件和启动时快照会增加活动量，通知驱动也不意味着痕迹消失。',
            'Deliberately replacing repeated enumeration with device-change feedback can leave mainly a receiving context and resident process during quiet periods, concentrating supplementary queries around actual changes. This weakens analytics relying on repeated execution or short-window query counts, while reception, message handling, later access, and output remain correlation points. Default broadcasts do not require an observable explicit registration each time. Frequent hotplug changes, replayed events, and startup snapshots can increase activity; notification-driven operation does not remove traces.')
        work_source = {
            'source_type': 'approved-peripheral-work',
            'name': paragraph('设备支持任务与主机身份映射', 'Device-support work and host identity mapping'),
            'channel': 'Managed asset inventory and approved support jobs',
            'required_fields': ['host_id', 'host_aliases', 'principal', 'executable', 'mode', 'device_scope', 'job_id', 'valid_from', 'valid_to']}
        result_source = {
            'source_type': 'conditional-device-query-result',
            'name': paragraph('仅启用结果分支时的可信设备查询输出', 'Trusted device-query output only when the result branch is enabled'),
            'channel': 'Separately deployed authorized stdout or result-artifact collection',
            'required_fields': ['host_id', 'timestamp', 'process_id', 'process_start', 'query_scope', 'result_content', 'result_validated', 'collector_id']}
        for a in analytics.values():
            a['data_requirements'].append(deepcopy(work_source))
        a = analytics['B016-T1120-NJA-WINDOWS-QUERY']
        a['data_requirements'] += [{
            'source_type': 'conditional-device-query-script',
            'name': paragraph('仅启用脚本分支时的重组 PowerShell 内容', 'Reconstructed PowerShell content only when script enrichment is enabled'),
            'channel': 'Microsoft-Windows-PowerShell/Operational event 4104 when configured',
            'required_fields': ['host_id', 'timestamp', 'process_id', 'script_block_id', 'message_number', 'message_total', 'script_block_text']}, deepcopy(result_source)]
        a['tuning_guidance']['paragraphs'].append(paragraph(
            '脚本分支先重组 ScriptBlockId、MessageNumber、MessageTotal 与 ScriptBlockText；利用资产清单将 Computer 与 XDR DeviceId 映射到同一 host_id，无法映射时分别保留，不强行连接。结果分支的输出必须绑定同一进程生命周期与实际查询范围；未部署相应采集时停留在请求等级。',
            'Reconstruct ScriptBlockId, MessageNumber, MessageTotal, and ScriptBlockText before script enrichment. Use the asset inventory to map Computer and XDR DeviceId to one host_id; retain separate records if mapping is unavailable. Bind supplemental output to the same process lifetime and actual query scope, retaining request-level conclusions when that collection is not deployed.'))
        for suffix in ['LINUX-QUERY', 'LINUX-MONITOR']:
            a = analytics['B016-T1120-NJA-' + suffix]
            a['data_requirements'][0]['required_fields'] = ['host_id' if x == 'node' else x for x in a['data_requirements'][0]['required_fields']]
            a['correlation']['dimensions'] = ['host_id' if x == 'node' else x for x in a['correlation']['dimensions']]
            a['tuning_guidance']['paragraphs'].append(paragraph(
                'host_id 来自可信采集来源并与资产清单核对，原始 audit node 存在时另行保留，不能假定默认日志一定含 node。按 host_id 与 audit_serial 拼接，缺少主机身份时禁止跨机合并；执行事件时间可作为该次进程起点，但后续 PID 关联仍须排除重用。',
                'Derive host_id from a trusted collection origin and verify it against inventory, retaining native audit node separately when present rather than assuming it exists by default. Join by host_id and audit_serial and prohibit cross-host merging without identity. Execution time can establish this process start, but later PID joins must still exclude reuse.'))
        a = analytics['B016-T1120-NJA-LINUX-QUERY']
        a['logic']['paragraphs'][1] = paragraph(
            '用可信采集来源的 host_id、auid、ses、pid 与事件时间连接执行者、登录会话及批准作业，区分宿主机设备视图和受限容器视图。对非设备管理角色发起全库导出、跨多类属性遍历或来自已知入侵会话的查询生成线索。SYSCALL success 仅说明执行系统调用状态，不提供查询返回内容；没有实际 stdout 或结果文件验证时，保留查询已发起且结果未知。',
            'Use trusted collector-origin host_id, auid, ses, pid, and event time to join execution, login session, and approved work, distinguishing host from restricted-container views. Generate leads for whole-database exports by non-device-management roles, walks across classes, or queries from a known compromised session. SYSCALL success establishes execution-syscall status rather than query content. Without actual stdout or validated files, retain query-issued and result-unknown status.')
        a['data_requirements'].append(deepcopy(result_source))
        a = analytics['B016-T1120-NJA-LINUX-MONITOR']
        a['data_requirements'].append({
            'source_type': 'conditional-device-monitor-output',
            'name': paragraph('仅启用反馈确认时的实际监听输出', 'Actual monitor output only when feedback confirmation is enabled'),
            'channel': 'Separately deployed authorized stdout capture for the selected udevadm monitor process',
            'required_fields': ['host_id', 'timestamp', 'process_id', 'process_start', 'action', 'devpath', 'subsystem', 'collector_id']})
        a['tuning_guidance']['paragraphs'].append(paragraph(
            '反馈分支把输出中的 ACTION、DEVPATH 与 SUBSYSTEM 映射为规范键，同时保留采集时间和进程起点。无输出或无法证明输出来自该监听器时，保留反馈未知，不将系统 udev 记录补造成应用收到的消息。',
            'Map ACTION, DEVPATH, and SUBSYSTEM from captured output to canonical keys while retaining collection time and process start. Missing output or unverified listener provenance leaves feedback unknown; system udev records must not be substituted for messages received by the application.'))
        case = next(x for x in h['library_candidates']['cases'] if object_key(x) == 'B016-T1120-CASE-ATTOR-DEVICE')
        case['time_range'] = None
        case['target_sectors_zh'] = []
        case['target_sectors_en'] = []

    if attack == 'T1069':
        p['application_scenarios_and_threat_model']['application_scenarios']['paragraphs'][0] = paragraph(
            '获得本地执行、域身份或云会话后，操作者可能先调查管理员、备份运维或特定资源关联组，选择后续凭据目标并核查可能的访问路径。ESET 的 ComRAT 调查列出本地和域组命令，提供父行为的实际活动证据；总体受害机构不能直接绑定到每条命令。报告未给逐命令完整返回，也未给组关系直接导致后继成功访问的逐步记录。',
            'After obtaining local execution, a domain identity, or a cloud session, an operator can survey administrative, backup-operation, or resource-related groups to select credential targets and investigate potential access paths. ESET lists local and domain group commands in its ComRAT investigation, providing evidence of the parent behavior in actual activity; aggregate victim institutions cannot be assigned to each command. The report lacks per-command complete outputs or a stepwise demonstration that a relationship caused successful later access.')
        case = h['library_candidates']['cases'][0]
        case['time_range'] = None
        case['target_sectors_zh'] = []
        case['target_sectors_en'] = []
        a = analytics['B016-T1069-NJA-IAM']
        a['tuning_guidance']['paragraphs'].append(paragraph(
            '保留原始 userIdentity，按原生 ARN、principalId 与 accessKeyId 派生规范会话键。errorCode 缺失时显式规范为 null，不能因必需键列表而丢弃成功读取；请求参数按对应 API 允许为空，关系范围也不能由空参数推断为全量。',
            'Retain raw userIdentity and derive canonical session keys from native ARN, principalId, and accessKeyId. Normalize absent errorCode to null instead of dropping successful reads because of a required-key list. Parameters can be null according to the API, and absent parameters do not imply complete scope.'))
    if attack in {'T1057', 'T1012'}:
        a = analytics['B016-T1057-NJA-RESIDENT' if attack == 'T1057' else 'B016-T1012-NJA-INPROCESS']
        a['data_requirements'].append({
            'source_type': 'conditional-query-carriage-proof',
            'name': paragraph('仅启用承载确认时的查询任务与实现证明', 'Query-task and implementation proof only when carrier confirmation is enabled'),
            'channel': 'Independently verified task records, executing-code provenance, or authorized call-chain capture',
            'required_fields': ['client_host', 'process_instance_id', 'task_id', 'query_scope', 'task_start', 'task_end', 'carriage_mode', 'evidence_locator', 'verification_state']})
        a['tuning_guidance']['paragraphs'].append(paragraph(
            '承载确认分支要求证明材料关联到被观察的同一客户端实例、任务范围与时点，并验证实际执行的入口或调用链；仅有通用产品文档、API 导入或可能存在的代码不能提升等级。没有该来源时仍可运行查询检测，但承载方式和有意替代保持未知。',
            'Carrier confirmation requires evidence tied to the same observed client instance, task scope, and time, verifying the executing entry or call chain. Generic product documentation, imports, or possibly present code do not raise the level. Query detection can run without this source, but carrier selection and deliberate substitution remain unknown.'))
    if attack == 'T1057':
        a = analytics['B016-T1057-NJA-UTILITY']
        a['data_requirements'].append({
            'source_type': 'conditional-process-query-output',
            'name': paragraph('仅启用结果确认时的可信进程查询输出', 'Trusted process-query output only when result confirmation is enabled'),
            'channel': 'Separately deployed authorized stdout or result-artifact capture',
            'required_fields': ['host_id', 'timestamp', 'process_instance_id', 'target_host', 'query_semantics', 'result_content', 'collector_id', 'result_validated']})
        for ref in h['library_candidates']['references']:
            if object_key(ref) == 'B016-T1057-REF-TRUSTEDSEC-SOURCE':
                ref['url'] = 'https://github.com/trustedsec/CS-Situational-Awareness-BOF/tree/fd96c4dcd88fd00eea902bebb20d0736e48f5f61'
            if object_key(ref) == 'B016-T1057-REF-BOF':
                ref['title_zh'] = 'Beacon Object Files 官方文档'
                ref['title_en'] = 'Beacon Object Files'
                ref['notes_zh'] = '官方明确比较每任务创建与注入和 Beacon 内执行的足迹，说明短任务、阻塞与崩溃约束。文档支持能力和设计目的，不证明任何特定恶意主体采用、所有 API 无日志或实测逃逸率；进程与注册表查询各需独立行为证据。'
                ref['notes_en'] = 'The official documentation compares per-task creation and injection with execution inside Beacon and describes short-task, blocking, and crash constraints. It supports capability and design purpose, not adoption by a particular malicious actor, absent API telemetry, or measured evasion. Process and Registry inquiries each require independent behavioral evidence.'
    if attack == 'T1012':
        h['recommendation']['decision'] = 'adapt'
        h['recommendation']['rationale']['paragraphs'][0] = paragraph(
            '保留固定 Enterprise 19.1 T1012 的注册表信息读取行为，并将正式范围收敛为一般环境配置探索及尚未确定专门信息结果的查询尝试。原基线也用软件等具体信息举例；这些结果在 Niji 中按直接目的由各自发现技术承担，不能因同样使用 Registry 再建立一个父级结果。联合公告证明 reg query 的实际使用，ESET 另证明一般键、值和数据枚举能力，官方文档界定读取与结果语义，因此采用 adapt 明确分流而不否定原行为。',
            'Preserve Registry information reads from fixed Enterprise 19.1 T1012 while converging formal scope on general environmental-configuration exploration and query attempts whose specialized information result remains unresolved. The baseline also illustrates specific information such as software; Niji assigns those results to their direct-purpose discovery owners rather than creating a second parent result merely because Registry access is used. The joint advisory establishes actual reg query use, ESET independently establishes general key, value, and data enumeration, and official documentation defines read and result semantics. Adapt makes this routing explicit without rejecting the original behavior.')
        p['name']['zh'] = '注册表查询'
        for field in ['definition_and_concept', 'stealth_characteristics']:
            for q in p[field]['paragraphs']:
                q['zh'] = q['zh'].replace('查询注册表是', '注册表查询是').replace('查询注册表借用', '注册表查询借用')
        q = p['research']['limitations']['paragraphs'][0]
        q['zh'] = q['zh'].replace('不冒充现场采用率或 measured evasion', '不等同于现场采用率或实测匿迹效果')
        case = h['library_candidates']['cases'][0]
        case['description_zh'] += ' 公告的汇总命令列表仅证明这种查询实现被使用，不能确定其每次直接信息目的；专门软件等结果不由本案例重复认定为一般配置结果。'
        case['description_en'] += ' The aggregate command list establishes use of the query implementation rather than every immediate information objective. Specific software or other specialized results are not reclassified by this case as general configuration results.'
        for a in analytics.values():
            for field in ['logic', 'tuning_guidance']:
                for q in a[field]['paragraphs']:
                    q['zh'] = q['zh'].replace('NJA-ACCESS', '键读取权限分析')
                    q['en'] = q['en'].replace('NJA-ACCESS', 'the key-read-rights analytic')
        a = analytics['B016-T1012-NJA-INPROCESS']
        a['logic']['paragraphs'][1] = paragraph(
            '同一进程实例的直接操作记录首先支持已观察驻留进程读取。只有任务记录、实际执行代码或调用链与该次查询正面关联，才能进一步标记驻留承载得到支持；同期采集完整且任务边界明确时，才比较每任务执行器是否被省去，缺少新进程本身不提高等级。可用栈解析时检查模块与批准职责的关系，结合环境探索范围和未批准来源排序。没有相应证明来源时保留查询线索与承载未知，不凭 COFF 装载或注入事件认定本子项。',
            'Direct operation records for the same process instance first establish an observed resident-process read. Raise the level to supported resident carriage only when task records, executing code, or a call chain positively link to that inquiry. Compare omission of a per-task executor only with complete contemporaneous capture and an established task boundary; missing process events alone do not raise the level. Where stack resolution exists, compare modules with approved duties and rank environmental scope and unapproved provenance. Without the required proof source, retain a query lead with carrier unknown rather than confirming this child from COFF loading or injection.')
        a['field_mapping']['zh'] += ' 本专用分析的直接归属分支限于本地读取，client_host 对应捕获主机 host_id；远程服务端 PID 不能直接当作远端查询客户端，跨机实现需要独立的两端会话与任务证明。'
        a['field_mapping']['en'] += ' The direct-attribution branch of this dedicated analytic covers local reads, with client_host mapped to capture-host host_id. A remote service PID is not the remote query client; cross-host implementations need independent evidence joining both endpoint sessions and tasks.'
    return h
