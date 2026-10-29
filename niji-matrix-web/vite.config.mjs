import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { spawn } from "node:child_process";
import { resolve } from "node:path";
import { readFile } from "node:fs/promises";
const root = resolve(process.env.NIJI_MATRIX_ROOT || "../niji-matrix");
function liveContent() {
  return {
    name: "niji-live-content",
    async configureServer(server) {
      let running = false,
        pending = false,
        timer,
        child,
        closed = false;
      function rebuild() {
        if (closed) return Promise.resolve();
        if (running) {
          pending = true;
          return Promise.resolve();
        }
        running = true;
        return new Promise((done) => {
          child = spawn(
            process.env.PYTHON || "python3",
            ["scripts/export.py"],
            { stdio: "inherit" },
          );
          child.on("error", (error) => {
            console.error(error);
            running = false;
            done();
          });
          child.on("exit", () => {
            running = false;
            server.ws.send({ type: "custom", event: "niji-content" });
            done();
            if (pending) {
              pending = false;
              rebuild();
            }
          });
        });
      }
      // Watch only the canonical inputs, never generated files or unrelated research files.
      const locations = [
        "matrix.yaml",
        "matrix",
        "mechanisms",
        "references",
        "claims",
        "cases",
        "detections",
        "analytics",
        "mitigations",
        "relationships",
        "schemas",
        "scripts",
      ];
      const paths = locations.map((x) => resolve(root, x));
      server.watcher.add(paths);
      const changed = (path) => {
        if (paths.some((p) => path === p || path.startsWith(p + "/"))) {
          clearTimeout(timer);
          timer = setTimeout(rebuild, 350);
        }
      };
      server.watcher.on("all", (_, path) => changed(path));
      server.httpServer?.once("close", () => {
        closed = true;
        clearTimeout(timer);
        child?.kill();
      });
      // New snapshots are created after Vite initializes its public-file cache.
      // Serve this narrow JSON namespace directly, including a real JSON 404.
      server.middlewares.use("/data/", async (req, res) => {
        res.setHeader("Cache-Control", "no-store");
        res.setHeader("Content-Type", "application/json; charset=utf-8");
        res.setHeader("X-Content-Type-Options", "nosniff");
        const path = (req.url || "").split("?")[0];
        if (!/^\/(?:status\.json|[a-f0-9]{16}\/(?:index\.json|objects\/[A-Za-z0-9-]+\.json))$/.test(path)) {
          res.statusCode = 404;
          res.end(JSON.stringify({ error: "Data not found" }));
          return;
        }
        try {
          const body = await readFile(resolve(server.config.publicDir, "data", path.slice(1)));
          res.end(req.method === "HEAD" ? undefined : body);
        } catch {
          res.statusCode = 404;
          res.end(JSON.stringify({ error: "Data not found" }));
        }
      });
      await rebuild();
    },
  };
}
export default defineConfig({
  base: process.env.VITE_BASE_PATH || "/",
  publicDir: process.env.NIJI_PUBLIC_DIR || "public",
  plugins: [react(), liveContent()],
  server: { watch: { ignored: ["**/public/data/**"] } },
});
