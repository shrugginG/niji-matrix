import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {mkdtemp,readFile,writeFile,mkdir,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createApp,MatrixRepository} from '../../../../tool/niji-matrix-review/server.mjs';
const root=fileURLToPath(new URL('../../../',import.meta.url));
const out=fileURLToPath(new URL(`./web-qa/${process.argv[2]}/`,import.meta.url));
await mkdir(out,{recursive:true});
const repository=new MatrixRepository(root), snapshot=await repository.snapshot();
assert.deepEqual(snapshot.issues,[]);
const parent=snapshot.objects[process.argv[2]];
assert.ok(parent && /^BATCH-TA0007-016$/.test(process.argv[3]));
const subjects=[parent.id,...parent.subtechnique_taxonomy.subtechnique_refs];
const strategies=[...new Set(subjects.flatMap(id=>snapshot.objects[id].defense.detections.strategy_refs))];
const analytics=[...new Set(strategies.flatMap(id=>snapshot.objects[id].analytic_refs))];
const mitigations=[...new Set(subjects.flatMap(id=>snapshot.objects[id].defense.mitigations.mitigation_refs))];
const ids=[...subjects,...strategies,...analytics,...mitigations];
const profile=await mkdtemp(join(tmpdir(),'niji-ta0007-b016-chrome-'));
const server=createApp(repository).listen(0,'127.0.0.1');
await new Promise(done=>server.once('listening',done));
const base=`http://127.0.0.1:${server.address().port}`;
const chrome=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-extensions','--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank'],{stdio:['ignore','ignore','pipe']});
let errors='';chrome.stderr.on('data',x=>{errors=(errors+x).slice(-3000)});
const pause=ms=>new Promise(done=>setTimeout(done,ms));
let ws;const report={parent:parent.id,api_issues:snapshot.issues,browser_errors:[],pages:[]};
try{
 let port;for(let n=0;n<200;n++){try{port=(await readFile(join(profile,'DevToolsActivePort'),'utf8')).split('\n')[0];break}catch{await pause(100)}}
 assert.ok(port,errors);
 const tabs=await fetch(`http://127.0.0.1:${port}/json/list`).then(r=>r.json());
 ws=new WebSocket(tabs.find(x=>x.type==='page').webSocketDebuggerUrl);
 await new Promise((done,reject)=>{ws.addEventListener('open',done,{once:true});ws.addEventListener('error',reject,{once:true})});
 let counter=0;const pending=new Map();
 ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.method==='Runtime.exceptionThrown')report.browser_errors.push(m.params.exceptionDetails.text);if(pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result)}});
 const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++counter;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});assert.ok(!r.exceptionDetails,JSON.stringify(r.exceptionDetails));return r.result.value};
 const until=async expression=>{for(let n=0;n<600;n++){if(await evaluate(expression))return;await pause(100)}throw new Error('Timeout: '+expression)};
 await call('Page.enable');await call('Runtime.enable');
 await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
 await call('Page.navigate',{url:base+'/#/object/'+parent.id});
 await until("document.querySelectorAll('.content-section').length>5");
 for(const lang of ['zh','en']){
  await evaluate(`document.querySelector('[data-lang="${lang}"]').click()`);
  await until(`document.documentElement.lang==='${lang==='zh'?'zh-CN':'en'}'`);
  for(const id of ids){
   const obj=snapshot.objects[id];await evaluate(`location.hash='#/object/${id}'`);
   await until(`document.querySelector('h1')?.textContent.includes(${JSON.stringify(obj.name[lang])})`);
   await evaluate("document.querySelectorAll('main details').forEach(x=>{x.open=true})");
   const rendered=await evaluate("({title:document.querySelector('h1').textContent,text:[...document.querySelectorAll('main .content-section:not(#source)')].map(x=>x.innerText).join(' '),sections:[...document.querySelectorAll('.content-section')].map(x=>x.id),links:[...document.querySelectorAll('main a[href^=\"#/object/\"]')].map(x=>x.getAttribute('href')),all_links:[...document.querySelectorAll('main a[href]')].map(x=>x.getAttribute('href'))})");
   // A Registry API source legitimately discusses undefined buffer contents.
   // Reject unbacked renderer placeholders without rejecting that authored term.
   const evidenceIDs=obj.evidence?.reference_refs??obj.evidence_refs??[];
   const expectedUndefined=(JSON.stringify([obj,...evidenceIDs.map(ref=>snapshot.objects[ref])]).match(/\bundefined\b/g)||[]).length;
   assert.ok((rendered.text.match(/\bundefined\b/g)||[]).length<=expectedUndefined,id+' unbacked undefined');
   assert.ok(await evaluate(`document.querySelector('#source pre')?.textContent.includes('${id}')`));
   if(subjects.includes(id)){
    assert.deepEqual(rendered.sections,['definition','stealth-characteristics','scope','context','mechanisms',...(id===parent.id?['subtechniques']:[]),'detections','mitigations','cases','claims','references','limitations','governance','source']);
    for(const s of [obj.definition_and_concept,obj.stealth_characteristics,obj.scope_boundary_definition,obj.application_scenarios_and_threat_model.application_scenarios,obj.application_scenarios_and_threat_model.threat_model.attacker_model,obj.application_scenarios_and_threat_model.threat_model.defender_model,obj.research.limitations])for(const p of s.paragraphs)assert.ok(rendered.text.includes(p[lang]),id+' missing paragraph');
    for(const m of obj.stealth_mechanisms)for(const p of m.analysis.paragraphs)assert.ok(rendered.text.includes(p[lang]));
    for(const ref of [...obj.defense.detections.strategy_refs,...obj.defense.mitigations.mitigation_refs,...obj.evidence.claim_refs,...obj.evidence.case_refs]){assert.ok(snapshot.objects[ref],ref);assert.ok(rendered.links.includes('#/object/'+ref),ref);}
    for(const ref of obj.evidence.reference_refs){assert.ok(snapshot.objects[ref],ref);assert.ok(rendered.text.includes(ref),ref);assert.ok(rendered.all_links.includes(snapshot.objects[ref].url),ref);}
   }
   if(strategies.includes(id))for(const aid of obj.analytic_refs){assert.ok(rendered.links.includes('#/object/'+aid));assert.ok(rendered.text.includes(snapshot.objects[aid].name[lang]));}
   if(analytics.includes(id)){for(const p of obj.logic.paragraphs)assert.ok(rendered.text.includes(p[lang]));for(const field of obj.data_requirements.flatMap(x=>x.required_fields))assert.ok(rendered.text.includes(field));for(const p of [...obj.false_positives,...obj.blind_spots])assert.ok(rendered.text.includes(p[lang]));for(const p of obj.tuning_guidance.paragraphs)assert.ok(rendered.text.includes(p[lang]));}
   if(mitigations.includes(id))for(const a of obj.applications){assert.ok(rendered.text.includes(a.target_ref));for(const f of ['use','expected_effect','limitations'])assert.ok(rendered.text.includes(a[f].paragraphs[0][lang]));}
   report.pages.push({id,lang,title:rendered.title,sections:rendered.sections,characters:rendered.text.length});
   if(id===parent.id||id===subjects[1]){
    await evaluate('window.scrollTo(0,0)');const shot=await call('Page.captureScreenshot',{format:'png'});await writeFile(join(out,`${id}-${lang}.png`),Buffer.from(shot.data,'base64'));
    for(const section of ['mechanisms','detections']){await evaluate(`document.getElementById('${section}').scrollIntoView({behavior:'instant',block:'start'})`);await until(`(()=>{const top=document.getElementById('${section}').getBoundingClientRect().top;return top>=-1&&top<200})()`);const detail=await call('Page.captureScreenshot',{format:'png'});await writeFile(join(out,`${id}-${lang}-${section}.png`),Buffer.from(detail.data,'base64'));}
   }
  }
 }
 const catalog=snapshot.tactics.find(x=>x.id==='TA0007');
 assert.ok(catalog.technique_ids.includes(parent.id));
 for(const lang of ['zh','en']){
  await evaluate(`document.querySelector('[data-lang="${lang}"]').click()`);
  await evaluate("location.hash='#/object/TA0007'");
  const name=lang==='zh'?'环境测绘':'Discovery';
  await until(`document.querySelector('h1')?.textContent.includes('${name}')`);
  const links=await evaluate("[...document.querySelectorAll('main a[href^=\"#/object/\"]')].map(x=>x.getAttribute('href'))");
  for(const id of catalog.technique_ids)assert.ok(links.includes('#/object/'+id));
  report.pages.push({id:'TA0007',lang,techniques:catalog.technique_ids.length});
 }
 assert.deepEqual(report.browser_errors,[]);report.status='passed';
 await writeFile(join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({status:report.status,pages:report.pages.length,api_issues:report.api_issues.length,browser_errors:report.browser_errors.length,output:out}));
}finally{ws?.close();chrome.kill('SIGTERM');await new Promise(done=>{if(chrome.exitCode!==null)done();else chrome.once('exit',done)});await new Promise(done=>server.close(done));await rm(profile,{recursive:true,force:true,maxRetries:10,retryDelay:100});}
