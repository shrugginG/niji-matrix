"""Project independently reviewed research into canonical contracts.

No reader prose is expanded by candidate-name substitution. Semantic text is the
reviewed handoffs, explicit primary edits below and T1040-child-reviewed.yaml.
"""
from copy import deepcopy
from pathlib import Path
import json
import re
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
SCOPE = ['T1680', 'T1654', 'T1046', 'T1135', 'T1040']
H = {a: yaml.safe_load((RUN / 'normalized-handoffs' / f'{a}.yaml').read_text()) for a in SCOPE}
EXTRA = yaml.safe_load((RUN / 'T1040-child-reviewed.yaml').read_text())
SUPPLEMENT = yaml.safe_load((RUN / 'T1040-taxonomy-supplement.yaml').read_text())
IDS = json.loads((RUN / 'allocated-ids.json').read_text())
TODAY = '2026-11-05'
assert json.loads((RUN / 'research-input-manifest.json').read_text())['all_five_handoffs_complete']


def key(o):
    return o.get('key', o.get('temporary_key'))


def pair(o, field):
    if isinstance(o.get(field), dict):
        return deepcopy(o[field])
    return {'zh': o.get(field + '_zh', ''), 'en': o.get(field + '_en', '')}


def lifecycle():
    return {'status': 'draft', 'version': '0.1.0', 'created': TODAY, 'modified': TODAY,
            'contributors': ['Niji Matrix Research'], 'reviewers': []}


MAP = {f'B015-{a}-PARENT': IDS['parents'][a] for a in SCOPE}
MAP.update({'B015-T1046-NJS-ADVERTISEMENT-SUBSTITUTION': IDS['NJS'][0],
            'B015-T1040-NJS-NO-ACTIVE-ENRICHMENT': IDS['NJS'][1],
            'B015-T1654-REF-ATTACK': 'REF-000625',
            'B015-T1046-REF-ATTACK': 'REF-000625',
            'B015-T1135-REF-ATTACK': 'REF-000625',
            'B015-T1680-REF-AUDITCTL': 'REF-000840',
            'B015-T1046-REF-CISA-FIVEHANDS': None,
            'B015-T1040-MIT-OBSERVATION-GOVERNANCE-APPLICATION': 'MIT-000186'})


def mapped(v):
    if isinstance(v, str):
        return MAP.get(v, v)
    if isinstance(v, list):
        return [mapped(x) for x in v if not (isinstance(x, str) and x in MAP and MAP[x] is None)]
    if isinstance(v, dict):
        return {k: mapped(x) for k, x in v.items()}
    return v


references = [(a, deepcopy(r)) for a in SCOPE for r in H[a]['library_candidates']['references'] if key(r) not in MAP]
references.append(('T1040', deepcopy(SUPPLEMENT['primary_evidence'][1])))
assert len(references) == len(IDS['REF']) == 44
for (_, obj), ident in zip(references, IDS['REF'], strict=True):
    MAP[key(obj)] = ident

claims = [(a, deepcopy(r)) for a in SCOPE for r in H[a]['library_candidates']['claims']]
claims += [('T1040', deepcopy(r)) for r in EXTRA['claims']]
cases = [(a, deepcopy(r)) for a in SCOPE for r in H[a]['library_candidates']['cases']]
strategies = [(a, deepcopy(r)) for a in SCOPE for r in H[a]['defense_candidates']['detection_strategies']]
strategies.append(('T1040', deepcopy(EXTRA['strategy'])))
analytics = [(a, deepcopy(r)) for a in SCOPE for r in H[a]['defense_candidates']['detection_analytics']]
analytics.append(('T1040', deepcopy(EXTRA['analytic'])))
mitigations = [(a, deepcopy(r)) for a in SCOPE for r in H[a]['defense_candidates']['mitigations'] if r.get('existing_ref') is None]
for kind, objects in [('CLM', claims), ('CASE', cases), ('DET', strategies), ('NJA', analytics), ('MIT', mitigations)]:
    assert len(objects) == len(IDS[kind]), (kind, len(objects), len(IDS[kind]))
    for (_, obj), ident in zip(objects, IDS[kind], strict=True):
        MAP[key(obj)] = ident

CLAIM_TYPES = {
    'B015-T1680-CLM-OBSERVED': 'technique-relevance',
    'B015-T1680-CLM-BOUNDARY': 'technique-boundary',
    'B015-T1680-CLM-FEATURE-OVERLAP': 'mechanism-mapping',
    'B015-T1680-CLM-DEFENSE-LEVELS': 'detection',
    'B015-T1654-CLM-PARENT': 'technique-boundary',
    'B015-T1654-CLM-RESULT-GRADING': 'technique-boundary',
    'B015-T1654-CLM-FD': 'mechanism-mapping',
    'B015-T1654-CLM-FEEDBACK': 'technique-relevance',
    'B015-T1654-CLM-AZURE-AUDIT': 'detection',
    'B015-T1135-CLM-RESULT-BOUNDARY': 'technique-boundary',
    'B015-T1135-CLM-NATIVE-APPEARANCE': 'mechanism-mapping',
    'B015-T1135-CLM-RETURN-GRADING': 'detection',
    'B015-T1135-CLM-AUDIT-LIMIT': 'detection',
    'B015-T1135-CLM-ANONYMOUS-LIMIT': 'mitigation',
}

WRITTEN = []
OBJECTS = []


def reference_ids(v):
    found = set()
    if isinstance(v, str) and re.fullmatch(r'REF-\d{6}', v):
        found.add(v)
    elif isinstance(v, list):
        for x in v:
            found |= reference_ids(x)
    elif isinstance(v, dict):
        for x in v.values():
            found |= reference_ids(x)
    return found


def emit(relative, obj, owner):
    obj = mapped(obj)
    text = yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120)
    assert 'B015-' not in text, (relative, 'unresolved temporary key')
    assert '__REQUIRED' not in text
    assert 'planning/' not in text, (relative, 'canonical planning reference')
    path = ROOT / relative
    if path.exists():
        assert yaml.safe_load(path.read_text()) == obj, f'Refusing to overwrite different object {path}'
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    WRITTEN.append(relative)
    OBJECTS.append((owner, obj))


def slug(obj):
    return key(obj).removeprefix('B015-').lower()


allowed_source_types = set(json.loads((ROOT / 'schemas/reference.schema.json').read_text())['properties']['source_type']['enum'])
for owner, r in references:
    title = pair(r, 'title')
    assert title['zh'] and title['en'], key(r)
    source_type = r.get('source_type', 'official-documentation')
    if source_type not in allowed_source_types:
        source_type = 'sample-analysis' if 'analysis' in source_type else 'official-documentation'
    identifiers = {'doi': None, 'rfc': None, 'arxiv': None, 'attack_id': None, 'other': []}
    identifiers.update(r.get('identifiers', {}))
    if 'RFC6763' in key(r):
        identifiers['rfc'] = '6763'
    if 'RFC6762' in key(r):
        identifiers['rfc'] = '6762'
    notes = pair(r, 'notes')
    if not notes['zh'] and isinstance(r.get('supported'), dict):
        notes = deepcopy(r['supported'])
        if isinstance(r.get('limits'), dict):
            notes = {lang: notes[lang] + (' ' if lang == 'en' else '') + r['limits'][lang] for lang in ['zh', 'en']}
    url = r['url']
    if key(r) == 'B015-T1654-REF-NOPINEAPPLE':
        url = json.loads((RUN / 'primary-source-verification.json').read_text())['WithSecure_No_Pineapple']['verified_report_url']
    published = r.get('published')
    if published is not None:
        published = str(published)
    obj = {'schema_version': '1.0.0', 'type': 'reference', 'id': MAP[key(r)],
           'title_zh': title['zh'], 'title_en': title['en'], 'source_type': source_type,
           'identifiers': identifiers, 'authors': r.get('authors', []), 'publisher': r.get('publisher'),
           'published': published, 'url': url, 'accessed': TODAY,
           'locator': r.get('locator'), 'archive_url': r.get('archive_url'),
           'credibility': r.get('credibility', 'high'), 'notes_zh': notes['zh'], 'notes_en': notes['en']}
    emit(f'references/{obj["id"]}-{slug(r)}.yaml', obj, owner)

for owner, r in claims:
    statement = pair(r, 'statement')
    if not statement['zh']:
        statement = pair(r, 'proposition')
    subjects = r.get('subject_keys', r.get('subject_refs', [f'B015-{owner}-PARENT']))
    if owner == 'T1046':
        child = H[owner]['proposed_subtechniques'][0]
        if key(r) in child['evidence']['claim_keys']:
            subjects = list(dict.fromkeys(subjects + [key(child)]))
    mode = r.get('evidence_mode', 'strongly-inferred')
    if mode not in {'directly-observed', 'strongly-inferred', 'hypothesized'}:
        mode = 'directly-observed' if key(r) == 'B015-T1680-CLM-OBSERVED' else 'strongly-inferred'
    obj = {'schema_version': '1.0.0', 'type': 'claim', 'id': MAP[key(r)],
           'claim_type': r.get('claim_type', CLAIM_TYPES.get(key(r))),
           'statement_zh': statement['zh'], 'statement_en': statement['en'],
           'subject_refs': subjects, 'evidence_refs': r.get('evidence_keys', r.get('evidence_refs', [])),
           'evidence_mode': mode, 'confidence': r.get('confidence', 'medium'), 'status': 'draft'}
    assert obj['claim_type'] and statement['zh'] and statement['en'], key(r)
    emit(f'claims/{obj["id"]}-{slug(r)}.yaml', obj, owner)

for owner, r in cases:
    name = pair(r, 'name')
    description = pair(r, 'description')
    if not description['zh']:
        description = deepcopy(r['central_observed_facts'])
    if owner == 'T1680':
        description['zh'] += ' 报告未公开逐主机属性值、具体 API 选择或存储查询的检测对照。'
        description['en'] += ' The report does not publish per-host values, particular API choices, or a storage-query detection comparison.'
    actor = r.get('actor_or_campaign')
    if key(r) == 'B015-T1135-CASE-LUNAR-SHARED-RESOURCE-RECON':
        actor = 'LunarWeb'
    obj = {'schema_version': '1.0.0', 'type': 'case', 'id': MAP[key(r)],
           'name_zh': name['zh'], 'name_en': name['en'], 'actor_or_campaign': actor,
           'subject_refs': r.get('subject_keys', r.get('supports_keys', [f'B015-{owner}-PARENT'])),
           'description_zh': description['zh'], 'description_en': description['en'],
           'time_range': r.get('time_range', r.get('observed_date_range')),
           'target_sectors_zh': [], 'target_sectors_en': [],
           'evidence_refs': r.get('evidence_keys', []), 'confidence': r.get('confidence', 'high'), 'status': 'draft'}
    emit(f'cases/{obj["id"]}-{slug(r)}.yaml', obj, owner)


def analytic_primary_edits(r):
    if key(r) == 'B015-T1046-NJA-INTERNAL-PROBES':
        r['correlation']['window'] = {
            'zh': '采用十五分钟审阅窗口与二十四小时目标并集，并至少保留七天职责基线；这些时窗是待本地验证的部署初值。',
            'en': 'Use fifteen-minute review windows, twenty-four-hour target unions, and at least seven days of role baseline; these are deployment starting values requiring local validation.'}
        r['data_requirements'] += [
            {'source_type': 'optional-sysmon-process-origin', 'name': {'zh': '启用进程归属补充时的 Sysmon 创建事件', 'en': 'Sysmon creation events when process-origin enrichment is enabled'},
             'channel': 'Microsoft-Windows-Sysmon/Operational event 1 when configured',
             'required_fields': ['Computer', 'UtcTime', 'ProcessGuid', 'ProcessId', 'Image', 'CommandLine', 'ParentProcessGuid']},
            {'source_type': 'optional-sysmon-network-origin', 'name': {'zh': '启用进程归属补充时的 Sysmon 连接事件', 'en': 'Sysmon network events when process-origin enrichment is enabled'},
             'channel': 'Microsoft-Windows-Sysmon/Operational event 3 when configured',
             'required_fields': ['Computer', 'UtcTime', 'ProcessGuid', 'Protocol', 'SourceIp', 'SourcePort', 'DestinationIp', 'DestinationPort']}]
    if key(r) == 'B015-T1046-NJA-ADVERTISEMENT-QUERY':
        r['correlation']['window'] = {
            'zh': '查询与公告关联初始五分钟，可选后继访问十分钟，设备职责基线七天；按链路时延与缓存行为验证时窗。',
            'en': 'Start with five minutes for query-advertisement association, ten minutes for optional successor access, and seven days of device-role baseline; validate windows against link delay and caching.'}
        r['data_requirements'] += [
            {'source_type': 'optional-successor-connection', 'name': {'zh': '启用后继关联时的独立连接记录', 'en': 'Independent connections when successor correlation is enabled'},
             'channel': 'Zeek conn.log or equivalently validated connection telemetry',
             'required_fields': ['timestamp', 'connection_uid', 'source_ip', 'source_port', 'destination_ip', 'destination_port', 'connection_state', 'transport_history']},
            {'source_type': 'optional-client-browse-result', 'name': {'zh': '启用结果确认时的可信客户端输出', 'en': 'Trusted client output when result confirmation is enabled'},
             'channel': 'Separately deployed validated client-output or request-level collector',
             'required_fields': ['device_id', 'observed_time', 'request_context', 'service_type', 'browsing_domain', 'returned_instances', 'result_scope', 'collector_identity']}]
    return r


def normalized_field_name(name):
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()


for owner, r in analytics:
    r = analytic_primary_edits(r)
    for requirement in r['data_requirements']:
        requirement['source_type'] = requirement['source_type'].replace('_', '-').lower()
        requirement['required_fields'] = [normalized_field_name(v) for v in requirement['required_fields']]
    r['correlation']['dimensions'] = [normalized_field_name(v) for v in r['correlation']['dimensions']]
    evidence = list(dict.fromkeys(r.get('evidence_keys', []) + r.get('optional_enrichment_evidence_keys', [])))
    obj = {'schema_version': '2.0.0', 'type': 'detection-analytic', 'id': MAP[key(r)],
           'strategy_ref': r['strategy_key'], **{k: r[k] for k in ['name', 'summary', 'domains', 'platforms', 'logic', 'data_requirements', 'observables', 'correlation', 'false_positives', 'blind_spots', 'tuning_guidance']},
           'evidence_refs': evidence, 'lifecycle': lifecycle()}
    assert isinstance(obj['correlation']['window'], dict), key(r)
    emit(f'analytics/{obj["id"]}-{slug(r)}.yaml', obj, owner)

for owner, r in strategies:
    analytic_keys = r['analytic_keys']
    evidence = set(r.get('evidence_keys', []))
    for _, analytic in analytics:
        if key(analytic) in analytic_keys:
            evidence.update(analytic.get('evidence_keys', []))
            evidence.update(analytic.get('optional_enrichment_evidence_keys', []))
    obj = {'schema_version': '2.0.0', 'type': 'detection-strategy', 'id': MAP[key(r)],
           **{k: r[k] for k in ['name', 'summary', 'description']}, 'detects_refs': r['detects_keys'],
           'domains': r['domains'], 'analytic_refs': analytic_keys, 'evidence_refs': sorted(evidence), 'lifecycle': lifecycle()}
    emit(f'detections/{obj["id"]}-{slug(r)}.yaml', obj, owner)


def applications(items):
    values = deepcopy(items)
    for value in values:
        value['target_ref'] = value.pop('target_key')
    return values


for owner, r in mitigations:
    obj = {'schema_version': '2.0.0', 'type': 'mitigation', 'id': MAP[key(r)],
           **{k: r[k] for k in ['name', 'summary', 'description', 'domains', 'measures']},
           'applications': applications(r['applications']), 'evidence_refs': r['evidence_keys'], 'lifecycle': lifecycle()}
    emit(f'mitigations/{obj["id"]}-{slug(r)}.yaml', obj, owner)

# Existing source identity and case meaning remain unchanged; only exact locators
# and directly applicable subjects/applications are extended.
extensions = {
    'REF-000073': ('; Discovery: drive names, size, free space and filesystem types',
                  ' 同文档 Discovery 段直接记录主机存储属性发现，不证明独立匿迹子项或逐查询输出。',
                  ' The same publication directly reports host storage-attribute discovery in its Discovery section without establishing an independent stealth child or per-query output.'),
    'REF-001049': ('; security-related log exfiltration to assess sample detection, linked report printed page 9',
                  ' 安全日志反馈是与既有 Gmail 和组策略命令不同的观察；不证明每次读取后均有行动调整。',
                  ' Security-log feedback is distinct from the existing Gmail and Group Policy command observations and does not establish adaptation after every read.'),
    'REF-000639': ('; recovered LunarWeb shell-command package: reconnaissance includes shared resources',
                  ' 已恢复命令包中的共享资源侦察不证明逐服务器返回清单、有效访问或正文读取；Turla 归因仍为来源给出的中等置信度。',
                  ' Shared-resource reconnaissance in a recovered command package does not establish per-server inventories, effective access, or content reads; Turla attribution remains the source\'s medium-confidence assessment.'),
    'REF-000625': ('; fixed Enterprise 19.1 T1680/T1654/T1046/T1135/T1040 parent inventory checked against the versioned workbook', '', ''),
}
for ident, (locator, zh, en) in extensions.items():
    path = next((ROOT / 'references').glob(ident + '-*.yaml'))
    obj = yaml.safe_load(path.read_text())
    if locator not in (obj.get('locator') or ''):
        obj['locator'] = (obj.get('locator') or '') + locator
    if zh and zh not in (obj.get('notes_zh') or ''):
        obj['notes_zh'] = (obj.get('notes_zh') or '') + zh
    if en and en not in (obj.get('notes_en') or ''):
        obj['notes_en'] = (obj.get('notes_en') or '') + en
    obj['accessed'] = TODAY
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))

path = next((ROOT / 'cases').glob('CASE-000259-*.yaml'))
obj = yaml.safe_load(path.read_text())
if IDS['parents']['T1046'] not in obj['subject_refs']:
    obj['subject_refs'].append(IDS['parents']['T1046'])
path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))

path = next((ROOT / 'mitigations').glob('MIT-000186-*.yaml'))
obj = yaml.safe_load(path.read_text())
proposal = H['T1040']['defense_candidates']['mitigations'][0]
new_applications = applications(proposal['applications']) + applications([EXTRA['mitigation_application']])
old_targets = {a['target_ref'] for a in obj['applications']}
obj['applications'] += [a for a in mapped(new_applications) if a['target_ref'] not in old_targets]
obj['evidence_refs'] = sorted(set(obj['evidence_refs'] + mapped(proposal['evidence_keys']) + [MAP['B015-T1040-REF-TCPDUMP4995']]))
obj['lifecycle'].update(version='0.2.0', modified=TODAY)
path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))


def paragraph(zh, en):
    return {'zh': zh, 'en': en}


def parent_primary_edits(attack, p):
    if attack == 'T1680':
        p['summary'] = paragraph('取得目标主机可见的驱动器、磁盘和卷及其存储属性，读取请求可呈现为正常存储盘点与容量维护。',
                                 'Acquire drives, disks, volumes, and storage attributes visible to a target host through requests that can resemble ordinary inventory and capacity maintenance.')
        p['scope_boundary_definition']['paragraphs'][1] = paragraph(
            '取得文件和目录名称或 .vmdk 路径归 NJT-0182，枚举远端可用共享归网络共享发现；只看到一个已映射盘符不满足后者。AWS、GCP 和 Azure 提供方的卷资源清单由 NJT-0139 处理，取得或复制存储正文属于后继收集，绕过文件视图的原始内容读取需满足 NJT-0108。打开句柄本身不证明取得正文；格式化、加密和关键扇区写入另行判断影响结果。容量监控、安装检查、备份、磁盘修复和事件响应都是正常反例，不能只凭工具或字段判断恶意。',
            'File and directory names or .vmdk paths belong to NJT-0182, and enumeration of remotely available shares belongs to Network Share Discovery; an existing mapped drive alone does not establish the latter. Provider-side AWS, GCP, and Azure volume inventories are handled by NJT-0139. Acquiring or copying storage content is later collection, while raw-content reads bypassing the file view must meet NJT-0108. A handle alone does not establish acquired content; formatting, encryption, and critical-sector writes need separate impact assessment. Capacity monitoring, installation checks, backup, repair, and incident response remain counterexamples, so tools or fields alone do not establish malice.')
    if attack == 'T1654':
        p['subtechnique_taxonomy']['narrative']['paragraphs'][1] = paragraph(
            '日志反馈的恶意用途已有记录，仍不能仅以用途命名子技术。需要把读取内容、反馈时点、下一步行为与防守观察对照连接，区分资料原有的不可见性和攻击者主动造成的变化。现有证据尚不足以完成这种独立划分，因此分类暂缓；后续结果级资料可以重新开启候选轴。',
            'Adversarial log feedback is documented, but purpose alone does not define a child. Acquired contents, feedback timing, subsequent behavior, and comparative defender observations must be connected to distinguish preexisting visibility limits from adversary-induced changes. Current evidence does not complete that independent partition, so taxonomy remains deferred and further result-level evidence can reopen candidate axes.')
    if attack == 'T1046':
        p['stealth_mechanisms'][1]['summary']['en'] = 'Move initial service surveying from listener probes to advertisement queries outside connection-only scan rules'
    if attack == 'T1135':
        p['application_scenarios_and_threat_model']['threat_model']['attacker_model']['paragraphs'][1]['zh'] = '攻击者可选择要查询的服务器、信息级别和查询方式，并在实现支持时续取结果页。操作受网络分段、服务可用性、当前身份、返回长度和动态共享状态限制；分页与重试首先是正常完整性处理，只有额外证据证明其用于改变防守关联时才可讨论匿迹变量。已有映射仅提供特定共享关系，不赋予查询整台服务器共享清单的额外权限。'
    if attack == 'T1040':
        p['subtechnique_taxonomy'] = {
            'narrative': {'paragraphs': [paragraph(
                '当前建立主动名称补全抑制子项，变量是解释所见报文时是否关闭本可发起的外部名称补全。NIST 的明确匿迹说明与固定 tcpdump 版本规范提供能力层级的因果支持；它不同于父级捕获位置与权限，要求额外保留有效解释设置、输入输出模式和捕获关联事实。该子项保持中等置信度，没有被改写成恶意现场采用案例。',
                'The current child is Active Name-Enrichment Suppression, whose variable is disabling external name enrichment that could otherwise occur while interpreting observed packets. NIST\'s explicit stealth rationale and a pinned tcpdump specification provide capability-level causal support. This differs from parent capture position and authority and adds effective interpretation settings, input/output mode, and capture-linked fact requirements. Confidence remains medium without rewriting capability evidence as malicious field adoption.'), paragraph(
                '观察位置与复制拓扑、过滤与截短、短时或环形缓冲以及实时解析等其他轴保留待研究，不能改名复制 NJT-0176 的凭据结果子项。被动观察属于父级核心，主动路径介入和新诱发认证归相邻对象。数值显示、DNS 缺席、-N 或纯写包不单独成立新子项；未来需要按具体采集器和结果验证补全抑制的实际效果。',
                'Other axes, including observation position and replication, filtering and truncation, short or ring buffers, and real-time parsing, remain research candidates rather than renamed NJT-0176 credential-result children. Passive observation defines the parent behavior; active path intervention and induced authentication belong to neighbors. Numeric display, absent DNS, -N, and raw-save-only mode do not individually establish the new child. Actual suppression effects require collector- and result-specific validation.')]},
            'coverage': 'established', 'subtechnique_keys': [key(EXTRA['child'])]}
        p['research']['limitations']['paragraphs'][1] = paragraph(
            '尚未开展真实主机、网络设备或云环境实验。检测窗口、审批模型、结果溯源字段和调优是实施设计，需验证部署版本和保留能力；镜像资源、计数增长或 PCAP 存在均不证明攻击者已解释内容。被动知识有时间和位置偏差，加密也不能保证隐藏全部网络事实。名称补全子项有明确能力和匿迹用途证据，仍缺实际恶意采用、相对事务数量和结果返回测量。',
            'No live host, network-device, or cloud experiment was conducted. Windows, approval models, result-provenance fields, and tuning are implementation designs requiring deployed-version and retention validation; mirror resources, increasing counters, or PCAP existence do not establish adversary interpretation. Passive knowledge is time- and location-biased, and encryption does not hide every network fact. The name-enrichment child has explicit capability and stealth-purpose support but lacks malicious field adoption, relative transaction counts, and fact-return measurements.')
    return p


def mechanisms(values):
    result = deepcopy(values)
    for m in result:
        m['evidence_refs'] = m.pop('evidence_keys', m.get('evidence_refs', []))
    return result


def defense_for(owner):
    strategy_refs = [MAP[key(r)] for a, r in strategies if a == owner]
    mitigation_refs = [MAP[key(r)] for a, r in mitigations if a == owner]
    if owner == 'T1040':
        mitigation_refs = ['MIT-000186']
    return {'detections': {'coverage': 'available', 'strategy_refs': strategy_refs},
            'mitigations': {'coverage': 'available', 'mitigation_refs': mitigation_refs}}


parent_paths = {}
for attack in SCOPE:
    p = parent_primary_edits(attack, deepcopy(H[attack]['proposed_content']))
    decision_kind = H[attack]['recommendation']['decision']
    recommendation = H[attack]['recommendation']
    rationale = recommendation['rationale']['paragraphs']
    scope_note = recommendation.get('scope_notes', recommendation.get('proposed_scope_notes'))
    scope_zh = scope_note['paragraphs'][0]['zh'] if scope_note else p['scope_boundary_definition']['paragraphs'][1]['zh']
    scope_en = scope_note['paragraphs'][0]['en'] if scope_note else p['scope_boundary_definition']['paragraphs'][1]['en']
    refs = {'REF-000625'} | reference_ids(mapped(p))
    refs |= {MAP[key(r)] for a, r in references if a == attack}
    for owner, obj in OBJECTS:
        if owner == attack:
            refs |= reference_ids(obj)
    decision = {'schema_version': '1.1.0', 'type': 'technique-decision',
                'id': f'DEC-TA0007-{attack}', 'tactic_ref': 'TA0007',
                'candidate': {'source_type': 'attack', 'source_attack_id': attack, 'source_attack_version': '19.1',
                              'name_en': H[attack]['candidate']['name']['en'], 'name_zh': H[attack]['candidate']['name']['zh']},
                'decision': decision_kind,
                'rationale_zh': ' '.join(q['zh'] for q in rationale),
                'rationale_en': ' '.join(q['en'] for q in rationale),
                'scope_notes_zh': scope_zh, 'scope_notes_en': scope_en,
                'gap_statement_zh': None, 'gap_statement_en': None,
                'original_attack_subtechniques_imported': False, 'resulting_technique_ref': IDS['parents'][attack],
                'evidence_refs': sorted(refs), 'confidence': recommendation.get('confidence', 'medium'),
                'review': {'status': 'draft', 'authors': ['Niji Matrix Research'], 'reviewers': [],
                           'review_notes_zh': '完整研究、跨候选边界、共享库身份、原生分类与主审字段深度检查已完成，待机器、Bundle 和双语 Web 验收。',
                           'review_notes_en': 'Complete research, cross-candidate boundaries, library identity, native taxonomy, and primary field-depth review are complete; machine, bundle, and bilingual Web acceptance remain.'}}
    emit(f'matrix/tactics/TA0007-discovery/decisions/{decision["id"]}.yaml', decision, attack)
    taxonomy = deepcopy(p['subtechnique_taxonomy'])
    taxonomy['subtechnique_refs'] = taxonomy.pop('subtechnique_keys', taxonomy.get('subtechnique_refs', []))
    claim_refs = [MAP[key(r)] for a, r in claims if a == attack]
    case_refs = [MAP[key(r)] for a, r in cases if a == attack]
    if attack == 'T1046':
        case_refs.append('CASE-000259')
    limitations = p.get('research', {}).get('limitations', H[attack]['research'].get('limitations'))
    parent = {'schema_version': '2.0.0', 'type': 'technique', 'id': IDS['parents'][attack],
              'name': p['name'], 'summary': p['summary'], 'aliases': p.get('aliases', []),
              'classification': {'tactic_refs': ['TA0007'], 'origin': {'kind': 'attack-retained' if decision_kind == 'retain' else 'attack-adapted',
                                                                   'source_attack_id': attack, 'source_attack_version': '19.1'},
                                 'decision_ref': decision['id']},
              **{k: p[k] for k in ['definition_and_concept', 'stealth_characteristics', 'scope_boundary_definition', 'application_scenarios_and_threat_model']},
              'stealth_mechanisms': mechanisms(p['stealth_mechanisms']), 'subtechnique_taxonomy': taxonomy,
              'defense': defense_for(attack), 'evidence': {'claim_refs': claim_refs, 'case_refs': case_refs, 'reference_refs': sorted(refs)},
              'research': {'limitations': limitations}, 'lifecycle': lifecycle()}
    parent_path = f'matrix/tactics/TA0007-discovery/techniques/{parent["id"]}-{attack.lower()}-discovery/technique.yaml'
    emit(parent_path, parent, attack)
    parent_paths[attack] = parent_path

for owner, p in [('T1046', H['T1046']['proposed_subtechniques'][0]), ('T1040', EXTRA['child'])]:
    parent_ref = IDS['parents'][owner]
    defense = p['defense']
    strategy_refs = defense.get('strategy_keys', defense.get('detection_strategy_keys'))
    child_refs = set(mapped(p['evidence']['reference_keys']))
    for m in mapped(mechanisms(p['stealth_mechanisms'])):
        child_refs.update(m['evidence_refs'])
    child = {'schema_version': '2.0.0', 'type': 'evasion-subtechnique', 'id': MAP[key(p)],
             'name': p['name'], 'summary': p['summary'], 'aliases': p.get('aliases', []),
             'parent_ref': parent_ref, 'lineage': {'attck_subtechnique_inherited': False},
             **{k: p[k] for k in ['definition_and_concept', 'stealth_characteristics', 'scope_boundary_definition', 'application_scenarios_and_threat_model']},
             'stealth_mechanisms': mechanisms(p['stealth_mechanisms']),
             'defense': {'detections': {'coverage': 'available', 'strategy_refs': strategy_refs},
                         'mitigations': {'coverage': 'available', 'mitigation_refs': defense['mitigation_keys']}},
             'evidence': {'claim_refs': p['evidence']['claim_keys'], 'case_refs': p['evidence']['case_keys'], 'reference_refs': sorted(child_refs)},
             'research': {'limitations': p['research']['limitations']}, 'lifecycle': lifecycle()}
    directory = str(Path(parent_paths[owner]).parent)
    emit(f'{directory}/subtechniques/{child["id"]}-{owner.lower()}-native/subtechnique.yaml', child, owner)

path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(path.read_text())
for work in plan['work_items']:
    attack = work['source_attack_id']
    if attack in SCOPE:
        work.update(decision_ref=f'DEC-TA0007-{attack}', resulting_technique_ref=IDS['parents'][attack], stage='authoring')
path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))

taxonomy_review = {'batch_ref': 'BATCH-TA0007-015', 'baseline': 'Enterprise 19.1', 'candidates': []}
for attack in SCOPE:
    original = H[attack]['research'].get('taxonomy_breadth_review', {})
    taxonomy_review['candidates'].append({'source_attack_id': attack, 'original_research': original,
                                        'primary_review': {'status': 'passed', 'formal_njs_count': int(attack in ['T1046', 'T1040']),
                                                           'supplement_ref': 'T1040-taxonomy-supplement.yaml' if attack == 'T1040' else None,
                                                           'original_attack_subtechniques_imported': False}})
(RUN / 'taxonomy-breadth-review.yaml').write_text(yaml.safe_dump(taxonomy_review, allow_unicode=True, sort_keys=False, width=120))
(RUN / 'canonical-id-map.json').write_text(json.dumps(MAP, ensure_ascii=False, indent=2) + '\n')
(RUN / 'written-object-paths.json').write_text(json.dumps(WRITTEN, indent=2) + '\n')
(RUN / 'canonical-parent-paths.json').write_text(json.dumps(parent_paths, indent=2) + '\n')
print(json.dumps({'new_canonical_objects': len(WRITTEN), 'parents': IDS['parents'], 'children': IDS['NJS'],
                  'new_sources': len(references), 'new_claims': len(claims), 'new_cases': len(cases),
                  'new_strategies': len(strategies), 'new_analytics': len(analytics), 'new_mitigations': len(mitigations),
                  'extended': ['REF-000073', 'REF-001049', 'REF-000639', 'REF-000625', 'CASE-000259', 'MIT-000186']}, ensure_ascii=False, indent=2))
