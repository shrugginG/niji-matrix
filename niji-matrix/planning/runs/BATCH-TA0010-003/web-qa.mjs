import { spawn } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const ids=[
  "NJT-0195","NJS-0195-001","NJS-0195-002","NJS-0195-003",
  "NJT-0196","NJS-0196-001","NJS-0196-002","NJT-0197",
  "DET-000226","DET-000227","DET-000228","DET-000229",
  "NJA-000281","NJA-000282","NJA-000283","NJA-000284","NJA-000285","NJA-000286",
  "MIT-000203","MIT-000204","MIT-000136","MIT-000156","MIT-000200"
];
const api=await (await fetch("http://127.0.0.1:18080/api/data")).json();
const objects=api.objects;
for(const id of ids) if(!objects[id]) throw new Error(`API missing ${id}`);
const profile=mkdtempSync("/tmp/niji-ta0010-b3-webqa-");
const chrome=spawn("/usr/bin/google-chrome",[
  "--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage","--disable-extensions","--no-first-run",
  "--remote-debugging-port=0","--remote-allow-origins=*",`--user-data-dir=${profile}`,"about:blank"
],{stdio:"ignore"});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let ws;let next=1;const pending=new Map();
async function command(method,params={}){
 const id=next++;return await new Promise((resolve,reject)=>{
  const timeout=setTimeout(()=>{pending.delete(id);reject(new Error(`CDP timeout ${method}`));},12000);
  pending.set(id,{resolve,reject,timeout});ws.send(JSON.stringify({id,method,params}));
 });
}
async function evaluate(expression){
 const r=await command("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true});
 if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result?.value;
}
const checks=[];
try{
 let port;
 for(let i=0;i<60;i++){try{port=Number(readFileSync(join(profile,"DevToolsActivePort"),"utf8").split("\n")[0]);break;}catch{}await sleep(100);}
 if(!port)throw new Error("Chrome CDP port unavailable");
 let pages;
 for(let i=0;i<60;i++){try{pages=await(await fetch(`http://127.0.0.1:${port}/json`)).json();if(pages.some(p=>p.type==="page"&&p.webSocketDebuggerUrl))break;}catch{}await sleep(100);}
 ws=new WebSocket(pages.find(p=>p.type==="page"&&p.webSocketDebuggerUrl).webSocketDebuggerUrl);
 await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(!pending.has(m.id))return;const p=pending.get(m.id);pending.delete(m.id);clearTimeout(p.timeout);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);};
 await command("Page.enable");await command("Runtime.enable");
 await command("Page.navigate",{url:"http://127.0.0.1:18080/"});await sleep(400);
 for(const lang of ["zh","en"]){
  await evaluate(`localStorage.setItem('niji-review-lang','${lang}')`);await command("Page.reload",{ignoreCache:true});await sleep(350);
  for(const id of ids){
   const o=objects[id];const expected=(o.name?.[lang]||o[`name_${lang}`]||id);
   await command("Page.navigate",{url:`http://127.0.0.1:18080/#/object/${id}`});
   let st;
   for(let i=0;i<70;i++){
    st=await evaluate(`(()=>({lang:document.documentElement.lang,title:document.querySelector('#content h1.page-title')?.firstChild?.textContent?.trim(),length:document.querySelector('#content')?.innerText?.length||0,sections:[...document.querySelectorAll('#content section[id]')].map(e=>e.id),text:document.querySelector('#content')?.innerText||''}))()`);
    if(st.title===expected&&st.length>220&&(lang==="zh"?st.lang==="zh-CN":st.lang==="en"))break;await sleep(100);
   }
   if(st.title!==expected)throw new Error(`${lang} ${id} title ${st.title}`);
   if(st.text.includes("对象不存在")||st.text.includes("Object not found"))throw new Error(`${lang} ${id} missing`);
   if(["technique","evasion-subtechnique"].includes(o.type)){
    for(const sec of ["definition","stealth-characteristics","scope","context","mechanisms","detections","mitigations","claims","references","limitations","source"])
     if(!st.sections.includes(sec))throw new Error(`${lang} ${id} missing section ${sec}`);
    if(o.type==="technique"&&!st.sections.includes("subtechniques"))throw new Error(`${lang} ${id} missing taxonomy`);
    for(const rid of [...(o.defense?.detections?.strategy_refs||[]),...(o.defense?.mitigations?.mitigation_refs||[]),...(o.evidence?.claim_refs||[])])
     if(!st.text.includes(rid))throw new Error(`${lang} ${id} missing linked ${rid}`);
   }
   if(o.type==="detection-strategy")for(const aid of o.analytic_refs||[])if(!st.text.includes(aid))throw new Error(`${lang} ${id} missing analytic ${aid}`);
   if(o.type==="detection-analytic"){
    for(const q of o.data_requirements||[])if(!st.text.includes(q.required_fields[0]))throw new Error(`${lang} ${id} missing data fields`);
   }
   if(o.type==="mitigation")for(const a of o.applications||[])if(!st.text.includes(a.target_ref))throw new Error(`${lang} ${id} missing application ${a.target_ref}`);
   checks.push({lang,id,type:o.type,characters:st.length,sections:st.sections.length});
  }
 }
 const tacticIssues=api.issues.filter(x=>x.path.includes("TA0010")||ids.some(id=>x.message.includes(id)));
 for(const lang of ["zh","en"]){
  await evaluate("localStorage.setItem('niji-review-lang','"+lang+"')");await command("Page.reload",{ignoreCache:true});await sleep(300);
  await evaluate("location.hash='#/object/TA0010'");let tacticText="";
  for(let i=0;i<50;i++){tacticText=await evaluate("document.querySelector('#content')?.innerText||''");if(tacticText.includes("NJT-0197"))break;await sleep(100);}
  for(const tacticId of ["NJT-0154","NJT-0155","NJT-0190","NJT-0191","NJT-0192","NJT-0193","NJT-0194","NJT-0195","NJT-0196","NJT-0197"])
   if(!tacticText.includes(tacticId))throw new Error(lang+" TA0010 missing "+tacticId);
 }
 writeFileSync("planning/runs/BATCH-TA0010-003/web-qa-result.json",JSON.stringify({status:"pass",api_issues:api.issues.length,ta0010_issues:tacticIssues,checks},null,2)+"\n");
 process.stdout.write(`Final-batch bilingual Review Web QA passed: ${checks.length} pages, ${ids.length} objects, two languages; TA0010 API issues ${tacticIssues.length}.\n`);
}catch(error){
 for(const lang of ["zh","en"]){
  await evaluate("localStorage.setItem('niji-review-lang','"+lang+"')");await command("Page.reload",{ignoreCache:true});await sleep(300);
  await evaluate("location.hash='#/object/TA0010'");let tacticText="";
  for(let i=0;i<50;i++){tacticText=await evaluate("document.querySelector('#content')?.innerText||''");if(tacticText.includes("NJT-0197"))break;await sleep(100);}
  for(const tacticId of ["NJT-0154","NJT-0155","NJT-0190","NJT-0191","NJT-0192","NJT-0193","NJT-0194","NJT-0195","NJT-0196","NJT-0197"])
   if(!tacticText.includes(tacticId))throw new Error(lang+" TA0010 missing "+tacticId);
 }
 writeFileSync("planning/runs/BATCH-TA0010-003/web-qa-result.json",JSON.stringify({status:"fail",error:String(error),checks},null,2)+"\n");
 process.stderr.write(String(error)+"\n");process.exitCode=1;
}finally{
 try{ws?.close();}catch{}chrome.kill("SIGTERM");await sleep(300);rmSync(profile,{recursive:true,force:true});
}
