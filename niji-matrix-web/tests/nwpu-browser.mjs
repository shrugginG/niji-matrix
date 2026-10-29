import {chromium,expect} from '@playwright/test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';
const b=await chromium.launch({channel:'chromium'});
try{
 const p=await b.newPage({viewport:{width:1700,height:1050},acceptDownloads:true});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto('http://127.0.0.1:18091/simulation');await p.locator('.sim-catalog').filter({hasText:'典型案例'}).locator('summary').hover();await p.getByRole('button',{name:/NSA 入侵西北工业大学/}).click();await expect(p).toHaveURL(/simulation\/draft\/scene-/);await expect(p.locator('.react-flow__node')).toHaveCount(87);await expect(p.locator('.react-flow__edge')).toHaveCount(99);
 await expect(p.locator('.sim-scene-views option')).toHaveCount(9);
 for(const view of ['organization','preparation','relays','foxacid','boundary','operations','office','tools'])await p.getByLabel('场景视图',{exact:true}).selectOption(view);
 await p.locator('.sim-scene-legend summary').click();await expect(p.locator('.sim-scene-legend')).toContainText('A1');
 await p.getByRole('button',{name:'图层',exact:true}).click();await p.locator('.sim-layer-list button').filter({hasText:'“精准外科医生”'}).click();await expect(p.locator('.sim-provenance')).toContainText('Linux');await expect(p.locator('.sim-provenance')).toContainText('报道陈述');
 const source=p.locator('.sim-provenance a').first();const response=await p.request.get(new URL(await source.getAttribute('href'),p.url()).href);assert.equal(response.status(),200);assert.match(response.headers()['content-type'],/image\/png/);
 await p.locator('.sim-layer-list button').filter({hasText:'A1 访问'}).click();await expect(p.locator('.sim-bound-item')).toContainText('NJT-0052');await expect(p.locator('.sim-provenance')).toContainText('原图');
 const download=p.waitForEvent('download');await p.getByRole('button',{name:'导出',exact:true}).click();const dl=await download;const scene=JSON.parse(await readFile(await dl.path(),'utf8'));assert.equal(scene.nodes.length,87);assert.equal(scene.edges.length,99);assert.equal(scene.bindings.length,48);assert.equal(scene.views.length,8);assert.equal(scene.sources.length,11);assert.ok(scene.edges.every(e=>e.provenance.length));assert.ok(scene.edges.some(e=>e.labelPosition));
 await p.getByLabel('导入场景文件',{exact:true}).setInputFiles({name:'nwpu-roundtrip.niji-scene.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(scene))});await expect(p.locator('.react-flow__node')).toHaveCount(87);await expect(p.getByLabel('场景名称',{exact:true})).toHaveValue(/导入/);
 await p.getByRole('button',{name:'保存',exact:true}).click();await expect(p.getByText('已保存到本机浏览器',{exact:true})).toBeVisible();await p.reload();await expect(p.locator('.react-flow__node')).toHaveCount(87);await expect(p.locator('.sim-scene-views option')).toHaveCount(9);
 const article=await p.request.get('http://127.0.0.1:18091/case-assets/nwpu/report.txt');assert.equal(article.status(),200);assert.match(await article.text(),/ABC_123/);
 await p.setViewportSize({width:390,height:844});assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
 console.log('PASS: catalog, 87 nodes/99 edges, eight views, legend, node/edge provenance, original figure/text links, bindings, full JSON roundtrip/reload and mobile');
}finally{await b.close();}
