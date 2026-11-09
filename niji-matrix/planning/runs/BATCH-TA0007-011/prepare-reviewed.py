"""Mechanical application of individually authored primary review and supplements."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import yaml

RUN = Path(__file__).resolve().parent
CANDIDATES = ['T1518', 'T1082', 'T1614', 'T1016', 'T1049']

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for kn, vn in node.value:
        key = loader.construct_object(kn, deep=deep)
        if key in result:
            raise ValueError(f'duplicate key: {key}')
        result[key] = loader.construct_object(vn, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def read(name):
    return yaml.load((RUN / name).read_text(), Loader=UniqueLoader)

def strict_bilingual(value, pointer=''):
    if isinstance(value, dict):
        if 'zh' in value or 'en' in value:
            assert set(value) == {'zh', 'en'}, (pointer, list(value))
            assert all(isinstance(value[k], str) and value[k].strip() for k in value), pointer
        for k, v in value.items():
            strict_bilingual(v, pointer + '/' + str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            strict_bilingual(v, pointer + '/' + str(i))

def apply_overrides(data, filename):
    path = RUN / filename
    if not path.exists():
        return
    edits = read(filename)
    for change in edits.get('bilingual_repairs', []) + edits.get('content_edits', []):
        parts = change['pointer'].strip('/').split('/')
        node = data
        for part in parts[:-1]:
            node = node[int(part)] if isinstance(node, list) else node[part]
        last = int(parts[-1]) if isinstance(node, list) else parts[-1]
        if change.get('append'):
            assert last == len(node), change['pointer']
            node.append(change['value'])
        else:
            assert last in node if isinstance(node, dict) else last < len(node)
            node[last] = change['value']

def key(item):
    return item.get('temporary_key', item.get('key'))

def append_unique(target, values):
    for value in values:
        if value not in target:
            target.append(value)

def apply_software_supplement(data):
    supplement = read('T1518-supplement-handoff.yaml')
    rev = supplement['parent_revisions']
    pc = data['proposed_content']
    for field in ['summary', 'stealth_characteristics', 'subtechnique_taxonomy']:
        pc[field] = rev[field]
    pc['scope_boundary_definition']['paragraphs'].append(rev['scope_boundary_append'])
    model = pc['application_scenarios_and_threat_model']
    model['application_scenarios']['paragraphs'].append(rev['application_scenarios_append'])
    model['threat_model']['attacker_model']['paragraphs'].append(rev['attacker_model_append'])
    pc['stealth_mechanisms'].insert(0, rev['add_stealth_mechanism'])
    for change in rev['existing_mechanism_role_changes']:
        next(m for m in pc['stealth_mechanisms'] if m['mechanism_ref'] == change['mechanism_ref'])['role'] = change['role']
    for kind, values in rev['append_evidence'].items():
        append_unique(pc['evidence'].setdefault(kind, []), values)
    data['research']['limitations'] = rev['research_limitations']
    data['proposed_subtechniques'] = supplement['proposed_subtechniques']
    data['library_candidates']['claims'].extend(supplement['library_candidates']['claims'])
    for category, extensions in supplement['defense_extensions'].items():
        for ext in extensions:
            obj = next(x for x in data['defense_candidates'][category] if key(x) == ext['existing_key'])
            for src, dst in [('add_detects_keys', 'detects_keys'), ('add_evidence_keys', 'evidence_keys')]:
                append_unique(obj.setdefault(dst, []), ext.get(src, []))
            for src, dst in [('description_append', 'description'), ('tuning_guidance_append', 'tuning_guidance')]:
                if src in ext:
                    obj[dst]['paragraphs'].append(ext[src])
            if 'logic_paragraph_4_replacement' in ext:
                obj['logic']['paragraphs'][3] = ext['logic_paragraph_4_replacement']
            obj.setdefault('applications', []).extend(ext.get('applications', []))
    for ext in supplement['shared_library_convergence']['claim_extensions']:
        obj = next(x for x in data['library_candidates']['claims'] if key(x) == ext['existing_key'])
        append_unique(obj['subject_keys'], ext['add_subject_keys'])
    data['research']['supplement_review'] = supplement['research_updates']
    data['research']['taxonomy_breadth_review']['supplement'] = supplement['research_updates']['breadth_review']
    breadth = data['research']['taxonomy_breadth_review']
    breadth['proposed_niji_child_count'] = 1
    for axis in breadth['candidate_stealth_axes_examined']:
        if axis['axis'] == 'resident-inline-carriage':
            axis.update(supplement['research_updates']['taxonomy_axis_resolution'])
        elif axis['axis'] in supplement['research_updates']['remaining_axes']:
            axis['supplement_resolution'] = supplement['research_updates']['remaining_axes'][axis['axis']]
    breadth['reviewer_notes'] = {
        'zh': '原始软件类别及其他候选轴的边界检查继续有效。补审以独立软件请求、客户端承载和工具创建观察差完成第二轮证据核验，原先暂缓的承载轴现建立一项子技术；其余证据不足的轴不升级，产品类别不复制为子项。',
        'en': 'The original product-category and other-axis boundary reviews remain applicable. Supplemental review independently verifies a software request, client carriage, and the utility-creation observation contrast, establishing one child on the previously deferred carrier axis. Other insufficiently evidenced axes remain unpromoted, and product categories are not copied as children.'}
    data['research']['rejected_mechanisms'] = [x for x in data['research']['rejected_mechanisms']
        if not (isinstance(x, dict) and x.get('mechanism_ref') == 'NM-BT')]

def main():
    inputs = {}
    for candidate in CANDIDATES:
        source = RUN / f'{candidate}-research-handoff.yaml'
        assert (RUN / f'{candidate}-evidence-verification.yaml').is_file(), candidate
        data = read(source.name)
        apply_overrides(data, f'{candidate}-primary-overrides.yaml')
        if candidate == 'T1518':
            apply_software_supplement(data)
        strict_bilingual(data)
        assert data['recommendation']['decision'] in {'retain', 'adapt'}
        assert data['recommendation']['original_attack_subtechniques_imported'] is False
        destination = RUN / f'{candidate}-reviewed-handoff.yaml'
        destination.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120))
        inputs[candidate] = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'reviewed_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
            'children': [key(x) for x in data['proposed_subtechniques']]}
    (RUN / 'review-input-manifest.json').write_text(json.dumps(inputs, indent=2) + '\n')
    print(json.dumps(inputs, indent=2))

if __name__ == '__main__':
    main()
