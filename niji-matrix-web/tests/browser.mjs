import { chromium, expect } from "@playwright/test";
import assert from "node:assert/strict";
import { mkdir } from "node:fs/promises";
const browser = await chromium.launch({ headless: true, channel: "chromium" });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
const { revision } = await (await page.request.get("http://127.0.0.1:18091/data/status.json")).json();
const index = await (await page.request.get(`http://127.0.0.1:18091/data/${revision}/index.json`)).json();
const techniqueCount = Object.values(index.objects).filter(record => record.type === "technique").length;
await page.goto("http://127.0.0.1:18091");
await page
  .getByRole("heading", { name: "匿迹技战术矩阵", exact: true })
  .waitFor();
await page
  .getByRole("button", { name: "展开 主动扫描 的子技术", exact: true })
  .click();
await page
  .getByRole("link", { name: "时间稀释扫描 NJS-0001-001", exact: true })
  .waitFor();
await page.getByLabel("搜索矩阵", { exact: true }).fill("NJS-0001-001");
await expect(page.locator(".technique-card")).toHaveCount(1);
await page
  .getByRole("link", { name: "时间稀释扫描 NJS-0001-001", exact: true })
  .click();
await page
  .getByRole("heading", { name: "时间稀释扫描", exact: true })
  .waitFor();
await page.getByRole("heading", { name: "定义与概念", exact: true }).waitFor();
await page.goBack();
assert.equal(
  await page.getByLabel("搜索矩阵", { exact: true }).inputValue(),
  "NJS-0001-001",
);
await page.getByLabel("清空搜索", { exact: true }).click();
await expect(page.getByLabel("搜索矩阵", { exact: true })).toHaveValue("");
await page.getByRole("button", { name: "列表", exact: true }).click();
await expect(page.locator(".object-row")).toHaveCount(techniqueCount);
await page.getByRole("button", { name: "矩阵", exact: true }).click();
await mkdir(".playwright", { recursive: true });
await page.locator(".matrix-board").waitFor();
await page.screenshot({ path: ".playwright/matrix-desktop.png" });
await page.goto("http://127.0.0.1:18091/objects/NJT-0001");
await page.getByRole("heading", { name: "主动扫描", exact: true }).waitFor();
await page.getByRole("heading", { name: "定义与概念", exact: true }).waitFor();
await page.screenshot({ path: ".playwright/detail-desktop.png" });
const strategy = page.locator('article a[href^="/objects/DET-"]').first();
await strategy.click();
await page.getByRole("heading", { name: "检测分析", exact: true }).waitFor();
await page.locator('article a[href^="/objects/NJA-"]').first().click();
await page.getByRole("heading", { name: "检测逻辑", exact: true }).waitFor();
await page.getByRole("heading", { name: "误报", exact: true }).waitFor();
await page.getByRole("heading", { name: "盲区", exact: true }).waitFor();
await page.goto("http://127.0.0.1:18091/library/reference");
await page.getByLabel("搜索当前知识库").fill("REF-000002");
await page.locator(".object-row").first().click();
await page
  .getByRole("link", { name: /查看原文/ })
  .first()
  .waitFor();
await page.setViewportSize({ width: 390, height: 844 });
await page.goto("http://127.0.0.1:18091/matrix");
await page
  .getByRole("heading", { name: "匿迹技战术矩阵", exact: true })
  .waitFor();
assert.ok(
  await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
);
await page.screenshot({ path: ".playwright/matrix-mobile.png" });
await page.goto("http://127.0.0.1:18091/objects/NJT-0001");
await page.getByRole("heading", { name: "定义与概念", exact: true }).waitFor();
assert.ok(
  await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
);
await page.screenshot({ path: ".playwright/detail-mobile.png" });
await page.getByRole("button", { name: "EN", exact: true }).click();
await page
  .getByRole("heading", { name: "Active Scanning", exact: true })
  .waitFor();
await page.getByLabel("全局搜索", { exact: true }).fill("NJT-0001");
await page.getByRole("button", { name: "提交搜索", exact: true }).click();
await expect(page.locator(".object-row")).toHaveCount(1);
await page.goto("http://127.0.0.1:18091/matrix?mechanism=NM-BT");
await page.locator(".matrix-board").waitFor();
assert.ok((await page.locator(".technique-card").count()) < techniqueCount);
await page.goto("http://127.0.0.1:18091/objects/NOT-FOUND");
await page.getByRole("heading", { name: "未找到该对象" }).waitFor();
assert.deepEqual(errors, []);
await browser.close();
console.log(
  "PASS: matrix, child search, history, list, detail, strategy → analytic, references, mobile, 404; no browser errors",
);
