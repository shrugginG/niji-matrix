"""Serialize reviewed handoffs and identity choices without canonical writes."""
from copy import deepcopy
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
SCOPE = ['T1201', 'T1120', 'T1069', 'T1057', 'T1012']
manifest = json.loads((RUN / 'research-input-manifest.json').read_text())
assert manifest['all_five_handoffs_complete'] and not manifest['structural_errors']
spec = importlib.util.spec_from_file_location('primary_edits', RUN / 'primary-edits.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
aliases = {
    'B016-T1057-REF-ATTACK': 'REF-000625',
    'B016-T1012-REF-ATTACK': 'REF-000625',
    'B016-T1069-REF-IAM-CLOUDTRAIL': 'B016-T1201-REF-IAMLOG',
    'B016-T1069-REF-SAM-RESTRICTION': 'B016-T1201-REF-SAMRESTRICT',
}
reviewed = RUN / 'reviewed-handoffs'
reviewed.mkdir(exist_ok=True)
H = {}
normalizations = []
for attack in SCOPE:
    path = RUN / f'{attack}-research-handoff.yaml'
    record = next(x for x in manifest['inputs'] if x['candidate'] == attack)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
    h = module.apply_primary_edits(attack, yaml.safe_load(path.read_text()))
    for a in h['defense_candidates']['detection_analytics']:
        if a.get('field_mapping'):
            a['tuning_guidance']['paragraphs'].append(deepcopy(a['field_mapping']))
        for d in a['data_requirements']:
            old = d['source_type']
            d['source_type'] = old.replace('_', '-').lower()
            if old != d['source_type']:
                normalizations.append({'object': module.object_key(a), 'field': 'source_type', 'from': old, 'to': d['source_type']})
            for n, field in enumerate(d['required_fields']):
                value = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', field)
                value = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', value).lower()
                if value != field:
                    normalizations.append({'object': module.object_key(a), 'field': 'required_fields', 'from': field, 'to': value})
                d['required_fields'][n] = value
        assert isinstance(a['correlation']['window'], dict)
    def verify(value):
        if isinstance(value, dict):
            if 'zh' in value or 'en' in value:
                assert set(value) == {'zh', 'en'} and all(isinstance(value[k], str) and value[k] for k in ['zh', 'en'])
            if 'paragraphs' in value:
                assert 1 <= len(value['paragraphs']) <= 4
            for item in value.values():
                verify(item)
        elif isinstance(value, list):
            for item in value:
                verify(item)
    verify(h)
    (reviewed / f'{attack}.yaml').write_text(yaml.safe_dump(h, allow_unicode=True, sort_keys=False, width=120))
    H[attack] = h

refs = {}
for attack in SCOPE:
    for proposal in H[attack]['library_candidates']['references']:
        key = module.object_key(proposal)
        if key in aliases:
            if aliases[key].startswith('B016-'):
                refs[aliases[key]]['locator'] += '; ' + (proposal.get('locator') or '')
            continue
        if key in refs:
            assert refs[key]['url'].rstrip('/') == proposal['url'].rstrip('/')
            refs[key]['locator'] += '; ' + (proposal.get('locator') or '')
        else:
            refs[key] = deepcopy(proposal)
for key, ref in refs.items():
    locator = ref.get('locator') or ''
    ref['locator'] = '; '.join(dict.fromkeys(x.strip() for x in locator.split(';') if x.strip()))
assert len(refs) == 62
counts = {'NJT': len(SCOPE), 'NJS': sum(len(h['proposed_subtechniques']) for h in H.values()), 'REF': len(refs)}
for kind, group, field in [('CLM', 'library_candidates', 'claims'), ('CASE', 'library_candidates', 'cases'),
                           ('DET', 'defense_candidates', 'detection_strategies'), ('NJA', 'defense_candidates', 'detection_analytics'),
                           ('MIT', 'defense_candidates', 'mitigations')]:
    counts[kind] = sum(1 for h in H.values() for o in h[group][field] if not o.get('existing_ref'))
(RUN / 'reference-projection.yaml').write_text(yaml.safe_dump(list(refs.values()), allow_unicode=True, sort_keys=False, width=120))
(RUN / 'library-aliases.json').write_text(json.dumps(aliases, indent=2) + '\n')
(RUN / 'allocation-counts.json').write_text(json.dumps(counts, indent=2) + '\n')
(RUN / 'data-field-normalization.json').write_text(json.dumps(normalizations, indent=2) + '\n')
print('REVIEWED COUNTS', json.dumps(counts))
for key, r in refs.items():
    for field in ['notes_zh', 'notes_en', 'locator']:
        if re.search(r'本批|交接|planning/|source key|this batch|handoff', str(r.get(field, '')), re.I):
            print('REVIEW REFERENCE META', key, field, r[field])
plan_path = ROOT / 'planning/tactics/TA0007.yaml'
plan = yaml.safe_load(plan_path.read_text())
for w in plan['work_items']:
    if w['source_attack_id'] in SCOPE:
        w['stage'] = 'decision-ready'
plan_path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=120))
