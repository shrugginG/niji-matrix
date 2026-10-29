import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const b=await chromium.launch({channel:'chromium'});
try{
 const p=await b.newPage({viewport:{width:1626,height:1000},acceptDownloads:true});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto('http://127.0.0.1:18091/simulation/preset/remote-access-trojan');await expect(p.locator('.react-flow__edge')).toHaveCount(5);
 await p.getByRole('button',{name:'图层',exact:true}).click();await p.locator('.sim-layer-list button').filter({hasText:'所属关系'}).click();
 await expect(p.getByLabel('起点锚点',{exact:true})).toHaveValue('bottom');await expect(p.getByLabel('终点锚点',{exact:true})).toHaveValue('top');
 async function dragEnd(id,end,node,port){const a=await p.locator(`.react-flow__edge[data-id="${id}"] .react-flow__edgeupdater-${end}`).boundingBox();assert.ok(a);const z=await p.locator(`.react-flow__node[data-id="${node}"] [data-handleid="${port}"]`).boundingBox();assert.ok(z);await p.mouse.move(a.x+a.width/2,a.y+a.height/2);await p.mouse.down();await p.mouse.move(z.x+z.width/2,z.y+z.height/2,{steps:20});await p.mouse.up();}
 await dragEnd('owner','target','client','left');await expect(p.getByLabel('终点锚点',{exact:true})).toHaveValue('left');
 await p.getByRole('button',{name:'撤销',exact:true}).click();await p.locator('.sim-layer-list button').filter({hasText:'所属关系'}).click();await expect(p.getByLabel('终点锚点',{exact:true})).toHaveValue('top');
 await p.locator('.sim-layer-list button').filter({hasText:'互联网'}).click();await expect(p.locator('.sim-bound-item')).toHaveCount(1);
 await dragEnd('net','target','server','top');await expect(p.locator('.sim-endpoints')).toContainText('业务服务器');await expect(p.getByLabel('终点锚点',{exact:true})).toHaveValue('top');await expect(p.locator('.sim-bound-item')).toHaveCount(1);
 await dragEnd('net','source','social','right');await expect(p.locator('.sim-endpoints')).toContainText('社交平台');
 const download=p.waitForEvent('download');await p.getByRole('button',{name:'导出',exact:true}).click();const file=await download;const s=JSON.parse(await readFile(await file.path(),'utf8'));const e=s.edges.find(e=>e.id==='net');assert.equal(e.target,'server');assert.equal(e.source,'social');assert.equal(e.targetPort,'top');assert.equal(e.anchorMode,'manual');assert.equal(s.bindings[0].target.id,'net');
 await p.getByRole('button',{name:'保存',exact:true}).click();await expect(p.getByText('已保存到本机浏览器',{exact:true})).toBeVisible();await p.reload();await p.getByRole('button',{name:'图层',exact:true}).click();await p.locator('.sim-layer-list button').filter({hasText:'互联网'}).click();await expect(p.getByLabel('终点锚点',{exact:true})).toHaveValue('top');await expect(p.locator('.sim-endpoints')).toContainText('业务服务器');
 await p.getByRole('button',{name:'自动优化锚点'}).click();await expect(p.getByText('当前随布局自动调整。',{exact:false})).toBeVisible();
 assert.deepEqual(errors,[]);console.log('PASS: legacy natural anchors, dragging both endpoints to new handles/nodes, undo, preserved binding, JSON persistence, reload, auto optimization');
}finally{await b.close();}
