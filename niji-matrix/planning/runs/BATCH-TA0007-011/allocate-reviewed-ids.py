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
    keys.add(f'B011-{t}-PARENT')
    keys.update(module['key'](c) for c in d['proposed_subtechniques'])

def check(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in {'temporary_key','key','parent_key','strategy_key','target_key','existing_key','existing_temporary_key'} or k.endswith('_keys'):
                for ref in v if isinstance(v,list) else [v]:
                    if isinstance(ref,str) and ref.startswith('B011-'):assert ref in keys,ref
            check(v)
    elif isinstance(value,list):
        for v in value:check(v)
for d in handoffs.values():
    for part in ['proposed_content','proposed_subtechniques','library_candidates','defense_candidates']:check(d[part])
counts={'NJT':len(handoffs),'NJS':sum(len(d['proposed_subtechniques']) for d in handoffs.values()),
        **{e:len(items) for e,items in groups.items()}}
(RUN/'allocation-counts.json').write_text(json.dumps(counts,indent=2)+'\n')
allocated={}
def reserve(entity,count,parent=None):
    args=[sys.executable,'scripts/allocate_id.py','reserve',entity,'--count',str(count),'--owner','BATCH-TA0007-011']
    if parent:args.extend(['--parent',parent])
    result=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True)
    values=result.stdout.strip().splitlines();assert len(values)==count,result.stdout
    print(entity,values,flush=True)
    return values
allocated['NJT']=reserve('NJT',counts['NJT'])
allocated['NJS']={}
destination=RUN/'allocated-ids.json'
destination.write_text(json.dumps(allocated,indent=2)+'\n')
for (t,d),parent in zip(handoffs.items(),allocated['NJT'],strict=True):
    allocated['NJS'][parent]=reserve('NJS',len(d['proposed_subtechniques']),parent)
    destination.write_text(json.dumps(allocated,indent=2)+'\n')
for entity,items in groups.items():
    allocated[entity]=reserve(entity,len(items)) if items else []
    destination.write_text(json.dumps(allocated,indent=2)+'\n')
