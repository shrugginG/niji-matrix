"""Mechanically apply primary-authored pointer overrides to frozen research."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import yaml

RUN=Path(__file__).resolve().parent
CANDIDATES=['T1033','T1007','T1124','T1673','T1497']

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader,node,deep=False):
    result={}
    for kn,vn in node.value:
        k=loader.construct_object(kn,deep=deep)
        if k in result:raise ValueError(f'Duplicate YAML key: {k}')
        result[k]=loader.construct_object(vn,deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)

def read(name):
    return yaml.load((RUN/name).read_text(),Loader=UniqueLoader)

def key(item):
    return item.get('temporary_key',item.get('key'))

def append_unique(items,values):
    for value in values:
        if value not in items:items.append(value)

def strict_bilingual(value,pointer=''):
    if isinstance(value,dict):
        if 'zh' in value or 'en' in value:
            assert set(value)=={'zh','en'},(pointer,list(value))
            assert all(isinstance(v,str) and v.strip() for v in value.values()),pointer
        for k,v in value.items():strict_bilingual(v,pointer+'/'+str(k))
    elif isinstance(value,list):
        for i,v in enumerate(value):strict_bilingual(v,pointer+'/'+str(i))

def apply_overrides(data,filename):
    path=RUN/filename
    if not path.is_file():return
    d=read(filename)
    for change in d.get('bilingual_repairs',[])+d.get('content_edits',[]):
        parts=change['pointer'].strip('/').split('/');node=data
        for part in parts[:-1]:node=node[int(part)] if isinstance(node,list) else node[part]
        last=int(parts[-1]) if isinstance(node,list) else parts[-1]
        if change.get('append'):
            assert last==len(node);node.append(deepcopy(change['value']))
        else:
            assert last in node if isinstance(node,dict) else last<len(node)
            node[last]=deepcopy(change['value'])

def main():
    assert (RUN/'admission-and-convergence.md').is_file(), 'Primary admission must precede reviewed projection'
    manifest={}
    for candidate in CANDIDATES:
        source=RUN/f'{candidate}-research-handoff.yaml'
        evidence=RUN/f'{candidate}-evidence-verification.yaml'
        assert source.is_file() and evidence.is_file(),candidate
        data=read(source.name)
        assert data['recommendation']['decision'] in {'retain','adapt','exclude'}
        apply_overrides(data,f'{candidate}-primary-overrides.yaml')
        strict_bilingual(data)
        destination=RUN/f'{candidate}-reviewed-handoff.yaml'
        destination.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=120))
        manifest[candidate]={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'evidence_sha256':hashlib.sha256(evidence.read_bytes()).hexdigest(),
            'reviewed_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),
            'decision':data['recommendation']['decision'],
            'existing_technique_ref':data.get('existing_technique_ref'),
            'proposed_children':[key(x) or x.get('id') for x in data.get('proposed_subtechniques',[])]}
    (RUN/'review-input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
