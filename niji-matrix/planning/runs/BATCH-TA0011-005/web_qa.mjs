import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const BASE = "http://127.0.0.1:19081";
const DEBUG = "http://127.0.0.1:19222";
const IDS = [
  "NJT-0221", "NJT-0222", "NJS-0222-001", "NJS-0222-002", "NJS-0222-003",
  "NJT-0223", "NJS-0223-001", "NJS-0223-002", "NJS-0223-003",
  "NJT-0052", "NJS-0052-001", "NJS-0052-002", "NJS-0052-003",
  "NJT-0224", "NJS-0224-001", "NJS-0224-002",
  ...Array.from({ length: 6 }, (_, i) => `DET-${String(257 + i).padStart(6, "0")}`),
  ...Array.from({ length: 9 }, (_, i) => `NJA-${String(343 + i).padStart(6, "0")}`),
  ...Array.from({ length: 5 }, (_, i) => `MIT-${String(227 + i).padStart(6, "0")}`),
];

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const profile = await mkdtemp(path.join(os.tmpdir(), "niji-ta0011-web-qa-"));
const chrome = spawn("google-chrome", [
  "--headless", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--disable-background-networking",
  `--user-data-dir=${profile}`, "--remote-debugging-port=19222", "about:blank",
], { stdio: "ignore" });

let socket;
try {
  let tabs;
  for (let i = 0; i < 100; i += 1) {
    try {
      tabs = await fetch(`${DEBUG}/json/list`).then((response) => response.json());
      if (tabs.some((tab) => tab.type === "page")) break;
    } catch { /* Chrome is still starting. */ }
    await delay(100);
  }
  assert.ok(tabs?.some((tab) => tab.type === "page"), "headless Chrome did not start");
  const tab = tabs.find((item) => item.type === "page");
  socket = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener("open", resolve, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });
  let sequence = 0;
  const pending = new Map();
  socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (!message.id || !pending.has(message.id)) return;
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message)); else resolve(message.result);
  });
  function call(method, params = {}) {
    const id = ++sequence;
    return new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
      socket.send(JSON.stringify({ id, method, params }));
    });
  }
  async function evaluate(expression) {
    const response = await call("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
    if (response.exceptionDetails) throw new Error(response.exceptionDetails.text);
    return response.result.value;
  }
  async function waitFor(predicate, label) {
    for (let i = 0; i < 100; i += 1) {
      const value = await evaluate(predicate);
      if (value) return value;
      await delay(50);
    }
    throw new Error(`Timed out waiting for ${label}`);
  }
  await call("Page.enable");
  await call("Runtime.enable");
  await call("Page.navigate", { url: `${BASE}/#/object/NJT-0221` });
  await waitFor("document.title.includes('端口预期语义错配')", "initial matrix render");
  const data = await fetch(`${BASE}/api/data`).then((response) => response.json());
  assert.deepEqual(data.issues, []);
  let pages = 0;
  let sectionChecks = 0;
  for (const lang of ["zh", "en"]) {
    await evaluate(`document.querySelector('[data-lang="${lang}"]').click(); true`);
    await evaluate(`location.hash = '#/object/NJT-0221'; true`);
    await waitFor(`document.documentElement.lang.startsWith(${JSON.stringify(lang)}) && document.title.includes(${JSON.stringify(data.objects["NJT-0221"].name[lang])})`, `${lang} render`);
    for (const id of IDS) {
      const name = data.objects[id].name[lang];
      await evaluate(`location.hash = '#/object/${id}'; true`);
      await waitFor(`document.title.includes(${JSON.stringify(name)}) && document.querySelector('article')?.textContent.includes(${JSON.stringify(id)})`, `${lang} ${id}`);
      const view = await evaluate(`(() => ({
        lang: document.documentElement.lang,
        title: document.title,
        toc: Array.from(document.querySelectorAll('.toc a')).map((a) => a.getAttribute('href')),
        links: Array.from(document.querySelectorAll('article a[href^="#/object/"]')).map((a) => a.getAttribute('href')),
        raw: Array.from(document.querySelectorAll('article pre')).some((node) => node.textContent.includes(${JSON.stringify(id)})),
        text: document.querySelector('article')?.textContent || ''
      }))()`);
      assert.ok(view.lang.startsWith(lang), `${id} language mismatch`);
      assert.ok(view.title.includes(name), `${id} title mismatch`);
      assert.ok(view.raw, `${id} raw YAML missing`);
      assert.ok(view.toc.length >= 3, `${id} contents missing`);
      if (id.startsWith("NJT-") || id.startsWith("NJS-")) {
        for (const section of ["definition", "stealth-characteristics", "scope", "context", "mechanisms", "detections", "mitigations", "limitations", "source"]) {
          assert.ok(view.toc.some((href) => href?.endsWith(`/${section}`)), `${id} missing ${section}`);
          sectionChecks += 1;
        }
        assert.ok(view.links.some((href) => href?.includes("DET-")), `${id} Detection Strategy link missing`);
        assert.ok(view.links.some((href) => href?.includes("MIT-")), `${id} Mitigation link missing`);
        sectionChecks += 2;
      } else if (id.startsWith("DET-")) {
        assert.ok(view.links.some((href) => href?.includes("NJA-")), `${id} Analytic expansion link missing`);
        sectionChecks += 1;
      } else if (id.startsWith("MIT-")) {
        assert.ok(view.toc.some((href) => href?.endsWith("/details")), `${id} mitigation details section missing`);
        assert.ok(view.text.includes(lang === "zh" ? "技术应用" : "Technique applications"), `${id} applications table missing`);
        sectionChecks += 1;
      }
      pages += 1;
    }
  }
  assert.equal(pages, IDS.length * 2);
  console.log(JSON.stringify({ pages, section_and_link_checks: sectionChecks, api_issues: data.issues.length, languages: ["zh", "en"] }));
} finally {
  socket?.close();
  chrome.kill("SIGTERM");
}
