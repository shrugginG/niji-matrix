"""Serialize the completed, individually reviewed T1018 content and resolved identities.

Semantic text is authored in the handoff, primary overrides and admission record.
This script maps fields and IDs, preserves existing shared-source applicability,
and writes the reviewed package as draft while acceptance runs.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
TODAY = '2026-11-07'
data = yaml.safe_load((RUN / 'T1018-reviewed-handoff.yaml').read_text())
ids = json.loads((RUN / 'allocated-ids.json').read_text())
assert set(ids) == {'NJT', 'NJS', 'REF', 'CLM', 'CASE', 'DET', 'NJA', 'MIT'}
manifest = json.loads((RUN / 'review-input-manifest.json').read_text())
assert hashlib.sha256((RUN / 'T1018-reviewed-handoff.yaml').read_bytes()).hexdigest() == manifest['reviewed_handoff_sha256']
parent, child = ids['NJT'][0], ids['NJS'][0]
mapping = {'B010-T1018-PARENT': parent, data['proposed_subtechniques'][0]['temporary_key']: child}
groups = {'REF': data['library_candidates']['references'], 'CLM': data['library_candidates']['claims'],
          'CASE': data['library_candidates']['cases'], 'DET': data['defense_candidates']['detection_strategies'],
          'NJA': data['defense_candidates']['detection_analytics'], 'MIT': data['defense_candidates']['mitigations']}
for entity, items in groups.items():
    for item, ident in zip(items, ids[entity], strict=True):
        mapping[item['temporary_key']] = ident
mapping['B010-T1018-REF-SSHCONFIG'] = 'REF-000614'
(RUN / 'canonical-id-map.json').write_text(json.dumps(mapping, indent=2) + '\n')


def canonical(value):
    if isinstance(value, str):
        return mapping.get(value, value)
    if isinstance(value, list):
        return [canonical(item) for item in value]
    if isinstance(value, dict):
        return {key: canonical(item) for key, item in value.items()}
    return value


def lifecycle():
    return {'status': 'draft', 'version': '0.1.0', 'created': TODAY, 'modified': TODAY,
            'contributors': ['Niji Matrix Research'], 'reviewers': []}


def ordered(obj, fields):
    assert set(obj) == set(fields), set(obj).symmetric_difference(fields)
    return {field: obj[field] for field in fields}


written = []
extended = []
before = {}


def write(relative, obj):
    path = ROOT / relative
    assert not path.exists(), f'Refusing to overwrite a new object: {path}'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(canonical(obj), allow_unicode=True, sort_keys=False, width=120))
    written.append(str(path.relative_to(ROOT)))


def extend_ref(ident, locator, zh, en, url=None, published=None, title=None):
    path = next((ROOT / 'references').glob(ident + '-*.yaml'))
    before[str(path.relative_to(ROOT))] = path.read_text()
    obj = yaml.safe_load(path.read_text())
    obj['accessed'] = TODAY
    obj['locator'] = (obj.get('locator') or '') + '; ' + locator
    obj['notes_zh'] = (obj.get('notes_zh') or '') + ' ' + zh
    obj['notes_en'] = (obj.get('notes_en') or '') + ' ' + en
    if url:
        obj['url'] = url
    if published:
        obj['published'] = published
    if title:
        obj['title_zh'], obj['title_en'] = title
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))
    extended.append(str(path.relative_to(ROOT)))


for item in groups['REF']:
    ident = mapping[item['temporary_key']]
    obj = {'schema_version': '1.0.0', 'type': 'reference', 'id': ident,
           'title_zh': item['title_zh'], 'title_en': item['title_en'],
           'source_type': item['source_type'],
           'identifiers': {'doi': None, 'rfc': None, 'arxiv': None, 'attack_id': None, 'other': []},
           'authors': item.get('authors', []), 'publisher': item.get('publisher'),
           'published': item.get('published'), 'url': item['url'], 'accessed': TODAY,
           'locator': item['locator'], 'archive_url': None, 'credibility': item['credibility'],
           'notes_zh': item.get('notes_zh', ''), 'notes_en': item.get('notes_en', '')}
    slug = item['temporary_key'].removeprefix('B010-T1018-REF-').lower()
    write(f'references/{ident}-remote-system-{slug}.yaml', obj)

extend_ref('REF-000625', 'Enterprise 19.1 T1018 v3.6 and zero child rows, independently extracted from the local techniques workbook in BATCH-TA0007-010/fixed-baseline-T1018.json',
           '本批仅用作远程系统发现父行为和零子项基线，不证明原生分类或检测效果。',
           'This delivery uses it only for Remote System Discovery parent scope and the zero-child baseline, not native taxonomy or detector effects.')
extend_ref('REF-000988', 'Original publication HermeticWizard section: known-IP gathering API list, subsequent connection validation and optional /24 expansion; preserve prior HermeticWiper disk-write locators',
           '补充已知地址收集与后继验证的阶段边界；不把全部 API 清单视为本地无网络读取。原始出版物替代此前转刊地址 https://www.esetngblog.com/post/isaacwiper-and-hermeticwizard-new-wiper-and-worm-targeting-ukraine，既有块层破坏事实仍适用。',
           'Adds known-address gathering and later-validation boundaries without treating the entire API list as local or network-free. The original publication replaces the prior repost URL; existing block-level destruction facts remain applicable.',
           url='https://www.welivesecurity.com/2022/03/01/isaacwiper-hermeticwizard-wiper-worm-targeting-ukraine/', published='2022-03-01')
extend_ref('REF-000230', 'Events 1, 3 and 22: process context; TCP/UDP network connections disabled by default; DNS queries may be cached; no arbitrary cache-read API result guarantee',
           '本批支持命令级上下文及缓存查询仍可有事件的限制，不提供主机候选返回表或一般文件读取结果。',
           'Supports command-level context and the possibility of cached-query events, not returned host-candidate tables or general file-read results.')
extend_ref('REF-000614', 'HashKnownHosts: new entries hashed, existing names not automatically converted; Host patterns and Hostname; prior ControlMaster/ControlPath/ForwardAgent locators preserved',
           '扩充同一手册中的已知主机标识保护和配置语义；不改变既有控制连接能力结论，哈希不防止验证已知候选。',
           'Extends the same manual with known-host identifier protection and configuration semantics while preserving prior connection-control conclusions; hashing does not prevent testing known candidates.',
           title=('OpenBSD ssh_config 配置手册', 'OpenBSD ssh_config Configuration Manual'))
extend_ref('REF-000201', 'Configured read-access auditing and persistent rules; Audit log grouping; preserve existing EXECVE coverage',
           '为目标 SSH 与主机资料的审计规则提供配置依据；不把可读打开等同正文取得。',
           'Supports configured auditing of targeted SSH and host material without equating read-capable opens with content acquisition.')
extend_ref('REF-000840', 'Read-access rule semantics, mount constraints, rule listing, auditctl -s enabled/lost/backlog and performance guidance',
           '本批要求规则和采集健康可核验，主机标识由采集器元数据提供；无事件不证明未访问。',
           'This delivery requires verifiable rule and collection health with collector-provided host identity; absent events do not establish no access.')

claim_types = {'B010-T1018-CLM-PARENT': 'technique-relevance',
               'B010-T1018-CLM-LOCAL-READ': 'technique-boundary',
               'B010-T1018-CLM-KINSING': 'subtechnique-existence',
               'B010-T1018-CLM-HERMETIC': 'case-attribution',
               'B010-T1018-CLM-CANDIDATE-NOT-LIVE': 'technique-boundary',
               'B010-T1018-CLM-OBSERVATION-GAP': 'mechanism-mapping'}
modes = {'documentation': 'strongly-inferred', 'observed': 'directly-observed',
         'inference': 'strongly-inferred', 'strongly-inferred': 'strongly-inferred'}
for item in groups['CLM']:
    ident = mapping[item['temporary_key']]
    obj = {'schema_version': '1.0.0', 'type': 'claim', 'id': ident,
           'claim_type': claim_types.get(item['temporary_key'], item['claim_type']),
           'statement_zh': item['statement']['zh'], 'statement_en': item['statement']['en'],
           'subject_refs': item['subject_keys'], 'evidence_refs': item['evidence_keys'],
           'evidence_mode': modes[item['evidence_mode']], 'confidence': item['confidence'], 'status': 'draft'}
    write(f'claims/{ident}-remote-system-{item["temporary_key"].removeprefix("B010-T1018-CLM-").lower()}.yaml', obj)

for item in groups['CASE']:
    ident = mapping[item['temporary_key']]
    is_kinsing = item['temporary_key'].endswith('KINSING')
    obj = {'schema_version': '1.0.0', 'type': 'case', 'id': ident,
           'name_zh': item['name']['zh'], 'name_en': item['name']['en'],
           'actor_or_campaign': 'Kinsing' if is_kinsing else None,
           'subject_refs': item['subject_keys'],
           'description_zh': '\n\n'.join(x['zh'] for x in item['description']['paragraphs']),
           'description_en': '\n\n'.join(x['en'] for x in item['description']['paragraphs']),
           'time_range': None if is_kinsing else '2022-02-23',
           'target_sectors_zh': [], 'target_sectors_en': [],
           'evidence_refs': item['evidence_keys'], 'confidence': 'high', 'status': 'draft'}
    write(f'cases/{ident}-{item["temporary_key"].removeprefix("B010-T1018-CASE-").lower()}-host-knowledge.yaml', obj)

analytic_by_key = {}
for item in groups['NJA']:
    obj = deepcopy(item)
    obj.update({'schema_version': '2.0.0', 'type': 'detection-analytic',
                'id': obj.pop('temporary_key'), 'strategy_ref': obj.pop('strategy_key'),
                'evidence_refs': obj.pop('evidence_keys'), 'lifecycle': lifecycle()})
    obj = ordered(obj, ['schema_version', 'type', 'id', 'strategy_ref', 'name', 'summary', 'domains', 'platforms',
                        'logic', 'data_requirements', 'observables', 'correlation', 'false_positives', 'blind_spots',
                        'tuning_guidance', 'evidence_refs', 'lifecycle'])
    analytic_by_key[item['temporary_key']] = obj
    write(f'analytics/{mapping[item["temporary_key"]]}-remote-system-{item["temporary_key"].removeprefix("B010-T1018-NJA-").lower()}.yaml', obj)

for item in groups['DET']:
    obj = deepcopy(item)
    evidence = set(obj.pop('evidence_keys'))
    for key in obj['analytic_keys']:
        evidence.update(analytic_by_key[key]['evidence_refs'])
    obj.update({'schema_version': '2.0.0', 'type': 'detection-strategy',
                'id': obj.pop('temporary_key'), 'detects_refs': obj.pop('detects_keys'),
                'analytic_refs': obj.pop('analytic_keys'), 'evidence_refs': sorted(evidence),
                'lifecycle': lifecycle()})
    obj = ordered(obj, ['schema_version', 'type', 'id', 'name', 'summary', 'description', 'detects_refs', 'domains',
                        'analytic_refs', 'evidence_refs', 'lifecycle'])
    write(f'detections/{mapping[item["temporary_key"]]}-remote-system-{item["temporary_key"].removeprefix("B010-T1018-DET-").lower()}.yaml', obj)

for item in groups['MIT']:
    obj = deepcopy(item)
    obj.update({'schema_version': '2.0.0', 'type': 'mitigation',
                'id': obj.pop('temporary_key'), 'evidence_refs': obj.pop('evidence_keys'),
                'lifecycle': lifecycle()})
    for index, app in enumerate(obj['applications']):
        obj['applications'][index] = {'target_ref': app.pop('target_key'), **app}
    obj = ordered(obj, ['schema_version', 'type', 'id', 'name', 'summary', 'description', 'domains',
                        'measures', 'applications', 'evidence_refs', 'lifecycle'])
    write(f'mitigations/{mapping[item["temporary_key"]]}-existing-host-knowledge-governance.yaml', obj)

recommendation = data['recommendation']
decision = {'schema_version': '1.1.0', 'type': 'technique-decision', 'id': 'DEC-TA0007-T1018',
            'tactic_ref': 'TA0007',
            'candidate': {'source_type': 'attack', 'source_attack_id': 'T1018', 'source_attack_version': '19.1',
                          'name_zh': data['candidate']['name']['zh'], 'name_en': data['candidate']['name']['en']},
            'decision': 'retain',
            'rationale_zh': '\n\n'.join(p['zh'] for p in recommendation['rationale']['paragraphs']),
            'rationale_en': '\n\n'.join(p['en'] for p in recommendation['rationale']['paragraphs']),
            'scope_notes_zh': '\n\n'.join(p['zh'] for p in recommendation['scope_notes']['paragraphs']),
            'scope_notes_en': '\n\n'.join(p['en'] for p in recommendation['scope_notes']['paragraphs']),
            'gap_statement_zh': None, 'gap_statement_en': None,
            'original_attack_subtechniques_imported': False, 'resulting_technique_ref': parent,
            'evidence_refs': recommendation['evidence_keys'], 'confidence': 'medium',
            'review': {'status': 'draft', 'authors': ['Niji Matrix Research'], 'reviewers': [],
                       'review_notes_zh': '独立研究、准入和主审收敛完成，正式内容进入质量、Bundle 与双语 Web 验收。',
                       'review_notes_en': 'Independent research, admission, and primary convergence are complete; canonical content enters quality, bundle, and bilingual Web acceptance.'}}
write('matrix/tactics/TA0007-discovery/decisions/DEC-TA0007-T1018.yaml', decision)

reader_fields = ['definition_and_concept', 'stealth_characteristics', 'scope_boundary_definition',
                 'application_scenarios_and_threat_model', 'stealth_mechanisms']


def reader_body(content):
    body = {key: deepcopy(content[key]) for key in reader_fields}
    for mechanism in body['stealth_mechanisms']:
        mechanism['evidence_refs'] = mechanism.pop('evidence_keys')
    body['stealth_mechanisms'] = [ordered(m, ['mechanism_ref', 'role', 'summary', 'analysis', 'evidence_refs', 'confidence'])
                                 for m in body['stealth_mechanisms']]
    return body


references = sorted(set(data['existing_library_reuse']['reference_refs'] + ids['REF']))
strategies = ids['DET']
mitigations = ids['MIT']
defense = {'detections': {'coverage': 'available', 'strategy_refs': strategies},
           'mitigations': {'coverage': 'available', 'mitigation_refs': mitigations}}
pc = data['proposed_content']
technique = {'schema_version': '2.0.0', 'type': 'technique', 'id': parent,
             'name': data['candidate']['name'], 'summary': pc['summary'], 'aliases': [],
             'classification': {'tactic_refs': ['TA0007'],
                                'origin': {'kind': 'attack-retained', 'source_attack_id': 'T1018', 'source_attack_version': '19.1'},
                                'decision_ref': 'DEC-TA0007-T1018'}}
technique.update(reader_body(pc))
technique['subtechnique_taxonomy'] = {'narrative': pc['subtechnique_taxonomy']['narrative'],
                                   'coverage': 'established', 'subtechnique_refs': [child]}
technique['defense'] = defense
technique['evidence'] = {'claim_refs': ids['CLM'], 'case_refs': ids['CASE'], 'reference_refs': references}
technique['research'] = {'limitations': data['research']['limitations']}
technique['lifecycle'] = lifecycle()
parent_dir = f'matrix/tactics/TA0007-discovery/techniques/{parent}-remote-system-discovery'
write(parent_dir + '/technique.yaml', technique)

content = data['proposed_subtechniques'][0]
subtechnique = {'schema_version': '2.0.0', 'type': 'evasion-subtechnique', 'id': child,
                'name': content['name'], 'summary': content['summary'], 'aliases': content['aliases'],
                'parent_ref': parent, 'lineage': {'attck_subtechnique_inherited': False}}
subtechnique.update(reader_body(content))
subtechnique['defense'] = deepcopy(defense)
subtechnique['evidence'] = {'claim_refs': [item['temporary_key'] for item in groups['CLM'] if content['temporary_key'] in item['subject_keys']],
                          'case_refs': ids['CASE'], 'reference_refs': references}
subtechnique['research'] = content['research']
subtechnique['lifecycle'] = lifecycle()
write(parent_dir + f'/subtechniques/{child}-local-host-knowledge-reuse/subtechnique.yaml', subtechnique)

plan_path = ROOT / 'planning/tactics/TA0007.yaml'
before[str(plan_path.relative_to(ROOT))] = plan_path.read_text()
plan = yaml.safe_load(plan_path.read_text())
work = next(w for w in plan['work_items'] if w['source_attack_id'] == 'T1018')
assert work['stage'] == 'researching'
work['stage'] = 'authoring'
work['decision_ref'] = decision['id']
work['resulting_technique_ref'] = parent
plan['candidate_inventory']['last_synced'] = TODAY
plan_path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))
(RUN / 'shared-objects-before.json').write_text(json.dumps(before, ensure_ascii=False, indent=2) + '\n')
(RUN / 'written-object-paths.json').write_text(json.dumps(written, ensure_ascii=False, indent=2) + '\n')
(RUN / 'extended-object-paths.json').write_text(json.dumps(extended, ensure_ascii=False, indent=2) + '\n')
(RUN / 'canonical-parent-paths.json').write_text(json.dumps({parent: parent_dir + '/technique.yaml'}, indent=2) + '\n')
print(json.dumps({'parent': parent, 'child': child, 'new_objects': len(written), 'extended_references': len(extended)}, ensure_ascii=False))
