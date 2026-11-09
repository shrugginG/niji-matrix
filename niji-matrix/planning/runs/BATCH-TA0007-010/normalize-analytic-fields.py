"""Apply the schema's mechanical field-key normalization and preserve native mapping."""
from pathlib import Path
import hashlib
import json
import yaml

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[2]
mapping = {'Computer': 'computer', 'UtcTime': 'utc_time', 'ProcessGuid': 'process_guid',
           'ParentProcessGuid': 'parent_process_guid', 'Image': 'image', 'CommandLine': 'command_line',
           'User': 'user', 'LogonGuid': 'logon_guid', 'ParentImage': 'parent_image'}
overrides = yaml.safe_load((RUN / 'primary-reviewed-overrides.yaml').read_text())


def normalize(obj):
    for source in obj['data_requirements']:
        source['required_fields'] = [mapping.get(value, value) for value in source['required_fields']]
    obj['correlation']['dimensions'] = [mapping.get(value, value) for value in obj['correlation']['dimensions']]
    if overrides['windows_normalization'] not in obj['logic']['paragraphs']:
        obj['logic']['paragraphs'].append(overrides['windows_normalization'])


path = RUN / 'T1018-reviewed-handoff.yaml'
reviewed = yaml.safe_load(path.read_text())
normalize(reviewed['defense_candidates']['detection_analytics'][0])
path.write_text(yaml.safe_dump(reviewed, allow_unicode=True, sort_keys=False, width=120))
canonical_path = next((ROOT / 'analytics').glob('NJA-000403-*.yaml'))
analytic = yaml.safe_load(canonical_path.read_text())
normalize(analytic)
canonical_path.write_text(yaml.safe_dump(analytic, allow_unicode=True, sort_keys=False, width=120))
(RUN / 'data-field-normalization.json').write_text(json.dumps({'native_to_canonical': mapping,
    'reason': 'Canonical analytic field keys are lowercase; native values and missing states remain unchanged.',
    'changed_object': 'NJA-000403'}, indent=2) + '\n')
manifest = json.loads((RUN / 'review-input-manifest.json').read_text())
manifest['primary_overrides_sha256'] = hashlib.sha256((RUN / 'primary-reviewed-overrides.yaml').read_bytes()).hexdigest()
manifest['reviewed_handoff_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
(RUN / 'review-input-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
quality = RUN / 'quality.log'
if quality.exists() and not (RUN / 'quality-first-pass.log').exists():
    quality.rename(RUN / 'quality-first-pass.log')
print(json.dumps(mapping))
