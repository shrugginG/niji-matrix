import {
  mkdtemp,
  cp,
  readFile,
  writeFile,
  rm,
  symlink,
  mkdir,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawn } from "node:child_process";
import assert from "node:assert/strict";
const dir = await mkdtemp(join(tmpdir(), "niji-watch-"));
let server;
try {
  const web = join(dir, "web"),
    matrix = join(dir, "niji-matrix");
  await mkdir(web);
  await cp(resolve("../niji-matrix"), matrix, {
    recursive: true,
    filter: (path) => !/(\/dist|\/planning|\/__pycache__)(\/|$)/.test(path),
  });
  for (const name of [
    "scripts",
    "vite.config.mjs",
    "package.json",
    "index.html",
  ])
    await cp(resolve(name), join(web, name), { recursive: true });
  await symlink(resolve("node_modules"), join(web, "node_modules"), "dir");
  const url = "http://127.0.0.1:18092/data/status.json";
  server = spawn(
    process.execPath,
    [
      resolve("node_modules/vite/bin/vite.js"),
      "--host",
      "127.0.0.1",
      "--port",
      "18092",
      "--strictPort",
    ],
    {
      cwd: web,
      env: { ...process.env, NIJI_MATRIX_ROOT: matrix },
      stdio: ["ignore", "pipe", "pipe"],
    },
  );
  let log = "";
  server.stdout.on("data", (d) => (log += d));
  server.stderr.on("data", (d) => (log += d));
  async function until(check) {
    const end = Date.now() + 120000;
    while (Date.now() < end) {
      if (server.exitCode !== null) throw new Error(log);
      try {
        const r = await fetch(url);
        const status = await r.json();
        if (check(status)) return status;
      } catch {}
      await new Promise((r) => setTimeout(r, 1000));
    }
    throw new Error("Watcher timeout: " + log);
  }
  const first = await until((s) => s.ok);
  const file = join(matrix, "matrix.yaml");
  const original = await readFile(file, "utf8");
  await writeFile(
    file,
    original.replace("name_zh: 匿迹技战术矩阵", "name_zh: 自动监听测试矩阵"),
  );
  const next = await until((s) => s.ok && s.revision !== first.revision);
  const data = await (
    await fetch(`http://127.0.0.1:18092/data/${next.revision}/index.json`)
  ).json();
  assert.equal(data.matrix.name_zh, "自动监听测试矩阵");
  console.log(
    "PASS: external YAML file edit triggers watcher, validation, and live snapshot publication",
  );
} finally {
  if (server && server.exitCode === null) {
    server.kill("SIGTERM");
    await new Promise((r) => server.once("exit", r));
  }
  await rm(dir, { recursive: true, force: true });
}
