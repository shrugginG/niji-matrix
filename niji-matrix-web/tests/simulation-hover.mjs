import {chromium,expect} from '@playwright/test';import assert from 'node:assert/strict';
const b=await chromium.launch({channel:'chromium'});
try{
 const p=await b.newPage({viewport:{width:1626,height:1000}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto('http://127.0.0.1:18091/simulation/preset/nwpu-nsa-report');await expect(p.locator('.react-flow__node')).toHaveCount(87);
 await p.getByRole('button',{name:'图层',exact:true}).click();await p.locator('.sim-layer-list button').filter({hasText:'酸狐狸 Foxacid'}).click();
 await p.locator('.react-flow__node[data-id="foxacid"] .sim-entity-title').hover();await expect(p.getByRole('tooltip')).toContainText('NJS-0053-002');await expect(p.getByRole('tooltip')).toContainText('漏洞适配客户端选择性交付');await expect(p.getByRole('tooltip')).toContainText('所属技术');await expect(p.getByRole('tooltip')).toContainText('场景应用');
 await p.screenshot({path:'.playwright/hover-node.png'});await p.mouse.move(100,100);await expect(p.getByRole('tooltip')).toHaveCount(0);
 await p.getByLabel('场景视图',{exact:true}).selectOption('boundary');
 const path=p.locator('.react-flow__edge[data-id="island-gateway"] .react-flow__edge-path');const point=await path.evaluate(el=>{const point=el.getPointAtLength(el.getTotalLength()*.7);const p=new DOMPoint(point.x,point.y).matrixTransform(el.getScreenCTM());return{x:p.x,y:p.y};});await p.mouse.move(point.x,point.y);await expect(p.getByRole('tooltip')).toContainText('NJT-0054');await expect(p.getByRole('tooltip')).toContainText('NJT-0130');await expect(p.locator('.sim-tech-hover-card')).toHaveCount(2);await p.screenshot({path:'.playwright/hover-edge.png'});
 const box=await p.getByRole('tooltip').boundingBox();assert.ok(box.x>=0&&box.y>=0&&box.x+box.width<=1626&&box.y+box.height<=1000);
 await p.keyboard.press('Escape');await expect(p.getByRole('tooltip')).toHaveCount(0);
 await p.getByLabel('场景视图',{exact:true}).selectOption('organization');await p.locator('.react-flow__node[data-id="tao"] .sim-entity-title').hover();await expect(p.getByRole('tooltip')).toHaveCount(0);
 assert.deepEqual(errors,[]);console.log('PASS: node and multi-tech edge hover, names/summaries/parent/application, immediate leave, Escape, viewport containment, no popup for unbound nodes');
}finally{await b.close();}
