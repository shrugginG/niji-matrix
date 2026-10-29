import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createRequire } from "node:module";
import { buildSync } from "esbuild";
const dir = mkdtempSync(join(tmpdir(), "niji-model-"));
buildSync({
  entryPoints: ["src/features/simulation/model.ts"],
  bundle: true,
  platform: "node",
  format: "cjs",
  outfile: join(dir, "model.cjs"),
  logLevel: "silent",
});
const { newId, parseScene, removeObjects, warnings, orderedNodes, naturalAnchors, updateAutomaticAnchors } = createRequire(
  import.meta.url,
)(join(dir, "model.cjs"));
process.on("exit", () => rmSync(dir, { recursive: true, force: true }));
const preset = () =>
  JSON.parse(
    readFileSync("scenes/threats/remote-access-trojan.niji-scene.json", "utf8"),
  );
test("presets round-trip with geometry, relations, references, and evidence", () => {
  for (const f of [
    "scenes/threats/remote-access-trojan.niji-scene.json",
    "scenes/cases/sality-scan.niji-scene.json",
  ]) {
    const scene = JSON.parse(readFileSync(f, "utf8"));
    assert.deepEqual(parseScene(JSON.parse(JSON.stringify(scene))), scene);
  }
});
test("rejects malformed graph references, hierarchy cycles, versions and unsafe URLs", () => {
  let s = preset();
  s.edges[0].target = "missing";
  assert.throws(() => parseScene(s), /端点/);
  s = preset();
  s.nodes[0].id = s.nodes[1].id;
  assert.throws(() => parseScene(s), /重复/);
  s = preset();
  s.nodes.find((n) => n.id === "provider").parentId = "provider";
  assert.throws(() => parseScene(s), /循环/);
  s = preset();
  s.schemaVersion = "2.0.0";
  assert.throws(() => parseScene(s), /格式/);
  s = preset();
  s.sources = [{ id: "src", title: "unsafe", url: "javascript:alert(1)" }];
  assert.throws(() => parseScene(s), /格式/);
  s = preset();
  s.bindings[0].target.id = "missing";
  assert.throws(() => parseScene(s), /目标/);
});
test("deleting a container removes descendants, attached edges and bindings", () => {
  const s = removeObjects(preset(), { kind: "node", id: "provider" });
  assert.ok(!s.nodes.some((n) => ["provider", "relay"].includes(n.id)));
  assert.ok(!s.edges.some((e) => e.source === "relay" || e.target === "relay"));
  assert.equal(s.bindings.length, 0);
  assert.doesNotThrow(() => parseScene(s));
});
test("missing or changed matrix content is retained with explicit warnings", () => {
  const s = preset();
  const ref = s.bindings[0].matrixRef;
  s.bindings[0].matrixRef = "NJT-9999";
  const valid = parseScene(s);
  assert.equal(valid.bindings[0].matrixRef, "NJT-9999");
  const messages = warnings(valid, { revision: "different", objects: {} });
  assert.ok(messages.some((m) => m.includes("快照")));
  assert.ok(messages.some((m) => m.includes("NJT-9999")));
  assert.ok(ref);
});
test("adapter orders parent containers before children without mutating source", () => {
  const s = preset();
  const reversed = [...s.nodes].reverse();
  const ordered = orderedNodes(reversed);
  for (const n of ordered)
    if (n.parentId)
      assert.ok(
        ordered.findIndex((p) => p.id === n.parentId) < ordered.indexOf(n),
      );
  assert.equal(reversed[0].id, s.nodes.at(-1).id);
});

test("natural ports face vertical, horizontal and nested targets", () => {
 const s=preset();const owner=s.edges.find(e=>e.id==='owner');
 assert.deepEqual(naturalAnchors(owner,s.nodes),{sourcePort:'bottom',targetPort:'top'});
 const net=s.edges.find(e=>e.id==='net');
 assert.deepEqual(naturalAnchors(net,s.nodes),{sourcePort:'right',targetPort:'left'});
 updateAutomaticAnchors(s,true);assert.equal(owner.anchorMode,'auto');assert.equal(owner.sourcePort,'bottom');
 owner.anchorMode='manual';owner.sourcePort='left';updateAutomaticAnchors(s);assert.equal(owner.sourcePort,'left');
 assert.doesNotThrow(()=>parseScene(s));
});

test("scene IDs support LAN HTTP without randomUUID and keep UUID v4 format",()=>{
 const descriptor=Object.getOwnPropertyDescriptor(globalThis.crypto,'randomUUID');
 Object.defineProperty(globalThis.crypto,'randomUUID',{value:undefined,configurable:true});
 try {
  const ids=new Set(Array.from({length:1000},()=>newId('node')));
  assert.equal(ids.size,1000);
  for(const id of ids)assert.match(id,/^node-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
 } finally {if(descriptor)Object.defineProperty(globalThis.crypto,'randomUUID',descriptor);else delete globalThis.crypto.randomUUID;}
});
