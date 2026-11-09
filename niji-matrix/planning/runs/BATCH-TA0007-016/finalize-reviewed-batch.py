"""Promote accepted content, verify final state and record the delivery."""
from pathlib import Path
import json
import re
import subprocess
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
IDS = json.loads((RUN / 'allocated-ids.json').read_text())
SCOPE = list(IDS['parents'])
assert all(x['exit_code'] == 0 for x in json.loads((RUN / 'machine-gate-results.json').read_text()))
assert all(x['exit_code'] == 0 for x in json.loads((RUN / 'after-polish-results.json').read_text()))
assert all(x['exit_code'] == 0 for x in json.loads((RUN / 'browser-run-results.json').read_text()))
quality = (RUN / 'quality.log').read_text()
web = (RUN / 'web-tests.log').read_text()
assert '校验通过：0 个错误，0 个警告。' in quality
assert '规划校验通过：0 个错误，0 个警告。' in quality
assert '0 组精确重复，0 组待审可能重复' in quality
assert 'Reader-prose audit passed: 209 parents' in quality
assert 'Ran 12 tests' in quality and '\nOK\n' in quality
assert 'dist/catalogs/library-catalog.json:' in quality
assert re.search(r'\bpass\s+140\b', web) and re.search(r'\bfail\s+0\b', web)
pages = 0
for ident in IDS['NJT']:
    report = json.loads((RUN / 'web-qa' / ident / 'report.json').read_text())
    assert report['status'] == 'passed' and report['api_issues'] == [] and report['browser_errors'] == []
    pages += len(report['pages'])
assert pages == 94, pages


def command(name, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    (RUN / (name + '.log')).write_text(p.stdout + p.stderr)
    assert p.returncode == 0, (name, p.stdout[-2000:], p.stderr[-2000:])
    print(json.dumps({'check': name, 'status': 'passed'}), flush=True)
    return p.stdout


# Verify Bundles contain the final reviewed wording before changing lifecycle.
for ident in IDS['NJT']:
    command('bundle-' + ident, ['python3', 'scripts/build_technique_bundle.py', ident])
paths = json.loads((RUN / 'written-object-paths.json').read_text())
for relative in paths:
    path = ROOT / relative
    o = yaml.safe_load(path.read_text())
    if 'lifecycle' in o:
        assert o['lifecycle']['status'] == 'draft'
        o['lifecycle']['status'] = 'review'
    elif o['type'] in {'claim', 'case'}:
        assert o['status'] == 'draft'
        o['status'] = 'review'
    elif o['type'] == 'technique-decision':
        o['review'].update(status='review', review_notes_zh='候选证据、准入、原生分类、双语字段深度、专用防御、共享库身份、ID 同步、质量、Bundle 与双语 Web 门禁均通过，等待人工领域审查。',
                          review_notes_en='Candidate evidence, admission, native taxonomy, bilingual field depth, subject-specific defenses, library identity, ID sync, quality, bundles, and bilingual Web gates pass pending human domain review.')
    else:
        continue
    path.write_text(yaml.safe_dump(o, allow_unicode=True, sort_keys=False, width=120))
for relative in json.loads((RUN / 'extended-object-paths.json').read_text()):
    if not relative.startswith('mitigations/'):
        continue
    path = ROOT / relative
    o = yaml.safe_load(path.read_text())
    assert o['lifecycle']['status'] == 'draft'
    o['lifecycle']['status'] = 'review'
    path.write_text(yaml.safe_dump(o, allow_unicode=True, sort_keys=False, width=120))

plan_path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(plan_path.read_text())
next(b for b in plan['batches'] if b['id'] == 'BATCH-TA0007-016')['status'] = 'review'
candidate_results = []
for work in plan['work_items']:
    attack = work['source_attack_id']
    if attack not in SCOPE:
        continue
    work['stage'] = 'review'
    decision = 'adapt' if attack == 'T1012' else 'retain'
    children = IDS['children'][attack]
    work['notes_zh'] += f' 本批 {decision} 形成 {IDS["parents"][attack]}，正式 NJS {len(children)} 项；独立研究、主审与全部验收通过，保持 review 等待人工领域审查。'
    work['notes_en'] += f' This batch {decision} admission produced {IDS["parents"][attack]} with {len(children)} formal NJS; independent research, primary review and acceptance pass, retaining review pending human domain approval.'
    candidate_results.append({'source_attack_id': attack, 'decision': decision, 'technique_ref': IDS['parents'][attack], 'subtechnique_refs': children})
assert len([w for w in plan['work_items'] if w.get('decision_ref')]) == 23
assert len([w for w in plan['work_items'] if not w.get('decision_ref')]) == 11
plan['gap_analysis']['notes_zh'] = '固定 Enterprise 19.1 TA0007 共 34 个父候选，已完成 23 项准入：正式技术 22 项，T1538 排除，正式 NJS 共 10 项。本批完成 T1201、T1120、T1069、T1057、T1012，新增 NJT 5、NJS 4；子项机理均保持中等置信，区分能力、样本设计和现场采用，不宣称实测规避。剩余 11 个父候选待准入；原生缺口与最终战术收敛仍开放，人工领域审查未完成。'
plan['gap_analysis']['notes_en'] = 'Fixed Enterprise 19.1 TA0007 has 34 parents and 23 completed admission decisions: 22 formal techniques, excluded T1538, and 10 formal NJS. This batch completed T1201, T1120, T1069, T1057 and T1012, adding five NJT and four NJS. Child mechanisms remain medium-confidence, separating capability, sample design and field adoption without claiming measured evasion. Eleven parents await admission; native gaps and final tactic convergence remain open, and human domain review is pending.'
plan_path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))

final_results = []
for name, args in [('final-validate', ['python3', 'scripts/validate.py']),
                   ('final-planning', ['python3', 'scripts/validate_planning.py']),
                   ('final-duplicates', ['python3', 'scripts/audit_duplicates.py', '--fail-on', 'exact']),
                   ('final-prose', ['python3', 'scripts/audit_reader_prose.py']),
                   ('final-catalog', ['python3', 'scripts/library_catalog.py']),
                   ('pipeline-status', ['python3', 'scripts/pipeline_status.py'])]:
    output = command(name, args)
    final_results.append({'check': name, 'exit_code': 0, 'tail': output[-600:]})
reserved = command('final-reservations', ['python3', 'scripts/allocate_id.py', 'list', '--status', 'reserved'])
assert '无 ID' in reserved
for ident in IDS['NJT']:
    command('bundle-' + ident, ['python3', 'scripts/build_technique_bundle.py', ident])
command('final-api-qa', ['node', 'planning/runs/BATCH-TA0007-016/final-api-qa.mjs'])
before = json.loads((RUN / 'existing-objects-before.json').read_text())
mit_path = next(k for k in before if k.startswith('mitigations/'))
mit = yaml.safe_load((ROOT / mit_path).read_text())
assert mit['measures'] == before[mit_path]['measures']
assert all(a in mit['applications'] for a in before[mit_path]['applications'])
assert len(mit['applications']) == len(before[mit_path]['applications']) + 1
(RUN / 'final-verification.json').write_text(json.dumps(final_results, ensure_ascii=False, indent=2) + '\n')

summary = {
    'schema_version': '1.0.0', 'type': 'batch-integration-summary', 'batch_ref': 'BATCH-TA0007-016', 'status': 'review',
    'delivery_control': {'overall_candidate_count': 34, 'batch_candidate_count': 5,
        'batch_size_rationale': {'zh': '按用户五候选范围分两轮独立研究，全部五份完整交接返回后由主 Agent 统一准入、共享身份和正式写入，逐候选门禁独立保留。',
                                'en': 'The user-requested five candidates were researched independently in two waves; the primary agent converged admission, shared identity and writing only after all five complete handoffs, preserving candidate gates.'},
        'previous_batch_gate_passed': True, 'research_subagent_count': 5, 'research_waves': 2,
        'canonical_integration_after_complete_handoffs': True},
    'candidate_results': candidate_results,
    'shared_library_resolutions': {'reference_proposals': 67, 'new_references': 62,
        'extend': ['REF-000625', 'REF-001049', 'REF-000484', 'REF-000583', 'REF-001041', 'REF-000073', 'REF-001230', 'REF-000025', 'REF-000506', 'MIT-000240 applications'],
        'create_ranges': {k: f'{IDS[k][0]}..{IDS[k][-1]}' for k in ['REF', 'CLM', 'CASE', 'DET', 'NJA', 'MIT']},
        'new_object_counts': {'NJT': 5, 'NJS': 4, 'REF': 62, 'CLM': 38, 'CASE': 7, 'DET': 9, 'NJA': 18, 'MIT': 5, 'REL': 0},
        'unchanged_shared_mitigation_measures_and_prior_applications_verified': True},
    'deferred_hypotheses': ['T1201 handle-chain omission, anonymity, in-process API, self-service substitution and temporal axes were independently reviewed; no native child passes the current evidence gate.',
        'T1120 historical views, filters, arbitrary APIs and cadence are not additional children.',
        'T1069 local/domain/cloud labels, token views, projection and temporal distribution do not create additional children.',
        'Resident process and Registry children need positive query and carrier proof; generic loading, injection and missing events are insufficient.',
        'Registry views, virtualization, remote access and offline copies retain their own evidence limits without extra children.'],
    'duplicate_resolution_refs': [],
    'semantic_validation': {'candidate_level_gates_passed': True, 'conclusion_level_evidence_passed': True,
        'njt_0001_field_responsibility_reviewed': True, 'bilingual_argument_depth_passed': True,
        'boilerplate_review_passed': True, 'taxonomy_breadth_reviewed': True, 'attack_breadth_gap_explained': True,
        'canonical_prose_bulk_generated': False},
    'validation': {'matrix_objects': 4491, 'schema_errors': 0, 'schema_warnings': 0, 'unresolved_duplicate_candidates': 0,
        'reviewed_similarity_resolutions': 12, 'infrastructure_tests': 12, 'web_tests': 140, 'web_api_issues': 0,
        'bilingual_browser_pages': pages, 'browser_errors': 0, 'bundles_built': IDS['NJT'], 'unexplained_reserved_ids': 0,
        'real_host_device_or_cloud_experiment_performed': False},
    'integration_corrections': ['Adapted Registry scope to direct-information ownership.',
        'Declared conditional output and task-carriage sources; preserved native field mappings and nullable identity/error states.',
        'Separated creator/reader/client/provider identities and protocol request/application-result levels.',
        'Removed unbound Case sectors and dates while preserving documented command observations.',
        'Merged repeated publications, pinned the TrustedSec source commit, extended existing locators, and preserved MIT-000240 measures.',
        'Corrected six Chinese confidence phrases without changing medium enums.',
        'Fixed a browser-harness false positive on the documented term undefined buffer contents and waited for instant section scrolling before screenshots.'],
    'TA0007_progress': {'fixed_parents': 34, 'completed_admission_decisions': 23, 'formal_parent_techniques': 22,
        'excluded_parents': 1, 'formal_njs': 10, 'remaining_parents': 11, 'human_domain_review_completed': False},
    'review_notes_zh': '本批完成五项候选，T1201/T1120/T1069/T1057 retain，T1012 adapt；新增五项 NJT、四项原生 NJS、九项 DET、十八项 NJA 和五项 MIT，并扩展 MIT-000240 一个应用。四项子项机理保持中等置信，未虚构现场采用或实测规避。质量、十二项基础设施测试、一百四十项 Web 测试、五个 Bundle 与九十四项实际双语页面检查通过，最终 API 与 ID 状态验证通过；全部保持 review，等待人工领域审查。TA0007 剩余十一项，战术尚未关闭。',
    'review_notes_en': 'Five candidates are complete: retain T1201/T1120/T1069/T1057 and adapt T1012. Five NJT, four native NJS, nine DET, eighteen NJA and five MIT were created, with one MIT-000240 application. Child mechanisms remain medium-confidence without invented field adoption or measured evasion. Quality, twelve infrastructure tests, 140 Web tests, five bundles and 94 actual bilingual page checks pass, with final API and ID verification. Keep all work in review pending human domain approval. Eleven TA0007 parents remain and the tactic is open.'}
(RUN / 'integration-summary.yaml').write_text(yaml.safe_dump(summary, allow_unicode=True, sort_keys=False, width=120))
print(json.dumps({'status': 'review', 'NJT': IDS['NJT'], 'NJS': IDS['NJS'], 'TA0007': summary['TA0007_progress'], 'browser_pages': pages}, ensure_ascii=False), flush=True)
