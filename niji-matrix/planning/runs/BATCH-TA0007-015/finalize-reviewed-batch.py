"""Promote this accepted delivery and record actual results, without publication."""
from pathlib import Path
import json
import re
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
IDS = json.loads((RUN / 'allocated-ids.json').read_text())
SCOPE = list(IDS['parents'])
quality = (RUN / 'quality.log').read_text()
web = (RUN / 'web-tests.log').read_text()
assert '校验通过：0 个错误，0 个警告。' in quality
assert '规划校验通过：0 个错误，0 个警告。' in quality
assert '0 组精确重复，0 组待审可能重复' in quality
assert 'Reader-prose audit passed: 204 parents' in quality
assert 'Ran 12 tests' in quality and '\nOK\n' in quality
assert 'dist/catalogs/library-catalog.json:' in quality
assert re.search(r'\bpass\s+140\b', web) and re.search(r'\bfail\s+0\b', web)
pages = 0
for ident in IDS['NJT']:
    report = json.loads((RUN / 'web-qa' / ident / 'report.json').read_text())
    assert report['status'] == 'passed' and report['api_issues'] == [] and report['browser_errors'] == []
    pages += len(report['pages'])
assert pages == 78

# Use descriptive paths for the final packages; IDs and parent_ref remain authoritative.
parent_slugs = {'T1680': 'local-storage-discovery', 'T1654': 'log-enumeration',
                'T1046': 'network-service-discovery', 'T1135': 'network-share-discovery',
                'T1040': 'passive-network-traffic-mapping'}
child_slugs = {'T1046': 'service-advertisement-lookup-substitution',
               'T1040': 'active-name-enrichment-suppression'}
parent_paths = json.loads((RUN / 'canonical-parent-paths.json').read_text())
paths = json.loads((RUN / 'written-object-paths.json').read_text())
replacements = []
for attack, old_file in list(parent_paths.items()):
    old_dir = Path(old_file).parent
    if attack in child_slugs:
        old_child = next((ROOT / old_dir / 'subtechniques').iterdir())
        child_id = yaml.safe_load((old_child / 'subtechnique.yaml').read_text())['id']
        new_child = old_child.parent / f'{child_id}-{child_slugs[attack]}'
        assert not new_child.exists()
        old_child.rename(new_child)
        replacements.append((str(old_child.relative_to(ROOT)), str(new_child.relative_to(ROOT))))
    new_dir = old_dir.parent / f'{IDS["parents"][attack]}-{parent_slugs[attack]}'
    assert not (ROOT / new_dir).exists()
    (ROOT / old_dir).rename(ROOT / new_dir)
    replacements.append((str(old_dir), str(new_dir)))
    parent_paths[attack] = str(new_dir / 'technique.yaml')
for old, new in replacements:
    paths = [p.replace(old, new, 1) if p.startswith(old) else p for p in paths]
(RUN / 'written-object-paths.json').write_text(json.dumps(paths, indent=2) + '\n')
(RUN / 'canonical-parent-paths.json').write_text(json.dumps(parent_paths, indent=2) + '\n')

for relative in paths:
    path = ROOT / relative
    obj = yaml.safe_load(path.read_text())
    if 'lifecycle' in obj:
        assert obj['lifecycle']['status'] == 'draft'
        obj['lifecycle']['status'] = 'review'
    elif obj['type'] in {'claim', 'case'}:
        assert obj['status'] == 'draft'
        obj['status'] = 'review'
    elif obj['type'] == 'technique-decision':
        obj['review']['status'] = 'review'
        obj['review']['review_notes_zh'] = '候选证据、原生分类、跨候选边界、双语字段深度、共享库去重、ID 同步、质量、Bundle 和实际双语 Web 门禁均通过；保持 review 等待人工领域审查。'
        obj['review']['review_notes_en'] = 'Candidate evidence, native taxonomy, cross-candidate boundaries, bilingual field depth, shared-library identity, ID sync, quality, bundles, and actual bilingual Web gates pass; retain review pending human domain approval.'
    else:
        continue
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))

path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(path.read_text())
next(b for b in plan['batches'] if b['id'] == 'BATCH-TA0007-015')['status'] = 'review'
candidate_results = []
for work in plan['work_items']:
    attack = work['source_attack_id']
    if attack not in SCOPE:
        continue
    work['stage'] = 'review'
    decision = 'adapt' if attack in {'T1680', 'T1040'} else 'retain'
    children = [IDS['NJS'][0]] if attack == 'T1046' else [IDS['NJS'][1]] if attack == 'T1040' else []
    work['notes_zh'] += f' 本批 {decision} 形成 {IDS["parents"][attack]}，正式 NJS {len(children)} 项；独立研究、主审、质量、Bundle 与双语 Web 验收通过，等待人工领域审查。'
    work['notes_en'] += f' This batch {decision} admission produced {IDS["parents"][attack]} with {len(children)} formal NJS; independent research, primary review, quality, bundle and bilingual Web acceptance pass pending human domain review.'
    candidate_results.append({'source_attack_id': attack, 'decision': decision,
                              'technique_ref': IDS['parents'][attack], 'subtechnique_refs': children})
plan['candidate_inventory']['last_synced'] = '2026-11-05'
plan['gap_analysis']['notes_zh'] = '固定 Enterprise 19.1 TA0007 的 34 个父候选已完整登记，现已完成 18 项准入决策：正式技术 17 项，其中 T1622 跨战术复用 NJT-0106；T1538 已 exclude。正式 NJS 共 6 项。本批完成 T1680、T1654、T1046、T1135、T1040，新增 NJT 5、NJS 2；主动名称补全抑制为中等置信度能力证据子项，不虚构现场采用。另有 16 个父候选待准入；战术级 Niji 原生缺口与最终收敛仍待后续，人工领域审查未完成。'
plan['gap_analysis']['notes_en'] = 'All 34 fixed Enterprise 19.1 TA0007 parent candidates are registered. Eighteen admission decisions yield seventeen formal techniques, including cross-tactic reuse of NJT-0106 for T1622; T1538 is excluded. Six formal NJS exist. This batch completed T1680, T1654, T1046, T1135 and T1040, adding five NJT and two NJS. Active Name-Enrichment Suppression is a medium-confidence capability-evidenced child without invented field adoption. Sixteen parents still await admission; tactic-wide Niji-native gaps and final convergence remain open, and human domain review is pending.'
path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))

summary = {
    'schema_version': '1.0.0', 'type': 'batch-integration-summary', 'batch_ref': 'BATCH-TA0007-015', 'status': 'review',
    'delivery_control': {'overall_candidate_count': 34, 'batch_candidate_count': 5,
        'batch_size_rationale': {'zh': '用户要求继续五项；五份独立研究分两轮完成，全部交接与补充分类返回后才统一准入、分配和写入，逐候选门禁独立保留。',
                                'en': 'The user requested five more candidates. Five independent handoffs were delivered in two waves, with admission, allocation and writing only after all handoffs and the bounded taxonomy supplement returned; candidate gates remain independent.'},
        'previous_batch_gate_passed': True, 'research_subagent_count': 5, 'research_waves': 2,
        'canonical_integration_after_complete_handoffs': True},
    'candidate_results': candidate_results,
    'shared_library_resolutions': {
        'reuse': ['REF-000840', 'REF-000994', 'REF-000334', 'REF-000366', 'REF-000463', 'REF-000474', 'REF-000476', 'REF-000598', 'REF-000623', 'REF-000634', 'REF-000791', 'REF-000792', 'REF-000794', 'REF-000795', 'REF-000796', 'REF-000797', 'REF-000801', 'REF-000819', 'REF-000200'],
        'extend': ['REF-000073', 'REF-001049', 'REF-000639', 'REF-000625', 'CASE-000259', 'MIT-000186 applications'],
        'create_ranges': {'references': 'REF-001217..REF-001260', 'claims': 'CLM-001178..CLM-001205',
                          'cases': 'CASE-000357..CASE-000363', 'detection_strategies': 'DET-000274..DET-000280',
                          'detection_analytics': 'NJA-000370..NJA-000384', 'mitigations': 'MIT-000241..MIT-000244', 'relationships': None}},
    'deferred_hypotheses': ['T1680 storage axes remain deferred after direct-object and evidence review.',
        'T1654 feedback purpose does not establish an acquisition-side stealth child.',
        'Unadmitted T1046 scan variables do not copy NJT-0001 children into a new phase.',
        'T1135 timing, origin and inspectability axes lack independent intentional trace evidence.',
        'T1040 has no qualifying victim-specific environmental-outcome Case; remaining axes stay deferred or adjacent.',
        'The name-enrichment child is capability-evidenced, not an observed malicious procedure or measured miss rate.'],
    'duplicate_resolution_refs': [],
    'semantic_validation': {'candidate_level_gates_passed': True, 'conclusion_level_evidence_passed': True,
        'njt_0001_field_responsibility_reviewed': True, 'bilingual_argument_depth_passed': True,
        'boilerplate_review_passed': True, 'taxonomy_breadth_reviewed': True,
        'attack_breadth_gap_explained': True, 'canonical_prose_bulk_generated': False},
    'validation': {'matrix_objects': 4338, 'schema_errors': 0, 'schema_warnings': 0,
        'unresolved_duplicate_candidates': 0, 'reviewed_similarity_resolutions': 12,
        'infrastructure_tests': 12, 'web_tests': 140, 'web_api_issues': 0,
        'bilingual_browser_pages': pages, 'browser_errors': 0, 'bundles_built': IDS['NJT'],
        'unexplained_reserved_ids': 0, 'real_host_device_or_cloud_experiment_performed': False},
    'integration_corrections': ['Recovered silently split bilingual flow scalars before canonical projection.',
        'Normalized native field spellings to canonical machine keys while preserving data-field-normalization.json.',
        'Resolved the relocated official WithSecure PDF and reused one publication across two distinct cases.',
        'Removed planning language and supplied complete bilingual correlation windows.',
        'Changed the existing shared-mitigation test to preserve required credential targets and target uniqueness without freezing all future applications.'],
    'review_notes_zh': '五项候选完成独立准入：T1680、T1040 adapt，T1654、T1046、T1135 retain。新增五项 NJT、两项原生 NJS、七项 DET、十五项 NJA、四项 MIT，并扩展 MIT-000186 两个应用；四十四项来源、二十八项原子主张与七个限定观察范围的案例完成共享身份审查。名称补全子项由 NIST 明确匿迹说明和固定 tcpdump 手册支持，保持 medium，不制造现场案例。内容、规划、重复、正文、十二项基础设施测试、一百四十项 Web 测试、五个 Bundle 和七十八个实际双语页面均通过；保持 review，等待人工领域审查和部署验证。TA0007 现有十七项正式技术、六项 NJS、一项排除，剩余十六个父候选，战术未关闭。',
    'review_notes_en': 'Five candidates completed independent admission: adapt for T1680 and T1040, retain for T1654, T1046 and T1135. Five NJT, two native NJS, seven DET, fifteen NJA and four MIT were created, with two MIT-000186 applications, forty-four sources, twenty-eight atomic claims and seven narrowly scoped cases after shared-identity review. The name-enrichment child has explicit NIST stealth rationale and pinned tcpdump capability support at medium confidence without a fabricated field case. Content, planning, duplicate and prose gates, twelve infrastructure tests, 140 Web tests, five bundles and 78 actual bilingual pages pass. Keep review pending human domain approval and deployment validation. TA0007 has seventeen formal techniques, six NJS, one exclusion and sixteen parents awaiting admission; the tactic remains open.'}
(RUN / 'integration-summary.yaml').write_text(yaml.safe_dump(summary, allow_unicode=True, sort_keys=False, width=120))
print(json.dumps({'batch': 'BATCH-TA0007-015', 'status': 'review', 'new_njt': 5, 'new_njs': 2,
                  'TA0007': {'decisions': 18, 'formal_techniques': 17, 'njs': 6, 'excluded': 1, 'remaining': 16}}, ensure_ascii=False))
