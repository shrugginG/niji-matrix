import { chromium, expect } from "@playwright/test";
import assert from "node:assert/strict";
import { mkdir } from "node:fs/promises";

const base = "http://127.0.0.1:18091";
const browser = await chromium.launch({ channel: "chromium" });
try {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  // Verify real new-tab navigation without depending on third-party availability.
  await context.route(url => url.origin !== base, route => route.fulfill({
    contentType: "text/html", body: "<!doctype html><title>Original source</title>",
  }));
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", error => errors.push(error.message));
  const { revision } = await (await page.request.get(`${base}/data/status.json`)).json();
  const index = await (await page.request.get(`${base}/data/${revision}/index.json`)).json();
  const reference = index.objects["REF-000002"];
  assert.ok(reference.url, "source URLs must be exported in the index");

  async function opensSource(link, url, keyboard = false) {
    await expect(link).toHaveAttribute("href", url);
    await expect(link).toHaveAttribute("target", "_blank");
    await expect(link).toHaveAttribute("rel", "noopener noreferrer");
    await expect(link).toHaveAttribute("aria-label", /新标签页打开/);
    assert.ok((await link.getAttribute("title")).includes(url));
    const current = page.url();
    if (keyboard) await link.focus();
    const [popup] = await Promise.all([
      page.waitForEvent("popup"), keyboard ? link.press("Enter") : link.click(),
    ]);
    await popup.waitForLoadState("domcontentloaded");
    assert.equal(popup.url(), url);
    assert.equal(await popup.evaluate(() => window.opener), null);
    assert.equal(page.url(), current, "opening the source must preserve the current page");
    await popup.close();
  }

  await page.goto(`${base}/library/reference?q=REF-000002`);
  await expect(page.locator(".object-table-entry")).toHaveCount(1);
  await opensSource(page.locator(".object-table-entry .source-link"), reference.url);
  await page.locator(".object-row").click();
  await expect(page).toHaveURL(`${base}/objects/REF-000002`);
  await opensSource(page.locator(".detail-subtitle .source-link"), reference.url, true);
  await opensSource(page.locator("#url .source-link"), reference.url);

  const archived = Object.values(index.objects).find(o => o.archive_url && o.archive_url !== o.url);
  assert.ok(archived, "the real data includes archived sources");
  await page.goto(`${base}/objects/${archived.id}`);
  await opensSource(page.locator(".detail-subtitle .source-link").filter({ hasText: "查看存档" }), archived.archive_url);

  await page.goto(`${base}/objects/NJT-0001`);
  const referenceRows = page.locator('.evidence-group[aria-label="参考资料"] .related-row');
  await expect(referenceRows).toHaveCount(12);
  for (const row of await referenceRows.all()) {
    const id = await row.locator("code").textContent();
    await expect(row.locator(".source-link").first()).toHaveAttribute("href", index.objects[id].url);
  }
  await opensSource(referenceRows.filter({ hasText: "REF-000002" }).locator(".source-link"), reference.url);
  await page.locator(".mechanism-evidence summary").first().click();
  const mechanismSource = page.locator(".mechanism-evidence .source-link").first();
  await opensSource(mechanismSource, await mechanismSource.getAttribute("href"));
  const sidebarSource = page.locator(".related .source-link").first();
  await opensSource(sidebarSource, index.objects["TA0043"].source.url);
  await expect(sidebarSource.locator("svg")).toBeVisible();
  await mkdir(".playwright", { recursive: true });
  await page.locator('.evidence-group[aria-label="参考资料"]').screenshot({ path: ".playwright/source-links-evidence.png" });

  for (const id of ["CLM-000001", "CASE-000001"]) {
    await page.goto(`${base}/objects/${id}`);
    const link = page.locator("#evidence_refs .source-link").first();
    await expect(link).toBeVisible();
    await opensSource(link, await link.getAttribute("href"));
  }
  await page.goto(`${base}/objects/TA0043`);
  await opensSource(page.locator(".detail-subtitle .source-link"), index.objects["TA0043"].source.url);
  await page.goto(`${base}/search?q=REF-000002`);
  await opensSource(page.locator(".object-table-entry .source-link"), reference.url);

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${base}/library/reference`);
  await expect(page.locator(".object-row")).toHaveCount(50);
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.getByLabel("搜索当前知识库").fill("REF-000002");
  await opensSource(page.locator(".object-table-entry .source-link"), reference.url);
  await page.getByRole("button", { name: "EN", exact: true }).click();
  await expect(page.locator(".object-table-entry .source-link")).toHaveAttribute("aria-label", `查看原文：${reference.title_en}（新标签页打开）`);
  await page.screenshot({ path: ".playwright/source-links-mobile.png" });

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(`${base}/simulation`);
  await page.locator(".sim-catalog").filter({ hasText: "典型案例" }).locator("summary").hover();
  await page.getByRole("button", { name: /Sality 隐蔽扫描案例/ }).click();
  await expect(page).toHaveURL(/simulation\/draft\/scene-/);
  const sceneSource = page.locator(".sim-source").filter({ hasText: "僵尸网络 / 隐蔽扫描分析" });
  await opensSource(sceneSource.locator(".source-link"), index.objects["REF-000005"].url);
  await expect(sceneSource.locator('a[href="/objects/REF-000005"]')).toBeVisible();
  await page.locator(".sim-source-editor summary").click();
  const customSource = "https://example.org/original?version=2#evidence";
  await page.getByLabel("资料链接", { exact: true }).nth(1).fill(customSource);
  await opensSource(sceneSource.locator(".source-link"), customSource);
  await page.getByLabel("资料链接", { exact: true }).nth(1).fill("javascript:alert(1)");
  await opensSource(sceneSource.locator(".source-link"), index.objects["REF-000005"].url);
  assert.equal(await page.locator("a a").count(), 0, "source links must not be nested inside other links");
  assert.deepEqual(errors, []);
  console.log("PASS: references, archives, related evidence, search, tactics, simulation sources, keyboard and mobile open the original URL in a separate tab; no browser errors");
} finally {
  await browser.close();
}
