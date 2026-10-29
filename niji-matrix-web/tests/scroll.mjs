import { chromium, expect } from '@playwright/test';
import assert from 'node:assert/strict';
const browser = await chromium.launch({channel:'chromium'});
try {
  const page = await browser.newPage({viewport:{width:1626,height:953}});
  await page.goto('http://127.0.0.1:18091/matrix');
  await page.locator('.technique-card').first().waitFor();
  const longColumn = page.locator('.tactic-column').filter({has:page.locator('.tactic-heading a[href="/objects/TA0005"]')});
  const shortColumn = page.locator('.tactic-column').filter({has:page.locator('.tactic-heading a[href="/objects/TA0042"]')});
  const before = await shortColumn.locator('.technique-card').first().boundingBox();
  const headingBefore = await longColumn.locator('.tactic-heading').boundingBox();
  const list = longColumn.locator('.techniques');
  await list.evaluate(el=>{el.scrollTop=el.scrollHeight;});
  await expect.poll(()=>list.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  const after = await shortColumn.locator('.technique-card').first().boundingBox();
  const headingAfter = await longColumn.locator('.tactic-heading').boundingBox();
  assert.equal(after.y,before.y,'Short column stays visible while the long one scrolls');
  assert.equal(headingAfter.y,headingBefore.y,'Tactic heading stays fixed');
  assert.equal(await shortColumn.locator('.techniques').evaluate(el=>el.scrollTop),0);
  assert.equal(await page.locator('.matrix-board').evaluate(el=>el.scrollTop),0);
  await expect(longColumn.locator('.technique-card').last()).toBeInViewport();
  await page.locator('.matrix-board').evaluate(el=>{el.scrollLeft=el.scrollWidth;});
  await expect(page.locator('.tactic-column').last()).toBeInViewport();
  await page.setViewportSize({width:390,height:844});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  console.log('PASS: independent column scrolling, retained short column, fixed headings, last-item access, horizontal scroll, mobile layout');
} finally { await browser.close(); }
