"""Primary-agent serialization of an individually reviewed temporary proposal.

No prose is originated here. Admission and shared identities must already be reviewed.
"""
from pathlib import Path
from datetime import datetime,timezone
import sys,re,copy,yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import allocate_id
from library_common import load_objects,canonicalize_url

batch=sys.argv[1]
run=ROOT/'planning/runs'/batch
previous='BATCH-TA0006-'+str(int(batch.rsplit('-',1)[1])-1).zfill(3)
if previous!='BATCH-TA0006-010':
 import json
 assert json.loads((ROOT/'planning/runs'/previous/'acceptance.json').read_text())['status']=='passed','Previous delivery batch must pass before canonical writing'
assert (run/'admission-and-taxonomy-review.md').is_file(),'Primary admission review required before allocation'
assert not (run/'id-map.yaml').exists(),'One-shot serializer: allocation already exists; continue from the recorded map instead of replaying'
proposal=yaml.safe_load((run/'approved-proposal.yaml').read_text())
resolutions=yaml.safe_load((run/'shared-resolutions.yaml').read_text())
existing,paths=load_objects(ROOT)
mapping=dict(resolutions.get('temporary_to_existing',{}))
for temp,id_ in mapping.items():assert id_ in existing,(temp,id_)
groups=[('references','REF','reference','references'),('claims','CLM','claim','claims'),('cases','CASE','case','cases'),('strategies','DET','detection-strategy','detections'),('analytics','NJA','detection-analytic','analytics'),('mitigations','MIT','mitigation','mitigations')]
parent=proposal['parent']; children=proposal.get('children',[])
assert parent['id'].startswith('TMP')
for g,_,_,_ in groups:
 for o in proposal.get(g,[]):
  assert o['id'].startswith('TMP'),(g,o['id'])
  if g=='references':
   matches=[v['id'] for v in existing.values() if v.get('type')=='reference' and canonicalize_url(v.get('url')) and canonicalize_url(v.get('url'))==canonicalize_url(o.get('url'))]
   if matches:assert mapping.get(o['id']) in matches,('Existing URL must be resolved explicitly',o['id'],matches)
# Use the official allocator algorithms under its single registry lock.
with allocate_id.lock_registry(ROOT):
 registry=allocate_id.load_reservations(ROOT)
 occupied=set(existing)|{x['id'] for x in registry['reservations']}
 now=datetime.now(timezone.utc).isoformat()
 def reserve(entity,count,parent_ref=None):
  result=allocate_id.next_ids(entity,count,occupied,parent_ref)
  occupied.update(result)
  registry['reservations'].extend(dict(id=x,entity=entity,owner=batch,status='reserved',created=now,updated=now) for x in result)
  return result
 parent_id=reserve('NJT',1)[0];mapping[parent['id']]=parent_id
 for obj,id_ in zip(children,reserve('NJS',len(children),parent_id)):mapping[obj['id']]=id_
 for g,entity,_,_ in groups:
  new=[o for o in proposal.get(g,[]) if o['id'] not in mapping]
  for o,id_ in zip(new,reserve(entity,len(new))):mapping[o['id']]=id_
 allocate_id.write_reservations(ROOT,registry)
(run/'id-map.yaml').write_text(yaml.safe_dump(mapping,allow_unicode=True,sort_keys=False))
def replace(v):
 if isinstance(v,str):return mapping.get(v,v)
 if isinstance(v,list):return [replace(x) for x in v]
 if isinstance(v,dict):
  result={k:replace(x) for k,x in v.items()}
  for key,value in result.items():
   if key.endswith('_refs') and isinstance(value,list) and all(isinstance(x,str) for x in value):result[key]=list(dict.fromkeys(value))
  return result
 return v
DATE='2026-11-05'
def lifecycle(o):
 life=o.setdefault('lifecycle',{})
 life.update(status='draft',version=life.get('version','0.1.0'),created=life.get('created',DATE),modified=DATE,contributors=life.get('contributors',['Niji Matrix Research']),reviewers=[])
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:90].rstrip('-')
written={}
def emit(path,o):
 if o.get('type') in {'technique','evasion-subtechnique'}:
  order=['schema_version','type','id','parent_ref','name','summary','aliases','classification','lineage','definition_and_concept','stealth_characteristics','scope_boundary_definition','application_scenarios_and_threat_model','stealth_mechanisms','subtechnique_taxonomy','defense','evidence','research','lifecycle']
  o={k:o[k] for k in order if k in o}|{k:v for k,v in o.items() if k not in order}
 text=yaml.safe_dump(o,allow_unicode=True,sort_keys=False,width=135)
 assert not re.search(r'TMP(?:1558|1552|1539)-|__REQUIRED',text),'Unresolved research key or placeholder'
 path=ROOT/path;assert not path.exists(),str(path)
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
 written[o['id']]=str(path.relative_to(ROOT))
# Canonical libraries precede the subject packages.
for g,_,kind,folder in groups:
 for raw in proposal.get(g,[]):
  if raw['id'] in resolutions.get('temporary_to_existing',{}):continue
  o=replace(copy.deepcopy(raw));o['type']=kind
  o['schema_version']='2.0.0' if g in ['strategies','analytics','mitigations'] else '1.0.0'
  if g in ['strategies','analytics','mitigations']:lifecycle(o)
  elif g in ['claims','cases']:o['status']='draft'
  title=o.get('title_en') or o.get('name_en') or o.get('name',{}).get('en','research-object')
  emit(Path(folder)/f'{o["id"]}-{slug(title)}.yaml',o)
for extension in resolutions.get('extensions',[]):
 id_=extension['id'];o=copy.deepcopy(existing[id_])
 if extension.get('append_locator'):o['locator']=(o.get('locator') or '')+'; '+extension['append_locator']
 for key,values in extension.get('append_unique',{}).items():
  target=o.setdefault(key,[])
  for value in replace(values):
   if value not in target:target.append(value)
 for key,value in extension.get('set',{}).items():o[key]=replace(value)
 if 'lifecycle' in o:o['lifecycle'].update(status='draft',modified=DATE,version=extension.get('version',o['lifecycle']['version']))
 paths[id_].write_text(yaml.safe_dump(o,allow_unicode=True,sort_keys=False,width=135))
 written[id_]=str(paths[id_].relative_to(ROOT))
decision=replace(copy.deepcopy(proposal['decision']))
source=decision['candidate']['source_attack_id']
decision.update(id=f'DEC-TA0006-{source}',schema_version='1.1.0',type='technique-decision',tactic_ref='TA0006',resulting_technique_ref=parent_id,original_attack_subtechniques_imported=False)
decision['candidate']['source_attack_version']='19.1'
decision.setdefault('review',{}).update(status='draft',authors=['Niji Matrix Research'],reviewers=[])
parent=replace(copy.deepcopy(parent));parent.update(schema_version='2.0.0',type='technique');lifecycle(parent)
parent['classification']=dict(tactic_refs=['TA0006'],origin=dict(kind='attack-'+('retained' if decision['decision']=='retain' else 'adapted'),source_attack_id=source,source_attack_version='19.1'),decision_ref=decision['id'])
parent['subtechnique_taxonomy']['subtechnique_refs']=[mapping[c['id']] for c in children]
base=Path('matrix/tactics/TA0006-credential-access/techniques')/f'{parent_id}-{slug(parent["name"]["en"])}'
emit(base/'technique.yaml',parent)
for raw in children:
 o=replace(copy.deepcopy(raw));o.update(schema_version='2.0.0',type='evasion-subtechnique',parent_ref=parent_id,lineage={'attck_subtechnique_inherited':False});lifecycle(o)
 emit(base/'subtechniques'/f'{o["id"]}-{slug(o["name"]["en"])}'/'subtechnique.yaml',o)
emit(Path('matrix/tactics/TA0006-credential-access/decisions')/f'{decision["id"]}.yaml',decision)
plan_file=ROOT/'planning/tactics/TA0006.yaml';plan=yaml.safe_load(plan_file.read_text())
for w in plan['work_items']:
 if w.get('source_attack_id')==source:
  w.update(stage='authoring',decision_ref=decision['id'],resulting_technique_ref=parent_id)
  w['notes_zh']='完整并行研究返回后由主 Agent 完成准入、原生分类和共享库裁决；正式草稿集成，等待本批独立质量、Bundle 与双语 Web 门禁。'
  w['notes_en']='After the complete parallel research returned, the primary agent adjudicated admission, native taxonomy, and shared identities. Canonical drafts are integrated pending independent quality, bundle, and bilingual Web gates.'
plan_file.write_text(yaml.safe_dump(plan,allow_unicode=True,sort_keys=False,width=135))
assert set(mapping.values()) <= set(written)|set(existing),'Every allocated/reused identity must resolve after serialization'
(run/'written-paths.yaml').write_text(yaml.safe_dump(written,allow_unicode=True,sort_keys=False))
print(yaml.safe_dump(dict(batch=batch,parent=parent_id,children=[mapping[c['id']] for c in children],written=len(written)),sort_keys=False))
