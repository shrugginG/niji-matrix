"""Project individually reviewed research into canonical schemas.

All semantic text comes from reviewed-handoffs and literal primary edits, never
from expansion of a common paragraph by candidate-name substitution.
"""
from copy import deepcopy
from pathlib import Path
import json
import re
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
TODAY = '2026-11-06'
SCOPE = ['T1201', 'T1120', 'T1069', 'T1057', 'T1012']
assert json.loads((RUN / 'research-input-manifest.json').read_text())['all_five_handoffs_complete']
IDS = json.loads((RUN / 'allocated-ids.json').read_text())
assert sum(len(v) for v in IDS['children'].values()) == 4
H = {a: yaml.safe_load((RUN / 'reviewed-handoffs' / f'{a}.yaml').read_text()) for a in SCOPE}


def key(o):
    return o.get('key', o.get('temporary_key'))


def pair(o, field):
    return deepcopy(o[field]) if isinstance(o.get(field), dict) else {'zh': o.get(field + '_zh', ''), 'en': o.get(field + '_en', '')}


def lifecycle():
    return {'status': 'draft', 'version': '0.1.0', 'created': TODAY, 'modified': TODAY,
            'contributors': ['Niji Matrix Research'], 'reviewers': []}


MAP = {f'B016-{a}-PARENT': IDS['parents'][a] for a in SCOPE}
for attack in SCOPE:
    for child, ident in zip(H[attack]['proposed_subtechniques'], IDS['children'][attack], strict=True):
        MAP[key(child)] = ident
references = yaml.safe_load((RUN / 'reference-projection.yaml').read_text())
for r, ident in zip(references, IDS['REF'], strict=True):
    MAP[key(r)] = ident
for alias, target in json.loads((RUN / 'library-aliases.json').read_text()).items():
    MAP[alias] = MAP.get(target, target)
groups = {}
for kind, section, field in [('CLM', 'library_candidates', 'claims'), ('CASE', 'library_candidates', 'cases'),
                            ('DET', 'defense_candidates', 'detection_strategies'), ('NJA', 'defense_candidates', 'detection_analytics'),
                            ('MIT', 'defense_candidates', 'mitigations')]:
    groups[kind] = [(a, deepcopy(o)) for a in SCOPE for o in H[a][section][field] if not o.get('existing_ref')]
    for (_, o), ident in zip(groups[kind], IDS[kind], strict=True):
        MAP[key(o)] = ident


def mapped(value):
    if isinstance(value, str):
        return MAP.get(value, value)
    if isinstance(value, list):
        return [mapped(x) for x in value]
    if isinstance(value, dict):
        result = {k: mapped(v) for k, v in value.items()}
        for k, v in result.items():
            if k.endswith('_refs') and isinstance(v, list) and all(isinstance(x, str) for x in v):
                result[k] = list(dict.fromkeys(v))
        return result
    return value


def evidence(o):
    return o.get('evidence_keys', o.get('evidence_refs', []))


def slug(o):
    return key(o).removeprefix('B016-').lower()


WRITTEN = []


def emit(relative, obj):
    obj = mapped(obj)
    text = yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120)
    assert 'B016-' not in text, relative
    assert 'planning/' not in text and '__REQUIRED' not in text, relative
    path = ROOT / relative
    if path.exists():
        assert yaml.safe_load(path.read_text()) == obj, f'Refusing different overwrite: {path}'
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    WRITTEN.append(relative)


allowed_types = set(json.loads((ROOT / 'schemas/reference.schema.json').read_text())['properties']['source_type']['enum'])
for r in references:
    title, notes = pair(r, 'title'), pair(r, 'notes')
    assert title['zh'] and title['en'] and notes['zh'] and notes['en'], key(r)
    assert r['source_type'] in allowed_types, (key(r), r['source_type'])
    ident = {'doi': None, 'rfc': None, 'arxiv': None, 'attack_id': None, 'other': []}
    ident.update(r.get('identifiers', {}))
    published = str(r['published']) if r.get('published') is not None else None
    obj = {'schema_version': '1.0.0', 'type': 'reference', 'id': MAP[key(r)],
           'title_zh': title['zh'], 'title_en': title['en'], 'source_type': r['source_type'], 'identifiers': ident,
           'authors': r.get('authors', []), 'publisher': r.get('publisher'), 'published': published,
           'url': r['url'], 'accessed': TODAY, 'locator': r.get('locator'), 'archive_url': r.get('archive_url'),
           'credibility': r.get('credibility', 'high'), 'notes_zh': notes['zh'], 'notes_en': notes['en']}
    emit(f'references/{obj["id"]}-{slug(r)}.yaml', obj)
for owner, r in groups['CLM']:
    statement = pair(r, 'statement')
    subjects = r.get('subject_keys', r.get('subject_refs', [f'B016-{owner}-PARENT']))
    if key(r) in H[owner]['proposed_content']['evidence']['claim_keys'] and f'B016-{owner}-PARENT' not in subjects:
        subjects = [f'B016-{owner}-PARENT', *subjects]
    obj = {'schema_version': '1.0.0', 'type': 'claim', 'id': MAP[key(r)], 'claim_type': r['claim_type'],
           'statement_zh': statement['zh'], 'statement_en': statement['en'], 'subject_refs': subjects,
           'evidence_refs': evidence(r), 'evidence_mode': r['evidence_mode'], 'confidence': r['confidence'], 'status': 'draft'}
    emit(f'claims/{obj["id"]}-{slug(r)}.yaml', obj)
for owner, r in groups['CASE']:
    name, description = pair(r, 'name'), pair(r, 'description')
    obj = {'schema_version': '1.0.0', 'type': 'case', 'id': MAP[key(r)],
           'name_zh': name['zh'], 'name_en': name['en'], 'actor_or_campaign': r.get('actor_or_campaign'),
           'subject_refs': r.get('subject_keys', r.get('subject_refs', [f'B016-{owner}-PARENT'])),
           'description_zh': description['zh'], 'description_en': description['en'],
           'time_range': r.get('time_range'), 'target_sectors_zh': r.get('target_sectors_zh', []),
           'target_sectors_en': r.get('target_sectors_en', []), 'evidence_refs': evidence(r),
           'confidence': r['confidence'], 'status': 'draft'}
    emit(f'cases/{obj["id"]}-{slug(r)}.yaml', obj)
for owner, r in groups['NJA']:
    obj = {'schema_version': '2.0.0', 'type': 'detection-analytic', 'id': MAP[key(r)], 'strategy_ref': r['strategy_key'],
           **{k: r[k] for k in ['name', 'summary', 'domains', 'platforms', 'logic', 'data_requirements', 'observables',
                               'correlation', 'false_positives', 'blind_spots', 'tuning_guidance']},
           'evidence_refs': evidence(r), 'lifecycle': lifecycle()}
    emit(f'analytics/{obj["id"]}-{slug(r)}.yaml', obj)
for owner, r in groups['DET']:
    analytic_keys = r['analytic_keys']
    refs = set(evidence(r))
    for _, a in groups['NJA']:
        if key(a) in analytic_keys:
            refs.update(evidence(a))
    obj = {'schema_version': '2.0.0', 'type': 'detection-strategy', 'id': MAP[key(r)],
           **{k: r[k] for k in ['name', 'summary', 'description']}, 'detects_refs': r['detects_keys'],
           'domains': r['domains'], 'analytic_refs': analytic_keys, 'evidence_refs': sorted(refs), 'lifecycle': lifecycle()}
    emit(f'detections/{obj["id"]}-{slug(r)}.yaml', obj)


def applications(values):
    return [{'target_ref': a.get('target_key', a.get('target_ref')), **{k: deepcopy(a[k]) for k in ['use', 'expected_effect', 'limitations']}} for a in values]


for owner, r in groups['MIT']:
    obj = {'schema_version': '2.0.0', 'type': 'mitigation', 'id': MAP[key(r)],
           **{k: r[k] for k in ['name', 'summary', 'description', 'domains']},
           'measures': [{k: x[k] for k in ['key', 'name', 'description', 'control_type']} for x in r['measures']],
           'applications': applications(r['applications']), 'evidence_refs': evidence(r), 'lifecycle': lifecycle()}
    emit(f'mitigations/{obj["id"]}-{slug(r)}.yaml', obj)


def mechanisms(values):
    return [{k: deepcopy(m[k]) for k in ['mechanism_ref', 'role', 'summary', 'analysis']} |
            {'evidence_refs': evidence(m), 'confidence': m['confidence']} for m in values]


def subject_defense(value):
    d, m = value['detections'], value['mitigations']
    return {'detections': {'coverage': d['coverage'], 'strategy_refs': d.get('strategy_keys', d.get('strategy_refs', []))},
            'mitigations': {'coverage': m['coverage'], 'mitigation_refs': m.get('mitigation_keys', m.get('mitigation_refs', []))}}


def subject_evidence(value):
    return {'claim_refs': value.get('claim_keys', value.get('claim_refs', [])),
            'case_refs': value.get('case_keys', value.get('case_refs', [])),
            'reference_refs': value.get('reference_keys', value.get('reference_refs', []))}


extensions = {
    'REF-000625': ('Enterprise 19.1 T1201, T1120, T1069, T1057 and T1012 parent records',
                   '本次固定版本对照支持父行为范围，不作为原生匿迹子项或检测字段的自动证据。',
                   'The pinned parent records anchor behavior scope rather than automatically proving native children or analytic fields.'),
    'REF-001049': ('Insight into attacker activity, article Figure 3 net accounts and local/domain group commands; linked report section 3.4 printed page 8 Figure 6',
                   '密码策略与组关系命令分别支持限定的查询活动观察，未公开逐查询结果；不证明匿名、无句柄、策略推导或驻留内联子项。',
                   'Password-policy and group commands support separate bounded query observations without per-query results; they do not establish anonymity, handle elision, policy inference, or resident inline children.'),
    'REF-000484': ('Device monitor and GSM fingerprinting paragraphs; linked Attor report section 4.3.1',
                   '设备身份和反馈后的指纹查询与既有截图、音频及上传架构观察分别判断，不证明每台主机的成功取数或检测变化。',
                   'Device identity and feedback-driven fingerprinting are separate from screenshot, audio, and upload-architecture observations and do not establish per-host acquisition or detection changes.'),
    'REF-000583': ('Section 4.3.1 Device monitor, printed page 16 onward; window and Shell/device-change reception followed by peripheral identification',
                   '设备通知、属性取得、存储属性、文件内容和驱动探测是不同事实；监听后的主动查询不能称为全程被动。',
                   'Device notifications, acquired properties, storage attributes, file content, and driver probing are distinct facts; active follow-up queries do not make the entire path passive.'),
    'REF-001041': ('Suricata 8.0.2 https://docs.suricata.io/en/suricata-8.0.2/output/eve/eve-json-format.html SMB and DCERPC fields, REQUEST/RESPONSE and BIND/BINDACK examples',
                   '此字段对照固定核查 8.0.2：接口列表主要位于绑定记录，SMB 或 RPC 层状态不等于 SAMR 应用返回；其他版本须另验。',
                   'The field check pins 8.0.2: interface lists mainly occur in bind records, and SMB or RPC status is not a SAMR application result. Other versions need separate validation.'),
    'REF-000073': ('Discovery running-process information; introductory living-off-the-land intent',
                   '运行进程发现是独立的观察；一般就地取材意图不证明每次注册表查询的目的、输出或匿迹结果。',
                   'Running-process discovery is a separate observation; general living-off-the-land intent does not establish the purpose, output, or stealth outcome of each Registry query.'),
    'REF-001230': ('Printed page 10 Table 5 Get-Process Lsass and tasklist; printed page 20 T1057 summary',
                   '进程定位与清单命令不等同后续凭据转储，输出重定向也不证明文件内的具体进程行或驻留内联执行。',
                   'Process-location and inventory commands differ from later credential dumping, and redirection establishes neither specific output rows nor resident inline execution.'),
    'REF-000025': ('Discovery, printed page 12 tool list reg query/reg save; official PDF also distributed at https://www.fbi.gov/file-repository/cyber-alerts/prc-state-sponsored-actors-compromise-and-maintain-persistent-access-to-u-s-critical-infrastructure.pdf',
                   'reg query 的工具使用与 reg save 或凭据副本是不同观察；汇总列表不公开每次查询路径、具体信息目的、返回值或进程内执行方式。',
                   'reg query use is distinct from reg save or credential copies; the aggregate list does not publish each query path, immediate information purpose, returned values, or in-process execution.'),
    'REF-000506': ('RC2CL Backdoor commands, command 155 enumeration of Registry values/keys/data; distinguish its mutation branches',
                   '该条支持逆向确认的一般注册表枚举能力，不能把同一命令中的创建、删除和设值当成读取，也不证明具体现场采用。',
                   'The entry supports reverse-engineered general Registry enumeration; create, delete, and set branches are not reads and do not establish specific field adoption.'),
}
titles = {
    'REF-000484': ('ESET 发现具有 GSM 指纹功能的 Attor 间谍平台', 'ESET Discovers Attor, a Spy Platform with Curious GSM Fingerprinting'),
    'REF-000583': ('AT 命令与 Tor 通信：Attor 间谍平台研究白皮书', 'AT Commands, Tor-Based Communications: Meet Attor, a Fantasy Creature and Also a Spy Platform'),
    'REF-000506': ('InvisiMole：自 2013 年隐蔽活动的多功能间谍软件', 'InvisiMole: Surprisingly Equipped Spyware, Undercover Since 2013'),
}
before_path = RUN / 'existing-objects-before.json'
before = json.loads(before_path.read_text()) if before_path.exists() else {}
extended_paths = []
for ident, (locator, zh, en) in extensions.items():
    path = next((ROOT / 'references').glob(ident + '-*.yaml'))
    obj = yaml.safe_load(path.read_text())
    before.setdefault(str(path.relative_to(ROOT)), deepcopy(obj))
    if locator not in (obj.get('locator') or ''):
        obj['locator'] = (obj.get('locator') or '') + '; ' + locator
    for lang, note in [('zh', zh), ('en', en)]:
        field = 'notes_' + lang
        if note not in (obj.get(field) or ''):
            obj[field] = (obj.get(field) or '') + ' ' + note
    if ident in titles:
        obj['title_zh'], obj['title_en'] = titles[ident]
    obj['accessed'] = TODAY
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))
    extended_paths.append(str(path.relative_to(ROOT)))
path = next((ROOT / 'mitigations').glob('MIT-000240-*.yaml'))
obj = yaml.safe_load(path.read_text())
before.setdefault(str(path.relative_to(ROOT)), deepcopy(obj))
proposal = next(x for x in H['T1069']['defense_candidates']['mitigations'] if x.get('existing_ref') == 'MIT-000240')
assert proposal['measures_unchanged']
addition = mapped(applications(proposal['application_additions'])[0])
old = next((a for a in obj['applications'] if a['target_ref'] == addition['target_ref']), None)
if old is None:
    obj['applications'].append(addition)
else:
    assert old == addition
obj['evidence_refs'] = sorted(set(obj['evidence_refs'] + mapped(evidence(proposal))))
obj['lifecycle'].update(status='draft', version='0.2.0', modified=TODAY)
assert obj['measures'] == before[str(path.relative_to(ROOT))]['measures']
for old_app in before[str(path.relative_to(ROOT))]['applications']:
    assert old_app in obj['applications']
path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))
extended_paths.append(str(path.relative_to(ROOT)))
before_path.write_text(json.dumps(before, ensure_ascii=False, indent=2, default=str) + '\n')
(RUN / 'extended-object-paths.json').write_text(json.dumps(extended_paths, indent=2) + '\n')


plan_path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(plan_path.read_text())
CORE = ['definition_and_concept', 'stealth_characteristics', 'scope_boundary_definition', 'application_scenarios_and_threat_model']
parent_slugs = ['password-policy-discovery', 'peripheral-device-discovery', 'permission-groups-discovery', 'process-discovery', 'registry-query']
child_slugs = {'T1120': 'notification-driven-peripheral-discovery', 'T1069': 'policy-relationship-inference-substitution',
               'T1057': 'resident-context-inline-process-survey', 'T1012': 'in-process-registry-query'}
parent_paths = {}
for attack, parent_slug in zip(SCOPE, parent_slugs, strict=True):
    p, recommendation = H[attack]['proposed_content'], H[attack]['recommendation']
    work = next(w for w in plan['work_items'] if w['source_attack_id'] == attack)
    rationale = recommendation['rationale']['paragraphs']
    scope = recommendation.get('scope_notes', p['scope_boundary_definition'])['paragraphs']
    refs = sorted(set(p['evidence']['reference_keys'] + ['REF-000625']))
    decision = {'schema_version': '1.1.0', 'type': 'technique-decision', 'id': f'DEC-TA0007-{attack}', 'tactic_ref': 'TA0007',
                'candidate': {'source_type': 'attack', 'source_attack_id': attack, 'source_attack_version': '19.1',
                              'name_en': work['name_en'], 'name_zh': work['name_zh']},
                'decision': recommendation['decision'], 'rationale_zh': ' '.join(x['zh'] for x in rationale),
                'rationale_en': ' '.join(x['en'] for x in rationale), 'scope_notes_zh': ' '.join(x['zh'] for x in scope),
                'scope_notes_en': ' '.join(x['en'] for x in scope), 'gap_statement_zh': None, 'gap_statement_en': None,
                'original_attack_subtechniques_imported': False, 'resulting_technique_ref': IDS['parents'][attack],
                'evidence_refs': refs, 'confidence': recommendation['confidence'],
                'review': {'status': 'draft', 'authors': ['Niji Matrix Research'], 'reviewers': [],
                           'review_notes_zh': '独立研究和主审准入、分类、字段深度与共享库身份审查完成，等待机器、Bundle 和双语 Web 验收。',
                           'review_notes_en': 'Independent research and primary admission, taxonomy, field-depth, and library-identity review are complete; machine, bundle, and bilingual Web acceptance remain.'}}
    emit(f'matrix/tactics/TA0007-discovery/decisions/{decision["id"]}.yaml', decision)
    taxonomy = deepcopy(p['subtechnique_taxonomy'])
    taxonomy['subtechnique_refs'] = taxonomy.pop('subtechnique_keys', [])
    parent = {'schema_version': '2.0.0', 'type': 'technique', 'id': IDS['parents'][attack],
              'name': p['name'], 'summary': p['summary'], 'aliases': p.get('aliases', []),
              'classification': {'tactic_refs': ['TA0007'], 'origin': {'kind': 'attack-retained' if recommendation['decision'] == 'retain' else 'attack-adapted',
                                                                   'source_attack_id': attack, 'source_attack_version': '19.1'}, 'decision_ref': decision['id']},
              **{k: p[k] for k in CORE}, 'stealth_mechanisms': mechanisms(p['stealth_mechanisms']),
              'subtechnique_taxonomy': taxonomy, 'defense': subject_defense(p['defense']), 'evidence': subject_evidence(p['evidence']),
              'research': {'limitations': p['research']['limitations']}, 'lifecycle': lifecycle()}
    directory = f'matrix/tactics/TA0007-discovery/techniques/{parent["id"]}-{parent_slug}'
    parent_paths[attack] = directory + '/technique.yaml'
    emit(parent_paths[attack], parent)
    for p in H[attack]['proposed_subtechniques']:
        child = {'schema_version': '2.0.0', 'type': 'evasion-subtechnique', 'id': MAP[key(p)],
                 'name': p['name'], 'summary': p['summary'], 'aliases': p.get('aliases', []),
                 'parent_ref': parent['id'], 'lineage': {'attck_subtechnique_inherited': False},
                 **{k: p[k] for k in CORE}, 'stealth_mechanisms': mechanisms(p['stealth_mechanisms']),
                 'defense': subject_defense(p['defense']), 'evidence': subject_evidence(p['evidence']),
                 'research': {'limitations': p['research']['limitations']}, 'lifecycle': lifecycle()}
        emit(f'{directory}/subtechniques/{child["id"]}-{child_slugs[attack]}/subtechnique.yaml', child)
    work.update(decision_ref=decision['id'], resulting_technique_ref=parent['id'], stage='authoring')
plan_path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))
(RUN / 'canonical-id-map.json').write_text(json.dumps(MAP, ensure_ascii=False, indent=2) + '\n')
(RUN / 'written-object-paths.json').write_text(json.dumps(WRITTEN, indent=2) + '\n')
(RUN / 'canonical-parent-paths.json').write_text(json.dumps(parent_paths, indent=2) + '\n')
assert len(WRITTEN) == 153, len(WRITTEN)
print(json.dumps({'new_objects': len(WRITTEN), 'parents': IDS['parents'], 'children': IDS['children']}, ensure_ascii=False))
