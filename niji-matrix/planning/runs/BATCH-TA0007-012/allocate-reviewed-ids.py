"""Reserve converged objects centrally through the canonical allocator."""
from pathlib import Path
import json
import runpy
import subprocess
import sys

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
module=runpy.run_path(str(RUN/'integrate-reviewed-content.py'))
assert (RUN/'admission-and-convergence.md').is_file()
assert not (RUN/'allocated-ids.json').exists(), 'Batch already allocated'
handoffs,groups,aliases,extensions=module['resolve_groups']()
keys={module['key'](x) for values in groups.values() for x in values}
keys.update(aliases)
for t,d in handoffs.items():
    keys.add(f'B012-{t}-PARENT')
    keys.update(module['key'](c) for c in d.get('proposed_subtechniques',[]) if module['key'](c))

def check(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in {'temporary_key','key','parent_key','strategy_key','target_key','existing_key','existing_temporary_key'} or k.endswith('_keys') or k.endswith('_refs'):
                for ref in v if isinstance(v,list) else [v]:
                    if isinstance(ref,str) and ref.startswith('B012-'):assert ref in keys,ref
            check(v)
    elif isinstance(value,list):
        for v in value:check(v)
for d in handoffs.values():
    for part in ['proposed_content','proposed_subtechniques','library_candidates','defense_candidates','canonical_revisions']:check(d.get(part,{}))
new_candidates=[t for t,d in handoffs.items() if d['recommendation']['decision']!='exclude' and not d.get('existing_technique_ref')]
counts={'NJT':len(new_candidates),'NJS':sum(len(handoffs[t].get('proposed_subtechniques',[])) for t in new_candidates),
        **{e:len(items) for e,items in groups.items()}}
(RUN/'allocation-counts.json').write_text(json.dumps(counts,indent=2)+'\n')
allocated={}
def reserve(entity,count,parent=None):
    args=[sys.executable,'scripts/allocate_id.py','reserve',entity,'--count',str(count),'--owner','BATCH-TA0007-012']
    if parent:args.extend(['--parent',parent])
    result=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True)
    values=result.stdout.strip().splitlines();assert len(values)==count,result.stdout
    print(entity,values,flush=True)
    return values
allocated['NJT']=reserve('NJT',counts['NJT']) if counts['NJT'] else []
allocated['parents']={t:d['existing_technique_ref'] for t,d in handoffs.items() if d.get('existing_technique_ref')}
allocated['parents'].update(dict(zip(new_candidates,allocated['NJT'],strict=True)))
allocated['parents'].update({t:None for t,d in handoffs.items() if d['recommendation']['decision']=='exclude'})
allocated['NJS']={}
destination=RUN/'allocated-ids.json'
destination.write_text(json.dumps(allocated,indent=2)+'\n')
for t in new_candidates:
    parent=allocated['parents'][t]
    count=len(handoffs[t].get('proposed_subtechniques',[]))
    allocated['NJS'][parent]=reserve('NJS',count,parent) if count else []
    destination.write_text(json.dumps(allocated,indent=2)+'\n')
for entity,items in groups.items():
    allocated[entity]=reserve(entity,len(items)) if items else []
    destination.write_text(json.dumps(allocated,indent=2)+'\n')
