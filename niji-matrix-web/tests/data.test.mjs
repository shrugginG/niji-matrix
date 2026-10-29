import test from "node:test";
import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
const root = new URL("../public/data/", import.meta.url);
const load = async (path) =>
  JSON.parse(await readFile(new URL(path, root), "utf8"));
test("canonical hierarchy, sources, and references are preserved", async () => {
  const status = await load("status.json");
  assert.equal(status.ok, true);
  const index = await load(`${status.revision}/index.json`);
  assert.equal(index.matrix.tactic_refs.length, 15);
  const parent = index.objects["NJT-0001"];
  assert.equal(parent.children.length, 5);
  for (const id of parent.children) {
    assert.equal(index.objects[id].parent_ref, parent.id);
    assert.match(id, /^NJS-0001-\d{3}$/);
  }
  const objects = Object.values(index.objects);
  const files = await readdir(new URL(`${status.revision}/objects/`, root));
  assert.equal(files.length, objects.length);
  for (const o of objects) {
    const full = await load(`${status.revision}/objects/${o.id}.json`);
    assert.equal(full.id, o.id);
    assert.ok(full._source);
    assert.equal(full._source.includes("planning/"), false);
    for (const field of ["url", "archive_url", "source"]) {
      assert.deepEqual(o[field], full[field], `${o.id}: list must retain ${field}`);
    }
    for (const ref of full._reverse) assert.ok(index.objects[ref], ref);
  }
});
test("detail retains required research and defense fields", async () => {
  const { revision } = await load("status.json");
  const obj = await load(`${revision}/objects/NJT-0001.json`);
  for (const key of [
    "definition_and_concept",
    "stealth_characteristics",
    "scope_boundary_definition",
    "application_scenarios_and_threat_model",
    "stealth_mechanisms",
    "subtechnique_taxonomy",
    "defense",
    "evidence",
    "research",
  ])
    assert.ok(obj[key], key);
  for (const id of obj.defense.detections.strategy_refs) {
    const strategy = await load(`${revision}/objects/${id}.json`);
    for (const aid of strategy.analytic_refs) {
      const analytic = await load(`${revision}/objects/${aid}.json`);
      assert.ok(analytic.logic);
      assert.ok(analytic.blind_spots);
    }
  }
});
