from pathlib import Path
import copy, hashlib, json, re, yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[5]
BATCH=Path(__file__).resolve().parents[2]
E=Path(__file__).resolve().parent
H=BATCH/'T1673-research-handoff.yaml'; V=BATCH/'T1673-evidence-verification.yaml'
class Strict(yaml.SafeLoader):pass
def mapping(loader,node,deep=False):
 out={}
 for k,v in node.value:
  key=loader.construct_object(k,deep=deep)
  if key in out:raise ValueError('Duplicate key '+str(key))
  out[key]=loader.construct_object(v,deep=deep)
 return out
Strict.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
def read(p):return yaml.load(p.read_text(),Loader=Strict)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
h=read(H);v=read(V)
errors=[];metrics={'bilingual_dicts':0,'narrative_sections':0,'machine_keys':0,'temporary_objects':0,'schema_objects':0,'raw_hashes':0,'derived_text_hashes':0}
def check(ok,msg):
 if not ok:errors.append(msg)
def walk(x,path='root'):
 if isinstance(x,dict):
  if 'zh' in x or 'en' in x:
   metrics['bilingual_dicts']+=1
   check(set(x)=={'zh','en'},path+' bilingual keys '+str(set(x)))
   check(all(isinstance(x.get(k),str) and x[k].strip() for k in ['zh','en']),path+' bilingual string values')
  for k,a in x.items():
   metrics['machine_keys']+=1
   check(isinstance(k,str) and re.fullmatch('[a-z][a-z0-9_]*',k)!=None,path+' nonlower key '+str(k))
   if k=='paragraphs':
    metrics['narrative_sections']+=1
    check(isinstance(a,list) and 1<=len(a)<=4,path+' paragraph count')
    if isinstance(a,list):
     for i,p in enumerate(a):
      check(isinstance(p,dict) and set(p)=={'zh','en'},path+f' paragraph {i} pairing')
      if isinstance(p,dict):
       for lang,t in p.items():
        if isinstance(t,str):check(not re.search(r'(^|\n)\s*(?:[-*#]|\d+\.)\s',t),path+' markdown fragment')
   if k in ['required_fields','dimensions'] and isinstance(a,list):
    check(len(a)==len(set(a)),path+' duplicate machine dimension')
    check(all(isinstance(z,str) and re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*',z) for z in a),path+' upper or malformed machine fields')
   walk(a,path+'.'+str(k))
 elif isinstance(x,list):
  for i,a in enumerate(x):walk(a,path+f'[{i}]')
walk(h,'handoff');walk(v,'verification')
objects=[h['proposed_content']]+h['proposed_subtechniques']
for group in ['detection_strategies','detection_analytics','mitigations']:objects+=h['defense_candidates'][group]
for group in ['references','claims','cases','detection_strategies','detection_analytics','mitigations','relationships']:objects+=h['library_candidates'][group]
idx={}
for o in objects:
 key=o['temporary_key'];check(key not in idx,'duplicate temporary object '+key);idx[key]=o
 check(key.startswith('B012-T1673-'),'wrong temporary prefix '+key)
metrics['temporary_objects']=len(idx)
check(len(idx)==26,'expected 26 complete temporary objects')
# Resolve all exact temporary pointers, plus confirmed existing semantic-library references.
canonical={}
for dirname in ['references','claims','cases','detections','analytics','mitigations','relationships','mechanisms']:
 for p in (ROOT/dirname).glob('*.yaml'):
  d=yaml.safe_load(p.read_text())
  if isinstance(d,dict) and d.get('id'):canonical[d['id']]=d
for p in (ROOT/'matrix/tactics').glob('*/techniques/*/technique.yaml'):
 d=yaml.safe_load(p.read_text());canonical[d['id']]=d
for p in (ROOT/'matrix/tactics').glob('*/techniques/*/subtechniques/*/subtechnique.yaml'):
 d=yaml.safe_load(p.read_text());canonical[d['id']]=d

def refs(x,path='root'):
 if isinstance(x,dict):
  for k,a in x.items():
   if k not in ['temporary_key','temporary_key_prefix']:refs(a,path+'.'+k)
 elif isinstance(x,list):
  for i,a in enumerate(x):refs(a,path+f'[{i}]')
 elif isinstance(x,str) and (x.startswith('B012-T1673-') or re.fullmatch(r'(?:REF|CLM|CASE|DET|NJA|MIT|NJT|NJS|NM)-[A-Z0-9-]+',x)):
  check(x in idx or x in canonical,'unresolved reference '+path+': '+x)
refs(h);refs(v)
check(h['recommendation']['decision']=='retain','wrong admission')
check(h['candidate']['source_attack_version']=='19.1','baseline')
check(h['recommendation']['original_attack_subtechniques_imported'] is False,'lineage import')
check(h['proposed_subtechniques']==[],'children')
check(h['proposed_content']['subtechnique_taxonomy']['coverage']=='deferred','taxonomy coverage')
check(h['proposed_content']['aliases']==[],'aliases shape')
check(h['proposed_content']['stealth_mechanisms'][0]['mechanism_ref']=='NM-FD','final mechanism')
check(len(h['proposed_content']['stealth_mechanisms'])==1,'supported mechanism count')
for m in h['proposed_content']['stealth_mechanisms']:
 for text in m['summary'].values():check(not re.search(r'[.!?。！？；;]$',text),'mechanism punctuation')
 check(set(m['evidence_keys'])<=set(h['proposed_content']['evidence']['reference_keys']),'mechanism evidence not in parent')
check(h['library_candidates']['claims'][0]['evidence_mode']=='strongly-inferred','admission claim mode')
check(all(c['time_range'] is None and c['target_sectors_zh']==[] and c['target_sectors_en']==[] for c in h['library_candidates']['cases']),'case metadata')
check(h['library_candidates']['references'][1]['url'].startswith('https://www.trendaisecurity.com/'),'Trend canonical URL')
for k in ['detection_strategies','detection_analytics','mitigations']:
 check(h['library_candidates'][k]==[],'duplicate defense storage '+k)
for s in h['defense_candidates']['detection_strategies']:
 check(s['detects_keys']==['B012-T1673-PARENT'],'strategy subjects')
 for a in s['analytic_keys']:check(idx[a]['strategy_key']==s['temporary_key'],'strategy analytic reverse')
 for a in s['analytic_keys']:check(set(idx[a]['evidence_keys'])<=set(s['evidence_keys']),'DET missing analytic evidence')
for m in h['defense_candidates']['mitigations']:
 targets=[a['target_key'] for a in m['applications']]
 check(len(targets)==len(set(targets)),'duplicate MIT applications')
 check('B012-T1673-PARENT' in targets,'MIT target')
# Local schema projection changes only temporary-link vocabulary and ID validation patterns.
# It allocates no canonical identities and writes no canonical objects.
renames={'temporary_key':'id','subject_keys':'subject_refs','evidence_keys':'evidence_refs','strategy_key':'strategy_ref','detects_keys':'detects_refs','analytic_keys':'analytic_refs','target_key':'target_ref','strategy_keys':'strategy_refs','mitigation_keys':'mitigation_refs','claim_keys':'claim_refs','case_keys':'case_refs','reference_keys':'reference_refs','subtechnique_keys':'subtechnique_refs'}
def project(x):
 if isinstance(x,dict):return {renames.get(k,k):project(a) for k,a in x.items()}
 if isinstance(x,list):return [project(a) for a in x]
 return x

def adapt_schema(x):
 if isinstance(x,dict):
  for k,a in list(x.items()):
   if k=='pattern' and isinstance(a,str) and a.startswith('^') and any(z in a for z in ['NJT-','NJS-','REF-','CLM-','CASE-','DET-','NJA-','MIT-']):
    x[k]='(?:'+a+')|(?:^B012-T1673-[A-Z0-9-]+$)'
   else:adapt_schema(a)
 elif isinstance(x,list):
  for a in x:adapt_schema(a)

schema_files={'technique':'technique','detection-strategy':'detection','detection-analytic':'analytic','mitigation':'mitigation','reference':'reference','claim':'claim','case':'case'}
for o in objects:
 s=json.loads((ROOT/'schemas'/f"{schema_files[o['type']]}.schema.json").read_text());adapt_schema(s)
 if o['type']=='technique':s['properties']['classification']['required'].remove('decision_ref')
 p=project(o)
 for e in Draft202012Validator(s,format_checker=FormatChecker()).iter_errors(p):
  errors.append(o['temporary_key']+' schema '+'.'.join(map(str,e.path))+': '+e.message)
 metrics['schema_objects']+=1
# Exact new-reference URLs must not collide with canonical publication identities.
for r in h['library_candidates']['references']:
 for c in canonical.values():
  if c.get('type')=='reference':check(c.get('url')!=r['url'],'exact URL duplicate '+r['temporary_key']+' '+c['id'])
for src in v['examined_sources']:
 check(sha(ROOT/src['raw_path'])==src['raw_sha256'],'raw hash '+src['artifact_key']);metrics['raw_hashes']+=1
 check(sha(ROOT/src['text_path'])==src['text_sha256'],'text hash '+src['artifact_key']);metrics['derived_text_hashes']+=1
 (ROOT/src['text_path']).read_text(encoding='utf-8',errors='strict')
check(sha(ROOT/v['primary_overrides']['path'])==v['primary_overrides']['sha256'],'override source modified')
check(sha(ROOT/v['fixed_baseline']['path'])==v['fixed_baseline']['sha256'],'baseline modified')
api=idx['B012-T1673-NJA-API-INVENTORY']
api_text=' '.join(p['en'] for p in api['logic']['paragraphs'])
for token in ['capture_state','page_state','property_state','missingSet','complete_for_explicit_paths','not_fully_assessable']:
 check(token in api_text,'missing API result distinction '+token)
check('page_state but partial property_state' in api['tuning_guidance']['paragraphs'][0]['en'],'property-partial acceptance scenario')
report={'status':'passed' if not errors else 'failed','metrics':metrics,'errors':errors,'scope':'candidate-staging-contract-and-adapted-canonical-object-schemas; no canonical allocation, build or Web gate'}
(E/'strict-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report,indent=2,ensure_ascii=False))
if errors:raise SystemExit(1)
