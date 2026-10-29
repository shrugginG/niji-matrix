import { chromium, expect } from "@playwright/test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
const base = process.env.NIJI_TEST_BASE_URL || "http://127.0.0.1:18091";
const browser = await chromium.launch({ channel: "chromium" });
try {
  const context = await browser.newContext({
    viewport: { width: 1626, height: 1000 },
    acceptDownloads: true,
  });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(`${base}/simulation`);
  await expect(page.getByText("从一张白板开始")).toBeVisible();
  await expect(page.locator(".react-flow__node")).toHaveCount(0);
  await page.getByLabel("场景名称", { exact: true }).fill("画布往返验收");
  await page.getByRole("button", { name: "添加PC", exact: true }).click();
  await page.getByLabel("对象名称", { exact: true }).fill("工作站");
  await page
    .getByLabel("对象备注", { exact: true })
    .fill("实体备注应在保存后保留");
  await page
    .getByRole("button", { name: "添加服务器", exact: true })
    .dragTo(page.locator(".sim-canvas"), {
      targetPosition: { x: 300, y: 180 },
    });
  await expect(page.locator(".react-flow__node")).toHaveCount(2);
  await page.getByLabel("对象名称", { exact: true }).fill("目标服务器");
  const station = page
    .locator(".react-flow__node")
    .filter({
      has: page.locator(".sim-entity-title strong", { hasText: "工作站" }),
    });
  const server = page
    .locator(".react-flow__node")
    .filter({
      has: page.locator(".sim-entity-title strong", { hasText: "目标服务器" }),
    });
  const source = await station.locator('[data-handleid="left"]').boundingBox();
  const target = await server.locator('[data-handleid="right"]').boundingBox();
  await page.mouse.move(
    source.x + source.width / 2,
    source.y + source.height / 2,
  );
  await page.mouse.down();
  await page.mouse.move(
    target.x + target.width / 2,
    target.y + target.height / 2,
    { steps: 15 },
  );
  await page.mouse.up();
  await expect(page.locator(".react-flow__edge")).toHaveCount(1);
  await page.getByLabel("对象名称", { exact: true }).fill("测试控制链路");
  await page.getByLabel("线型", { exact: true }).selectOption("dotted");
  await page.getByLabel("方向", { exact: true }).selectOption("both");
  await page
    .getByRole("button", { name: "添加技术 / 子技术", exact: true })
    .click();
  await page.getByLabel("搜索技术或子技术").fill("NJS-0001-001");
  await page
    .locator(".sim-tech-option")
    .filter({ hasText: "NJS-0001-001" })
    .getByRole("checkbox")
    .check();
  await page.getByRole("button", { name: "应用所选" }).click();
  await expect(page.locator(".sim-bound-item")).toHaveCount(1);
  await page.getByLabel("NJS-0001-001 应用说明").fill("连线上的机理关联");
  await station.locator(".sim-entity-title").click();
  await page
    .getByRole("button", { name: "添加技术 / 子技术", exact: true })
    .click();
  await page.getByLabel("搜索技术或子技术").fill("NJT-0001");
  await page
    .locator(".sim-tech-parent .sim-tech-option")
    .filter({ hasText: "NJT-0001" })
    .getByRole("checkbox")
    .check();
  await page.getByRole("button", { name: "应用所选" }).click();
  await expect(page.locator(".sim-bound-item")).toHaveCount(1);
  await page.getByRole("button", { name: "删除选中对象", exact: true }).click();
  await expect(page.locator(".react-flow__node")).toHaveCount(1);
  await expect(page.locator(".react-flow__edge")).toHaveCount(0);
  await page.getByRole("button", { name: "撤销", exact: true }).click();
  await expect(page.locator(".react-flow__node")).toHaveCount(2);
  await expect(page.locator(".react-flow__edge")).toHaveCount(1);
  await page.getByRole("button", { name: "保存", exact: true }).click();
  await expect(
    page.getByText("已保存到本机浏览器", { exact: true }),
  ).toBeVisible();
  const download = page.waitForEvent("download");
  await page.getByRole("button", { name: "导出", exact: true }).click();
  const downloaded = await download;
  const exported = JSON.parse(await readFile(await downloaded.path(), "utf8"));
  assert.equal(exported.nodes.length, 2);
  assert.equal(exported.edges.length, 1);
  assert.equal(exported.bindings.length, 2);
  assert.equal(exported.edges[0].lineStyle, "dotted");
  assert.equal(exported.edges[0].direction, "both");
  assert.equal(
    exported.nodes.find((n) => n.name === "工作站").notes,
    "实体备注应在保存后保留",
  );
  await page.reload();
  await expect(page.locator(".react-flow__node")).toHaveCount(2);
  await expect(page.getByLabel("场景名称", { exact: true })).toHaveValue(
    "画布往返验收",
  );
  await page.getByRole("button", { name: "新建", exact: true }).click();
  await expect(page.locator(".react-flow__node")).toHaveCount(0);
  await page
    .getByLabel("导入场景文件", { exact: true })
    .setInputFiles({
      name: "roundtrip.niji-scene.json",
      mimeType: "application/json",
      buffer: Buffer.from(JSON.stringify(exported)),
    });
  await expect(page.locator(".react-flow__node")).toHaveCount(2);
  await expect(page.locator(".react-flow__edge")).toHaveCount(1);
  const invalid = structuredClone(exported);
  invalid.edges[0].target = "missing";
  await page
    .getByLabel("导入场景文件", { exact: true })
    .setInputFiles({
      name: "bad.json",
      mimeType: "application/json",
      buffer: Buffer.from(JSON.stringify(invalid)),
    });
  await expect(page.getByRole("alert")).toContainText("连线端点不存在");
  await expect(page.locator(".react-flow__node")).toHaveCount(2);
  await page.getByRole("button", { name: "关闭错误提示" }).click();
  await page
    .locator(".sim-catalog")
    .filter({ hasText: "典型案例" })
    .locator("summary")
    .hover();
  await page.getByRole("button", { name: /Sality 隐蔽扫描/ }).click();
  await expect(page).toHaveURL(/simulation\/draft\/scene-/);
  await expect(page.locator(".react-flow__node")).toHaveCount(4);
  await expect(page.locator(".react-flow__edge")).toHaveCount(4);
  await expect(page.locator(".sim-scene-overview")).toContainText("Sality 隐蔽扫描");
  await page
    .getByLabel("场景名称", { exact: true })
    .fill("Sality 案例编辑副本");
  await page.getByRole("button", { name: "保存", exact: true }).click();
  await expect(
    page.getByText("已保存到本机浏览器", { exact: true }),
  ).toBeVisible();
  await page.reload();
  await expect(page.getByLabel("场景名称", { exact: true })).toHaveValue(
    "Sality 案例编辑副本",
  );
  await expect(page.locator(".react-flow__node")).toHaveCount(4);
  await page.getByRole("button", { name: "草稿", exact: true }).click();
  await expect(page.getByRole("dialog", { name: "本地草稿" })).toBeVisible();
  await page.getByRole("button", { name: "关闭草稿列表" }).click();
  await page.screenshot({ path: ".playwright/simulation-sality.png" });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  );
  await page.screenshot({ path: ".playwright/simulation-mobile.png" });
  assert.deepEqual(errors, []);
  console.log(
    "PASS: blank canvas, palette drag/drop, connection, node/edge bindings, properties, delete/undo, autosave/reload, JSON roundtrip, invalid import preservation, preset menu, drafts, mobile; no browser errors",
  );
} finally {
  await browser.close();
}
