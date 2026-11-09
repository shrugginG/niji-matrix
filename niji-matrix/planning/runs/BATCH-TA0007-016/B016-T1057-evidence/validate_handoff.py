from pathlib import Path
import json
import re
import yaml
from jsonschema import Draft202012Validator

ROOT = Path('/home/shrugging/project/theory_research/niji-matrix')
RUN = ROOT / 'planning/runs/BATCH-TA0007-016'
path = RUN / 'T1057-research-handoff.yaml'
handoff = yaml.safe_load(path.read_text())
errors = []
bilingual_count = 0

def walk(value, location='$'):
    global bilingual_count
    if isinstance(value, dict):
        if 'zh' in value or 'en' in value:
            bilingual_count += 1
            if set(value) != {'zh', 'en'}:
                errors.append({'path': location, 'error': 'Bilingual maps must contain exactly zh/en'})
            if not all(isinstance(value.get(k), str) and value[k].strip() for k in ['zh', 'en']):
                errors.append({'path': location, 'error': 'Missing bilingual text'})
        if 'paragraphs' in value and not 1 <= len(value['paragraphs']) <= 4:
            errors.append({'path': location, 'error': 'Paragraph count outside 1-4'})
        if 'source_type' in value and not re.fullmatch('[a-z]+(?:-[a-z]+)*', value['source_type']):
            errors.append({'path': location, 'error': 'Noncanonical source type'})
        for key in ['required_fields', 'dimensions']:
            for field in value.get(key, []):
                if not re.fullmatch('[a-z][a-z0-9_]*', field):
                    errors.append({'path': location + '.' + key, 'error': field})
        if 'mechanism_ref' in value and 'summary' in value:
            for lang, text in value['summary'].items():
                if text.rstrip().endswith(('.', '。', '!', '！', '?', '？', ';', '；', ':', '：')):
                    errors.append({'path': location + '.summary.' + lang, 'error': 'Sentence-ending punctuation'})
        for key, item in value.items():
            walk(item, location + '.' + key)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            walk(item, location + '[' + str(i) + ']')

walk(handoff)
known = {}
for folder in ['references', 'claims', 'cases', 'detections', 'analytics', 'mitigations', 'relationships']:
    for candidate in (ROOT / folder).glob('*.yaml'):
        obj = yaml.safe_load(candidate.read_text())
        known[obj['id']] = obj

mapping = {
    handoff['proposed_content']['temporary_key']: 'NJT-9998',
    handoff['proposed_subtechniques'][0]['temporary_key']: 'NJS-9998-001',
}
sections = [
    ('references', 'REF', 'reference', '1.0.0'),
    ('claims', 'CLM', 'claim', '1.0.0'),
    ('cases', 'CASE', 'case', '1.0.0'),
    ('detection_strategies', 'DET', 'detection', '2.0.0'),
    ('detection_analytics', 'NJA', 'analytic', '2.0.0'),
    ('mitigations', 'MIT', 'mitigation', '2.0.0'),
]
for field, prefix, _, _ in sections:
    objects = handoff['library_candidates'].get(field, []) or handoff['defense_candidates'].get(field, [])
    for i, obj in enumerate(objects):
        mapping[obj['temporary_key']] = f'{prefix}-{990000+i:06d}'

referenced = set(re.findall(r'\b(?:B016-T1057-[A-Z0-9-]+|REF-\d{6})\b', path.read_text()))
missing = sorted(referenced - set(known) - set(mapping) - {'B016-T1057'})
for key in missing:
    errors.append({'path': '$', 'error': 'Unresolved identity: ' + key})

def normalize_url(url):
    return (url or '').split('?')[0].rstrip('/').lower()

reference_duplicates = []
for obj in handoff['library_candidates']['references']:
    matches = [key for key, old in known.items() if key.startswith('REF-') and normalize_url(old.get('url')) == normalize_url(obj['url'])]
    if matches:
        reference_duplicates.append({'key': obj['temporary_key'], 'existing': matches})
        errors.append({'path': obj['temporary_key'], 'error': 'Duplicate canonical reference URL'})

renames = {
    'strategy_key': 'strategy_ref', 'parent_key': 'parent_ref', 'target_key': 'target_ref',
    'analytic_keys': 'analytic_refs', 'detects_keys': 'detects_refs', 'strategy_keys': 'strategy_refs',
    'mitigation_keys': 'mitigation_refs', 'subtechnique_keys': 'subtechnique_refs', 'subject_keys': 'subject_refs',
    'evidence_keys': 'evidence_refs', 'claim_keys': 'claim_refs', 'case_keys': 'case_refs', 'reference_keys': 'reference_refs',
}

def project(value):
    if isinstance(value, str):
        return mapping.get(value, value)
    if isinstance(value, list):
        return [project(item) for item in value]
    if isinstance(value, dict):
        return {renames.get(key, key): project(item) for key, item in value.items() if key != 'temporary_key'}
    return value

lifecycle = {'status': 'draft', 'version': '0.1.0', 'created': '2026-11-06', 'modified': '2026-11-06', 'contributors': ['Niji Matrix Research'], 'reviewers': []}
checks = []
for field, prefix, schema, version in sections:
    objects = handoff['library_candidates'].get(field, []) or handoff['defense_candidates'].get(field, [])
    for original in objects:
        obj = project(original)
        obj.update(schema_version=version, id=mapping[original['temporary_key']], type={'detection': 'detection-strategy', 'analytic': 'detection-analytic'}.get(schema, schema))
        if version == '2.0.0':
            obj['lifecycle'] = lifecycle
        checks.append((original['temporary_key'], schema, obj))
for original, schema in [(handoff['proposed_content'], 'technique'), (handoff['proposed_subtechniques'][0], 'subtechnique')]:
    obj = project(original)
    obj.update(schema_version='2.0.0', type='evasion-subtechnique' if schema == 'subtechnique' else schema, id=mapping[original['temporary_key']], lifecycle=lifecycle)
    if schema == 'technique':
        obj['classification'] = {'tactic_refs': ['TA0007'], 'origin': {'kind': 'attack-retained', 'source_attack_id': 'T1057', 'source_attack_version': '19.1'}, 'decision_ref': 'DEC-TA0007-T1057'}
    checks.append((original['temporary_key'], schema, obj))

schema_errors = []
for key, schema, obj in checks:
    validator = Draft202012Validator(json.loads((ROOT / 'schemas' / f'{schema}.schema.json').read_text()))
    for error in validator.iter_errors(obj):
        schema_errors.append({'key': key, 'path': '.'.join(map(str, error.absolute_path)), 'error': error.message})

strategies = {obj['temporary_key']: obj for obj in handoff['defense_candidates']['detection_strategies']}
for analytic in handoff['defense_candidates']['detection_analytics']:
    strategy = strategies[analytic['strategy_key']]
    if analytic['temporary_key'] not in strategy['analytic_keys']:
        errors.append({'path': analytic['temporary_key'], 'error': 'Nonreciprocal strategy link'})
    unsupported = set(analytic['evidence_keys']) - set(strategy['evidence_keys'])
    if unsupported:
        errors.append({'path': strategy['temporary_key'], 'error': 'Missing analytic evidence', 'missing': sorted(unsupported)})

report = {
    'yaml_parse': True,
    'bilingual_pairs': bilingual_count,
    'temporary_objects': len(mapping),
    'missing_references': missing,
    'canonical_reference_duplicates': reference_duplicates,
    'content_contract_errors': errors,
    'canonical_shape_projection_checked': len(checks),
    'schema_errors': schema_errors,
    'projection_notice': 'Temporary identities projected only in memory. Classification and draft lifecycle supplied mechanically. No canonical IDs reserved and no canonical files written.',
}
(RUN / 'B016-T1057-evidence/validation-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors or schema_errors else 0)
