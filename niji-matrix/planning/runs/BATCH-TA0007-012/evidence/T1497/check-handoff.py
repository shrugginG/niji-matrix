"""Strict staging validation without allocating or writing canonical identities."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import re
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path('/home/shrugging/project/theory_research/niji-matrix')
RUN=ROOT/'planning/runs/BATCH-TA0007-012'
OUT=RUN/'evidence/T1497'
errors=[]
class UniqueLoader(yaml.SafeLoader): pass
def unique_mapping(loader,node,deep=False):
    result={}
    for keynode,valnode in node.value:
        key=loader.construct_object(keynode,deep=deep)
        if key in result: raise ValueError('Duplicate YAML key: '+str(key))
        result[key]=loader.construct_object(valnode,deep=deep)
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)
docs={}
for n in ['T1497-research-handoff.yaml','T1497-evidence-verification.yaml']:
    docs[n]=yaml.load((RUN/n).read_text(),Loader=UniqueLoader)
h=docs['T1497-research-handoff.yaml']; v=docs['T1497-evidence-verification.yaml']
counts={'bilingual_dictionaries':0,'paragraph_sections':0,'native_machine_fields':0,'source_refs_checked':0,'schema_objects':0}
def walk(value,path=''):
    if isinstance(value,dict):
        if 'zh' in value or 'en' in value:
            counts['bilingual_dictionaries']+=1
            if set(value)!={'zh','en'} or not all(isinstance(value[x],str) and value[x].strip() for x in ['zh','en']): errors.append('Bilingual contract: '+path)
            if 'en' in value and isinstance(value['en'],str):
                if re.search(r'\b(?:with|to|under|about)(?:0x|[0-9])',value['en'],re.I): errors.append('English spacing: '+path)
                if re.search(r'\b(?:to|under|belongs to)\s*00[123]\b',value['en']): errors.append('Abbreviated child identity: '+path)
        if 'paragraphs' in value:
            counts['paragraph_sections']+=1
            p=value['paragraphs']
            if not isinstance(p,list) or not 1<=len(p)<=4: errors.append('Paragraph count: '+path)
        if 'required_fields' in value:
            for f in value['required_fields']:
                counts['native_machine_fields']+=1
                if f!=f.lower() or not re.fullmatch(r'[a-z0-9_.-]+',f): errors.append('Machine field: '+path+':'+f)
        if 'dimensions' in value and isinstance(value['dimensions'],list):
            for f in value['dimensions']:
                if isinstance(f,str) and (f!=f.lower() or not re.fullmatch(r'[a-z0-9_.-]+',f)): errors.append('Dimension: '+path+':'+f)
        for key,item in value.items(): walk(item,path+'/'+str(key))
    elif isinstance(value,list):
        for i,item in enumerate(value): walk(item,path+'/'+str(i))
for n,d in docs.items(): walk(d,n)

spec=importlib.util.spec_from_file_location('niji_validator',ROOT/'scripts/validate.py')
val=importlib.util.module_from_spec(spec);spec.loader.exec_module(val)
canonical={}
for p in val.iter_content_files():
    item=yaml.safe_load(p.read_text())
    if isinstance(item,dict) and 'id' in item: canonical[item['id']]=item
known=set(canonical)|set(h['reviewed_existing_package'])
newrefs=h['library_candidates']['references']; tempkeys=[x['temporary_key'] for x in newrefs]
assert len(tempkeys)==len(set(tempkeys))
known.update(tempkeys)
def walk_evidence(value,path=''):
    if isinstance(value,dict):
        for k,item in value.items():
            if k in ['evidence_keys','reference_keys','parent_behavior_keys','boundary_keys','evidence_refs','reference_refs','subject_refs','claim_refs','case_refs','strategy_refs','analytic_refs','mitigation_refs','detects_refs','subtechnique_refs'] and isinstance(item,list):
                for ref in item:
                    counts['source_refs_checked']+=1
                    if ref not in known: errors.append('Unresolved reference: '+path+'/'+k+':'+str(ref))
            walk_evidence(item,path+'/'+str(k))
    elif isinstance(value,list):
        for i,item in enumerate(value): walk_evidence(item,path+'/'+str(i))
walk_evidence(h)
for ref,obj in h['reviewed_existing_package'].items():
    if obj.get('id')!=ref: errors.append('Identity mismatch: '+ref)
    for target,field in val.walk_references(obj):
        if target not in known: errors.append('Canonical reference: '+ref+':'+field+':'+target)
    typ=obj['type']; schema=json.loads((ROOT/'schemas'/val.SCHEMA_FOR_TYPE[typ]).read_text())
    # Research-only REF aliases are accepted in-memory; existing formal object identities remain unchanged.
    def allow_temp(x):
        if isinstance(x,dict):
            if x.get('pattern')=='^REF-[0-9]{6}$': x['pattern']='^(REF-[0-9]{6}|B012-T1497-REF-[A-Z0-9-]+)$'
            for y in x.values(): allow_temp(y)
        elif isinstance(x,list):
            for y in x: allow_temp(y)
    allow_temp(schema)
    for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(obj): errors.append('Schema '+ref+' '+str(list(e.path))+': '+e.message)
    counts['schema_objects']+=1
for obj in newrefs:
    schema=json.loads((ROOT/'schemas/reference.schema.json').read_text())
    schema['required']=['temporary_key' if x=='id' else x for x in schema['required']]
    schema['properties']['temporary_key']={'type':'string','pattern':'^B012-T1497-REF-[A-Z0-9-]+$'}
    for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(obj): errors.append('REF schema '+obj['temporary_key']+': '+e.message)
    counts['schema_objects']+=1

p=h['reviewed_existing_package']['NJT-0122']
assert p['classification']['decision_ref']=='DEC-TA0005-T1497'
assert p['classification']['tactic_refs']==['TA0005','TA0007']
for ref in ['NJS-0122-001','NJS-0122-002','NJS-0122-003']:
    d=h['reviewed_existing_package'][ref]
    assert d['parent_ref']=='NJT-0122' and d['lineage']['attck_subtechnique_inherited'] is False
    for lang in ['zh','en']:
        assert d['stealth_characteristics']['paragraphs'][0][lang].startswith(d['name'][lang])
    for mech in d['stealth_mechanisms']:
        assert all(x in d['evidence']['reference_refs'] for x in mech['evidence_refs'])
for ref in ['NJT-0122','NJS-0122-001','NJS-0122-002','NJS-0122-003']:
    for m in h['reviewed_existing_package'][ref]['stealth_mechanisms']:
        for t in m['summary'].values():
            if t.endswith(('.', '。','!','！','?','？',';', '；',':','：')): errors.append('Mechanism summary punctuation: '+ref)
mit=h['reviewed_existing_package']['MIT-000120']; old=yaml.safe_load((OUT/'before-MIT-000120.yaml').read_text())
assert mit['measures']==old['measures']
assert [a['target_ref'] for a in mit['applications']]==[a['target_ref'] for a in old['applications']]
assert [a['limitations'] for a in mit['applications']]==[a['limitations'] for a in old['applications']]
for ref in ['NJA-000107','NJA-000128','NJA-000129']:
    d=h['reviewed_existing_package'][ref]; source={s['source_type']:s for s in d['data_requirements']}
    assert 'analyst-condition-review-register' in source
    assert not any(f.startswith('condition.') for f in source['sample-native-call-and-controlflow-capture']['required_fields'])
    assert 'event.guest_clock_unit' in source['sample-native-call-and-controlflow-capture']['required_fields']
    assert d['strategy_ref']=='DET-000119'
assert set(h['reviewed_existing_package']['DET-000119']['analytic_refs'])=={'NJA-000107','NJA-000128','NJA-000129'}
for row in v['source_records']:
    q=Path(row['path']);q=q if q.is_absolute() else ROOT.parent/q
    assert hashlib.sha256(q.read_bytes()).hexdigest()==row['sha256']
for ref,sha in h['existing_package_audit']['before_sha256'].items():
    assert hashlib.sha256((OUT/('before-'+ref+'.yaml')).read_bytes()).hexdigest()==sha
report={'status':'pass' if not errors else 'fail','errors':errors,'counts':counts,'reference_candidates':len(newrefs),'source_artifacts_verified':len(v['source_records']),'canonical_writes_performed':False,'canonical_ids_allocated':False,'schema_validation_note':'In-memory schemas accept research REF temporary aliases only; no formal ID was invented. Reference candidates validate temporary_key instead of canonical id.','mit_measures_and_original_targets_and_limitations_preserved':True,'condition_semantics_separate_from_raw_capture':True}
(OUT/'strict-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors: raise SystemExit(1)
frozen={n:hashlib.sha256((RUN/n).read_bytes()).hexdigest() for n in docs}
(OUT/'freeze-manifest.json').write_text(json.dumps({'files':frozen,'strict_check_sha256':hashlib.sha256((OUT/'strict-check-report.json').read_bytes()).hexdigest()},indent=2)+'\n')
print(json.dumps({'frozen_sha256':frozen},indent=2))
