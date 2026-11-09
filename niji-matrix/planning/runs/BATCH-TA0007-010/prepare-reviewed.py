"""Mechanically apply individually authored primary overrides to the completed handoff."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import yaml

RUN = Path(__file__).resolve().parent


class UniqueLoader(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
source = RUN / 'T1018-research-handoff.yaml'
data = yaml.load(source.read_text(), Loader=UniqueLoader)
overrides = yaml.load((RUN / 'primary-reviewed-overrides.yaml').read_text(), Loader=UniqueLoader)
assert data['recommendation']['decision'] == 'retain'
assert len(data['proposed_subtechniques']) == 1
assert (RUN / 'T1018-evidence-verification.yaml').is_file()
assert (RUN / 'admission-and-convergence.md').is_file()
reviewed = deepcopy(data)
reviewed['proposed_content']['subtechnique_taxonomy']['narrative'] = overrides['parent_taxonomy']['narrative']
reviewed['research']['limitations'] = overrides['parent_limitations']
reviewed['library_candidates']['references'].extend(overrides['additional_references'])
reviewed['library_candidates']['claims'].extend(overrides['additional_claims'])
windows, linux = reviewed['defense_candidates']['detection_analytics']
windows['logic'] = overrides['windows_logic']
windows['data_requirements'][0]['required_fields'].append('ParentImage')
windows['evidence_keys'].append('REF-001250')
linux['logic'] = overrides['linux_logic']
linux['data_requirements'][0]['required_fields'].remove('node')
linux['data_requirements'].append(overrides['linux_collector_source'])
health = next(x for x in linux['data_requirements'] if x['source_type'] == 'linux-audit-collection-health')
health['required_fields'].remove('collector_node_name')
health['required_fields'].extend(['collector_host_id', 'boot_id'])
linux['correlation']['dimensions'] = ['collector_host_id', 'boot_id', 'auid', 'uid', 'ses', 'pid', 'ppid', 'audit_timestamp', 'audit_serial', 'name']
linux['evidence_keys'].extend(['B010-T1018-REF-OPEN', 'B010-T1018-REF-OPENAT2'])
for ref in ['REF-001250', 'REF-001198', 'REF-000379', 'REF-001079']:
    if ref not in reviewed['existing_library_reuse']['reference_refs']:
        reviewed['existing_library_reuse']['reference_refs'].append(ref)
for child in reviewed['proposed_subtechniques']:
    for ref in ['REF-000379', 'REF-001079']:
        if ref not in child['evidence']['reference_keys']:
            child['evidence']['reference_keys'].append(ref)
keys = set()
for category in ['references', 'claims', 'cases']:
    for item in reviewed['library_candidates'][category]:
        assert item['temporary_key'] not in keys
        keys.add(item['temporary_key'])
for category in ['detection_strategies', 'detection_analytics', 'mitigations']:
    for item in reviewed['defense_candidates'][category]:
        assert item['temporary_key'] not in keys
        keys.add(item['temporary_key'])
keys.update(['B010-T1018-PARENT', 'B010-T1018-CHILD-LOCAL-KNOWLEDGE'])


def check(value):
    if isinstance(value, str) and value.startswith('B010-T1018-'):
        # Prefix declarations and an extended existing source key are metadata.
        if value not in {'B010-T1018-', 'B010-T1018-REF-SSHCONFIG'}:
            assert value in keys, value
    elif isinstance(value, list):
        for item in value:
            check(item)
    elif isinstance(value, dict):
        for item in value.values():
            check(item)


check(reviewed)
(RUN / 'T1018-reviewed-handoff.yaml').write_text(yaml.safe_dump(reviewed, allow_unicode=True, sort_keys=False, width=120))
counts = {'NJT': 1, 'NJS': 1, 'REF': len(reviewed['library_candidates']['references']),
          'CLM': len(reviewed['library_candidates']['claims']), 'CASE': len(reviewed['library_candidates']['cases']),
          'DET': len(reviewed['defense_candidates']['detection_strategies']),
          'NJA': len(reviewed['defense_candidates']['detection_analytics']),
          'MIT': len(reviewed['defense_candidates']['mitigations'])}
(RUN / 'allocation-counts.json').write_text(json.dumps(counts, indent=2) + '\n')
(RUN / 'review-input-manifest.json').write_text(json.dumps({
    'complete_research_handoff_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'primary_overrides_sha256': hashlib.sha256((RUN / 'primary-reviewed-overrides.yaml').read_bytes()).hexdigest(),
    'reviewed_handoff_sha256': hashlib.sha256((RUN / 'T1018-reviewed-handoff.yaml').read_bytes()).hexdigest(),
    'canonical_writing_after_complete_handoff': True,
    'allocation_counts': counts,
}, indent=2) + '\n')
(RUN / 'taxonomy-breadth-review.yaml').write_text(yaml.safe_dump(reviewed['research']['taxonomy_breadth_review'], allow_unicode=True, sort_keys=False, width=120))
print(json.dumps(counts))
