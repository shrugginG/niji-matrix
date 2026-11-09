"""Read-only structural and identity inspection; no semantic conclusions or IDs."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from collections import defaultdict
import hashlib
import json
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
SCOPE = ['T1201', 'T1120', 'T1069', 'T1057', 'T1012']


def key(value):
    return value.get('key', value.get('temporary_key'))


def normalized_url(value):
    p = urlsplit(value or '')
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), p.query, ''))


def bilingual_issues(value, path=''):
    result = []
    if isinstance(value, dict):
        if 'zh' in value or 'en' in value:
            if set(value) != {'zh', 'en'} or not all(isinstance(value.get(x), str) and value[x].strip() for x in ['zh', 'en']):
                result.append(path)
        for k, v in value.items():
            result.extend(bilingual_issues(v, path + '/' + str(k)))
    elif isinstance(value, list):
        for n, v in enumerate(value):
            result.extend(bilingual_issues(v, path + '/' + str(n)))
    return result


catalog = json.loads((ROOT / 'dist/catalogs/library-catalog.json').read_text())
urls = defaultdict(list)
for ref in catalog['libraries']['reference']:
    urls[normalized_url(ref.get('canonical_url'))].append(ref['id'])
manifest = {'batch_ref': 'BATCH-TA0007-016', 'all_five_handoffs_complete': False, 'inputs': []}
new_refs = []
errors = []
for attack in SCOPE:
    path = RUN / f'{attack}-research-handoff.yaml'
    if not path.exists():
        errors.append(f'Missing {path.name}')
        continue
    raw = path.read_bytes()
    h = yaml.safe_load(raw)
    pair_errors = bilingual_issues(h)
    errors.extend(f'{attack} bilingual map {x}' for x in pair_errors)
    assert h['candidate']['source_attack_id'] == attack
    assert h['batch_ref'] == 'BATCH-TA0007-016'
    record = {'candidate': attack, 'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest(),
              'decision_proposed': h['recommendation']['decision'],
              'children_proposed': len(h.get('proposed_subtechniques', [])),
              'top_level_keys': list(h), 'content_keys': list(h['proposed_content']),
              'library_counts': {k: len(v) for k, v in h['library_candidates'].items()},
              'defense_counts': {k: len(v) for k, v in h['defense_candidates'].items()},
              'bilingual_map_issues': pair_errors}
    manifest['inputs'].append(record)
    for ref in h['library_candidates']['references']:
        new_refs.append({'candidate': attack, 'temporary_key': key(ref), 'url': ref.get('url'),
                         'existing_url_matches': urls[normalized_url(ref.get('url'))]})
manifest['all_five_handoffs_complete'] = len(manifest['inputs']) == 5 and not errors
manifest['structural_errors'] = errors
(RUN / 'research-input-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
(RUN / 'reference-identity-precheck.json').write_text(json.dumps(new_refs, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(manifest, ensure_ascii=False, indent=2))
print('REFERENCE IDENTITIES', json.dumps(new_refs, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
