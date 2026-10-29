import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
const base=(process.env.PAGES_TEST_URL||'http://127.0.0.1:18093/niji-matrix/').replace(/\/?$/,'/');
const browser=await chromium.launch({channel:'chromium'});
try{
 const page=await browser.newPage({viewport:{width:1626,height:1000}});const errors=[],bad=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().includes('favicon'))bad.push(`${r.status()} ${r.url()}`);});
 await page.goto(`${base}#/matrix`);await expect(page.getByRole('heading',{name:'匿迹技战术矩阵',exact:true})).toBeVisible();await expect(page.locator('.tactic-heading')).toHaveCount(15);
 await page.goto(`${base}#/objects/NJT-0001`);await expect(page.getByRole('heading',{name:'主动扫描',exact:true})).toBeVisible();
 await page.locator('.outline').getByRole('link',{name:'匿迹机理',exact:true}).click();await expect(page).toHaveURL(/#\/objects\/NJT-0001#stealth_mechanisms$/);await expect(page.locator('#stealth_mechanisms')).toBeInViewport();
 await page.locator('.mechanism-jump').first().click();await expect(page).toHaveURL(/#\/objects\/NJT-0001#mechanism-/);await page.reload();await expect(page.locator('.mechanism-card').first()).toBeInViewport();
 await page.goto(`${base}#/simulation`);await expect(page.getByText('从一张白板开始')).toBeVisible();await page.getByRole('button',{name:'添加PC',exact:true}).click();await page.getByLabel('对象名称',{exact:true}).fill('Pages 测试终端');await page.getByRole('button',{name:'保存',exact:true}).click();await expect(page.getByText('已保存到本机浏览器',{exact:true})).toBeVisible();await page.reload();await expect(page.locator('.sim-entity-title')).toContainText('Pages 测试终端');
 await page.goto(`${base}#/simulation/preset/nwpu-nsa-report`);await expect(page.locator('.react-flow__node')).toHaveCount(87);await expect(page).toHaveURL(/#\/simulation\/draft\/scene-/);
 await page.getByRole('button',{name:'图层',exact:true}).click();await page.locator('.sim-layer-list button').filter({hasText:'“吐司面包”'}).click();
 const href=await page.locator('.sim-provenance a').filter({hasText:'原图'}).first().getAttribute('href');const material=new URL(href,base);assert.ok(material.pathname.startsWith(new URL(base).pathname+'case-assets/'));const response=await page.request.get(material.href);assert.equal(response.status(),200);assert.match(response.headers()['content-type'],/image\/png/);
 assert.deepEqual(errors,[]);assert.deepEqual(bad,[]);
 console.log(`PASS: ${base} matrix, details, section hashes, reload, canvas draft persistence, case and prefixed material links`);
}finally{await browser.close();}
