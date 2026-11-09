"""Promote only the accepted candidate after checking actual gate artifacts."""
from collections import Counter
from pathlib import Path
import json
import re
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
quality = (RUN / 'quality.log').read_text()
web = (RUN / 'web-tests.log').read_text()
browser = json.loads((RUN / 'web-qa/NJT-0242/report.json').read_text())
duplicates = json.loads((RUN / 'duplicate-audit-final.json').read_text())
assert '校验通过：0 个错误，0 个警告。' in quality
assert '规划校验通过：0 个错误，0 个警告。' in quality
assert 'Reader-prose audit passed: 210 parents' in quality
assert 'Ran 12 tests' in quality and '\nOK\n' in quality
assert 'dist/catalogs/library-catalog.json:' in quality
assert not duplicates['exact'] and not duplicates['possible']
assert re.search(r'pass\s+140\b', web) and re.search(r'fail\s+0\b', web)
assert browser['status'] == 'passed' and len(browser['pages']) == 16
assert browser['api_issues'] == [] and browser['browser_errors'] == []
assert (ROOT / 'dist/techniques/NJT-0242.json').is_file()
registry = yaml.safe_load((ROOT / 'planning/id-reservations.yaml').read_text())
assert not [r for r in registry['reservations'] if r['status'] == 'reserved']
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
        obj['review']['review_notes_zh'] = '独立研究、准入、原生分类、双语字段深度、共享库去重、ID 同步、质量、Bundle 和实际双语 Web 门禁通过；保持 review 等待人工领域审查。'
        obj['review']['review_notes_en'] = 'Independent research, admission, native taxonomy, bilingual field depth, shared identity, ID sync, quality, bundle and actual bilingual Web gates pass; keep review pending human domain approval.'
    else:
        continue
    path.write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=120))

plan_path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(plan_path.read_text())
next(b for b in plan['batches'] if b['id'] == 'BATCH-TA0007-010')['status'] = 'review'
work = next(w for w in plan['work_items'] if w['source_attack_id'] == 'T1018')
work['stage'] = 'review'
work['notes_zh'] = '固定清单第 24 项；Enterprise 19.1 无 ATT&CK 子项。单候选 retain 建立 NJT-0242 与 NJS-0242-001 本地既存主机知识复用；十个原生轴经独立研究和主审，NM-BT 保持中等置信。两项阶段限定案例、Windows 命令与 Linux 文件访问分析及目标化缓解完成质量、Bundle 和双语 Web 验收，保持 review 等待人工领域审查。'
work['notes_en'] = 'Fixed inventory position 24; Enterprise 19.1 has no ATT&CK children. The single-candidate retain decision establishes NJT-0242 and NJS-0242-001 Local Host-Knowledge Reuse. Ten native axes received independent research and primary review; NM-BT remains medium-confidence. Two stage-limited cases, Windows-command and Linux-file-access analytics and targeted mitigation pass quality, bundle and bilingual Web acceptance; keep review pending human domain approval.'
plan['candidate_inventory']['last_synced'] = '2026-11-07'
plan['gap_analysis']['status'] = 'pending'
plan['gap_analysis']['notes_zh'] = '固定 Enterprise 19.1 TA0007 共 34 个父候选，已完成 24 项准入：23 项正式技术、T1538 排除、11 项正式 NJS。本批单独完成 T1018，新增 NJT 1、NJS 1；主机记录、当前可达性与后继访问明确分开，匿迹机理保持中等置信，未宣称实测规避。剩余 10 个父候选待准入，13 项既有父技术的子分类仍 deferred；原生缺口、最终战术收敛及人工领域审查尚未完成。'
plan['gap_analysis']['notes_en'] = 'Fixed Enterprise 19.1 TA0007 has 34 parent candidates and 24 completed admission decisions: 23 formal techniques, excluded T1538, and 11 formal NJS. This delivery completes only T1018, adding one NJT and one NJS. Stored host records, current reachability and later access remain distinct; stealth mechanisms retain medium confidence without measured-evasion claims. Ten parents still await admission, thirteen existing parent taxonomies remain deferred, and native gaps, tactic-wide convergence and human domain review remain open.'
plan_path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))
stages = Counter(w['stage'] for w in plan['work_items'])
assert stages == {'review': 23, 'excluded': 1, 'untriaged': 10}, stages
summary_path = RUN / 'integration-summary.yaml'
summary = yaml.safe_load(summary_path.read_text())
summary['status'] = 'review'
summary['validation'] = {'matrix_objects': 4523, 'schema_errors': 0, 'schema_warnings': 0,
                         'planning_errors': 0, 'planning_warnings': 0,
                         'unresolved_duplicate_candidates': 0,
                         'reviewed_similarity_resolutions': len(duplicates['resolved']),
                         'infrastructure_tests': 12, 'web_tests': 140, 'web_api_issues': 0,
                         'bilingual_browser_pages': 16, 'browser_errors': 0,
                         'bundles_built': ['NJT-0242'], 'unexplained_reserved_ids': 0,
                         'real_host_device_or_cloud_experiment_performed': False,
                         'post_promotion_verification': 'pending'}
summary_path.write_text(yaml.safe_dump(summary, allow_unicode=True, sort_keys=False, width=120))
print(json.dumps({'batch': summary['batch_ref'], 'status': 'review', 'stages': dict(stages),
                  'TA0007': summary['TA0007_progress']}, ensure_ascii=False))
