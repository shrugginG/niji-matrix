import {mkdtemp,cp,readdir,rm,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
const root=resolve(import.meta.dirname,'..');
const temp=await mkdtemp(join(tmpdir(),'niji-pages-'));
const publicDir=join(temp,'public');
const base=process.env.VITE_BASE_PATH || '/niji-matrix/';
const env={...process.env,VITE_BASE_PATH:base,VITE_ROUTER_MODE:'hash',NIJI_PUBLIC_DIR:publicDir,NIJI_DATA_OUT:join(publicDir,'data')};
function run(command,args){const r=spawnSync(command,args,{cwd:root,env,stdio:'inherit'});if(r.error)throw r.error;if(r.status!==0)throw new Error(`${command} failed (${r.status})`);}
try{
 for(const item of await readdir(join(root,'public'),{withFileTypes:true})){
  if(item.name!=='data')await cp(join(root,'public',item.name),join(publicDir,item.name),{recursive:true});
 }
 run(process.env.PYTHON || 'python3',['scripts/export.py']);
 run(process.execPath,['node_modules/typescript/bin/tsc','--noEmit']);
 run(process.execPath,['node_modules/vite/bin/vite.js','build','--outDir','dist-pages']);
 await writeFile(join(root,'dist-pages','.nojekyll'),'');
 console.log(`Pages ready at base ${base}; only the current data snapshot was included.`);
}finally{await rm(temp,{recursive:true,force:true});}
