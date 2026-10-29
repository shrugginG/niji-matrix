import { chromium, expect } from "@playwright/test";
const browser = await chromium.launch({ headless: true, channel: "chromium" });
const page = await browser.newPage();
await page.goto("http://127.0.0.1:18091");
await page
  .getByRole("heading", { name: "匿迹技战术矩阵", exact: true })
  .waitFor();
await page.route("**/data/status.json", (route) =>
  route.fulfill({
    json: { ok: false, message: "自动化测试：内容 Schema 校验失败" },
  }),
);
await expect(page.getByRole("alert")).toContainText(
  "正在显示上次成功校验的版本",
  { timeout: 10000 },
);
await page.unroute("**/data/status.json");
await expect(page.getByRole("alert")).toHaveCount(0, { timeout: 10000 });
await browser.close();
console.log(
  "PASS: background sync failure is visible and recovery clears it automatically",
);
