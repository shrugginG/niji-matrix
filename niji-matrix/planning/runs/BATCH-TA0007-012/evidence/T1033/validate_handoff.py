from pathlib import Path
import yaml,json,re,hashlib
root=Path(__file__).resolve().parents[2]
repo=root.parents[2]
class Strict(yaml.SafeLoader):pass
def mapping(loader,node,deep=False):
 out={}
 for k,v in node.value:
  key=loader.construct_object(k,deep=deep)
  if key in out:raise ValueError('duplicate YAML key '+str(key))
  out[key]=loader.construct_object(v,deep=deep)
 return out
Strict.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
def read(p):return yaml.load(p.read_text(),Loader=Strict)
h=read(root/'T1033-research-handoff.yaml');v=read(root/'T1033-evidence-verification.yaml')
counts={'bilingual_maps':0,'paragraph_sections':0,'flat_bilingual_pairs':0}
def walk(x,path='root'):
 if isinstance(x,dict):
  if 'zh' in x or 'en' in x:
   assert set(x)=={'zh','en'},(path,'bilingual keys',list(x))
   assert all(isinstance(x[k],str) and x[k].strip() for k in ('zh','en')),(path,'bilingual value')
   counts['bilingual_maps']+=1
  if 'paragraphs' in x:
   assert isinstance(x['paragraphs'],list) and 1<=len(x['paragraphs'])<=4,(path,'paragraph count')
   counts['paragraph_sections']+=1
  for k in x:
   if k.endswith('_zh'):
    en=k[:-3]+'_en';assert en in x,(path,k,'missing English')
    assert type(x[k])==type(x[en]),(path,k,'unequal types')
    counts['flat_bilingual_pairs']+=1
   if k.endswith('_en') and not k.endswith('_zh_en'):assert k[:-3]+'_zh' in x,(path,k,'missing Chinese')
  for k,z in x.items():walk(z,path+'.'+k)
 elif isinstance(x,list):
  for i,z in enumerate(x):walk(z,path+'['+str(i)+']')
walk(h);walk(v)
objects=[h['proposed_content']]+h['proposed_subtechniques']
for group in ('detection_strategies','detection_analytics','mitigations'):
 objects+=h['defense_candidates'][group]
for group in ('references','claims','cases'):
 objects+=h['library_candidates'][group]
defs={o['temporary_key']:o for o in objects};assert len(defs)==len(objects)
all_values=[]
def strings(x):
 if isinstance(x,str):all_values.append(x)
 elif isinstance(x,dict):
  for k,z in x.items():
   if k!='temporary_key_prefix':strings(z)
 elif isinstance(x,list):
  for z in x:strings(z)
strings(h);strings(v)
temprefs={s for s in all_values if re.fullmatch(r'B012-T1033-[A-Z0-9-]+',s)}
assert not(temprefs-set(defs)),('unresolved temporary refs',temprefs-set(defs))
canonical_refs={s for s in all_values if re.fullmatch(r'(?:REF|CASE|DET|NJA|MIT|NJT|NJS|CLM|NM)-[A-Z0-9-]+',s)}
canonical_ids={}
for d in ('references','cases','claims','detections','analytics','mitigations','mechanisms'):
 for p in (repo/d).glob('*.yaml'):
  o=read(p);canonical_ids[o['id']]=p
for p in (repo/'matrix').rglob('*.yaml'):
 o=read(p)
 if isinstance(o,dict) and 'id'in o:canonical_ids[o['id']]=p
assert not(canonical_refs-set(canonical_ids)),('unresolved canonical refs',canonical_refs-set(canonical_ids))
assert h['candidate']['source_attack_version']=='19.1'
assert h['recommendation']['decision'] in ('retain','adapt','exclude','add')
assert h['recommendation']['original_attack_subtechniques_imported'] is False
conf={'high','medium','low','hypothesis'}
for o in objects:
 assert 'id' not in o,('formal ID introduced',o['temporary_key'])
 if 'confidence'in o:assert o['confidence']in conf
 if 'lifecycle'in o:assert o['lifecycle']['status']=='draft'
 for m in o.get('stealth_mechanisms',[]):
  assert m['mechanism_ref'] in ('NM-BT','NM-FD','NM-ST','NM-DO')
  assert m['role']in ('primary','secondary') and m['confidence']in conf
  assert set(m['evidence_keys'])<=set(o['evidence']['reference_keys'])
  assert not any(m['summary'][k][-1]in '.。!?！？;；:'for k in ('zh','en'))
 if o['type']=='claim':
  assert o['claim_type']in ('technique-relevance','technique-boundary','mechanism-mapping','subtechnique-existence','case-attribution','detection','mitigation','other')
  assert o['evidence_mode']in ('directly-observed','strongly-inferred','hypothesized')
for c in h['proposed_subtechniques']:
 assert c['parent_key']==h['proposed_content']['temporary_key'] and not c['lineage']['attck_subtechnique_inherited']
 assert all(c['stealth_characteristics']['paragraphs'][0][lang].startswith(c['name'][lang])for lang in ('zh','en'))
strategies=h['defense_candidates']['detection_strategies'];analytics=h['defense_candidates']['detection_analytics']
for d in strategies:
 aa=[a for a in analytics if a['strategy_key']==d['temporary_key']]
 assert set(d['analytic_keys'])=={a['temporary_key']for a in aa}
 assert set().union(*(set(a['evidence_keys'])for a in aa))<=set(d['evidence_keys'])
for a in analytics:
 assert all(x==x.lower() for x in a['platforms']+a['correlation']['dimensions'])
 for data in a['data_requirements']:
  assert data['source_type']==data['source_type'].lower()
  assert data['required_fields'] and all(x==x.lower()for x in data['required_fields'])
for m in h['defense_candidates']['mitigations']:
 targets=[a['target_key']for a in m['applications']];assert len(targets)==len(set(targets))
 assert set(targets)=={x['temporary_key']for x in [h['proposed_content']]+h['proposed_subtechniques']}
 assert all(z['control_type']in ('preventive','exposure-reduction','cost-increasing','detective-support','containment','governance')for z in m['measures'])
urls={str(read(p).get('url','')).rstrip('/').lower():p for p in (repo/'references').glob('*.yaml')}
assert all(x['url'].rstrip('/').lower()not in urls for x in h['library_candidates']['references']), 'duplicate new REF URL'
for s in v['download_hashes']:
 assert 'error' not in s,s
 p=root/'evidence/T1033'/s['file']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],s['file']
for s in v['original_sources_examined']:
 for f in s['artifacts']:assert (root/'evidence/T1033'/f).is_file(),f
assert v['fixed_baseline_sha256']==hashlib.sha256((root/'fixed-baseline-T1033.json').read_bytes()).hexdigest()
report={'status':'pass','strict_duplicate_keys':'pass','bilingual_keys':'pass','temporary_references':'pass','canonical_references':'pass','enums':'pass','paragraph_counts':'pass','child_exact_name_opening':'pass','strategy_analytic_bidirection':'pass','mitigation_targets':'pass','new_reference_url_duplicates':'none','download_hashes':'pass','temporary_object_count':len(objects),'new_reference_count':len(h['library_candidates']['references']),'new_claim_count':len(h['library_candidates']['claims']),'new_case_count':len(h['library_candidates']['cases']),'original_snapshot_count':len(v['download_hashes']),**counts}
(root/'evidence/T1033/validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
