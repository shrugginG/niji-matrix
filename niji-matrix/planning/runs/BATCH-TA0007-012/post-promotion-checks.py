"""Run only checks affected by lifecycle/planning promotion and rebuild delivery bundles."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json,os,subprocess,sys
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
ids=json.loads((RUN/'allocated-ids.json').read_text())
parents=[ids['parents'][t] for t in ['T1033','T1007','T1124','T1673','T1497']]
checks=[('final-content-validation.log',[sys.executable,'scripts/validate.py']),('final-planning-validation.log',[sys.executable,'scripts/validate_planning.py']),('final-catalog.log',[sys.executable,'scripts/library_catalog.py']),('final-reserved-ids.log',[sys.executable,'scripts/allocate_id.py','list','--status','reserved']),('final-pipeline-status.log',[sys.executable,'scripts/pipeline_status.py'])]
def run_check(item):
 name,args=item
 x=subprocess.run(args,cwd=ROOT,capture_output=True,text=True);(RUN/name).write_text(x.stdout+x.stderr);return name,x.returncode
with ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(run_check,checks))
print(json.dumps(results),flush=True);assert all(code==0 for name,code in results)
def build(p):
 x=subprocess.run([sys.executable,'scripts/build_technique_bundle.py',p],cwd=ROOT,capture_output=True,text=True);return p,x.returncode,x.stdout+x.stderr
with ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(build,parents))
(RUN/'final-bundles.log').write_text('\n'.join(p+'\n'+out for p,code,out in results));print(json.dumps([{'bundle':p,'code':code} for p,code,out in results]),flush=True);assert all(code==0 for p,code,out in results)
def qa(p):
 x=subprocess.run(['node',str(RUN/'browser-qa.mjs'),p,'BATCH-TA0007-012'],cwd=ROOT.parents[0],env={**os.environ,'NIJI_EXPECT_REVIEW':'1'},capture_output=True,text=True);return p,x.returncode,x.stdout+x.stderr
with ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(qa,parents))
(RUN/'final-browser-qa.log').write_text('\n'.join(p+'\n'+out for p,code,out in results));print(json.dumps([{'browser':p,'code':code} for p,code,out in results]),flush=True);assert all(code==0 for p,code,out in results)
