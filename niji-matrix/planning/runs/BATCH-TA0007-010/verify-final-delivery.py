"""Verify final delivery artifacts and record current, reproducible acceptance facts."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
quality = (RUN / 'final-quality.log').read_text()
assert '校验通过：0 个错误，0 个警告。' in quality
assert '规划校验通过：0 个错误，0 个警告。' in quality
assert '0 组精确重复，0 组待审可能重复，13 组已审查相似项' in quality
assert 'Reader-prose audit passed: 210 parents' in quality
assert re.search(r'Ran 12 tests', quality) and '\nOK\n' in quality
assert 'dist/catalogs/library-catalog.json:' in quality
for name, expected in [('final-content-validation.log', '校验通过：0 个错误，0 个警告。'),
                       ('final-planning-validation.log', '规划校验通过：0 个错误，0 个警告。')]:
    assert expected in (RUN / name).read_text(), name
web = (RUN / 'web-tests.log').read_text()
assert re.search(r'pass\s+140\b', web) and re.search(r'fail\s+0\b', web)
browser = json.loads((RUN / 'web-qa/NJT-0242/report.json').read_text())
assert browser['status'] == 'passed' and len(browser['pages']) == 16
assert browser['api_issues'] == [] and browser['browser_errors'] == []
assert json.loads((RUN / 'final-browser-qa.log').read_text())['status'] == 'passed'
dups = json.loads((RUN / 'duplicate-audit-final.json').read_text())
assert not dups['exact'] and not dups['possible']
registry = yaml.safe_load((ROOT / 'planning/id-reservations.yaml').read_text())
reserved = [x for x in registry['reservations'] if x['status'] == 'reserved']
assert not reserved
plan = yaml.safe_load((ROOT / 'planning/tactics/TA0007.yaml').read_text())
stages = Counter(x['stage'] for x in plan['work_items'])
assert dict(stages) == {'review': 23, 'excluded': 1, 'untriaged': 10}
assert plan['candidate_inventory']['status'] == 'complete' and plan['gap_analysis']['status'] == 'pending'
bundle_path = ROOT / 'dist/techniques/NJT-0242.json'
bundle = json.loads(bundle_path.read_text())
assert bundle['technique']['id'] == 'NJT-0242'
assert bundle['technique']['lifecycle']['status'] == 'review'
assert [x['id'] for x in bundle['subtechniques']] == ['NJS-0242-001']
assert bundle['subtechniques'][0]['parent_ref'] == 'NJT-0242'
for group in ['subtechniques', 'detection_strategies', 'detection_analytics', 'mitigations']:
    assert all(x['lifecycle']['status'] == 'review' for x in bundle[group]), group
for analytic in bundle['detection_analytics']:
    assert all(re.fullmatch(r'[a-z0-9_.-]+', field) for source in analytic['data_requirements'] for field in source['required_fields'])
paths = json.loads((RUN / 'written-object-paths.json').read_text())
hashes = {relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() for relative in paths}
report = {'date': '2026-11-07', 'batch': 'BATCH-TA0007-010', 'status': 'passed',
          'make_quality': 'passed', 'matrix_objects': 4523, 'content_errors': 0, 'content_warnings': 0,
          'planning_errors': 0, 'planning_warnings': 0, 'exact_duplicates': 0, 'unresolved_possible_duplicates': 0,
          'reviewed_similarity_resolutions': len(dups['resolved']), 'infrastructure_tests': 12, 'web_tests': 140,
          'bilingual_browser_pages': len(browser['pages']), 'api_issues': 0, 'browser_errors': 0,
          'reserved_ids': len(reserved), 'bundle': str(bundle_path.relative_to(ROOT)),
          'bundle_sha256': hashlib.sha256(bundle_path.read_bytes()).hexdigest(), 'new_canonical_objects': len(paths),
          'canonical_file_sha256': hashes, 'TA0007_stages': dict(stages),
          'remaining_parent_candidates': [x['source_attack_id'] for x in plan['work_items'] if x['stage'] == 'untriaged'],
          'human_domain_review_completed': False, 'real_host_detector_experiment_performed': False}
(RUN / 'final-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
summary_path = RUN / 'integration-summary.yaml'
summary = yaml.safe_load(summary_path.read_text())
summary['validation']['post_promotion_verification'] = 'passed'
summary['validation']['authoritative_quality_log'] = 'final-quality.log'
summary['validation']['authoritative_browser_log'] = 'final-browser-qa.log'
summary['validation']['bundle_sha256'] = report['bundle_sha256']
summary_path.write_text(yaml.safe_dump(summary, allow_unicode=True, sort_keys=False, width=120))
print(json.dumps({key: value for key, value in report.items() if key != 'canonical_file_sha256'}, ensure_ascii=False))
