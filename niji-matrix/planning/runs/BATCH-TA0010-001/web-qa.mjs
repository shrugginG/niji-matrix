import { spawn } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
const profile = mkdtempSync("/tmp/niji-ta0010-webqa-");
const chrome = spawn("/usr/bin/google-chrome", [
  "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
  "--no-first-run", "--disable-extensions", "--remote-debugging-port=0", "--remote-allow-origins=*",
  `--user-data-dir=${profile}`, "about:blank"
], {stdio:"ignore"});
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws;
let next = 1;
const pending = new Map();
async function command(method, params={}) {
  const id=next++;
  return await new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>{pending.delete(id);reject(new Error(`CDP timeout: ${method}`));},10000);
    pending.set(id,{resolve,reject,timeout});
    ws.send(JSON.stringify({id,method,params}));
  });
}
async function evaluate(expression) {
  const response=await command("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true});
  if (response.exceptionDetails) throw new Error(JSON.stringify(response.exceptionDetails));
  return response.result?.value;
}
const expected=[
  ["NJT-0154","外传规模约束","Exfiltration Volume Shaping","technique"],
  ["NJS-0154-001","单元限额切块外传","Per-Unit Capped Chunk Exfiltration","child"],
  ["NJS-0154-002","时间窗限额外传","Time-Window Capped Exfiltration","child"],
  ["NJT-0155","定时传输","Scheduled Transfer","technique"],
  ["NJS-0155-001","周期积压外传","Periodic Queued Exfiltration","child"],
  ["DET-000171","外传单元与长窗总量关联","Exfiltration Unit and Long-Horizon Volume Correlation","defense"],
  ["NJA-000186","重复小型上传的对象谱系关联","Repeated Small-Upload Object Lineage Correlation","defense"],
  ["NJA-000187","低峰值外传的长窗累计与进程核验","Low-Peak Exfiltration Long-Window Accumulation and Process Check","defense"],
  ["MIT-000156","受控出口与累计上传预算","Governed Egress and Cumulative Upload Budget","defense"],
  ["DET-000172","待发数据与周期出站关联","Queued Data and Periodic Egress Correlation","defense"],
  ["NJA-000188","待发—周期出站长窗关联","Queued-to-Periodic Egress Long-Window Correlation","defense"],
  ["MIT-000157","受管外传路径与周期作业授权","Managed Egress Paths and Periodic Job Authorization","defense"],
];
const checks=[];
try {
  let port;
  for(let i=0;i<50;i++){
    try {port=Number(readFileSync(join(profile,"DevToolsActivePort"),"utf8").split("\n")[0]);break;}catch{}
    await sleep(100);
  }
  if(!port) throw new Error("Chrome CDP port unavailable");
  let pages;
  for(let i=0;i<50;i++){
    try {pages=await (await fetch(`http://127.0.0.1:${port}/json`)).json();if(pages.some(p=>p.type==="page"&&p.webSocketDebuggerUrl)) break;}catch{}
    await sleep(100);
  }
  ws=new WebSocket(pages.find(p=>p.type==="page"&&p.webSocketDebuggerUrl).webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
  ws.onmessage=event=>{
    const msg=JSON.parse(event.data);
    if(!pending.has(msg.id)) return;
    const item=pending.get(msg.id);pending.delete(msg.id);clearTimeout(item.timeout);
    if(msg.error) item.reject(new Error(JSON.stringify(msg.error)));
    else item.resolve(msg.result);
  };
  await command("Page.enable");
  await command("Runtime.enable");
  await command("Page.navigate",{url:"http://127.0.0.1:18080/"});
  for(let i=0;i<50;i++){if(await evaluate("document.readyState === 'complete'"))break;await sleep(100);}
  for(const lang of ["zh","en"]){
    await evaluate(`localStorage.setItem('niji-review-lang', '${lang}')`);
    await command('Page.reload',{ignoreCache:true});
    await sleep(350);
    for(const [id,zh,en,kind] of expected){
      await command("Page.navigate",{url:`http://127.0.0.1:18080/#/object/${id}`});
      const name=lang==="zh"?zh:en;
      let state;
      for(let i=0;i<60;i++){
        state=await evaluate(`(()=>({lang:document.documentElement.lang,title:document.querySelector('#content h1.page-title')?.firstChild?.textContent?.trim(),length:document.querySelector('#content')?.innerText?.length||0,sections:[...document.querySelectorAll('#content section[id]')].map(e=>e.id),text:document.querySelector('#content')?.innerText||''}))()`);
        if(state.title===name && state.length>250 && (lang==="zh"?state.lang==="zh-CN":state.lang==="en"))break;
        await sleep(100);
      }
      if(state.title!==name) throw new Error(`${lang} ${id} title: ${state.title}; url=${await evaluate("location.href")}; text=${state.text.slice(0,300)}`);
      if(state.length<250) throw new Error(`${lang} ${id} empty body`);
      if(state.text.includes("对象不存在")||state.text.includes("Object not found")) throw new Error(`${lang} ${id} missing page`);
      if(kind==="technique"||kind==="child"){
        for(const section of ["definition","stealth-characteristics","scope","context","mechanisms","detections","mitigations","claims","references","limitations","source"])
          if(!state.sections.includes(section)) throw new Error(`${lang} ${id} missing ${section}`);
        if(kind==="technique" && !state.sections.includes("subtechniques")) throw new Error(`${lang} ${id} missing taxonomy`);
      }
      if(id==="DET-000171" && !state.text.includes("NJA-000186"))throw new Error(`${lang} ${id} missing analytic`);
      if(id==="DET-000172" && !state.text.includes("NJA-000188"))throw new Error(`${lang} ${id} missing analytic`);
      if(id==="MIT-000156" && !state.text.includes("NJS-0154-002"))throw new Error(`${lang} ${id} missing application`);
      if(id==="MIT-000157" && !state.text.includes("NJS-0155-001"))throw new Error(`${lang} ${id} missing application`);
      checks.push({lang,id,kind,characters:state.length,sections:state.sections.length});
    }
  }
  writeFileSync("planning/runs/BATCH-TA0010-001/web-qa-result.json",JSON.stringify({status:"pass",checks},null,2)+"\n");
  process.stdout.write(`Bilingual Review Web QA passed: ${checks.length} pages, ${expected.length} objects, two languages.\n`);
} catch(error) {
  writeFileSync("planning/runs/BATCH-TA0010-001/web-qa-result.json",JSON.stringify({status:"fail",error:String(error),checks},null,2)+"\n");
  process.stderr.write(String(error)+"\n");
  process.exitCode=1;
} finally {
  try{ws?.close();}catch{}
  chrome.kill("SIGTERM");
  await sleep(300);
  rmSync(profile,{recursive:true,force:true});
}
