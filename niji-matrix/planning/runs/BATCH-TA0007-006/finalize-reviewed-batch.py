"""Promote the accepted single-candidate delivery and record actual gate results."""
from pathlib import Path
import json
import re
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
quality = (RUN / 'quality.log').read_text()
web = (RUN / 'web-tests-final.log').read_text()
browser = json.loads((RUN / 'web-qa/report.json').read_text())
assert '校验通过：0 个错误，0 个警告。' in quality
assert '规划校验通过：0 个错误，0 个警告。' in quality
assert '0 组精确重复，0 组待审可能重复' in quality
assert 'Ran 12 tests' in quality and '\nOK\n' in quality
assert 'dist/catalogs/library-catalog.json:' in quality
assert re.search(r'pass\s+140\b', web) and re.search(r'fail\s+0\b', web)
assert browser['status'] == 'passed' and len(browser['pages']) == 14
assert browser['api_issues'] == [] and browser['browser_errors'] == []

paths = json.loads((RUN / 'written-object-paths.json').read_text())
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
        obj['review']['review_notes_zh'] = '候选证据、原生分类、双语字段深度、共享库去重、ID 同步、质量、Bundle 和实际双语 Web 门禁均通过；保持 review 等待人工领域审查。'
        obj['review']['review_notes_en'] = 'Candidate evidence, native taxonomy, bilingual field depth, shared-library identity, ID sync, quality, bundle, and actual bilingual Web gates pass; retain review pending human domain approval.'
    else:
        continue
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))

path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(path.read_text())
next(b for b in plan['batches'] if b['id'] == 'BATCH-TA0007-006')['status'] = 'review'
work = next(w for w in plan['work_items'] if w['source_attack_id'] == 'T1615')
work['stage'] = 'review'
work['notes_zh'] = '固定清单第 13 项；ATT&CK 19.1 无子项，仅作广度背景。单候选试点 retain 为 NJT-0231；六个原生轴已审查，证据不足的独立子项保持 deferred，新增 NJS 0。三项分读取面分析和目标化缓解、质量与双语 Web 验收通过，等待人工领域审查。'
work['notes_en'] = 'Fixed inventory position 13; ATT&CK 19.1 has no children and supplies breadth context only. The single-candidate pilot retained NJT-0231. Six native axes were reviewed; evidence-limited independent children remain deferred, with zero NJS added. Three read-plane analytics, target-specific mitigation, quality and bilingual Web acceptance pass pending human domain review.'
plan['candidate_inventory']['last_synced'] = '2026-11-05'
plan['gap_analysis']['notes_zh'] = '固定 Enterprise 19.1 TA0007 的 34 个父候选已完整登记。完成 13 项准入决策，正式技术 12 项，其中 T1622 跨战术复用 NJT-0106；T1538 已 exclude。正式 NJS 共 4 项，T1615 单候选试点新增 NJT 1、NJS 0。另有 21 个父候选待准入；Niji 原生缺口与战术级收敛仍待后续，人工领域审查尚未完成。'
plan['gap_analysis']['notes_en'] = 'All 34 fixed Enterprise 19.1 TA0007 parent candidates are registered. Thirteen admission decisions yield twelve formal techniques, including cross-tactic reuse of NJT-0106 for T1622; T1538 is excluded. Four formal NJS exist, with the T1615 single-candidate pilot adding one NJT and zero NJS. Twenty-one parents still await admission; Niji-native gap assessment and tactic-wide convergence remain open, and human domain review is pending.'
path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))

summary = {
    'schema_version': '1.0.0', 'type': 'batch-integration-summary',
    'batch_ref': 'BATCH-TA0007-006', 'status': 'review',
    'delivery_control': {
        'overall_candidate_count': 34, 'batch_candidate_count': 1,
        'batch_size_rationale': {
            'zh': '用户明确要求先开发一个候选测试效果；仅处理 T1615，T1680 与 T1654 保留在计划批次 015。用户随后明确确认目标为 TA0007 环境测绘。',
            'en': 'The user explicitly requested a one-candidate pilot. Only T1615 was delivered; T1680 and T1654 remain in planned batch 015. The user subsequently confirmed TA0007 Discovery as the intended scope.'},
        'previous_batch_gate_passed': True,
        'research_subagent_count': 1,
        'canonical_integration_after_complete_handoff': True},
    'candidate_results': [{'source_attack_id': 'T1615', 'decision': 'retain',
                           'technique_ref': 'NJT-0231', 'subtechnique_refs': []}],
    'shared_library_resolutions': {
        'reuse': ['REF-000341', 'REF-000366', 'REF-000463', 'REF-000377', 'REF-000474', 'REF-000379'],
        'extend': ['REF-001049', 'REF-000625'],
        'create_ranges': {'references': 'REF-001211..REF-001216', 'claims': 'CLM-001173..CLM-001177',
                          'cases': 'CASE-000356', 'detection_strategies': 'DET-000273',
                          'detection_analytics': 'NJA-000367..NJA-000369',
                          'mitigations': 'MIT-000240', 'relationships': None}},
    'deferred_hypotheses': [
        'Local-result or cache substitution lacks deliberate-selection and same-operation trace evidence.',
        'Scoped reads, timing/client borrowing and report-artifact avoidance lack independent child evidence.',
        'No measured miss rate, complete command output or Windows-domain deployment result is claimed.'],
    'duplicate_resolution_refs': [],
    'semantic_validation': {
        'candidate_level_gates_passed': True, 'conclusion_level_evidence_passed': True,
        'njt_0001_field_responsibility_reviewed': True, 'bilingual_argument_depth_passed': True,
        'boilerplate_review_passed': True, 'taxonomy_breadth_reviewed': True,
        'attack_breadth_gap_explained': True, 'canonical_prose_bulk_generated': False},
    'validation': {
        'matrix_objects': 4221, 'schema_errors': 0, 'schema_warnings': 0,
        'unresolved_duplicate_candidates': 0, 'reviewed_similarity_resolutions': 12,
        'infrastructure_tests': 12, 'web_tests': 140, 'web_api_issues': 0,
        'bilingual_browser_pages': 14, 'browser_errors': 0,
        'bundles_built': ['NJT-0231'], 'unexplained_reserved_ids': 0,
        'real_windows_domain_experiment_performed': False},
    'review_notes_zh': 'T1615 retain 建立 NJT-0231，采用一项 medium NM-FD；六个原生轴证据审查后分类 deferred，新增 NJS 0。新增一项 DET、三项区分端点请求、GPC 属性读取与 SYSVOL 访问等级的 NJA，以及保留必要客户端读取权的 MIT；五项 CLM、独立 ComRAT 命令案例与六项 Microsoft 来源完整连接。初始序列化与引用导航断言问题已纠正，最终质量和双语 Web 门禁均通过。保持 review 等待人工领域审查，检测设计仍需真实环境验证。TA0007 现有 12 项正式技术、4 项 NJS、1 项 exclude、21 项父候选待准入，战术未关闭。',
    'review_notes_en': 'T1615 was retained as NJT-0231 with one medium-confidence NM-FD mechanism. Six native axes were reviewed and taxonomy remains deferred with zero new NJS. One DET, three NJAs separating endpoint requests, GPC property reads and SYSVOL access grades, and one MIT preserving required client reads are connected to five Claims, a distinct ComRAT command case and six Microsoft sources. Initial serialization and reference-navigation assertion issues were corrected; final quality and bilingual Web gates pass. Keep review pending human domain approval; detection design still needs deployment validation. TA0007 has twelve formal techniques, four NJS, one exclusion and twenty-one parents awaiting admission, so the tactic remains open.'}
(RUN / 'integration-summary.yaml').write_text(yaml.safe_dump(summary, allow_unicode=True, sort_keys=False, width=120))
print(json.dumps({'batch': 'BATCH-TA0007-006', 'status': 'review',
                  'TA0007': {'candidate_decisions': 13, 'techniques': 12, 'njs': 4,
                              'excluded': 1, 'remaining_candidates': 21}}, ensure_ascii=False))
