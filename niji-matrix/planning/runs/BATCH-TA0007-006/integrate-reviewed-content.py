"""Serialize the individually reviewed T1615 handoff and primary-authored defense.

Semantic decisions and prose are in the handoff, admission record and primary-defense.yaml.
This script performs explicit field mapping, ID replacement and mechanical serialization.
"""
from copy import deepcopy
from pathlib import Path
import json
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
HANDOFF = yaml.safe_load((RUN / 'T1615-research-handoff.yaml').read_text())
PRIMARY = yaml.safe_load((RUN / 'primary-defense.yaml').read_text())
IDS = json.loads((RUN / 'allocated-ids.json').read_text())
TODAY = '2026-11-05'
PARENT = IDS['NJT'][0]
MAP = {
    'B006-T1615-PARENT': PARENT,
    'B006-T1615-REF-ATTACK': 'REF-000625',
    'B006-T1615-DET-POLICY-READ': IDS['DET'][0],
    'B006-T1615-NJA-ENDPOINT': IDS['NJA'][0],
    'B006-T1615-NJA-DIRECTORY': IDS['NJA'][1],
    'B006-T1615-NJA-SYSVOL': IDS['NJA'][2],
    'B006-T1615-MIT-READ-GOVERNANCE': IDS['MIT'][0],
    'B006-T1615-CASE-TURLA-POLICY-SURVEY': IDS['CASE'][0],
}
REF_KEYS = ['GPRESULT', 'RESULTS', 'PROTOCOL', '4662', 'MS16-072', 'CACHE']
for key, ident in zip(REF_KEYS, IDS['REF'], strict=True):
    MAP['B006-T1615-REF-' + key] = ident
for item, ident in zip(HANDOFF['library_candidates']['claims'], IDS['CLM'], strict=True):
    MAP[item['temporary_key']] = ident


def canonical(value):
    if isinstance(value, str):
        return MAP.get(value, value)
    if isinstance(value, list):
        return [canonical(item) for item in value]
    if isinstance(value, dict):
        return {key: canonical(item) for key, item in value.items()}
    return value


def lifecycle():
    return {'status': 'draft', 'version': '0.1.0', 'created': TODAY, 'modified': TODAY,
            'contributors': ['Niji Matrix Research'], 'reviewers': []}


written = []


def write(relative, obj):
    path = ROOT / relative
    assert not path.exists(), f'Refusing to overwrite new object {path}'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(canonical(obj), allow_unicode=True, sort_keys=False, width=120))
    written.append(str(path.relative_to(ROOT)))


# All six exact source identities were reviewed against the generated canonical catalog.
for key, ident in zip(REF_KEYS, IDS['REF'], strict=True):
    r = next(r for r in HANDOFF['library_candidates']['references']
             if r['temporary_key'] == 'B006-T1615-REF-' + key)
    obj = {'schema_version': '1.0.0', 'type': 'reference', 'id': ident,
           'title_zh': r['title']['zh'], 'title_en': r['title']['en'],
           'source_type': 'official-documentation', 'authors': r['authors'],
           'publisher': 'Microsoft Support' if key == 'MS16-072' else 'Microsoft Learn',
           'published': r.get('published'), 'url': r['url'], 'accessed': TODAY,
           'locator': r['locator'], 'archive_url': None, 'credibility': 'high',
           'notes_zh': r['supported']['zh'] + r['limits']['zh'],
           'notes_en': r['supported']['en'] + ' ' + r['limits']['en']}
    write(f'references/{ident}-group-policy-{key.lower()}.yaml', obj)

# Extend the same publication without replacing its existing C2 meaning or canonical URL.
path = next((ROOT / 'references').glob('REF-001049-*.yaml'))
ref = yaml.safe_load(path.read_text())
ref['title_zh'] = '从 Agent.BTZ 到 ComRAT v4：十年历程'
ref['accessed'] = TODAY
ref['locator'] += '; policy reconnaissance: article Insight into attacker activity, Figure 3; linked report section 3.4, printed page 8, Figure 6, https://www.welivesecurity.com/wp-content/uploads/2020/05/ESET_Turla_ComRAT.pdf'
ref['notes_zh'] += ' 同一研究的正文与关联白皮书记录 gpresult /z 和 /v 操作者命令；它们支持组策略调查尝试，不证明完整返回值、独立匿迹子技术或告警规避。'
ref['notes_en'] += ' The article and linked report from the same research record operator gpresult /z and /v commands, supporting policy-survey attempts without establishing complete returned values, a distinct stealth child, or alert evasion.'
path.write_text(yaml.safe_dump(ref, allow_unicode=True, sort_keys=False, width=120))

path = next((ROOT / 'references').glob('REF-000625-*.yaml'))
ref = yaml.safe_load(path.read_text())
ref['locator'] += '; Enterprise 19.1 T1615 Group Policy Discovery and zero ATT&CK children, independently checked against the local versioned techniques workbook'
ref['accessed'] = TODAY
path.write_text(yaml.safe_dump(ref, allow_unicode=True, sort_keys=False, width=120))

claim_types = ['technique-boundary', 'mechanism-mapping', 'detection', 'mitigation', 'case-attribution']
for i, r in enumerate(HANDOFF['library_candidates']['claims']):
    ident = MAP[r['temporary_key']]
    subjects = [PARENT]
    if i == 2:
        subjects += IDS['DET'] + IDS['NJA'][1:]
    if i == 3:
        subjects += IDS['MIT']
    if i == 4:
        subjects += IDS['CASE']
    obj = {'schema_version': '1.0.0', 'type': 'claim', 'id': ident,
           'claim_type': claim_types[i], 'statement_zh': r['statement']['zh'],
           'statement_en': r['statement']['en'], 'subject_refs': subjects,
           'evidence_refs': r['evidence_keys'],
           'evidence_mode': 'directly-observed' if i == 4 else 'strongly-inferred',
           'confidence': r['confidence'], 'status': 'draft'}
    write(f'claims/{ident}-group-policy-{r["temporary_key"].removeprefix("B006-T1615-CLM-").lower()}.yaml', obj)

r = HANDOFF['library_candidates']['cases'][0]
case = {'schema_version': '1.0.0', 'type': 'case', 'id': IDS['CASE'][0],
        'name_zh': r['name']['zh'], 'name_en': r['name']['en'],
        'actor_or_campaign': r['actor_or_campaign'], 'subject_refs': [PARENT],
        'description_zh': r['description']['zh'] + ' 报告的总体受害机构不能直接绑定到此命令清单，故本案例不指定命令对应的目标行业。',
        'description_en': r['description']['en'] + ' The report does not map its aggregate victim institutions to these commands, so this case assigns no command-specific target sector.',
        'time_range': None, 'target_sectors_zh': [], 'target_sectors_en': [],
        'evidence_refs': r['evidence_keys'], 'confidence': 'high', 'status': 'draft'}
write(f'cases/{IDS["CASE"][0]}-turla-comrat-group-policy-query.yaml', case)

# Endpoint analytic: retain the reviewed process and script design, but keep optional
# observation requirements in the schema's one data_requirements model.
endpoint = deepcopy(HANDOFF['defense_candidates']['detection_analytics'][0])
endpoint['schema_version'] = '2.0.0'
endpoint['type'] = 'detection-analytic'
endpoint['id'] = endpoint.pop('temporary_key')
endpoint['strategy_ref'] = endpoint.pop('strategy_key')
endpoint['evidence_refs'] = endpoint.pop('evidence_keys')
optional = endpoint.pop('optional_data_requirements')
for item in optional:
    item['name']['zh'] = '启用补充分支时的' + item['name']['zh']
    item['name']['en'] = 'When the supplemental branch is enabled: ' + item['name']['en']
endpoint['data_requirements'] += optional
endpoint['logic']['paragraphs'][0] = {
    'zh': '基础查询识别分支使用完整进程创建和批准任务清单，选择 gpresult 带 /r、/v、/z、/h 或 /x 的结果请求，规范化 /s、/user、/scope 与输出目标。单独帮助或无有效查询语义的参数保留为帮助或错误上下文；有效查询即使后来失败也保留 policy_query_failed，不由失败反推无攻击意图。Sysmon 事件 1 不包含命令返回内容或可靠的执行成功状态，不能据此判定请求成功。',
    'en': 'The base query-identification branch uses complete process creation and approved-work inventory to select gpresult result requests containing /r, /v, /z, /h, or /x and normalize /s, /user, /scope, and output destination. Help alone or arguments without valid query semantics remain help or error context. Retain policy_query_failed for a valid query that subsequently fails rather than inferring benign intent from failure. Sysmon event 1 contains neither command output nor reliable execution-success status and cannot establish query success.'}
endpoint['logic']['paragraphs'].append({
    'zh': '脚本与结果确认是按部署能力启用的补充分支，不是基础分支默认存在的数据。启用 Windows PowerShell 4104 时按 ScriptBlockId、MessageNumber 和 MessageTotal 重组同一脚本，再依据实际 Group Policy 或 RSoP 查询语义识别请求，不仅匹配函数名称；其他运行时须另验通道。启用结果采集时，用进程、生成时间和目标范围确认报表或输出内容有效；文件创建、已有同名报表或空结果均不足以升级证据。不能取得该补充数据时明确保持查询尝试等级。',
    'en': 'Script and result confirmation are supplemental branches enabled according to deployment capability, not data assumed by the base branch. With Windows PowerShell event 4104 enabled, reconstruct each script using ScriptBlockId, MessageNumber, and MessageTotal and identify actual Group Policy or RSoP query semantics rather than function names alone; validate channels separately for other runtimes. With result collection enabled, validate report or output content using process, generation time, and target scope. File creation, a preexisting report with the same name, or an empty result cannot raise the evidence level. Without supplemental data explicitly retain attempt-level evidence.'})
endpoint['lifecycle'] = lifecycle()
write(f'analytics/{IDS["NJA"][0]}-group-policy-resultant-query-lineage.yaml', endpoint)

for key, ident, slug in [('directory_analytic', IDS['NJA'][1], 'gpo-directory-property-read'),
                         ('sysvol_analytic', IDS['NJA'][2], 'sysvol-policy-template-read-grading')]:
    obj = deepcopy(PRIMARY[key]); obj['lifecycle'] = lifecycle()
    write(f'analytics/{ident}-{slug}.yaml', obj)

strategy = deepcopy(PRIMARY['strategy'])
strategy['evidence_refs'] = sorted(set(endpoint['evidence_refs'] + PRIMARY['directory_analytic']['evidence_refs'] + PRIMARY['sysvol_analytic']['evidence_refs']))
strategy['lifecycle'] = lifecycle()
write(f'detections/{IDS["DET"][0]}-group-policy-information-read-context.yaml', strategy)

mit = deepcopy(HANDOFF['defense_candidates']['mitigations'][0])
mit['schema_version'] = '2.0.0'
mit['type'] = 'mitigation'
mit['id'] = mit.pop('temporary_key')
mit['evidence_refs'] = mit.pop('evidence_keys')
for application in mit['applications']:
    application['target_ref'] = application.pop('target_key')
mit['lifecycle'] = lifecycle()
write(f'mitigations/{IDS["MIT"][0]}-group-policy-read-and-result-delegation-governance.yaml', mit)

recommendation = HANDOFF['recommendation']
decision = {'schema_version': '1.1.0', 'type': 'technique-decision',
            'id': 'DEC-TA0007-T1615', 'tactic_ref': 'TA0007',
            'candidate': {'source_type': 'attack', 'source_attack_id': 'T1615',
                          'source_attack_version': '19.1', 'name_en': 'Group Policy Discovery', 'name_zh': '组策略发现'},
            'decision': 'retain',
            'rationale_zh': recommendation['rationale']['paragraphs'][0]['zh'],
            'rationale_en': recommendation['rationale']['paragraphs'][0]['en'],
            'scope_notes_zh': recommendation['proposed_scope_notes']['paragraphs'][0]['zh'],
            'scope_notes_en': recommendation['proposed_scope_notes']['paragraphs'][0]['en'],
            'gap_statement_zh': '本地结果与缓存、范围收窄及时间或来源选择缺少有意控制与同案痕迹对照，原生子技术分类暂缓；未来按结论级证据重审。',
            'gap_statement_en': 'Local results and caches, scope narrowing, and timing or origin selection lack deliberate-control evidence and same-case trace comparisons; native taxonomy remains deferred for conclusion-level reassessment.',
            'original_attack_subtechniques_imported': False, 'resulting_technique_ref': PARENT,
            'evidence_refs': ['REF-000625', 'B006-T1615-REF-GPRESULT', 'B006-T1615-REF-RESULTS', 'B006-T1615-REF-PROTOCOL', 'REF-001049'],
            'confidence': 'medium',
            'review': {'status': 'draft', 'authors': ['Niji Matrix Research'], 'reviewers': [],
                       'review_notes_zh': '研究、准入、分类、证据限界与主审字段深度检查已完成，待机器、Bundle 和双语 Web 验收。',
                       'review_notes_en': 'Research, admission, taxonomy, evidence limits, and primary field-depth review are complete; machine, bundle, and bilingual Web acceptance remain.'}}
write('matrix/tactics/TA0007-discovery/decisions/DEC-TA0007-T1615.yaml', decision)

content = deepcopy(HANDOFF['proposed_content'])
taxonomy = content.pop('proposed_subtechnique_taxonomy')
taxonomy['subtechnique_refs'] = []
content['scope_boundary_definition']['paragraphs'][0] = {
    'zh': '纳入以理解组策略为直接目的的 GPO 标识、属性、链接、权限、策略文件和本地或远端结果策略集读取。已识别为策略对象的标识与关系本身就是策略信息，不要求每次取得完整模板内容；仅列普通文件或路径而没有识别策略对象、属性或应用关系时，归入 NJT-0182 文件与目录发现。一般账户、组和信任枚举仍由各自技术负责，文件或注册表查询应按取得的信息语义判断，而不是按命令名称归类。',
    'en': 'Include reads of GPO identities, properties, links, permissions, policy files, and local or remote resultant-policy data whose direct purpose is understanding Group Policy. Identities and relationships already recognized as policy objects are policy information without requiring complete template retrieval every time. A generic file or path listing without policy-object identity, attributes, or application relationships belongs to NJT-0182 File and Directory Discovery. General account, group, and trust enumeration retains its own owner; classify file or registry queries by the information acquired rather than the command name.'}
taxonomy['narrative']['paragraphs'][0] = {
    'zh': '已分别审查既有本地结果或缓存复用、目录与文件读取面选择、窄对象或属性范围、时间与客户端来源，以及控制台输出替代持久报表等变量。本地结果与缓存可能改变信息取得位置，但能力文档和 gpresult 案例尚未证明攻击者有意用它替代域侧查询或减少了哪些事件；缓存处理也可能联系域控制器，不能预设完全离线。其他轴缺乏同案痕迹与防御差异对照。',
    'en': 'The review separately examined existing local results or caches, directory versus file read planes, narrow object or attribute scope, timing and client origin, and console output instead of persistent reports. Local results and caches could change acquisition location, but capability documentation and the gpresult case do not establish deliberate substitution for domain queries or reductions in particular events. Cache processing can still contact a domain controller, so wholly offline operation must not be assumed. The other axes lack same-case trace and defensive comparisons.'}
mechanisms = content.pop('stealth_mechanisms')
for mechanism in mechanisms:
    mechanism['evidence_refs'] = mechanism.pop('evidence_keys')
parent = {'schema_version': '2.0.0', 'type': 'technique', 'id': PARENT,
          'name': HANDOFF['candidate']['name'], 'summary': content.pop('summary'), 'aliases': [],
          'classification': {'tactic_refs': ['TA0007'],
                             'origin': {'kind': 'attack-retained', 'source_attack_id': 'T1615', 'source_attack_version': '19.1'},
                             'decision_ref': 'DEC-TA0007-T1615'},
          **content, 'stealth_mechanisms': mechanisms, 'subtechnique_taxonomy': taxonomy,
          'defense': {'detections': {'coverage': 'available', 'strategy_refs': IDS['DET']},
                      'mitigations': {'coverage': 'available', 'mitigation_refs': IDS['MIT']}},
          'evidence': {'claim_refs': IDS['CLM'], 'case_refs': IDS['CASE'],
                       'reference_refs': ['REF-000625', 'REF-000341', 'REF-001049', 'REF-000366', 'REF-000463', 'REF-000377', 'REF-000474', 'REF-000379'] + IDS['REF']},
          'research': {'limitations': HANDOFF['research']['limitations']}, 'lifecycle': lifecycle()}
write(f'matrix/tactics/TA0007-discovery/techniques/{PARENT}-group-policy-discovery/technique.yaml', parent)

path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(path.read_text())
work = next(w for w in plan['work_items'] if w['source_attack_id'] == 'T1615')
work.update(decision_ref='DEC-TA0007-T1615', resulting_technique_ref=PARENT, stage='authoring')
path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))
taxonomy_record = deepcopy(HANDOFF['research']['taxonomy_breadth_review'])
taxonomy_record['primary_review'] = {'status': 'passed', 'formal_njs_count': 0,
                                    'conclusion': 'Retain parent; six axes reviewed; unsupported children remain deferred.',
                                    'admission_record': 'admission-and-convergence.md'}
(RUN / 'taxonomy-breadth-review.yaml').write_text(yaml.safe_dump(taxonomy_record, allow_unicode=True, sort_keys=False, width=120))
(RUN / 'written-object-paths.json').write_text(json.dumps(written, indent=2) + '\n')
print(json.dumps({'parent': PARENT, 'new_objects': len(written), 'new_njs': 0, 'paths': written}, ensure_ascii=False, indent=2))
