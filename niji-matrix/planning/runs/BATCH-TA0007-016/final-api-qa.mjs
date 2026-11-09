import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {MatrixRepository} from '../../../../tool/niji-matrix-review/server.mjs';
const root=fileURLToPath(new URL('../../../',import.meta.url));
const ids=JSON.parse(await readFile(new URL('./allocated-ids.json',import.meta.url),'utf8'));
const snapshot=await new MatrixRepository(root).snapshot();
assert.deepEqual(snapshot.issues,[]);
const checked=[];
for(const kind of ['NJT','NJS','CLM','CASE','DET','NJA','MIT'])for(const id of ids[kind]){
 const o=snapshot.objects[id];assert.ok(o,id);
 assert.equal(o.lifecycle?.status??o.status,'review',id);
 assert.deepEqual(o.lifecycle?.reviewers??[],[],id);
 checked.push(id);
}
const mit=snapshot.objects['MIT-000240'];
assert.equal(mit.lifecycle.status,'review');
assert.ok(mit.applications.some(a=>a.target_ref==='NJT-0231'));
assert.ok(mit.applications.some(a=>a.target_ref===ids.children.T1069[0]));
assert.equal(new Set(mit.applications.map(a=>a.target_ref)).size,mit.applications.length);
const discovery=snapshot.tactics.find(x=>x.id==='TA0007');
assert.equal(discovery.technique_ids.length,22);
for(const id of ids.NJT)assert.ok(discovery.technique_ids.includes(id));
const report={status:'passed',api_issues:[],review_objects_checked:checked.length,ids:checked,shared_mitigation:'MIT-000240',TA0007_formal_parents:22};
await writeFile(new URL('./final-api-qa.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,review_objects_checked:checked.length,api_issues:0,TA0007_formal_parents:22}));
