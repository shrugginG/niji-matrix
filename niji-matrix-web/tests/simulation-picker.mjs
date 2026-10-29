import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
const browser=await chromium.launch({channel:'chromium'});
try{
 const page=await browser.newPage({viewport:{width:1626,height:1000}});
 await page.goto('http://127.0.0.1:18091/simulation');await page.getByRole('button',{name:'添加PC',exact:true}).click();await page.getByRole('button',{name:'添加技术 / 子技术',exact:true}).click();
 await expect(page.locator('.sim-tactic-card')).toHaveCount(15);await expect(page.locator('.sim-tech-option')).toHaveCount(0);await page.locator('.sim-picker').screenshot({path:'.playwright/picker-tactics-home.png'});
 const tactic=id=>page.locator('.sim-tactic-card').filter({has:page.locator(`[data-tactic="${id}"]`)});
 await tactic('TA0043').click();const parent=page.locator('.sim-tech-parent').filter({hasText:'NJT-0001'});await parent.getByRole('button').click();const child=page.locator('.sim-tech-option').filter({hasText:'NJS-0001-001'});await child.getByRole('checkbox').check();await expect(parent.getByRole('checkbox')).not.toBeChecked();
 await page.getByRole('button',{name:'全部战术',exact:true}).click();await expect(tactic('TA0043')).toContainText('已选 1');await tactic('TA0042').click();await page.locator('.sim-tech-parent').first().getByRole('checkbox').check();await expect(page.getByText('已选择 2 项',{exact:true})).toBeVisible();
 await page.getByRole('button',{name:'全部战术',exact:true}).click();await tactic('TA0043').click();await expect(child.getByRole('checkbox')).toBeChecked();await page.locator('.sim-picker').screenshot({path:'.playwright/picker-tactic-techniques.png'});
 await page.getByRole('button',{name:'全部战术',exact:true}).click();await page.getByLabel('搜索技术或子技术').fill('NJS-0001-001');await expect(page.locator('.sim-tech-option.is-child')).toHaveCount(1);await expect(child.getByRole('checkbox')).toBeChecked();await page.getByRole('button',{name:'应用所选',exact:true}).click();await expect(page.locator('.sim-bound-item')).toHaveCount(2);
 await page.getByRole('button',{name:'添加技术 / 子技术',exact:true}).click();await expect(page.locator('.sim-tactic-card')).toHaveCount(15);await expect(page.getByText('已选择 2 项',{exact:true})).toBeVisible();await page.getByLabel('搜索技术或子技术').fill('NJS-0001-001');await child.getByRole('checkbox').uncheck();await page.getByRole('button',{name:'取消',exact:true}).click();await expect(page.locator('.sim-bound-item')).toHaveCount(2);
 await page.setViewportSize({width:390,height:844});await page.getByRole('button',{name:'添加技术 / 子技术',exact:true}).click();await expect(page.locator('.sim-tactic-card')).toHaveCount(15);assert.ok(await page.locator('.sim-picker').evaluate(el=>el.scrollWidth<=el.clientWidth));await page.locator('.sim-picker').screenshot({path:'.playwright/picker-tactics-mobile.png'});
 console.log('PASS: 15-tactic homepage, drilldown, independent parent/child selection, cross-tactic persistence, global search, apply/reopen, cancel and mobile');
}finally{await browser.close();}
